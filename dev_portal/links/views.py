from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from links.models import Link
from django.views import generic
from django.core import serializers
from django.http import HttpResponse

class LinkView(generic.DetailView):
  model=Link
  template_name = 'links/details.html'

# Create your views here.
@login_required
def index(request):
  l = Link.objects.filter(user=request.user)
  #l = Link.objects.all()
  context  = {'list': l}
  return render(request, 'links/index.html', context)

@login_required
def list(request):
  return HttpResponse(
            serializers.serialize('json',
              Link.objects.filter(user=request.user)),
            content_type='application/json')
