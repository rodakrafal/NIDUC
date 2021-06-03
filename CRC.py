import pycrc.algorithms
import copy


class CRC:
    message = []
    bitsamount = 1

    def __init__(self, message):
        self.message = copy.deepcopy(message)

    def getCRS(self, choice):
        if choice == 0:
            crc = pycrc.algorithms.Crc(width=8, poly=0x07,
                                       reflect_in=False, xor_in=0x00,
                                       reflect_out=False, xor_out=0x00)
            self.bitsamount = 8
        if choice == 1:
            self.bitsamount = 16
            crc = pycrc.algorithms.Crc(width=16, poly=0x8005,
                                       reflect_in=True, xor_in=0x0000,
                                       reflect_out=True, xor_out=0x0000)
        if choice == 2:
            crc = pycrc.algorithms.Crc(width=32, poly=0x04C11DB7,
                                       reflect_in=True, xor_in=0xFFFFFFFF,
                                       reflect_out=True, xor_out=0xFFFFFFFF)
            self.bitsamount = 32

        if choice == 2:
            self.bitsamount = 64
            crc = pycrc.algorithms.Crc(width=64, poly=0x000000000000001b,
                                       reflect_in=True, xor_in=0x0000000000000000,
                                       reflect_out=True, xor_out=0x0000000000000000)

        z = len(self.message)
        sum = 0
        for x in self.message:
            t = x * 2 ** (z - 1)
            sum = sum + t
            z -= 1
        hexval = hex(sum)
        strval = str(hexval)
        if len(strval)%2!=0:
            strval = strval[:2] + "0" + strval[2:]
        convertedval = bytes.fromhex(strval[2:])
        my_crc = crc.table_driven(convertedval)
        crc_sendFrame = format(my_crc)
        return crc_sendFrame

    def getCRCbites(self):
        return self.bitsamount
