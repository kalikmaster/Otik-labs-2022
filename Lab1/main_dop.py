import os
from turtle import bgcolor


def encode(path, filename):
    signature = bytes.fromhex('0000000000564449')
    version = bytes.fromhex('0000')
    alg = bytes.fromhex('000000000000')
    with open(filename, 'wb') as f:
        f.write(signature)
        f.write(version)
        f.write(alg)
        print("Все найденные файлы:")
        for subpath, subdirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(subpath, file)
                print(file_path)
                name_size = len(file_path.encode('utf-8')) 
                size = os.stat(file_path).st_size                   
                f.write(name_size.to_bytes(1, byteorder='big'))
                # if byteorder is "big", the most significant byte is at the beginning of the byte array
                f.write(file_path.encode('utf-8')) #путь до файла
                f.write(size.to_bytes(8, byteorder='big'))
                with open(file_path, 'rb') as f2:
                    f.write(f2.read())
    print('\nУспешно создан архив!')


def decode(file):
    with open(file, 'rb') as f:
        signature = f.read(8)
        if signature != bytes.fromhex('0000000000564449'):  # check for correct signature
            print("Ошибка в сигнатуре файла")
            return
        version = f.read(2)
        if version != bytes.fromhex('0000'):  # check for latest version
            return
        alg = f.read(6)
        # do something with algorithms
        while(1):
            name_size = int.from_bytes(f.read(1), byteorder='big')
            filename = f.read(name_size).decode('utf-8') 
            if filename == "":
                break
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            file_size = int.from_bytes(f.read(8), byteorder='big')
            with open(filename, 'wb') as f2:
                f2.write(f.read(file_size))
    print('\nФайл успешно декодирован!')

def read_file_name(arg):
    name = input("Введите имя файла с расширением:\n")
    name.split(".")[0]
    if arg == 1:
        names = (name, name.split(".")[0]+".vdi")
    
    return names


if __name__ == '__main__':
    while(1):
        print("-"*70 + "\n\
Что вы хотите сделать?\n \
1. Закодировать\n \
2. Декодировать\n \
0. Выход\n")
        choice = input()
        if choice == '1':
            name = input("Введите имя папки:\n")
            encode(name, name+".vdi")            
        elif choice == '2':
            name = input("Введите имя файла с расширением:\n")
            decode(name)            
        elif choice == '0':
            break
        else:
            print("Введите номер команды!")