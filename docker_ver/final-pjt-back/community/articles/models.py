from django.db import models

# Create your models here.
class Article(models.Model):
    user_id = models.TextField()
    title = models.CharField(max_length=100)
    movie_title = models.TextField()
    music_title = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    user_id = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Like(models.Model):
    user_id = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)