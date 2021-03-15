import numpy as np


def main():
    with open("/Users/sangmin/Downloads/wssa", 'rb') as f:
        byte = f.read(16+4+8+5+28+18+80 )
        next_byte = f.read(88)
        #print(byte)
        print(next_byte)
        #print(byte.split())
        print(next_byte.split())
        # Headder 180
        # Headlen 2887
        # curpops 171


if __name__ == "__main__":
    main()


