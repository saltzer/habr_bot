from aiogram import Bot, types, filters
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, message
from config import TOKEN
from bs4 import BeautifulSoup, SoupStrainer
import urllib.request
from datetime import datetime
import h_url
from key_categories import inline_kb_full
from key_command import inline_kb_com
import os, subprocess

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
invite = ########

button_help = KeyboardButton('/help')
button_categories = KeyboardButton('/categories')
button_com = KeyboardButton('/command')

markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button_help).add(button_categories).add(button_com)

def soup(url):
    soup = BeautifulSoup(url, features="lxml")
    for link in soup.find_all('a', href=True):
        if '/blog/' in link['href'] or '/post/' in link['href']:
            if not link['href'].endswith('blog/') and not link['href'].endswith('comments/'):
                res = "https://habr.com" + link['href']
                return res

def log(line):
    log = open('log.txt', 'a')
    log.write(line)
    log.close()

#---------main_buttons---------

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    chat_id = message.chat.id
    name = message.chat.first_name
    print(chat_id)
    if chat_id != invite:
        await message.reply("Where your invite code?")
        log("! Неудачная попытка запуска бота юзером " + name + " | Время: " + str(datetime.now()) + '\n')
    else:
        await message.reply("Бот для чтения статей с habr.com\n/help - для помощи.", reply_markup=markup)
        log("Удачный запуск бота, открыта клавиатура юзером " + name + " | Время: " + str(datetime.now()) + '\n')

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    chat_id = message.chat.id
    name = message.chat.first_name
    if chat_id != invite:
        await message.reply("Where your invite code?")
        log("! Неудачная попытка обратиться к помощи юзером " + name + " | Время: " + str(datetime.now()) + '\n')
    else:
        await message.reply("Бот для чтения статей с habr.com \n\nБот отвечает на команды:\n\n/start - запуск бота\n/help - вывод этого сообщения\n/categories - просмотр хабов\n/command - выполнить команду")
        log("Удачное обращение к помощи юзером " + name + " | Время: " + str(datetime.now()) + '\n')

@dp.message_handler(commands=['categories'])
async def process_categories_command(message: types.Message):
    chat_id = message.chat.id
    name = message.chat.first_name
    if chat_id != invite:
        await message.reply("Where your invite code?")
        log("! Неудачная попытка открыть категории юзером " + name + " | Время: " + str(datetime.now()) + '\n')
    else:
        await message.reply("Доступные хабы:", reply_markup=inline_kb_full)
        log("Открыты кнопки с хабами юзером " + name + " | Время: " + str(datetime.now()) + '\n')

@dp.message_handler(commands=['command'])
async def process_categories_command(message: types.Message):
    chat_id = message.chat.id
    name = message.chat.first_name
    if chat_id != invite:
        await message.reply("Where your invite code?")
        log("! Неудачная попытка открыть кнопки с командами юзером " + name + " | Время: " + str(datetime.now()) + '\n')
    else:
        await message.reply("Доступные команды:", reply_markup=inline_kb_com)
        log("Открыты кнопки с командами юзером " + name + " | Время: " + str(datetime.now()) + '\n')

#---------callback_categories---------

@dp.callback_query_handler(lambda c: c.data == 'InfoSec')
async def process_callback_button(callback_query: types.CallbackQuery):
    url = urllib.request.urlopen(h_url.url_infosec)
    res = soup(url)
    await bot.send_message(callback_query.from_user.id, res)
    log("Выдана статья по InfoSec" + " | Время: " + str(datetime.now()) + '\n')
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == 'Py')
async def process_callback_button(callback_query: types.CallbackQuery):
    url = urllib.request.urlopen(h_url.url_py)
    res = soup(url)
    await bot.send_message(callback_query.from_user.id, res)
    log("Выдана статья по Py" + " | Время: " + str(datetime.now()) + '\n')
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == 'PopScien')
async def process_callback_button(callback_query: types.CallbackQuery):
    url = urllib.request.urlopen(h_url.url_popscien)
    res = soup(url)
    await bot.send_message(callback_query.from_user.id, res)
    log("Выдана статья по PopScien" + " | Время: " + str(datetime.now()) + '\n')
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == 'DIY')
async def process_callback_button(callback_query: types.CallbackQuery):
    url = urllib.request.urlopen(h_url.url_diy)
    res = soup(url)
    await bot.send_message(callback_query.from_user.id, res)
    log("Выдана статья по DIY" + " | Время: " + str(datetime.now()) + '\n')
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == 'Gadgets')
async def process_callback_button(callback_query: types.CallbackQuery):
    url = urllib.request.urlopen(h_url.url_gadgets)
    res = soup(url)
    await bot.send_message(callback_query.from_user.id, res)
    log("Выдана статья по Gadgets" + " | Время: " + str(datetime.now()) + '\n')
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == 'DevMic')
async def process_callback_button(callback_query: types.CallbackQuery):
    url = urllib.request.urlopen(h_url.url_devmic)
    res = soup(url)
    await bot.send_message(callback_query.from_user.id, res)
    log("Выдана статья по DevMic" + " | Время: " + str(datetime.now()) + '\n')
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == 'ServAdm')
async def process_callback_button(callback_query: types.CallbackQuery):
    url = urllib.request.urlopen(h_url.url_servadm)
    res = soup(url)
    await bot.send_message(callback_query.from_user.id, res)
    log("Выдана статья по ServAdm" + " | Время: " + str(datetime.now()) + '\n')
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == 'DevOps')
async def process_callback_button(callback_query: types.CallbackQuery):
    url = urllib.request.urlopen(h_url.url_devops)
    res = soup(url)
    await bot.send_message(callback_query.from_user.id, res)
    log("Выдана статья по DevOps" + " | Время: " + str(datetime.now()) + '\n')
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == 'Network')
async def process_callback_button(callback_query: types.CallbackQuery):
    url = urllib.request.urlopen(h_url.url_network)
    res = soup(url)
    await bot.send_message(callback_query.from_user.id, res)
    log("Выдана статья по Network" + " | Время: " + str(datetime.now()) + '\n')
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == 'Nix')
async def process_callback_button(callback_query: types.CallbackQuery):
    url = urllib.request.urlopen(h_url.url_nix)
    res = soup(url)
    await bot.send_message(callback_query.from_user.id, res)
    log("Выдана статья по Nix" + " | Время: " + str(datetime.now()) + '\n')
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == 'Robot')
async def process_callback_button(callback_query: types.CallbackQuery):
    url = urllib.request.urlopen(h_url.url_robot)
    res = soup(url)
    await bot.send_message(callback_query.from_user.id, res)
    log("Выдана статья по Robot" + " | Время: " + str(datetime.now()) + '\n')
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == 'SysDev')
async def process_callback_button(callback_query: types.CallbackQuery):
    url = urllib.request.urlopen(h_url.url_sysdev)
    res = soup(url)
    await bot.send_message(callback_query.from_user.id, res)
    log("Выдана статья по SysDev" + " | Время: " + str(datetime.now()) + '\n')
    await bot.answer_callback_query(callback_query.id)

#---------callback_commands---------

@dp.callback_query_handler(lambda c: c.data == 'reboot')
async def process_callback_button(callback_query: types.CallbackQuery):
    log("Выполнена команда reboot " + " | Время: " + str(datetime.now()) + '\n')
    os.system("reboot")
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == 'shutdown')
async def process_callback_button(callback_query: types.CallbackQuery):
    log("Выполнена команда shutdown " + " | Время: " + str(datetime.now()) + '\n')
    os.system("shutdown")
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == 'get_log')
async def process_callback_button(callback_query: types.CallbackQuery):
    try:
        with open('log.txt', 'rb') as file:
            await bot.send_document(invite, file)
        await bot.answer_callback_query(callback_query.id)
    except:
        await bot.send_message(invite, "Error send log")

@dp.callback_query_handler(lambda c: c.data == 'check_net')
async def process_callback_button(callback_query: types.CallbackQuery):
    try:
        command = ['wget -O - -q icanhazip.com']
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        res = process.stdout.read().decode('gbk')
        await bot.send_message(invite, res)
        await bot.answer_callback_query(callback_query.id)
    except:
        await bot.send_message(invite, "Error check IP")

@dp.message_handler()
async def echo_message(msg: types.Message):
    log(msg.chat.full_name + " | " + "@" + msg.chat.username + ": " + msg.text + '\n')
    await bot.send_message(msg.from_user.id, 'Hmmm...')

if __name__ == '__main__':
    executor.start_polling(dp)