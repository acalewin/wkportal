from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class WKUser(models.Model):
  apikey = models.CharField(max_length=50)
  user = models.OneToOneField(User)

class Kanji(models.Model):
  character = models.CharField(max_length=10)
  meaning = models.CharField(max_length=200)
  onyomi = models.CharField(max_length=10)
  kunyomi = models.CharField(max_length=10)
  important_reading = models.CharField(max_length=10)
  level = models.IntegerField()

class KanjiStatus(models.Model):
  user = models.OneToOneField(WKUser)
  Kanji = models.OneToOneField(Kanji)
  srs = models.CharField(max_length=20)
  burned = models.BooleanField()
