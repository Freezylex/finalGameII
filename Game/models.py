from django.db import models
import csv,sys,os
import django

class Player(models.Model):
    ID = models.IntegerField(auto_created=True, unique=True)
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

    def NextYear(self, a, b):
        self.Day += 1
        self.Active_a_pred = self.Active_a
        self.Active_b_pred = self.Active_b
        self.Active_a = a
        self.Active_b = b

    def percentage_increase_active_a(self):
        return round(((-self.Active_a_pred + self.Active_a) / self.Active_a_pred) * 100, 2)

    def percentage_increase_active_b(self):
        return round(((-self.Active_b_pred + self.Active_b) / self.Active_b_pred) * 100, 2)

    def education(self):
        if self.Education == 0:
            return 'Необразованность. Тип: 0 из бесконечности'
        elif self.Education == 1:
            return 'Образование 1. Вы закончили 4 класса образования. Очень неплохо. '
        elif self.Education > 1 & self.Education < 3:
            return f'Уровень образования {self.Education}. Надеюсь, вы уже поняли, что дефолт скоро... очень скоро :)))'
        else:
            return f'Образование {self.Education}. Да вы просто мой кумир!! '

    def SumActive(self):
        return self.Active_a + self.Active_b

    def SumActive_percentage_increase(self):
        res = (self.Active_a + self.Active_b - self.Active_a_pred - self.Active_b_pred) / (self.Active_a_pred + self.Active_b_pred)
        if res >= 0:
            output = f"+ {round(100 * res, 2)}"
        else:
            output = f"{round(100 * res, 2)}"
        return output

    def obnulit(self):
        self.Day = 1
        self.Active_a_pred = 100
        self.Active_a = 100
        self.Active_b = 100
        self.Active_b_pred = 100
        self.Education = 0
        return 1




class Active(models.Model):
    Id = models.AutoField(primary_key=True)
    Name = models.CharField('name', max_length=200, null=False, unique=True)
    Name_eng = models.CharField('name_eng', max_length=200)

    def __str__(self):
        return self.Name


class Factor(models.Model):
    Name1 = models.ForeignKey(Active, on_delete=models.CASCADE, null=True, related_name='active_a')
    Name2 = models.ForeignKey(Active, on_delete=models.CASCADE, null=True, related_name='active_b')
    Day = models.IntegerField('day', null=False)
    UserID = models.ForeignKey(Player, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return str(self.Day) + ' ' + str(self.UserID) + ' ' + str(self.Name1) + ' ' + str(self.Name2)


class Admin(models.Model):
    Day = models.IntegerField('Day', null=False)

    def __str__(self):
        return "Наступил день " + str(self.Day)
