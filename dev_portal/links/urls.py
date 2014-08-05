from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from links import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
  url(r'^details/(?P<pk>\d+)', login_required(views.LinkView.as_view()), name='details'),
  url(r'^list/', views.list, name='list'),
)
