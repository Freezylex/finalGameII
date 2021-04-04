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
        rating = list(players).index(player) + 1
        actives = Active.objects.all()[:player.Day + 2]
    except:
        raise Http404('Что-то пошло не так в to Main menue')
    return render(request, "player/mainWindow.html", {'player': player, 'players': players,
                                                      'actives': actives, 'rating': rating})


def to_top_players(request, player_nam):
    try:
        player = Player.objects.get(Name=player_nam)
        # player.save()
        players = Player.objects.order_by('-Active_a').order_by('-Active_b')
        rating = list(players).index(player) + 1
        user_choices = []
        if player.Day == 1:
            user_choices.append('На данном месте появятся резульаты сделанных вами инвестиций')
        else:
            data = factory.repo
            if data:
                pass

            else:
                user_choices.append('err in data. repository is not initialised')





    except:
        raise Http404('Что-то пошло не так')
    return render(request, "player/statistica.html", {'player': player, 'players': players, 'rating': rating})


def to_personal_page(request):
    try:
        a = Player.objects.filter(Name=request.POST['user'])
        if len(a) == 0:
            player = Player(Name=request.POST['user'])
            player.save()
        else:
            player = a[0]
        players = Player.objects.order_by('-Active_a').order_by('-Active_b')
        rating = list(players).index(player) + 1
    except:
        raise Http404('Что-то пошло не так')
    return render(request, "player/Personal Page.html", {'player': player, 'players': players, 'rating': rating})


def next_step(request, play):
    try:
        player = Player.objects.get(Name=play)
        # player.save()
        players = Player.objects.order_by('-Active_a').order_by('-Active_b')
        rating = list(players).index(player) + 1
        flag = Admin.objects.order_by('-Day')[0].Day
        print(flag)
        if player.Day == flag:
            pass
    except:
        raise Http404('Что-то пошло не так oooo')
    return render(request, "player/Personal Page.html", {'player': player, 'players': players, 'rating': rating})


def make_choice(request, player_name):
    try:
        player = Player.objects.get(Name=player_name)
        day = list(Admin.objects.all())[-1:][0].Day
        # player.save()
        players = Player.objects.order_by('Active_a').order_by('Active_b')
        rating = list(players).index(player) + 1
        actives = Active.objects.all()[:day + 2]
        a = list(dict(request.POST.items()).keys())[1:]
        if len(a) == 2:
            a.sort(key=lambda x: x[0], reverse=True)  # now the first in pair is activeA in russian and etc
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
        rating = list(players).index(player) + 1
        actives = Active.objects.all()[:day + 2]
    except:
        raise Http404('Что-то пошло не так в make_chio')
    return render(request, "player/mainWindow.html", {'player': player, 'players': players,
                                                      'actives': actives, 'rating': rating})


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
        # сразу же меняем день
        new_day = Admin(Day=day + 1)
        # new_day.save()
    except:
        raise Http404('Что-то пошло не так в to Main menue')
    return None


factory = Factory()


def next_day_admin(request, year):
    try:

        flag = True
        day = list(Admin.objects.all())[-1:][0].Day  # Получаем текущий день от админа
        day1 = day
        Admin.objects.all().delete()  # удаляем этот день из базы
        user_factors = Factor.objects.filter(Day=day)  # достаем все выборы за этот день
        players = Player.objects.all()  # достали игроков и активы
        actives = Active.objects.all()
        if int(year) == 400:  # если нажата кнопка превести всех пользователей в состояние по-умлочанию
            newday = Admin(Day=1)  # сохраняем день на 1
            newday.save()
            players = Player.objects.all()
            for i in players:
                i.obnulit()  # у всех игроков тоже обнуляем день и активы по умолчанию
                i.save()

            day = 1  # загружаем 1й день

            return render(request, "player/AdminPage.html", {'user_factors': user_factors, 'actives': actives,
                                                             'players': players, 'day': day})
        if int(year) == 500:  # если нажата кнопка удалить всех пользователей
            players = Player.objects.all()  # удаляем пользователей
            players.delete()
            players = Player.objects.all()
            Admin(Day=day1).save()  # день сохраняем текущий
            return render(request, "player/AdminPage.html", {'user_factors': user_factors, 'actives': actives,
                                                             'players': players, 'day': day1})

        if int(year) == 600:  # если нажата кнопка - загрузить тестовый массив юзеров - можно убрать в репозиторий
            Player(Name='Добротворский').save()
            Player(Name='Михайлов').save()
            Player(Name='Шипиль').save()
            Player(Name='Дубровский').save()
            Player(Name='testUser').save()
            d = Admin(Day=day)  # сохраняем текущий день и показываем всех пользователей
            d.save()
            players = Player.objects.all()
            return render(request, "player/AdminPage.html", {'user_factors': user_factors, 'actives': actives,
                                                             'players': players, 'day': day})

        if int(year) == 1000 or int(year) == 0:  # если нажата кнопка - предыдущий год. тогда
            if day == 0:  # нельзя уходить в отрицуательные значения - мб добавить что
                day += 1
            new_day = Admin(Day=day - 1)
        else:
            new_day = Admin(Day=day + 1)
        new_day.save()  # просто меняем день на новый
        day = new_day.Day

        # now make calculations:
        if int(year) != 1000 and int(year) != 0:  # если нажата кнопка следующий год
            k = sorted(user_factors, key=lambda x: x.UserID.ID)  # отсортируем выборы юзеров по ид (отметим, что
            # выбрали только тех юзеров, которые сделали выбор в данном году)
            idshniki = [i.UserID.ID for i in k]  # чтобы был всегда один и тот же порядок
            game1 = factory.get_repository(idshniki)  # нициализируем репозиторий только по тем юзерам, которые сделали
            # первый ход. Те, кто не сделали первых ход в дальнейшем будут игнорироваться. - Это можно пофиксить через
            # репозиторий. Если это не первый год, то вызывается уже существующий репозиторий
            if len(idshniki) < len(game1.id_):
                flag = False  # если тех, кто сделал выбор в текущем году меньше, чем тех, кто сделал выбор в первом году
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
                    #  до этого все строчки про то, как преобразовать в нужный вид полученные данные + для тех, кто не
                    # сделал выбор - деньги по-умолчанию в банке
                game1.Choice(day1,
                                  list_of_actives_a,
                                  list_of_actives_b
                                  )  # делаем выбор
            else:
                a = [i.Name1.Name_eng for i in k] # если количество пользователей одинаково, тогда все проще
                b = [i.Name2.Name_eng for i in k]
                game1.Choice(day1,
                                  [i.Name1.Name_eng for i in k],
                                  [i.Name2.Name_eng for i in k]
                                  )
            dataframe = game1.Gamble(day1) # проводим расчёты
            i = 0
            act_a = 'asset_1_' + str(day1)
            act_b = 'asset_2_' + str(day1)
            for a, b in game1.data[[act_a, act_b]].to_numpy():
                user = k[i]
                if flag:
                    user = user.UserID # тут просто был  просчет с юзером и идшником
                user.NextYear(a.round(), b.round())
                user.save()
                i += 1



    except:
        raise Http404('Что-то пошло не так в to Main menue')
    return render(request, "player/AdminPage.html", {'user_factors': user_factors, 'actives': actives,
                                                     'players': players, 'day': day})


def to_admin_page(request):
    try:
        try:
            day = list(Admin.objects.all())[-1:][0].Day
        except:
            day = 1
            Admin(Day=1).save()
        user_factors = Factor.objects.filter(Day=day)
        players = Player.objects.all()
        actives = Active.objects.all()  # todo допилить админскую страничку
    except:
        raise Http404('Что-то пошло не так в to_admin_page')
    return render(request, "player/AdminPage.html", {'user_factors': user_factors, 'actives': actives,
                                                     'players': players, 'day': day})
