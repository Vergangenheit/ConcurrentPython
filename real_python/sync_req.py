from typing import List
import requests
from requests import Response
import re
import time

HREF_RE = re.compile(r'href="(.*?)"')


def read_urls() -> List:
    with open('../urls.txt', 'r') as f:
        urls: List = f.readlines()
        urls: List = [i.replace('\n', '') for i in urls]

    return urls


def get_html(url: str) -> str:
    resp: Response = requests.get(url)

    return resp.text


def get_content(html: str) -> List:
    hrefs: List = HREF_RE.findall(html)

    return hrefs


def write_urls(hrefs: List):
    with open('../foundurls.txt', 'w') as f:
        for href in hrefs:
            f.write(href)
            f.write('\n')



def main() -> None:
    t0 = time.perf_counter()
    final_list: List = []
    urls: List = read_urls()
    for url in urls:
        text: str = get_html(url)
        hrefs: List = get_content(text)
        final_list.extend(hrefs)
    write_urls(final_list)
    t1 = time.perf_counter()
    print(f"took {t1 - t0} secs")


if __name__ == "__main__":
    main()
