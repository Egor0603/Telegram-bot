import requests
import json
from config import access_key2
from collections import defaultdict


class ConvertionException(Exception):
    pass


class UserInfo:
    def __init__(self):
        self.f = 'EUR'
        self.t = 'RUB'


class UserDB:
    def __init__(self):
        self.db = defaultdict(UserInfo)

    def change_from(self,user_id,  val):
        self.db[user_id].f = val

    def change_to(self, user_id, val):
        self.db[user_id].t = val

    def get_pair(self, user_id):
        user = self.db[user_id]
        return user.f, user.t


class Converter:
    @staticmethod
    def get_price(values):
        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров')

        quote, base, amount = values

        if quote == base:
            raise ConvertionException(f'Не удалось перевести одинаковые валюты {base}')

        quote_ticker = quote
        base_ticker = base
        try:
            amount == float(amount)
        except ValueError:
            ConvertionException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://free.currconv.com/api/v7/convert?q={quote_ticker}_{base_ticker}&compact=ultra&apiKey={access_key2}')
        total_base = float(json.loads(r.content)[f'{quote_ticker}_{base_ticker}']) * float(amount)

        return round(total_base, 3)
