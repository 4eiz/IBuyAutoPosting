from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.client import Menu_callback, k_private_menu
from app.private_menu.subscribe import message_for_info_user
from data import users

router = Router()

 
@router.callback_query(Menu_callback.filter(F.menu == 'private_menu'))
async def work_menu(call: CallbackQuery, callback_data: Menu_callback):
    user_id = call.from_user.id
    user_name = call.from_user.first_name


    text = await message_for_info_user(user_id, user_name)

    kb = k_private_menu()
    await call.message.edit_text(text, reply_markup=kb)