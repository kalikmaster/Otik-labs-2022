import math
from tabulate import tabulate

def task1(filename):
    count = [0] * 256
    with open(filename, 'rb') as f:
        byte = f.read(1)
        while byte != b'':
            count[int.from_bytes(byte, byteorder="big")] += 1
            byte = f.read(1)
    sum = 0
    for i in range(256):
        sum += count[i]
    print('Number of elements: ' + str(sum))
    table = []
    for i in range(256):
        if count[i] != 0:
            table.append([repr(chr(i)), count[i], count[i] / sum, -math.log(count[i] / sum, 2)])
    I = 0
    for i in range(len(table)):
        I += table[i][1] * table[i][3]
    print('Amount of information: ' + str(I))
    print("-------------------------------------------------------")
    print("Характеристика символов с сортировкой по алфавиту")
    print("-------------------------------------------------------")
    print(tabulate(table, headers=['Символ\u2193', 'Кол-во', 'Вероятность', 'Кол-во информации']))
    print("-------------------------------------------------------\n")
    table.sort(key=lambda x: x[1], reverse=True)
    print("-------------------------------------------------------")
    print("Характеристика символов с сортировкой по количеству")
    print("-------------------------------------------------------")
    print(tabulate(table, headers=['Символ', 'Кол-во\u2193', 'Вероятность', 'Кол-во информации']))


if __name__ == '__main__':
    task1('task1.txt')
