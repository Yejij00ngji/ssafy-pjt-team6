from django_filters import rest_framework as filters
from .models import DepositProducts

class ProductFilter(filters.FilterSet):
  bank = filters.CharFilter(field_name="kor_co_nm", lookup_expr='exact')

  term = filters.NumberFilter(field_name="options__save_trm", lookup_expr='contains')

  class Meta:
    model = DepositProducts
    fields = ['bank', 'term']