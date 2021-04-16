class Coder:
    message = []

    def __init__(self, message):
        self.message = message

    def coder(self):
        z = 0
        for elements in self.message:
            if elements == 1:
                z += 1
        if z % 2 == 0:
            self.message.append(0)
        else:
            self.message.append(1)
