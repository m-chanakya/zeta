from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from users.models import *
from games.models import *

import json
from django.http import HttpResponse

from django.utils import timezone
from datetime import timedelta

@login_required
def latest_cards_game(request):
	if request.method == "GET":
		cards = Cards.objects.filter(is_result_generated=False).order_by("-created").first()
		card_game = {'id': cards.id, 'created': cards.created.strftime("%H:%M %Y:%m:%d")}
		return HttpResponse(json.dumps(card_game), content_type="application/json")	

@login_required	
def latest_tiles_game(request):
	if request.method == "GET":
		tiles = Tiles.objects.filter(is_result_generated=False).order_by("-created").first()
		tile_game = {'id': tiles.id, 'created': tiles.created.strftime("%H:%M %Y:%m:%d")}
		return HttpResponse(json.dumps(tile_game), content_type="application/json")

@login_required
def make_bet(request):
	if request.method == 'POST':
		data = request.POST
		response = {'status': 0, "msg": "Bet placed"}
		game_type = data.get("game", False)
		game_id = data.get("gameid", False)
		cell_id = data.get("cellid", False)
		no_of_tickets = int(data.get("tickets", False))

		print game_type, game_id, cell_id, no_of_tickets

		if game_type and cell_id and no_of_tickets and no_of_tickets > 0 and game_id and game_type in ['cards', 'tiles']:
			try:
				group, suit, value = cell_id[1:].split('-')
			except:
				response['status'] = 1
				response['msg'] = "Invalid cell chosen"
				return HttpResponse(json.dumps(tile_game), content_type="application/json")
			if game_type == "cards":
				game = Cards.objects.filter(pk = game_id)
				if game.exists():
					game = game.first()
				else:
					response['status'] = 1
					response['msg'] = "Invaild Bet: Game doesn't exist"
					return HttpResponse(json.dumps(response), content_type="application/json")

				cell = CardCell.objects.filter(game = game, group = group, suit = suit, value = value)
				if cell.exists():
					cell = cell.first()
				else:
					response['status'] = 1
					response['msg'] = "Invaild Bet: Cell doesn't exist"
					return HttpResponse(json.dumps(response), content_type="application/json")

				start_time = cell.game.created
				end_time = start_time + timezone.timedelta(minutes = 20)
				cur_time = timezone.now()

				print "TIME", timezone.now()

				if cur_time >= start_time and cur_time < end_time:
					cost_of_tickets = no_of_tickets*cell.game.ticket_cost
					if cost_of_tickets <= request.user.profile.points:
						bet = CardBet.objects.create(user=request.user, cell = cell, no_of_tickets = no_of_tickets)
						response['msg'] = "Bet has been placed"
						response['data'] = {
							'user_id': bet.user.id,
							'points_left': bet.user.profile.points,
							'cell': bet.cell.group + " " + bet.cell.suit + " " + bet.cell.value,
							'game': bet.cell.game.id,
							'no_of_tickets': bet.no_of_tickets
						}
					else:
						response['status'] = 1
						response['msg'] = "You don't have enough money buy these tickets"
				else:
					response['status'] = 1
					response['msg'] = "Betting for this game is closed"
			
			elif game_type == "tiles":

				game = Tiles.objects.filter(pk = game_id)
				if game.exists():
					game = game.first()
				else:
					response['status'] = 1
					response['msg'] = "Invaild Bet: Game doesn't exist"
					return HttpResponse(json.dumps(response), content_type="application/json")

				cell = TileCell.objects.filter(game = game, group = group, suit = suit, value = value)
				if cell.exists():
					cell = cell.first()
				else:
					response['status'] = 1
					response['msg'] = "Invaild Bet: Cell doesn't exist"
					return HttpResponse(json.dumps(response), content_type="application/json")

				start_time = cell.game.created
				end_time = start_time + timezone.timedelta(minutes = 20)
				cur_time = timezone.now()

				print "TIME", cur_time

				if cur_time >= start_time and cur_time < end_time:
					cost_of_tickets = no_of_tickets*cell.game.ticket_cost
					print "TICKET COST", cost_of_tickets
					print "USER POINTS", request.user.profile.points
					if cost_of_tickets <= request.user.profile.points:
						bet = TileBet.objects.create(user=request.user, cell = cell, no_of_tickets = no_of_tickets)
						response['msg'] = "Bet has been placed"
						response['data'] = {
							'user_id': bet.user.id,
							'points_left': bet.user.profile.points,
							'cell': bet.cell.group + " " + bet.cell.suit + " " + bet.cell.value,
							'game': bet.cell.game.id,
							'no_of_tickets': bet.no_of_tickets
						}
					else:
						response['status'] = 1
						response['msg'] = "You don't have enough money buy these tickets"
				else:
					response['status'] = 1
					response['msg'] = "Betting for this game is closed"

		else:
			response['status'] = 1
			response['msg'] = "Invalid Bet"
		return HttpResponse(json.dumps(response), content_type="application/json")

def get_latest_game_time(request):
	if request.method == "GET":
		response = {'status': 0}

def make_game_json(game, type):
	return {
		'id': game.id,
		'type': type,
		'date': game.created.strftime("%H:%M %Y:%m:%d")
	}

@user_passes_test(lambda u: u.is_superuser)
def view_games(request):
	if request.method == "GET":
		response = {'status': 0}
		games = []
		for each in Cards.objects.filter(is_result_generated = False).order_by("created"):
			games.append(make_game_json(each, "cards"))
		for each in Tiles.objects.filter(is_result_generated = False).order_by("created"):
			games.append(make_game_json(each, "tiles"))
		response['data'] = games
		return HttpResponse(json.dumps(response), content_type="application/json")

def view_results(request):
	if request.method == 'GET':
		card_results = []
		for each in Cards.objects.filter(is_result_generated = True).order_by("-created"):
			winners = {}
			for every in each.cells.filter(winner=True):
				winners[every.group] = every.suit+" "+every.value
			result = {
				'created': each.created.strftime("%H:%M %Y:%m:%d"),
				'winners': winners
			}
			card_results.append(result)

		tile_results = []
		for each in Tiles.objects.filter(is_result_generated = True).order_by("-created"):
			winners = {}
			for every in each.cells.filter(winner=True):
				winners[every.group] = every.suit+" "+every.value
			result = {
				'created': each.created.strftime("%H:%M %Y:%m:%d"),
				'winners': winners
			}
			tile_results.append(result)

		response = {'cards' : card_results, 'tiles' : tile_results}
		print response
		return HttpResponse(json.dumps(response), content_type="application/json")

@user_passes_test(lambda u: u.is_superuser)
def generate_result(request):
	if request.method == 'POST':
		data = request.POST
		response = {'status': 0, "msg": "Result Generated"}
		game_type = data.get("game_type", False)
		game_id = data.get("game_id", False)
		result_type = data.get("result_type", False)
		print data
		if game_type and game_id and result_type and game_type in ["cards", "tiles"] and result_type in ["auto", "manual"]:

			if game_type == "cards":
				game = Cards.objects.filter(is_result_generated=False).filter(pk=game_id)
			elif game_type == "tiles":
				game = Tiles.objects.filter(is_result_generated=False).filter(pk=game_id)
			else:
				response['status'] = 1
				response['msg'] = "Invalid Game Type"
				return HttpResponse(json.dumps(response), content_type="application/json")
			
			if game.exists():
				game = game.first()
				cells = game.cells

			else:
				response['status'] = 1
				response['msg'] = "Game doesn't exist"
				return HttpResponse(json.dumps(response), content_type="application/json")

			if result_type == "auto":
				percentage = data.get("percentage", False)
				percentage = int(percentage)
				if percentage and percentage > 0 and percentage <= 100:
					sum = 0
					for each in cells.filter():
						sum += each.total_bets
					print "Total Bets", sum
					if sum > 0:
						diff = 100
						ans = tuple()
						for eA in cells.filter(group = "A"):
							for eB in cells.filter(group = "B"):
								for eC in cells.filter(group  = "C"):
									win_percent = (eA.total_bets + eB.total_bets + eC.total_bets)*100/sum
									if win_percent != 0:
										print win_percent, eA, eB, eC
									if ( win_percent <= percentage and percentage - win_percent <= diff):
										diff = percentage - win_percent
										ans = (eA, eB, eC)
						cellA, cellB, cellC = ans
					else:
						response['status'] = 1
						response['msg'] = "No bets have been placed"
						return HttpResponse(json.dumps(response), content_type="application/json")
				else:
					response['status'] = 1
					response['msg'] = "Invalid Percentage"
					return HttpResponse(json.dumps(response), content_type="application/json")

			elif result_type == "manual":
				a_winner = data.get("A", False)
				b_winner = data.get("B", False)
				c_winner = data.get("C", False)
				if a_winner and b_winner and c_winner:
					try:
						sA, vA = a_winner.split()
						sB, vB = b_winner.split()
						sC, vC = c_winner.split()
					except:
						response['status'] = 1
						response['msg'] = "Bad Request: Invalid cell chosen"
						return HttpResponse(json.dumps(response), content_type="application/json")
					cellA = cells.filter(group = "A", suit = sA, value = vA)
					cellB = cells.filter(group = "B", suit = sB, value = vB)
					cellC = cells.filter(group = "C", suit = sC, value = vC)
					if cellA.exists() and cellB.exists() and cellC.exists():
						cellA = cellA.first()
						cellB = cellB.first()
						cellC = cellC.first()
					else:
						response['status'] = 1
						response['msg'] = "Bad Request: Invalid cell chosen"
						return HttpResponse(json.dumps(response), content_type="application/json")
				else:
					response['status'] = 1
					response['msg'] = "Bad Request: Send data for all groups"
					return HttpResponse(json.dumps(response), content_type="application/json")
		else:
			response['status'] = 1
			response['msg'] = "Bad Request"
			return HttpResponse(json.dumps(response), content_type="application/json")


		#DECLARE WINNING CELLS
		game.is_result_generated = True
		game.save()
		cellA.winner = cellB.winner = cellC.winner = True
		cellA.save()
		cellB.save()
		cellC.save()
		response['data'] = {
			"A": cellA.suit+cellA.value,
			"B": cellB.suit+cellB.value,
			"C": cellC.suit+cellC.value,
		}

		#PAY THE WINNERS
		winners = []
		if game_type == "cards":
			bets = CardBet.objects.filter(cell__in = [cellA, cellB, cellC])
		else:
			bets = TileBet.objects.filter(cell__in = [cellA, cellB, cellC])

		for each in bets:
			print each.user.username
			profile = each.user.profile
			profile.points += each.no_of_tickets * each.cell.game.winner_prize
			profile.save()
			winners.append({
				'user': profile.user.username,
				'points': profile.points
				})
		response['data']['winners'] = winners

		return HttpResponse(json.dumps(response), content_type="application/json")