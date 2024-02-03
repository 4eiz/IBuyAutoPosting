import asyncio

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from keyboards.client import Menu_callback, money, Money_callback, anwser_for_buy, Buy_answer, k_private_menu
from data import users, subscribes
from data.subscribes import select_time_SUB

import time
import datetime

class Buying(StatesGroup):
    answer = State()

router = Router()



async def message_for_info_user(user_id, user_name):
    record = await users.user_profile(user_id)

    user_id = record[0]
    balance = record[1]
    accounts = record[2]
    chats = record[3]
    send_messages = record[10]
    active_mailings = record[11]
    subscribe = time_sub_dat(record[5])
    if subscribe == False:
        subscribe = 'Нету'
        await users.set_free(user_id, 7, 9999999999999)
    elif subscribe == 'Нету':
        subscribe = 'Нету'
    



    text = f'''<b>
👥 {user_name}, ваш профиль:

🔖 Ваш ID: <code>{user_id}</code>
💸 Баланс: <code>{balance}$</code>

📋 Аккаунты: <code>{accounts} шт.</code>
💬 Чаты: <code>{chats} шт.</code>
📤 Отправлено сообщений: <code>{send_messages} шт.</code>

🔊 Активные рассылки: <code>{active_mailings} шт.</code>

📅 Подписка активна: <code>{subscribe}</code>
</b>'''
    
    return text

def days_to_seconds(days):
    return days * 24 * 60 * 60

def time_sub_dat(get_time):
    time_now = int(time.time())

    
    middle_time = int(get_time) - time_now


    if middle_time <= 0:
        return False
    elif middle_time >= 1709232395:
        return 'Нету'
    else:
        dt = str(datetime.timedelta(seconds=middle_time))
        return dt


#----------------------------------

@router.callback_query(Menu_callback.filter(F.menu == 'subscribe'))
async def show(call: CallbackQuery, callback_data: Menu_callback):
    text = '<b>⏳ Выберите срок действия подписки: </b>'
    kb = await money()
    await call.message.edit_text(text, reply_markup=kb)


@router.callback_query(Money_callback.filter(F.prefix == 'sub'))
async def buy_subcribe(call: CallbackQuery, callback_data: Money_callback, state: FSMContext):

    price = callback_data.price
    sub_id = callback_data.id
    await state.update_data(price=price, subscription_id=sub_id)

    user_name = call.from_user.first_name
    user_id = call.from_user.id
    record = await users.user_profile(user_id)
    balance = record[1]
    sub_status = await check_sub(user_id)


    if sub_status == 'Нету':
        if balance >= price:
            await call.message.edit_text(text=f"Оплатить подписку {callback_data.name}?", reply_markup=anwser_for_buy())
            await state.set_state(Buying.answer)
        
        else:
            await call.message.edit_text('Недостаточно средств!')
            await state.clear()
            text = await message_for_info_user(user_id, user_name)
            await call.message.answer(text=text, reply_markup=k_private_menu())
    
    elif sub_status == 'Есть':
        await call.message.edit_text('У вас уже имеется подписка!')
        await state.clear()
        text = await message_for_info_user(user_id, user_name)
        await call.message.answer(text=text, reply_markup=k_private_menu())

    else:
        await call.message.edit_text('<b>Ошибка ⚠️</b>')




@router.callback_query(Buy_answer.filter(F.buy == 'yes'))
async def buy_subcribe_answer(call: CallbackQuery, callback_data: Buy_answer, state: FSMContext):
    user_id = call.from_user.id
    user_name = call.from_user.first_name

    user_data = await state.get_data()

    price = user_data.get('price')
    subscription_id = user_data.get('subscription_id')

    record = await users.user_profile(user_id)
    balance = record[1]

    balance = balance - price
    temp = subscribes.select_time_SUB(subscription_id)
    time_sub = int(time.time()) + days_to_seconds(temp)

    print('Айди подписки:', subscription_id)
    print('Время подписки', time_sub)

    await users.update_sub(user_id, balance, subscription_id, time_sub)

    await state.clear()
    text = await message_for_info_user(user_id, user_name)
    kb = k_private_menu()
    await call.message.edit_text(text=text, reply_markup=kb)


#-----------------------------------

async def check_sub(user_id):
    sub = await users.user_profile(user_id)
    sub = sub[4]
    if sub == 7:
        return 'Нету'
    else: 
        return 'Есть'


#-----------------------------------

@router.callback_query(Buy_answer.filter(F.buy == 'cancel'))
async def cmd_cancel(call: CallbackQuery, callback_data: Menu_callback, state: FSMContext):
    
    await state.clear()
    await call.message.edit_text(text="Действие отменено")

    text = '<b>⏳ Выберите срок действия подписки: </b>'
    kb = await money()
    await call.message.answer(text, reply_markup=kb)