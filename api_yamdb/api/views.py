from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from reviews.models import Category, Comment, Genre, Review, Title

from .filters import TitleFilter
from .permissions import AdminAccess, CommentReviewPermission, ReaderOrAdmin
from .serializers import (CategoriesSerializer, CommentSerializer,
                          GenresSerializer, MeSerializer,
                          MyTokenObtainPairSerializer, ReviewSerializer,
                          TitleSerializer, UserRegistrationSerializer,
                          UsersSerializer)
from .service import send_email

User = get_user_model()


class GenresViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (ReaderOrAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class CategoriesViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
    permission_classes = (ReaderOrAdmin,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (ReaderOrAdmin,)
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ["get", "post", "patch", "delete"]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, AdminAccess)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    http_method_names = ["post", "patch", "delete", "get"]
    lookup_field = "username"

    @action(
        detail=False,
        methods=["get", "patch"],
        url_path="me",
        permission_classes=[
            IsAuthenticated,
        ],
        serializer_class=MeSerializer,
    )
    def get_patch_me_user(self, request):
        if request.method == "PATCH":
            serializer = MeSerializer(
                request.user,
                data=request.data,
                context={"request": request},
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = MeSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (CommentReviewPermission,)
    http_method_names = ["get", "post", "patch", "delete"]

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(review=review, author=self.request.user)

    def perform_update(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(review=review, author=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    permission_classes = (CommentReviewPermission,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"title_id": self.kwargs.get("title_id")})
        return context

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = Title.objects.get(id=title_id)
        serializer.save(author=self.request.user, title=title)

    def perform_update(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = Title.objects.get(id=title_id)
        serializer.save(author=self.request.user, title=title)


@api_view(["POST"])
@permission_classes([AllowAny])
def user_registration(request):
    try:
        user = User.objects.get(
            email=request.data.get("email"),
            username=request.data.get("username"),
        )
        send_email(request.data.get("email"), user)
        return Response(request.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email = serializer.data.get("email")
        username = serializer.data.get("username")
        user = User.objects.get(email=email, username=username)
        send_email(request.data.get("email"), user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = MyTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            user = User.objects.get(username=username)
            refresh = RefreshToken.for_user(user)
            return Response(
                {"token": str(refresh.access_token)},
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
