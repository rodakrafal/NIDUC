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


def createGraph2(par1, par2, textX, textY, par3, par4, par5, par6, label1, label2, label3, label4, label5):
    plt.plot(par1, par2, label = label1)
    plt.plot(par1, par3, label = label2)
    plt.plot(par1, par4, label=label3)
    plt.plot(par1, par5, label=label4)
    # plt.plot(par1, par6, label=label5)
    plt.xlabel(textX)
    plt.ylabel(textY)
    plt.legend()
    plt.show()


def createGraphPareto(ber, e, ber1, e1, ber2, e2, ber3, e3, ber4, e4, ber5, e5, ber6, e6, ber7, e7, ber8, e8, ber9, e9,
                      textX, textY, label1, label2, label3, label4, label5, label6, label7, label8, label9, label10,
                      title):
    print("\n")
    print(ber)
    print(ber1)
    print(ber2)
    print(ber3)
    print(ber4)
    print(e)
    print(e1)
    print(e2)
    print(e3)
    print(e4)
    plt.plot(1, 0, "ro", label="Sytuacja idealna", color="orange")
    plt.plot(e, ber, "ro", label=label1, color="red")
    plt.plot(e1, ber1, "ro", label=label2, color="blue")
    plt.plot(e2, ber2, "ro", label=label3, color="green")
    plt.plot(e3, ber3, "ro", label=label4, color="yellow")
    plt.plot(e4, ber4, "ro", label=label5, color="black")
    plt.plot(e5, ber5, "ro", label=label6, color="cyan")
    plt.plot(e6, ber6, "ro", label=label7, color="gray")
    plt.plot(e7, ber7, "ro", label=label8, color="magenta")
    plt.plot(e8, ber8, "ro", label=label9, color="pink")
    plt.plot(e9, ber9, "ro", label=label10, color="purple")
    plt.title(title)
    plt.xlim(-0.1, 1.1)
    plt.ylim(-0.1, 1.1)
    plt.xlabel(textX)
    plt.ylabel(textY)
    plt.legend()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.tight_layout()
    plt.gca().invert_xaxis()
    plt.show()


def const_size(max_size, percent, frameamount, framecapacity, enlarging):
    errors = []
    sizeFrame = []
    while framecapacity <= max_size:
        j = 0
        incorrectFrames = 0
        messagesize = frameamount * framecapacity
        while j < 4:
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
        while j < 4:
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


def parity_bit_pareto(percent, messagesize, frameamount, framecapacity, ber, e):
    j = 0
    while j < 4:
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
        j += 1
        incorrectFrames = compare(message.message, decoder.receivedFrames)
        ber += incorrectFrames / len(decoder.receivedFrames)
        e += ((len(decoder.receivedFrames) - incorrectFrames) / (len(coder.sentFrames[0]) * frameamount))
        message.message.clear()
        coder.message.clear()
        coder.sentFrames.clear()
        channel.message.clear()
        decoder.message.clear()
        decoder.receivedFrames.clear()
    ber /= j
    e /= j
    return [ber, e]


def CRC_pareto(choice, percent, messagesize, frameamount, framecapacity, ber, e):
    j = 0
    while j < 1:

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
        j += 1
        incorrectFrames = compare(message.message, decoder.receivedFrames)
        ber += incorrectFrames / len(decoder.receivedFrames)
        e += ((len(decoder.receivedFrames) - incorrectFrames) / (len(coder.sentFrames[0]) * frameamount))
        message.message.clear()
        coder.message.clear()
        coder.sentFrames.clear()
        channel.message.clear()
        decoder.message.clear()
        decoder.receivedFrames.clear()
    ber /= j
    e /= j
    print(choice)
    return [ber, e]



def ber_parity_bits_const_percent(max_size, percent, frameamount, framecapacity, enlarging):
    berArray = []
    eArray = []
    sizeFrame = []
    while framecapacity <= max_size:
        j = 0
        ber = 0
        e = 0
        messagesize = frameamount * framecapacity
        while j < 4:
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
            e += ((len(decoder.receivedFrames) - incorrectFrames) / (len(coder.sentFrames[0])*frameamount))
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


def ber_parity_bits_const_percent2(max_size, percent, frameamount, framecapacity, enlarging, sizeFrame, eArray,
                               berArray, generate):
    #berArray = []
    #eArray = []
    #sizeFrame = []
    while framecapacity <= max_size:
        j = 0
        ber = 0
        e = 0
        messagesize = frameamount * framecapacity
        while j < 4:
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
            e += ((len(decoder.receivedFrames) - incorrectFrames) / (len(coder.sentFrames[0])*frameamount))
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
    if not generate:
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
        while j < 4:
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
            e += ((len(decoder.receivedFrames) - incorrectFrames) / (len(coder.sentFrames[0])*frameamount))
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
    createGraph(percentArray, berArray, "Procent przekłamania", "Wskaźnik BER")
    createGraph(percentArray, eArray, "Procent przekłamania", "Wskaźnik E")


def ber_parity_bits_const_size2(max_percent, percent, frameamount, framecapacity, enlarging, percentArray, eArray,
                               berArray, generate):
    # berArray = []
    # eArray = []
    # percentArray = []
    while percent <= max_percent:
        j = 0
        e = 0
        ber = 0
        messagesize = frameamount * framecapacity
        while j < 4:
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
            e += ((len(decoder.receivedFrames) - incorrectFrames) / (len(coder.sentFrames[0])*frameamount))
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
    if not generate:
        createGraph(percentArray, berArray, "Procent przekłamania", "Wskaźnik BER")
        createGraph(percentArray, eArray, "Procent przekłamania", "Wskaźnik E")


def CRC_BER_const_percent(max_size, percent, frameamount, framecapacity, enlarging, choice):
    berArray = []
    eArray = []
    sizeFrame = []
    while framecapacity <= max_size:
        j = 0
        ber = 0
        e = 0
        messagesize = frameamount * framecapacity
        while j < 4:
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
            incorrectFrames = compare(message.message, decoder.receivedFrames)
            ber += incorrectFrames / len(decoder.receivedFrames)
            e += ((len(decoder.receivedFrames) - incorrectFrames) / (len(coder.sentFrames[0])*frameamount))
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


def CRC_BER_const_percent2(max_size, percent, frameamount, framecapacity, enlarging, choice, sizeFrame, eArray,
                       berArray, generate):
    #berArray = []
    #eArray = []
    #sizeFrame = []
    while framecapacity <= max_size:
        j = 0
        ber = 0
        e = 0
        messagesize = frameamount * framecapacity
        while j < 4:
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
            incorrectFrames = compare(message.message, decoder.receivedFrames)
            ber += incorrectFrames / len(decoder.receivedFrames)
            e += ((len(decoder.receivedFrames) - incorrectFrames) / (len(coder.sentFrames[0])*frameamount))
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
    if not  generate:
        createGraph(sizeFrame, berArray, "Rozmiar ramki", "Wskaźnik BER")
        createGraph(sizeFrame, eArray, "Rozmiar ramki", "Wskaźnik E")


def CRC_BER_const_size(max_percent, percent, frameamount, framecapacity, enlarging, choice):
    berArray = []
    eArray = []
    percentArray = []
    while percent <= max_percent:
        j = 0
        e = 0
        ber = 0
        messagesize = frameamount * framecapacity
        while j < 1:
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
            incorrectFrames = compare(message.message, decoder.receivedFrames)
            ber += incorrectFrames / len(decoder.receivedFrames)
            e += ((len(decoder.receivedFrames) - incorrectFrames) / (len(coder.sentFrames[0])*frameamount))
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
    createGraph(percentArray, berArray, "Procent przekłamania", "Wskaźnik BER")
    createGraph(percentArray, eArray, "Procent przekłamania", "Wskaźnik E")


def CRC_BER_const_size2(max_percent, percent, frameamount, framecapacity, enlarging, choice, percentArray, eArray,
                       berArray, generate):
    # berArray = []
    # eArray = []
    # percentArray = []
    while percent <= max_percent:
        j = 0
        e = 0
        ber = 0
        messagesize = frameamount * framecapacity
        while j < 1:
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
            incorrectFrames = compare(message.message, decoder.receivedFrames)
            ber += incorrectFrames / len(decoder.receivedFrames)
            e += ((len(decoder.receivedFrames) - incorrectFrames) / (len(coder.sentFrames[0])*frameamount))
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
    if not generate:
        createGraph(percentArray, berArray, "Procent przekłamania", "Wskaźnik BER")
        createGraph(percentArray, eArray, "Procent przekłamania", "Wskaźnik E")


def main():
    print("-------------------------------- ARQ --------------------------------")
    a = int(input("Wybierz rodzaj zabezpieczenia kontroli poprawności wysłanego pakietu:\n 1 - Brak zabezpieczenia*\n "
                  "2 - Bit parzystości\n 3 - Cykliczny kod nadmiarowy\n 4 - Porównanie kodów\n 5 - Zbiór Pareto\n\tWybór: "))
    if a != 5:
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
    elif a == 3:
        graph_type = int(input("Wybierz typ grafu:\n 1 - zestałym procentem błędu \n 2 - zestałym rozmiarem ramki\n"))
        if graph_type == 1:
            choice = int(input("Podaj który kod CRC chcesz wybrać (0-3): "))
            max_size = int(input("Podaj maxymalny rozmiar ramki\n"))
            enlarging = int(input("Podaj o ile bedziemy zwikszać ramke\n"))
            CRC_BER_const_percent(max_size, percent, frameamount, framecapacity, enlarging, choice)
        if graph_type == 2:
            choice = int(input("Podaj który kod CRC chcesz wybrać (0-3): "))
            max_percent = int(input("Podaj maxymalny procent zakłamania\n"))
            enlarging = int(input("Podaj o ile procent bedziemy zwikszać przekłamanie\n"))
            CRC_BER_const_size(max_percent, percent, frameamount, framecapacity, enlarging, choice)
    elif a == 4:
        graph_type = int(input("Wybierz typ grafu:\n 1 - zestałym procentem błędu \n 2 - zestałym rozmiarem ramki\n"))
        if graph_type == 1:
            # choice = int(input("Podaj który kod CRC chcesz wybrać (0-3): "))
            max_size = int(input("Podaj maxymalny rozmiar ramki\n"))
            enlarging = int(input("Podaj o ile bedziemy zwikszać ramke\n"))
            sizeFrame = []
            eArray = []
            berArray = []
            sizeFrame1 = []
            eArray1 = []
            berArray1 = []
            eArray2 = []
            berArray2 = []
            eArray3 = []
            berArray3 = []
            eArray4 = []
            berArray4 = []
            ber_parity_bits_const_percent2(max_size, percent, frameamount, framecapacity, enlarging, sizeFrame,
                                       eArray, berArray, True)
            CRC_BER_const_percent2(max_size, percent, frameamount, framecapacity, enlarging, 0, sizeFrame1,
                               eArray1, berArray1, True)
            CRC_BER_const_percent2(max_size, percent, frameamount, framecapacity, enlarging, 1, sizeFrame1,
                                   eArray2, berArray2, True)
            CRC_BER_const_percent2(max_size, percent, frameamount, framecapacity, enlarging, 2, sizeFrame1,
                                   eArray3, berArray3, True)
            # CRC_BER_const_percent2(max_size, percent, frameamount, framecapacity, enlarging, 3, sizeFrame1,
            #                        eArray4, berArray4, True)
            # createGraph2(sizeFrame, berArray, "Rozmiar ramki", "Wskaźnik BER", berArray1, berArray2, berArray3, berArray4, "Bit parzystości",
            #              "CRC 8 bit", "CRC 16 bit", "CRC 32 bit", "CRC 64 bit")
            # createGraph2(sizeFrame, eArray, "Rozmiar ramki", "Wskaźnik E", eArray1, eArray2, eArray3, eArray4, "Bit parzystości",
            #              "CRC 8 bit", "CRC 16 bit", "CRC 32 bit", "CRC 64 bit")

            createGraph2(sizeFrame, berArray, "Rozmiar ramki", "Wskaźnik BER", berArray1, berArray2, berArray3, berArray4, "Bit parzystości",
                         "CRC 8 bit", "CRC 16 bit", "CRC 32 bit", "CRC 64 bit")
            createGraph2(sizeFrame, eArray, "Rozmiar ramki", "Wskaźnik E", eArray1, eArray2, eArray3, berArray4, "Bit parzystości",
                         "CRC 8 bit", "CRC 16 bit", "CRC 32 bit", "CRC 64 bit")
        if graph_type == 2:
            # choice = int(input("Podaj który kod CRC chcesz wybrać (0-3): "))
            max_percent = int(input("Podaj maxymalny procent zakłamania\n"))
            enlarging = int(input("Podaj o ile procent bedziemy zwikszać przekłamanie\n"))
            percentArray = []
            eArray = []
            berArray = []
            percentArray1 = []
            eArray1 = []
            berArray1 = []
            eArray2 = []
            berArray2 = []
            eArray3 = []
            berArray3 = []
            eArray4 = []
            berArray4 = []

            ber_parity_bits_const_size2(max_percent, percent, frameamount, framecapacity, enlarging, percentArray,
                                       eArray, berArray, True)
            CRC_BER_const_size2(max_percent, percent, frameamount, framecapacity, enlarging, 0, percentArray1,
                               eArray1, berArray1, True)
            CRC_BER_const_size2(max_percent, percent, frameamount, framecapacity, enlarging, 1, percentArray1,
                                eArray2, berArray2, True)
            CRC_BER_const_size2(max_percent, percent, frameamount, framecapacity, enlarging, 2, percentArray1,
                                eArray3, berArray3, True)
            # CRC_BER_const_size2(max_percent, percent, frameamount, framecapacity, enlarging, 3, percentArray1,
            #                     eArray4, berArray4, True)

            # createGraph2(percentArray, berArray, "Procent przekłamania", "Wskaźnik BER", berArray1, berArray2, berArray3, berArray4,
            #              "Bit parzystości", "CRC 8 bit", "CRC 16 bit", "CRC 32 bit", "CRC 64 bit")
            # createGraph2(percentArray, eArray, "Procent przekłamania", "Wskaźnik E", eArray1, eArray2, eArray3, eArray4, "Bit parzystości",
            #              "CRC 8 bit", "CRC 16 bit", "CRC 32 bit", "CRC 64 bit")

            createGraph2(percentArray, berArray, "Procent przekłamania", "Wskaźnik BER", berArray1, berArray2, berArray3, berArray4,
                         "Bit parzystości", "CRC 8 bit", "CRC 16 bit", "CRC 32 bit", "CRC 64 bit")
            createGraph2(percentArray, eArray, "Procent przekłamania", "Wskaźnik E", eArray1, eArray2, eArray3, eArray4, "Bit parzystości",
                         "CRC 8 bit", "CRC 16 bit", "CRC 32 bit", "CRC 64 bit")
    elif a == 5:
        frameamount = 1
        framecapacity = int(input("Podaj ilośc bitów w ramce: "))
        messagesize = frameamount * framecapacity
        percent = int(input("Podaj procent przekłamania: "))
        ber = 0
        e = 0
        ber1 = 0
        e1 = 0
        ber2 = 0
        e2 = 0
        ber3 = 0
        e3 = 0
        ber4 = 0
        e4 = 0
        ber5 = 0
        e5 = 0
        ber6 = 0
        e6 = 0
        ber7 = 0
        e7 = 0
        ber8 = 0
        e8 = 0
        ber9 = 0
        e9 = 0
        temp = parity_bit_pareto(percent, messagesize, frameamount, framecapacity, ber, e)
        ber = temp[0]
        e = temp[1]
        temp = CRC_pareto(0,  percent, messagesize, frameamount, framecapacity, ber1, e1)
        ber1 = temp[0]
        e1 = temp[1]
        temp = CRC_pareto(1, percent, messagesize, frameamount, framecapacity, ber2, e2)
        ber2 = temp[0]
        e2 = temp[1]
        temp = CRC_pareto(2, percent, messagesize, frameamount, framecapacity, ber3, e3)
        ber3 = temp[0]
        e3 = temp[1]
        temp = CRC_pareto(3, percent, messagesize, frameamount, framecapacity, ber4, e4)
        ber4 = temp[0]
        e4 = temp[1]

        temp = parity_bit_pareto(percent, 24, 1, 24, ber5, e5)
        ber5 = temp[0]
        e5 = temp[1]
        temp = CRC_pareto(0, percent, 24, 1, 24, ber6, e6)
        ber6 = temp[0]
        e6 = temp[1]
        temp = CRC_pareto(1, percent, 24, 1, 24, ber7, e7)
        ber7 = temp[0]
        e7 = temp[1]
        temp = CRC_pareto(2, percent, 24, 1, 24, ber8, e8)
        ber8 = temp[0]
        e8 = temp[1]
        temp = CRC_pareto(3, percent, 24, 1, 24, ber9, e9)
        ber9 = temp[0]
        e9 = temp[1]

        createGraphPareto(ber, e, ber1, e1, ber2, e2, ber3, e3, ber4, e4, ber5, e5, ber6, e6, ber7, e7, ber8, e8, ber9,
                          e9, "Wskaźnik E", "Wskaźnik BER", "Bit parzystości 16 bit",
                         "CRC-8 16 bit", "CRC-16 16 bit", "CRC-32 16 bit", "CRC-64 16 bit",
                          "Bit parzystości 32 bit", "CRC-8 32 bit", "CRC-16 32 bit", "CRC-32 32 bit", "CRC-64 32 bit",
                          "Wykres BER/E dla różnych kodowań\n Procent przekłamania p = " + str(percent) + "\n "
                                                                                "Rozmiar ramki = " + str(framecapacity))
    else:
        print("\nWybrano błędną opcje, program zakończy działanie.")


if __name__ == "__main__":
    main()
