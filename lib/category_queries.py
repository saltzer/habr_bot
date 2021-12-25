from lib.hubs import Hubs
from lib.utils import parse, log
import urllib.request
from datetime import datetime


async def process_callback_handler(url: Hubs, bot, query) -> None:
    res = parse(urllib.request.urlopen(url))
    await bot.send_message(query.from_user.id, res)
    log(f"[{datetime.now()}] Выдана статья по {url}\n")
    await bot.answer_callback_query(query.id)


def register_category_queries(dispatcher, bot):
    @dispatcher.callback_query_handler(lambda c: c.data == "InfoSec")
    async def process_callback_button(callback_query):
        await process_callback_handler(Hubs.infosec, bot, callback_query)

    @dispatcher.callback_query_handler(lambda c: c.data == "Py")
    async def process_callback_button(callback_query):
        await process_callback_handler(Hubs.py, bot, callback_query)

    @dispatcher.callback_query_handler(lambda c: c.data == "PopScien")
    async def process_callback_button(callback_query):
        await process_callback_handler(Hubs.popscien, bot, callback_query)

    @dispatcher.callback_query_handler(lambda c: c.data == "DIY")
    async def process_callback_button(callback_query):
        await process_callback_handler(Hubs.diy, bot, callback_query)

    @dispatcher.callback_query_handler(lambda c: c.data == "Gadgets")
    async def process_callback_button(callback_query):
        await process_callback_handler(Hubs.gadgets, bot, callback_query)

    @dispatcher.callback_query_handler(lambda c: c.data == "DevMic")
    async def process_callback_button(callback_query):
        await process_callback_handler(Hubs.devmic, bot, callback_query)

    @dispatcher.callback_query_handler(lambda c: c.data == "ServAdm")
    async def process_callback_button(callback_query):
        await process_callback_handler(Hubs.servadm, bot, callback_query)

    @dispatcher.callback_query_handler(lambda c: c.data == "DevOps")
    async def process_callback_button(callback_query):
        await process_callback_handler(Hubs.devops, bot, callback_query)

    @dispatcher.callback_query_handler(lambda c: c.data == "Network")
    async def process_callback_button(callback_query):
        await process_callback_handler(Hubs.network, bot, callback_query)

    @dispatcher.callback_query_handler(lambda c: c.data == "Nix")
    async def process_callback_button(callback_query):
        await process_callback_handler(Hubs.nix, bot, callback_query)

    @dispatcher.callback_query_handler(lambda c: c.data == "Robot")
    async def process_callback_button(callback_query):
        await process_callback_handler(Hubs.robot, bot, callback_query)

    @dispatcher.callback_query_handler(lambda c: c.data == "SysDev")
    async def process_callback_button(callback_query):
        await process_callback_handler(Hubs.sysdev, bot, callback_query)
