from django.urls import path, include
from .views import ReviewViewSet, CommentViewSet
from rest_framework import routers

v1_router = routers.DefaultRouter()

v1_router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet)
v1_router.register(r'titles/(?P<title_id>\d+)/reviews/'
                   r'(?P<review_id>\d+)/comments',
                   CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
