import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction

# 모델 이름 변경 감안: 사용자 코드는 DepositProducts를 사용하나, 
# 이전 대화에서 FinanceProduct를 사용했으므로 DepositProducts로 가정하고 작성합니다.
from products.models import DepositProducts, DepositOptions 

# API 기본 정보 설정
API_KEY = settings.API_KEY
BASE_URL = 'https://finlife.fss.or.kr/finlifeapi/'
DEPOSIT_URL = BASE_URL + 'depositProductsSearch.json'
TOP_FIN_GRP_NO = '020000' # 은행 권역 코드

class Command(BaseCommand):
    # 도움말 메시지 정의
    help = '금융감독원 정기예금 API 데이터를 수집하여 DB에 저장합니다.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- [START] 정기예금 데이터 수집 시작 ---'))
        
        # 1. API 호출 및 데이터 가져오기
        data = self._fetch_api_data()
        
        if not data:
            self.stdout.write(self.style.ERROR('❌ API 데이터 수집 실패. 명령을 종료합니다.'))
            return

        # 2. 데이터베이스에 저장
        self._save_products_and_options(data['baseList'], data['optionList'])

        self.stdout.write(self.style.SUCCESS('✨ [END] 정기예금 데이터 수집 및 DB 저장 완료!'))


    def _fetch_api_data(self):
        """금감원 API를 호출하여 데이터를 JSON 형태로 반환"""
        params = {
            'auth': API_KEY,
            'topFinGrpNo': TOP_FIN_GRP_NO,
            'pageNo': 1
        }
        
        try:
            response = requests.get(DEPOSIT_URL, params=params).json()
            
            # API 오류 응답 체크
            if response.get('result', {}).get('ERR_CD') == '900':
                self.stderr.write(self.style.ERROR(
                    f"❌ API 인증/요청 오류: {response.get('RESULT', {}).get('ERR_MSG', '알 수 없는 오류')}"
                ))
                return None
            
            # 여기서 페이지네이션 로직을 추가하여 모든 페이지의 데이터를 가져올 수 있습니다.
            # (편의상 첫 페이지만 가져오는 것으로 리팩토링했습니다.)
            return response.get('result')

        except requests.RequestException as e:
            self.stderr.write(self.style.ERROR(f'❌ API 요청 중 네트워크 오류 발생: {e}'))
            return None
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'❌ 데이터 파싱 중 오류 발생: {e}'))
            return None


    @transaction.atomic
    def _save_products_and_options(self, base_list, option_list):
        """상품과 옵션 데이터를 DB에 저장 (최적화)"""
        
        self.stdout.write(f'총 상품: {len(base_list)}개, 총 옵션: {len(option_list)}개 처리 시작.')
        
        # 1. 상품 정보 저장 (update_or_create 사용)
        product_codes = []
        for product_data in base_list:
            # 💡 데이터를 명확하고 간결하게 처리
            data = {
                'fin_co_no': product_data.get('fin_co_no', ''),
                'kor_co_nm': product_data.get('kor_co_nm', '알 수 없음'),
                'fin_prdt_nm': product_data.get('fin_prdt_nm', '알 수 없음'),
                'join_member': product_data.get('join_member', ''),
                'join_way': product_data.get('join_way', ''),
                'join_deny': product_data.get('join_deny', 0), # 기본값 0 처리
                'dcls_strt_day': product_data.get('dcls_strt_day', '00000000'),
                'max_limit': product_data.get('max_limit'), # None 허용
                'spcl_cnd': product_data.get('spcl_cnd'),
                'mtrt_int': product_data.get('mtrt_int'),
                'etc_note': product_data.get('etc_note'),
                # 'product_type': 'DEPOSIT' (모델 default 값 사용 권장)
            }
            
            # NOT NULL 필드에 빈 문자열이 아닌 None이 들어갈 위험 방지
            for key in ['spcl_cnd', 'mtrt_int', 'etc_note']:
                if data[key] is None:
                    data[key] = ''

            DepositProducts.objects.update_or_create(
                fin_prdt_cd=product_data['fin_prdt_cd'],
                defaults=data
            )
            product_codes.append(product_data['fin_prdt_cd'])
            
        self.stdout.write(self.style.NOTICE(f'✅ 상품 정보 {len(base_list)}개 저장 완료.'))


        # 2. 옵션 정보 저장 (N+1 쿼리 방지 최적화)
        
        # 📌 최적화 핵심: 저장된 모든 상품 인스턴스를 한 번에 불러와 딕셔너리로 만듭니다.
        products_dict = {
            p.fin_prdt_cd: p 
            for p in DepositProducts.objects.filter(fin_prdt_cd__in=product_codes)
        }
        
        options_to_create = []
        
        # 기존 옵션 데이터 삭제 (옵션만 업데이트하는 경우도 있지만, 여기서는 초기화)
        # 💡 옵션은 상품 코드와 save_trm을 조합하여 Unique함을 가정합니다.
        DepositOptions.objects.filter(product__fin_prdt_cd__in=product_codes).delete()
        
        for option_data in option_list:
            fin_prdt_cd = option_data.get('fin_prdt_cd')
            product_instance = products_dict.get(fin_prdt_cd)
            
            if not product_instance:
                # 상품을 찾을 수 없는 경우 경고만 출력하고 건너뜁니다.
                continue

            # 💡 금리 -1 처리 로직 간결화
            # intr_rate, intr_rate2는 FloatField일 경우 None을 허용하는 것이 좋습니다.
            # 만약 NOT NULL이라면 0이나 -1을 사용해야 합니다. (여기서는 -1을 사용한 기존 로직 유지)
            intr_rate_val = option_data.get('intr_rate')
            intr_rate2_val = option_data.get('intr_rate2')

            options_to_create.append(DepositOptions(
                product=product_instance,
                save_trm=int(option_data.get('save_trm')),
                intr_rate_type_nm=option_data.get('intr_rate_type_nm'),
                intr_rate_type=option_data.get('intr_rate_type', 'N/A'),
                intr_rate=intr_rate_val if intr_rate_val is not None else -1,
                intr_rate2=intr_rate2_val if intr_rate2_val is not None else -1,
            ))
            
        # 📌 성능 최적화: BULK INSERT 사용
        DepositOptions.objects.bulk_create(options_to_create, ignore_conflicts=True)
        
        self.stdout.write(self.style.NOTICE(f'✅ 옵션 정보 {len(options_to_create)}개 저장 완료.'))