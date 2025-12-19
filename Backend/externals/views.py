from django.shortcuts import render

# Create your views here.
import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

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