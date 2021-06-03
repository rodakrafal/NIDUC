from CRC import *
import copy


class Coder:
    message = []
    howManyFrames = 20
    frameLength = 5
    sentFrames = []

    def __init__(self, message):
        self.message = copy.deepcopy(message)

    def coder(self):
        z = 0
        for elements in self.message:
            if elements == 1:
                z += 1
        if z % 2 == 0:
            self.message.append(0)
        else:
            self.message.append(1)

    def code_frames(self, frame):
        sum = frame.count(1)
        return sum % 2

    def createFrames(self, isparity, choice):
        for i in range(self.howManyFrames):
            self.sentFrames.append([])
            for j in range(self.frameLength):
                self.sentFrames[i].append(self.message[i * self.frameLength + j])
            if isparity:
                self.sentFrames[i].append(self.code_frames(self.sentFrames[i]))
            else:
                crc = CRC(self.sentFrames[i])
                x = int(crc.getCRS(choice))
                y = crc.getCRCbites()
                temp = [int(digit) for digit in bin(x)[2:]]
                temptofill = y - len(temp)
                for z in range(temptofill):
                    temp.insert(z,0)
                for z in range(y):
                    self.sentFrames[i].append(temp[z])

    def getHowManyFrames(self):
        return self.howManyFrames

    def getFrameLength(self):
        return self.frameLength