import io
import math
from bitstring import BitArray


class Node:

    def __init__(self, data=None, freq=None, left=None, right=None):
        self.data = data
        self.freq = freq
        self.left = left
        self.right = right

    def is_leaf(self):
        return self.left is None and self.right is None


def find_min(first: list, second: list):
    if not second:
        return first.pop(0)
    if not first:
        return second.pop(0)
    if first[0].freq < second[0].freq:
        return first.pop(0)
    return second.pop(0)


def build_huffman_tree(symbols: list[list]) -> Node:
    first = []
    second = []
    for symbol in symbols:
        first.append(Node(symbol[0], symbol[1]))
    while not (first == [] and len(second) == 1):
        left = find_min(first, second)
        right = find_min(first, second)
        second.append(Node("", left.freq + right.freq, left, right))
    return second.pop()


def get_huffman_codes(root: Node, code: str, symbols: list[list]) -> None:
    if root.left:
        code += '0'
        get_huffman_codes(root.left, code, symbols)
        code = code[:-1]
    if root.right:
        code += '1'
        get_huffman_codes(root.right, code, symbols)
        code = code[:-1]
    if root.is_leaf():
        for symbol in symbols:
            if symbol[0] == root.data:
                symbol.append(code)
        # print('Symbol: {}, code: {}'.format(chr(root.data), code))


def encode_huffman(input_buffer, output_buffer) -> None:
    symbols = []
    for i in range(256):
        symbols.append([i, 0])
    byte = input_buffer.read(1)
    while byte != b"":
        symbols[int.from_bytes(byte, byteorder="big")][1] += 1
        byte = input_buffer.read(1)
    present_symbols = []
    for symbol in symbols:
        if symbol[1] != 0:
            present_symbols.append([symbol[0], symbol[1]])
    present_symbols = sorted(present_symbols, key=lambda x: x[1])
    tree = build_huffman_tree(present_symbols)
    get_huffman_codes(tree, "", present_symbols)
    compressed_size = 0
    for symbol in present_symbols:
        compressed_size += symbol[1] * len(symbol[2])
    output_buffer.write(compressed_size.to_bytes(9, byteorder='big'))
    output_buffer.write(len(present_symbols).to_bytes(1, byteorder='big'))
    for symbol in present_symbols:
        output_buffer.write(symbol[0].to_bytes(1, byteorder="big"))
        output_buffer.write(len(symbol[2]).to_bytes(1, byteorder="big"))
    codes = ""
    for symbol in present_symbols:
        codes += symbol[2]
    b1 = BitArray(bin=codes)
    b1.tofile(output_buffer)
    symbols_dict = {}
    for symbol in present_symbols:
        symbols_dict[symbol[0]] = symbol[2]
    input_buffer.seek(0)
    byte = input_buffer.read(1)
    compressed_content = ""
    while byte != b"":
        # print(int.from_bytes(byte, byteorder="big"))
        compressed_content += symbols_dict[int.from_bytes(byte, byteorder="big")]
        byte = input_buffer.read(1)
    b2 = BitArray(bin=compressed_content)
    b2.tofile(output_buffer)
    return output_buffer


def decode_huffman(input_buffer, output_buffer) -> None:
    compressed_size = int.from_bytes(input_buffer.read(9), byteorder="big")
    table_size = int.from_bytes(input_buffer.read(1), byteorder="big")
    symbols = []
    codes_length = 0
    for i in range(table_size):
        byte = input_buffer.read(1)
        code_length = int.from_bytes(input_buffer.read(1), byteorder="big")
        codes_length += code_length
        symbols.append([byte, code_length])
    codes = input_buffer.read(math.ceil(codes_length / 8))
    bytes_dict = {}
    byte_number = 0
    bit_number = 0
    for symbol in symbols:
        code = ""
        for j in range(symbol[1]):
            bit = (codes[byte_number] >> (8 - bit_number - 1)) & 1
            code += str(bit)
            bit_number += 1
            byte_number += bit_number // 8
            bit_number %= 8
        bytes_dict[code] = symbol[0]
    content = input_buffer.read(math.ceil(compressed_size / 8))
    byte_number = 0
    bit_number = 0
    code = ""
    while byte_number * 8 + bit_number < compressed_size:
        code += str((content[byte_number] >> (8 - bit_number - 1)) & 1)
        if code in bytes_dict:
            output_buffer.write(bytes_dict[code])
            code = ""
        bit_number += 1
        byte_number += bit_number // 8
        bit_number %= 8


if __name__ == '__main__':
    with open('new_file.txt', 'rb') as file:
        file.read(13)
        file2 = open('new_file2.txt', 'wb')
        decode_huffman(file, file2)
        file2.close()
