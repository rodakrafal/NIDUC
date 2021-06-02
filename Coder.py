import copy


class Coder:
    message = []
    howManyFrames = 20
    frameLength = 5
    sentFrames = []

    def __init__(self, message):
        self.message = copy.copy(message)

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
        sum = 0
        for j in range(self.frameLength):
            sum += frame[j]
        return sum % 2

    def createFrames(self):
        for i in range(self.howManyFrames):
            self.sentFrames.append([])
            for j in range(self.frameLength):
                self.sentFrames[i].append(self.message[i * self.frameLength + j])
            self.sentFrames[i].append(self.code_frames(self.sentFrames[i])) # coś tu się pierdoli

    def getHowManyFrames(self):
        return self.howManyFrames

    def getFrameLength(self):
        return self.frameLength
