import random
import copy


class Chanel:
    message = []
    frameLength = 0
    howManyFrames = 0

    def __init__(self, message):
        self.message = copy.copy(message)

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

    def channelForStopAndWait(self, p):
        for i in range(self.howManyFrames):
            for j in range(self.frameLength):
                rand = random.randint(0, 100)
                if rand < p:
                    if self.message[i][j] == 1:
                        self.message[i][j] = 0
                    else:
                        self.message[i][j] = 1
