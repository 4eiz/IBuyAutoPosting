from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.client import Menu_callback, k_work_menu
from app.work_menu.text_edit import message_for_info_user
from data.users import user_profile

router = Router()

text2 = '''
<b>🚫 У Вас нет подписки

Чтобы использовать данную функцию бота, оформите подписку.</b>'''

@router.callback_query(Menu_callback.filter(F.menu == 'work_menu'))
async def work_menu(call: CallbackQuery, callback_data: Menu_callback):
    user_id = call.from_user.id
    user_data = await user_profile(user_id)
    sub = user_data[4]

    if sub == 7:
        await call.message.edit_text(text2)
    else:
        text = await message_for_info_user(user_id)
        markup = await k_work_menu(user_id)
        await call.message.edit_text(text, reply_markup=markup)
