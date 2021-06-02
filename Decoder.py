import binascii
import pycrc.algorithms


class Decoder:
    message = []
    frameLength = 0
    howManyFrames = 0
    ack = 0

    # def __init__(self, msg):
    #     self.message = copy.copy(msg)
    #     self.size = len(msg) - 1

    def getParityBit(self):
        return self.message[self.frameLength]

    def countNumberOfOnes(self):
        counter = 0
        i = 0
        while i < self.frameLength:
            if self.message[i] == 1:
                counter += 1
            i += 1
        counter = counter % 2
        return counter

    def decodeParity(self):
        number_of_ones = self.countNumberOfOnes()
        parity_bit = self.getParityBit()
        if parity_bit == number_of_ones:
            return 0
        else:
            return 1

    # def createFrame(self, message):

    def decodeCRC(self):
        number_of_ones = self.countNumberOfOnes()
        parity_bit = self.getParityBit()
        if parity_bit == number_of_ones:
            return 0
        else:
            return 1

    def getCRS (self, choice,counter,receive, check):
        if (choice == 0):
            crc = pycrc.algorithms.Crc(width=8, poly=0x07,
                                       reflect_in=False, xor_in=0x00,
                                       reflect_out=False, xor_out=0x00)

        if (choice == 1):
            crc = pycrc.algorithms.Crc(width=16, poly=0x8005,
                                       reflect_in=True, xor_in=0x0000,
                                       reflect_out=True, xor_out=0x0000)
        if (choice == 2):
            crc = pycrc.algorithms.Crc(width=32, poly=0x04C11DB7,
                                       reflect_in=True, xor_in=0xFFFFFFFF,
                                       reflect_out=True, xor_out=0xFFFFFFFF)

        z = len(self.sentFrames[counter])-1
        sum = 0
        if(receive == 0):
            for x in self.sentFrames[counter]:
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
        test = str(hexval)
        if (sum <= 15):
            test = test[:2] + "0" + test[2:]
        proszedzialaj = bytes.fromhex(test[2:])
        my_crc = crc.table_driven(proszedzialaj)
        crc_sendFrame = format(my_crc)
        if(check ==1):
            print(test[2:])
            print('{:#08x}'.format(my_crc))
        return crc_sendFrame
