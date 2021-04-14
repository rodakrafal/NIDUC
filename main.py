from Decoder import *
from Generator import *
from Coder import  *
from Chanel import *


def main():
    print("Hello")
    message = Generator(6)
    message.generate()
    print(message.message)
    coder = Coder(message.message)
    coder.coder()
    print(coder.message)
    channel = Chanel(coder.message)
    channel.channel(50)
    print(channel.message)
    decoder = Decoder(channel.message)
    print(decoder.decode())



if __name__ == "__main__":
    main()
