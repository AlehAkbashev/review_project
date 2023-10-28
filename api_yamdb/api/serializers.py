from rest_framework import serializers
import datetime as dt

from django.contrib.auth import get_user_model

User = get_user_model()

from reviews.models import (
    Categories,
    Genres,
    GenreTitle,
    Title,
    Comment,
    Review,
)



class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genres


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Categories


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Title
    
    def validate_year(self, value):
        year = dt.date.today().year
        if year > year+1:
            raise serializers.ValidationError("Check year of title")
        return value


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
        fields = '__all__'
        model = User


class MeSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)
    
    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User
