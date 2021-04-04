# from .models import Player
import numpy as np
import  pandas as pd

class Factory:
    def __init__(self):
        self.repo = None

    def get_repository(self, id_):
        self.repo = self.repo or Repository(id_)
        return self.repo

class Repository:
    def __init__(self, id_):
        id_ = np.array(id_)
        self.id_ = id_
        data = pd.DataFrame({"id": id_})  # инициализация id
        data["TOTAL"] = 200
        data["educ"] = 0
        data["educ_nakop"] = 0
        data["asset_1_0"] = 100  # инициализация актива 1
        data["asset_2_0"] = 100  # инициализация актива 2
        data = data.set_index("id")  # смена индекса на id

        self.data = data

    def Choice(self,
               year,  # номер года
               asset_1_choice,  # список из выборов игроков касательно инвестиций актива 1
               asset_2_choice  # список из выборов игроков касательно инвестиций актива 2
               ):
        year_1 = "year_1_" + str(year)  # название колонки с выборами касательно актива 1
        year_2 = "year_2_" + str(year)  # название колонки с выборами касательно актива 2

        self.data[year_1] = asset_1_choice
        self.data[year_2] = asset_2_choice

        '''ЭТУ ФУНКЦИЮ МОЖНО БУДЕТ ИЗМЕНЯТЬ В ЗАВИСИМОСТИ ОТ ХАРАКТЕРА ПРИНИМАЕМЫХ ДАННЫХ ПО ВЫБОРУ АКТИВА'''


    def Gamble(self, year):  # номер года

        asset_1_was = "asset_1_" + str(year - 1)  # получаем тикер актива 1, который подается на вход
        asset_2_was = "asset_2_" + str(year - 1)  # получаем тикер актива 2, который подается на вход

        asset_1_is = "asset_1_" + str(year)  # получаем тикер актива 1, который подается на выход
        asset_2_is = "asset_2_" + str(year)  # получаем тикер актива 2, который подается на выход

        choice_1 = "year_1_" + str(year)  # получаем тикер выбора инвестиции актива 1
        choice_2 = "year_2_" + str(year)  # получаем тикер выбора инвестиции актива 2

        self.data[asset_1_is] = 0  # иницциализация нового значения актива 1 нулем
        self.data[asset_2_is] = 0  # иницциализация нового значения актива 2 нулем

        N_together = self.data[self.data[choice_1] == "stock_together"][choice_1].count()
        N_together += self.data[self.data[choice_2] == "stock_together"][choice_2].count()

        N_only = self.data[self.data[choice_1] == "stock_only"][choice_1].count()
        N_only += self.data[self.data[choice_2] == "stock_only"][choice_2].count()

        for index, row in self.data.iterrows():  # цикл, потому что игроков мало -> будет быстро

            '''ДОБАВИТЬ ЗАЩИТУ ОТ СЛУЧЧАЕВ, КОГДА ИГРОК НИЧЕГО НЕ ВЫБРАЛ (ТОГДА ВСЕ ДЕНЬГИ ИДУТ В БАНК)'''
            # без защиты код сломается

            result_1 = human(row[asset_1_was], row[choice_1], self.data, index, N_together,
                             N_only)  # считаем новую стоимость актива 1
            result_2 = human(row[asset_2_was], row[choice_2], self.data, index, N_together,
                             N_only)  # считаем новую стоимость актива 2

            self.data.loc[index, asset_1_is] = result_1  # обновляем актив 1 в новой колонке
            self.data.loc[index, asset_2_is] = result_2  # обновляем актив 2 в новой колонке

        self.data.loc[:, "educ"] += self.data.loc[:, "educ_nakop"]
        self.data["educ_nakop"] = 0
        self.data["TOTAL"] = self.data[asset_1_is] + self.data[asset_2_is]


# %%

def human(asset,  # актив игрока
          choice,  # выбор игрока по 1 активу
          data,  # наш датафрейм self.data
          idx,  # имя игрока
          N_together,
          N_only
          ):
    dt = {"bank": bank, "sosed": sosed, "education": education,
          "korp_bond": korp_bond, "gov_bond": gov_bond, "stock_together": stock_together,
          "stock_only": stock_only}
    # словарь из возможных опций для инвестирования

    return dt[choice](asset, data, idx, N_together, N_only)


# %%

educ_dohod = 0.01


def bank(asset,  # актив
         data,  # наш основной датафрейм (self.data)
         idx,  # имя игрока
         a,
         b,
         vanilla_dohod=0.06,  # доход в банке
         educ_dohod=educ_dohod  # доход от образования
         ):
    # expectation = (1 + vanilla_dohod + data.loc[idx,"educ"] * educ_dohod) * asset
    # матожидание этой миниигры

    return (1 + vanilla_dohod + data.loc[idx, "educ"] * educ_dohod) * asset


def sosed(asset,  # актив
          data,  # наш основной датафрейм (self.data)
          idx,  # имя игрока
          a,
          b,
          defolt_prob=0.6,  # вероятность потери средств
          dohod_sosed=0.15,  # доход инвестиции в соседа
          lose=0.2,  # какую часть актива игрок потеряет в случае дефолта
          educ_dohod=educ_dohod  # доход от образования
          ):
    # expectation = defolt_prob*(1-lose+data.loc[idx,"educ"]*educ_dohod)*asset + (1-defolt_prob)*(1+dohod_sosed+data.loc[idx,"educ"]*educ_dohod)*asset
    # матожидание этой миниигры

    if np.random.binomial(1, defolt_prob, 1):
        return asset * (1 - lose + data.loc[idx, "educ"] * educ_dohod)

    else:
        return asset * (1 + dohod_sosed + data.loc[idx, "educ"] * educ_dohod)


def education(asset,
              data,
              idx,  # имя игрока
              a,
              b,
              educ_dohod=educ_dohod
              ):
    # expectation = (1+data.loc[idx,"educ"]*educ_dohod)*asset
    data.loc[idx, "educ_nakop"] += 1

    return asset * (1 + data.loc[idx, "educ"] * educ_dohod)


def korp_bond(asset,  # актив
              data,  # наш основной датафрейм (self.data)
              idx,  # имя игрока
              a,
              b,
              defolt_prob=0.5,  # вероятность плохого исхода
              dohod_good=0.1,  # доход при хорошем исходе
              dohod_bad=0.05,  # доход при плохом исходе
              educ_dohod=educ_dohod  # доход от образования
              ):
    # expectation = defolt_prob*(1+dohod_bad+data.loc[idx,"educ"]*educ_dohod)*asset + (1-defolt_prob)*(1+dohod_good+data.loc[idx,"educ"]*educ_dohod)*asset
    # матожидание этой миниигры
    # return expectation

    if np.random.binomial(1, defolt_prob, 1):
        return asset * (1 + dohod_bad + data.loc[idx, "educ"] * educ_dohod)

    else:
        return asset * (1 + dohod_good + data.loc[idx, "educ"] * educ_dohod)


educ_dohod = 0.01


def gov_bond(asset,  # актив
             data,  # наш основной датафрейм (self.data)
             idx,  # имя игрока
             a,
             b,
             vanilla_dohod=0.07,  # доход в бонде
             educ_dohod=educ_dohod  # доход от образования
             ):
    # expectation = (1 + vanilla_dohod + data.loc[idx,"educ"] * educ_dohod) * asset
    # матожидание этой миниигры

    return (1 + vanilla_dohod + data.loc[idx, "educ"] * educ_dohod) * asset


def stock_together(asset,  # актив
                   data,  # наш основной датафрейм (self.data)
                   idx,  # имя игрока
                   N_together,
                   N_only,
                   vanilla_dohod=0.02,  # доход от дивидендов
                   educ_dohod=educ_dohod  # доход от образования
                   ):
    N = data.shape[0] * 2
    n = N_together

    if n / N >= 0 and n / N < 0.1:
        extra_dohod = 0.02
    elif n / N >= 0.1 and n / N < 0.2:
        extra_dohod = 0.05
    elif n / N >= 0.2 and n / N < 0.3:
        extra_dohod = 0.09
    elif n / N >= 0.3 and n / N < 0.4:
        extra_dohod = 0.14
    else:
        extra_dohod = 0.2

    return (1 + vanilla_dohod + extra_dohod + data.loc[idx, "educ"] * educ_dohod) * asset


def stock_only(asset,  # актив
               data,  # наш основной датафрейм (self.data)
               idx,  # имя игрока
               N_together,
               N_only,
               vanilla_dohod=0.02,  # доход от дивидендов
               educ_dohod=educ_dohod  # доход от образования
               ):
    N = data.shape[0] * 2
    n = N_only

    if n / N >= 0 and n / N < 0.1:
        extra_dohod = 0.2
    elif n / N >= 0.1 and n / N < 0.2:
        extra_dohod = 0.15
    elif n / N >= 0.2 and n / N < 0.3:
        extra_dohod = 0.1
    elif n / N >= 0.3 and n / N < 0.4:
        extra_dohod = 0.5
    else:
        extra_dohod = 0

    return (1 + vanilla_dohod + extra_dohod + data.loc[idx, "educ"] * educ_dohod) * asset



a = None
b = 0
b = Repository(np.arange(1,4,1)) and a and b
print(b)
# game_1 = Repository(np.arange(1,4,1))
# print(game_1.data)
# game_1.Choice(1,
#            ["bank","bank","sosed"],
#            ["bank","sosed","sosed"]
#            )

# print(game_1.gamble(1))


repo = Repository([1])
repo.Choice(1, ['education'], ['education'])
a = repo.Gamble(1)
print(repo.data)
# print(np.arange(1, 4, 1))
# print(repo.data)
# player = Player?
# day1 = 0
# act_a = 'asset_1_' + str(day1)
# act_b = 'asset_2_' + str(day1)
# for a, b, c in repo.data[[act_a, act_b, 'educ']].to_numpy():
#     print(a, b, c)

