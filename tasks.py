import os
from multiprocessing import current_process
from threading import current_thread
from typing import List
import requests
from aiohttp import ClientSession


def make_request(num: int):
    # io-bound

    pid: int = os.getpid()
    thread_name: str = current_thread().name
    process_name: str = current_process().name
    print(f"{pid} - {process_name} - {thread_name}")

    requests.get("https://httpbin.org/ip")


async def make_request_async(num: int, client: ClientSession):
    # io-bound

    pid: int = os.getpid()
    thread_name: str = current_thread().name
    process_name: str = current_process().name
    print(f"{pid} - {process_name} - {thread_name}")

    await client.get("https://httpbin.org/ip")


def get_prime_numbers(num) -> List:
    # cpu-bound

    pid: int = os.getpid()
    thread_name: str = current_thread().name
    process_name: str = current_process().name
    print(f"{pid} - {process_name} - {thread_name}")

    numbers: List = []

    prime: List = [True for i in range(num + 1)]
    p = 2

    while p * p <= num:
        if prime[p]:
            for i in range(p * 2, num + 1, p):
                prime[i] = False
        p += 1

    prime[0] = False
    prime[1] = False

    for p in range(num + 1):
        if prime[p]:
            numbers.append(p)

    return numbers