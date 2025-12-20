from django.shortcuts import render

# Create your views here.
import pandas as pd
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
def get_asset_prices(asset_type):
    # 파일 경로 설정 (자산 타입에 따라 파일 선택)
    file_name = f"{asset_type.capitalize()}_prices.xlsx"
    file_path = os.path.join(settings.BASE_DIR, 'CRUD', 'data', file_name)
    
    # 엑셀 읽기
    df = pd.read_excel(file_path)
    
    # 날짜와 가격 컬럼만 추출 (컬럼명은 실제 엑셀 파일에 맞게 수정 필요)
    # 예: 날짜, 종가(Price)
    return df

@api_view(['GET'])
def asset_price_list(request):
    asset_type = request.query_params.get('type', 'gold') # 기본값 gold
    start_date = request.query_params.get('start')
    end_date = request.query_params.get('end')
    
    df = get_asset_prices(asset_type)

    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date')
    
    # 날짜 필터링 로직 (데이터가 많을 경우 pandas에서 미리 처리하는 게 좋음)
    if start_date and end_date:
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    result = []
    for _, row in df.iterrows():
        result.append({
            'date': row['Date'].strftime('%Y-%m-%d'),
            'price': float(str(row['Close/Last']).replace(',', '')) # 콤마 제거 후 실수 변환
        })
        
    return Response(result)