from config import BASE_URL
from bs4 import BeautifulSoup
from uptime import boottime
import sqlite3
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

def get_film(film_name):
    name_list = []
    description_list = []
    link_list = []

    try:
        db = sqlite3.connect('../DB_films.db')
        cur = db.cursor()
        print("Подключен к SQLite")

        for name in cur.execute('SELECT NAME FROM DB_films WHERE NAME LIKE ?', ('%' + film_name + '%',)):
            name_list.append(name[0])

        cur.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if db:
            db.close()
            print("Соединение с SQLite закрыто")



def uptime():
    return str(boottime())