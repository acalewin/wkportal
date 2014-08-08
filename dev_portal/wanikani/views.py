from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from wanikani.models import WKUser, KanjiStatus, VocabStatus, Sentence
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.http import HttpResponse
from datetime import timedelta, datetime
import wanikani.tasks
from wanikani.pynikani import Pynikani
import pytz
import json

# Create your views here.
@login_required
def details(request):
  return render(request, 'wanikani/settings.html')

@login_required
def setkey(request):
  #set the apikey for the user

  try:
    new_key = request.POST['apikey']
  except (KeyError):
    return HttpResponse(
      json.dumps(
        {'error': 'No API key found user'}),
        content_type='application/json')
  else:
    try:
      request.user.wkuser
    except ObjectDoesNotExist:
      wk = WKUser(apikey=new_key, user=request.user,
        kanji_refresh=datetime(1900,1,1), vocab_refresh=datetime(1900,1,1))
      wk.save()

    request.user.wkuser.apikey = new_key
    request.user.wkuser.save()
  return HttpResponse(
    json.dumps(
      {'success': 'Key Saved'}),
      content_type='application/json')

@login_required
def kanji(request, ):
  wkdata = request.user.wkuser

  if wkdata:
    key = wkdata.apikey
  else:
    return HttpResponse(
      json.dumps(
        {'error': 'No API key found user'}),
        content_type='application/json')

  if datetime.now(pytz.utc) - wkdata.kanji_refresh > timedelta(minutes=30):
    wanikani.tasks.get_kanji.delay(request.user)
    # message = 'Task queue for background.'

  return HttpResponse(
              serializers.serialize('json',
              KanjiStatus.objects.filter(user=request.user.wkuser)),
              content_type='application/json')

@login_required
def vocab(request):
  wkdata = request.user.wkuser

  if wkdata:
    key = wkdata.apikey
  else:
    return HttpResponse(
      serializers.serialize('json',
        {'error': 'No API key found user'}),
        content_type='application/json')

  if datetime.now(pytz.utc) - wkdata.vocab_refresh > timedelta(minutes=30):
    wanikani.tasks.get_vocab.delay(request.user)
    return HttpResponse("Job queued as a background task")
  else:
    return HttpResponse(
              serializers.serialize('json',
                VocabStatus.objects.filter(user=request.user.wkuser)),
              content_type='application/json')

@login_required
def counts(request):
  pass

def gradekanji(request):
  graded_sentence = None
  sentence = None
  try:
    sentence = request.POST['sentence']
  except (KeyError):
    return HttpResponse(json.dumps(
      {'error': 'No sentence to parse'}),
      content_type='application/json')
  apikey = None
  if request.user.is_authenticated():
      try:
        wkinfo = request.user.wkuser
        apikey = wkinfo.apikey
        return HttpResponse(json.dumps(
          wkinfo.grade_sentence_kanji(sentence)),
          content_type='application/json')
      except (ObjectDoesNotExist):
        pass #Swallow this, we'll try the POST object next

  if not apikey:
        try:
          apikey = request.POST['apikey']
        except (KeyError):
          return HttpResponse(json.dumps(
            {'error': 'No apikey to use'}),
            content_type='application/json')
  return HttpResponse(json.dumps(
          Pynikani(apikey).grade_sentence_kanji(sentence)),
          content_type='application/json')

@login_required
def savesentence(request):
  sentence = None
  try:
    sentence = request.POST['sentence']
  except (KeyError):
    return HttpResponse(json.dumps(
      {'error': 'No sentence to save'}),
      content_type='application/json')

  s = Sentence(user=request.user.wkuser, sentence=sentence)
  s.save()
  return HttpResponse(json.dumps({
    'message': 'Sentence saved'
  }), content_type='application/json')

@login_required
def delsentence(request):
  sentence = None
  try:
    sentence = request.POST['sentence']
  except (KeyError):
    return HttpResponse(json.dumps(
      {'error': 'No sentence to delete'}),
      content_type='application/json')

  s = Sentence.objects.get(pk=sentence)
  if s:
    s.destroy()
  return HttpResponse(json.dumps({
    'message': 'Sentence deleted'
  }), content_type='application/json')


@login_required
def listsentences(request, ):
  wkdata = request.user.wkuser

  return HttpResponse(
              serializers.serialize('json',
              Sentence.objects.filter(user=request.user.wkuser)),
              content_type='application/json')
