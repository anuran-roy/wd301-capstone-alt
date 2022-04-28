from django_filters import rest_framework as filters

from .models import Task


class TaskFilters(filters.FilterSet):
    status = filters.CharFilter(field_name="status__title")
    
    class Meta:
        model = Task
        fields = [
            "status"
        ]

