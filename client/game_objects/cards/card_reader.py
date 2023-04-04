import json
import os
import re
import pathlib

from client.game_objects.cards.card_conditions import CARD_ID_TO_CONDITION_MAP
from client.game_objects.entities.condition_card import ConditionCard
from client.utils.singelton import Singleton


class CardReader(Singleton):
    def __init__(self):
        self.cards = self.__read_cards()
        self.__map_condition_functions_to_cards()

    def __read_cards(self):
        current_path = f"{pathlib.Path(__file__).parent.resolve()}{os.path.sep}"
        cards = []
        for f in os.listdir(current_path):
            if re.match(r"[0-9]+.*.json", f):
                with open(current_path + f) as curr_file:
                    x = json.load(curr_file, object_hook=lambda d: ConditionCard(**d))
                    cards.append(x)

        return cards

    def __map_condition_functions_to_cards(self):
        [
            setattr(card, "check_condition", CARD_ID_TO_CONDITION_MAP.get(card.id))
            for card in self.cards
            if CARD_ID_TO_CONDITION_MAP.get(card.id)
        ]
