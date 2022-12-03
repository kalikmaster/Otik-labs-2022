import os
import io
import logging
from huffman import encode_huffman
from huffman import decode_huffman

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

signature = bytes.fromhex('0000000000564449')
version = bytes.fromhex('0001')


def encode_file(file, output_buffer, params: dict) -> None:
    if params['alg_type'] == '0000':
        logging.debug('encoding alg 0000')
        output_buffer.write(file.read())
        return
    if params['alg_type'] == '0001':
        logging.debug("encoding alg 0001")
        encode_huffman(file, output_buffer)
        return
    logging.error('Параметр alg_type не распознан, файл не закодирован')


def encode(path: str, output_buffer, params: dict) -> None:
    if params['alg_types'] != '00' and params['alg_types'] != '01' and params['alg_types'] != '02':
        return
    all_files_buffer = io.BytesIO()
    output_buffer.write(signature)
    output_buffer.write(version)
    output_buffer.write(bytes.fromhex(params['alg_types']))
    print("Все найденные файлы:")
    for subpath, subdirs, files in os.walk(path):
        for filename in files:
            file_path = os.path.join(subpath, filename)
            print(file_path)
            name_size = len(file_path.encode('utf-8'))
            size = os.stat(file_path).st_size
            file = open(file_path, 'rb')
            if params['alg_types'] == '00' or params['alg_types'] == '01':
                output_buffer.write(name_size.to_bytes(1, byteorder='big'))
                output_buffer.write(file_path.encode('utf-8'))
                output_buffer.write(size.to_bytes(8, byteorder='big'))
                if params['smart'] and params['alg_types'] == '01':
                    temp_buffer1 = io.BytesIO()
                    temp_buffer2 = io.BytesIO()
                    temp_buffer1.write(bytes.fromhex('0000'))
                    temp_buffer2.write(bytes.fromhex('0001'))
                    encode_file(file, temp_buffer1, {'alg_type': '0000'})
                    file.seek(0)
                    encode_file(file, temp_buffer2, {'alg_type': '0001'})
                    if temp_buffer1.getbuffer().nbytes <= temp_buffer2.getbuffer().nbytes:
                        temp_buffer1.seek(0)
                        output_buffer.write(temp_buffer1.read())
                    else:
                        temp_buffer2.seek(0)
                        output_buffer.write(temp_buffer2.read())
                else:
                    if params['alg_types'] == '01':
                        output_buffer.write(bytes.fromhex(params['alg_type']))
                    encode_file(file, output_buffer, params)
            if params['alg_types'] == '02':
                all_files_buffer.write(name_size.to_bytes(1, byteorder='big'))
                all_files_buffer.write(file_path.encode('utf-8'))
                all_files_buffer.write(size.to_bytes(8, byteorder='big'))
                all_files_buffer.write(file.read())
            file.close()
    if params['alg_types'] == '00' or params['alg_types'] == '01':
        print('\nФайл успешно закодирован!')
        return
    if params['alg_types'] == '02':
        all_files_buffer.seek(0)
        output_buffer.write(all_files_buffer.getbuffer().nbytes.to_bytes(8, byteorder="big"))
        output_buffer.write(bytes.fromhex(params['alg_type']))
        encode_file(all_files_buffer, output_buffer, params)
        print('\nФайл успешно закодирован!')
        return


def decode(file):
    signature_value = file.read(8)
    if signature != signature_value:  # check for correct signature
        print("Ошибка в сигнатуре файла")
        return
    version_value = file.read(2)
    if version != version_value:  # check for latest version
        print("Ошибка. Несовместимая версия")
        return
    alg_types = file.read(1)
    if alg_types == bytes.fromhex('00') or alg_types == bytes.fromhex('01'):
        while True:
            name_size = int.from_bytes(file.read(1), byteorder='big')
            filename = file.read(name_size).decode('utf-8')
            if filename == "":
                break
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            file_size = int.from_bytes(file.read(8), byteorder='big')
            with open(filename, 'wb') as file2:
                if alg_types == bytes.fromhex('00'):
                    file2.write(file.read(file_size))
                if alg_types == bytes.fromhex('01'):
                    alg_type = file.read(2)
                    if alg_type == bytes.fromhex('0000'):
                        file2.write(file.read(file_size))
                    if alg_type == bytes.fromhex('0001'):
                        decode_huffman(file, file2)
        print('\nФайл успешно декодирован!')
    if alg_types == bytes.fromhex('02'):
        file_size = int.from_bytes(file.read(8), byteorder='big')
        alg_type = file.read(2)
        buf = io.BytesIO()
        if alg_type == bytes.fromhex('0000'):
            buf.write(file.read())
        if alg_type == bytes.fromhex('0001'):
            decode_huffman(file, buf)
        buf.seek(0)
        while True:
            name_size = int.from_bytes(buf.read(1), byteorder='big')
            filename = buf.read(name_size).decode('utf-8')
            if filename == "":
                break
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            file_size = int.from_bytes(buf.read(8), byteorder='big')
            with open(filename, 'wb') as file2:
                file2.write(buf.read(file_size))


if __name__ == '__main__':
    params = {'alg_types': '01', 'alg_type': '0001', 'smart': True}
    #with open('new_file.txt', 'wb') as file:
    #    encode('test', file, params)
    with open('new_file.txt', 'rb') as file:
        decode(file)
