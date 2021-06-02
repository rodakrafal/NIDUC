from Decoder import *
from Generator import *
from Coder import *
from Chanel import *
from Ber import *
from Model import *
import copy
import matplotlib.pyplot as plt


def createGraph(par1, par2, textX, textY, par3, par4, textX2, textY2, par5, par6, textX3, textY4):
    plt.subplot(1, 3, 1)
    plt.plot(par1, par2)
    plt.xlabel(textX)
    plt.ylabel(textY)
    plt.subplot(1, 3, 2)
    plt.plot(par3, par4)
    plt.xlabel(textX2)
    plt.ylabel(textY2)
    plt.subplot(1, 3, 3)
    plt.plot(par5, par6)
    plt.xlabel(textX3)
    plt.ylabel(textY4)
    plt.show()


def const_size(size, max_size, percent):
    arr_errors = []
    size_array = []
    arr_ber = []
    arr_e = []
    while size <= max_size:
        size_array.append(size)
        counter = 0
        count = 0
        ber = 0
        e = 0
        while counter < 100:
            message = Generator(size)
            message.generate()
            coder = Coder(message.message)
            coder.coder()
            channel = Chanel(coder.message)
            channel.channel(percent)
            decoder = Decoder()
            decoder.message = copy.copy(channel.message)
            decoder.size = size
            tmp = decoder.decode()
            if tmp == 1:
                count += 1
            counter += 1
            incorrect_bits = compare(message.message, decoder.message)
            tem = (len(decoder.message) - incorrect_bits) / len(decoder.message)
            temp = incorrect_bits / len(decoder.message)
            ber += temp
            e += tem
            message.message.clear()
        arr_errors.append(count)
        ber /= 100
        e /= 100
        arr_ber.append(ber)
        arr_e.append(e)
        size += 50
    print(arr_errors)
    print(arr_ber)
    print(arr_e)
    print(size_array)
    createGraph(size_array, arr_errors, "Rozmiar tablicy", "Liczba znalezionych błędów na 100 prób",
                size_array, arr_ber, "Rozmiar tablicy", "Współczynnik BER",
                size_array, arr_e, "Rozmiar tablicy", "Współczynnik E")


def const_percent(size, max_percent):
    percent = 0
    arr_errors = []
    percent_array = []
    arr_ber = []
    arr_e = []
    while percent <= max_percent:
        percent_array.append(percent)
        counter = 0
        count = 0
        ber = 0
        e = 0
        while counter < 100:
            message = Generator(size)
            message.generate()
            coder = Coder(message.message)
            coder.coder()
            channel = Chanel(coder.message)
            channel.channel(percent)
            decoder = Decoder()
            decoder.message = copy.copy(channel.message)
            decoder.size = size
            tmp = decoder.decode()
            if tmp == 1:
                count += 1
            counter += 1
            incorrect_bits = compare(message.message, decoder.message)
            tem = (len(decoder.message) - incorrect_bits) / len(decoder.message)
            temp = incorrect_bits / len(decoder.message)
            ber += temp
            e += tem
            message.message.clear()
        ber /= 100
        e /= 100
        arr_ber.append(ber)
        arr_errors.append(count)
        arr_e.append(e)
        percent += 1
    print(arr_errors)
    print(arr_ber)
    print(percent_array)
    createGraph(percent_array, arr_errors, "Procent zakłóceń", "Liczba znalezionych błędów na 100 prób",
                percent_array, arr_ber, "Procent zakłóceń", "Wspolczynnik ber",
                size_array, arr_e, "Rozmiar tablicy", "Współczynnik E")


def main():
    a = int(input("Wybierz rodzaj arq:\n 1 - Podstatwowy\n 2 - Stop and wait z bitem parzystości\n"))
    if a == 1:
        graph_type = int(input("Wybierz typ grafu:\n 1 - zestałym rozmiarem ramki \n 2 - zestałym procentem błędu\n"))
        if graph_type == 1:
            max_size = int(input("Podaj maksymalna długość ramki\n"))
            size = int(input("Podaj początkowy rozmiar ramki\n"))
            percent = int(input("Podaj procent zakłamania\n"))
            const_size(size, max_size, percent)
        if graph_type == 2:
            size = int(input("Podaj rozmiar ramki\n"))
            max_percent = int(input("Podaj maxymalny procent zakłamania\n"))
            const_percent(size, max_percent)
    if a == 2:
        message = Generator(100)
        message.generate()

        coder = Coder(message.message)
        coder.createFrames() # coś tu trzeba naprawić z bitami parzystości
        decoder = Decoder()

        i = 0
        while i < 1:
            channel = Chanel(coder.sentFrames)
            channel.frameLength = coder.getFrameLength()
            channel.howManyFrames = coder.getHowManyFrames()
            channel.channelForStopAndWait(20)

            decoder.frameLength = coder.getFrameLength()
            decoder.howManyFrames = coder.getHowManyFrames()
            decoder.message = copy.copy(channel.message[i])

            print(coder.sentFrames)
            print(channel.message)
            print(decoder.message)
            print(decoder.countNumberOfOnes())
            print(decoder.getParityBit())
            print(decoder.decode())
            i += 1


if __name__ == "__main__":
    main()
