from django.core.mail import EmailMessage
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import  User

from .permissions import (AdminModeratorAuthorPermission, AdminOnly,
                          IsAdminUserOrReadOnly)
from .serializers import (GetTokenSerializer,
                          NotAdminSerializer,
                          SignUpSerializer,
                          UsersSerializer)
from .utils import generate_confirmation_code, send_confirmation_code


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, AdminOnly,)
    lookup_field = 'username'
    search_fields = ('username', )

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
    """
    Получение JWT-токена в обмен на username и confirmation code.
    Права доступа: Доступно без токена. Пример тела запроса:
    {
        "username": "string",
        "confirmation_code": "string"
    }
    """
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


# class APISignup(APIView):
#     permission_classes = (permissions.AllowAny,)
#     @staticmethod
#     def send_email(data):
#         email = EmailMessage(
#             subject=data['email_subject'],
#             body=data['email_body'],
#             to=[data['to_email']]
#         )
#         email.send()

#     def post(self, request):
#         serializer = SignUpSerializer(data=request.data)
#         serializer.is_valid()
#         email = serializer.validated_data.get('email')
#         username = serializer.validated_data.get('username')
#         if serializer.is_valid():
#             confirmation_code = generate_confirmation_code()
#             # user = User.objects.filter(email=email, username=username).exists()
#             user, created = User.objects.get_or_create(email=email)
#             if created is False:
#                 if user.username == username:
#                     user.confirmation_code = confirmation_code
#                     user.save()
#                     return Response('Token refresh', status=status.HTTP_200_OK)
#                 else:
#                     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#             return Response(
#                 serializer.data,
#                 status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class APISignup(APIView):
    """Регистирирует пользователя и отправляет ему код подтверждения."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        is_valid =  serializer.is_valid()
        if request.data.get('username') == 'me':
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=request.data.get('username'),
                               email=request.data.get('email')).exists():
            user = User.objects.get(username=request.data.get('username'),
                               email=request.data.get('email'))
            user.confirmation_code = generate_confirmation_code()
            user.save()
            return Response('Token refresh', status=status.HTTP_200_OK)
        if is_valid:
            email = request.data.get('email')
            username = request.data.get('username')
            User.objects.create_user(email=email, username=username)
            confirmation_code = generate_confirmation_code()
            User.objects.filter(email=email).update(
                confirmation_code = confirmation_code)
            send_confirmation_code(email, confirmation_code)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
