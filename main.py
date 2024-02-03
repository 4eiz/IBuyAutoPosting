import asyncio
import logging
from app.work_menu import menu_wk, text_edit, newsletter, send_notifications, show_text, delay
from app.private_menu import menu_pr, subscribe
from app.money import replenishment
from app.admin_menu import admin
from app import general_hd, upload_account
from aiogram import Bot, Dispatcher

from config import bot



async def start():
    dp = Dispatcher()

    dp.include_routers(
        general_hd.router,
        text_edit.router,
        newsletter.router,
        send_notifications.router,
        delay.router,
        show_text.router,
        menu_wk.router,
        menu_pr.router,
        subscribe.router,
        replenishment.router,
        upload_account.router,
        admin.router,
    )

    logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start())
