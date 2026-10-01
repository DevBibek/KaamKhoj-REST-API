from infrastructure.jobs.models import Job
import django_filters
class JobFilters(django_filters.FilterSet):
    min_salary = django_filters.NumberFilter(
        field_name="salary",
        lookup_expr="gte"
    ),
    
    max_salary = django_filters.NumberFilter(
        field_name="salary",
        lookup_expr= "lte"
    )
    class Meta:
        model = Job
        fields =[
            "location",
            "is_active",
            "title",
            "company",
            "salary"
        ]