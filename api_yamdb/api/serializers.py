import datetime as dt
from typing import Dict

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre

User = get_user_model()


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genre


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Category


class CategoryField(serializers.RelatedField):
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
    category = CategoryField()
    genre = GenreField(many=True)
    rating = serializers.SerializerMethodField(read_only=True)

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

    def validate_year(self, value):
        current_year = dt.date.today().year
        if value > current_year + 1:
            raise serializers.ValidationError("Check year of title")
        return value

    def create(self, validated_data):
        genres = validated_data.pop("genre")
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre = Genre.objects.get(slug=genre["slug"])
            TitleGenre.objects.create(title_id=title, genre_id=current_genre)
        return title

    def update(self, instance, validated_data):
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

    def get_rating(self, obj):
        title = Title.objects.get(pk=obj.id)
        rating = Review.objects.filter(title=title).aggregate(Avg("score"))
        return rating["score__avg"]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")


class ReviewSerializer(serializers.ModelSerializer):
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
        data = super().validate(data)
        try:
            title = get_object_or_404(Title, pk=self.context["title_id"])
            Review.objects.get(
                title=title, author=self.context["request"].user
            )
            if self.context["request"].method == "PATCH":
                return data
            raise serializers.ValidationError(
                "You cannot write more than one review on the same title"
            )
        except Review.DoesNotExist:
            return data

    def update(self, instance, validated_data):
        instance.text = self.validated_data.get("text", instance.text)
        instance.score = self.validated_data.get("score", instance.score)
        instance.save()
        return instance


class UsersSerializer(serializers.ModelSerializer):
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


class MeSerializer(serializers.ModelSerializer):
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
        if (
            self.context.get("request").user.role != "admin"
            and not self.context.get("request").user.is_superuser
        ):
            return self.context.get("request").user.role
        return value


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("email", "username")
        model = User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].required = False

    def validate(self, data) -> Dict[str, str]:
        username = data.get("username")
        confirmation_code = data.get("confirmation_code")
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError(
                {"error": "Your confirmation_code does not match"}
            )
        return data
