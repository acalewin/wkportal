from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from wanikani.models import WKUser
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.http import HttpResponse

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
    return render(request, 'wanikani/settings.html')
  else:
    try:
      request.user.wkuser
    except ObjectDoesNotExist:
      wk = WKUser(apikey=new_key, user=request.user)
      wk.save()

    request.user.wkuser.apikey = new_key
    request.user.wkuser.save()
  return render(request, 'wanikani/settings.html')

@login_required
def kanji(request):
  wkdata = request.user.wkuser

  if wkdata:
    key = wkdata.apikey
  else:
    return render(request, 'wanikani/error.html', {'error': "No key found"})

  pyni = Pynikani(apikey=key)
  return HttpResponse(
            serializers.serialize('json',
              pyni.kanji()),
            content_type='application/json')
