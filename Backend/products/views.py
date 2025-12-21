from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import DepositOptions, DepositProducts, FinancialProfile
from .serializers import DepositOptionsSerializer, DepositProductsSerializer, DepositProductsDetailsSerializer
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
from .services import simulate_mydata_linking

@api_view(['POST'])
def link_mydata_api(request):
    # 로그인한 유저의 프로필 가져오기
    profile = request.user.FinancialProfile
    
    # 마이데이터 시뮬레이션 실행
    updated_profile = simulate_mydata_linking(profile)
    
    return Response({
        "message": "마이데이터 2.0 연동이 완료되었습니다.",
        "linked_orgs": updated_profile.linked_org_count,
        "total_balance": updated_profile.balance_amt
    })