from django.shortcuts import render

from rest_framework import viewsets, permissions, generics
from rest_framework.exceptions import PermissionDenied
from .models import Assignment, Submission
from .serializers import AssignmentSerializer, SubmissionSerializer, SubmissionCheckSerializer

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'

class AssignmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['group']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Assignment.objects.all()
        elif user.role == 'teacher':
            return Assignment.objects.filter(created_by=user)
        else:  # student
            return Assignment.objects.filter(group__students__user=user)

    def perform_create(self, serializer):
        if self.request.user.role not in ['teacher', 'admin']:
            raise PermissionDenied("Только преподаватель может создавать задания.")
        serializer.save()

class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'assignment']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Submission.objects.all()
        elif user.role == 'teacher':
            return Submission.objects.filter(assignment__created_by=user)
        else:
            return Submission.objects.filter(student=user)

    def partial_update(self, request, *args, **kwargs):
        # Только учитель может проверять
        if request.user.role not in ['teacher', 'admin']:
            raise PermissionDenied("Только преподаватель может проверять задания.")
        return super().partial_update(request, *args, **kwargs)
