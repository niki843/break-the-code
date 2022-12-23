import json
import os
import re
import pathlib

from entity.condition_card import ConditionCard
from cards.card_conditions import CARD_ID_TO_CONDITION_MAP
from utils.singelton import Singleton


class CardReader(Singleton):
    def __init__(self):
        self.cards = self.__read_cards()
        self.__map_condition_functions_to_cards()

    def __read_cards(self):
        current_path = f"{pathlib.Path(__file__).parent.resolve()}{os.path.sep}"
        card_names = [
            f
            for f in os.listdir(current_path)
            if re.match(r"[0-9]+.*.json", f)
        ]
        cards = []

        for card in card_names:
            f = open(current_path + card)
            x = json.load(f, object_hook=lambda d: ConditionCard(**d))
            cards.append(x)

        return cards

    def __map_condition_functions_to_cards(self):
        [
            setattr(card, "check_condition", CARD_ID_TO_CONDITION_MAP.get(card.id))
            for card in self.cards
            if CARD_ID_TO_CONDITION_MAP.get(card.id)
        ]
