from django.shortcuts import render

from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Attendance
from .serializers import AttendanceSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['student', 'group', 'date', 'status']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Attendance.objects.all()
        elif user.role == 'teacher':
            return Attendance.objects.filter(group__teacher=user)
        else:
            return Attendance.objects.filter(student=user)

    def perform_create(self, serializer):
        if self.request.user.role not in ['teacher', 'admin']:
            raise PermissionDenied("Только преподаватель может отмечать посещаемость.")
        serializer.save()
