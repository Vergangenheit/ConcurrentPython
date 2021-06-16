import time
import threading
from threading import Thread
from tasks import make_request
from typing import List


def main():
    threads: List = []
    for num in range(1, 101):
        thread: Thread = threading.Thread(
            target=make_request,
            args=[num]
        )
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()


if __name__ == "__main__":
    start_time = time.perf_counter()

    main()

    end_time = time.perf_counter()
    print(f"Elapsed run time: {end_time - start_time} seconds.")