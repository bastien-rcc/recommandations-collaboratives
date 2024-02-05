from rest_framework import permissions, viewsets
from urbanvitaliz.utils import has_perm
from .serializers import ResourceSerializer
from . import models


########################################################################
# REST API
########################################################################


class IsResourceManagerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to ...
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return has_perm(request.user, "sites.manage_resources", request.site)


class ResourceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows resources to be listed or edited
    """

    def get_queryset(self):
        qs = models.Resource.on_site
        if not has_perm(self.request.user, "sites.manage_resources", self.request.site):
            qs = qs.filter(status__gt=models.Resource.TO_REVIEW)
        return qs.order_by("-created_on", "-updated_on")

    serializer_class = ResourceSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsResourceManagerOrReadOnly,
    ]


# eof
