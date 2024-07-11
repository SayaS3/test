
import random
from copy import deepcopy as dcopy
from typing import List, Tuple, Union, Dict
import time
from two_square_cipher import decrypt
import string

def generate_random_key(lenkey=25):
    alphabet = list(string.ascii_uppercase.replace('J', ''))
    key_part = random.sample(alphabet, lenkey)
    for letter in key_part:
        alphabet.remove(letter)
    key = key_part + alphabet
    return ''.join(key)

def swap2(key: str, lenkey=25) -> str:
    key_list = list(dcopy(key))
    idx1, idx2 = random.sample(range(lenkey), 2)
    key_list[idx1], key_list[idx2] = key_list[idx2], key_list[idx1]
    return ''.join(key_list)


def swap3(key, lenkey=25):
    key2 = list(dcopy(key))
    idx1, idx2, idx3 = random.sample(range(lenkey), 3)
    if random.random() < 0.5:
        key2[idx1], key2[idx2], key2[idx3] = key2[idx2], key2[idx3], key2[idx1]
    else:
        key2[idx1], key2[idx2], key2[idx3] = key2[idx3], key2[idx1], key2[idx2]
    return ''.join(key2)


def changeOne(key: str, lenkey=25) -> str:
    key_list = list(dcopy(key))
    idx1 = random.choice(range(lenkey))
    if lenkey < len(key):
        letter1 = random.choice(key[lenkey:])
        idx2 = key.index(letter1)
        key_list[idx1], key_list[idx2] = key_list[idx2], key_list[idx1]
        key_list = key_list[:lenkey] + sorted(key_list[lenkey:])
    return ''.join(key_list)


def changeTwo(key: str, lenkey=25) -> str:
    key_list = list(dcopy(key))
    idx1 = random.choice(range(lenkey))
    idx2 = random.choice(range(lenkey))
    while idx2 == idx1:  # Upewniamy się, że idx2 jest różne od idx1
        idx2 = random.choice(range(lenkey))

    key_list[idx1], key_list[idx2] = key_list[idx2], key_list[idx1]

    return ''.join(key_list)


'''
def reverse_columns(key: str, lenkey=25) -> str:
    matrix = [list(key[i:i + 5]) for i in range(0, 25, 5)]
    col_index = random.randint(0, 4)
    column = [matrix[row][col_index] for row in range(5)]
    column.reverse()
    for row in range(5):
        matrix[row][col_index] = column[row]
    reversed_key = ''.join([''.join(row) for row in matrix])
    reversed_key_list = list(reversed_key)
    sorted_part = ''.join(sorted(reversed_key_list[lenkey:]))
    final_key = ''.join(reversed_key_list[:lenkey]) + sorted_part
    return final_key
'''


def shuffle_rows_columns(key: str, lenkey=25) -> str:
    max_row = max(0, lenkey // 5 - 1)
    probs = [0, 0.05, 0.15, 0.3, 0.5]

    if random.random() < 1.0 - probs[max_row]:
        matrix = [list(key[i:i + 5]) for i in range(0, 25, 5)]
        col_index = random.randint(0, 4)
        column = [matrix[row][col_index] for row in range(5)]
        random.shuffle(column)
        for row in range(5):
            matrix[row][col_index] = column[row]
        reversed_key = ''.join([''.join(row) for row in matrix])
        reversed_key_list = list(reversed_key)
        sorted_part = ''.join(sorted(reversed_key_list[lenkey:]))
        final_key = ''.join(reversed_key_list[:lenkey]) + sorted_part
        return final_key
    else:
        row_index = random.randint(0, max_row)
        final_key = dcopy(key)
        random.shuffle(final_key[row_index])

        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        test = set([c for sublist in final_key for c in sublist])
        # print( f'test = {test}')
        assert test == set(list(alphabet)), f' ! !!! ! !'

        return final_key


def swap_rows(key: str, lenkey=25) -> str:
    matrix = [list(key[i:i + 5]) for i in range(0, 25, 5)]
    row1, row2 = random.sample(range(5), 2)
    matrix[row1], matrix[row2] = matrix[row2], matrix[row1]
    swapped_key = ''.join([''.join(row) for row in matrix])
    final_key = swapped_key[:lenkey] + ''.join(sorted(swapped_key[lenkey:]))
    return final_key


def swap_columns(key: str, lenkey=25) -> str:
    matrix = [list(key[i:i + 5]) for i in range(0, 25, 5)]
    col1, col2 = random.sample(range(5), 2)
    for row in matrix:
        row[col1], row[col2] = row[col2], row[col1]
    swapped_key = ''.join([''.join(row) for row in matrix])
    final_key = swapped_key[:lenkey] + ''.join(sorted(swapped_key[lenkey:]))
    return final_key

def transpose_key(key: str, lenkey=25) -> str:
    matrix = [list(key[i:i + 5]) for i in range(0, 25, 5)]
    transposed_matrix = [[matrix[j][i] for j in range(5)] for i in range(5)]
    transposed_key = ''.join([''.join(row) for row in transposed_matrix])
    transposed_part = transposed_key[:lenkey]
    remaining_part = transposed_key[lenkey:]
    sorted_remaining_part = ''.join(sorted(remaining_part))
    final_key = transposed_part + sorted_remaining_part
    return final_key

def change_key(key: str, lenkey=25) -> str:
    r_prob = [0.3 + 0.3 * lenkey / 25, 0.19 * lenkey / 25,
              0.4-0.4* lenkey/25,
              0, 0.01, 0.01, 0.005, 0.185]
    sum_r = [sum(r_prob[:i + 1]) for i in range(len(r_prob))]
    # print( f'sum_r = {sum_r}')
    r = random.random()
    if r < sum_r[0]:
        return swap2(key, lenkey)
    elif r < sum_r[1]:
        return swap3(key, lenkey)
    elif r < sum_r[2]:
        return changeOne(key, lenkey)
    elif r < sum_r[3]:
        return changeTwo(key, lenkey)
    elif r < sum_r[4]:
        return swap_columns(key, lenkey)
    elif r < sum_r[5]:
        return swap_rows(key, lenkey)
    elif r < sum_r[6]:
        return transpose_key(key, lenkey)
    else:
        return shuffle_rows_columns(key, lenkey)


def HillClimbing(ciphertext: str, ns, lenkey=25, timelimit: int = 60, max_restarts: int = 1000) -> List[Union[int,
str]]:
    best_global_score = -float('inf')
    best_global_key1 = None
    best_global_key2 = None
    best_score_runtime = 0

    def generate_new_keys(lenkey):
        return generate_random_key(lenkey), generate_random_key(lenkey)

    def run_hill_climbing(start_key1, start_key2):
        nonlocal best_global_score, best_global_key1, best_global_key2, best_score_runtime
        t1 = time.time()  # Define t1 here
        iters = 0

        keyOld1 = start_key1
        keyOld2 = start_key2
        decrypted_text = decrypt(ciphertext, keyOld1, keyOld2)

        if not isinstance(decrypted_text, str):
            raise ValueError("Decryption failed to return a string.")

        scoreOld = ns.score(decrypted_text)
        print('Rozpoczęcie wspinaczki')

        last_best_score = scoreOld
        best_key1 = keyOld1
        best_key2 = keyOld2

        while time.time() - t1 < timelimit:
            iters += 1
            if random.random() < 0.5:
                keyNew1 = change_key(keyOld1, lenkey)
                keyNew2 = keyOld2
            else:
                keyNew2 = change_key(keyOld2, lenkey)
                keyNew1 = keyOld1
            decrypted_text = decrypt(ciphertext, keyNew1, keyNew2)

            if not isinstance(decrypted_text, str):
                continue

            scoreNew = ns.score(decrypted_text)

            if scoreNew > scoreOld:
                keyOld1 = keyNew1
                keyOld2 = keyNew2
                scoreOld = scoreNew
                print(f'Wynik: {scoreOld},\tKlucze: {keyOld1} {keyOld2}')
                # print(f'')
                if scoreOld > last_best_score:
                    last_best_score = scoreOld
                    best_key1 = keyOld1
                    best_key2 = keyOld2
                    best_score_runtime = time.time() - t1
                    t1 = time.time()

                    if scoreOld > best_global_score:
                        best_global_score = scoreOld
                        best_global_key1 = keyOld1
                        best_global_key2 = keyOld2

                if scoreOld / (len(ciphertext) - 1) > -2.4:  # -1493.8647289319945:
                    break
            else:
                if time.time() - t1 > 10:
                    print(f"Restartowanie z powodu braku poprawy, {iters} iteracji")
                    return False, best_key1, best_key2, t1

        czas_pracy = time.time() - t1
        print(f'Czas działania: {czas_pracy} sekund, {iters} iteracji')
        return True, best_key1, best_key2, t1

    start_key1, start_key2 = generate_new_keys(lenkey)
    restart_count = 0
    total_runtime = 0
    while restart_count < max_restarts:
        success, best_key1, best_key2, t1 = run_hill_climbing(start_key1, start_key2)
        total_runtime += time.time() - t1
        if success:
            break
        else:
            restart_count += 1
            start_key1, start_key2 = generate_new_keys(lenkey)

    decrypted_text = decrypt(ciphertext, best_global_key1, best_global_key2)
    if not isinstance(decrypted_text, str):
        raise ValueError("Decryption failed to return a string.")

    best_score = ns.score(decrypted_text)
    if best_score / (len(ciphertext) - 1) > -2.4:
        print(f"Klucz 1: {best_global_key1}")
        print(f"Klucz 2: {best_global_key2}")
        print(f"Najlepszy wynik: {best_global_score}")
        print(f"Czas najlepszego wyniku: {best_score_runtime} sekund")
        print(f"Ostatni wynik: {best_score}, liczba restartów: {restart_count}")
        print(f"Zdeszyfrowany tekst: {decrypted_text}")
        print("Oczekiwany score: -3670.893372781515")

    print(f"Całkowity czas działania: {total_runtime} sekund")

    return [best_global_score, best_global_key1, best_global_key2, decrypted_text]