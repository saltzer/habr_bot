from config import BASE_URL
from bs4 import BeautifulSoup
from uptime import boottime
import sqlite3, re
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


async def get_film(message):
    film_name = message.text
    if "/" in film_name:
        await message.reply("Обнаружен недопустимый символ")
    else:

        name_list = []
        description_list = []
        link_list = []

        try:
            db = sqlite3.connect('/home/user/PycharmProjects/habr_bot/DB_films.db')
            cur = db.cursor()

            for name in cur.execute('SELECT NAME FROM Films_DB WHERE NAME LIKE ?', ('%' + film_name + '%',)):
                name_list.append(name[0])

            for description in cur.execute('SELECT DESCRIPTION FROM Films_DB WHERE NAME LIKE ?', ('%' + film_name + '%',)):
                description_list.append(description[0])

            for link in cur.execute('SELECT LINK FROM Films_DB WHERE NAME LIKE ?', ('%' + film_name + '%',)):
                link_list.append(link[0])

            cur.close()

            if not name_list:
                name_list.append('В базе нет такого фильма')

            name_res = str(name_list)
            name_res = re.sub(r"['[\]n]", "", name_res)

            description_res = str(description_list)
            description_res = re.sub(r"['[\]n]", "", description_res)

            link_res = str(link_list)
            link_res = re.sub(r"['[\]]", "", link_res)


        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        finally:
            if db:
                db.close()

    return name_res


def uptime():
    return str(boottime())