from django.urls import path
from .views import ProgressView, DashboardView

urlpatterns = [
    path('progress/', ProgressView.as_view()),
    path('dashboard/', DashboardView.as_view()),
]