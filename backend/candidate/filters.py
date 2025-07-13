import django_filters

from .models import ApplicationStatus, Candidate, Department, StatusHistory


class CandidateFilter(django_filters.FilterSet):
    """Filter for candidates based on various criteria."""

    department = django_filters.ChoiceFilter(choices=Department.choices, help_text="Filter by department")
    status = django_filters.ChoiceFilter(
        field_name="current_status", choices=ApplicationStatus.choices, help_text="Filter by current application status"
    )

    class Meta:
        model = Candidate
        fields = {
            "full_name": ["exact", "icontains", "istartswith"],
            "email": ["exact", "icontains"],
            "department": ["exact"],
            "current_status": ["exact"],
        }


class StatusHistoryFilter(django_filters.FilterSet):
    """Filter for status history records."""

    candidate = django_filters.UUIDFilter(field_name="candidate__id", help_text="Filter by candidate ID")

    status = django_filters.ChoiceFilter(
        field_name="new_status", choices=ApplicationStatus.choices, help_text="Filter by status"
    )

    admin_name = django_filters.CharFilter(lookup_expr="icontains", help_text="Filter by admin name")

    created_after = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte", help_text="Status changes after this date"
    )

    created_before = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte", help_text="Status changes before this date"
    )

    class Meta:
        model = StatusHistory
        fields = ["candidate", "new_status", "admin_name", "created_at"]
