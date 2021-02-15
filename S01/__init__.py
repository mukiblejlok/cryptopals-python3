import string
from collections import Counter
from itertools import combinations
from typing import List, Dict, Sequence, Tuple

ENGLISH_CHAR_FRQ = {
    "A": 0.084966, "B": 0.020720, "C": 0.045388, "D": 0.033844, "E": 0.111607, "F": 0.018121, "G": 0.024705,
    "H": 0.030034, "I": 0.075448, "J": 0.001965, "K": 0.011016, "L": 0.054893, "M": 0.030129, "N": 0.066544,
    "O": 0.071635, "P": 0.031671, "Q": 0.001962, "R": 0.075809, "S": 0.057351, "T": 0.069509, "U": 0.036308,
    "V": 0.010074, "W": 0.012899, "X": 0.002902, "Y": 0.017779, "Z": 0.002722,
}


def xor_bytes(bytes1: bytes, bytes2: bytes) -> bytes:
    result = bytearray()
    for b1, b2 in zip(bytes1, bytes2):
        result.append(b1 ^ b2)
    return bytes(result)


def xor_bytes_with_char(bytes1: bytes, char: str) -> bytes:
    b2 = ord(char)
    result = bytearray()
    for b1 in bytes1:
        result.append(b1 ^ b2)
    return bytes(result)


def evaluate_text(text: str, frq_dict: Dict = None) -> float:
    frq_dict = frq_dict if frq_dict else ENGLISH_CHAR_FRQ

    text_length = len(text)
    # Remove Spaces
    text = text.upper().replace(" ", "")

    text_frq_counter = Counter(text)
    score = 0.0
    for char, frq in text_frq_counter.items():
        expected_frq = frq_dict.get(char, 0.0)
        actual_frq = frq / text_length * 100.0
        score += abs(actual_frq - expected_frq)
    return score / text_length


def repeating_xor(input_bytes, key):
    repeats = len(input_bytes) // len(key) + 1
    repeating_key = bytearray(key) * repeats
    return xor_bytes(input_bytes, repeating_key)


def hamming_distance(bytes1, bytes2) -> int:
    assert len(bytes1) == len(bytes2)
    result = xor_bytes(bytes1, bytes2)
    result_as_int = int(result.hex(), 16)
    no_of_ones = bin(result_as_int).count("1")
    return no_of_ones


def transpose_bytes(input_bytes: bytes, key_length: int) -> List[bytes]:
    list_of_transposed_bytes = []
    for i in range(key_length):
        transposed_bytes = input_bytes[i::key_length]
        list_of_transposed_bytes.append(transposed_bytes)
    return list_of_transposed_bytes


def best_char_for_bytes(input_bytes, chars=string.printable):
    best_score = float("inf")
    code_char = None
    for char in chars:
        output_bytes = xor_bytes_with_char(input_bytes, char)
        try:
            score = evaluate_text(output_bytes.decode())
            if score < best_score:
                best_score = score
                code_char = char
        except UnicodeDecodeError:
            continue
    return code_char, best_score


def get_key_length_normalized_distances(input_bytes: bytes, test_cases: Sequence[int]) -> List[Tuple[int, float]]:
    keys = []
    for key_size in range(2, 42):
        chunks = [input_bytes[i * key_size:(i + 1) * key_size] for i in range(4)]
        # print(chunks)
        distance = 0
        for (c1, c2) in combinations(chunks, 2):
            distance += hamming_distance(c1, c2)
        distance /= (len(chunks) * key_size)
        keys.append((key_size, distance))
    return keys

if __name__ == '__main__':
    texts = (
        "Cooking MC's like a pound of bacon",
        "QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ"
    )
    for _text in texts:
        print(f"{_text} - {evaluate_text(_text):.3f}")

    print(hamming_distance(b"this is a test", b"wokka wokka!!!"))

    print(transpose_bytes(b"abcdefghijklmnoprst", 4))
