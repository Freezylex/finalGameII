from django.db import models
import csv, sys, os
import django
import json


class Player(models.Model):
    ID = models.AutoField(auto_created=True, primary_key=True, unique=True)
    Name = models.CharField('name', max_length=200, unique=True, null=False)
    Active_a = models.FloatField('active_a', default=100, null=False)
    Active_a_pred = models.FloatField('active_a', default=100, null=False)
    Active_b = models.FloatField('active_b', default=100, null=False)
    Active_b_pred = models.FloatField('active_b', default=100, null=False)
    Active_c = models.FloatField('active_c', default=100, null=False)
    Active_c_pred = models.FloatField('active_c', default=100, null=False)
    Education = models.IntegerField('education', default=0)
    Day = models.IntegerField('day', default=1, null=False)
    History = models.CharField('history', max_length=400, null=False, default='[200]')

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

    def __str__(self):
        return self.Name

    def get_history(self):
        return self.History

    def append_to_history(self, x):
        self.History = self.History[:-1] + ',' + str(x) + self.History[-1]
        return 1

    def current(self, day):
        return day == self.Day  # текущий день. Возможно, можно поставить и день - 1

    def SumActive(self):
        return self.Active_a + self.Active_b + self.Active_c

    def NextYear(self, a, b, c):
        self.Day += 1
        self.Active_a_pred = self.Active_a
        self.Active_b_pred = self.Active_b
        self.Active_c_pred = self.Active_c
        self.Active_a = a
        self.Active_b = b
        self.Active_c = c
        self.append_to_history(self.SumActive())

    def percentage_increase_active_a(self):
        res = (-self.Active_a_pred + self.Active_a) / self.Active_a_pred
        if res >= 0:
            output = f"+{round(100 * res, 2)}%"
        else:
            output = f"{round(100 * res, 2)}%"
        return output

    def percentage_increase_active_b(self):
        res = (-self.Active_b_pred + self.Active_b) / self.Active_b_pred
        if res >= 0:
            output = f"+{round(100 * res, 2)}%"
        else:
            output = f"{round(100 * res, 2)}%"
        return output

    def percentage_increase_active_c(self):
        res = (-self.Active_c_pred + self.Active_c) / self.Active_c_pred
        if res >= 0:
            output = f"+{round(100 * res, 2)}%"
        else:
            output = f"{round(100 * res, 2)}%"
        return output


    def education(self):
        if self.Education == 0:
            return '0'
        elif self.Education == 1:
            return '1'
        elif self.Education > 4:
            return f'Уровень образования {self.Education}. Надеюсь, вы уже поняли, что дефолт скоро... очень скоро :)))'
        else:
            return f'{self.Education}'

    def SumActive_percentage_increase(self):
        res = (self.Active_a + self.Active_b - self.Active_a_pred - self.Active_b_pred + self.Active_c
               - self.Active_c_pred) / (
                    self.Active_a_pred + self.Active_b_pred + self.Active_c_pred)
        if res >= 0:
            output = f"+{round(100 * res, 2)} %"
        else:
            output = f"{round(100 * res, 2)}%"
        return output

    def obnulit(self):
        self.Day = 1
        self.Active_a_pred = 100
        self.Active_a = 100
        self.Active_b = 100
        self.Active_c = 100
        self.Active_b_pred = 100
        self.Active_c_pred = 100
        self.Education = 0
        self.History = '[200]'
        return 1

    def one_year_back(self):
        self.Day -= 1
        new = json.loads(self.History)
        self.Active_a = self.Active_a_pred
        self.Active_b = self.Active_b_pred
        self.Active_c = self.Active_c_pred
        if len(new) < 3:
            i = 0
        else:
            i = -3
        self.Active_a_pred = new[i] // 3
        self.Active_b_pred = new[i] // 3
        self.Active_c_pred = new[i] // 3
        self.History = json.dumps(new[:-1])


class Active(models.Model):
    Id = models.AutoField(primary_key=True)
    Name = models.CharField('name', max_length=200, null=False, unique=True)
    Name_eng = models.CharField('name_eng', max_length=200)

    def __str__(self):
        return self.Name


class Factor(models.Model):
    Name1 = models.ForeignKey(Active, on_delete=models.CASCADE, null=True, related_name='active_a')
    Name2 = models.ForeignKey(Active, on_delete=models.CASCADE, null=True, related_name='active_b')
    Name3 = models.ForeignKey(Active, on_delete=models.CASCADE, null=True, related_name='active_c')
    Day = models.IntegerField('day', null=False)
    UserID = models.ForeignKey(Player, on_delete=models.CASCADE, null=False)
    ActA_increase = models.CharField('actAinc', max_length=10, null=True, default="обрабатывается")
    ActB_increase = models.CharField('actBinc', max_length=10, null=True, default="обрабатывается")
    ActC_increase = models.CharField('actCinc', max_length=10, null=True, default="обрабатывается")

    def __str__(self):
        return str(self.Day) + ' ' + str(self.UserID) + ' ' + str(self.Name1) + ' ' + str(self.Name2) \
               + ' ' + str(self.Name3)


class Admin(models.Model):
    Day = models.IntegerField('Day', null=False)

    def __str__(self):
        return "Наступил день " + str(self.Day)
