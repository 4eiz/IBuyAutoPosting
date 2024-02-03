import asyncio

from aiocryptopay import AioCryptoPay
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from aiocryptopay import AioCryptoPay, Networks

from keyboards.client import Menu_callback, k_private_menu, k_repl, cancel_rep, Buy_answer
from app.private_menu.subscribe import message_for_info_user
from data.users import update_balance, user_profile
from config import bot, CRYPTO_TOKEN


class CryproBot(StatesGroup):
    sum = State()

router = Router()


@router.callback_query(Menu_callback.filter(F.menu == 'replenish'))
async def rep1(call: CallbackQuery, callback_data: Menu_callback, state: FSMContext):

    text = '<b>🔢 Введите сумму для пополнения баланса</b>'
    id = call.message.message_id

    await state.update_data(del_mes_id=id)
    await call.message.edit_text(text, reply_markup=cancel_rep())
    await state.set_state(CryproBot.sum)
   



@router.message(CryproBot.sum)
async def show(message: Message, state: FSMContext):
    amount = float(message.text.replace(',', '.'))

    user_data = await state.get_data()
    chat_id = message.chat.id
    mes_id = user_data.get('del_mes_id')
    # await Bot.delete_message(self=Bot, chat_id=chat_id, message_id=mes_id)

    

    text = '''<b>⏳ 🔹 Перейдите по ссылке из кнопки для оплаты!

🔄 После успешной оплаты, средства автоматически поступят на ваш баланс. </b>'''



    crypto = AioCryptoPay(token=CRYPTO_TOKEN, network=Networks.MAIN_NET)
    invoice = await crypto.create_invoice(asset='USDT', amount=amount)
    mes_rep = await message.answer(text, reply_markup=k_repl(invoice.bot_invoice_url))
    
    
    await state.update_data(id=invoice.invoice_id)

    timeout = 60 * 5  # 60 минут
    interval = 5

    while timeout > 0:
        await asyncio.sleep(interval)

        # Проверяем статус платежа
        print('Ошибка payment_status')
        payment_status = await check_crypto_bot_invoice(invoice.invoice_id)

        if payment_status == True:
            user_id = message.from_user.id
            
            balance =  await user_profile(user_id)
            balance = float(balance[1]) + amount
            # Платеж выполнен, выполните соответствующие действия
            await update_balance(user_id, balance)

            text_success = f'Баланс пополнен на {amount}'

            await message.answer(text_success)

            user_id = message.from_user.id
            user_name = message.from_user.first_name
            text = await message_for_info_user(user_id, user_name)

            await message.answer(text, reply_markup=k_private_menu())
            await bot.delete_message(chat_id=message.chat.id, message_id=mes_rep.message_id)
            break
        else:
            # Платеж не выполнен, уменьшаем таймаут
            timeout -= interval
            

    if timeout <= 0:
        # Таймаут истек, отменяем платеж и отправляем сообщение об отмене
        await bot.delete_message(chat_id=message.chat.id, message_id=mes_rep.message_id)
        await crypto.delete_invoice(invoice_id=invoice.invoice_id)

    await state.clear()



@router.callback_query(Buy_answer.filter(F.buy == 'private_menu'))
async def cmd_cancel(call: CallbackQuery, callback_data: Buy_answer, state: FSMContext):
    
    crypto = AioCryptoPay(token=CRYPTO_TOKEN, network=Networks.MAIN_NET)
    user_data = await state.get_data()
    invoice = user_data.get('id')

    await crypto.delete_invoice(invoice_id=invoice)
    await call.message.edit_text(
        text="Пополнение отменено",
    )

    user_id = call.from_user.id
    user_name = call.from_user.first_name
    text = await message_for_info_user(user_id, user_name)


    await call.message.edit_text(text, reply_markup=k_private_menu())
    await state.clear()



#-----------------------------


async def check_crypto_bot_invoice(invoice_id: int):
    cryptopay = AioCryptoPay(CRYPTO_TOKEN)
    invoice = await cryptopay.get_invoices(invoice_ids=invoice_id)
    await cryptopay.close()
    if invoice.status == 'paid':
        return True
    else:
        return False