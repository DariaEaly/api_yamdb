from django.urls import path, include
from .views import ReviewViewSet, CommentViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews/'
                r'(?P<review_id>\d+)/comments',
                CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
]
