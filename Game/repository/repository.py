# from .models import Player
import numpy as np
import  pandas as pd


class Repository(object):
    def __init__(self, id_):
        id_ = np.array(id_)
        data = pd.DataFrame({"id": id_})  # инициализация id
        data["asset_1_0"] = 100  # инициализация актива 1
        data["asset_2_0"] = 100  # инициализация актива 2
        data = data.set_index("id")  # смена индекса на id

        self.data = data

    def obrasovanie(self, asset, vanilla_dohod=0.02):

        return (1 + vanilla_dohod) * asset

    def bank(self, asset,  # актив
             vanilla_dohod=0.06  # доход в банке
             ):

        # expectation = (1 + vanilla_dohod) * asset
        # матожидание этой миниигры

        return (1 + vanilla_dohod) * asset

    def sosed(self, asset,  # актив
              defolt_prob=0.6,  # вероятность потери средств
              dohod_sosed=0.15,  # доход инвестиции в соседа
              lose=0.2  # какую часть актива игрок потеряет в случае дефолта
              ):

        # expectation = defolt_prob*(1-lose)*asset + (1-defolt_prob)*(1+dohod_sosed)*asset
        # матожидание этой миниигры

        if np.random.binomial(1, defolt_prob, 1):
            return asset * (1 - lose)

        else:
            return asset * (1 + dohod_sosed)

    def human(self, asset,  # актив игрока
              choice):  # выбор игрока в годе n

        dt = {"bank": self.bank, "startap": self.sosed, "obrasovanie": self.obrasovanie}  # словарь из возможных опций для инвестирования

        return dt[choice](asset)

    def initialize(self, id_  # список айдишников игроков
                   ):

        id_ = np.array(id_)
        data = pd.DataFrame({"id": id_})  # инициализация id
        data["asset_1_0"] = 100  # инициализация актива 1
        data["asset_2_0"] = 100  # инициализация актива 2
        data = data.set_index("id")  # смена индекса на id
        return data

    def choice(self,
               year,  # номер года
               asset_1_choice,  # список из выборов игроков касательно инвестиций актива 1
               asset_2_choice  # список из выборов игроков касательно инвестиций актива 2
               ):

        year_1 = "year_1_" + str(year)  # название колонки с выборами касательно актива 1
        year_2 = "year_2_" + str(year)  # название колонки с выборами касательно актива 2

        self.data[year_1] = asset_1_choice
        self.data[year_2] = asset_2_choice

        '''ЭТУ ФУНКЦИЮ МОЖНО БУДЕТ ИЗМЕНЯТЬ В ЗАВИСИМОСТИ ОТ ХАРАКТЕРА ПРИНИМАЕМЫХ ДАННЫХ ПО ВЫБОРУ АКТИВА'''
        '''МИША СОСАТТ МИША СОСАТТ МИША СОСАТТ МИША СОСАТТ МИША СОСАТТ МИША СОСАТТ'''
        '''МИША СОСАТТ МИША СОСАТТ МИША СОСАТТ МИША СОСАТТ МИША СОСАТТ МИША СОСАТТ'''
        '''МИША СОСАТТ МИША СОСАТТ МИША СОСАТТ МИША СОСАТТ МИША СОСАТТ МИША СОСАТТ'''
        '''МИША СОСАТТ МИША СОСАТТ МИША СОСАТТ МИША СОСАТТ МИША СОСАТТ МИША СОСАТТ'''
        '''МИША СОСАТТ МИША СОСАТТ МИША СОСАТТ МИША СОСАТТ МИША СОСАТТ МИША СОСАТТ'''
        return self.data

    def gamble(self, year):  # номер года

        asset_1_was = "asset_1_" + str(year - 1)  # получаем тикер актива 1, который подается на вход
        asset_2_was = "asset_2_" + str(year - 1)  # получаем тикер актива 2, который подается на вход

        asset_1_is = "asset_1_" + str(year)  # получаем тикер актива 1, который подается на выход
        asset_2_is = "asset_2_" + str(year)  # получаем тикер актива 2, который подается на выход

        choice_1 = "year_1_" + str(year)  # получаем тикер выбора инвестиции актива 1
        choice_2 = "year_2_" + str(year)  # получаем тикер выбора инвестиции актива 2

        self.data[asset_1_is] = 0  # иницциализация нового значения актива 1 нулем
        self.data[asset_2_is] = 0  # иницциализация нового значения актива 2 нулем

        for index, row in self.data.iterrows():  # цикл, потому что игроков мало -> будет быстро

            '''ДОБАВИТЬ ЗАЩИТУ ОТ СЛУЧЧАЕВ, КОГДА ИГРОК НИЧЕГО НЕ ВЫБРАЛ (ТОГДА ВСЕ ДЕНЬГИ ИДУТ В БАНК)'''
            # без защиты код сломается

            result_1 = self.human(row[asset_1_was], row[choice_1])  # считаем новую стоимость актива 1
            result_2 = self.human(row[asset_2_was], row[choice_2])  # считаем новую стоимость актива 2

            self.data.loc[index, asset_1_is] = result_1  # обновляем актив 1 в новой колонке
            self.data.loc[index, asset_2_is] = result_2  # обновляем актив 2 в новой колонке

        return self.data


game_1 = Repository(np.arange(1,4,1))
print(game_1.data)
game_1.choice(1,
           ["bank","bank","sosed"],
           ["bank","sosed","sosed"]
           )

# print(game_1.gamble(1))


# repo = Repository(np.arange(1, 4, 2))
# print(np.arange(1, 4, 1))

# player = Player?