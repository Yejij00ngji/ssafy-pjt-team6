from django_filters import rest_framework as filters
from .models import FinancialProduct

class ProductFilter(filters.FilterSet):
  bank = filters.CharFilter(field_name="kor_co_nm", lookup_expr='icontains')

  product_type = filters.ChoiceFilter(
        field_name="product_type",
        choices=(('DEPOSIT', '정기예금'), ('SAVING', '적금'))
    )

  term = filters.NumberFilter(field_name="options__save_trm", lookup_expr='contains')

  class Meta:
    model = FinancialProduct
    fields = ['bank', 'term']