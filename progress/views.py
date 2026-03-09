from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Avg, Count, Q
from assignments.models import Submission
from attendance.models import Attendance
from users.models import User

class ProgressView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        submissions = Submission.objects.filter(student=user, score__isnull=False)
        avg_score = submissions.aggregate(avg=Avg('score'))['avg'] or 0

        total = Attendance.objects.filter(student=user).count()
        present = Attendance.objects.filter(student=user, status='present').count()
        attendance_percent = round((present / total * 100), 1) if total > 0 else 0

        return Response({
            'average_score': round(avg_score, 1),
            'attendance_percent': attendance_percent,
            'submissions_count': submissions.count(),
        })

class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role not in ['admin']:
            return Response({'detail': 'Нет доступа'}, status=403)

        students = User.objects.filter(role='student').annotate(
            avg=Avg('submissions__score'),
            total_attendance=Count('attendances'),
            present_attendance=Count('attendances', filter=Q(attendances__status='present'))
        ).values('id', 'full_name', 'avg', 'total_attendance', 'present_attendance')

        return Response({'students': list(students)})
