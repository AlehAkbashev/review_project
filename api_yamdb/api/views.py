from django.shortcuts import render
from rest_framework import viewsets
from .serializers import GenresSerializer, TitleSerializer, CategoriesSerializer
from reviews.models import Genres, Title, Categories


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = None


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
