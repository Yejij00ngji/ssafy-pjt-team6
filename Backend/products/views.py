from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Avg

from .models import DepositOptions, DepositProducts
from users.models import FinancialProfile
from .serializers import DepositOptionsSerializer, DepositProductsSerializer, DepositProductsDetailsSerializer
from .services import simulate_mydata_linking, predict_user_cluster
from .filters import ProductFilter

from datetime import date
from dateutil.relativedelta import relativedelta

@api_view(['GET'])
def products(request):
  if request.method == 'GET':
    
    queryset = DepositProducts.objects.all().distinct()

    filterset = ProductFilter(request.GET, queryset=queryset)

    if filterset.is_valid():
      queryset = filterset.qs

    serializer = DepositProductsSerializer(queryset, many=True)
    return Response(serializer.data)
  
@api_view(['GET','POST'])
def product_details(request, pk):
  if request.method == 'GET':
    deposit_product = DepositProducts.objects.get(pk=pk)
    serializer = DepositProductsDetailsSerializer(deposit_product)
    return Response(serializer.data)

@api_view(['GET'])
def options(request):
  if request.method == 'GET':
    subscribed_option_ids = request.user.subscriptions.values_list('deposit_option_id', flat=True)

    subscribed_options = DepositOptions.objects.filter(id__in=subscribed_option_ids).select_related('product')
    serializer = DepositOptionsSerializer(subscribed_options, many=True)

    # deposit_options = DepositOptions.objects.all()
    # serializer = DepositOptionsSerializer(deposit_options,many=True)
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