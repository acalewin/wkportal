from django.conf.urls import patterns, url
from wanikani import views

urlpatterns = patterns('',
  #url(r'^$', views.index, name='index'),
  url(r'^details/', views.details, name='details'),
  url(r'^setkey/', views.setkey, name='setkey'),
  url(r'^kanji/', views.kanji, name='kanji'),
  url(r'^vocab/', views.vocab, name='vocab'),
)
