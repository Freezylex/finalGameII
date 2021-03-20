from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# from .static.hard.banking import Repository
# Create your views here.

from django.shortcuts import render
from .models import Player, Active, Factor, Admin
from Game.repository.repository import Repository, Factory
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


def to_MainWindow(request, player):
    try:
        player = Player.objects.get(Name=player)
        # player.save()
        players = Player.objects.order_by('-Active_a').order_by('-Active_b')
        actives = Active.objects.all()[:player.Day + 2]
    except:
        raise Http404('Что-то пошло не так в to Main menue')
    return render(request, "player/mainWindow.html", {'player': player, 'players': players,
                                                      'actives' : actives})


def to_top_players(request, player_nam):
    try:
        player = Player.objects.get(Name=player_nam)
        # player.save()
        players = Player.objects.order_by('-Active_a').order_by('-Active_b')

    except:
        raise Http404('Что-то пошло не так')
    return render(request, "player/statistica.html", {'player': player, 'players': players})


def to_personal_page(request):
    try:
        a = Player.objects.filter(Name=request.POST['user'])
        if len(a) == 0:
            player = Player(Name=request.POST['user'])
            player.save()
        else:
            player = a[0]
        players = Player.objects.order_by('-Active_a').order_by('-Active_b')
    except:
        raise Http404('Что-то пошло не так')
    return render(request, "player/Personal Page.html", {'player': player, 'players': players})


def next_step(request, play):
    try:
        player = Player.objects.get(Name=play)
        # player.save()
        players = Player.objects.order_by('-Active_a').order_by('-Active_b')
        flag = Admin.objects.order_by('-Day')[0].Day
        print(flag)
        if player.Day == flag:
            pass
    except:
        raise Http404('Что-то пошло не так oooo')
    return render(request, "player/Personal Page.html", {'player': player, 'players': players})



def make_choice(request, player_name):
    try:
        player = Player.objects.get(Name=player_name)
        day = list(Admin.objects.all())[-1:][0].Day
        # player.save()
        players = Player.objects.order_by('Active_a').order_by('Active_b')
        actives = Active.objects.all()[:day + 2]
        a = list(dict(request.POST.items()).keys())[1:]
        if len(a) == 2:
            a.sort(key=lambda x: x[0], reverse=True)    # now the first in pair is activeA in russian and etc
            print(a)
            print(set([i.Name for i in actives]))
            print(Factor.objects.all())
            act_a = Active.objects.get(Name__startswith=a[0])
            act_b = Active.objects.get(Name_eng__startswith=a[1])
            user_factors = Factor(Name1=act_a, Name2=act_b, Day=day, UserID=player)
            # print('we are here')
            factor = Factor.objects.filter(Day=day, UserID=player)
            if len(factor) != 0:
                print(factor)
                factor.delete()
                # print('factors deleted')
                print(Factor.objects.all())
            user_factors.save()
            # player.NextYear()
            # player.Active_a += 220
            # player.Active_b += 20
            # player.save()
    except Active.DoesNotExist:
        day = list(Admin.objects.all())[-1:][0].Day
        player = Player.objects.get(Name=player_name)
        # player.save()
        players = Player.objects.order_by('-Active_a').order_by('-Active_b')
        actives = Active.objects.all()[:day + 2]
    except:
        raise Http404('Что-то пошло не так в make_chio')
    return render(request, "player/mainWindow.html", {'player': player, 'players': players,
                                                      'actives': actives})

# def to_M(request, player_name):
#     try:
#         player = Player.objects.get(Name=player_name)
#         # player.save()
#         players = Player.objects.all()  # TODO sort palyers according their effectivness during the game
#         actives = Active.objects.all()[:player.Day + 2]
#     except:
#         raise Http404('Что-то пошло не так в to Main menue')
#     return render(request, "player/mainWindow.html", {'player': player, 'players': players,
#                                                       'actives' : actives})


def next_day(request):
    try:
        day = Admin.objects.order_by('-Day')[0].Day
        user_factors = Factor.objects.filter(Day=day)
        players = Player.objects.all()
        actves = Active.objects.all()
        for i in user_factors:
            print(i)
        #сразу же меняем день
        new_day = Admin(Day=day + 1)
        # new_day.save()
    except:
        raise Http404('Что-то пошло не так в to Main menue')
    return None


factory = Factory()


def next_day_admin(request, year):
    try:
        flag = True
        day = list(Admin.objects.all())[-1:][0].Day
        day1 = day
        Admin.objects.all().delete()
        user_factors = Factor.objects.filter(Day=day)
        players = Player.objects.all()
        actives = Active.objects.all() # todo допилить админскую страничку
        actves = Active.objects.all()
        for i in user_factors:
            print(i)
        #сразу же меняем день
        if int(year) == 1000:
            if day == 0:
                day += 1
            new_day = Admin(Day=day - 1)
        else:
            new_day = Admin(Day=day + 1)
        new_day.save()
        day = new_day.Day

        # now make calculations:
        if int(year) != 1000:
            k = sorted(user_factors, key=lambda x: x.UserID.ID)
            idshniki = [i.UserID.ID for i in k]
            game1 = factory.get_repository(idshniki)
            if len(idshniki) < len(game1.id_):
                flag = False
                p = game1.id_
                list_of_actives_a = []
                list_of_actives_b = []
                dict_k = {el.UserID.ID: el for el in k}
                k = []
                for i in game1.id_:
                    k.append(Player.objects.get(ID__exact=i))
                    if i in dict_k:
                        elem = dict_k[i]
                        list_of_actives_a.append(elem.Name1.Name_eng)
                        list_of_actives_b.append(elem.Name2.Name_eng)
                    else:
                        list_of_actives_a.append('bank')
                        list_of_actives_b.append('bank')

                ch = game1.Choice(day1,
                                  list_of_actives_a,
                                  list_of_actives_b
                             )
            else:
                a = [i.Name1.Name_eng for i in k]
                b = [i.Name2.Name_eng for i in k]
                print(b)
                print(game1.id_)
                print(day1)
                ch = game1.Choice(day1,
                             [i.Name1.Name_eng for i in k],
                             [i.Name2.Name_eng for i in k]
                             )
                print(ch)
            print('sdf')
            ar = game1.Gamble(day1)
            print('fdsf')
            i = 0
            actA = 'asset_1_' + str(day1)
            actB = 'asset_2_' + str(day1)
            for a, b in ar[[actA, actB]].to_numpy():
                user = k[i]
                if flag:
                    user = user.UserID
                user.NextYear(a.round(), b.round())
                user.save()
                i += 1


    except:
        raise Http404('Что-то пошло не так в to Main menue')
    return render(request, "player/AdminPage.html", {'user_factors': user_factors, 'actives': actives,
                                                     'players': players, 'day': day})


def to_admin_page(request):
    try:
        day = list(Admin.objects.all())[-1:][0].Day
        user_factors = Factor.objects.filter(Day=day)
        players = Player.objects.all()
        actives = Active.objects.all() # todo допилить админскую страничку
    except:
        raise Http404('Что-то пошло не так в to_admin_page')
    return render(request, "player/AdminPage.html", {'user_factors': user_factors, 'actives': actives,
                                                     'players': players, 'day': day})

