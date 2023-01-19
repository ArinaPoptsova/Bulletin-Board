import django_filters

from bulletins.models import Response


class ResponseFilter(django_filters.FilterSet):
    bulletin__title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Response
        fields = ('bulletin__title',)
