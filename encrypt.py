from constants import E_TABLE, P_TABLE, LEFT_SHIFT_SCHEDULE, IP_TABLE, PC1_TABLE, PC2_TABLE, IP_INVERSE_TABLE, S_BOX

NUMBER_OF_ROUNDS = 16
BLOCK_SIZE = 64
KEY_SIZE = 64


def string_xor(str1, str2):
    assert (len(str1) == len(str2))
    return bin(int(str1, 2) ^ int(str2, 2))[2:].zfill(len(str1))


def f_function(text, key):
    text = ''.join([text[i - 1] for i in E_TABLE])
    text = string_xor(text, key)

    num_of_s_boxes = len(S_BOX)

    new_text = ""

    for i in range(0, num_of_s_boxes):
        row = text[i * 6] + text[i * 6 + 5]
        row = int(row, 2)

        column = text[i * 6 + 1: i * 6 + 5]
        column = int(column, 2)

        s_value = S_BOX[i][row][column]
        new_text += bin(s_value)[2:].zfill(4)

    new_text = "".join([new_text[i - 1] for i in P_TABLE])

    return new_text


def dea_round(text, key):
    text_len = len(text)
    left = text[: text_len // 2]
    right = text[text_len // 2:]

    new_right = string_xor(left, f_function(right, key))
    new_left = right

    return new_left + new_right


def shift_key(key, round_number):
    key_len = len(key)
    left_key = key[:key_len // 2]
    right_key = key[key_len // 2:]

    bits_rotated = LEFT_SHIFT_SCHEDULE[round_number]
    left_key = left_key[bits_rotated:] + left_key[:bits_rotated]
    right_key = right_key[bits_rotated:] + right_key[:bits_rotated]

    new_key = left_key + right_key

    return new_key


def encrypt(plaintext, key):
    plaintext = bin(int(plaintext, 16))[2:].zfill(BLOCK_SIZE)
    key = bin(int(key, 16))[2:].zfill(BLOCK_SIZE)

    assert (len(key) == KEY_SIZE and len(plaintext) == BLOCK_SIZE)

    plaintext = ''.join([plaintext[i - 1] for i in IP_TABLE])
    key = ''.join(key[i - 1] for i in PC1_TABLE)

    for round_number in range(NUMBER_OF_ROUNDS):
        key = shift_key(key, round_number)
        round_key = "".join([key[i - 1] for i in PC2_TABLE])
        plaintext = dea_round(plaintext, round_key)

    plaintext = plaintext[BLOCK_SIZE // 2:] + plaintext[:BLOCK_SIZE // 2]

    plaintext = ''.join([plaintext[i - 1] for i in IP_INVERSE_TABLE])

    cypher_text = hex(int(plaintext, 2))[2:].zfill(BLOCK_SIZE // 4)

    return cypher_text


if __name__ == "__main__":
    PLAINTEXT = "02468aceeca86420"
    KEY = "0f1571c947d9e859"
    print(encrypt(PLAINTEXT, KEY))
