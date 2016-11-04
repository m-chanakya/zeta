from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

class Board(models.Model):
	reward = models.PositiveIntegerField(default = 0)

	def __unicode__(self):
		return str(self.pk)

class Cell(models.Model):
	board = models.ForeignKey(Board)
	x = models.PositiveSmallIntegerField()
	y = models.PositiveSmallIntegerField()
	value = models.IntegerField(default = 0)
	lucky = models.BooleanField(default = False)

	def __unicode__(self):
		return str(self.board.pk), "(", str(self.x), ",", str(self.y), ")"

class Bet(models.Model):
	cell = models.ForeignKey(Cell)
	user = models.ForeignKey(User)
	value = models.PositiveIntegerField(default = 0)

	def __unicode__(self):
		return self.user.username, str(self.cell.board.pk), "(", str(self.cell.x), ",", str(self.cell.y), ")", str(self.bet)
