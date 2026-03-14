from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import UserViewSets

router = DefaultRouter()
router.register(r'users', UserViewSets, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
