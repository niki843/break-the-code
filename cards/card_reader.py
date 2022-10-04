import json
import os

from card import Card
from constants import CARDS_PATH
from utils.singelton import Singleton


class CardReader(Singleton):
    def __init__(self):
        self.cards = self.__read_cards()

    def __read_cards(self):
        card_names = os.listdir("cards\\")
        x = None

        for card in card_names:
            f = open(CARDS_PATH + card)
            x = json.load(f, object_hook=lambda d: Card(**d))

        return x

