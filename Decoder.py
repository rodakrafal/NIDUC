from CRC import *


class Decoder:
    message = []
    receivedFrames = []
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

    def decodeParity(self):
        number_of_ones = self.countNumberOfOnes()
        parity_bit = self.getParityBit()
        if parity_bit == number_of_ones:
            self.ack = 0
            return 0
        else:
            self.ack = 1
            return 1

    def createFrame(self):
        for j in range(self.frameLength):
            self.receivedFrames.append(self.message[j])
        self.howManyFrames += 1

    def decodeCRC(self):
        crc = CRC(self.message[:self.frameLength])
        # print(self.message)
        x = int(crc.getCRS(0))
        y = crc.getCRCbites()
        temp = [int(digit) for digit in bin(x)[2:]]
        temptofill = y - len(temp)
        for z in range(temptofill):
            temp.insert(z, 0)
        y = 0
        for z in range(self.frameLength, len(self.message)):
            if self.message[z] != temp[y]:
                self.ack = 1
                return 1
            y += 1
        self.ack = 0
        return 0
