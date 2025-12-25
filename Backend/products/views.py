from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Avg, Count, Prefetch

from .models import ProductOption, FinancialProduct, Subscription
from users.models import FinancialProfile
from .serializers import ProductOptionSerializer, FinancialProductSerializer, FinancialProductDetailSerializer, SubscriptionSerializer, ProductOptionDetailSerializer, ShowOptionSerializer
from .filters import ProductFilter

from products.services.engine import recommend_products, save_recommendations
from .services.save_nodata import update_profile_by_survey_safe
from ai.services.recommendation_explainer import explain_recommendation 

from datetime import date
from dateutil.relativedelta import relativedelta
import traceback

"""
예/적금 상품 조회
"""
@api_view(['GET'])
def products(request):
    if request.method == 'GET':
        term = request.query_params.get('term')
        
        queryset = FinancialProduct.objects.all().distinct()

        if term:
            filtered_options = ProductOption.objects.filter(save_trm=term)
            queryset = queryset.prefetch_related(
                Prefetch('options', queryset=filtered_options)
            )
        else:
            queryset = queryset.prefetch_related('options')

        filterset = ProductFilter(request.GET, queryset=queryset)

        if filterset.is_valid():
            queryset = filterset.qs
        else:
            return Response(filterset.errors, status=400)

        serializer = FinancialProductSerializer(queryset, many=True)
        return Response(serializer.data)

# 상품 상세 정보 조회
@api_view(['GET','POST'])
def product_details(request, pk):
  if request.method == 'GET':
    deposit_product = FinancialProduct.objects.get(pk=pk)
    serializer = FinancialProductDetailSerializer(deposit_product)
    return Response(serializer.data)

# 상품 옵션 정보 조회
@api_view(['GET'])
def options(request):
  if request.method == 'GET':
    subscribed_option_ids = request.user.subscriptions.values_list('product_option_id', flat=True)

    subscribed_options = ProductOption.objects.filter(id__in=subscribed_option_ids).select_related('product')
    serializer = ProductOptionSerializer(subscribed_options, many=True)

    return Response(serializer.data)

"""
가입 정보 관리
"""  
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def subscriptions(request, subscription_id=None):
    # 1. POST: 상품 가입
    if request.method == 'POST':
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            option = serializer.validated_data['product_option']
            months = option.save_trm
            expired_date = date.today() + relativedelta(months=months)

            serializer.save(
                user=request.user, 
                expired_at=expired_date,
                init_intr_rate=option.intr_rate or 0,
                init_intr_rate2=option.intr_rate2 or 0,
                init_save_trm=option.save_trm,
                init_intr_rate_type_nm=option.intr_rate_type_nm,
                is_active=True
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    # 2. GET: 내 가입 목록 조회
    elif request.method == 'GET':
        user_subscriptions = Subscription.objects.filter(user=request.user)
        serializer = SubscriptionSerializer(user_subscriptions, many=True)
        return Response(serializer.data)

    # 3. DELETE: 상품 해지 (삭제)
    elif request.method == 'DELETE':
        
        # 방식 A: Subscription 테이블의 고유 ID(pk)로 삭제 (권장)
        if subscription_id:
            subscription = get_object_or_404(Subscription, id=subscription_id)
            subscription.delete()
            return Response({"message": "해당 상품 가입이 성공적으로 해지되었습니다."}, status=status.HTTP_204_NO_CONTENT)
            
        return Response({"error": "삭제할 ID가 제공되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)

"""
상품 추천 로직
"""

# 미동의자/동의자 추천 결과 통일
# 공통: 추천 결과를 통일된 응답으로 빌드
def build_recommendation_response(user, profile, raw_recommendations, user_query=None, is_mydata=True):
    """
    raw_recommendations: recommend_products가 반환한 리스트(각 항목에 'product_option' 및 score/confidence 등 포함)
    is_mydata: 마이데이터 동의 여부 (향후 explain_recommendation에 전달할 때 사용 가능)
    반환: dict (Response에 바로 넣을 수 있는 형태)
    """
    serialized = []
    # 먼저 기본 정보 평탄화
    for rec in raw_recommendations:
        opt = rec.get('product_option')
        option_data = ProductOptionDetailSerializer(opt).data
        product = opt.product
        option_data.update({
            "fin_prdt_nm": product.fin_prdt_nm,
            "kor_co_nm": product.kor_co_nm,
            "score": round(rec.get("score", 0), 3),
            "confidence": round(rec.get("confidence", 0), 3),
            "similarity": round(rec.get("similarity", 0), 2),
            "cluster_weight": round(rec.get("cluster_weight", 0), 2),
            "ai_analysis": None
        })
        serialized.append(option_data)

    # 상위 1개(인덱스 0)에 대해서만 explain_recommendation 호출 (비용/지연 고려)
    if serialized:
        top = serialized[0]
        # explain_recommendation expects certain keys (we pass a compact dict)
        explain_input = {
            "fin_prdt_nm": top.get("fin_prdt_nm"),
            "intr_rate": top.get("intr_rate"),
            "intr_rate2": top.get("intr_rate2"),
            "save_trm": top.get("save_trm"),
            "similarity": top.get("similarity"),
            "cluster_weight": top.get("cluster_weight"),
            "confidence": int((top.get("confidence", 0) or 0) * 100)
        }
        try:
            ai = explain_recommendation(user, explain_input, user_query, is_mydata=is_mydata)
            top["ai_analysis"] = {
                "reason": ai.get("reason"),
                "report": ai.get("report"),
                "nudge": ai.get("nudge"),
            }
        except Exception as e:
            top["ai_analysis"] = {
                "reason": "데이터 기반 추천입니다.",
                "report": None,
                "nudge": None
            }

    # 프로필 스냅샷
    profile_snapshot = {
        "annual_income_amt": profile.annual_income_amt,
        "invest_eval_amt": profile.invest_eval_amt,
        "balance_amt": profile.balance_amt,
        "withdrawable_amt": profile.withdrawable_amt,
        "expense_growth_rate": profile.expense_growth_rate,
        "expense_to_income_ratio": profile.expense_to_income_ratio,
        "cluster_label": profile.cluster_label,
        "cluster_name": (profile.cluster_name or "").strip(),
    }

    persona_data = {
        "name": profile_snapshot["cluster_name"] or "자산 분석가",
        "label": profile_snapshot["cluster_label"],
        "icon": "💰" if is_mydata else "📝",
        "description": f"사용자 성향: {profile_snapshot['cluster_name']}"
    }

    payload = {
        "user": user.email,
        "is_mydata_linked": bool(getattr(profile, 'is_mydata_linked', False)),
        "persona": persona_data,
        "cluster": profile_snapshot["cluster_label"],
        "profile": profile_snapshot,
        "recommendations": serialized,
        "query_used": user_query
    }
    return payload

# 마이데이터 동의자
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendations(request):
    user = request.user
    # 프론트에서 보낸 자연어 쿼리
    user_query = request.query_params.get('query', None)

    # 1. 금융 프로필 확인
    try:
        # 1. 안전하게 프로필 확보
        profile, created = FinancialProfile.objects.get_or_create(user=user)
    except Exception:
        return Response({"error": "금융 프로필을 찾을 수 없습니다."}, status=404)

    # 2. 마이데이터 미동의자 및 설문 미완료자 차단
    # 클러스터 라벨이 없다는 것은 마이데이터 연동도 안 되었고 설문조사도 안 했다는 의미입니다.
    if not profile.is_mydata_linked and profile.cluster_label is None:
        return Response({"error": "마이데이터 연동 또는 설문조사가 필요합니다.", "code": "NEED_DATA_LINK"}, status=400)

    # 3. 추천 로직 실행 (recommend_products 함수 내부에서 profile의 데이터를 기반으로 연산됨)
    recommendations = recommend_products(user, top_n=3, user_query=user_query)
    
    if not recommendations:
        return Response({"error": "추천 결과가 없습니다."}, status=404)

    # 4. DB 저장 (추천 기록)
    save_recommendations(user, profile, recommendations)

    # 공통 빌더로 응답 생성 (LLM 호출은 여기서 is_mydata=True로 처리됩니다)
    response_payload = build_recommendation_response(user, profile, recommendations, user_query, is_mydata=True)
    return Response(response_payload)

# 미동의자 로직
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_survey(request):
    user = request.user
    survey_data = request.data
    user_query = survey_data.get('query') or request.query_params.get('query')


    # 1. 여기서 확실하게 생성 또는 가져오기를 수행
    profile, created = FinancialProfile.objects.get_or_create(user=user)
    
    # 2. 설문 데이터로 프로필 업데이트 및 클러스터 할당
    # 이 함수 내부에서 '유효성 검사'와 'assign_cluster_logic'이 차례로 실행됩니다.
    profile = update_profile_by_survey_safe(profile, survey_data)

    # 1. 추천 결과 가져오기 (List of dicts)
    raw_recommendations = recommend_products(user, top_n=3, user_query=user_query)
    
            # profile 업데이트 및 추천 raw 생성은 기존대로
    # raw_recommendations = recommend_products(...)
    response_payload = build_recommendation_response(user, profile, raw_recommendations, user_query=user_query, is_mydata=False)
    return Response(response_payload, status=200)
    
def get_queryset(self):
    term = self.request.query_params.get('term')
    queryset = FinancialProduct.objects.all()
    
    if term:
        # term이 있을 경우, options를 가져올 때 해당 term만 필터링해서 가져옴
        return queryset.prefetch_related(
            Prefetch('options', queryset=ProductOption.objects.filter(save_trm=term))
        ).filter(options__save_trm=term).distinct()
    
    return queryset.prefetch_related('options')

"""
마이데이터 해제
"""
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def disconnect_mydata(request):
    profile = request.user.financialprofile
    # 모델에 정의한 초기화 메서드 실행
    profile.disconnect_mydata()
    
    return Response({
        "message": "마이데이터 연동이 성공적으로 해지되었으며, 모든 데이터가 초기화되었습니다.",
        "is_mydata_linked": False
    }, status=200)

# PATCH 메서드로 변경하여 리소스의 부분 수정을 명시함
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_mydata(request):
    user = request.user
    
    # 1. 프로필 가져오기 또는 생성
    profile, created = FinancialProfile.objects.get_or_create(user=user)
    
    # 2. 정보 업데이트 (부분 수정)
    profile.is_mydata_linked = True
    profile.save()
    
    # 3. 성공 응답 반환
    return Response({
        "message": "마이데이터 이용 동의가 완료되었습니다.",
        "is_mydata_linked": profile.is_mydata_linked,
    }, status=200)

@api_view(['GET'])
def show_option(request, option_id):
    option = ProductOption.objects.get(id=option_id)

    serializer = ShowOptionSerializer(option)

    return Response(serializer.data)

# views.py
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_user_status(request):
#     # FinancialProfile이 없으면 생성, 있으면 가져옴
#     profile, created = FinancialProfile.objects.get_or_create(user=request.user)
    
#     return Response({
#         "is_mydata_linked": profile.is_mydata_linked,
#         "cluster_label": profile.cluster_label,
#         "cluster_name": profile.cluster_name,
#         "nickname": request.user.nickname
#     }, status=200)