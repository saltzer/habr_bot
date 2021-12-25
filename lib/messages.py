from typing import Callable
from lib.commands import Command
from lib.utils import log
from datetime import datetime
from lib.key_categories import inline_kb_full
from lib.key_command import inline_kb_com
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

markup = (
    ReplyKeyboardMarkup(resize_keyboard=True)
    .add(KeyboardButton("/help"))
    .add(KeyboardButton("/categories"))
    .add(KeyboardButton("/command"))
)


def user_authorized(id: int, inviteId: int) -> bool:
    return id == inviteId


def register_message_handlers(dispatcher, bot, inviteCode):
    async def message_handler(message, handler: Callable) -> None:
        chat_id = message.chat.id
        name = message.chat.first_name

        if user_authorized(chat_id, inviteCode):
            await handler()
            log(f"![{datetime.now()}] Success access from user: {name}\n")
        else:
            await message.reply("Where is your invite code?")
            log(f"![{datetime.now()}] Unregistered user: {name}\n")

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

    @dispatcher.message_handler()
    async def echo_message(msg):
        log(f"{msg.chat.full_name} | @{msg.chat.username}: {msg.text}\n")
        await bot.send_message(msg.from_user.id, "Hmmm...")