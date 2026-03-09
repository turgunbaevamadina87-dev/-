from django.db import models

from django.db import models
from users.models import User
from groups.models import Group

class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'present', 'Present'
        ABSENT = 'absent', 'Absent'
        LATE = 'late', 'Late'

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PRESENT)

    class Meta:
        unique_together = ('student', 'date', 'group')  # нельзя дважды отметить одного студента

    def __str__(self):
        return f"{self.student.username} — {self.date} — {self.status}"
