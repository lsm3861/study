import numpy as np

def main():
    with open("/Users/sangmin/Downloads/wssa", 'rb') as f:
        byte = f.read(16+4+8+5+28+18+80)
        next_byte = f.read(100)
        print(byte)
        print(next_byte)
        print(byte.split())
        print(next_byte.split())


if __name__ == "__main__":
    main()


