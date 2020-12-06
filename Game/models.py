from django.db import models
import csv,sys,os
import django


class Player(models.Model):
    Name = models.CharField('name', max_length=200, primary_key=True, unique=True, null=False)
    Active_a = models.FloatField('active_a', default=100, null=False)
    Active_b = models.FloatField('active_b', default=100, null=False)
    Education = models.FloatField('education', default=0)
    Day = models.IntegerField('day', default=1, null=False)

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

    def __str__(self):
        return self.Name

    def current(self, day):
        return day == self.Day   # текущий день. Возможно, можно поставить и день - 1

    def NextYear(self, day):
        self.Day += 1





