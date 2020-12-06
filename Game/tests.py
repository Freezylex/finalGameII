from django.test import TestCase
# from .models import Player
# Create your tests here.
import csv,sys,os
import os
from datetime import datetime
dir_path = os.path.dirname(os.path.realpath(__file__))
project_dir = dir_path[:-5] + '/finalGame'
print(project_dir)
# print(os.environ['DJANGO_SETTINGS_MODULE'])
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()
from Game.models import Player


player = Player(Name='Aleks Velikiy')
print(player.Active_a)
# player.save()
players = Player.objects.all()
