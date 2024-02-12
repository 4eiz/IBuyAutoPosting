import aiosqlite
import pickle
import asyncio


async def maxID():
    try:
        async with aiosqlite.connect('data/base/base.db') as db:
            cursor = await db.execute("SELECT MAX(id) FROM accounts;")
            records = await cursor.fetchone()

            if records[0] is None:
                return 0
            else:
                print(records[0])
                return records[0]

    except aiosqlite.Error as error:
        print("Не удалось выбрать данные из таблицы.", error)
        return 0
    finally:
        print("Соединение с SQLite закрыто")

async def main():
    await maxID()

if __name__ == "__main__":
    asyncio.run(main())



async def add_account(max_id, user_id, account_name, chats):
    db = None  # Объявите переменную db заранее

    try:
        db = await aiosqlite.connect('data/base/base.db')
        serialized_chats = pickle.dumps(chats)
        insert_query = "INSERT INTO accounts (id, user_id, account_name, chats) VALUES (?, ?, ?, ?);"
        await db.execute(insert_query, (max_id, user_id, account_name, serialized_chats))
        await db.commit()
        print(f"Аккаунт для пользователя {user_id} успешно добавлен.")

    except aiosqlite.Error as error:
        print("Не удалось добавить новую запись в таблицу.", error)
    finally:
        if db:
            try:
                await db.close()
            except aiosqlite.Error as close_error:
                print("Ошибка при закрытии соединения.", close_error)


async def update_account_chats(account_name, new_chats):
    db = None

    try:
        db = await aiosqlite.connect('data/base/base.db')
        serialized_chats = pickle.dumps(new_chats)
        update_query = "UPDATE accounts SET chats = ? WHERE account_name = ?;"
        await db.execute(update_query, (serialized_chats, account_name))
        await db.commit()
        print(f"Список чатов для аккаунта {account_name} успешно обновлен.")

    except aiosqlite.Error as error:
        print("Не удалось обновить список чатов.", error)
    finally:
        if db:
            try:
                await db.close()
            except aiosqlite.Error as close_error:
                print("Ошибка при закрытии соединения.", close_error)


async def get_chats(acc):
    db = await aiosqlite.connect('data/base/base.db')

    try:
        select_query = "SELECT chats FROM accounts WHERE account_name=?;"
        cursor = await db.execute(select_query, (acc,))
        result = await cursor.fetchone()

        if result:
            # Десериализуем байты в список чатов
            chats = pickle.loads(result[0])
            return chats
        else:
            print(f"Нет записей для пользователя {acc}.")
            return []

    except aiosqlite.Error as error:
        print("Не удалось выбрать данные из таблицы.", error)
    finally:
        await db.close()

