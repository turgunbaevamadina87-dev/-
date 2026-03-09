from django.db import models

from django.db import models
from users.models import User

class Group(models.Model):
    class Level(models.TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED = 'advanced', 'Advanced'

    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='teaching_groups')
    level = models.CharField(max_length=20, choices=Level.choices, default=Level.BEGINNER)
    start_date = models.DateField()

    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name='students')
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} — {self.group}"
