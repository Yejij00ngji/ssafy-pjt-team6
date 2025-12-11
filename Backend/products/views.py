import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings  # settings.py에서 API_KEY 가져옴
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

from .models import DepositProducts, DepositOptions

# API 기본 정보 설정
API_KEY = settings.API_KEY # settings.py에서 설정된 환경변수
BASE_URL = 'https://finlife.fss.or.kr/finlifeapi/' # 실제 데이터가 있는 금감원 주소

# ====================
# API 데이터 수집 및 저장
# ====================
@api_view(['GET'])
def save_deposit_products(request):

    # 1. API 요청 URL 및 파라미터 설정
    url = BASE_URL + 'depositProductsSearch.json'
    params = {
        'auth': API_KEY,
        'topFinGrpNo': '020000', # 은행 (권역 코드)
        'pageNo': 1
    }

    try:
        # 2. requests 라이브러리를 사용하여 API 호출
        response = requests.get(url, params=params).json()
        # 디버깅 코드
        print('--- API Response Status: ---')
        print(response.get('result', {}).get('ERR_CD', 'N/A')) # API 오류 코드 출력
        print('--- API Response Keys: ---')
        print(response.keys())
        
        # 3. 데이터 파싱
        base_list = response.get('result', {}).get('baseList', []) 
        option_list = response.get('result', {}).get('optionList', [])
        
        print('--- Data Counts ---')
        print(f'상품 목록 개수 (baseList): {len(base_list)}')
        print(f'옵션 목록 개수 (optionList): {len(option_list)}')

        # API 호출에 실패했을 경우 예외 처리
        if response.get('RESULT', {}).get('ERR_CD') == '900':
             return Response({'message': 'API 호출 오류: 인증키 또는 요청 문제'}, status=400)
        
        # 3. 데이터 파싱
        # API 응답 구조: {'result': {'baseList': [상품 리스트], 'optionList': [옵션 리스트]}}
        base_list = response.get('result', {}).get('baseList', []) # 상품 정보 리스트
        option_list = response.get('result', {}).get('optionList', []) # 옵션 정보 리스트

        # 4. 상품 정보 (DepositProducts) 저장
        # 중복 방지를 위해 상품 코드(fin_prdt_cd)를 기준으로 업데이트하거나 생성
        for product_data in base_list:
            fin_prdt_cd = product_data.get('fin_prdt_cd')
            
            # --- 💡 NOT NULL 오류 방지 및 데이터 타입 처리 ---
            # 1. join_deny 처리: API에 값이 없거나 None이면 0으로 대체 (NOT NULL 오류 방지)
            join_deny_value = product_data.get('join_deny', 0)
            
            # 2. max_limit 처리: API에 값이 없거나 None이면 0(혹은 None)으로 대체 (IntegerField 오류 방지)
            # max_limit는 모델에서 null=True가 가능하나, 깔끔한 데이터 처리를 위해 기본값 0을 줄 수 있습니다.
            max_limit_value = product_data.get('max_limit', None)
            
            # 3. dcls_strt_day 처리: NOT NULL 필드이므로, 값이 없으면 빈 문자열 또는 '00000000' 등으로 처리
            dcls_strt_day_value = product_data.get('dcls_strt_day', '00000000')

            # --- 💡 DepositProducts.objects.update_or_create 호출 ---
            deposit_product, created = DepositProducts.objects.update_or_create(
                # 1. 조회 조건 (API 응답 필드: fin_prdt_cd)
                fin_prdt_cd=fin_prdt_cd,
                
                # 2. 업데이트/생성 시 사용될 데이터 (defaults)
                defaults={
                    # 📌 NOT NULL이면서 API 응답에 반드시 있어야 하는 필드들
                    'fin_co_no': product_data.get('fin_co_no', ''),
                    'kor_co_nm': product_data.get('kor_co_nm', '알 수 없음'),
                    'fin_prdt_nm': product_data.get('fin_prdt_nm', '알 수 없음'),
                    'join_member': product_data.get('join_member', ''),
                    'join_way': product_data.get('join_way', ''),
                    
                    # 📌 오류 발생 필드: 기본값 적용
                    'join_deny': join_deny_value, 
                    'dcls_strt_day': dcls_strt_day_value,
                    
                    # 📌 null=True가 허용되는 필드들 (API에 없어도 None으로 저장됨)
                    'spcl_cnd': product_data.get('spcl_cnd'),
                    'mtrt_int': product_data.get('mtrt_int'),
                    'etc_note': product_data.get('etc_note'),
                    'max_limit': max_limit_value, 
                    
                    # 📌 default 값이 모델에 정의된 필드 (선택적: 넣지 않아도 됨)
                    # 'product_type': 'DEPOSIT' # 모델에 default='DEPOSIT'이 있으므로 생략 가능
                }
            )

        # 5. 옵션 정보 (DepositOptions) 저장
        option_success_count = 0 
        for option_data in option_list:
            fin_prdt_cd = option_data.get('fin_prdt_cd')

            try:
                # 🚨 외래키 인스턴스 조회 (추가 필요)
                deposit_product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
                
                # --- 💡 금리 -1 처리 로직 ---
                intr_rate_val = option_data.get('intr_rate')
                intr_rate2_val = option_data.get('intr_rate2')
                cleaned_intr_rate = intr_rate_val if intr_rate_val is not None else -1
                cleaned_intr_rate2 = intr_rate2_val if intr_rate2_val is not None else -1

                DepositOptions.objects.update_or_create(
                    # 1. 조회 조건 (product 변수 사용)
                    product=deposit_product,
                    save_trm=option_data.get('save_trm'),
                    intr_rate_type_nm=option_data.get('intr_rate_type_nm'),

                    # 2. 업데이트/생성 시 사용될 데이터
                    defaults={
                        'intr_rate': cleaned_intr_rate,
                        'intr_rate2': cleaned_intr_rate2,
                        'intr_rate_type': option_data.get('intr_rate_type', 'N/A'),
                    }
                )
                option_success_count += 1
                
            except DepositProducts.DoesNotExist:
                # ❌ 상품 코드가 DepositProducts에 없는 옵션은 건너뜁니다.
                print(f"❌ OPTIONS SKIPPED: 상품 코드 {fin_prdt_cd}의 상품이 DB에 없어 옵션 저장 건너뜀.")
                continue
                
            except Exception as e:
                # ❌ 기타 오류 (IntegrityError, ValueError 등)
                print(f"❌ OPTIONS FAILED: 상품 코드 {fin_prdt_cd} - 저장 오류: {e}")
                # 이 로그를 통해 어떤 오류가 났는지 정확히 알 수 있습니다.
                
        # print(f"--- Final Option Save Count: {option_success_count} / {len(option_list)} ---")

        # 6. 저장 완료 응답 반환
        return Response({"message": "okay"}, status=200)

    except requests.RequestException as e:
        return Response({'message': f'API 요청 중 오류 발생: {e}'}, status=500)
    except Exception as e:
        return Response({'message': f'데이터 저장 중 오류 발생: {e}'}, status=500)

