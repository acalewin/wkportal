from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class WKUser(models.Model):
  apikey = models.CharField(max_length=50)
  kanji_refresh = models.DateTimeField()
  vocab_refresh = models.DateTimeField()
  user = models.OneToOneField(User)
  level = models.IntegerField(default=1)

  def grade_sentence_kanji(self, sent):
    """Grades a block of text passed in as sent and returns
    a list of dicts that are the character and the srs level based on the
    user's wanikani apikey"""
    grade = list()
    for c in sent:
      k=Kanji.objects.filter(character=c).first()
      if k:
        stat = KanjiStatus.objects.filter(user=self, kanji=k).first()
      else:
        stat = None
      if stat:
        grade.append(dict(character=c, status=stat.srs))
      else:
        grade.append(dict(character=c, status=''))
    return grade

  def __str__(self):
    return self.user.username

class Kanji(models.Model):
  character = models.CharField(max_length=50, unique=True)
  meaning = models.CharField(max_length=200)
  onyomi = models.CharField(max_length=50, default='')
  kunyomi = models.CharField(max_length=50, default='')
  important_reading = models.CharField(max_length=50)
  level = models.IntegerField()

  def __str__(self):
    return self.character

class KanjiStatus(models.Model):
  user = models.ForeignKey(WKUser)
  kanji = models.ForeignKey(Kanji)
  srs = models.CharField(max_length=20)
  burned = models.BooleanField()

  def __str__(self):
    return "%s - %s" % (str(self.user), str(self.kanji))


  class Meta:
    unique_together = (('user', 'kanji'),)

class Vocab(models.Model):
  character = models.CharField(max_length=10, unique=True)
  meaning = models.CharField(max_length=200)
  kana = models.CharField(max_length=10, default='')
  level = models.IntegerField()

  def __str__(self):
    return self.character

class VocabStatus(models.Model):
  user = models.ForeignKey(WKUser)
  vocab = models.ForeignKey(Vocab)
  srs = models.CharField(max_length=20)
  burned = models.BooleanField()

  def __str__(self):
    return "%s - %s" % (str(self.user), str(self.vocab))

  class Meta:
    unique_together = (('user', 'vocab'),)
