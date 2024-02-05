from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram import types
from data.users import user_profile
from data.subscribes import SelectTable
from config import CHANNEL_URL


class Menu_callback(CallbackData, prefix="menu"):
    menu: str


class Money_callback(CallbackData, prefix="money"):
    id: int
    name: str
    price: float
    prefix: str


class Buy_answer(CallbackData, prefix="answer"):
    buy: str


class ButtonTexts:
    BACK = "↩️ Назад"
    CANCEL = "↩️ Отмена"
    SUBSCRIBE = "⚜️ Подписка"
    REPLENISH = "💸 Пополнить"
    PAY = "Оплатить"


async def money():
    temp_list = []
    kb = []
    records = SelectTable()

    for record in records[:6]:
        temp_list.append(types.InlineKeyboardButton(
            text=f"{record[1]} - {float(record[2])}$", callback_data=Money_callback(id=record[0], name=record[1], price=float(record[2]), prefix='sub').pack()))
        if len(temp_list) == 2:
            kb.append(temp_list.copy())
            temp_list.clear()

    if temp_list:
        kb.append(temp_list)
    kb.append([
        types.InlineKeyboardButton(
            text=ButtonTexts.BACK, callback_data=Menu_callback(menu="private_menu").pack()),
    ])

    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def anwser_for_buy():
    kb = [
        [
            types.InlineKeyboardButton(text=ButtonTexts.PAY, callback_data=Buy_answer(buy="yes").pack())
        ],
        [
            types.InlineKeyboardButton(text=ButtonTexts.CANCEL, callback_data=Buy_answer(buy="cancel").pack())
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def k_menu():
    kb = [
        [
            types.InlineKeyboardButton(
                text='💼 Рабочий кабинет', callback_data=Menu_callback(menu="work_menu").pack()),
            types.InlineKeyboardButton(
                text='👤 Личный кабинет', callback_data=Menu_callback(menu="private_menu").pack())
        ],
        [
            types.InlineKeyboardButton(
                text='📤 Загрузить аккаунт', callback_data=Menu_callback(menu="upl_acc").pack()),
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def k_menu2():
    kb = [
        [
            types.InlineKeyboardButton(text='💼 Рабочий кабинет', callback_data=Menu_callback(menu="work_menu").pack()),
            types.InlineKeyboardButton(text='👤 Личный кабинет', callback_data=Menu_callback(menu="private_menu").pack())
        ],
        [
            types.InlineKeyboardButton(text='📤 Загрузить аккаунт', callback_data=Menu_callback(menu="upl_acc").pack()),
        ],
        [
            types.InlineKeyboardButton(text='⚙️ Админ панель', callback_data=Menu_callback(menu="admin").pack()),
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def cancel_in():
    kb = [
        [
            types.InlineKeyboardButton(
                text=ButtonTexts.CANCEL, callback_data=Menu_callback(menu="cancel").pack())
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def cancel_rp():
    kb = [
        [
            KeyboardButton(text=ButtonTexts.BACK)
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


async def k_work_menu(user_id):
    kb = [
        [
            types.InlineKeyboardButton(
                text='🖍️ Текст', callback_data=Menu_callback(menu="text").pack()),
            types.InlineKeyboardButton(
                text='⏰ Задержка', callback_data=Menu_callback(menu="delay").pack()),
        ],

        [
            types.InlineKeyboardButton(
                text=f'{(await user_profile(user_id))[8]} Отправка уведомлений', callback_data=Menu_callback(menu="send_notifications").pack()),
            types.InlineKeyboardButton(
                text=f'{(await user_profile(user_id))[9]} Рассылка', callback_data=Menu_callback(menu="newsletter").pack()),
        ],

        [
            types.InlineKeyboardButton(
                text='📜 Показать текст', callback_data=Menu_callback(menu="show_text").pack()),
        ],

        [
            types.InlineKeyboardButton(text=ButtonTexts.BACK, callback_data=Menu_callback(menu="menu").pack())
        ]
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def k_private_menu():
    kb = [
        [
            types.InlineKeyboardButton(
                text=ButtonTexts.SUBSCRIBE, callback_data=Menu_callback(menu="subscribe").pack()),
            types.InlineKeyboardButton(
                text=ButtonTexts.REPLENISH, callback_data=Menu_callback(menu="replenish").pack()),
        ],

        [
            types.InlineKeyboardButton(
                text=ButtonTexts.BACK, callback_data=Menu_callback(menu="menu").pack()),
        ],
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def k_repl(url):
    kb = [
        [
            types.InlineKeyboardButton(text=ButtonTexts.PAY, url=url)
        ],
        [
            types.InlineKeyboardButton(
                text=ButtonTexts.CANCEL, callback_data=Buy_answer(buy="private_menu").pack())
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def cancel_rep():
    kb = [
        [
            types.InlineKeyboardButton(
                text=ButtonTexts.CANCEL, callback_data=Menu_callback(menu="private_menu").pack())
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def cancel_upl():
    kb = [
        [
            types.InlineKeyboardButton(
                text=ButtonTexts.CANCEL, callback_data=Menu_callback(menu="menu").pack())
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def admin_panel():
    kb = [
        [
            types.InlineKeyboardButton(text='💸 Изменить баланс', callback_data=Menu_callback(menu="change_balance").pack()),
            types.InlineKeyboardButton(text='🌐 Изменить проски', callback_data=Menu_callback(menu="change_proxy").pack()),
        ],
        [
            types.InlineKeyboardButton(text=ButtonTexts.BACK, callback_data=Menu_callback(menu="menu").pack())
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def update_account_method():
    kb = [
        [
            types.InlineKeyboardButton(text='📤 Загрузить сессию', callback_data=Menu_callback(menu="upl_acc_method").pack()),
            types.InlineKeyboardButton(text='📱 Войти номеру', callback_data=Menu_callback(menu="upl_acc_method_2").pack()),
        ],
        [
            types.InlineKeyboardButton(text=ButtonTexts.BACK, callback_data=Menu_callback(menu="menu").pack())
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)

def menu_subscribe():
    kb = [
        [
            types.InlineKeyboardButton(text='КАНАЛ', url=CHANNEL_URL),
        ],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)