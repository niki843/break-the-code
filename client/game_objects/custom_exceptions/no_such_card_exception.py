class NoSuchCardException(Exception):
    def __init__(self, card_id, message_end, message="Card {0} is not existing {1}"):
        self.card_id = card_id
        self.message = message
        self.message_end = message_end
        super().__init__(self.message.format(self.card_id, self.message_end))

    def __str__(self):
        return self.message.format(self.card_id, self.message_end)
