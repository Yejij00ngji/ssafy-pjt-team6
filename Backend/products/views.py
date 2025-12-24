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
  elif request.method == 'GET':
    user_subscriptions = Subscription.objects.filter(user=request.user)
    serializer = SubscriptionSerializer(user_subscriptions, many=True)
    return Response(serializer.data)

# -----------------------------------------------------------------------------------------
# 추천 로직
# -----------------------------------------------------------------------------------------
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendations(request):
    logger.info("추천 요청이 들어왔습니다.")

    user = request.user

    try:
        profile = user.financialprofile
    except:
        logger.error("금융 프로필을 찾을 수 없습니다.")  # 오류 로그
        return Response({"error": "금융 프로필 없음"}, status=404)

    if profile.cluster_label not in [0, 1, 2, 3, 4]:
        logger.warning("마이데이터 연동이 필요합니다.")  # 경고 로그
        return Response({"error": "마이데이터 연동 필요"}, status=400)

    # 추천 로직 실행
    recommendations = recommend_products(user, top_n=3)
    
    if not recommendations:
        logger.warning("추천 결과가 없습니다.")  # 경고 로그
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
        
    logger.info(f"추천결과: {result}")

    return Response({
        "user": user.username,
        "cluster": profile.cluster_label,
        "recommendations": result
    })

def get_queryset(self):
    term = self.request.query_params.get('term')
    queryset = FinancialProduct.objects.all()
    
    if term:
        # term이 있을 경우, options를 가져올 때 해당 term만 필터링해서 가져옴
        return queryset.prefetch_related(
            Prefetch('options', queryset=ProductOption.objects.filter(save_trm=term))
        ).filter(options__save_trm=term).distinct()
    
    return queryset.prefetch_related('options')