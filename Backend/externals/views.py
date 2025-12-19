from django.shortcuts import render

# Create your views here.
import requests
import os
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# 1. 유튜브 검색 (상세 정보 포함)
@api_view(['GET'])
def youtube_search(request):
    query = request.query_params.get('q')
    api_key = settings.YOUTUBE_API_KEY
    
    # 1. 먼저 검색 결과(ID)를 가져옴
    search_url = "https://www.googleapis.com/youtube/v3/search"
    search_params = {
        'key': api_key, 'part': 'snippet', 'q': query, 'type': 'video', 'maxResults': 10
    }
    search_res = requests.get(search_url, params=search_params).json()
    video_ids = [item['id']['videoId'] for item in search_res.get('items', [])]

    # 2. 영상 ID들로 상세 정보(조회수, 전체 설명 등)를 다시 요청
    video_url = "https://www.googleapis.com/youtube/v3/videos"
    video_params = {
        'key': api_key,
        'part': 'snippet,statistics', # 상세 설명과 통계 정보 요청
        'id': ','.join(video_ids)
    }
    video_res = requests.get(video_url, params=video_params).json()

    results = []
    for item in video_res.get('items', []):
        results.append({
            'videoId': item['id'],
            'title': item['snippet']['title'],
            'thumbnail': item['snippet']['thumbnails']['high']['url'],
            'channelName': item['snippet']['channelTitle'],
            'description': item['snippet']['description'], # 이제 전체 설명이 들어옵니다.
            'publishedAt': item['snippet']['publishedAt'],
            'viewCount': item['statistics'].get('viewCount', 0), # 조회수 추가
        })
    return Response(results)

# 2. 카카오 모빌리티 경로 안내 (멀캠 역삼 -> 은행)
@api_view(['GET'])
def get_route(request):
    origin = request.query_params.get('origin', "127.039585,37.5012743")
    destination = request.query_params.get('destination')
    
    if not destination:
        return Response({"error": "목적지 좌표가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

    # settings에서 키 가져오기
    api_key = settings.KAKAO_PATH_KEY 
    url = "https://apis-navi.kakaomobility.com/v1/directions"
    
    headers = {"Authorization": f"KakaoAK {api_key}"}
    params = {
        "origin": origin,
        "destination": destination,
        "priority": "RECOMMEND"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        return Response(response.json(), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "모빌리티 API 호출 실패"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 3. 금/은 시세 확인 
