from rest_framework import serializers
from django.utils import timezone
from .models import Assignment, Submission

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'
        read_only_fields = ['created_by']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ['student', 'status', 'score']

    def validate(self, data):

        assignment = data.get('assignment')
        if assignment and assignment.deadline < timezone.now():
            raise serializers.ValidationError("Дедлайн истёк! Нельзя сдать задание.")
        return data

    def create(self, validated_data):
        validated_data['student'] = self.context['request'].user
        return super().create(validated_data)

class SubmissionCheckSerializer(serializers.ModelSerializer):
    """Только для преподавателя — проверка работы"""
    class Meta:
        model = Submission
        fields = ['score', 'status']