from django_filters import rest_framework as filters
from .models import FinancialProduct

class ProductFilter(filters.FilterSet):

  # 검색 기준 은행 탐색
  bank = filters.CharFilter(field_name="kor_co_nm", lookup_expr='icontains')

  product_type = filters.CharFilter(method='filter_product_type')

  # term: 1, 3, 6, 12, 24, 36
  term = filters.NumberFilter(field_name="options__save_trm")

  class Meta:
    model = FinancialProduct
    fields = ['bank', 'term', 'product_type']

  def filter_product_type(self, queryset, name, value):
        if value in ['ALL', '', None]:
            return queryset
        return queryset.filter(product_type=value)