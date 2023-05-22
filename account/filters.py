import  django_filters 
from django.shortcuts import get_object_or_404
from django.db.models import Q

from account.models import *



class ProductFilters(django_filters.FilterSet):
    price = django_filters.NumberFilter(field_name="publish_price")
    min_price = django_filters.NumberFilter(field_name="publish_price", lookup_expr='gte')
    max_price= django_filters.NumberFilter(field_name="publish_price", lookup_expr='lte')

    category = django_filters.CharFilter(field_name="category", method='filter_by_category')

    brand = django_filters.CharFilter(field_name='brand',method='filter_brand')

    options = django_filters.CharFilter(field_name='attributes__value',method='filter_by_attributes')

    class Meta:
        model = Product
        fields = ('price','min_price','max_price')

    def filter_by_category(self, queryset, name, value):
        if value:
            try:
                category = get_object_or_404(Category, name=value)
                descendants = category.get_children_and_self()
                products = queryset.filter(category__in=descendants)
                return products
            except Category.DoesNotExist:
                return []

        else:
            return queryset
            
    def filter_brand(self, queryset, name , value):

        filters = { 'brand__in': value.split(",") }
        queryset = queryset.filter(**filters)
        return queryset
    
    def filter_by_attributes(self, queryset, name , value):

        filters = { f'{name}__in': value.split(",") }
        queryset = queryset.filter(**filters)
        return queryset
        # filters = Q()
        # for val in value.split(","):
        #     filters = filters | Q(attributes__value__in=val)
        # queryset = queryset.filter(filters)
        # return queryset