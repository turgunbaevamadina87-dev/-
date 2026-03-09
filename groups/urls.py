from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupViewSet, StudentProfileViewSet

router = DefaultRouter()
router.register('groups', GroupViewSet, basename='groups')
router.register('student-profiles', StudentProfileViewSet, basename='student-profiles')

urlpatterns = [path('', include(router.urls))]