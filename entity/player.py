class Player:
    def __init__(self, player_id, name):
        self.id = player_id
        self.name = name
        self.number_cards = []

    def get_name(self):
        return self.name

    def get_cards(self):
        return self.number_cards.copy()

    def get_id(self):
        return self.id

    def order_cards(self):
        self.number_cards.sort(key=lambda x: x.number)
        self.number_cards.sort(key=lambda x: x.color.value)

    def update_number_cards(self, numbers: list):
        if len(numbers) != 5 and len(numbers) != 4:
            raise ValueError("Invalid amount of numbers, 4-5 numbers are expected!")

        if self.number_cards:
            raise Exception("Numbers have been already set!")

        self.number_cards = numbers
