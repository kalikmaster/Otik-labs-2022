import os
import io
import logging
from huffman import encode_huffman

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
        output_buffer.write(bytes.fromhex(params['alg_type']))
        encode_file(all_files_buffer, output_buffer, params)
        print('\nФайл успешно закодирован!')
        return


if __name__ == '__main__':
    params = {'alg_types': '02', 'alg_type': '0001'}
    with open('new_file.txt', 'wb') as f:
        encode('test', f, params)
