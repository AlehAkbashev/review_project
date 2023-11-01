from rest_framework import (
    viewsets,
    pagination,
    status,
    filters
)
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .permissions import AdminAccess, ReaderOrAdmin
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
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TitleFilter

User = get_user_model()


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    pagination_class = PageNumberPagination
    permission_classes = (ReaderOrAdmin, )
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'delete']
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = pagination.PageNumberPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'
    permission_classes = (ReaderOrAdmin, )
    http_method_names = ['get', 'post', 'delete']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (ReaderOrAdmin,)
    filter_backends = (DjangoFilterBackend, )
    pagination_class = pagination.PageNumberPagination
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, AdminAccess)
    pagination_class = pagination.PageNumberPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
    http_method_names = ['post', 'patch', 'delete', 'get']
    lookup_field = "username"

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        serializer.save()
        user = User.objects.get(email=email)
        send_email(email, user)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=[IsAuthenticated,],
        serializer_class=MeSerializer
    )
    def get_patch_me_user(self, request):
        if request.method == 'PATCH':
            serializer = MeSerializer(
                request.user,
                data=request.data,
                context={'request': request},
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = MeSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(review=review, author=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)
