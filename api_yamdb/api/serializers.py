from typing import Any, Dict
from rest_framework import serializers
import datetime as dt

from django.contrib.auth import get_user_model
from reviews.models import (
    Categories,
    Genres,
    TitleGenre,
    Title,
    Comment,
    Review,
)
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken, Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genres


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Categories


class CategoryField(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Categories

    def to_internal_value(self, data):
        category_obj = get_object_or_404(Categories, slug=data)
        return category_obj
    
    def to_representation(self, instance):
        print(instance)
        return super().to_representation(instance)


class GenreField(serializers.ModelSerializer):
    
    class Meta:
        fields = ('name', 'slug')
        model = Genres

    def to_internal_value(self, data):
        genre_obj = Genres.objects.get(slug=data)
        return {'name': genre_obj.name, 'slug': genre_obj.slug}


class TitleSerializer(serializers.ModelSerializer):
    category = CategoryField()
    genre = GenreField(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if year > year + 1:
            raise serializers.ValidationError("Check year of title")
        return value

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre = Genres.objects.get(slug=genre['slug'])
            TitleGenre.objects.create(title_id=title, genre_id=current_genre)
        return title
    
    def get_rating(self, obj):
        title = Title.objects.get(pk=obj.id)
        rating = Review.objects.filter(title=title).aggregate(Avg('score'))
        return rating['score__avg']


class GenreTitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = TitleGenre


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date'
        )


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User


class MeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User

    def validate_role(self, value):
        if (
            self.context.get('request').user.role != 'admin'
            and not self.context.get('request').user.is_superuser
        ):
            return self.context.get('request').user.role
        return value
    

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('email', 'username')
        model = User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass

    # def __init__(self, *args, **kwargs) -> None:
    #     super().__init__(*args, **kwargs)
    #     self.fields['password'].required = False

    # @classmethod
    # def get_token(cls, user) -> Token:
    #     return RefreshToken.for_user(user)
    
    # def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
    #     attrs.update({'password': ''})
    #     print(self.initial_data)
    #     data = {}
    #     refresh = self.get_token(self.user)
    #     data['token'] = refresh
    #     return data

    # def validate(self, data):
    #     print(1)
    #     print(data)
    #     user = get_object_or_404(User, username=data['username'])
    #     if not default_token_generator.check_token(
    #         user,
    #         data['confirmation_code']
    #     ):
    #         raise serializers.ValidationError('Confirmation code does not match')
    #     return data
