from __future__ import absolute_import

from celery import shared_task
from wanikani.views import Pynikani
from wanikani.models import Kanji, KanjiStatus
from datetime import datetime
from django.db.utils import IntegrityError
import pytz

@shared_task
def get_kanji(user):
  """This will retrieve the kanji from the WK API up to the calling user's max
  level, in groups of 10 levels"""
  key = user.wkuser.apikey
  kanji_list = []

  if key:
    pyni = Pynikani(apikey=key)
    max_lev = int(pyni.user_information()['level'])
    user.wkuser.level = max_lev
    user.wkuser.save()
    lev = 1
    while max_lev > lev:
      kanji_list += pyni.kanji(','.join([str(l) for l in range(lev,lev+10)]))
      lev += 10
    kanji_list += pyni.kanji(','.join([str(l) for l in range(lev,max_lev+1)]))

  for c in kanji_list:
    kanji = Kanji.objects.filter(character=c['character']).first()
    if kanji is None:
      kanji = Kanji(
        character=c['character'],
        meaning=c['meaning'],
        onyomi=c['onyomi'] or '',
        kunyomi=c['kunyomi'] or '',
        important_reading=c['important_reading'],
        level=c['level'],
        )
      kanji.save()

    if c.get('user_specific'):
      kanji_stats = KanjiStatus.objects.filter(kanji=kanji, user=user.wkuser).first()
      if kanji_stats is None:
        kanji_stats = KanjiStatus(
          kanji=kanji,
          user=user.wkuser,
          srs=c['user_specific']['srs'],
          burned=c['user_specific']['burned']
        )
      else:
        # same as above, unique constraints
        kanji_stats = KanjiStatus.objects.filter(kanji=kanji, user=user.wkuser).first()
        kanji_stats.srs = c['user_specific']['srs']
        kanji_stats.burned = c['user_specific']['burned']
      kanji_stats.save()

  user.wkuser.kanji_refresh=datetime.now(pytz.utc)
  user.wkuser.save()

@shared_task
def get_vocab(user):
  """This will retrieve the vocab from the WK API up to the calling user's max
  level, in groups of 10 levels"""
  key = user.wkuser.apikey
  vocab_list = []
  if key:
    pyni = Pynikani(apikey=key)
    max_lev = int(pyni.user_information()['level'])
    user.wkuser.level = max_lev
    user.wkuser.save()
    lev = 1
    while max_lev > lev:
      vocab_list += pyni.vocab(','.join([str(l) for l in range(lev,lev+10)]))
      lev += 10
    vocab_list += pyni.vocab(','.join([str(l) for l in range(lev,max_lev+1)]))


  for c in vocab_list:
    vocab = Vocab.objects.filter(character=c['character']).first()
    if vocab is None:
      vocab = Vocab(
        character=c['character'],
        meaning=c['meaning'],
        kana=c['kana'] or '',
        level=c['level'],
        )
      vocab.save()

    if c.get('user_specific'):
      vocab_stats = VocabStatus.objects.filter(vocab=vocab, user=user.wkuser).first()
      if vocab_stats is None:
        vocab_stats = VocabStatus(
          vocab=vocab,
          user=user.wkuser,
          srs=c['user_specific']['srs'],
          burned=c['user_specific']['burned']
        )
      else:
        # same as above, unique constraints
        vocab_stats = KanjiStatus.objects.filter(kanji=kanji, user=user.wkuser).first()
        vocab_stats.srs = c['user_specific']['srs']
        vocab_stats.burned = c['user_specific']['burned']
      vocab_stats.save()

  user.wkuser.vocab_refresh=datetime.now(pytz.utc)
  user.wkuser.save()
