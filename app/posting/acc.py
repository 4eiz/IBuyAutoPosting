import asyncio
from pyrogram import Client

api_id = '14782929'
api_hash = '854102044c03d405a7f82e8c319ac7f7'


async def main():
    async with Client("my_account2", api_id, api_hash) as app:
        await app.send_message("me", "Greetings from **Pyrogram**!")


asyncio.run(main())