from django.test import TestCase
# from .models import Player
# Create your tests here.
import csv, sys, os
import os
from datetime import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))
project_dir = dir_path[:-5] + '/finalGame'
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django

django.setup()
from Game.models import Player, Active, Factor, Admin
from Game.repository.repository import Repository, Factory
import numpy as np

# player = Player(Name='Aleks 120')
# print(player.Active_a)
# player.save()
# player = Player.objects.get(Name='Aleks 120')
# print(player.get_history())
# player.append_to_history(205)
# print(player.get_history())
# print(player.Active_a)
# print(Player.objects.get(Name='Aleks 120').Active_a)
# print(Player.objects.order_by('-Active_a', 'Active_b'))
# players = Player.objects.all()
# print(Player.objects.all())
# Player.objects.all().delete()


# game_1 = Repository(np.arange(1,4,1))
# print(game_1.data)
# game_1.choice(1,
#            ["bank","bank","sosed"],
#            ["bank","sosed","sosed"]
#            )
#
# print(game_1.gamble(1))


# k = ['Банк', 'Стартап Соседа', 'Образование', 'Гособлигации'
#     , 'Корпоративыне облигации']
# z = ['bank', 'startap', 'obrasovanie', 'gosobligatszii', 'korporativnye']
# for i in range(len(k)):
#     act = Active(Id=i, Name=k[i], Name_eng=z[i])
#     act.save()
# print(Active.objects.all())

# print(Admin.objects.all()[0].Day)
# print(Factor.objects.all())
# game_1 = Repository(np.arange(1,4,1))
# print(game_1.data)
# game_1.choice(1,
#            ["bank","bank","sosed"],
#            ["bank","sosed","sosed"]
#            )

# pla = Player.objects.all()
# act = Active.objects.all()
# pla.delete()
# fact = Factor.objects.all()
# fact.delete()
# print(act)
# user_factors = Factor(Name1=act[0], Name2=act[1], Day=1, UserID=pla[0])
# user_factors.save()
# pla.delete()
# aa = Factor.objects.all()
# k = sorted(aa, key=lambda x: x.UserID.ID)
# print([i.Name1.Name_eng for i in k])
# print(sorted([i.UserID.ID for i in a]))
# print(pla)
# a = pla[0]
# print(a.ID)
# print([i.ID for i in pla])
# game1 = Repository([i.UserID.ID for i in k])
# game1.choice(1,
#            [i.Name1.Name_eng for i in k],
#            [i.Name2.Name_eng for i in k]
#            )
# ar = game1.gamble(1)
# actA = ar['asset_1_1']
# actB = ar['asset_2_1']
# print(ar[['asset_1_1','asset_2_1']])
# i = 0
# for a, b in ar[['asset_1_1','asset_2_1']].to_numpy():
#     user = k[i].UserID
#     user.NextYear(a.round(), b.round())
#     # user.save()
#     i += 1
# a = list(Admin.objects.all())
# Admin.objects.all().delete()
# aa = Admin(Day=1)
# aa.save()
# for i in aa[4:]:
#     i.delete()
# aa = Factor.objects.all()
# print(aa)
# j = Repository(list(range(4)))
# df = j.Choice(1,
#     ['sosed', 'bank', 'education', 'sosed'],
#     ['bank', 'sosed',  'education', 'sosed']
# )
# print(df)
# dr = j.Gamble(1)
# print(dr)
# a = Player.objects.filter(Name__startswith='Николай')
# for i in a:
#     print(i.Active_a)
#     print(i.Active_a_pred)
#     print(i.percentage_increase_active_a())
#     i.Active_a_pred = 100
#     i.Active_a = 100
#     i.Active_b_pred = 100
#     i.Active_b = 100
#     i.Day = 2
#     i.save()
#
#
# f = Factory()
# a = f.get_repository(id_=[1, 2])
# a.Choice(1, ['bank', 'bank'], ['bank', 'bank'])
# a.Gamble(1)
# print(a.data)
# print('st')
# ii = 1
# choices = []
# for i in a.data[a.data.index.isin([2])][a.data.columns[5:]].T[2]:
#     choices.append(f'year{ii}')
#     choices.append(f'')
#
# Admin(Day=1).save()
# print(Admin.objects.all())

# import json
#
# a='[200]'
# f = json.loads(a)
# f.append(5)
#
# print(f)
# a = Active(Name='Сток Тугезер', Name_eng='stock_together')
# print(a)
# a.save()
# a = Active(Name='Сток онли', Name_eng='stock_only')
# print(a)
# a.save()
# a = Active(Name='Индекс Биржи', Name_eng='stock_index')
# print(a)
# a.save()
# from django.db.models import F
# a = Player.objects.annotate(s=F('Active_a') + F('Active_b')).order_by('-s')
# print(a)
