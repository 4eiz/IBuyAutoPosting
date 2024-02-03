from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from keyboards.client import Menu_callback, k_work_menu, cancel_in
from data import users
from app.work_menu.text_edit import message_for_info_user


class Delay(StatesGroup):
    text = State()


router = Router()




@router.callback_query(Menu_callback.filter(F.menu == 'delay'))
async def delay(call: CallbackQuery, callback_data: Menu_callback, state: FSMContext):
    await state.set_state(Delay.text)
    await call.message.edit_text('<b>Задержка происходит в минутах, вам нужно указать только цифру \n\nВведите задержку:</b>', reply_markup=cancel_in())


@router.message(Delay.text)
async def delay1(message: Message, state: FSMContext):
    flag = True
    try:
        delay = int(message.text)
        flag = True
    except:
        await message.answer('<b>🚫 Введите число!</b>')

    
    if flag == True:
        user_id = message.from_user.id
        await users.update_delay(user_id, delay)

        await state.clear()

        text = await message_for_info_user(user_id)

        await message.answer('✅ Задержка изменена!')
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