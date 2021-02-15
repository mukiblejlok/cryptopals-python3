import base64

from S01 import (
    xor_bytes, xor_bytes_with_char, xor_bytes_with_repeating_key, evaluate_text, transpose_bytes,
    find_best_char_for_bytes, get_key_length_normalized_distances
)


def challenge_1():
    # Challenge 1
    input_string = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    # Hex to Bytes
    output_bytes = bytearray.fromhex(input_string)
    # bytes to b64
    output_b64 = base64.b64encode(output_bytes)
    assert output_b64 == b"SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
    print("Challenge 1 - OK")


def challenge_2():
    input_string1 = "1c0111001f010100061a024b53535009181c"
    input_string2 = "686974207468652062756c6c277320657965"
    bytes1 = bytearray.fromhex(input_string1)
    bytes2 = bytearray.fromhex(input_string2)
    output_bytes = xor_bytes(bytes1, bytes2)
    assert output_bytes.hex() == "746865206b696420646f6e277420706c6179"
    print("Challenge 2 - OK")


def challenge_3():
    hex_input_string = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    input_bytes = bytearray.fromhex(hex_input_string)
    best_char, score = find_best_char_for_bytes(input_bytes=input_bytes)
    output_bytes = xor_bytes_with_char(input_bytes, best_char)
    print(f"Challenge 3 - {output_bytes} | (Char: {best_char}, Score: {score:3f})")


def challenge_4():
    with open(r"S01\s1c4.txt") as f:
        lines_to_test = f.readlines()
    best_score = float("inf")
    best_char = None
    best_line = None
    output_bytes = None
    for i, line in enumerate(lines_to_test):
        input_bytes = bytearray.fromhex(line)
        char, score = find_best_char_for_bytes(input_bytes)
        if score < best_score:
            best_char = char
            best_score = score
            best_line = i
            output_bytes = xor_bytes_with_char(input_bytes, best_char)
    print(f"Challenge 4 - {output_bytes} | (Line: {best_line}, Char: {best_char}, Score: {best_score:3f})")


def challenge_5():
    input_bytes1 = b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    key = b"ICE"
    expected_hex_string = ("0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272"
                           "a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f")
    output_bytes = xor_bytes_with_repeating_key(input_bytes1, key)
    assert output_bytes.hex() == expected_hex_string
    print("Challenge 5 - OK")


def challenge_6():
    # Read bytes from b64 encoded file
    with open(r"S01\s1c6.txt", "rb") as f:
        input_bytes = base64.b64decode(f.read())

    # Estimate best key size
    keys = get_key_length_normalized_distances(input_bytes, test_cases=range(2, 42))
    top_keys = sorted(keys, key=lambda x: x[1])[:5]
    # Find the best matching key
    best_score = float("inf")
    best_key = None
    best_text = None
    for key_size, _ in top_keys:
        list_of_bytes = transpose_bytes(input_bytes, key_size)
        total_score = 0.0
        estimated_key = ""
        for b in list_of_bytes:
            char, score = find_best_char_for_bytes(b)
            estimated_key += char
        estimated_key = estimated_key.encode()
        output_text = xor_bytes_with_repeating_key(input_bytes, estimated_key).decode()
        text_score = evaluate_text(output_text)

        if text_score < best_score:
            best_score = total_score
            best_key = estimated_key
            best_text = output_text

    print(f"Challenge 6 - Best Key: {best_key}, Text: \"{best_text[:20].strip()}...{best_text[-20:].strip()}\"")


if __name__ == '__main__':
    challenge_1()
    challenge_2()
    challenge_3()
    challenge_4()
    challenge_5()
    challenge_6()
