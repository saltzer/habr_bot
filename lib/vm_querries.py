from lib.utils import log
from datetime import datetime
import os, subprocess


def register_vm_queries(dispatcher, bot, inviteCode):
    @dispatcher.callback_query_handler(lambda c: c.data == "reboot")
    async def process_callback_button(callback_query):
        log("Выполнена команда reboot " + " | Время: " + str(datetime.now()) + "\n")
        os.system("reboot")
        await bot.answer_callback_query(callback_query.id)

    @dispatcher.callback_query_handler(lambda c: c.data == "shutdown")
    async def process_callback_button(callback_query):
        log("Выполнена команда shutdown " + " | Время: " + str(datetime.now()) + "\n")
        os.system("shutdown")
        await bot.answer_callback_query(callback_query.id)

    @dispatcher.callback_query_handler(lambda c: c.data == "get_log")
    async def process_callback_button(callback_query):
        try:
            with open("log.txt", "rb") as file:
                await bot.send_document(inviteCode, file)
            await bot.answer_callback_query(callback_query.id)
        except:
            await bot.send_message(inviteCode, "Error send log")

    @dispatcher.callback_query_handler(lambda c: c.data == "check_net")
    async def process_callback_button(callback_query):
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
