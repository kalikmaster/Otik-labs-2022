import math
import os


def task3():
    count = [0] * 256
    for filename in os.listdir("../different_encodings/"):
        with open(os.path.join("../different_encodings/", filename), 'rb') as f:
            byte = f.read(1)
            while byte != b'':
                count[int.from_bytes(byte, byteorder="big")] += 1
                byte = f.read(1)
    sum = 0
    for i in range(256):
        sum += count[i]
    table = []
    table_without_ascii = []
    for i in range(256):
        if count[i] != 0:
            table.append([i, count[i], count[i] / sum, -math.log(count[i] / sum, 2)])
            if i > 127:
                table_without_ascii.append([i, count[i], count[i] / sum, -math.log(count[i] / sum, 2)])
    table.sort(key=lambda x: x[1], reverse=True)
    print("-------------------------------------------------------")
    print("Наиболее частые октеты")
    print("-------------------------------------------------------")
    print("Октет Кол-во\u2193 Вероятность Кол-во информации")
    for symbol in table[0:4]:
        print("%5x %7d %11.2f %17.2f" % tuple(symbol))
    print("-------------------------------------------------------\n")
    table_without_ascii.sort(key=lambda x: x[1], reverse=True)
    print("-------------------------------------------------------")
    print("Наиболее частые октеты без ASCII")
    print("-------------------------------------------------------")
    print("Октет Кол-во\u2193 Вероятность Кол-во информации")
    for symbol in table_without_ascii[0:4]:
        print("%5x %7d %11.2f %17.2f" % tuple(symbol))
    print("-------------------------------------------------------\n")
  

def encoding_specifier(filename):
    count = [0] * 256
    encodings = ["windows-1251", "KOI8-R", "IBM866", "ISO-8859-5"]
    for encoding in encodings:
        with open(filename, 'rb') as f:
            byte = f.read(1)
            while byte != b'':
                count[int.from_bytes(byte, byteorder="big")] += 1
                byte = f.read(1)
        table = []
        for i in range(256):
            if count[i] != 0:
                table.append([(i.to_bytes((i.bit_length() + 7) // 8, 'big'))\
                    .decode(encoding=encoding), count[i]])
        table.sort(key=lambda x: x[1], reverse=True)
        print("-------------------------------------------------------")
        print(encoding)
        print("-------------------------------------------------------")
        print("Символ Кол-во\u2193")
        for symbol in table:
            print("%6r %7d" % tuple(symbol))
        print("-------------------------------------------------------\n")
    

def main():
    #task3()
    encoding_specifier("4.txt")


if __name__ == "__main__":
    main()