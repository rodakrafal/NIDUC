class Decoder:
    message = []

    def __init__(self, msg):
        self.message = msg
        self.size = len(msg) - 1

    def getParityBit(self):
        return self.message[self.size]

    def countNumberOfOnes(self):
        counter = 0
        i = 0
        while i < self.size:
            if self.message[i] == 1:
                counter += 1
            i += 1
        counter = counter % 2
        return counter

    def printArray(self):
        print(self.message)

    def decode(self):
        number_of_ones = self.countNumberOfOnes()
        parity_bit = self.getParityBit()
        if parity_bit == number_of_ones:
            return bool(1)
        else:
            return bool(0)
