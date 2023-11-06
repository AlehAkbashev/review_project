import datetime as dt
from typing import Dict

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre
from django.core.validators import RegexValidator

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


class CategoryField(serializers.RelatedField):
    """
    Поле для сериализации категории.
    """

    class Meta:
        fields = ("name", "slug")
        model = Category

    def to_representation(self, instance):
        return {"name": instance.name, "slug": instance.slug}

    def to_internal_value(self, data):
        try:
            category_obj = Category.objects.get(slug=data)
        except Category.DoesNotExist:
            raise serializers.ValidationError("This category does not exist")
        return category_obj

    def get_queryset(self):
        return Category.objects.all()


class GenreField(serializers.RelatedField):
    """
    Поле для сериализации жанра.
    """

    class Meta:
        fields = ("name", "slug")
        model = Genre

    def to_representation(self, instance):
        return {"name": instance.name, "slug": instance.slug}

    def to_internal_value(self, data):
        try:
            genre_obj = Genre.objects.get(slug=data)
        except Genre.DoesNotExist:
            raise serializers.ValidationError("This genre does not exist")
        return {"name": genre_obj.name, "slug": genre_obj.slug}

    def get_queryset(self):
        return Genre.objects.all()


class TitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор тайтлов.
    """

    category = CategoryField()
    genre = GenreField(many=True)
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

    def create(self, validated_data):
        """
        Создает новый тайтл.
        """

        genres = validated_data.pop("genre")
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre = Genre.objects.get(slug=genre["slug"])
            TitleGenre.objects.create(title_id=title, genre_id=current_genre)
        return title

    def update(self, instance, validated_data):
        """
        Обновляет информацию о тайтле.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.year = validated_data.get("year", instance.year)
        instance.description = validated_data.get(
            "description", instance.description
        )
        instance.category = validated_data.get("category", instance.category)
        if "genre" in validated_data:
            genre_list = []
            genres = validated_data.pop("genre")
            for genre in genres:
                current_genre = Genre.objects.get(slug=genre["slug"])
                genre_list.append(current_genre)
            instance.genre.set(genre_list)
        instance.save()
        return instance


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
                title=title,
                author=self.context["request"].user
            ).exists():
                raise serializers.ValidationError(
                    "You cannot write more than one review on the same title"
                )
            return data
        if self.context["request"].method == "PATCH":
            return data

    def update(self, instance, validated_data):
        """
        Обновляет экземпляр модели Review.
        """
        instance.text = self.validated_data.get("text", instance.text)
        instance.score = self.validated_data.get("score", instance.score)
        instance.save()
        return instance


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
    username = serializers.SlugField(max_length=150)
    email = serializers.EmailField(max_length=254)

    def validate(self, data):
        if data["username"] == "me":
            raise serializers.ValidationError(
                "You cannot use Me for username"
            )
        return data


class MyTokenObtainPairSerializer(serializers.Serializer):
    username = serializers.SlugField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     """
#     Сериализатор для получения токена доступа.
#     """

#     confirmation_code = serializers.CharField(required=True)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["password"].required = False

#     def validate(self, data) -> Dict[str, str]:
#         """
#         Проверяет данные сериализатора.
#         """

#         username = data.get("username")
#         confirmation_code = data.get("confirmation_code")
#         user = get_object_or_404(User, username=username)
#         if not default_token_generator.check_token(user, confirmation_code):
#             raise serializers.ValidationError(
#                 {"error": "Your confirmation_code does not match"}
#             )
#         return data
