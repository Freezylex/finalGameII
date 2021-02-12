from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from .static.hard.banking import Repository
# Create your views here.

from django.shortcuts import render
from .models import Player, Active, Factor
# from Game.repository.repository import Repository
import numpy as np

# game_1 = Repository(np.arange(1,4,1))
# print(game_1.data)
# game_1.choice(1,
#            ["bank","bank","sosed"],
#            ["bank","sosed","sosed"]
#            )
#
# print(game_1.gamble(1))

user_name = ['None']

repo = Repository()


def index(request):
    try:
        pass
    except:
        raise Http404('Что-то пошло не так')
    return render(request, "player/authorization.html")


def to_MainWindow(request):
    try:
        player = Player.objects.get(Name=user_name[0])
        # player.save()
        players = Player.objects.all()  # TODO sort palyers according their effectivness during the game
        actives = Active.objects.all()[:player.Day + 2]
    except:
        raise Http404('Что-то пошло не так')
    return render(request, "player/mainWindow.html", {'player': player, 'players': players,
                                                      'actives' : actives})


def to_top_players(request):
    try:
        player = Player.objects.get(Name=user_name[0])
        # player.save()
        players = Player.objects.all() # TODO sort palyers according their effectivness during the game

    except:
        raise Http404('Что-то пошло не так')
    return render(request, "player/statistica.html", {'player': player, 'players': players})


def to_personal_page(request):
    try:
        player = Player(Name=request.POST['user'])
        player.save()
        players = Player.objects.all() # TODO sort palyers according their effectivness during the game
        user_name[0] = request.POST['user']
    except:
        raise Http404('Что-то пошло не так')
    return render(request, "player/Personal Page.html", {'player': player, 'players': players})


def next_step(request):
    try:
        print('d')
        print(user_name[0])
        player = Player.objects.get(Name=user_name[0])
        print('d')
        # player.save()
        players = Player.objects.all() # TODO sort palyers according their effectivness during the game

    except:
        raise Http404('Что-то пошло не так oooo')
    return render(request, "player/Personal Page.html", {'player': player, 'players': players})

def to_admin_page(request):
    try:
        pass
    except:
        raise Http404('Что-то пошло не так')
    return render(request, "player/AdminPage.html")