from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from keyboards.client import Menu_callback, k_work_menu
from data import users
from app.work_menu.text_edit import message_for_info_user

router = Router()



@router.callback_query(Menu_callback.filter(F.menu == 'send_notifications'))
async def notifications(call: CallbackQuery, callback_data: Menu_callback):
    user_id = call.from_user.id
    record = await users.user_profile(user_id)
    newsletter = record[8]

    if newsletter == '🟢':
        await users.update_notifications(user_id, '🔴')
        newsletter = '🔴'

    elif newsletter == '🔴':
        await users.update_notifications(user_id, '🟢')
        newsletter = '🟢'

    text = await message_for_info_user(user_id)
    markup = await k_work_menu(user_id)
    await call.message.edit_text(text, reply_markup=markup)