import asyncio
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from keyboards.client import Menu_callback, k_work_menu, cancel_in
from data import users

class Text(StatesGroup):
    text = State()

router = Router()

async def message_for_info_user(user_id):
    record = await users.user_profile(user_id)

    text = record[6]
    delay = record[7]
    notifications = record[8]
    newsletter = record[9]

    text = f'''<b>
Смена информации по всем чатам
        
📜Текст:╍╍╍╍╍╍╍╍╍╍╍╍
{text}
╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍

Задержка: ⏰ <code>{delay} мин.</code>
Уведомления: {notifications}
Статус рассылки: {newsletter}
</b>'''

    return text

@router.callback_query(Menu_callback.filter(F.menu == 'text'))
async def text(call: CallbackQuery, callback_data: Menu_callback, state: FSMContext):
    await state.set_state(Text.text)
    await call.message.edit_text('Введите ваш новый текст:', reply_markup=cancel_in())

@router.message(Text.text)
async def form_text(message: Message, state: FSMContext):
    text = str(message.text)
    user_id = message.from_user.id
    
    await users.update_text(user_id, text)

    await state.clear()

    text = await message_for_info_user(user_id)

    await message.answer('Текст изменен!')
    kb = await k_work_menu(user_id)
    await message.answer(text, reply_markup=kb)


@router.callback_query(Menu_callback.filter(F.menu == 'cancel'))
async def cmd_cancel(call: CallbackQuery, callback_data: Menu_callback, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        text="Действие отменено",
    )

    user_id = call.from_user.id
    text = await message_for_info_user(user_id)

    kb = await k_work_menu(user_id)
    await call.message.answer(text, reply_markup=kb)
