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
    print('Sorted by alphabet:')
    for i in table:
        print(i)
    table.sort(key = lambda x: x[1], reverse=True)
    print('Sorted by quantity:')
    for i in table:
        print(i)


if __name__ == '__main__':
    task1('task1.txt')
