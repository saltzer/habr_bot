from aiogram import Bot, types, filters
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    message,
)
from config import TOKEN
import urllib.request
from datetime import datetime
from lib.hubs import Hubs
from lib.utils import log, parse
from lib.commands import Command
from lib.key_categories import inline_kb_full
from lib.key_command import inline_kb_com
import os, subprocess

bot = Bot(token=TOKEN)

dispatcher = Dispatcher(bot)
inviteCode = "########"

markup = (
    ReplyKeyboardMarkup(resize_keyboard=True)
    .add(KeyboardButton("/help"))
    .add(KeyboardButton("/categories"))
    .add(KeyboardButton("/command"))
)


def user_authorized(id: int, inviteId: int) -> bool:
    return id == inviteId


async def message_handler(message: types.Message, handler: function) -> None:
    chat_id = message.chat.id
    name = message.chat.first_name

    if user_authorized(chat_id, inviteCode):
        await handler()
        log(f"![{datetime.now()}] Success access from user: {name}\n")
    else:
        await message.reply("Where is your invite code?")
        log(f"![{datetime.now()}] Unregistered user: {name}\n")


async def process_callback_handler(
    url: Hubs, bot: Bot, query: types.CallbackQuery
) -> None:
    res = parse(urllib.request.urlopen(url))
    await bot.send_message(query.from_user.id, res)
    log(f"[{datetime.now()}] Выдана статья по {url}\n")
    await bot.answer_callback_query(query.id)


# ---------main_buttons---------
@dispatcher.message_handler(commands=[Command.Start])
async def process_start_command(message: types.Message):
    async def handler():
        await message.reply(
            "Бот для чтения статей с habr.com\n/help - для помощи.", reply_markup=markup
        )

    message_handler(message, handler)


@dispatcher.message_handler(commands=[Command.Help])
async def process_help_command(message: types.Message):
    async def handler():
        await message.reply(
            """ Бот для чтения статей с habr.com
        Бот отвечает на команды:
            /start - запуск бота
            /help - вывод этого сообщения
            /categories - просмотр хабов
            /command - выполнить команду
        """
        )

    message_handler(message, handler)


@dispatcher.message_handler(commands=[Command.Categories])
async def process_categories_command(message: types.Message):
    async def handler():
        await message.reply("Доступные хабы:", reply_markup=inline_kb_full)

    message_handler(message, handler)


@dispatcher.message_handler(commands=[Command.Vm])
async def process_vm_command(message: types.Message):
    async def handler():
        await message.reply("Доступные команды:", reply_markup=inline_kb_com)

    message_handler(message, handler)


# ---------callback_categories---------
@dispatcher.callback_query_handler(lambda c: c.data == "InfoSec")
async def process_callback_button(callback_query: types.CallbackQuery):
    await process_callback_handler(Hubs.infosec, bot, callback_query)


@dispatcher.callback_query_handler(lambda c: c.data == "Py")
async def process_callback_button(callback_query: types.CallbackQuery):
    await process_callback_handler(Hubs.py, bot, callback_query)


@dispatcher.callback_query_handler(lambda c: c.data == "PopScien")
async def process_callback_button(callback_query: types.CallbackQuery):
    await process_callback_handler(Hubs.popscien, bot, callback_query)


@dispatcher.callback_query_handler(lambda c: c.data == "DIY")
async def process_callback_button(callback_query: types.CallbackQuery):
    await process_callback_handler(Hubs.diy, bot, callback_query)


@dispatcher.callback_query_handler(lambda c: c.data == "Gadgets")
async def process_callback_button(callback_query: types.CallbackQuery):
    await process_callback_handler(Hubs.gadgets, bot, callback_query)


@dispatcher.callback_query_handler(lambda c: c.data == "DevMic")
async def process_callback_button(callback_query: types.CallbackQuery):
    await process_callback_handler(Hubs.devmic, bot, callback_query)


@dispatcher.callback_query_handler(lambda c: c.data == "ServAdm")
async def process_callback_button(callback_query: types.CallbackQuery):
    await process_callback_handler(Hubs.servadm, bot, callback_query)


@dispatcher.callback_query_handler(lambda c: c.data == "DevOps")
async def process_callback_button(callback_query: types.CallbackQuery):
    await process_callback_handler(Hubs.devops, bot, callback_query)


@dispatcher.callback_query_handler(lambda c: c.data == "Network")
async def process_callback_button(callback_query: types.CallbackQuery):
    await process_callback_handler(Hubs.network, bot, callback_query)


@dispatcher.callback_query_handler(lambda c: c.data == "Nix")
async def process_callback_button(callback_query: types.CallbackQuery):
    await process_callback_handler(Hubs.nix, bot, callback_query)


@dispatcher.callback_query_handler(lambda c: c.data == "Robot")
async def process_callback_button(callback_query: types.CallbackQuery):
    await process_callback_handler(Hubs.robot, bot, callback_query)


@dispatcher.callback_query_handler(lambda c: c.data == "SysDev")
async def process_callback_button(callback_query: types.CallbackQuery):
    await process_callback_handler(Hubs.sysdev, bot, callback_query)


# ---------callback_commands---------
@dispatcher.callback_query_handler(lambda c: c.data == "reboot")
async def process_callback_button(callback_query: types.CallbackQuery):
    log("Выполнена команда reboot " + " | Время: " + str(datetime.now()) + "\n")
    os.system("reboot")
    await bot.answer_callback_query(callback_query.id)


@dispatcher.callback_query_handler(lambda c: c.data == "shutdown")
async def process_callback_button(callback_query: types.CallbackQuery):
    log("Выполнена команда shutdown " + " | Время: " + str(datetime.now()) + "\n")
    os.system("shutdown")
    await bot.answer_callback_query(callback_query.id)


@dispatcher.callback_query_handler(lambda c: c.data == "get_log")
async def process_callback_button(callback_query: types.CallbackQuery):
    try:
        with open("log.txt", "rb") as file:
            await bot.send_document(inviteCode, file)
        await bot.answer_callback_query(callback_query.id)
    except:
        await bot.send_message(inviteCode, "Error send log")


@dispatcher.callback_query_handler(lambda c: c.data == "check_net")
async def process_callback_button(callback_query: types.CallbackQuery):
    try:
        command = ["wget -O - -q icanhazip.com"]
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )
        res = process.stdout.read().decode("gbk")
        await bot.send_message(inviteCode, res)
        await bot.answer_callback_query(callback_query.id)
    except:
        await bot.send_message(inviteCode, "Error check IP")


@dispatcher.message_handler()
async def echo_message(msg: types.Message):
    log(msg.chat.full_name + " | " + "@" + msg.chat.username + ": " + msg.text + "\n")
    await bot.send_message(msg.from_user.id, "Hmmm...")


if __name__ == "__main__":
    executor.start_polling(dispatcher)
