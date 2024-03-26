from django.db import models

# Create your models here.
class Student(models.Model):
    def __str__(self):
        return self.name
    
    name = models.CharField(default="", max_length=30)
    age = models.IntegerField(default=0)
    major = models.CharField(default="", max_length=100)
    github = models.CharField(default="", max_length=200)