
import time
from ngram_score import NgramScore
from two_square_cipher import encrypt, decrypt, filter_text
from simm_anneling_returning_mp import SGSA_MP_timelimit, generate_random_key
from multiprocessing import cpu_count

def compare_texts(text1, text2):
    text1 = filter_text(text1)
    text2 = filter_text(text2)

    min_len = min(len(text1), len(text2))
    text1 = text1[:min_len]
    text2 = text2[:min_len]

    matching_letters = sum(1 for a, b in zip(text1, text2) if a == b)
    return matching_letters / len(text1)

def test_cipher(cipher_text, plain_text, ns, key_length, num_tests):
    results = []
    successes = 0
    average_time = 0
    read_time = None

    for i in range(num_tests):
        start_time = time.time()
        print(f'Key length: {key_length}, attempt: {i}')
        best_score, best_key1, best_key2, decrypted_text = SGSA_MP_timelimit(
            cipher_text, ns, key_length
        )
        elapsed_time = time.time() - start_time
        average_time += elapsed_time

        decrypted_text = decrypt(cipher_text, best_key1, best_key2)
        success_rate = compare_texts(decrypted_text, plain_text)

        if success_rate >= 0.90:  # 90% success rate
            successes += 1
            if read_time is None or elapsed_time < read_time:
                read_time = elapsed_time

        results.append((elapsed_time, decrypted_text, success_rate))

    success_rate = successes / num_tests
    average_time /= num_tests

    return success_rate, average_time, read_time, results

if __name__ == "__main__":
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    ns = NgramScore('./english_bigrams.txt')

    key_lengths = [5, 10, 15, 20, 25]
    num_tests = 1

    # Read text from file
    with open("text3.txt", "r") as f:
        plain_text = f.read().replace('\n', '').upper()
    filtered_text = filter_text(plain_text)

    all_results = []
    lentexts = len(filtered_text)
    text_lengths = [lentexts]
    for text_length in text_lengths:
        for key_length in key_lengths:
            key1 = generate_random_key(key_length)
            key2 = generate_random_key(key_length)
            cipher_text = encrypt(filtered_text, key1, key2)

            success_rate, average_time, read_time, results = test_cipher(
                cipher_text, filtered_text, ns, key_length, num_tests
            )

            test_result = (
                text_length,
                key_length,
                success_rate,
                results[0][1][:]
            )

            all_results.append(test_result)
            print(f"Key lengths: {key_length}")
            print(f"Success rate: {success_rate * 100:.2f}%")
            print(f"Sample result: {results[0][1][:]}...")

            # Save detailed results of each attempt
            with open("results.txt", "a") as results_file:
                results_file.write(f"\nKey length: {key_length}\n")
                results_file.write(f"Success rate: {success_rate * 100:.2f}%\n")
                results_file.write(f"Average time: {average_time:.2f} s\n")
                if read_time is not None:
                    results_file.write(f"Read time: {read_time:.2f} s\n")
                else:
                    results_file.write("Read time: not available\n")
                for i, (elapsed_time, decrypted_text, success_rate) in enumerate(results):
                    results_file.write(f"Attempt {i+1}:\n")
                    results_file.write(f"Elapsed time: {elapsed_time:.2f} s\n")
                    results_file.write(f"Success rate: {success_rate * 100:.2f}%\n")
                    results_file.write(f"Decrypted text: {decrypted_text[:]}...\n")
                results_file.write("\n")

    # Save summary of all results to text file
    with open("results.txt", "a") as results_file:
        results_file.write("Summary of all tests:\n")
        for result in all_results:
            text_length, key_length, success_rate, sample_result = result
            results_file.write(f"Text length: {text_length}, Key length: {key_length}\n")
            results_file.write(f"Success rate: {success_rate * 100:.2f}%\n")
            results_file.write(f"Sample result: {sample_result}...\n\n")

    # Print summary of all results
    print("\nSummary of all tests:")
    for result in all_results:
        text_length, key_length, success_rate, sample_result = result
        print(f"Text length: {text_length}, Key length: {key_length}")
        print(f"Success rate: {success_rate * 100:.2f}%")
        print(f"Sample result: {sample_result}...")