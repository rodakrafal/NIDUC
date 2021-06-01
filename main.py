# # from Decoder import *
# # from Generator import *
# # from Coder import *
# # from Chanel import *
# # import matplotlib.pyplot as plt
# #
# #
# # def createGraph():
# #     a = input("Wybierz typ grafu:\n 1 - ze stałym rozmiarem ramki \n 2 - ze stałym procentem błędu\n")
# #     if a == 1:
# #         size = 20
# #         arr = []
# #         size_array = []
# #         while size < 10000:
# #             print(size)
# #             size_array.append(size)
# #             counter = 0
# #             count = 0
# #             while counter < 1000:
# #                 message = Generator(size)
# #                 message.generate()
# #                 coder = Coder(message.message)
# #                 coder.coder()
# #                 channel = Chanel(coder.message)
# #                 channel.channel(5)
# #                 decoder = Decoder(channel.message)
# #                 tmp = decoder.decode()
# #                 if tmp == 1:
# #                     count += 1
# #                 counter += 1
# #             arr.append(count)
# #             size += 50
# #         print(arr)
# #         print(size_array)
# #         plt.plot(size_array, arr)
# #         plt.xlabel("Rozmiar tablicy")
# #         plt.ylabel("Liczba znalezionych błędów na 1000 prób")
# #         plt.show()
# #     if a == 2:
# #         percent = 0
# #         arr = []
# #         percent_array = []
# #         while percent < 20:
# #             percent_array.append(percent)
# #             counter = 0
# #             count = 0
# #             while counter < 100:
# #                 message = Generator(80)
# #                 message.generate()
# #                 coder = Coder(message.message)
# #                 coder.coder()
# #                 channel = Chanel(coder.message)
# #                 channel.channel(percent)
# #                 decoder = Decoder(channel.message)
# #                 tmp = decoder.decode()
# #                 if tmp == 1:
# #                     count += 1
# #                 counter += 1
# #             print(percent)
# #             arr.append(count)
# #             percent += 1
# #         print(arr)
# #         print(percent_array)
# #         plt.plot(percent_array, arr)
# #         plt.xlabel("Procent zakłóceń")
# #         plt.ylabel("Liczba znalezionych błędów na 100 prób")
# #         plt.show()
# #
# #
# # def main():
# #     a = int(input("Wybierz typ grafu:\n 1 - zestałym rozmiarem ramki \n 2 - zestałym procentem błędu\n"))
# #     if a == 1:
# #         size = 20
# #         arr = []
# #         size_array = []
# #         while size < 10000:
# #             print(size)
# #             size_array.append(size)
# #             counter = 0
# #             count = 0
# #             while counter < 100:
# #                 message = Generator(size)
# #                 message.generate()
# #                 coder = Coder(message.message)
# #                 coder.coder()
# #                 channel = Chanel(coder.message)
# #                 channel.channel(5)
# #                 decoder = Decoder(channel.message)
# #                 tmp = decoder.decode()
# #                 if tmp == 1:
# #                     count += 1
# #                 counter += 1
# #             arr.append(count)
# #             size += 50
# #         print(arr)
# #         print(size_array)
# #         plt.plot(size_array, arr)
# #         plt.xlabel("Rozmiar tablicy")
# #         plt.ylabel("Liczba znalezionych błędów na 100 prób")
# #         plt.show()
# #     if a == 2:
# #         percent = 0
# #         arr = []
# #         percent_array = []
# #         while percent < 20:
# #             percent_array.append(percent)
# #             counter = 0
# #             count = 0
# #             while counter < 100:
# #                 message = Generator(80)
# #                 message.generate()
# #                 coder = Coder(message.message)
# #                 coder.coder()
# #                 channel = Chanel(coder.message)
# #                 channel.channel(percent)
# #                 decoder = Decoder(channel.message)
# #                 tmp = decoder.decode()
# #                 if tmp == 1:
# #                     count += 1
# #                 counter += 1
# #             print(percent)
# #             arr.append(count)
# #             percent += 1
# #         print(arr)
# #         print(percent_array)
# #         plt.plot(percent_array, arr)
# #         plt.xlabel("Procent zakłóceń")
# #         plt.ylabel("Liczba znalezionych błędów na 100 prób")
# #         plt.show()
# #
# #
# # if __name__ == "__main__":
# #     main()
#
#
# import binascii
# import pycrc.algorithms
#
# # crc = pycrc.algorithms.Crc(width=8, poly=0x07,
# #                            reflect_in=False, xor_in=0x00,
# #                            reflect_out=False, xor_out=0x00)
#
# crc = pycrc.algorithms.Crc(width=16, poly=0x8005,
#                            reflect_in=True, xor_in=0x0000,
#                            reflect_out=True, xor_out=0x0000)
#
# # crc = pycrc.algorithms.Crc(width=32, poly=0x04C11DB7,
# #                            reflect_in=True, xor_in=0xFFFFFFFF,
# #                            reflect_out=True, xor_out=0xFFFFFFFF)
#
#
# data1 = [1,1,1,1,1,1,1,1]
#
# def tobits(s):
#     result = []
#     for c in s:
#         bits = bin(ord(c))[2:]
#         bits = '00000000'[len(bits):] + bits
#         result.extend([int(b) for b in bits])
#     return result
#
#
# z = len(data1)
# t = 0
# sum = 0
#
# for x in data1:
#     t = x*2**(z-1)
#     sum = sum + t
#     z -= 1
#
# hexval = hex(sum)
# print (hexval)
#
# test = str(hexval)
#
# print(test[2:])
# # data = "69"
#
# datax = binascii.a2b_hex(
#     test[2:])  # your data is probably already in binary form, so you won't have to convert it again.
# my_crc = crc.table_driven(datax)  # calculate the CRC, using the bit-by-bit-fast algorithm.
# print('{:#09x}'.format(my_crc))
# temp1 = tobits(format(my_crc))
# print(temp1)


from Model import Model


def run():
    model = Model()
    model.fillMessage()                                                                                                 # tworzenie msg
    model.createFrames()                                                                                                # dzielenie msg na ramki + bit parzystosci
    model.fillBadFrames()
    # model.printFrames(model.sentFrames)
    model.stopAndWait()
    # model.stopAndWaitCRC(1)
    # model.selectiveRepeat()

if __name__ == '__main__':
    run()