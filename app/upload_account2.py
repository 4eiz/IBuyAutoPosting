import os, random

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from keyboards.client import Menu_callback, k_work_menu, cancel_upl, k_menu
from data import chats, users, admin
from config import API_ID, API_HASH

from pyrogram import Client, filters
from pyrogram.errors import (
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)



class Acc(StatesGroup):
    number = State()
    code = State()
    chats_acc = State()



router = Router()





def get_random_proxy():
    proxies = admin.get_proxies()
    if proxies:
        proxy = random.choice(proxies)
    parts = proxy.split("@")
    login_pass = parts[0].split(":")
    login = login_pass[0]
    password = login_pass[1] if len(login_pass) > 1 else ""
    ip_port = parts[1].split(":")
    ip = ":".join(ip_port[:-1])
    port = ip_port[-1]

    PROXY = {
        "scheme": "socks5",
        "hostname": ip,
        "port": int(port),
        "username": login,
        "password": password
    }

    return PROXY



@router.callback_query(Menu_callback.filter(F.menu == 'upl_acc_method_2'))
async def update_account(call: CallbackQuery, callback_data: Menu_callback, state: FSMContext):
    await state.set_state(Acc.number)
    await call.message.edit_text('<b>Введите номер телефона:</b>', reply_markup=cancel_upl())


@router.message(Acc.number)
async def set_number(message: Message, state: FSMContext):
    user_id = message.from_user.id
    phone_number = message.text
    new_file_id = await chats.maxID()+1
    filename = f'{user_id}_{new_file_id}.session'

    destination_folder = os.path.abspath(f'app/posting/{str(user_id)}')

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    path = f"app/posting/{user_id}/{filename[:-8]}"
    print('path', path)
    proxy = get_random_proxy()
    client = Client(path, API_ID, API_HASH, proxy=proxy)
    await client.connect()
    try:
        code = await client.send_code(phone_number)
        print('Отправка')
    except (PhoneNumberInvalid):
        await message.answer('<b>🚫 Номер некорректный</b>')
        return

    await message.answer('<b>Введите код:</b>', reply_markup=cancel_upl())

    await state.update_data(filename=filename, phone_number=phone_number, client=client, code=code)
    await state.set_state(Acc.code)


@router.message(Acc.code)
async def set_code(message: Message, state: FSMContext):

    user_id = message.from_user.id
    phone_code = message.text

    user_data = await state.get_data()
    filename = user_data.get('filename')
    phone_number = user_data.get('phone_number')
    client = user_data.get('client')
    code = user_data.get('code')

    
    try:
        await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        await client.disconnect()
    except (PhoneCodeInvalid):
        await message.answer('<b>❌ Код подтверждения неверный</b>')
        return


    record = await users.user_profile(user_id)
    amount = record[2] + 1
    await users.update_accounts(user_id, amount)

    await message.answer('<b>Введите чаты: </b>')
    await state.set_state(Acc.chats_acc)



@router.message(Acc.chats_acc)
async def set_chats(message: Message, state: FSMContext):
    user_id = message.from_user.id

    chatss = [chat.strip() for chat in message.text.split('\n') if chat.strip()]
    chat_list = []
    chat_list.extend(chatss)

    amount = len(chatss)
    record = await users.user_profile(user_id)
    amount = record[3] + amount

    await users.update_chats(user_id, amount)

    user_data = await state.get_data()
    max_id = user_data.get('max_id')
    filename = user_data.get('filename')

    await chats.add_account(max_id, user_id, filename, chatss)

    await message.answer("<b>Аккаунт успешно добавлен.</b>")
    await message.answer(f'👋 Здравствуйте, {message.from_user.first_name}!\n\n'
                         'Вы сейчас находитесь в главном меню.', reply_markup=k_menu())

    await state.clear()

