import sqlite3





def maxID():
    try:
        sqlite_connection = sqlite3.connect('data/base/base.db')
        cursor = sqlite_connection.cursor()

        sqlite_selection_query = "SELECT MAX(id) FROM subscribes;"
        cursor.execute(sqlite_selection_query)
        records = cursor.fetchone()
        cursor.close()
        if records[0] == None:
            return 0
        else:
            print(records[0])
            return records[0]
    except sqlite3.Error as error:
        print("Не удалось выбрать данные из таблицы.", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


async def new(name, price, time_sub):
    try:
        sqlite_connection = sqlite3.connect('data/base/base.db')
        cursor = sqlite_connection.cursor()
        print('База данных подключена.')

        insert_query = '''INSERT INTO subscribes (id, name, price, time)
                            VALUES (?, ?, ?, ?);''' 
        data_tuple = (maxID() + 1, name, price, time_sub)
        cursor.execute(insert_query, data_tuple)
        sqlite_connection.commit()
        print('Запись успешно добавлена.')
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при подключении к SQlite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

base = [
    ('1 нед (5 акк)', 150, 7),
    ('1 мес (5 акк)', 350, 30),
    ('1 нед (10 акк)', 250, 7),
    ('1 мес (10 акк)', 450, 30),
    ('1 нед (30 акк)', 500, 7),
    ('1 мес (30 акк)', 1200, 30),
    ('FREE', 0, 9999999999999)
]


# for i in base:
#     new(i[0], i[1], i[2])



def SelectTable():
    try:
        sqlite_connection = sqlite3.connect('data/base/base.db')
        cursor = sqlite_connection.cursor()
        print('База данных подкючена.')

        sqlite_selection_query = "SELECT * From subscribes;"
        cursor.execute(sqlite_selection_query)
        record = cursor.fetchall()
        cursor.close()
        return record
    except sqlite3.Error as error:
        print("Не удалось выбрать данные из таблицы.", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def select_time_SUB(id):
    try:
        sqlite_connection = sqlite3.connect('data/base/base.db')
        cursor = sqlite_connection.cursor()

        sqlite_selection_query = "SELECT time FROM subscribes WHERE id=?;"
        cursor.execute(sqlite_selection_query, (id,))
        record = cursor.fetchone()
        cursor.close()
        print(record[0])
        return record[0]
    except sqlite3.Error as error:
        print("Не удалось выбрать данные из таблицы.", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def select_sub(id):
    try:
        sqlite_connection = sqlite3.connect('data/base/base.db')
        cursor = sqlite_connection.cursor()

        sqlite_selection_query = "SELECT * FROM subscribes WHERE id=?;"
        cursor.execute(sqlite_selection_query, (id,))
        record = cursor.fetchone()
        cursor.close()
        print(record[0])
        return record[0]
    except sqlite3.Error as error:
        print("Не удалось выбрать данные из таблицы.", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()