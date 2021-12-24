from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


b_reboot = InlineKeyboardButton('$ reboot vm',                     callback_data='reboot')
b_shutdown = InlineKeyboardButton('$ shutdown vm',                 callback_data='shutdown')
b_mycom = InlineKeyboardButton('$ my command',                     callback_data='mycom')
b_getlog = InlineKeyboardButton('$ get log',                       callback_data='get_log')

inline_kb_com = InlineKeyboardMarkup(row_width=2).add(b_reboot, b_shutdown, b_mycom, b_getlog)