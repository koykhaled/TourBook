from datetime import datetime, timedelta
from django_filters import rest_framework as filters
from ..models.offers import OfferRequest


class OfferRequestFilterService(filters.FilterSet):
    date = filters.DateFilter(
        field_name='created_at', lookup_expr='date'
    )
    time = filters.TimeFilter(
        field_name='created_at',
        lookup_expr='range',
        method='filter_time_range'
    )
    created_at = filters.DateTimeFilter(field_name='created_at')

    class Meta:
        model = OfferRequest
        fields = ['date', 'time', 'created_at']

    def filter_time_range(self, queryset, name, value):
        start_time = datetime.combine(
            datetime.today(), value) - timedelta(seconds=30)
        end_time = datetime.combine(
            datetime.today(), value) + timedelta(seconds=30)
        return queryset.filter(created_at__range=(start_time, end_time))
