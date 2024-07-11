
from multiprocessing import cpu_count as mp_cpu_count, cpu_count, Pool
from multiprocessing import Pool as mp_pool
import math
import random
from copy import deepcopy as dcopy
import time
from typing import List, Union

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
              0.4-0.4 * lenkey/25,
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


def AcceptanceFunction(valueOld, valueNew, temp):
    probability = math.exp(-0.5*(valueOld - valueNew)/temp)
    if random.random() < probability:
        return True
    else:
        return False
def SimAnnealing_returning( ct,ns, lenk=25, tempDelta = -0.005):
    t1 = time.time()
    starttemp = 100
    endtemp = 1
    temp = starttemp
    #tempDelta = -0.0005

    keyOld1 = generate_random_key(lenk)
    keyOld2 = generate_random_key(lenk)
    scoreOld = ns.score(decrypt(ct, keyOld1, keyOld2))
    keyMax1, keyMax2, scoreMax = keyOld1, keyOld2, scoreOld
    # print(f'przekazane klucze = {keyOld1 + " " + keyOld2}, oldscore: {scoreOld}')

    temp = starttemp
    j, j_list = 0, []
    while temp >= endtemp:
        if random.random() < 0.5:
            keyNew1 = change_key(keyOld1, lenk)
            keyNew2 = keyOld2
        else:
            keyNew2 = change_key(keyOld2, lenk)
            keyNew1 = keyOld1
        scoreNew = ns.score(decrypt(ct, keyNew1, keyNew2))
        if scoreNew > scoreOld:
            keyOld1, keyOld2, scoreOld = keyNew1, keyNew2, scoreNew
            if scoreOld > scoreMax:  # w 'scoreMax' zapamiętujemy najlepszy wynik przejścia
                j_list.append(j)
                keyMax1, keyMax2, scoreMax, j = keyOld1, keyOld2, scoreOld, 0
                print( f'{scoreOld}, temp: {temp}') #,'\t', msg )
        elif AcceptanceFunction(scoreOld, scoreNew, temp):
            # if abs( scoreOld- scoreNew) > 40:
            #     print( f'{scoreOld} -> {scoreNew}')
            keyOld1, keyOld2, scoreOld = keyNew1, keyNew2, scoreNew
        j += 1
        if j > 250:
            keyOld1, keyOld2, scoreOld, j = keyMax1, keyMax2, scoreMax, 0
        temp += tempDelta
    j_listmean = sum(j_list) / len(j_list) if j_list else 0
    j_listmax = max(j_list) if j_list else 0
    return [scoreMax, keyMax1, keyMax2, decrypt(ct, keyMax1, keyMax2), j_listmean, j_listmax]


def SGSA_MP_timelimit(ct, ns, lenk, timelimit=20, spam=False):
    t1 = time.time()
    if spam:
        print('SGHC_MP with timelimit')
    ncore = cpu_count()
    printedValue, wyniki, uzyte_watki = -9e99, [], 0
    while time.time() - t1 < timelimit:
        with Pool() as pool:
            n_chunks = 3 * (ncore - 1)
            iterable = [[ct,ns,lenk] for i in range(n_chunks)]
            results = []
            for args in iterable:
                result = pool.apply_async(SimAnnealing_returning, args)
                results.append(result)

            uzyte_watki += n_chunks

            # Oczekiwanie na zakończenie wszystkich zadań w czasie timelimit
            t2 = time.time()
            for result in results:
                try:
                    result.wait(timeout=max(0, timelimit - (t2 - t1)))
                    wyniki.append(result.get())
                except TimeoutError:
                    continue

        wyniki.sort(reverse=True)

        # Wykorzystaj najlepsze wyniki z Symulowanego Wyżarzania do Hill Climbing
        best_score = wyniki[0][0]
        best_key1 = wyniki[0][1]
        best_key2 = wyniki[0][2]


        print(best_key1)

        # Wykonaj Hill Climbing na najlepszych wynikach
        hill_climbing_result = HillClimbingMP(ct, best_key1, best_key2,best_score,ns, lenk)

        if hill_climbing_result[0] > printedValue:
            if spam:
                print(hill_climbing_result[0], end='\t')
            printedValue = hill_climbing_result[0]
        else:
            if spam:
                print('<', end=' ')

        t2 = time.time()
        if t2 - t1 >= timelimit:
            break

    t2 = time.time()
    print(f'\nSGHC_MP evaluated in {round(t2 - t1, 2)} sec and used {uzyte_watki} threads')
    return hill_climbing_result

def HillClimbingMP(ciphertext: str, key1, key2, scoreOld, ns, lenkey=25, timelimit: int = 30) -> List[Union[int, str]]:
    keyOld1 = key1
    keyOld2 = key2
    decrypted_text = decrypt(ciphertext, keyOld1, keyOld2)

    if not isinstance(decrypted_text, str):
        raise ValueError("Decryption failed to return a string.")

    scoreOld = scoreOld
    keyMax1, keyMax2, scoreMax = keyOld1, keyOld2, scoreOld

    print(f'przekazane klucze = {keyOld1 + " " + keyOld2}, oldscore: {scoreOld}')

    t1 = time.time()
    print('wspinanie się')

    while time.time() - t1 < timelimit:
        if random.random() < 0.5:
            keyNew1 = change_key(keyOld1,lenkey)
            keyNew2 = keyOld2
        else:
            keyNew2 = change_key(keyOld2,lenkey)
            keyNew1 = keyOld1
        decrypted_text = decrypt(ciphertext, keyNew1, keyNew2)

        if not isinstance(decrypted_text, str):
            continue

        scoreNew = ns.score(decrypted_text)
        if scoreNew > scoreOld:
            keyOld1 = keyNew1
            keyOld2 = keyNew2
            scoreOld = scoreNew
            print(f'scoreOld = {scoreOld}')
            print(f'keys = {keyOld1 + " " + keyOld2}')
            #print(f'keys = {keyNew1 + " " + fullKey2}')
            if scoreOld > scoreMax:     # w 'scoreMax' zapamiętujemy najlepszy wynik przejścia
                keyMax1, keyMax2, scoreMax =  keyOld1, keyOld2, scoreOld

        if scoreOld / (len(ciphertext) - 1) > -2.4:  # -1493.8647289319945:
            break

    return [scoreMax, keyMax1, keyMax2, decrypt(ciphertext, keyMax1, keyMax2)]
#
# def HillClimbingMP2(ciphertext: str, lenkey=25, ns, timelimit: int = 20) -> List[Union[int, str]]:
#     keyOld1 = generate_random_key(lenkey)
#     keyOld2 = generate_random_key(lenkey)
#     decrypted_text = decrypt(ciphertext, keyOld1, keyOld2)
#
#     if not isinstance(decrypted_text, str):
#         raise ValueError("Decryption failed to return a string.")
#
#     scoreOld = ns.score(decrypted_text)
#     print(f'przekazane klucze = {keyOld1 + " " + keyOld2}, oldscore: {scoreOld}')
#     keyMax1, keyMax2, scoreMax = keyOld1, keyOld2, scoreOld
#     t1 = time.time()
#     print('wspinanie się')
#
#     while time.time() - t1 < timelimit:
#         if random.random() < 0.5:
#             keyNew1 = change_key(keyOld1,lenkey)
#             keyNew2 = keyOld2
#         else:
#             keyNew2 = change_key(keyOld2,lenkey)
#             keyNew1 = keyOld1
#         decrypted_text = decrypt(ciphertext, keyNew1, keyNew2)
#
#         if not isinstance(decrypted_text, str):
#             continue
#
#         scoreNew = ns.score(decrypted_text)
#         if scoreNew > scoreOld:
#             keyOld1 = keyNew1
#             keyOld2 = keyNew2
#             scoreOld = scoreNew
#             print(f'scoreOld = {scoreOld}')
#             print(f'keys = {keyOld1 + " " + keyOld2}')
#             #print(f'keys = {keyNew1 + " " + fullKey2}')
#             if scoreOld > scoreMax:     # w 'scoreMax' zapamiętujemy najlepszy wynik przejścia
#                 keyMax1, keyMax2, scoreMax =  keyOld1, keyOld2, scoreOld
#         if scoreOld / (len(ciphertext) - 1) > -2.4:  # -1493.8647289319945:
#             break
#
#     return [scoreMax, keyMax1, keyMax2, ciphertext, decrypt(ciphertext, keyOld1, keyOld2)]