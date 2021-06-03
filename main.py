from Decoder import *
from Generator import *
from Coder import *
from Channel import *
from Ber import *
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
            channel = Channel(coder.message)
            channel.channel(percent)
            decoder = Decoder()
            decoder.message = copy.deepcopy(channel.message)
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
            channel = Channel(coder.message)
            channel.channel(percent)
            decoder = Decoder()
            decoder.message = copy.deepcopy(channel.message)
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
                percent_array, arr_e, "Rozmiar tablicy", "Współczynnik E")


def main():
    print("-------------------------------- ARQ --------------------------------")
    a = int(input("Wybierz rodzaj zabezpieczenia kontroli poprawności wysłanego pakietu:\n 1 - Brak zabezpieczenia*\n "
                  "2 - Bit parzystości\n 3 - Cykliczny kod nadmiarowy\n\tWybór: "))
    frameamount = int(input("Podaj ilośc ramek: "))
    framecapacity = int(input("Podaj ilośc bitów w ramce: "))
    messagesize = frameamount * framecapacity
    percent = int(input("Podaj procent przekłamania: "))

    if a == 1:
        graph_type = int(input("Wybierz typ grafu:\n 1 - zestałym rozmiarem ramki \n 2 - zestałym procentem błędu\n"))
        if graph_type == 1:
            print("na razie nic")
        if graph_type == 2:
            max_percent = int(input("Podaj maxymalny procent zakłamania\n"))


        message = Generator(messagesize)
        message.generate()

        coder = Coder(message.message)
        coder.howManyFrames = frameamount
        coder.frameLength = framecapacity
        coder.createFrames(True, 0)
        decoder = Decoder()
        i = 0
        while i < frameamount:
            channel = Channel(coder.sentFrames)
            channel.frameLength = framecapacity
            channel.howManyFrames = frameamount
            channel.channelParity(percent)

            decoder.frameLength = coder.getFrameLength()
            decoder.message = copy.deepcopy(channel.message[i])
            decoder.decodeParity()

            # print(coder.sentFrames)
            # print(channel.message)
            # print(decoder.message)
            # print(decoder.countNumberOfOnes())
            # print(decoder.getParityBit())

            decoder.createFrame()
            i += 1

        print(message.message)
        print(decoder.receivedFrames)
    elif a == 2:
        message = Generator(messagesize)
        message.generate()

        coder = Coder(message.message)
        coder.howManyFrames = frameamount
        coder.frameLength = framecapacity
        coder.createFrames(True, 0)
        decoder = Decoder()
        i = 0
        while i < frameamount:
            channel = Channel(coder.sentFrames)
            channel.frameLength = framecapacity
            channel.howManyFrames = frameamount
            channel.channelParity(percent)

            decoder.frameLength = coder.getFrameLength()
            decoder.message = copy.deepcopy(channel.message[i])
            decoder.decodeParity()

            print(coder.sentFrames)
            print(channel.message)
            print(decoder.message)
            print(decoder.countNumberOfOnes())
            print(decoder.getParityBit())

            if decoder.ack == 0:
                i += 1
                decoder.createFrame()
            print(message.message)
            print(decoder.receivedFrames)

    elif a == 3:
        choice = int(input("Podaj który kod CRC chcesz wybrać (0-3): "))

        message = Generator(messagesize)
        message.generate()

        coder = Coder(message.message)
        coder.howManyFrames = frameamount
        coder.frameLength = framecapacity
        coder.createFrames(False, choice)
        decoder = Decoder()
        i = 0
        while i < frameamount:
            channel = Channel(coder.sentFrames)
            channel.frameLength = framecapacity
            channel.howManyFrames = frameamount
            channel.channelCRC(percent)

            decoder.frameLength = coder.getFrameLength()
            decoder.message = copy.deepcopy(channel.message[i])
            decoder.decodeCRC(choice)

            if decoder.ack == 0:
                i += 1
                decoder.createFrame()

            # print(message.message)
            # print(decoder.receivedFrames)
            # i += 1

        print(coder.sentFrames)
        print(channel.message)
        print(message.message)
        print(decoder.receivedFrames)
    else:
        print("\nWybrano błędną opcje, program zakończy działanie.")


if __name__ == "__main__":
    main()
