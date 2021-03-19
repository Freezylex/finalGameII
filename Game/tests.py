from django.test import TestCase
# from .models import Player
# Create your tests here.
import csv,sys,os
import os
from datetime import datetime
dir_path = os.path.dirname(os.path.realpath(__file__))
project_dir = dir_path[:-5] + '/finalGame'
# print(project_dir)
# print(os.environ['DJANGO_SETTINGS_MODULE'])
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()
from Game.models import Player, Active, Factor, Admin
from Game.repository.repository import Repository
import numpy as np

# player = Player(Name='Aleks 120')
# print(player.Active_a)
# player.save()
# player = Player.objects.get(Name='Aleks 120')
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
print(Factor.objects.all())
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
print(Factor.objects.all())
# print(pla)
# a = pla[0]
# print(a.ID)
# print([i.ID for i in pla])
# game1 = Repository([i.ID for i in pla])
# game1.choice(1,
#            ["bank","bank","sosed"],
#            ["bank","sosed","sosed"]
#            )
# print(game1.gamble(1))
a = list(Admin.objects.all())
# Admin.objects.all().delete()
# aa = Admin(Day=1)
# aa.save()
print(a)