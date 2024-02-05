import os

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from keyboards.client import Menu_callback, update_account_method, cancel_upl, k_menu
from data import chats, users
from main import bot

class Acc(StatesGroup):
    session = State()
    chats = State()



router = Router()


text = '''<b>
Выберите вариант загрузки сессии:
</b>'''

@router.callback_query(Menu_callback.filter(F.menu == 'upl_acc'))
async def file(call: CallbackQuery, callback_data: Menu_callback, state: FSMContext):
    await state.set_state(Acc.session)
    await call.message.edit_text(text, reply_markup=update_account_method())





text_answer = '''
<b>Внимание!
Ваш файл должен отличаться названием от других загруженных вами аккаунтов!

Загрузите ваш файл .session:</b>
'''



@router.callback_query(Menu_callback.filter(F.menu == 'upl_acc_method'))
async def file(call: CallbackQuery, callback_data: Menu_callback, state: FSMContext):
    await state.set_state(Acc.session)
    await call.message.edit_text(text_answer, reply_markup=cancel_upl())


@router.message(Acc.session)
async def upload_account(message: Message, state: FSMContext):

    user_id = message.from_user.id

    file_id = message.document.file_id

    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    file_data = await bot.download_file(file_path)

    destination_folder = os.path.abspath(f'app/posting/{str(user_id)}')

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)


    new_file_id = await chats.maxID()+1


    filename = f"{user_id}_{new_file_id}.session"
    destination_path_to_save = os.path.join(destination_folder, filename)

    with open(destination_path_to_save, 'wb') as destination_file:
        destination_file.write(file_data.read())
    
    record = await users.user_profile(user_id)
    amount = record[2] + 1

    await users.update_accounts(user_id, amount)

    await message.answer('<b>Загрузите ваши чаты для этого аккаунта в формате .txt</b>', parse_mode='HTML', reply_markup=cancel_upl())

    await state.update_data(filename=filename, max_id=new_file_id)
    await state.set_state(Acc.chats)



@router.message(Acc.chats)
async def process_links_file(message: Message, state: FSMContext):
    user_id = message.from_user.id

    if not message.document:
        await message.answer("Пожалуйста, прикрепите файл с расширением .txt, содержащий ссылки.")
        return

    file_id = message.document.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path

    file_data = await bot.download_file(file_path)


    links_data = file_data.read().decode('utf-8')
    links_list = links_data.splitlines()

    user_data = await state.get_data()
    filename = user_data.get('filename')

    max_id = user_data.get('max_id')

    amount = len(links_list)

    record = await users.user_profile(user_id)
    amount += record[3] 


    await users.update_chats(user_id, amount)

    await chats.add_account(max_id, user_id, filename, links_list)

    await message.answer("<b>Аккаунт успешно добавлен.</b>")

    await message.answer(f'👋 Здравствуйте, {message.from_user.first_name}!\n\n'
                         'Вы сейчас находитесь в главном меню.', reply_markup=k_menu())

    await state.clear()



#----------------------------------
    




