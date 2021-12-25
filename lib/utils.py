from config import BASE_URL
from bs4 import BeautifulSoup


def compose_hub_url(endpoint):
    return f"{BASE_URL}/ru/hub/{endpoint}/"


def log(line):
    log = open("log.txt", "a")
    log.write(line)
    log.close()


def parse(url):
    soup = BeautifulSoup(url, features="lxml")
    for link in soup.find_all("a", href=True):
        if "/blog/" in link["href"] or "/post/" in link["href"]:
            if not link["href"].endswith("blog/") and not link["href"].endswith(
                "comments/"
            ):
                res = BASE_URL + link["href"]
                return res
