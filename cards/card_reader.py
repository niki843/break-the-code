import json
import os
import re

from entity.condition_card import ConditionCard
from cards.card_conditions import CARD_ID_TO_CONDITION_MAP
from constants import CARDS_PATH
from utils.singelton import Singleton


class CardReader(Singleton):
    def __init__(self):
        self.cards = self.__read_cards()
        self.__map_condition_functions_to_cards()

    def __read_cards(self):
        card_names = [
            f
            for f in os.listdir(f"cards{os.path.sep}")
            if re.match(r"[0-9]+.*\.json", f)
        ]
        cards = []

        for card in card_names:
            f = open(CARDS_PATH + card)
            x = json.load(f, object_hook=lambda d: ConditionCard(**d))
            cards.append(x)

        return cards

    def __map_condition_functions_to_cards(self):
        [
            setattr(card, "check_condition", CARD_ID_TO_CONDITION_MAP.get(card.id))
            for card in self.cards
            if CARD_ID_TO_CONDITION_MAP.get(card.id)
        ]
