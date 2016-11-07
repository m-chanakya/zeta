from __future__ import unicode_literals
from django.db.models.signals import post_save

from django.contrib.auth.models import User
from django.db import models

class Cards(models.Model):
	ticket_cost = models.PositiveIntegerField(default=10)
	winner_prize = models.PositiveIntegerField(default=100)
	is_result_generated = models.BooleanField(default = False)
	created = models.DateTimeField(auto_now_add=True)

class CardCell(models.Model):
	SUITS = (
                ("C", "Clubs"),
                ("S", "Spades"),
                ("D", "Diamonds"),
                ("H", "Hearts")
        )
	VALUES = (
                ("J", "Jack"),
                ("Q", "Queen"),
                ("K", "King")
        )
	GROUPS = (
                ("A", "A"),
                ("B", "B"),
                ("C", "C")
        )
	game = models.ForeignKey(Cards, related_name = "cells")
	suit = models.CharField(max_length = 1, choices = SUITS)
	value = models.CharField(max_length = 1, choices = VALUES)
	group = models.CharField(max_length = 1, choices = GROUPS)
	total_bets = models.PositiveIntegerField(default=0)
	winner = models.BooleanField(default = False)

	class Meta:
		unique_together = ("game", "suit", "value", "group")

class CardBet(models.Model):
	user = models.ForeignKey(User)
	cell = models.ForeignKey(CardCell)
	no_of_tickets = models.PositiveIntegerField()

	def save(self, *args, **kwargs):
		if self.pk is None:
			self.cell.total_bets += self.no_of_tickets
			self.cell.save()
		return super(Profile, self).save(*args, **kwargs)


class Tiles(models.Model):
	ticket_cost = models.PositiveIntegerField(default=10)
	winner_prize = models.PositiveIntegerField(default=100)
	is_result_generated = models.BooleanField(default = False)
	created = models.DateTimeField(auto_now_add=True)

class TileCell(models.Model):
	SUITS = (
                ("A", "A"),
                ("B", "B"),
            )
	VALUES = (
                ("1", "1"),
                ("2", "2"),
                ("3", "3"),
                ("4", "4"),
                ("5", "5"),
        )
	GROUPS = (
                ("A", "A"),
                ("B", "B"),
                ("C", "C")
        )
	game = models.ForeignKey(Tiles, related_name = "cells")
	suit = models.CharField(max_length = 1, choices = SUITS)
	value = models.CharField(max_length = 1, choices = VALUES)
	group = models.CharField(max_length = 1, choices = GROUPS)
	total_bets = models.PositiveIntegerField(default=0)
	winner = models.BooleanField(default = False)

	class Meta:
		unique_together = ("game", "suit", "value", "group")

class TileBet(models.Model):
	user = models.ForeignKey(User)
	cell = models.ForeignKey(TileCell)
	no_of_tickets = models.PositiveIntegerField()

	def save(self, *args, **kwargs):
		if self.pk is None:
			self.cell.total_bets += self.no_of_tickets
			self.cell.save()
		return super(Profile, self).save(*args, **kwargs)


def create_card_cells(sender, instance, created, **kwargs):
    if created:
        for group in ["A", "B", "C"]:
        	for suit in ["C", "S", "D", "H"]:
        		for value in ["J", "Q", "K"]:
        			CardCell.objects.create(game = instance, group = group, suit = suit, value = value)

def create_tile_cells(sender, instance, created, **kwargs):
    if created:
        for group in ["A", "B", "C"]:
        	for suit in ["A", "B"]:
        		for value in ["1", "2", "3", "4", "5"]:
        			TileCell.objects.create(game = instance, group = group, suit = suit, value = value)


post_save.connect(create_card_cells, sender=Cards)
post_save.connect(create_tile_cells, sender=Tiles)