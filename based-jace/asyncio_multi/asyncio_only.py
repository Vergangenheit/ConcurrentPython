import asyncio
from bs4 import BeautifulSoup
import urllib.request
import aiohttp
import aiofiles
from typing import Coroutine,List
import time


async def get_and_scrape_pages(num_pages: int, output_file: str):
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


async def main():
    NUM_PAGES = 100  # Number of pages to scrape altogether
    OUTPUT_FILE = "./wiki_titles.tsv"  # File to append our scraped titles to

    await get_and_scrape_pages(NUM_PAGES, OUTPUT_FILE)

if __name__ == "__main__":
    print("Starting...")
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(f"Time to complete threading read/writes: {round(end - start, 2)} seconds")


