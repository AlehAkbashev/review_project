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

User = get_user_model()


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
        if year > year + 1:
            raise serializers.ValidationError("Check year of title")
        return value


class GenreTitleSerializer(serializers.ModelSerializer):
    # title_id = serializers.SlugRelatedField(many=False, read_only=True, slug_field='title_name')
    class Meta:
        fields = '__all__'
        model = TitleGenre


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
            raise serializers.ValidationError(
                "You don't have permission to change ROLE"
            )
        return value
