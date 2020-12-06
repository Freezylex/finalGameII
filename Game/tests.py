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
from Game.models import Player
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
Player.objects.all().delete()


# game_1 = Repository(np.arange(1,4,1))
# print(game_1.data)
# game_1.choice(1,
#            ["bank","bank","sosed"],
#            ["bank","sosed","sosed"]
#            )
#
# print(game_1.gamble(1))

