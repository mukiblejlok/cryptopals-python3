import base64
import string
from itertools import combinations

from tools import hex2base64, xor_bytes, xor_bytes_with_char, evaluate_text, repeating_xor, hamming_distance, \
    transpose_bytes


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
        except:
            continue
    return code_char, best_score


if __name__ == '__main__':

    # Challenge 1
    hex_input_string = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    output_bytes = hex2base64(hex_input_string)
    assert output_bytes.decode() == "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
    print("Challenge 1 - OK")

    # Challenge 2
    hex_input_string1 = "1c0111001f010100061a024b53535009181c"
    hex_input_string2 = "686974207468652062756c6c277320657965"
    input_bytes1 = bytearray.fromhex(hex_input_string1)
    input_bytes2 = bytearray.fromhex(hex_input_string2)
    output_bytes = xor_bytes(input_bytes1, input_bytes2)
    assert output_bytes.hex() == "746865206b696420646f6e277420706c6179"
    print("Challenge 2 - OK")

    # Challenge 3
    hex_input_string = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    input_bytes = bytearray.fromhex(hex_input_string)
    best_char, score = best_char_for_bytes(input_bytes=input_bytes)
    output_bytes = xor_bytes_with_char(input_bytes, best_char)
    print(f"Challenge 3 - {output_bytes} | (Char: {best_char}, Score: {score:3f})")

    # Challenge 4
    with open(r"files\s1c4.txt") as f:
        lines_to_test = f.readlines()
    best_score = float("inf")
    best_char = None
    best_line = None
    for i, line in enumerate(lines_to_test):
        input_bytes = bytearray.fromhex(line)
        char, score = best_char_for_bytes(input_bytes)
        if score < best_score:
            best_char = char
            best_score = score
            best_line = i
    print(f"Challenge 4 - {output_bytes} | (Line: {best_line}, Char: {best_char}, Score: {best_score:3f})")

    # Challenge 5
    input_bytes1 = b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    key = b"ICE"
    output_bytes1 = repeating_xor(input_bytes1, key)
    assert output_bytes1.hex() == "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"

    # Challenge 6
    # Get bytes from file
    with open("files\s1c6.txt", "rb") as f:
        input_bytes = base64.b64decode(f.read())
        # input_bytes = f.read()
    # Estimate best key size
    keys = []
    for key_size in range(2, 42):
        chunks = [input_bytes[i * key_size:(i + 1) * key_size] for i in range(4)]
        # print(chunks)
        distance = 0
        for (c1, c2) in combinations(chunks, 2):
            distance += hamming_distance(c1, c2)
        distance /= (6 * key_size)
        keys.append((key_size, distance))

    top_keys = sorted(keys, key=lambda x: x[1])[:10]
    # Find the best matching key
    best_score = float("inf")
    best_key = None
    best_text = None
    for key_size, _ in top_keys:
        list_of_bytes = transpose_bytes(input_bytes, key_size)
        total_score = 0.0
        estimated_key = ""

        for b in list_of_bytes:
            char, score = best_char_for_bytes(b)
            estimated_key += char
        estimated_key = estimated_key.encode()
        output_text = repeating_xor(input_bytes, estimated_key).decode()
        text_score = evaluate_text(output_text)

        if text_score < best_score:
            best_score = total_score
            best_key = estimated_key
            best_text = output_text

    print(f"Key: {best_key}")
    print(f"Text:\n{best_text}")
