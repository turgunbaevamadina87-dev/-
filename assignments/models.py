from django.db import models

from django.db import models
from users.models import User
from groups.models import Group

class Assignment(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assignments')

    def __str__(self):
        return self.title

class Submission(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = 'submitted', 'Submitted'
        CHECKED = 'checked', 'Checked'
        REJECTED = 'rejected', 'Rejected'

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='submissions/')
    comment = models.TextField(blank=True)
    score = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUBMITTED)

    def __str__(self):
        return f"{self.student.username} — {self.assignment.title}"
