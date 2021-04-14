import random


class Generator:
    message = []

    def __init__(self, size):
        self._size = size

    def get_size(self):
        return self._size

    def set_size(self, size):
        self._size = size

    def get_message(self):
        return self.message

    def generate(self):
        for x in range(self._size):
            self.message.append(random.randint(0, 1))
        return self.message



