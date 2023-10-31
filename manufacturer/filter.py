from rest_framework import filters


class UserNetworkFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        if user.is_authenticated:
            return queryset.filter(user=user)
        return queryset.none()
