from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    owner = models.TextField()

    
# Create your models here.
