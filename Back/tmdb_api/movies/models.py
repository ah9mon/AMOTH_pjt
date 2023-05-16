from django.db import models

# Create your models here.
class Movie(models.Model):
    movie_id = models.IntegerField()
    title = models.TextField()
    overview = models.TextField()
    release_date = models.TextField()
    poster_path = models.TextField()