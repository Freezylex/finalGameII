from django.http import Http404
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .models import Player
from Game.repository.repository import Repository
import numpy as np

# game_1 = Repository(np.arange(1,4,1))
# print(game_1.data)
# game_1.choice(1,
#            ["bank","bank","sosed"],
#            ["bank","sosed","sosed"]
#            )
#
# print(game_1.gamble(1))


def index(request):
    try:
        pass
    except:
        raise Http404('Что-то пошло не так')
    return render(request, "player/authorization.html")


def to_MainWindow(request):
    try:
        pass
    except:
        raise Http404('Что-то пошло не так')
    return render(request, "player/mainWindow.html")


def to_top_players(request):
    try:
        pass
    except:
        raise Http404('Что-то пошло не так')
    return render(request, "player/statistica.html")


def to_personal_page(request):
    try:
        player = Player(Name=request.POST['user'])
        player.save()
        players = Player.objects.all() # TODO sort palyers according their effectivness during the game
    except:
        raise Http404('Что-то пошло не так')
    return render(request, "player/Personal Page.html", {'player': player, 'players': players})

def to_admin_page(request):
    try:
        pass
    except:
        raise Http404('Что-то пошло не так')
    return render(request, "player/AdminPage.html")