from config import BASE_URL
from bs4 import BeautifulSoup
from uptime import boottime
from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    STATE_FILM = State()


def compose_hub_url(endpoint):
    return f"{BASE_URL}/ru/hub/{endpoint}/"


def log(line):
    with open("log.txt", "a") as log:
        log.write(line)


def parse(url):
    soup = BeautifulSoup(url, features="lxml")
    for link in soup.find_all("a", href=True):
        if "/blog/" in link["href"] or "/post/" in link["href"]:
            if not link["href"].endswith("blog/") and not link["href"].endswith(
                "comments/"
            ):
                res = BASE_URL + link["href"]
                return res


def uptime():
    return str(boottime())