from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import SubscriptionSerializer
from .models import Subscription
from datetime import date
from dateutil.relativedelta import relativedelta



# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def subscriptions(request):
  if request.method == 'POST':
    serializer = SubscriptionSerializer(data = request.data)
    
    if serializer.is_valid(raise_exception=True):

      # 가입 날짜 기준 만기일 계산
      option = serializer.validated_data['deposit_option']
      months = option.save_trm
      expired_date = date.today() + relativedelta(months=months)

      serializer.save(user=request.user, expired_at=expired_date)

      return Response(serializer.data, status=status.HTTP_201_CREATED)
  elif request.method == 'GET':
    user_subscriptions = Subscription.objects.filter(user=request.user)
    serializer = SubscriptionSerializer(user_subscriptions, many=True)
    return Response(serializer.data)