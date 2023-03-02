from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Review, Title, User
from django.urls import reverse

from .permissions import (AdminOnly, IsAdminUserOrReadOnly,
                          IsAuthorAdminModeratorOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetTokenSerializer,
                          NotAdminSerializer, ReviewSerializer,
                          SignUpSerializer, TitleReadSerializer, UsersSerializer, TitlePostSerializer)
from .utils import generate_confirmation_code, send_confirmation_code


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, AdminOnly,)
    lookup_field = 'username'
    search_fields = ('username', )
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, )
    http_method_names = ['get', 'patch', 'delete', 'post']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UsersSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class APIGetToken(APIView):
    """Получаем токен"""
    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)


class APISignup(APIView):
    """Регистрирует пользователя и отправляет ему код подтверждения."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        is_valid = serializer.is_valid()
        if request.data.get('username') == 'me':
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(username=request.data.get('username'),
                               email=request.data.get('email')).exists():
            user = User.objects.get(
                username=request.data.get('username'),
                email=request.data.get('email')
            )
            user.confirmation_code = generate_confirmation_code()
            user.save()
            return Response('Token refresh', status=status.HTTP_200_OK)
        if is_valid:
            email = request.data.get('email')
            username = request.data.get('username')
            User.objects.create_user(email=email, username=username)
            confirmation_code = generate_confirmation_code()
            User.objects.filter(email=email).update(
                confirmation_code=confirmation_code
            )
            send_confirmation_code(email, confirmation_code)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination
    lookup_field='slug'


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination
    lookup_field='slug'


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'name', 'year')
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = Title.objects.all()
        genre = self.request.query_params.get('genre')
        category = self.request.query_params.get('category')
        if genre is not None:
            queryset = queryset.filter(genre__slug=genre)
        if category is not None:
            queryset = queryset.filter(category__slug=category)
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return  TitleReadSerializer
        return TitlePostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):

        review_id = self.kwargs.get('review_id')

        new_queryset = Comment.objects.filter(review=review_id)
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
        super(CommentViewSet, self).perform_update(serializer)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        new_queryset = Review.objects.filter(title=title_id)
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
