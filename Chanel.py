import random


class Chanel:
    message = []

    def __init__(self, message):
        self.message = message

    def channel(self, p):
        length = len(self.message)
        i = 0
        while i < length - 1:
            rand = random.randint(0, 100)
            if rand < p:
                if self.message[i] == 1:
                    self.message[i] = 0
                else:
                    self.message[i] = 1
            i += 1