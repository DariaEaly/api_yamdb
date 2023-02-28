from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from reviews.models import Review, Comment, Title
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.db.models import Avg


class TitleSerializer(serializers.ModelSerializer):

    rating = serializers.SerializerMethodField(
        required=False
    )

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(Avg('score'))['score__avg']


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
