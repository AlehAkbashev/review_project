from rest_framework import filters, mixins, viewsets

from api.permissions import ReaderOrAdmin


class CategoryGenreMixin(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    permission_classes = (ReaderOrAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
