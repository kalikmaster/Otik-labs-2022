import math

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
            table.append([chr(i), count[i], count[i] / sum, -math.log(count[i] / sum, 2)])
    I = 0
    for i in range(len(table)):
        I += table[i][1] * table[i][3]
    print('Amount of information: ' + str(I))
    print("-------------------------------------------------")
    print("Характеристика символов с сортировкой по алфавиту")
    print("-------------------------------------------------")
    print('Символ\u2193\tКол-во\tВероятность\tКол-во информации')
    for i in table:
        print("%s\t%d\t%.2f\t\t%.2f" % (repr(i[0]), i[1], i[2], i[3]))
    print("-------------------------------------------------\n")
    table.sort(key=lambda x: x[1], reverse=True)
    print("---------------------------------------------------")
    print("Характеристика символов с сортировкой по количеству")
    print("---------------------------------------------------")
    print('Символ\tКол-во\u2193\tВероятность\tКол-во информации')
    for i in table:
        print("%s\t%d\t%.2f\t\t%.2f" % (repr(i[0]), i[1], i[2], i[3]))


if __name__ == '__main__':
    task1('task1.txt')
