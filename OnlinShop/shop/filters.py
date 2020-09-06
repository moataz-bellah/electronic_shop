import django_filters
from . import models
class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = models.Product
        fields = ['name','price','brand','category']
