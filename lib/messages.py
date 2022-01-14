import re
import sqlite3
from typing import Callable
from lib.commands import Command
from lib.utils import log, States, get_film
from datetime import datetime
from lib.key_categories import inline_kb_full
from lib.key_command import inline_kb_com
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

markup = (
    ReplyKeyboardMarkup(resize_keyboard=True)
    .add(KeyboardButton("/help"))
    .add(KeyboardButton("/categories"))
    .add(KeyboardButton("/command"))
    .add(KeyboardButton("/films"))
)


def user_authorized(id: int, invite_id: int) -> bool:
    return id == invite_id


def register_message_handlers(dispatcher, bot, invite_code):

    async def message_handler(message, handler: Callable) -> None:
        chat_id = message.chat.id
        name = message.chat.first_name

        if user_authorized(chat_id, invite_code):
            await handler()
            log(f"[{datetime.now()}] Success access from user: {name}\n")
        else:
            await message.reply("Where is your invite code?")
            log(f"[{datetime.now()}] Unregistered user: {name}\n")

    @dispatcher.message_handler(commands=[Command.Start])
    async def process_start_command(message):
        async def handler():
            await message.reply(
                "Бот для чтения статей с habr.com\n/help - для помощи.",
                reply_markup=markup,
            )

        await message_handler(message, handler)

    @dispatcher.message_handler(commands=[Command.Help])
    async def process_help_command(message):
        async def handler():
            await message.reply(
                """ Бот для чтения статей с habr.com
Бот отвечает на команды:
    /start - запуск бота
    /help - вывод этого сообщения
    /categories - просмотр хабов
    /command - выполнить команду
    /films - поиск фильма по БД
            """
            )

        await message_handler(message, handler)

    @dispatcher.message_handler(commands=[Command.Categories])
    async def process_categories_command(message):
        async def handler():
            await message.reply("Доступные хабы:", reply_markup=inline_kb_full)

        await message_handler(message, handler)

    @dispatcher.message_handler(commands=[Command.Vm])
    async def process_vm_command(message):
        async def handler():
            await message.reply("Доступные команды:", reply_markup=inline_kb_com)

        await message_handler(message, handler)


    @dispatcher.message_handler(commands=[Command.Films])
    async def process_await_torrent_film(message):
        await States.STATE_FILM.set()
        await message.reply("Название фильма:")


    @dispatcher.message_handler(state=States.STATE_FILM)
    async def process_torrent_film(message, state: FSMContext):
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

            await bot.send_message(message.from_user.id, name_res + '\n' + '\n' + description_res[1 : -1] + '\n' + '\n' + link_res, reply_markup=markup, parse_mode='HTML')

        await state.finish()
        await state.reset_state()



    @dispatcher.message_handler()
    async def echo_message(msg):
        log(f"{msg.chat.full_name} | @{msg.chat.username}: {msg.text}\n")
        await bot.send_message(msg.from_user.id, "Hmmm...")