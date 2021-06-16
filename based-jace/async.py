import asyncio
import aiohttp
import aiofiles
import time
from typing import Set, List


async def write_genre(filename: str):
    """
    Uses genrenator from binaryjazz.us to write a random genre to the
    name of the given file
    """
    async with aiohttp.ClientSession() as session:
        async with session.get("https://binaryjazz.us/wp-json/genrenator/v1/genre/") as resp:
            resp.raise_for_status()
            genre: str = await resp.json()

    async with aiofiles.open(filename, "w") as new_file:
        print(f'Writing "{genre}" to {filename}"...')
        await new_file.write(genre)


async def main():
    tasks: List = []

    for i in range(5):
        tasks.append(write_genre(f"new_file{i}.txt"))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    print("Starting...")
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(f"Time to complete threading read/writes: {round(end - start, 2)} seconds")
