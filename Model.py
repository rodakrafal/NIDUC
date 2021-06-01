import random
import time
import binascii
import pycrc.algorithms

class Model:
    message = []                                                                                                        # ciag ktory bedziemy przesylac
    bits = 160                                                                                                          # ile bitow w wiadomosci
    sentFrames = []                                                                                                     # lista ramek ktora wysylamy
    receivedFrames = []                                                                                                 # odbierana lista ramek
    badFrames = []                                                                                                      # nry zlych ramek
    howManyFrames = 20                                                                                                 # ilosc utworzonych ramek
    frameLength = 8                                                                                                     # dlugosc 1 ramki
    prob = 80                                                                                                           # prawdopodobienstwo zepsucia
    incorrectlySent = 0                                                                                                 # stat: niepoprawne (suma)
    correctlySent = 0                                                                                                   # stat: poprawne (suma)

    def fillBadFrames(self):
        self.badFrames = list(range(self.howManyFrames))

    def fillMessage(self):
        for i in range(self.bits):
            self.message.append(random.randint(0, 1))                                                                   # uzupelnia message 0 lub 1

    def printFrames(self, frame):                                                                                       # wypisuje ciag bitow
        for i in range(self.howManyFrames):
            print(frame[i], end="")
            print('\n')

    def parityBit(self, frame):                                                                                         # wyznaczanie bitu parzystosci
        sum = 0
        for j in range(self.frameLength):
            sum += frame[j]
        return (sum % 2)

    def createFrames(self):                                                                                             # dzielenie na ramki
        for i in range(self.howManyFrames):
            self.sentFrames.append([])
            for j in range(self.frameLength):
                self.sentFrames[i].append(self.message[i * self.frameLength + j])
            self.sentFrames[i].append(self.parityBit(self.sentFrames[i]))


    def getCRS (self, choice,counter,receive, check):

        if (choice == 0):
            # print("wybrałes 0")
            crc = pycrc.algorithms.Crc(width=8, poly=0x07,
                                       reflect_in=False, xor_in=0x00,
                                       reflect_out=False, xor_out=0x00)

        if (choice == 1):
            # print("wybrałes 1")
            crc = pycrc.algorithms.Crc(width=16, poly=0x8005,
                                       reflect_in=True, xor_in=0x0000,
                                       reflect_out=True, xor_out=0x0000)
        if (choice == 2):
            # print("wybrałes 2")
            crc = pycrc.algorithms.Crc(width=32, poly=0x04C11DB7,
                                       reflect_in=True, xor_in=0xFFFFFFFF,
                                       reflect_out=True, xor_out=0xFFFFFFFF)

        z = len(self.sentFrames[counter])-1
        sum = 0
        # print(z)
        if(receive == 0):
            for x in self.sentFrames[counter]:
                # print(x)
                if (z == 0):
                    break
                t = x * 2 ** (z - 1)
                sum = sum + t
                z -= 1
        if(receive==1):
            for x in self.receivedFrames[counter]:
                # print(x)
                if (z == 0):
                    break
                t = x * 2 ** (z - 1)
                sum = sum + t
                z -= 1
        hexval = hex(sum)
        # print(hexval)
        test = str(hexval)
        # print(test[2:])
        if (sum <= 15):
            test = test[:2] + "0" + test[2:]
            # print("WYKONALEM SIE?")
        proszedzialaj = bytes.fromhex(test[2:])
        # print(proszedzialaj)
        # Obliczony kod crc dla podanego odebranego ciagu
        my_crc = crc.table_driven(proszedzialaj)

        crc_sendFrame = format(my_crc)
        if(check ==1):
            print(test[2:])
            print('{:#08x}'.format(my_crc))
        return crc_sendFrame


    def stopAndWait(self):                                                                                              # tworzenie bledow i wpisywanie
        print(self.message)
        counter = 0                                                                                                     # ich do receivedFrames
        while counter < self.howManyFrames:
            self.receivedFrames.append([])                                                                              # prawdopodobienstwo do ktorego bd porownywac
            for i in range(self.frameLength):
                a = random.randint(0,100)
                if a < self.prob:                                                                                       # jesli a mniejsze
                    self.receivedFrames[counter].append(self.sentFrames[counter][i])                                    # wpisz co jest
                else:                                                                                                   # jak nie
                    if self.sentFrames[counter][i] == 1:                                                                # to podmien
                        self.receivedFrames[counter].append(0)
                    else:
                        self.receivedFrames[counter].append(1)

            pb = self.parityBit(self.receivedFrames[counter])  # jaki wyjdzie bit parzystosci
            self.receivedFrames[counter].append(pb)
            pSend = 0
            for i in self.sentFrames[counter]:
                if(i == self.frameLength - 1):
                    pSend = i
            # print(pSend)
            if pb == pSend:                                                    # jesli jest k
                counter += 1
                # self.correctlySent += 1
            if pb != pSend:                                                                                                 # jesli !k
                self.receivedFrames.remove(self.receivedFrames[counter])
                # self.incorrectlySent += 1

        print(self.sentFrames)
        print(self.receivedFrames)



    def stopAndWaitCRC(self, choice):
        counter = 0                                                                                                     # ich do receivedFrames
        while counter < self.howManyFrames:
            self.receivedFrames.append([])                                                                              # prawdopodobienstwo do ktorego bd porownywac
            for i in range(self.frameLength + 1):
                a = random.randint(0,100)
                if a < self.prob:                                                                                       # jesli a mniejsze
                    self.receivedFrames[counter].append(self.sentFrames[counter][i])                                    # wpisz co jest
                else:                                                                                                   # jak nie
                    if self.sentFrames[counter][i] == 1:                                                                # to podmien
                        self.receivedFrames[counter].append(0)
                    else:
                        self.receivedFrames[counter].append(1)

            crs_Send = self.getCRS(choice,counter,0,0)
            crs_Received = self.getCRS(choice,counter,1,0)
            print(crs_Send)
            print(crs_Received)
            print("Nowa iteracja")
            if crs_Send == crs_Received:
                print(crs_Send)
                print(crs_Received)
                print(self.getCRS(choice,counter,0,1))
                print(self.getCRS(choice,counter,1,1))
                print("Teoretycznie sie udało")
                counter += 1
                self.correctlySent += 1
            else:                                                                                                       # jesli !k
                self.receivedFrames.remove(self.receivedFrames[counter])
                self.incorrectlySent += 1

        print(self.sentFrames[1:][1:])
        print(self.receivedFrames)


    def selectiveRepeat(self):
        for counter in range(len(self.sentFrames)):
            if self.badFrames.__contains__(counter):                                                                    # jesli w liscie badFrames jest numer ramki to wysylamy
                self.receivedFrames.append([])
                for i in range(self.frameLength + 1):
                    a = random.randint(0, 100)
                    if a < self.prob:
                        self.receivedFrames[counter].append(self.sentFrames[counter][i])
                    else:
                        if self.sentFrames[counter][i] == 1:
                            self.receivedFrames[counter].append(0)
                        else:
                            self.receivedFrames[counter].append(1)
                pb = self.parityBit(self.receivedFrames[counter])
                if pb == self.receivedFrames[counter][self.frameLength]:
                    self.correctlySent += 1
                    self.badFrames.remove(counter)
                    time.sleep(1)
                    print("The parity bit for ", counter, " frame is correct! removed")
                else:
                    self.receivedFrames[counter] = []                                                                   # jak zle wyslana to czyszczenie ramki sposobem NASA
                    self.incorrectlySent += 1
                    time.sleep(1)
                    print("The parity bit is incorrect, ", counter, " frame not removed.")
        if len(self.badFrames) != 0:
            print("Created retransmit list: ", self.badFrames)
            print("Retransmition ", self.correctlySent, "/", self.incorrectlySent)
            self.selectiveRepeat()
        else:
            print("Sending completed! Result: ", self.correctlySent, " correctly sent frames, ", self.incorrectlySent,
                  " incorrectly sent frames.\n")