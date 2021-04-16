from Decoder import *
from Generator import *
from Coder import *
from Chanel import *
import matplotlib.pyplot as plt


def createGraph():
    a = input("Wybierz typ grafu:\n 1 - zestałym rozmiarem ramki \n 2 - zestałym procentem błędu\n")
    if a == 1:
        size = 20
        arr = []
        size_array = []
        while size < 1000:
            size_array.append(size)
            counter = 0
            count = 0
            while counter < 100:
                message = Generator(size)
                message.generate()
                coder = Coder(message.message)
                coder.coder()
                channel = Chanel(coder.message)
                channel.channel(5)
                decoder = Decoder(channel.message)
                tmp = decoder.decode()
                if tmp == 1:
                    count += 1
                counter += 1
            arr.append(count)
            size += 50
        print(arr)
        print(size_array)
        plt.plot(size_array, arr)
        plt.xlabel("Rozmiar tablicy")
        plt.ylabel("Liczba znalezionych błędów na 100 prób")
        plt.show()
    if a == 2:
        percent = 0
        arr = []
        percent_array = []
        while percent < 20:
            percent_array.append(percent)
            counter = 0
            count = 0
            while counter < 100:
                message = Generator(80)
                message.generate()
                coder = Coder(message.message)
                coder.coder()
                channel = Chanel(coder.message)
                channel.channel(percent)
                decoder = Decoder(channel.message)
                tmp = decoder.decode()
                if tmp == 1:
                    count += 1
                counter += 1
            print(percent)
            arr.append(count)
            percent += 1
        print(arr)
        print(percent_array)
        plt.plot(percent_array, arr)
        plt.xlabel("Procent zakłóceń")
        plt.ylabel("Liczba znalezionych błędów na 100 prób")
        plt.show()


def main():
    a = int(input("Wybierz typ grafu:\n 1 - zestałym rozmiarem ramki \n 2 - zestałym procentem błędu\n"))
    if a == 1:
        print("elo")
        size = 20
        arr = []
        size_array = []
        while size < 1000:
            size_array.append(size)
            counter = 0
            count = 0
            while counter < 100:
                message = Generator(size)
                message.generate()
                coder = Coder(message.message)
                coder.coder()
                channel = Chanel(coder.message)
                channel.channel(5)
                decoder = Decoder(channel.message)
                tmp = decoder.decode()
                if tmp == 1:
                    count += 1
                counter += 1
            arr.append(count)
            size += 50
        print(arr)
        print(size_array)
        plt.plot(size_array, arr)
        plt.xlabel("Rozmiar tablicy")
        plt.ylabel("Liczba znalezionych błędów na 100 prób")
        plt.show()
    if a == 2:
        percent = 0
        arr = []
        percent_array = []
        while percent < 20:
            percent_array.append(percent)
            counter = 0
            count = 0
            while counter < 100:
                message = Generator(80)
                message.generate()
                coder = Coder(message.message)
                coder.coder()
                channel = Chanel(coder.message)
                channel.channel(percent)
                decoder = Decoder(channel.message)
                tmp = decoder.decode()
                if tmp == 1:
                    count += 1
                counter += 1
            print(percent)
            arr.append(count)
            percent += 1
        print(arr)
        print(percent_array)
        plt.plot(percent_array, arr)
        plt.xlabel("Procent zakłóceń")
        plt.ylabel("Liczba znalezionych błędów na 100 prób")
        plt.show()


if __name__ == "__main__":
    main()
