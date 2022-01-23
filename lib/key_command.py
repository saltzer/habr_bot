from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

b_reboot = InlineKeyboardButton("$ reboot vm", callback_data="reboot")
b_shutdown = InlineKeyboardButton("$ shutdown vm", callback_data="shutdown")
b_get_info = InlineKeyboardButton("$ get info", callback_data="get_info")
b_getlog = InlineKeyboardButton("$ get log", callback_data="get_log")
b_restart_bot = InlineKeyboardButton("$ restart bot", callback_data="restart_bot")
b_kill_bot = InlineKeyboardButton("$ kill bot", callback_data="kill_bot")
b_update_db = InlineKeyboardButton("$ update DB", callback_data="update_db")

inline_kb_com = InlineKeyboardMarkup(row_width=2).add(
    b_reboot, b_shutdown, b_get_info, b_getlog, b_restart_bot, b_kill_bot, b_update_db
)
