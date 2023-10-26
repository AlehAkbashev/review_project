from rest_framework import serializers
import datetime as dt

from reviews.models import Genres, Categories, Title


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
