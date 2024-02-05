import asyncio
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from keyboards.client import Menu_callback, k_menu2, cancel_upl, admin_panel
from data import users, admin

class Admin(StatesGroup):
    id = State()
    balance = State()

router = Router()

def text():
    users = admin.get_users_count()
    messages = admin.get_totals()
    
    text = f'''<b>
👥 Количество юзеров: <code>{users}</code>
📨 Количество сообщений: <code>{messages[0]}</code>
</b>
'''
    return text


@router.callback_query(Menu_callback.filter(F.menu == 'admin'))
async def admin_menu(call: CallbackQuery, callback_data: Menu_callback):
    await call.message.edit_text(text(), reply_markup=admin_panel())



@router.callback_query(Menu_callback.filter(F.menu == 'change_balance'))
async def change_balance(call: CallbackQuery, callback_data: Menu_callback, state: FSMContext):
    await state.set_state(Admin.id)
    await call.message.edit_text('<b>Введите айди юзера:</b>', reply_markup=cancel_upl())

@router.message(Admin.id)
async def change_balance2(message: Message, state: FSMContext):
    id = int(message.text)
    user_id = message.from_user.id

    await state.update_data(id=id)
    
    await message.answer('<b>Введите новый баланс:</b>', reply_markup=cancel_upl())

    await state.set_state(Admin.balance)


@router.message(Admin.balance)
async def result1(message: Message, state: FSMContext):

    user_data = await state.get_data()
    id = user_data.get('id')  
    balance = int(message.text)

    await users.update_balance(id, balance)
    
    await message.answer('<b>Баланс успешно изменен!</b>')
    await message.answer(f'<b>👋 Здравствуйте, {message.from_user.first_name}!\n\n'
                        'Вы сейчас находитесь в главном меню.</b>', reply_markup=k_menu2())

    await state.clear()
