from rest_framework import serializers
import datetime as dt
from pytils.translit import slugify

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
