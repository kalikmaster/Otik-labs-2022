from collections import defaultdict
from math import log2


def read_unicode_file():
    file_name = input("Введите имя файла: ")
    try:
        with open(file_name, "r") as f:
            file_data = f.read()
            file_len = len(file_data)
            print("-------------------------------------------------")
            print("Длина файла:", file_len)
            file_symbols = defaultdict(int)
            for symbol in file_data: #получаем количество вхождений
                file_symbols[symbol] += 1
            information_quantity = 0
            #создаётся словарь, где ключ - символ, а значение - список.
            #dict[<символ>] = [<кол-во символов>, <вероятность>, <кол-во информации>]
            for key, value in file_symbols.items(): 
                temp = value / file_len #вероятность каждого символа
                file_symbols[key] = [value, temp, -log2(temp)]
                information_quantity += value * file_symbols[key][2]
            print("Общее кол-во информации: %.2f" % information_quantity)
            print("-------------------------------------------------")
            print("Характеристика символов с сортировкой по алфавиту")
            print("-------------------------------------------------")
            print('Символ\u2193 Кол-во Вероятность Кол-во информации')
            for key, value in dict(sorted(file_symbols.items())).items():
                print("%7s %6d %11.2f %17.2f" % (repr(key), value[0], value[1], value[2])) 
            print("-------------------------------------------------\n")
            print("---------------------------------------------------")
            print("Характеристика символов с сортировкой по количеству")
            print("---------------------------------------------------")
            print('Символ Кол-во\u2193 Вероятность Кол-во информации')
            for key, value in dict(sorted(file_symbols.items(), key= lambda item: item[1][0], reverse=True)).items():
                print("%6s %7d %11.2f %17.2f" % (repr(key), value[0], value[1], value[2]))
            print("---------------------------------------------------")
    except UnicodeDecodeError:
        print("Невозможно считать файл в данном формате!")


def main():
    read_unicode_file()

if __name__ == "__main__":
    main()