from Decoder import *
from Generator import *
from Coder import *
from Channel import *
from Ber import *
import copy
import matplotlib.pyplot as plt


def createGraph(par1, par2, textX, textY):
    plt.plot(par1, par2)
    plt.xlabel(textX)
    plt.ylabel(textY)
    plt.show()


def const_size(max_size, percent, frameamount, framecapacity, enlarging):
    errors = []
    sizeFrame = []
    while framecapacity <= max_size:
        j = 0
        incorrectFrames = 0
        messagesize = frameamount * framecapacity
        while j < 10:
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
                if decoder.decodeParity() == 1:
                    incorrectFrames += 1

                decoder.createFrame()
                i += 1
            message.message.clear()
            coder.message.clear()
            coder.sentFrames.clear()
            channel.message.clear()
            decoder.message.clear()
            decoder.receivedFrames.clear()
            j += 1
        print(framecapacity)
        errors.append(incorrectFrames / j)
        sizeFrame.append(framecapacity)
        framecapacity += enlarging
    print(errors)
    print(sizeFrame)
    createGraph(sizeFrame, errors, "Rozmiar ramki", "Liczba wykrytych błędów")


def const_percent(max_percent, percent, frameamount, framecapacity, enlarging):
    errors = []
    percentArray = []
    while percent <= max_percent:
        j = 0
        incorrectFrames = 0
        messagesize = frameamount * framecapacity
        while j < 10:
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
                if decoder.decodeParity() == 1:
                    incorrectFrames += 1

                decoder.createFrame()
                i += 1
            message.message.clear()
            coder.message.clear()
            coder.sentFrames.clear()
            channel.message.clear()
            decoder.message.clear()
            decoder.receivedFrames.clear()
            j += 1
        print(percent)
        errors.append(incorrectFrames / j)
        percentArray.append(percent)
        percent += enlarging
    print(errors)
    print(percentArray)
    createGraph(percentArray, errors, "Procent przekłamania", "Liczba wykrytych błędów")


def ber_parity_bits_const_percent(max_size, percent, frameamount, framecapacity, enlarging):
    berArray = []
    eArray = []
    sizeFrame = []
    while framecapacity <= max_size:
        j = 0
        ber = 0
        e = 0
        messagesize = frameamount * framecapacity
        while j < 10:
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

                if decoder.ack == 0:
                    i += 1
                    decoder.createFrame()
            incorrectFrames = compare(message.message, decoder.receivedFrames)
            ber += incorrectFrames / len(decoder.receivedFrames)
            e += ((len(decoder.receivedFrames) - incorrectFrames) / len(coder.sentFrames))
            message.message.clear()
            coder.message.clear()
            coder.sentFrames.clear()
            channel.message.clear()
            decoder.message.clear()
            decoder.receivedFrames.clear()
            j += 1
        print(framecapacity)
        berArray.append(ber / j)
        eArray.append(e / j)
        sizeFrame.append(framecapacity)
        framecapacity += enlarging
    print(berArray)
    print(eArray)
    print(sizeFrame)
    createGraph(sizeFrame, berArray, "Rozmiar ramki", "Wskaźnik BER")
    createGraph(sizeFrame, eArray, "Rozmiar ramki", "Wskaźnik E")


def ber_parity_bits_const_size(max_percent, percent, frameamount, framecapacity, enlarging):
    berArray = []
    eArray = []
    percentArray = []
    while percent <= max_percent:
        j = 0
        e = 0
        ber = 0
        messagesize = frameamount * framecapacity
        while j < 10:
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

                if decoder.ack == 0:
                    i += 1
                    decoder.createFrame()
            incorrectFrames = compare(message.message, decoder.receivedFrames)
            ber += incorrectFrames / len(decoder.receivedFrames)
            e += ((len(decoder.receivedFrames) - incorrectFrames) / len(coder.sentFrames))
            message.message.clear()
            coder.message.clear()
            coder.sentFrames.clear()
            channel.message.clear()
            decoder.message.clear()
            decoder.receivedFrames.clear()
            j += 1
        print(percent)
        berArray.append(ber / j)
        eArray.append(e / j)
        percentArray.append(percent)
        percent += enlarging
    print(berArray)
    print(eArray)
    print(percentArray)
    createGraph(percentArray, berArray, "Rozmiar ramki", "Wskaźnik BER")
    createGraph(percentArray, eArray, "Rozmiar ramki", "Wskaźnik E")


def main():
    print("-------------------------------- ARQ --------------------------------")
    a = int(input("Wybierz rodzaj zabezpieczenia kontroli poprawności wysłanego pakietu:\n 1 - Brak zabezpieczenia*\n "
                  "2 - Bit parzystości\n 3 - Cykliczny kod nadmiarowy\n\tWybór: "))
    frameamount = int(input("Podaj ilośc ramek: "))
    framecapacity = int(input("Podaj ilośc bitów w ramce: "))
    messagesize = frameamount * framecapacity
    percent = int(input("Podaj procent przekłamania: "))

    if a == 1:
        graph_type = int(input("Wybierz typ grafu:\n 1 - zestałym procentem błędu \n 2 - zestałym rozmiarem ramki\n"))
        if graph_type == 1:
            max_size = int(input("Podaj maxymalny rozmiar ramki\n"))
            enlarging = int(input("Podaj o ile bedziemy zwikszać ramke\n"))
            ber_parity_bits_const_percent(max_size, percent, frameamount, framecapacity, enlarging)
        if graph_type == 2:
            max_percent = int(input("Podaj maxymalny procent zakłamania\n"))
            enlarging = int(input("Podaj o ile procent bedziemy zwikszać przekłamanie\n"))
            const_percent(max_percent, percent, frameamount, framecapacity, enlarging)
    elif a == 2:
        graph_type = int(input("Wybierz typ grafu:\n 1 - zestałym procentem błędu \n 2 - zestałym rozmiarem ramki\n"))
        if graph_type == 1:
            max_size = int(input("Podaj maxymalny rozmiar ramki\n"))
            enlarging = int(input("Podaj o ile bedziemy zwikszać ramke\n"))
            ber_parity_bits_const_percent(max_size, percent, frameamount, framecapacity, enlarging)
        if graph_type == 2:
            max_percent = int(input("Podaj maxymalny procent zakłamania\n"))
            enlarging = int(input("Podaj o ile procent bedziemy zwikszać przekłamanie\n"))
            ber_parity_bits_const_size(max_percent, percent, frameamount, framecapacity, enlarging)

        # message = Generator(messagesize)
        # message.generate()
        #
        # coder = Coder(message.message)
        # coder.howManyFrames = frameamount
        # coder.frameLength = framecapacity
        # coder.createFrames(True, 0)
        # decoder = Decoder()
        # i = 0
        # while i < frameamount:
        #     channel = Channel(coder.sentFrames)
        #     channel.frameLength = framecapacity
        #     channel.howManyFrames = frameamount
        #     channel.channelParity(percent)
        #
        #     decoder.frameLength = coder.getFrameLength()
        #     decoder.message = copy.deepcopy(channel.message[i])
        #     decoder.decodeParity()
        #
        #     if decoder.ack == 0:
        #         i += 1
        #         decoder.createFrame()
        #     print(message.message)
        #     print(decoder.receivedFrames)

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
