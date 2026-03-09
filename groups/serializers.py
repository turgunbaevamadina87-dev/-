from rest_framework import serializers
from .models import Group, StudentProfile

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = ['teacher']

    def create(self, validated_data):
        # Учитель автоматически = текущий пользователь
        validated_data['teacher'] = self.context['request'].user
        return super().create(validated_data)

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'
        read_only_fields = ['user', 'enrollment_date']