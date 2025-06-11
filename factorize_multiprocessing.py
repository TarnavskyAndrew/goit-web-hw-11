from multiprocessing import Pool, cpu_count
from colorama import Fore
from time import sleep, perf_counter
from tqdm import tqdm

#  синхронна реалізація:
def factorize_sync(*numbers):
    result = []
    # for number in numbers:
    for number in tqdm(
        numbers,
        desc=f"{Fore.CYAN}Sync{Fore.RESET}", 
        ascii=True, 
        ncols=150
    ):
        sleep(0.5)  # імітація навантаження
        divisors = [i for i in range(1, number + 1) if number % i == 0]
        result.append(divisors)
    return result


def find_divisors(number):
    sleep(0.5)  # імітація навантаження
    return [i for i in range(1, number + 1) if number % i == 0]


# багатопроцесна реалізація:
def factorize_parallel(*numbers):
    with Pool(cpu_count()) as pool:
        # result = pool.map(find_divisors, numbers)
        result = list(
            tqdm(
                pool.imap(find_divisors, numbers),
                total=len(numbers),
                desc=f"{Fore.MAGENTA}Parallel{Fore.RESET}",
                ascii=True,
                ncols=150,
            )
        )
    return result

if __name__ == '__main__':
    test_values = (128, 255, 99999, 10651060)

    print(f"Available cores: {cpu_count()}")

    # синхронно
    start = perf_counter()
    a1, b1, c1, d1 = factorize_sync(*test_values)
    sync_time = perf_counter() - start
    print(f"{Fore.CYAN}Sync -> {sync_time:.2f} sec.{Fore.RESET}")

    # паралельно
    start = perf_counter()
    a2, b2, c2, d2 = factorize_parallel(*test_values)
    parallel_time = perf_counter() - start
    print(f"{Fore.MAGENTA}Parallel -> {parallel_time:.2f} sec.{Fore.RESET}")

    # Порівняння в скільки разів швидше працює multiprocessing версія, порівняно зі звичайною.
    speedup = sync_time / parallel_time
    print(f"Acceleration: x{speedup:.2f}")

    # Перевірка
    assert [a1, b1, c1, d1] == [a2, b2, c2, d2]

    assert a2 == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b2 == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c2 == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d2 == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
                  380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    print(f"{Fore.GREEN}Test passed!{Fore.RESET}")
