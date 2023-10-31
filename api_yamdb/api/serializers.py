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
User = get_user_model()


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genres


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Categories


class GenreTitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genres


class GenreField(serializers.SlugRelatedField):

    def to_representation(self, value):
        print(value)
        return {
            'name': value.name,
            'slug': value.slug
        }

    def to_internal_value(self, data):
        genres_data = []
        for genre in data:
            current_genre = get_object_or_404(Genres, slug=genre)
            genres_data.append(
                {
                    "slug": current_genre.slug,
                    "name": current_genre.name
                }
            )
        return genres_data


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        required=True,
        queryset=Categories.objects.all(),
        slug_field='slug',
    )
    genre = GenreField(
        queryset = Genres.objects.all(),
        slug_field = 'slug',
        required = True
    )

    class Meta:
        exclude = ('id',)
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
            GenreTitle.objects.create(title_id=title, genre_id=current_genre)
        return title

class GenreTitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = GenreTitle


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Review
        fields = '__all__'


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
