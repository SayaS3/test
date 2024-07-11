
import string


def generate_square(key):
    key_without = []
    if len(key) < 25:
        for i in key:
            if i not in key_without:
                key_without.append(i)

        alfabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'  # Pominięto "J"
        for i in alfabet:
            if i not in key_without:
                key_without.append(i)
    else:
        key_without = list(key)

    table = [key_without[i:i + 5] for i in range(0, len(key_without), 5)]
    dict = {table[i][j]: (i, j) for i in range(5) for j in range(5)}

    return table, dict

def filter_text(plain_text):
    filtered_text = ''
    plaintext = plain_text.upper()
    for character in plaintext:
        if character in string.ascii_uppercase:
            filtered_text += 'I' if character == 'J' else character
    return filtered_text

def encrypt(filtered_text, key1, key2):
    # Szyfrowanie tekstu jawnego za pomocą dwóch kwadratów
    square1, dict1 = generate_square(key1)
    square2, dict2 = generate_square(key2)

    encrypted_text = []

    for i in range(0, len(filtered_text), 2):
        a, b = filtered_text[i], filtered_text[i + 1]
        row1, col1 = dict1[a]
        row2, col2 = dict2[b]

        encrypted_text.append(square1[row1][col2])
        encrypted_text.append(square2[row2][col1])

    return ''.join(encrypted_text)

def decrypt(cipher_text, key1, key2):
    # Deszyfrowanie tekstu za pomocą dwóch kwadratów
    square1, dict1 = generate_square(key1)
    square2, dict2 = generate_square(key2)

    decrypted_text = []

    for i in range(0, len(cipher_text), 2):
        a, b = cipher_text[i], cipher_text[i + 1]
        row1, col1 = dict1[a]
        row2, col2 = dict2[b]

        decrypted_text.append(square1[row1][col2])
        decrypted_text.append(square2[row2][col1])

    return ''.join(decrypted_text)

def read_plaintext_from_file(file_path: str) -> str:
    try:
        with open(file_path, "r") as file:
            plaintext = file.read()
        return plaintext
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return ""

def print_square(squarea, squareb):
    # Wyświetlanie kwadratu szyfrującego lub deszyfrującego
    table_a, _ = squarea  # Rozpakowanie kwadratu, ignorujemy słownik
    table_b, _ = squareb
    for row in range(5):
        row_a = ' '.join(table_a[row])
        row_b = ' '.join(table_b[row])
        print(f"{row_a}     {row_b}")
