"""

-----------------------------------------------------------------------------------------------------------------------

Temat: Szyfrowanie/deszyfrowania i astak na szyfr dwóch kwadratów z wykorzystaniem Symulowanego Wyżarzania i HillClimbing
Autorzy: Damian Kloch, Łukasz Kozioł

-----------------------------------------------------------------------------------------------------------------------

Opis projektu
Projekt koncentruje się na deszyfrowaniu tekstów zaszyfrowanych szyfrem Dwukwadratowym (Two-Square Cipher) przy
użyciu metody Symulowanego Wyżarzania (Simulated Annealing) oraz HilClimbing. Celem projektu jest implementacja
efektywnego algorytmu deszyfrowania, który wykorzystuje oceny n-gramowe do porównywania tekstów oraz wykorzystuje
wieloprocesorowość  do przyspieszenia procesu deszyfrowania. Na początku atak odbywa sie za pomocą Symulowanego
Wyżarzania a następnie przekazywane do HilClimbing są key1, key2, scoreOld i za pomocą wspimaczki wyniki sa
udoskonalane.

-----------------------------------------------------------------------------------------------------------------------

Pliki projektu:
-    hillclimbing.py: Zawiera implementację metody wspinaczki (Hill Climbing) jako alternatywnego podejścia do
deszyfrowania.
-    main.py: Główny plik projektu, w którym odbywa się testowanie skuteczności deszyfrowania dla różnych długości
kluczy i tekstów.
-    simm_anneling_returning_mp.py: Zawiera implementację metody Symulowanego Wyżarzania z wieloprocesorowością.
-    two_square_cipher.py: Zawiera implementację szyfru Dwukwadratowego oraz funkcje pomocnicze do szyfrowania i
deszyfrowania tekstów.
-    tests.py: Program implementuje szyfr Two Square i testuje jego efektywność w odszyfrowywaniu tekstów
zaszyfrowanych  za pomocą różnych długości kluczy. Dodatkowo, program zawiera funkcje porównujące teksty
i oceniające skuteczność odszyfrowywania.
-    ngrqm_score.py: ten plik zawiera implementację klasy NgramScore, która jest używana do oceniania tekstów na
podstawie częstotliwości występowania n-gramów w języku angielskim/włoskim
-    text3.txt: głowny tekst sluzacy do szyfrowania/deszyfrowania w jezyku angielskim
-    plaintextIT: głowny tekst sluzacy do szyfrowania/deszyfrowania w jezyku włoskim
-    wyniki_text1564_90%: wyniki działania tests.py dla tekstu text3.txt dlugosci 1564 (po oczyszczeniu) oraz
akceptowanej poprawnosci deszyfrowane tekstu z tekstem oryginalnym wynoszącym 90%
-    italian_bigrams.txt: plik zawierajacy włoskie bigramy
-    english_bigrams.txt: plik zawierający angielskie bigramy

-----------------------------------------------------------------------------------------------------------------------

"""



from two_square_cipher import read_plaintext_from_file, encrypt, print_square, generate_square, filter_text
from hillclimbing import generate_random_key
from ngram_score import NgramScore
from simm_anneling_returning_mp import  SGSA_MP_timelimit

if __name__ == "__main__":
    # Zapytaj użytkownika o język
    language = input("Podaj język (1 - angielski, 2 - włoski): ")
    if language == '1':
        ngram_file = 'english_bigrams.txt'
        plaintext_file = "text3.txt"
    elif language == '2':
        ngram_file = 'italian_bigrams.txt'
        plaintext_file = "plaintextIT.txt"
    else:
        print("Niepoprawny wybór języka.")
        exit()

    # Zapytaj użytkownika o długość klucza
    lenkey = int(input("Podaj długość klucza: "))

    # Generowanie kluczy
    key1 = generate_random_key(lenkey)
    key2 = generate_random_key(lenkey)

    # Wczytywanie i filtrowanie tekstu jawnego
    plaintext = read_plaintext_from_file(plaintext_file)
    filtered_text = filter_text(plaintext)

    # Szyfrowanie tekstu jawnego
    ciphertext = encrypt(filtered_text, key1, key2)
    print("Original Plaintext:\n", filtered_text)
    print("Ciphertext:\n", ciphertext)

    ns = NgramScore(ngram_file)

    if ciphertext:
        expected_score = ns.score(filtered_text)
        square1 = generate_square(key1)
        square2 = generate_square(key2)
        best_score, best_key1, best_key2, decrypted_text = SGSA_MP_timelimit(ciphertext, ns, lenkey)
        print(f"Best score: {best_score}")
        print(f"Expected score: {expected_score}")
        square3 = generate_square(best_key1)
        square4 = generate_square(best_key2)
        print("best keys:")
        print_square(square3, square4)
        print("original keys:")
        print_square(square1, square2)
        print(f"Decrypted text: {decrypted_text}")
    else:
        print("Encryption failed.")
