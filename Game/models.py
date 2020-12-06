from django.db import models
import csv,sys,os
import django

class Player(models.Model):
    Name = models.CharField('name', max_length=200, primary_key=True, unique=True, null=False)
    Active_a = models.FloatField('active_a', default=100, null=False)
    Active_a_pred = models.FloatField('active_a', default=100, null=False)
    Active_b = models.FloatField('active_b', default=100, null=False)
    Active_b_pred = models.FloatField('active_b', default=100, null=False)
    Education = models.IntegerField('education', default=0)
    Day = models.IntegerField('day', default=1, null=False)

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

    def __str__(self):
        return self.Name

    def current(self, day):
        return day == self.Day   # текущий день. Возможно, можно поставить и день - 1

    def NextYear(self, choiceA, choiceB):
        self.Day += 1
        # TODO add more functionality

    def percentage_increase_active_a(self):
        return ((self.Active_a_pred - self.Active_a) / self.Active_a) * 100

    def percentage_increase_active_b(self):
        return ((self.Active_b_pred - self.Active_b) / self.Active_b) * 100

    def education(self):
        if self.Education == 0:
            return 'Образование на 0. Вы пока тупой, зато с деньгами)'
        elif self.Education == 1:
            return 'Образование 1. Вы закончили 4 класса образования. Очень неплохо. '
        elif self.Education > 1 & self.Education < 3:
            return f'Уровень образования {self.Education}. Надеюсь, вы уже поняли, что дефолт скоро... очень скоро :)))'
        else:
            return f'Образование {self.Education}. Да вы просто мой кумир!! '

    def SumActive(self):
        return self.Active_a + self.Active_b




# class Factor(models.Model):
#     Name = models.CharField('name', max_length=200, primary_key=True, unique=True, null=False)
#     Day = models.IntegerField('day', null=False)
#     UserID = models.ForeignKey(Player)
#
#     def __str__(self):
#         return self.Name   # factor - это табличка с ресурсами, которые выбрали все пользователи.
#




