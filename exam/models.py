from django.db import models

# Create your models here.
    
class Exam(models.Model):
    doctorId = models.IntegerField()
    questions = models.JSONField(default=list)
    degrees = models.JSONField(default=list)
    answers = models.JSONField(default=list)

    def __str__(self):
        return f'exam {self.id}'