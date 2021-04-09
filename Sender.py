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


def channel(array, p):
    for x in range(len(array)):
        if random.randint(0, 100) < p:
            if array[x] == 1:
                array[x] = 0
            else:
                array[x] = 1

    return array


def coder(array, n):
    y = 0
    z = 0
    for x in range(len(array)):
        if (x % n) == 0:
            z += 1
    print(z)

percent = 5
data1 = Generator(1000)
var = data1.generate()
print(var)
var2 = var.copy()
channel(var2, percent)
coder(var, 4)
