from bs4 import BeautifulSoup
import requests
import random
import sqlite3

from config import LORDFILM_0


db = sqlite3.connect("DB_films.db")
cur = db.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS Films_DB (
    ID INTEGER PRIMARY KEY,
    RESOURCE TEXT,
    NAME TEXT,
    DESCRIPTION TEXT,
    LINK TEXT
)""")
db.commit()

resource = "Lordfilm"

user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

user_agent = random.choice(user_agent_list)
headers = {'User-Agent': user_agent}

x = 1
url = LORDFILM_0


while True:
    i = 0
    page = BeautifulSoup(requests.get(url,headers=headers).text, "lxml")

    name_list = []
    date_list = []
    link1_list = []
    description_list = []


    for name in page.find_all("div", class_="th-title"):
        name_text = name.text
        print(name_text)
        name_list.append(name_text)

    for film in page.find_all("div", class_="th-item"):
        Link_STR = film.find("a", class_="th-in with-mask").get('href')
        link1_list.append(Link_STR)


    for link0 in link1_list:

        page2 = BeautifulSoup(requests.get(link0,headers=headers).text, "lxml")

        description = page2.find("div", class_="fdesc clearfix slice-this").text

        b_split_list = description.split("						")
        b1 = b_split_list[-1]

        description_list.append(b1)


    while i < len(description_list):
        name1 = name_list[i]
        description1 = description_list[i]
        link2 = link1_list[i]

        cur.execute("""INSERT INTO Films_DB (
            RESOURCE, 
            NAME,
            DESCRIPTION, 
            LINK) VALUES (?, ?, ?, ?);""", (
                resource,
                name1,
                description1,
                link2))
        db.commit()

        print("Успешно добавлено " + str(i))
        i = i + 1


    x = x + 1
    url = LORDFILM_0 + "page/" + str(x) + "/"
    print(url)


    if x == 919:
        print("БД собрана, всего элементов: " + str(919 * 36))
        cur.close()
        db.close()
        break