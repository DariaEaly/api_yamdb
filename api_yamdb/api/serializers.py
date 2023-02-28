from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import User
import re


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
            



class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)
    def validate_username(self, value):
        reg = re.compile(r'^[\w.@+-]+')
        if not reg.match(value):
            raise serializers.ValidationError(
                'Имя пользователя не совпадает с паттерном'
            )
        return value

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