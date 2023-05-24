from django.db import models

# Create your models here.
class User(models.Model):
    nickname = models.CharField(max_length=100)
    profile_image = models.TextField(null=True)
    email = models.TextField()

  

