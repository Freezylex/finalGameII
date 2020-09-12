from django.http import Http404
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render


def index(request):
    return render(request, "player/statistica.html")

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
        pass
    except:
        raise Http404('Что-то пошло не так')
    return render(request, "player/Personal Page.html")
