import datetime
import re

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title, User


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')

    def validate_username(self, value):
        reg = re.compile(r'^[\w.@+-]+')
        if not reg.match(value):
            raise serializers.ValidationError(
                'Имя пользователя не совпадает с паттерном'
            )
        return value


class NotAdminSerializer(UsersSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        reg = re.compile(r'^[\w.@+-]+')
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя не может быть "me"'
            )
        elif User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Пользователь уже есть'
            )
        elif not reg.match(value):
            raise serializers.ValidationError(
                'Имя пользователя не совпадает с паттерном'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = SlugRelatedField(slug_field='username', read_only=True)

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError('Минимум 1, максимум 10.')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Можно написать только 1 отзыв')
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('author', 'review')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField()

    class Meta:
        fields = '__all__'
        model = Title


class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug')
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True)

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        if value > datetime.date.today().year:
            raise serializers.ValidationError('Проверьте год выпуска')
        return value
