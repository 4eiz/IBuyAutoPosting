from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from keyboards.client import Menu_callback, k_menu2, cancel_upl
from data import admin

class Admin(StatesGroup):
    proxy = State()

router = Router()


@router.callback_query(Menu_callback.filter(F.menu == 'change_proxy'))
async def change_proxy(call: CallbackQuery, callback_data: Menu_callback, state: FSMContext):
    await state.set_state(Admin.proxy)
    await call.message.edit_text('<b>Введите новый прокси:</b>', reply_markup=cancel_upl())



@router.message(Admin.proxy)
async def result(message: Message, state: FSMContext):
  
    proxy = message.text
    print(proxy)
    admin.update_proxy(proxy)
    
    await message.answer('<b>Прокси успешно изменен!</b>')
    await message.answer(f'<b>👋 Здравствуйте, {message.from_user.first_name}!\n\n'
                        'Вы сейчас находитесь в главном меню.</b>', reply_markup=k_menu2())

    await state.clear()



    
      
    