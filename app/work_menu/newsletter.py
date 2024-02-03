from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.client import Menu_callback, k_work_menu
from data import users
from app.work_menu.text_edit import message_for_info_user

from app.posting import start_bot_for_accounts

router = Router()

@router.callback_query(Menu_callback.filter(F.menu == 'newsletter'))
async def text(call: CallbackQuery, callback_data: Menu_callback):

    user_id = call.from_user.id

    record = await users.user_profile(user_id)
    newsletter = record[9]

    if newsletter == '🟢':
        await users.update_newsletter(user_id, '🔴')
        newsletter = '🔴'
        await users.update_active_mailings(user_id, 0)

        text = await message_for_info_user(user_id)
        markup = await k_work_menu(user_id)
        await call.message.edit_text(text, reply_markup=markup)


    elif newsletter == '🔴':
        await users.update_newsletter(user_id, '🟢')
        newsletter = '🟢'
        
        text = await message_for_info_user(user_id)
        markup = await k_work_menu(user_id)
        await call.message.edit_text(text, reply_markup=markup)
    
        await start_bot_for_accounts(user_id)
