import time
from urllib.request import Request, urlopen
import json
import threading
from threading import Thread
from typing import List


def write_genre(file_name: str):
    """
    Uses genrenator from binaryjazz.us to write a random genre to the
    name of the given file
    """

    req: Request = Request("https://binaryjazz.us/wp-json/genrenator/v1/genre/", headers={'User-Agent': 'Mozilla/5.0'})
    genre: str = json.load(urlopen(req))

    with open(file_name, "w") as new_file:
        print(f'Writing "{genre}" to "{file_name}"...')
        new_file.write(genre)

def main():
    threads: List = []

    for i in range(5):
        thread: Thread = threading.Thread(
            target=write_genre,
            args=[f"new_file{i}.txt"]
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def main2():
    for i in range(5):
        write_genre(f"new_file{i}.txt")

if __name__ == "__main__":
    print("Starting...")
    start = time.time()
    main()
    end = time.time()
    print(f"Time to complete threading read/writes: {round(end - start, 2)} seconds")
