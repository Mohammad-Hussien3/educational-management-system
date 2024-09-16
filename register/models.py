from django.db import models
# Create your models here.

class User(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    Email = models.EmailField(unique=True)
    Password = models.CharField(max_length=100)
    Type = models.CharField(max_length=20, blank=True, null=True)
    verify = models.BooleanField(default=False)
    isAdmin = models.BooleanField(default=False)
    
    def __str__(self):
        return self.firstName + " " + self.lastName + " " + str(self.id)
    

class Doctor(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, unique=True)
    degrees = models.JSONField(default=list, blank=True)
    courseRequest = models.JSONField(default=list, blank=True)

    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, unique=True)
    degrees = models.JSONField(default=list, blank=True)
    

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, unique=True)
    requests = models.JSONField(default=list, blank=True)