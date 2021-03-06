from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

b_infosec = InlineKeyboardButton("Информационная безопасность", callback_data="InfoSec")
b_py = InlineKeyboardButton("Python", callback_data="Py")
b_popscien = InlineKeyboardButton("Научно-популярное", callback_data="PopScien")
b_diy = InlineKeyboardButton("DIY", callback_data="DIY")
b_gadgets = InlineKeyboardButton("Гаджеты", callback_data="Gadgets")
b_devmic = InlineKeyboardButton(
    "Программирование микроконтроллеров", callback_data="DevMic"
)
b_servadm = InlineKeyboardButton("Серверное администрирование", callback_data="ServAdm")
b_devops = InlineKeyboardButton("DevOps", callback_data="DevOps")
b_net = InlineKeyboardButton("Сетевые технологии", callback_data="Network")
b_nix = InlineKeyboardButton("*nix", callback_data="Nix")
b_robotics = InlineKeyboardButton("Робототехника", callback_data="Robot")
b_sysdev = InlineKeyboardButton("Системное программирование", callback_data="SysDev")

inline_kb_full = InlineKeyboardMarkup(row_width=1).add(
    b_devmic, b_infosec, b_servadm, b_sysdev
)
inline_kb_full.add(b_net, b_robotics)
inline_kb_full.row(b_py, b_popscien)
inline_kb_full.row(b_gadgets, b_devops)
inline_kb_full.row(b_diy, b_nix)
