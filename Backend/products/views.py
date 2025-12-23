from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Avg, Count

# from .models import ProductOption, FinancialProduct, Subscription
from .models import ProductOption, FinancialProduct, Subscription
from users.models import FinancialProfile
# from .serializers import ProductOptionSerializer, FinancialProductSerializer, FinancialProductDetailsSerializer, SubscriptionSerializer
from .serializers import ProductOptionSerializer, FinancialProductSerializer, FinancialProductDetailSerializer, SubscriptionSerializer
from .services import simulate_mydata_linking, predict_user_cluster
from .filters import ProductFilter

from datetime import date
from dateutil.relativedelta import relativedelta

# 전체 상품 조회
@api_view(['GET'])
def products(request):
  if request.method == 'GET':
    
    queryset = FinancialProduct.objects.all().distinct()

    filterset = ProductFilter(request.GET, queryset=queryset)

    if filterset.is_valid():
      queryset = filterset.qs

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
  
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def subscriptions(request):
  if request.method == 'POST':
    serializer = SubscriptionSerializer(data = request.data)
    
    if serializer.is_valid(raise_exception=True):

      # 가입 날짜 기준 만기일 계산
      option = serializer.validated_data['product_option']
      months = option.save_trm
      expired_date = date.today() + relativedelta(months=months)

      serializer.save(user=request.user, expired_at=expired_date)

      return Response(serializer.data, status=status.HTTP_201_CREATED)
  elif request.method == 'GET':
    user_subscriptions = Subscription.objects.filter(user=request.user)
    serializer = SubscriptionSerializer(user_subscriptions, many=True)
    return Response(serializer.data)

# -----------------------------------------------------------------------------------------
# 마이데이터 생성
# -----------------------------------------------------------------------------------------

@api_view(['POST'])
def link_mydata_api(request):
    profile = request.user.financialprofile
    
    # 1. 가상 데이터 채우기
    updated_profile = simulate_mydata_linking(profile)
    
    # 2. [전략 B] 학습된 모델로 즉시 예측
    cluster_label = predict_user_cluster(updated_profile)
    
    return Response({
        "message": "AI 분석 완료",
        "persona_id": cluster_label
    })

@api_view(['GET'])
def get_my_financial_report(request):
    """
    내 데이터와 내가 속한 그룹의 평균을 비교하여 차트용 데이터를 보냅니다.
    """
    try:
        my_profile = request.user.financialprofile
        if not my_profile.cluster_label:
            return Response({"error": "먼저 마이데이터를 연동해주세요."}, status=400)
            
        # 1. 내 지표 계산
        my_data = {
            "income": my_profile.annual_income_amt,
            "balance": my_profile.balance_amt,
            "invest_ratio": round(my_profile.invest_eval_amt / (my_profile.balance_amt + my_profile.invest_eval_amt + 1), 2),
            "expense_growth": my_profile.expense_growth_rate
        }

        # 2. 내가 속한 그룹의 평균 데이터 가져오기 (DB 집계)
        group_stats = FinancialProfile.objects.filter(
            cluster_label=my_profile.cluster_label
        ).aggregate(
            avg_income=Avg('annual_income_amt'),
            avg_balance=Avg('balance_amt'),
            avg_growth=Avg('expense_growth_rate')
        )

        return Response({
            "my_data": my_data,
            "group_avg": group_stats,
            "persona": my_profile.cluster_label  # 예: "0" (나중에 명칭 매핑 가능)
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)
  
# 본격적인 상품 추천 로직
@api_view(['GET'])
def recommend_by_portfolio(request):
    user = request.user
    
    # 1. 유저의 프로필 및 클러스터 확인
    try:
        profile = user.financialprofile
        my_label = profile.cluster_label
        if not my_label:
            return Response({"message": "마이데이터 연동이 필요합니다."}, status=400)
    except Exception:
        return Response({"message": "프로필을 찾을 수 없습니다."}, status=404)

    # 2. 나와 같은 그룹인 유저들의 ID 리스트 추출
    similar_user_ids = FinancialProfile.objects.filter(
        cluster_label=my_label
    ).exclude(user=user).values_list('user_id', flat=True)

    # 3. 그들이 가입한 상품(ProductOption) 중 가장 인기 있는 것 Top 3
    # Subscription 테이블을 통해 인기 상품 집계
    recommended_items = Subscription.objects.filter(
        user_id__in=similar_user_ids
    ).values('product_option') \
     .annotate(subscriber_count=Count('user')) \
     .order_by('-subscriber_count')[:3]

    # 4. 상품 상세 정보 담기
    recommend_list = []
    for item in recommended_items:
        option = ProductOption.objects.get(id=item['product_option'])
        recommend_list.append({
            "product_name": option.product.fin_prdt_nm,
            "bank_name": option.product.kor_co_nm,
            "intr_rate": option.intr_rate,
            "intr_rate2": option.intr_rate2,
            "save_trm": option.save_trm,
            "subscriber_count": item['subscriber_count'] # "ㅇㅇ님 그룹에서 n명이 선택함" 강조용
        })

    return Response({
        "username": user.username,
        "persona": my_label,
        "recommendations": recommend_list
    })