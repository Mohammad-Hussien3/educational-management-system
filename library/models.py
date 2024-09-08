from django.db import models

# Create your models here.

class Article(models.Model):
    doctorId = models.IntegerField()
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=10000)

    def __str__(self):
        return self.title + ' ' + str(self.id)
