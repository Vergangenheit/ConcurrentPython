import asyncio
import aiofiles
import aiohttp
from aiohttp import ClientSession
from aiohttp.client_reqrep import ClientResponse
from typing import List, Set, IO
import requests
from requests import Response
import bs4
from bs4 import BeautifulSoup, ResultSet
import re
import time
import urllib.parse
from urllib.error import URLError
import logging
from logging import Logger
import sys
import pathlib

HREF_RE = re.compile(r'href="(.*?)"')

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)

logger: Logger = logging.getLogger("areq")
logging.getLogger("chardet.charsetprober").disabled = True


async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    """GET request wrapper to fetch page HTML.

    kwargs are passed to `session.request()`.
    """

    resp: ClientResponse = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    logger.info("Got response [%s] for URL: %s", resp.status, url)
    html = await resp.text()
    return html


async def parse(url: str, session: ClientSession, **kwargs) -> Set:
    """Find HREFs in the HTML of `url`."""
    found: Set = set()
    try:
        html = await fetch_html(url=url, session=session, **kwargs)
    except (
            aiohttp.ClientError,
            aiohttp.http_exceptions.HttpProcessingError
    ) as e:
        logger.error(
            "aiohttp exception for %s [%s]: %s",
            url,
            getattr(e, "status", None),
            getattr(e, "message", None),
        )
        return found
    except Exception as e:
        logger.error(
            "aiohttp exception for %s [%s]: %s",
            url,
            getattr(e, "status", None),
            getattr(e, "message", None),
        )
        return found

    else:
        for link in HREF_RE.findall(html):
            try:
                abslink: str = urllib.parse.urljoin(url, link)
            except (URLError, ValueError):
                logger.exception("Error parsing URL: %s", link)
                pass
            else:
                found.add(abslink)
        logger.info("Found %d links for %s", len(found), url)

        return found


async def write_one(file: IO, url: str, **kwargs) -> None:
    """Write the found HREFs from `url` to `file`."""
    res: Set = await parse(url=url, **kwargs)
    if not res:
        return None
    async with aiofiles.open(file, "a") as f:
        for p in res:
            await f.write(f"{url}\t{p}\n")
        logger.info("Wrote results for source URL: %s", url)


async def bulk_crawl_and_write(file: IO, urls: Set, **kwargs) -> None:
    """Crawl & write concurrently to `file` for multiple `urls`."""
    async with aiohttp.ClientSession() as session:
        tasks: List = []
        for url in urls:
            tasks.append(write_one(file=file, url=url, session=session, **kwargs))
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    t0 = time.perf_counter()
    here = pathlib.Path(__file__).parent.parent

    with open(here.joinpath("urls.txt")) as infile:
        urls: Set = set(map(str.strip, infile))

    outpath: str = here.joinpath("foundurls.txt")
    with open(outpath, "w") as outfile:
        outfile.write("source_url\tparsed_url\n")

    asyncio.run(bulk_crawl_and_write(file=outpath, urls=urls))
    t1 = time.perf_counter()
    print(f"took {t1 - t0} secs")
