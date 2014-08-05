from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Link(models.Model):
  title = models.CharField(max_length=250)
  added = models.DateTimeField('date added')
  url = models.CharField(max_length=512)
  user = models.ForeignKey(User)

  def __str__(self):
    return self.url
