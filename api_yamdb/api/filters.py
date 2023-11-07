from django_filters import rest_framework as filters
from reviews.models import Title


class TitleFilter(filters.FilterSet):
    """
    Фильтр для модели Title.

    Позволяет фильтровать записи по категории, жанру, году и имени.
    """

    category = filters.CharFilter(field_name="category__slug")
    genre = filters.CharFilter(field_name="genre__slug")

    class Meta:
        fields = ("category", "genre", "year", "name")
        model = Title
