from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Avg, Count, Prefetch

from .models import ProductOption, FinancialProduct, Subscription
from users.models import FinancialProfile
from .serializers import ProductOptionSerializer, FinancialProductSerializer, FinancialProductDetailSerializer, SubscriptionSerializer
from .filters import ProductFilter
from .services.recommendations import recommend_products
from .services.save_nodata import update_profile_by_survey_safe

from datetime import date
from dateutil.relativedelta import relativedelta

from products.services.recommendation_history import save_recommendations

# 전체 상품 조회
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

    # product_options = ProductOption.objects.all()
    # serializer = ProductOptionSerializer(product_options,many=True)
    return Response(serializer.data)

# =================================================================================
# 예적금 통합
# =================================================================================
  
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
        # URL 파라미터로 넘어온 subscription_id를 사용하거나 
        # request body에서 product_option_id를 받아 처리할 수 있습니다.
        
        # 방식 A: Subscription 테이블의 고유 ID(pk)로 삭제 (권장)
        if subscription_id:
            subscription = get_object_or_404(Subscription, id=subscription_id)
            subscription.delete()
            return Response({"message": "해당 상품 가입이 성공적으로 해지되었습니다."}, status=status.HTTP_204_NO_CONTENT)
            
        return Response({"error": "삭제할 ID가 제공되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------------------------------------------------------------------
# 추천 로직
# -----------------------------------------------------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendations(request):

    user = request.user

    # 1. 금융 프로필 확인
    try:
        # 1. 안전하게 프로필 확보
        profile, created = FinancialProfile.objects.get_or_create(user=user)
    except Exception:
        return Response({"error": "금융 프로필을 찾을 수 없습니다."}, status=404)

    # 2. 마이데이터 미동의자 및 설문 미완료자 차단
    # 클러스터 라벨이 없다는 것은 마이데이터 연동도 안 되었고 설문조사도 안 했다는 의미입니다.
    if profile.cluster_label is None:
        return Response({"error": "마이데이터 연동 또는 설문조사가 필요합니다.", "code": "NEED_DATA_LINK"}, status=400)


    # 4. 추천 로직 실행 (recommend_products 함수 내부에서 profile의 데이터를 기반으로 연산됨)
    recommendations = recommend_products(user, top_n=3)
    
    if not recommendations:
        return Response({"error": "추천 결과가 없습니다."}, status=404)

    # 🔥 여기서 DB 저장
    save_recommendations(user, profile, recommendations)
    
    result = []
    for rec in recommendations:
        option = rec["product_option"]
        result.append({
            "product_option_id": option.id,
            "product_name": option.product.fin_prdt_nm,
            "bank_name": option.product.kor_co_nm,
            "intr_rate": option.intr_rate,
            "intr_rate2": option.intr_rate2,
            "save_trm": option.save_trm,
            "score": round(rec["score"], 3),
            "confidence": round(rec["confidence"], 3),
            "reason": rec["reason"]  # 여기서 이유 추가
        })
        
    return Response({
        "user": user.username,
        "cluster": profile.cluster_label,
        "recommendations": result
    })

# 미동의자 로직
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_survey(request):
    user = request.user
    survey_data = request.data

    try:
        # 1. 여기서 확실하게 생성 또는 가져오기를 수행
        profile, created = FinancialProfile.objects.get_or_create(user=user)
        
        # 2. profile 객체를 직접 함수에 넘겨주세요 (user 대신 profile을 넘기는 게 안전)
        profile = update_profile_by_survey_safe(profile, survey_data)
        
        return Response({
            "message": "설문이 완료되었습니다.",
            "cluster": profile.cluster_label
        }, status=200)
        
    except Exception as e:
        # 에러가 나면 정확히 어떤 에러인지 서버 터미널(VSCode 등)에 찍힙니다.
        print(f"🔥 백엔드 에러 발생: {str(e)}") 
        return Response({"error": str(e)}, status=400)
    
def get_queryset(self):
    term = self.request.query_params.get('term')
    queryset = FinancialProduct.objects.all()
    
    if term:
        # term이 있을 경우, options를 가져올 때 해당 term만 필터링해서 가져옴
        return queryset.prefetch_related(
            Prefetch('options', queryset=ProductOption.objects.filter(save_trm=term))
        ).filter(options__save_trm=term).distinct()
    
    return queryset.prefetch_related('options')