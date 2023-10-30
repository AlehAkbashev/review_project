from rest_framework import (
    viewsets,
    pagination,
    status,
    permissions,
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .permissions import AdminAccess, UserMeAccess, ReaderOrAdmin
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
from users.service import send_email

User = get_user_model()


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [ReaderOrAdmin, AllowAny]
    pagination_class = PageNumberPagination

    def destroy(self, request, *args, **kwargs):
        genre = get_object_or_404(Genres, slug=self.kwargs.get('slug'))
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer

    permission_classes = (ReaderOrAdmin, AllowAny)

    # def create(self, request, *args, **kwargs):
    #     slug = self.kwargs.get('slug')
    #     return super().create(request, *args, **kwargs)



class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (ReaderOrAdmin, )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, AdminAccess)
    pagination_class = pagination.PageNumberPagination

    lookup_field = "username"

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        serializer.save()
        user = User.objects.get(email=email)
        send_email(email, user)


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def get_patch_me_user(request):
    if request.method == 'PATCH':
        user = get_object_or_404(
            User,
            username=request.user.username
        )
        serializer = MeSerializer(
            user,
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
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
