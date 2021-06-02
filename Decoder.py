import copy


class Decoder:
    message = []
    frameLength = 0
    howManyFrames = 0
    ack = 0

    # def __init__(self, msg):
    #     self.message = copy.copy(msg)
    #     self.size = len(msg) - 1

    def getParityBit(self):
        return self.message[self.frameLength]

    def countNumberOfOnes(self):
        counter = 0
        i = 0
        while i < self.frameLength:
            if self.message[i] == 1:
                counter += 1
            i += 1
        counter = counter % 2
        return counter

    def decode(self):
        number_of_ones = self.countNumberOfOnes()
        parity_bit = self.getParityBit()
        if parity_bit == number_of_ones:
            return 0
        else:
            return 1

    # def createFrame(self, message):
