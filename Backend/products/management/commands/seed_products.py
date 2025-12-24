import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from products.models import FinancialProduct, ProductOption
# from ai.services.recommendation_explainer import get_embedding  # 🔥 임베딩 함수 임포트

# API 기본 정보 설정
API_KEY = settings.API_KEY
BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'
# DEPOSIT_URL = BASE_URL + 'depositProductsSearch.json'
TOP_FIN_GRP_NO = '020000' # 은행 권역 코드


class Command(BaseCommand):
    help = '금융감독원 API로부터 정기예금 및 적금 데이터를 통합 수집하여 DB에 저장합니다.'

    def handle(self, *args, **options):
        # 1. 수집 대상 정의 (예금, 적금)
        target_apis = [
            {'type': 'DEPOSIT', 'url': 'depositProductsSearch.json', 'name': '정기예금'},
            {'type': 'SAVING', 'url': 'savingProductsSearch.json', 'name': '적금'},
        ]

        for api in target_apis:
            self.stdout.write(self.style.SUCCESS(f'--- [START] {api["name"]} 데이터 수집 시작 ---'))
            
            data = self._fetch_api_data(api['url'])
            if not data:
                self.stdout.write(self.style.ERROR(f'❌ {api["name"]} 데이터 수집 실패.'))
                continue

            # 2. 통합 모델에 저장 (기존 로직 유지하며 type 추가)
            self._save_products_and_options(data['baseList'], data['optionList'], api['type'])
            self.stdout.write(self.style.SUCCESS(f'✨ [END] {api["name"]} 저장 완료!'))

    def _fetch_api_data(self, endpoint):
        params = {
            'auth': settings.API_KEY, # settings에 설정된 키 사용
            'topFinGrpNo': '020000',
            'pageNo': 1
        }
        try:
            url = f'https://finlife.fss.or.kr/finlifeapi/{endpoint}'
            response = requests.get(url, params=params).json()
            if response.get('result', {}).get('ERR_CD') == '900':
                return None
            return response.get('result')
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'❌ API 오류: {e}'))
            return None

    @transaction.atomic
    def _save_products_and_options(self, base_list, option_list, p_type):
        """기존 최적화 로직을 활용한 통합 저장"""
        
        product_codes = []
        for product_data in base_list:

            # 통합 모델에 맞게 필드 매핑
            data = {
                'product_type': p_type, # 구분 필드 추가
                'kor_co_nm': product_data.get('kor_co_nm', '알 수 없음'),
                'fin_prdt_nm': product_data.get('fin_prdt_nm', '알 수 없음'),
                'join_member': product_data.get('join_member', ''),
                'join_way': product_data.get('join_way', ''),
                'join_deny': product_data.get('join_deny', 0),
                'spcl_cnd': product_data.get('spcl_cnd') or '',
                'mtrt_int': product_data.get('mtrt_int') or '',
                'etc_note': product_data.get('etc_note') or '',
                'rsrv_type_nm': product_data.get('rsrv_type_nm'), # 적금 전용 필드
            }

            FinancialProduct.objects.update_or_create(
                fin_prdt_cd=product_data['fin_prdt_cd'],
                defaults=data
            )
            product_codes.append(product_data['fin_prdt_cd'])

        # 옵션 처리 (기존의 bulk_create 최적화 방식 유지)
        products_dict = {
            p.fin_prdt_cd: p 
            for p in FinancialProduct.objects.filter(fin_prdt_cd__in=product_codes)
        }
        
        # 기존 해당 상품들의 옵션만 초기화
        ProductOption.objects.filter(product__fin_prdt_cd__in=product_codes).delete()
        
        options_to_create = []
        for option_data in option_list:
            fin_prdt_cd = option_data.get('fin_prdt_cd')
            product_instance = products_dict.get(fin_prdt_cd)
            
            if product_instance:
                # 🔥 여기서 해당 상품의 텍스트로 임베딩 생성
                # (상품 하나에 옵션이 여러 개라면, product_instance에서 미리 계산한 걸 재사용하는 게 효율적입니다)
                # embedding_text = f"{product_instance.fin_prdt_nm} {product_instance.etc_note}"
                # p_embedding = get_embedding(embedding_text)

                options_to_create.append(ProductOption(
                    product=product_instance,
                    fin_prdt_cd=fin_prdt_cd,
                    save_trm=int(option_data.get('save_trm')),
                    intr_rate_type_nm=option_data.get('intr_rate_type_nm'),
                    intr_rate=option_data.get('intr_rate') if option_data.get('intr_rate') is not None else -1,
                    intr_rate2=option_data.get('intr_rate2') if option_data.get('intr_rate2') is not None else -1,
                    # embedding=p_embedding,
                ))
            
        ProductOption.objects.bulk_create(options_to_create, ignore_conflicts=True)