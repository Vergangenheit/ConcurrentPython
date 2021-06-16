import time
import multiprocessing
from multiprocessing import Pool, cpu_count
from tasks import get_prime_numbers


def main():
    with Pool(cpu_count() - 1) as pool:
        pool.starmap(get_prime_numbers, zip(range(1000, 16000)))
        pool.close()
        pool.join()


if __name__ == "__main__":
    start_time = time.perf_counter()

    main()

    end_time = time.perf_counter()
    print(f"Elapsed run time: {end_time - start_time} seconds.")
