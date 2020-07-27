from django_filters import rest_framework as filters

from .models import Like


class LikeFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter(field_name='created_at')

    class Meta:
        model = Like
        fields = ('date', )
