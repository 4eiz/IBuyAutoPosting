from pyrogram import Client, errors
import requests
import asyncio
import os
import random


from data import users, chats
from config import API_ID, API_HASH, PROXY, API_TOKEN

async def join_and_send_message(client, link, text, user_id, account):
    try:
        record = await users.user_profile(user_id)

        send_messages = record[10]
        status = record[8]

        if not link.startswith('https://t.me/+'):   
            username = link.split("/")[-1]
            try:
                await client.join_chat(username)
            except:
                pass
            try:
                await client.send_message(username, text)
            except errors.FloodWait as e:
                if status == '🟢':
                    await send(error=f'Спамблок: {account}', user_id=user_id)
                    return
            except UnboundLocalError as e:
                pass
            except Exception as e:
                if status == '🟢':
                    await send(error=f'Ошибка при вступлении в чат: {e} \n\n {account}:{link}', user_id=user_id)
                    return

            amount = send_messages + 1
            await users.update_messages(user_id, amount)
            print(f"Сообщение отправлено в чат {username}")
        else:
            try:
                await client.join_chat(link)
                chat = await client.get_chat(link)
            except:
                chat = await client.get_chat(link)

            try:
                await client.send_message(chat.id, text)
            except errors.FloodWait as e:
                if status == '🟢':
                    await send(error=f'Спамблок: {account}', user_id=user_id)
                    return
            except UnboundLocalError as e:
                pass
            except Exception as e:
                if status == '🟢':
                    await send(error=f'Ошибка при вступлении в чат: {e} \n\n {account}:{link}', user_id=user_id)
                    return

            amount = send_messages + 1
            await users.update_messages(user_id, amount)
            print(f"Сообщение отправлено в чат {link}")
    except Exception as e:
        print(f'Ошибка при отправке сообщения в чат {link}: {e}')



async def spamming(client, user_id, text, account):
    while True:
        status = (await users.user_profile(user_id))[9]
        if status == '🔴':
            try:
                await client.disconnect()
            except:
                pass
            break
        
        chats_list = await chats.get_chats(account)
        for chat_link in chats_list:
            status = (await users.user_profile(user_id))[9]
            if status == '🔴':
                try:
                    await client.disconnect()
                except:
                    pass
                break
            await join_and_send_message(client, chat_link, text, user_id, account)
            delay = (await users.user_profile(user_id))[7]

            for i in range(delay * 60):
                status = (await users.user_profile(user_id))[9]
                if status == '🔴':
                    try:
                        await client.disconnect()
                    except:
                        pass
                    break

                await asyncio.sleep(1)



async def main(account_file, user_id, text, account):
    status = (await users.user_profile(user_id))[8]
    try:
        async with Client(account_file, API_ID, API_HASH, proxy=PROXY) as client:
            await spamming(client, user_id, text, account)

    except errors.Unauthorized as e:
        if status == '🟢':
            await send(error=f'Ошибка сессии: {account}', user_id=user_id)
        
        try:
            os.remove(f'{account_file}.session')
            print(f'Файл сессии {account_file} удален.')
            record = await users.user_profile(user_id)
            amount = record[2] - 1
            await users.update_accounts(user_id, amount)
        except Exception as delete_error:
            print(f'Ошибка при удалении файла сессии {account_file}: {delete_error}')



async def send(error, user_id):
    try:
        with requests.Session() as session:
            session.headers['Accept'] = 'text/html,app/xhtml+xml,app/xml;q=0.9,*/*;q=0.8'
            session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'

            url = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={user_id}'
            session.post(url, data={'text': f"{error}"})
    except Exception as e:
        print(e)


async def start_bot_for_accounts(user_id):
    folder_path = f'app/posting/{user_id}'
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith('.session')]
    text = (await users.user_profile(user_id))[6]
    
    tasks = []
    for account in files:
        delay_minutes = random.randint(1, 5)
        record = (await users.user_profile(user_id))[11]
        amount = record + 1
        await users.update_active_mailings(user_id, amount)

        session_path = os.path.join(folder_path, account)[:-8]
        print('account', account)
        task = asyncio.create_task(main(session_path, user_id, text, account))
        tasks.append(task)

    await asyncio.gather(*tasks)
