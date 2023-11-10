from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class GenresSerializer(serializers.ModelSerializer):
    """
    Сериализатор жанров.
    """

    class Meta:
        fields = ("name", "slug")
        model = Genre


class CategoriesSerializer(serializers.ModelSerializer):
    """
    Сериализатор категорий.
    """

    class Meta:
        fields = ("name", "slug")
        model = Category


class TitleWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для записи произведений.
    """

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )

    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
        )
        model = Title

    def to_representation(self, instance):
        title = TitleReadSerializer(instance)
        return title.data


class TitleReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения произведений.
    """

    category = CategoriesSerializer()
    genre = GenresSerializer(many=True)
    rating = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )
        model = Title


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор комментария.
    """

    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Review.
    """

    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Review
        fields = (
            "id",
            "text",
            "author",
            "score",
            "pub_date",
        )

    def validate(self, data):
        """
        Проверяет данные сериализатора.
        """
        data = super().validate(data)
        if self.context["request"].method == "POST":
            title = get_object_or_404(Title, pk=self.context["title_id"])
            if Review.objects.filter(
                title=title, author=self.context["request"].user
            ).exists():
                raise serializers.ValidationError(
                    "You cannot write more than one review on the same title"
                )
        return data


class UsersSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User.
    """

    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = User

    def validate_role(self, value):
        """
        Проверяет роль пользователя.
        """
        if (
            self.context.get("request").method == "PATCH"
            and not self.context.get("request").user.is_admin
        ):
            return self.context.get("request").user.role
        return value


class UserRegistrationSerializer(serializers.Serializer):
    """
    Сериализатор для регистрации пользователя.
    """

    username = serializers.SlugField(
        max_length=settings.USERNAME_MAX_LENGTH,
        required=True
    )
    email = serializers.EmailField(
        max_length=settings.EMAIL_MAX_LENGTH,
        required=True
    )

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError("You cannot use Me for username")
        return value

    def validate(self, data):
        user_with_username = User.objects.filter(
            username=data["username"]
        ).first()
        user_with_email = User.objects.filter(email=data["email"]).first()
        if user_with_username:
            if not user_with_email:
                raise serializers.ValidationError(
                    {"username": "This username is already used"}
                )
        elif user_with_email != user_with_username:
            raise serializers.ValidationError(
                {
                    "username": "This username is already used",
                    "email": "This email is already used",
                }
            )
        elif not user_with_username and user_with_email:
            raise serializers.ValidationError(
                {"email": "This email is already used"}
            )
        return data


class MyTokenObtainPairSerializer(serializers.Serializer):
    username = serializers.SlugField(
        max_length=settings.USERNAME_MAX_LENGTH, required=True
    )
    confirmation_code = serializers.CharField(required=True)
