from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab
from celery.decorators import periodic_task

from games.models import *

'''
Runs Every 20 minutes
from 8 a.m to 10 p.m
'''
@periodic_task(run_every = crontab(minute="*/20", hour="8-22"))
def make_new_games():
	Cards.objects.create()
	Tiles.objects.create()
	print "New Game Started"