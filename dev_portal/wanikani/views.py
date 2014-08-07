from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from wanikani.models import WKUser, KanjiStatus, VocabStatus, Sentence
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.http import HttpResponse
from datetime import timedelta, datetime
import wanikani.tasks
import pytz
import json

class Pynikani:
  def __init__(self, apikey):
    self.apikey = apikey

  def _call(self, resource, arg=None):
    """Consolidating making resource calls to the WK api"""
    if not self.apikey:
      self.error = "No API Key found"
      return None
    url = "https://www.wanikani.com/api/user/%s/%s" \
    % (self.apikey, resource)
    if arg:
      url += "/%s" % arg
    try:
      req = requests.get(url)
      req.raise_for_status()
      data = req.json()
    except requests.exceptions.ConnectionError:
      self.error = 'Conn Error'
      data = None
    except requests.exceptions.HTTPError as e:
      self.error = e.response.status_code
      data = None
    self.error = None
    return data

  def user_information(self):
    """User information call"""
    data = self._call(resource="user-information")
    return data['user_information']

  def study_queue(self):
    """Study queue call"""
    data = self._call(resource="study-queue")
    return data['requested_information']

  def level_progression(self):
    """Level progression call"""
    data = self._call(resource="level-progression")
    return data.get('requested_information')

  def srs_distribution(self):
    """SRS distribution call"""
    data = self._call(resource="srs-distribution")
    return data.get('requested_information')

  def recent_unlocks(self, limit=10):
    """Recent unlocks
limit: max number of items to return"""
    data = self._call(resource='recent-unlocks', arg=limit)
    return data.get('requested_information')

  def critical_items(self, thresh=75):
    """Critical items
thresh: threshold of percentage correct to use"""
    data = self._call(resource='critical-items', arg=thresh)
    return data.get('requested_information')

  def radicals(self, level=None):
    """radicals api call
level: level to retrieve radicals from"""
    data = self._call(resource='radicals', arg=level)
    return data.get('requested_information')

  def kanji(self, level=None):
    """kanji api call
level: level to retrieve kanji from"""
    data = self._call(resource='kanji', arg=level)
    if not data:
      return dict()
    return data.get('requested_information')

  def vocab(self, level=None):
    """vocabulary api call
level: level to retrieve vocab from"""
    data = self._call(resource='vocabulary', arg=level)
    retval = data.get('requested_information')
    if level or not retval: #This needs to be unwrapped, because for some reason
      return retval
    else:
      return retval.get('general')

  def grade_sentence_kanji(self, sent):
    """Grades a block of text passed in as sent and returns
    a list of dicts that are the character and the srs level based on the
    user's wanikani apikey"""
    grade = list()
    kanji_list = self.kanji()
    for c in sent:
      # known kanji information if any
      kanji_info = next((x for x in kanji_list if x['character'] == c), None)
      if not kanji_info: #we have no info for this kanji
        grade.append(dict(character=c, status=''))
        continue
      srs_status = None
      if 'user_specific' not in kanji_info:  # user hasn't seen this kanji
        grade.append(dict(character=c, status=''))
        continue
      srs_status = kanji_info['user_specific']['srs']
      grade.append(dict(character=c, status=srs_status))

    return grade

  def __str__(self):
    return self.user.username


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
