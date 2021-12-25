from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

b_reboot = InlineKeyboardButton('$ reboot vm',                     callback_data='reboot')
b_shutdown = InlineKeyboardButton('$ shutdown vm',                 callback_data='shutdown')
b_checknet = InlineKeyboardButton('$ check IP',                callback_data='check_net')
b_getlog = InlineKeyboardButton('$ get log',                       callback_data='get_log')

inline_kb_com = InlineKeyboardMarkup(row_width=2).add(b_reboot, b_shutdown, b_checknet, b_getlog)