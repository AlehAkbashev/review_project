from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Comment, Genre, Review, Title

from .filters import TitleFilter
from .permissions import AdminAccess, CommentReviewPermission, ReaderOrAdmin
from .serializers import (CategoriesSerializer, CommentSerializer,
                          GenresSerializer,
                          MyTokenObtainPairSerializer, ReviewSerializer,
                          TitleSerializer, UserRegistrationSerializer,
                          UsersSerializer)
from .service import send_email
from django.db.models import Avg
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()


class CategoryGenreMixin(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin
):
    permission_classes = (ReaderOrAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(CategoryGenreMixin):
    serializer_class = GenresSerializer
    queryset = Genre.objects.all()


class CategoryViewSet(CategoryGenreMixin):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с произведениями.
    """

    permission_classes = (ReaderOrAdmin,)
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        return Title.objects.all().annotate(rating=Avg("reviews__score"))


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с пользователями.
    """

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
        serializer_class=UsersSerializer,
    )
    def get_patch_me_user(self, request):
        """
        Получение и обновление информации о текущем пользователе.
        """
        if request.method == "PATCH":
            serializer = UsersSerializer(
                request.user,
                data=request.data,
                context={"request": request},
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = UsersSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с комментариями.
    """

    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (CommentReviewPermission, IsAuthenticatedOrReadOnly)
    http_method_names = ["get", "post", "patch", "delete"]

    def perform_create(self, serializer):
        """
        Выполняет создание комментария.
        """
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(review=review, author=self.request.user)

    def perform_update(self, serializer):
        """
        Выполняет обновление комментария.
        """
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(review=review, author=self.request.user)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        return review.comments.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с отзывами.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    permission_classes = (CommentReviewPermission, IsAuthenticatedOrReadOnly)

    def get_serializer_context(self):
        """
        Возвращает контекст сериализатора.
        """
        context = super().get_serializer_context()
        context.update({"title_id": self.kwargs.get("title_id")})
        return context

    def perform_create(self, serializer):
        """
        Выполняет создание отзыва.
        """
        title_id = self.kwargs.get("title_id")
        title = Title.objects.get(id=title_id)
        serializer.save(author=self.request.user, title=title)

    def perform_update(self, serializer):
        """
        Выполняет обновление отзыва.
        """
        title_id = self.kwargs.get("title_id")
        title = Title.objects.get(id=title_id)
        serializer.save(author=self.request.user, title=title)


@api_view(["POST"])
@permission_classes([AllowAny])
def user_registration(request):
    """
    Регистрация пользователя.

    Parameters:
    - request: Запрос с данными пользователя.

    Returns:
    - Response: Ответ с данными пользователя или ошибкой.

    Raises:
    - User.DoesNotExist: Если пользователь не существует.
    - UserRegistrationSerializer.ValidationError:
    Если данные пользователя некорректны.
    """
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get("email")
    username = serializer.validated_data.get("username")
    user_one = User.objects.filter(username=username)
    user_two = User.objects.filter(email=email)
    check_user_email = user_one == user_two
    only_email = (
        User.objects.filter(email=email)
        and not User.objects.filter(username=username)
    )
    only_username = (
        User.objects.filter(username=username)
        and not User.objects.filter(email=email)
    )
    if not check_user_email:
        return Response(
            {
                "username": "This username may be already used",
                "email": "This email may be already used"
            }
            status=status.HTTP_400_BAD_REQUEST
        )
    user, created = User.objects.get_or_create(
        email=serializer.validated_data.get("email"),
        username=serializer.validated_data.get("username"),
    )
    send_email(request.data.get("email"), user)
    return Response(request.data, status=status.HTTP_200_OK)


class MyTokenObtainPairView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = MyTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        confirmation_code = serializer.validated_data.get("confirmation_code")
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                {"error": "Confirmation code does not match"},
                status=status.HTTP_400_BAD_REQUEST
            )
        refresh = RefreshToken.for_user(user)
        return Response(
            {"token": str(refresh.access_token)}
        )
