import random

class Generator:
    def __init__(self, size):
        self._size = size
        self._message = []

    def get_size(self):
        return self._size

    def set_size(self, size):
        self._size = size

    def get_message(self):
        print(self._message)

    def generate(self):
        for x in range(self._size):
            self._message.append(random.randint(0, 1))
        return self._message

