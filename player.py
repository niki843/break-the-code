

class Player:
    def __init__(self, player_id, name):
        self.id = player_id
        self.name = name
        self.numbers = []

    def get_name(self):
        return self.name

    def get_numbers(self):
        return self.numbers.copy()

    def update_numbers(self, numbers: list):
        if len(numbers) != 5 and len(numbers) != 4:
            raise ValueError("Invalid amount of numbers, 4-5 numbers are expected!")

        if self.numbers:
            raise Exception("Numbers have been already set!")

        self.numbers = numbers
