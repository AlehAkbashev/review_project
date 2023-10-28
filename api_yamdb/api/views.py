import csv
from rest_framework import (
  viewsets, 
  generics, 
  views, 
  mixins, 
  status,
  permissions,
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .permissions import AdminAccess
from .serializers import (
  GenresSerializer, 
  TitleSerializer, 
  CategoriesSerializer, 
  CommentSerializer,
  ReviewSerializer,
  UsersSerializer, 
  MeSerializer,
)
from reviews.models import (
  Genres, 
  Title, 
  Categories, 
  Comment,
  Review,
)

User = get_user_model()


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = permissions.AllowAny


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = permissions.AllowAny


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, AdminAccess)


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def get_patch_me_user(request):

    if request.method == 'PATCH':
        user = get_object_or_404(User, username=request.user.username)
        serializer = MeSerializer(user, data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    user = get_object_or_404(User, username=request.user.username)
    serializer = MeSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

  
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

