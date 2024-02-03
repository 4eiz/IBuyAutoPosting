import aiosqlite
import pickle


async def maxID():
    try:
        async with aiosqlite.connect('data/base/base.db') as db:
            cursor = await db.execute("SELECT MAX(id) FROM users;")
            records = await cursor.fetchone()
            return records[0] if records[0] is not None else 0

    except aiosqlite.Error as error:
        print("Не удалось выбрать данные из таблицы.", error)

async def new(users_id, balance, accounts, chats, subscribe, time_sub, text, delay, notifications, newsletter, messages, active_mailings):
    try:
        async with aiosqlite.connect('data/base/base.db') as db:
            insert_query = '''INSERT INTO users (id, balance, accounts, chats, subscribe, time_sub, text, delay, notifications, newsletter, messages, active_mailings)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
            data_tuple = (users_id, balance, accounts, chats, subscribe, time_sub, text, delay, notifications, newsletter, messages, active_mailings)
            await db.execute(insert_query, data_tuple)
            await db.commit()
            print('Запись успешно добавлена.')

    except aiosqlite.Error as error:
        print("Ошибка при подключении к SQlite", error)

async def check_id_in_database(user_id):
    try:
        async with aiosqlite.connect('data/base/base.db') as db:
            cursor = await db.execute("SELECT EXISTS(SELECT 1 FROM users WHERE id = ?);", (user_id,))
            result = await cursor.fetchone()
            return "+" if result[0] else "-"

    except aiosqlite.Error as error:
        print("Ошибка при подключении к SQLite", error)
        return "ошибка"

async def user_profile(user_id):
    try:
        async with aiosqlite.connect('data/base/base.db') as db:
            select_query = "SELECT * FROM users WHERE id=?;"
            cursor = await db.execute(select_query, (user_id,))
            record = await cursor.fetchall()
            return record[0]

    except aiosqlite.Error as error:
        print("Не удалось выбрать данные из таблицы.", error)

async def update_text(user_id, new_text):
    try:
        async with aiosqlite.connect('data/base/base.db') as db:
            update_query = "UPDATE users set text=? WHERE id=?;"
            await db.execute(update_query, (new_text, user_id,))
            await db.commit()
            print("Запись", user_id, "успешна обновлена.")

    except aiosqlite.Error as error:
        print("Не удалось выбрать данные из таблицы.", error)

async def update_notifications(user_id, notifications):
    try:
        async with aiosqlite.connect('data/base/base.db') as db:
            update_query = "UPDATE users set notifications=? WHERE id=?;"
            await db.execute(update_query, (notifications, user_id,))
            await db.commit()
            print("Запись", user_id, "успешна обновлена.")

    except aiosqlite.Error as error:
        print("Не удалось выбрать данные из таблицы.", error)



async def update_delay(user_id, delay):
    try:
        async with aiosqlite.connect('data/base/base.db') as db:
            update_query = "UPDATE users set delay=? WHERE id=?;"
            await db.execute(update_query, (delay, user_id,))
            await db.commit()
            print("Запись", user_id, "успешна обновлена.")

    except aiosqlite.Error as error:
        print("Не удалось выбрать данные из таблицы.", error)



async def update_sub(user_id, balance, sub_id, time_sub):
    try:
        async with aiosqlite.connect('data/base/base.db') as db:
            update_query = "UPDATE users SET balance=?, subscribe=?, time_sub=? WHERE id=?;"
            await db.execute(update_query, (balance, sub_id, time_sub, user_id,))
            await db.commit()
            print(f"Подписка пользователя с ID {user_id} успешно обновлена на {sub_id}.")

    except aiosqlite.Error as error:
        print("Ошибка при обновлении подписки пользователя:", error)



async def update_time_sub(user_id, time_sub):
    try:
        async with aiosqlite.connect('data/base/base.db') as db:
            update_query = "UPDATE users SET time_sub=? WHERE id=?;"
            await db.execute(update_query, (time_sub, user_id,))
            await db.commit()

    except aiosqlite.Error as error:
        print("Ошибка при обновлении времени подписки пользователя:", error)


async def set_free(user_id, sub_id, time_sub):
    try:
        async with aiosqlite.connect('data/base/base.db') as db:
            update_query = "UPDATE users SET subscribe=?, time_sub=? WHERE id=?;"
            await db.execute(update_query, (sub_id, time_sub, user_id,))
            await db.commit()
            print(f"Подписка пользователя с ID {user_id} успешно обновлена на {sub_id}.")

    except aiosqlite.Error as error:
        print("Ошибка при обновлении подписки пользователя:", error)


async def update_balance(user_id, balance):
    try:
        async with aiosqlite.connect('data/base/base.db') as db:
            update_query = "UPDATE users SET balance=? WHERE id=?;"
            await db.execute(update_query, (balance, user_id,))
            await db.commit()

    except aiosqlite.Error as error:
        print("Ошибка при пополнении баланса пользователя:", error)


async def update_messages(user_id, amount):
    try:
        async with aiosqlite.connect('data/base/base.db') as db:
            update_query = "UPDATE users SET messages=? WHERE id=?;"
            await db.execute(update_query, (amount, user_id,))
            await db.commit()

    except aiosqlite.Error as error:
        print("Ошибка при обновлении количества сообщений пользователя:", error)


async def update_newsletter(user_id, newsletter):
    try:
        async with aiosqlite.connect('data/base/base.db') as db:
            update_query = "UPDATE users SET newsletter=? WHERE id=?;"
            await db.execute(update_query, (newsletter, user_id,))
            await db.commit()

    except aiosqlite.Error as error:
        print("Ошибка при обновлении рассылки пользователя:", error)


async def update_active_mailings(user_id, amount):
    try:
        async with aiosqlite.connect('data/base/base.db') as db:
            update_query = "UPDATE users SET active_mailings=? WHERE id=?;"
            await db.execute(update_query, (amount, user_id,))
            await db.commit()

    except aiosqlite.Error as error:
        print("Ошибка при обновлении активных рассылок пользователя:", error)


async def update_accounts(user_id, amount):
    try:
        async with aiosqlite.connect('data/base/base.db') as db:
            update_query = "UPDATE users SET accounts=? WHERE id=?;"
            await db.execute(update_query, (amount, user_id,))
            await db.commit()

    except aiosqlite.Error as error:
        print("Ошибка при обновлении количества аккаунтов пользователя:", error)

async def update_chats(user_id, amount):
    try:
        async with aiosqlite.connect('data/base/base.db') as db:
            update_query = "UPDATE users SET chats=? WHERE id=?;"
            await db.execute(update_query, (amount, user_id,))
            await db.commit()

    except aiosqlite.Error as error:
        print("Ошибка при обновлении количества чатов пользователя:", error)

