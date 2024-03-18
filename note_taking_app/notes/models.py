from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        app_label = 'notes'

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    pinned = models.BooleanField(default=False)
    image = models.ImageField(upload_to='note_images/', null=True, blank=True)
    background_color = models.CharField(max_length=20, null=True, blank=True)
    tags = models.ManyToManyField(Tag)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)