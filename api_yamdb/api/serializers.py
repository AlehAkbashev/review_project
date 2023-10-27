from rest_framework import serializers
from .models import Categories, Genres, Title, Comment, Review


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer()
    genre = GenresSerializer(many=True)

    class Meta:
        model = Title
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Review
        fields = '__all__'
