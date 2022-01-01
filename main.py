from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN, INVITE_CODE
from lib.category_queries import register_category_queries
from lib.messages import register_message_handlers
from lib.vm_querries import register_vm_queries
from lib.utils import uptime


bot = Bot(token=TOKEN)

dispatcher = Dispatcher(bot)
invite_code = INVITE_CODE


register_message_handlers(dispatcher, bot, invite_code)
register_category_queries(dispatcher, bot)
register_vm_queries(dispatcher, bot, invite_code, uptime())

if __name__ == "__main__":
    executor.start_polling(dispatcher)