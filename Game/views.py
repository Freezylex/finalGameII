import json

import numpy as np
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import F

# from .static.hard.banking import Repository
# Create your views here.

from django.shortcuts import render
from .models import Player, Active, Factor, Admin
from Game.repository.repository import Repository, Factory



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
        players = Factory.get_players()
        rating = list(players).index(player) + 1
        day = list(Admin.objects.all())[-1:][0].Day #TODO поменять на день пользоватлея
        len_rating = len(players)
        id_actives = [0, 1, 2, 8]
        if day >= 4:
            id_actives += [3, 4]
        if day > 6:
            id_actives += [5, 7]
            id_actives.remove(1)
        actives = [i for i in Active.objects.all() if i.Id in id_actives]

    except:
        raise Http404('Что-то пошло не так в to Main menue')
    return render(request, "player/mainWindow.html", {'player': player, 'len_rating': len_rating,
                                                      'players': players,
                                                      'actives': actives, 'rating': rating, 'day':day})


def to_top_players(request, player_nam):
    try:
        player = Player.objects.get(Name=player_nam)
        day = list(Admin.objects.all())[-1:][0].Day
        # if day == 1:
        #     stata = ['Здесь появится статистика по предыдущим годам'] # Перевести стату в репозиторий
        # else:
        #     repo = factory.get_repository(1)
        #     stata = list(repo.data.iloc[player.ID])
        #     factors = Factor.objects.filter(UserID__factor=player.ID) # не хватает истории того, что приносло
            # какие диведенты

        # player.save()
        players = Factory.get_players()
        rating = list(players).index(player) + 1
        user_choices = Factor.objects.filter(UserID=player).order_by('Day')
        # if player.Day == 1:
        #     user_choices.append('На данном месте появятся резульаты сделанных вами инвестиций')
        # else:
        #     data = factory.repo
        #     if data:
        #         pass
        #
        #     else:
        #         user_choices.append('err in data. repository is not initialised')

        years = json.dumps(list(range(1, day + 1)))

    except:
        raise Http404('Что-то пошло не так')
    return render(request, "player/statistica.html", {'years': years, 'player': player, 'user_choices' : user_choices,
                                                      'players': players, 'rating': rating})


def to_personal_page(request):
    try:
        if request.POST['user'] =='adminPage':
            try:
                try:
                    day = list(Admin.objects.all())[-1:][0].Day
                except:
                    day = 1
                    Admin(Day=1).save()
                user_factors = Factor.objects.filter(Day=day)
                actives = Active.objects.all()
                players = Factory.get_players()
            except:
                raise Http404('Что-то пошло не так в to_admin_page')
            return render(request, "player/AdminPage.html", {'counter': len(user_factors), 'q': len(players), 'actives': actives,
                                                     'players': players, 'day': day})

        a = Player.objects.filter(Name=request.POST['user'])
        if len(a) == 0:
            player = Player(Name=request.POST['user'])
            player.save()
        else:
            player = a[0]
        players = Factory.get_players()
        rating = list(players).index(player) + 1
    except:
        raise Http404('Что-то пошло не так')
    return render(request, "player/Personal Page.html", {'player': player, 'players': players, 'rating': rating})

def to_top(request, player):
    try:
        a = Player.objects.filter(Name=player)
        player = a[0]
        players = Factory.get_players()
        rating = list(players).index(player) + 1
    except:
        raise Http404('Что-то пошло не так')
    return render(request, "player/Personal Page.html", {'player': player, 'players': players, 'rating': rating})



def next_step(request, play):
    try:
        st_only = False
        player = Player.objects.get(Name=play)
        # player.save()
        players = Factory.get_players()
        rating = list(players).index(player) + 1
        flag = Admin.objects.order_by('-Day')[0].Day
        day = list(Admin.objects.all())[-1:][0].Day

        if player.Day == flag:
            pass
        len_rating = len(players)
        id_actives = [0, 1, 2, 8]
        if day >= 4:
            id_actives += [3, 4]
        if day > 6:
            id_actives += [5, 7]
            # id_actives.remove(1)
            if st_only:
                id_actives += [6]
        print(day)
        actives = [i for i in Active.objects.all() if i.Id in id_actives]
    except:
        raise Http404('Что-то пошло не так в make_chio')
    return render(request, "player/mainWindow.html", {'player': player, 'len_rating': len_rating,
                                                      'players': players,
                                                      'actives': actives, 'rating': rating, 'day':day})




def make_choice(request, player_name):  # игроком нажата клавиша (подтвердить выбор)
    try:
        st_only=False
        player = Player.objects.get(Name=player_name)
        player.Day = player.Day + 1 #TODO Позже перестать использовать день как флаг что игрок сделал ход
        player.save()
        day = list(Admin.objects.all())[-1:][0].Day
        # player.save()
        players = Factory.get_players()
        rating = list(players).index(player) + 1
        ##
        len_rating = len(players)
        id_actives = [0, 1, 2, 8]
        if day >= 4:
            id_actives += [3, 4]
        if day > 6:
            id_actives += [5, 7]
            id_actives.remove(1)
            if st_only:
                id_actives += [6]
        actives = [i for i in Active.objects.all() if i.Id in id_actives]
        ##
        a = request.POST.get('activeA')
        b = request.POST.get('activeB')
        с = request.POST.get('activeС')
        if not a:
            a = 'Банк'
        if not b:
            b = 'Банк'
        if not с:
            с = 'Банк'
        act_a = Active.objects.get(Name__startswith=a)
        act_b = Active.objects.get(Name__startswith=b)
        act_с = Active.objects.get(Name__startswith=с)
        user_factors = Factor(Name1=act_a, Name2=act_b, Name3=act_с, Day=day, UserID=player)
        factor = Factor.objects.filter(Day=day, UserID=player)
        if len(factor) != 0:
            factor.delete()
        user_factors.save()
        if None: ## TODO add async
            pass
    except:
        raise Http404('Что-то пошло не так в make_chio')
    return render(request, "player/mainWindow.html", {'player': player, 'len_rating': len_rating,
                                                      'players': players,
                                                      'actives': actives, 'rating': rating, 'day':day})


# factory = Factory()


def next_day_admin(request, year):
    try:
        factory = Factory()
        empty_choice = 'bank'
        flag = True
        day = list(Admin.objects.all())[-1:][0].Day  # Получаем текущий день от админа
        day1 = day
        was_more_than_40 = list(Admin.objects.all())[-1:][0].Was_more_fourty
        print(was_more_than_40, 'Was_more_print')
        Admin.objects.all().delete()  # удаляем этот день из базы
        user_factors = Factor.objects.filter(Day=day)  # достаем все выборы за этот день
        players = Factory.get_players()
        actives = Active.objects.all()
        if int(year) == 400:  # если нажата кнопка превести всех пользователей в состояние по-умлочанию
            newday = Admin(Day=1, Was_more_fourty=was_more_than_40)  # сохраняем день на 1
            newday.save()
            Factor.objects.all().delete()
            for i in players:
                i.obnulit()  # у всех игроков тоже обнуляем день и активы по умолчанию
                i.save()

            day = 1  # загружаем 1й день

            return render(request, "player/AdminPage.html", {'counter': len(user_factors), 'q': len(players), 'actives': actives,
                                                     'players': players, 'day': day})
        if int(year) == 500:  # если нажата кнопка удалить всех пользователей
            players.delete()  # удаляем пользователей
            Admin(Day=day1).save()  # день сохраняем текущий
            counter = len(user_factors)
            q = len(players)
            return render(request, "player/AdminPage.html", {'counter': counter, 'q': q, 'actives': actives,
                                                     'players': players, 'day': day})

        if int(year) == 600:  # если нажата кнопка - загрузить тестовый массив юзеров - можно убрать в репозиторий
            Player(Name='Добротворский').save()
            Player(Name='Михайлов').save()
            Player(Name='Шипиль').save()
            Player(Name='Дубровский').save()
            Player(Name='testUser').save()
            d = Admin(Day=day)  # сохраняем текущий день и показываем всех пользователей
            d.save()
            players = Factory.get_players()
            counter = len(user_factors)
            q = len(players)
            return render(request, "player/AdminPage.html", {'counter': counter, 'q': q, 'actives': actives,
                                                     'players': players, 'day': day})
        if int(year) == 1000 or int(year) == 0:  # если нажата кнопка - предыдущий год. тогда
            if day == 0:  # нельзя уходить в отрицуательные значения - мб добавить что
                day += 1
            new_day = Admin(Day=day - 1)
            for player in players:
                player.one_year_back()
                player.save()
            fact_del = Factor.objects.filter(Day__gte=day)
            fact_del.delete()
        else:
            new_day = Admin(Day=day + 1, Was_more_fourty=was_more_than_40)
        new_day.save()  # просто меняем день на новый
        day = new_day.Day


        # now make calculations:
        if int(year) != 1000 and int(year) != 0:  # если нажата кнопка следующий год
            k = sorted(user_factors, key=lambda x: x.UserID.ID)  # отсортируем выборы юзеров по ид (отметим, что
            # выбрали только тех юзеров, которые сделали выбор в данном году)
            idshniki = [i.UserID.ID for i in k]  # чтобы был всегда один и тот же порядок
            id_players_sorted = sorted([i.ID for i in list(players)])
            #TODO ВОТ ТУТ НАДО ДОСТАТЬ ПЕРЕМЕННУЮ ИЗ БД И ОТПРАВИТЬ ЕЕ В ФУНКЦИЮ get_repository (аргумент flag_40, линия 33 в repository.py)
            game1 = factory.get_repository(id_players_sorted, flag_40 = was_more_than_40)  # нициализируем репозиторий только по тем юзерам, которые сделали
            # первый ход. Те, кто не сделали первых ход в дальнейшем будут игнорироваться. - Это можно пофиксить через
            # репозиторий. Если это не первый год, то вызывается уже существующий репозиторий
            if len(idshniki) < len(game1.id_):
                flag = False  # если тех, кто сделал выбор в текущем году меньше, чем тех, кто сделал выбор в первом году
                list_of_actives_a = []
                list_of_actives_b = []
                list_of_actives_c = []
                dict_k = {el.UserID.ID: el for el in k}
                k = []
                default_act = Active.objects.get(Name_eng=empty_choice)
                for i in game1.id_:
                    player_ = Player.objects.get(ID__exact=i)
                    k.append(player_)
                    if i in dict_k:
                        elem = dict_k[i]
                        list_of_actives_a.append(elem.Name1.Name_eng)
                        list_of_actives_b.append(elem.Name2.Name_eng)
                        list_of_actives_c.append(elem.Name3.Name_eng)
                    else:
                        list_of_actives_a.append(empty_choice)
                        list_of_actives_b.append(empty_choice)
                        list_of_actives_c.append(empty_choice)
                        Factor(Day=day1, UserID=player_, Name1=default_act, Name2=default_act, Name3=default_act).save() # ту логику лучше убрать в репозиторий
                    #  до этого все строчки про то, как преобразовать в нужный вид полученные данные + для тех, кто не
                    # сделал выбор - деньги по-умолчанию в банке
                game1.Choice(day1,
                             list_of_actives_a,
                             list_of_actives_b,
                             list_of_actives_c

                             )  # делаем выбор
            else:
                a = [i.Name1.Name_eng for i in k]
                b = [i.Name2.Name_eng for i in k]
                c = [i.Name3.Name_eng for i in k]
                game1.Choice(day1,
                             [i.Name1.Name_eng for i in k],
                             [i.Name2.Name_eng for i in k],
                             [i.Name3.Name_eng for i in k]
                             )
            dataframe, was_more_than_40 = game1.Gamble(day1)  # проводим расчёты
            #TODO ВОТ ТУТ Я ДОСТАЛ ЭТУ ПЕРЕМЕННУЮ И ЕЕ ТЕПЕРЬ НАДО КАК-ТО СОХРАНИТЬ В БД - ОНА ОДНА НА ВСЕХ
            i = 0
            act_a = 'asset_' + str(day1) + '_1'
            act_b = 'asset_' + str(day1) + '_2'
            act_c = 'asset_' + str(day1) + '_3'
            #act_a_historical = 'asset_' + str(day1) + '_1_' + 'for_dohod'
            #act_b_historical = 'asset_' + str(day1) + '_2_' + 'for_dohod'
            #act_c_historical = 'asset_' + str(day1) + '_3_' + 'for_dohod'

            for a, b, c, d, e, f, g in game1.data[[act_a, act_b, act_c, #a, b, c, aa, bb, cc, d, e, f, g
                         #act_a_historical,act_b_historical, act_c_historical,
                                                   'educ', 'mortgage_count', 'further_mortgage',
                                                   'now_mortgage']].to_numpy():
                user = k[i]
                if flag:
                    user = user.UserID  # тут просто был  просчет с юзером и идшником
                user.NextYear(np.round(a, 4), np.round(b, 4), np.round(c, 4), e, f, g, d) # aa,bb,cc
                user.Education = d
                user.save()
                f = user.factor_set.filter(Day=day1)[0]
                f.ActA_increase = user.percentage_increase_active_a()
                f.ActB_increase = user.percentage_increase_active_b()
                f.ActC_increase = user.percentage_increase_active_c()
                f.save()
                i += 1
        Admin.objects.all().delete()
        new_day = Admin(Day=day, Was_more_fourty=was_more_than_40)
        new_day.save()  # просто меняем день на новый
        day = new_day.Day
        players = Factory.get_players()
        counter = len(Factor.objects.filter(Day=day))
        q = len(players)
    except:
        raise Http404('Что-то пошло не так в to_admin_page')
    return render(request, "player/AdminPage.html", {'counter': counter, 'q' : q, 'actives': actives,
                                                     'players': players, 'day': day})

def to_admin_page(request):
    try:
        try:
            day = list(Admin.objects.all())[-1:][0].Day
            try:
                a = Player.objects.filter(Name=request.POST['user'])[0]
                a.Name = "Игрок1" + str((np.random.randint(50, 10000) % 5000) + np.random.randint(2, 20) ** 2 % 79)
                a.save()
            except:
                pass
        except:
            day = 1
            print('err')
            Admin(Day=1).save()
        user_factors = Factor.objects.filter(Day=day)
        players = Factory.get_players()
        actives = Active.objects.all()  # todo допилить админскую страничку
        counter = len(user_factors)
        q = len(players)
    except:
        raise Http404('Что-то пошло не так в to_admin_page')
    return render(request, "player/AdminPage.html", {'counter': counter, 'q' : q, 'actives': actives,
                                                     'players': players, 'day': day})

