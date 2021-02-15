import base64
from collections import Counter
from typing import List

english_character_frequency = {
    "E": 11.1607,
    "M": 3.0129,
    "A": 8.4966,
    "H": 3.0034,
    "R": 7.5809,
    "G": 2.4705,
    "I": 7.5448,
    "B": 2.0720,
    "O": 7.1635,
    "F": 1.8121,
    "T": 6.9509,
    "Y": 1.7779,
    "N": 6.6544,
    "W": 1.2899,
    "S": 5.7351,
    "K": 1.1016,
    "L": 5.4893,
    "V": 1.0074,
    "C": 4.5388,
    "X": 0.2902,
    "U": 3.6308,
    "Z": 0.2722,
    "D": 3.3844,
    "J": 0.1965,
    "P": 3.1671,
    "Q": 0.1962,
}


def hex2base64(hex_str: str) -> bytes:
    # hex string -> bytes
    b = bytearray.fromhex(hex_str)
    # bytes to b64
    b64 = base64.b64encode(b)
    return b64


def xor_bytes(bytes1: bytes, bytes2: bytes) -> bytes:
    result = bytearray()
    for b1, b2 in zip(bytes1, bytes2):
        result.append(b1 ^ b2)
    return bytes(result)


def xor_bytes_with_char(bytes1: bytes, char: str) -> bytes:
    result = bytearray()
    b2 = ord(char)
    for b1 in bytes1:
        result.append(b1 ^ b2)
    return bytes(result)


def evaluate_text(text: str) -> float:
    text_length = len(text)
    text = text.upper().replace(" ", "")
    frq_counter = Counter(text)

    score = 0.0
    for char, frq in frq_counter.items():
        expected_frq = english_character_frequency.get(char, 0.0)
        actual_frq = frq / text_length * 100.0
        score += abs(actual_frq - expected_frq)
    return score / text_length


def repeating_xor(input_bytes, key):
    repeats = len(input_bytes) // len(key) + 1
    repeating_key = bytearray(key) * repeats
    result = bytearray()
    for b1, b2 in zip(input_bytes, repeating_key):
        result.append(b1 ^ b2)
    return result


def hamming_distance(bytes1, bytes2) -> int:
    assert len(bytes1) == len(bytes2)
    result = bytearray()
    for b1, b2 in zip(bytes1, bytes2):
        result.append(b1 ^ b2)

    result_as_int = int(result.hex(), 16)
    no_of_ones = bin(result_as_int).count("1")
    return no_of_ones


def transpose_bytes(input_bytes: str, key_length: int) -> List[bytes]:
    transposed_bytes = []
    for i in range(key_length):
        transposed_bytes.append(input_bytes[i::key_length])
    return transposed_bytes


if __name__ == '__main__':
    texts = (
        "Cooking MC's like a pound of bacon",
        "QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ"
    )
    for text in texts:
        print(text, evaluate_text(text))

    print(hamming_distance(b"this is a test", b"wokka wokka!!!"))

    print(transpose_bytes(b"abcdefghijklmnoprst", 3))

