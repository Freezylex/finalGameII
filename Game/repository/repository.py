# from .models import Player
import numpy as np
import  pandas as pd


class History(): # на страничку статистики выдается лист из историй конкретного юзера. В каждой: год,выбор, доходность
    def __init__(self, year, person, act_a, act_b, increase_a, increase_b):
        self.year = year
        self.person = person
        self.act_a = act_a
        self.act_b = act_b
        self.increase_a = increase_a
        self.increase_b = increase_b


class Factory:
    def __init__(self):
        self.repo = None

    def get_repository(self, id_):
        self.repo = self.repo or Repository(id_)
        return self.repo

    def delete_repo(self):
        self.repo = None

import pandas as pd
import numpy as np


import pandas as pd
import numpy as np


class InvestingOptions:
    '''
    Класс для реализации различных инвестиционных возможностей в игре. Почти все активы строятся одинаковым образом:
    на вход подаются индексы игроков, сумма в предыдущий год по данному активу, колонка для инициализации результата
    инвестирования в инструмент.
    '''

    def __init__(self, df: pd.DataFrame, year: int, educ_dohod: float,
                 inflation_rate: float, number_only: float,
                 number_together: float):
        self.data = df  # датафрейм с информацией по текущей игре
        self.choice_1 = "year_" + str(year) + '_1'
        self.choice_2 = "year_" + str(year) + '_2'
        self.prev_money_1 = 'asset_' + str(year - 1) + '_1'
        self.prev_money_2 = 'asset_' + str(year - 1) + '_1'
        self.future_money_1 = 'asset_' + str(year) + '_1'
        self.future_money_2 = 'asset_' + str(year) + '_2'
        self.educ = educ_dohod
        self.inflat = inflation_rate
        self.stock_only_ratio = number_only  # коэффициент участников для акции с отрицательной бетой
        self.stock_together_ratio = number_together  # коэффициент участников для акции роста
        self.year = year
        self.was_more_than_40 = False

    def bank(self, indexes,
             mon_fut, mon_prev, flag=0):
        '''

        Реализация инвествыбора "вложение в банк".
        ВАЖНО!!!! ПОСЛЕДУЮЩИЕ ФУНКЦИИ РАБОТАЮТ ПО ТАКОМУ ЖЕ ПРИНЦИПУ

        :param indexes: индексы игроков, которые выбрали банк - np.array
        :param mon_fut: колонка, куда будет начислена сумма по результатам инвестирования - str
        :param mon_prev: колонка, откуда будет взята сумма по результатам прошлых инвестирований - str
        :param flag: по дефолту 0 - для дополнительного дохода от образования необходимо поставить 1
        :return: self
        '''
        self.data.loc[indexes, mon_fut] = self.data.loc[indexes, mon_prev] * (
                1 + self.inflat - 0.005) + self.data.loc[indexes, mon_prev] * self.educ * flag * self.data.loc[
                                              indexes, 'educ']
        return self

    def korp_bond(self, indexes,
                  mon_fut, mon_prev, flag=0):
        scalar_value = np.random.choice(a=[0.035, 0, -0.01], p=[0.25, 0.5, 0.25])
        array_of_returns = np.array([1 + self.inflat + scalar_value] * len(self.data))
        self.data.loc[indexes, mon_fut] = self.data.loc[indexes, mon_prev] * (
            array_of_returns) + self.data.loc[indexes, mon_prev] * self.educ * flag * self.data.loc[
                                              indexes, 'educ']
        return self

    def gov_bond(self, indexes, mon_fut,
                 mon_prev, flag=0):
        self.data.loc[indexes, mon_fut] = self.data.loc[indexes, mon_prev] * (
                1 + self.inflat + 0.005) + self.data.loc[indexes, mon_prev] * self.educ * flag * self.data.loc[
                                              indexes, 'educ']
        return self

    def education(self, indexes, mon_fut, mon_prev):
        # поставь ограничение на 8-ой уровень образования
        self.data.loc[indexes, 'educ'] += 1
        self.data.loc[self.data['educ'] > 4] = 4  # ограничение на образование
        self.data.loc[indexes, mon_fut] = self.data.loc[indexes, mon_prev]
        return self

    def stock_only(self, indexes, mon_fut,
                   mon_prev, flag=0):
        if 0 < self.stock_together_ratio < 0.1:
            market_premium = self.inflat + 0.03 + flag * self.educ
        elif 0.1 <= self.stock_together_ratio < 0.2:
            market_premium = self.inflat + 0.05 + flag * self.educ
        elif 0.2 <= self.stock_together_ratio < 0.4:
            market_premium = self.inflat + 0.07 + flag * self.educ
        elif 0.4 <= self.stock_together_ratio < 0.6:
            market_premium = self.inflat + 0.09 + flag * self.educ
        else:
            market_premium = self.inflat - 0.03 + flag * self.educ
        self.data.loc[indexes, mon_fut] = self.data.loc[indexes, mon_prev](1 + market_premium)
        return self

    def stock_together(self, indexes, mon_fut, mon_prev, flag=0):
        '''

        АКЦИЯ РОСТА

        :param indexes:
        :param mon_fut:
        :param mon_prev:
        :param flag:
        :return:
        '''
        if not self.was_more_than_40:
            if self.year == 7:
                market_premium = self.inflat + 0.005
            elif self.year == 8:
                market_premium = self.inflat + 0.055
            elif self.year == 9:
                market_premium = self.inflat + 0.115
            elif self.year == 1:
                market_premium = self.inflat + 0.155
            if self.stock_together_ratio > 0.4:
                market_premium = self.inflat - 0.325
                self.was_more_than_40 = True
        else:
            market_premium = self.inflat - 0.01
        self.data.loc[indexes, mon_fut] = self.data.loc[indexes, mon_prev](1 + market_premium) + self.data.loc[
            indexes, mon_prev] * self.educ * flag * self.data.loc[
                                              indexes, 'educ']
        return self

    def stock_index(self, indexes, mon_fut, mon_prev, flag=0):
        expected_return = 1 + self.inflat + 0.015
        '''
        ЭТО КАК РАЗ БАРСУЧИЙ СЛУЧАЙ
        нормальное распределение с матожиданием 4 и дисперсией 1. При этом дивы по дефолту 3
        '''
        scale = 0.01
        vector_of_returns = np.array(
            [np.random.normal(loc=expected_return, scale=scale)] * len(self.data))
        self.data.loc[indexes, mon_fut] = self.data.loc[indexes, mon_prev] * vector_of_returns + self.data.loc[
            indexes, mon_prev] * self.educ * flag * self.data.loc[
                                              indexes, 'educ']
        return self

    def sosed(self, indexes, mon_fut,
              mon_prev,
              default_prob=0.66, loose=0.04, flag=0):
        dohod_sosed = self.inflat + 0.055
        outcomes = np.random.binomial(1, default_prob, size=len(indexes))  # 1 - дефолт, 0 - успех
        good_outcomes = np.ones(shape=len(outcomes)) - outcomes
        pr_mon = self.data.loc[indexes, mon_prev]  # деньги с предыдущего года
        this_year = pr_mon * (np.ones(shape=len(indexes)) - loose * outcomes + dohod_sosed * good_outcomes) + \
                    self.data.loc[indexes, mon_prev] * self.educ * flag * self.data.loc[
                        indexes, 'educ']
        self.data.loc[indexes, mon_fut] = this_year
        return self

    def _return_bool_flag(self):
        '''
        Изначально функция была написана для того, чтобы флаг не менялся в зависимости от порядка
        вложения в актив (например, если education был выбран в качестве первого актива, то повторный вызов
        accrue привел бы к увеличению доходности

        :return: булевское значение для того, чтобы можно было начислять допдоход по образованию
        '''
        if self.year == 1:
            return 0
        return 1

    def _accrue_money_(self, year_column, prev_money, fut_money):
        '''
        Проход по всем функциям и начисление.

        !!!!!!!!!ПОКА НЕЯСНО КАК СРАВНИВАТЬ NaN - у меня пандас отказывается сравнивать np.nan, полученный
        на вход в датафрейм с nan
        !!!!!!!

        :param year_column: колонка, где находятся выборы участников в этот год - str
        :param prev_money: колонка, откуда будет взята сумма по результатам прошлых инвестирований - str
        :param fut_money: колонка, куда будет начислена сумма по результатам инвестирования - str
        :return: self
        '''
        opportunities = self.data[year_column].unique()
        option_dict = {'bank': self.bank, 'sosed': self.sosed,
                       'korp_bond': self.korp_bond,
                       'gov_bond': self.gov_bond,
                       'stock_together': self.stock_together,
                       'stock_only': self.stock_only,
                       'stock_index': self.stock_index}
        bool_flag = self._return_bool_flag()
        for option in opportunities:
            players_with_educ = self.data[(self.data['educ'] != 0) & (self.data[year_column] == option)].index
            players_without_educ = self.data[(self.data['educ'] == 0) & (self.data[year_column] == option)].index
            if option == 'education':
                ind_for_ed = self.data[self.data[year_column] == 'education'].index
                self.education(ind_for_ed, fut_money, prev_money)
                continue
            try:
                option_dict[option](players_with_educ, fut_money, prev_money, flag=bool_flag)
                option_dict[option](players_without_educ, fut_money, prev_money)
            except:
                self.bank(players_with_educ, fut_money, prev_money)
                self.bank(players_without_educ, fut_money, prev_money)
        return self

    def accrue(self):
        '''

        Проход по инвестиционным опциям и начисление доходности для всех игроков

        :return: pd.DataFrame - итоговый датафрейм после 1 года игры.
        '''
        self._accrue_money_(self.choice_1, self.prev_money_1, self.future_money_1)
        self._accrue_money_(self.choice_2, self.prev_money_2, self.future_money_2)
        return self.data


class Repository:

    def __init__(self, id_, inflation_rate=0.045, educ_dohod=0.005):
        '''

        Базовое правило в названии колонок: сначала ГОД, потом номер актива

        :param id_: айдишники игроков
        :param inflation_rate: базовая цифра, от которой отталкиваются дальнейшие проценты - уровень инфляции
        '''
        id_ = np.array(id_)
        self.id_ = id_
        data = pd.DataFrame({"id": id_})  # инициализация id
        data["TOTAL"] = 200
        data["educ"] = 0
        data["educ_nakop"] = 0
        data["asset_0_1"] = 100  # инициализация актива 1
        data["asset_0_2"] = 100  # инициализация актива 2
        data = data.set_index("id")  # смена индекса на id

        self.data = data
        self.inflation = inflation_rate
        self.educ_dohod = educ_dohod

    def Choice(self,
               year,  # номер года
               asset_1_choice,  # список из выборов игроков касательно инвестиций актива 1
               asset_2_choice  # список из выборов игроков касательно инвестиций актива 2
               ):
        year_1 = "year_" + str(year) + '_1'  # название колонки с выборами касательно актива 1
        year_2 = "year_" + str(year) + '_2'  # название колонки с выборами касательно актива 2

        self.data[year_1] = asset_1_choice
        self.data[year_2] = asset_2_choice

        '''ЭТУ ФУНКЦИЮ МОЖНО БУДЕТ ИЗМЕНЯТЬ В ЗАВИСИМОСТИ ОТ ХАРАКТЕРА ПРИНИМАЕМЫХ ДАННЫХ ПО ВЫБОРУ АКТИВА'''
        ''' я не понял зачем нам тут это, но ладно, оставлю (комментарий от меня)'''
        return self.data

    def Gamble(self, year):  # номер года

        asset_1_is = "asset_" + str(year) + '_1'  # получаем тикер актива 1, который подается на выход
        asset_2_is = "asset_" + str(year) + '_2'  # получаем тикер актива 2, который подается на выход

        choice_1 = "year_" + str(year) + '_1'  # получаем тикер выбора инвестиции актива 1
        choice_2 = "year_" + str(year) + '_2'  # получаем тикер выбора инвестиции актива 2

        self.data[asset_1_is] = 0  # иницциализация нового значения актива 1 нулем
        self.data[asset_2_is] = 0  # иницциализация нового значения актива 2 нулем

        N_together = self.data[self.data[choice_1] == "stock_together"][choice_1].count()
        N_together += self.data[self.data[choice_2] == "stock_together"][choice_2].count()

        N_only = self.data[self.data[choice_1] == "stock_only"][choice_1].count()
        N_only += self.data[self.data[choice_2] == "stock_only"][choice_2].count()

        gambling = InvestingOptions(self.data, year, educ_dohod=self.educ_dohod,
                                    inflation_rate=self.inflation,
                                    number_only=N_only / len(self.data),
                                    number_together=N_together / len(self.data))
        new_data = gambling.accrue()
        self.data = new_data
        self.data["TOTAL"] = self.data[asset_1_is] + self.data[asset_2_is]
        return self.data

    def get_history(self, person_id):
        stata = None
        if self.data is not None:
            stata = self.data.iloc[[person_id]]
            print(stata.head())
        list_history = []
        # for i in range(stata.shape[1]
        # cursor = 0

        return stata



# a = Factory()
#
# game_1 = a.get_repository(np.arange(1, 4, 1))
# # game_1.get_history(1)
#
# game_1.Choice(1,
#               ["sosed" ,"education",'sosed'],
#               ["bank", "education", "sosed"]
#               )
# game_1.Choice(1,
#               ["" ,"",'',"",''],
#               ["", "", "","",'']
#               )
# print(game_1.data)
# game_1.Gamble(1)
# print(game_1.data)
# print(game_1.data.iloc[1])
#
# print(list(game_1.data.iloc[1]))
# game_1.get_history(0)

# game_1 = GAME(np.arange(1, 4, 1))
# game_1.Choice(1,
#               ['sosed', 'education', 'sosed'],
#               ['bank', 'education', 'sosed']
#               )
# game_1.data
# game_1.Gamble(1)
# print(game_1.data)
