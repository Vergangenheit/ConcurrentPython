import asyncio  # Gives us async/await
import aiohttp  # For asynchronously making HTTP requests
import aiofiles  # For asynchronously performing file I/O operations
import concurrent.futures  # Allows creating new processes
from concurrent.futures import ProcessPoolExecutor, Future
from multiprocessing import cpu_count  # Returns our number of CPU cores
from bs4 import BeautifulSoup  # For easy webpage scraping
from math import floor  # Helps divide up our requests evenly across our CPU cores
from typing import Coroutine, List
import time


async def get_and_scrape_pages(num_pages: int, output_file: str) -> Coroutine:
    """
    Makes {{ num_pages }} requests to Wikipedia to receive {{ num_pages }} random
    articles, then scrapes each page for its title and appends it to {{ output_file }},
    separating each title with a tab: "\\t"
    #### Arguments
    ---
    num_pages: int -
        Number of random Wikipedia pages to request and scrape
    output_file: str -
        File to append titles to
    """
    async with aiohttp.ClientSession() as session, aiofiles.open(output_file, "a+", encoding="utf-8") as f:
        for _ in range(num_pages):
            async with session.get('https://en.wikipedia.org/wiki/Special:Random') as resp:
                if resp.status > 399:
                    resp.raise_for_status()

                page: Coroutine = await resp.text()
                soup: BeautifulSoup = BeautifulSoup(page, features="html.parser")
                title: str = soup.find("h1").text
                await f.write(title + "\t")
        await f.write("\n")


def start_scraping(num_pages: int, output_file: str):
    asyncio.run(get_and_scrape_pages(num_pages, output_file))


def main():
    NUM_PAGES = 100  # Number of pages to scrape altogether
    OUTPUT_FILE = "./wiki_titles.tsv"  # File to append our scraped titles to
    NUM_CORES: int = cpu_count()

    PAGES_PER_CORE = floor(NUM_PAGES / NUM_CORES)
    PAGES_FOR_FINAL_CORE = PAGES_PER_CORE + NUM_PAGES % PAGES_PER_CORE  # For our final core

    futures: List[Future] = []
    with ProcessPoolExecutor(NUM_CORES) as executor:
        for i in range(NUM_CORES):
            new_future: Future = executor.submit(start_scraping, num_pages=PAGES_PER_CORE,
                                                 output_file=OUTPUT_FILE)
            futures.append(new_future)

        futures.append(executor.submit(start_scraping, num_pages=PAGES_FOR_FINAL_CORE, output_file=OUTPUT_FILE))

    concurrent.futures.wait(futures)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f'Time to complete: {round(time.time() - start, 2)} seconds.')
