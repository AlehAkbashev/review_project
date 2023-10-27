from rest_framework import serializers
import datetime as dt

from reviews.models import Categories, Genres, Title, Comment, Review


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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Review
        fields = '__all__'
