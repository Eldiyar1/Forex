import django_filters
from .models import Schedule


class ScheduleFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name="date", input_formats=['%d.%m.%Y'], lookup_expr="exact", label="Дата")

    class Meta:
        model = Schedule
        fields = ('date',)
