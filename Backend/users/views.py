from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserDetailSerializer

# Create your views here.

@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated]) # 로그인한 사용자만 접근 가능
def profile_update_view(request):
    user = request.user
    
    # 1. 프로필 정보 조회 (GET)
    if request.method == 'GET':
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

    # 2. 프로필 정보 수정 (PUT/PATCH)
    elif request.method in ['PUT', 'PATCH']:
        # partial=True를 설정하면 nickname이나 email 중 하나만 보내도 수정 가능합니다.
        serializer = UserDetailSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)