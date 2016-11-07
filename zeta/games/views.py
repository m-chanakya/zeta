from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from users.models import *
from games.models import *

import json
from django.http import HttpResponse

from django.utils import timezone
from datetime import timedelta

@login_required
def make_bet(request):
	if request.method == 'POST':
		data = request.POST
		response = {'status': 0, "msg": "Bet placed"}
		game_type = data.get("game", False)
		cell_id = data.get("cellid", False)
		no_of_tickets = data.get("tickets", False)
		if game_type and cell_id and no_of_tickets and game_type in ['cards', 'tiles']:
			if game_type == "cards":
				cell = CardCell.objects.filter(pk=cell_id)
				if cell.exists():
					cell = cell.first()
				else:
					response['status'] = 1
					response['msg'] = "Invaild Bet: Cell doesn't exist"
					return HttpResponse(json.dumps(response), content_type="application/json")
				start_time = cell.game.created
				end_time = start_time + timezone.timedelta(minutes = 20)
				cur_time = timezone.now()
				if cur_time >= start_time and cur_time < end_time:
					bet = CardBet.objects.create(user=request.user, cell = cell, no_of_tickets = no_of_tickets)
				else:
					response['status'] = 1
					response['msg'] = "Betting for this game is closed"
			elif game_type == "tiles":
				cell = TileCell.objects.filter(pk=cell_id)
				if cell.exists():
					cell = cell.first()
					bet = TileBet.objects.create(user=request.user, cell = cell, no_of_tickets = no_of_tickets)
				else:
					response['status'] = 1
					response['msg'] = "Invaild Bet: Cell doesn't exist"
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
		'date': game.created.strftime("%H:%M %Y:%M:%d")
	}

@user_passes_test(lambda u: u.is_superuser)
def view_games(request):
	if request.method == "GET":
		response = {'status': 0}
		games = []
		for each in Cards.objects.filter(is_result_generated = False).order_by("-created"):
			games.append(make_game_json(each, "cards"))
		for each in Tiles.objects.filter(is_result_generated = False).order_by("-created"):
			games.append(make_game_json(each, "tiles"))
		response['data'] = games
		return HttpResponse(json.dumps(response), content_type="application/json")

def view_results(request):
	if request.method == 'GET':
		response = {'status': 0}
		
		card_results = []
		for each in Cards.objects.filter(is_result_generated = True).order_by("-created"):
			winners = {}
			for every in each.cells.filter(winner=True):
				winners[every.group] = every.suit+" "+every.value
			result = {
				'created': each.created.strftime("%H:%M %Y:%M:%d"),
				'winners': winners
			}
			card_results.append(result)

		tile_results = []
		for each in Tiles.objects.filter(is_result_generated = True).order_by("-created"):
			winners = {}
			for every in each.cells.filter(winner=True):
				winners[every.group] = every.suit+" "+every.value
			result = {
				'created': each.created.strftime("%H:%M %Y:%M:%d"),
				'winners': winners
			}
			tile_results.append(result)

		response['data'] = {'cards': card_results, 'tiles': tile_results}
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
					if sum > 0:
						diff = 100
						ans = tuple()
						for eA in cells.filter(group = "A"):
							for eB in cells.filter(group = "B"):
								for eC in cells.filter(group  = "C"):
									win_percent = (eA.total_bets + eB.total_bets + eC.total_bets)*100/sum
									if ( win_percent <= percentage and percentage - win_percent <= diff):
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
			user = each.user
			user.points += each.no_of_tickets * each.cell.game.winner_prize
			user.save()
			winner.append({
				'user': user.username,
				'points': user.points
				})
		response['data']['winners'] = winners

		return HttpResponse(json.dumps(response), content_type="application/json")