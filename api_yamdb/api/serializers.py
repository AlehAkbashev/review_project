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
from rest_framework.validators import UniqueTogetherValidator

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
        try:
            category_obj = Categories.objects.get(slug=data)
        except Categories.DoesNotExist:
            raise serializers.ValidationError('This category does not exist')
        return category_obj


class GenreField(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genres

    def to_internal_value(self, data):
        try:
            genre_obj = Genres.objects.get(slug=data)
        except Genres.DoesNotExist:
            raise serializers.ValidationError('This genre does not exist')
        return {'name': genre_obj.name, 'slug': genre_obj.slug}


class TitleSerializer(serializers.ModelSerializer):
    category = CategoryField()
    genre = GenreField(many=True)
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        model = Title

    def validate_year(self, value):
        current_year = dt.date.today().year
        if value > current_year + 1:
            raise serializers.ValidationError("Check year of title")
        return value

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre = Genres.objects.get(slug=genre['slug'])
            TitleGenre.objects.create(title_id=title, genre_id=current_genre)
        return title

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        if 'genre' in validated_data:
            genre_list = []
            genres = validated_data.pop('genre')
            for genre in genres:
                current_genre = Genres.objects.get(slug=genre['slug'])
                genre_list.append(current_genre)
            instance.genre.set(genre_list)
        instance.save()
        return instance

    def get_rating(self, obj):
        title = Title.objects.get(pk=obj.id)
        rating = Review.objects.filter(title=title).aggregate(Avg('score'))
        return rating['score__avg']


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
            'pub_date',
        )
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        print(self.context)
        title = Title.objects.get(pk=self.context['title_id'])
        try:
            Review.objects.get(title=title)
            raise serializers.ValidationError('You cannot write more than one review on the same title')
        except Review.DoesNotExist:
            return attrs


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

