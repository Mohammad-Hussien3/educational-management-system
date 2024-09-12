from django.db import models
from register.models import Doctor, Student
# Create your models here.

class Course(models.Model):
    courseName = models.CharField(max_length=60)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='courses')
    registeredStudents = models.ManyToManyField(Student, related_name='courses', blank=True)
    contents = models.JSONField(default=list, blank=True)