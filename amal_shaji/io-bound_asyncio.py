import asyncio
from asyncio import AbstractEventLoop
import time
import aiohttp
from tasks import make_request_async
from typing import List, Coroutine


async def main() -> Coroutine:
    # tasks: List = []
    # async with aiohttp.ClientSession() as client:
    #     for num in range(1, 101):
    #         tasks.append(make_request_async(num, client))
    #     await asyncio.gather(*tasks)
    async with aiohttp.ClientSession() as client:
        return await asyncio.gather(
            *[make_request_async(num, client) for num in range(1, 101)]
        )


if __name__ == "__main__":
    start_time = time.perf_counter()
    loop: AbstractEventLoop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    end_time = time.perf_counter()
    print(f"Elapsed run time: {end_time - start_time} seconds.")