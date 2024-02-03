from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.client import Menu_callback, k_work_menu, cancel_in
from data.users import user_profile
from app.work_menu.text_edit import message_for_info_user

router = Router()

@router.callback_query(Menu_callback.filter(F.menu == 'show_text'))
async def show_text(call: CallbackQuery, callback_data: Menu_callback):
    user_id = call.from_user.id

    record = await user_profile(user_id)
    my_text = str(record[6])

    text = await message_for_info_user(user_id)

    await call.message.edit_text(my_text, reply_markup=cancel_in())

@router.callback_query(Menu_callback.filter(F.menu == 'cancel'))
async def work_menu(call: CallbackQuery, callback_data: Menu_callback):
    user_id = call.from_user.id
    text = await message_for_info_user(user_id)

    await call.message.edit_text(text, reply_markup=cancel_in())
