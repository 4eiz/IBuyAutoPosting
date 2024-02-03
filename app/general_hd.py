from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.client import k_menu, Menu_callback, k_menu2, menu_subscribe
from data import users

from config import ADMIN, bot, CHANNEL_ID



router = Router()








@router.callback_query(Menu_callback.filter(F.menu == 'menu'))
async def menu(call: CallbackQuery, callback_data: Menu_callback, state: FSMContext):
    try:
        await state.clear()
    except:
        pass
    if call.from_user.id == ADMIN:
        await call.message.edit_text(f'<b>👋 Здравствуйте, {call.from_user.first_name}!\n\n'
                            'Вы сейчас находитесь в главном меню.</b>', reply_markup=k_menu2())
    else:
        await call.message.edit_text(f'<b>👋 Здравствуйте, {call.from_user.first_name}!\n\n'
                            'Вы сейчас находитесь в главном меню.</b>', reply_markup=k_menu())


@router.message(CommandStart())
async def start(message: Message):
    id = message.from_user.id

    sub = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=id)
    if sub.status != 'left':
        start_user = await users.check_id_in_database(id)
        if start_user == '+':
            pass
        else:    
            await users.new(id, 0, 0, 0, 7, 0, '', '15', '🔴', '🔴', 0, 0)

        if message.from_user.id == ADMIN:
            await message.answer(f'<b>👋 Здравствуйте, {message.from_user.first_name}!\n\n'
                                'Вы сейчас находитесь в главном меню.</b>', reply_markup=k_menu2())
        else:
            await message.answer(f'<b>👋 Здравствуйте, {message.from_user.first_name}!\n\n'
                                'Вы сейчас находитесь в главном меню.</b>', reply_markup=k_menu())
            
    else:
        await message.answer('Подпишитесь на канал', reply_markup=menu_subscribe())




