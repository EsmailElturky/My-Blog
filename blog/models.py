from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(null=True, max_length=100)
    photo = models.ImageField(upload_to='profiles_photos/')

    def __str__(self):
        return self.name


class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='posts_photos/')
    content = models.TextField()

    def __str__(self):
        return self.title
