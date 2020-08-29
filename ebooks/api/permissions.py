from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        # check if user is admin
        is_admin = super().has_permission(request, view)
        # return any http requests if they don't alter data (i.e 'SAFE_METHODS' like Get, Head, Options)
        # if not SAFE_METHOD, return if it is an admin request
        return request.method in permissions.SAFE_METHODS or is_admin


class IsReviewAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.review_author == request.user
