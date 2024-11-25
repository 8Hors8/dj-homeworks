import django_filters
from django_filters import rest_framework as filters
from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    created_at = django_filters.DateFromToRangeFilter(field_name='created_at')
    creator = django_filters.NumberFilter(field_name='creator')
    creator_username = django_filters.CharFilter(field_name='creator__username', lookup_expr='icontains')
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')

    class Meta:
        model = Advertisement
        fields = ['created_at', 'creator', 'creator_username', 'status']