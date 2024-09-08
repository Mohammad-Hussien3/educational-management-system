from rest_framework import serializers
from .models import User, Doctor, Student

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'firstName', 'lastName', 'Email', 'Password', 'Type', 'verify']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['user', 'degrees', 'courses']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['degrees']
    