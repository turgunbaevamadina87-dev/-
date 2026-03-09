from django.shortcuts import render

from rest_framework import viewsets, permissions
from .models import Group, StudentProfile
from .serializers import GroupSerializer, StudentProfileSerializer
from users.models import User

class IsAdminOrTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role in ['admin', 'teacher']

class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    permission_classes = [IsAdminOrTeacher]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Group.objects.all()
        elif user.role == 'teacher':
            return Group.objects.filter(teacher=user)
        else:  # student
            return Group.objects.filter(students__user=user)

class StudentProfileViewSet(viewsets.ModelViewSet):
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return StudentProfile.objects.all()
        return StudentProfile.objects.filter(user=user)
