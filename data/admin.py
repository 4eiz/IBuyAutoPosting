import sqlite3


def get_totals():
    try:
        sqlite_connection = sqlite3.connect('data/base/base.db')
        cursor = sqlite_connection.cursor()

        query = "SELECT SUM(messages) AS total_messages FROM users;"
        cursor.execute(query)

        totals = cursor.fetchone()

        return totals
    
    except sqlite3.Error as error:
        print("Ошибка при выполнении SQL-запроса:", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")



def get_users_count():
    try:
        sqlite_connection = sqlite3.connect('data/base/base.db')
        cursor = sqlite_connection.cursor()

        sqlite_selection_query = "SELECT COUNT(id) FROM users;"
        cursor.execute(sqlite_selection_query)
        count = cursor.fetchone()[0]

        return count

    except sqlite3.Error as error:
        print("Ошибка при подключении к SQLite", error)
        return None

    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def add_proxy(proxy):
    try:
        sqlite_connection = sqlite3.connect('data/base/base.db')
        cursor = sqlite_connection.cursor()
        print('База данных подключена.')

        insert_query = '''INSERT INTO proxies (id, proxy)
                            VALUES (?, ?);'''
         
        data_tuple = (1, proxy)              
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


def get_proxy():
    try:
        sqlite_connection = sqlite3.connect('data/base/base.db')
        cursor = sqlite_connection.cursor()

        sqlite_selection_query = "SELECT proxy FROM proxies;"
        cursor.execute(sqlite_selection_query)
        count = cursor.fetchone()[0]

        cursor.close()
        return count

    except sqlite3.Error as error:
        print("Ошибка при подключении к SQLite", error)
        return None

    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def update_proxy(proxy):
    try:
        sqlite_connection = sqlite3.connect("data/base/base.db")
        cursor = sqlite_connection.cursor()

        sqlite_selection_query = "UPDATE proxies SET proxy=? WHERE id=1;"
        cursor.execute(sqlite_selection_query, (proxy,))
        sqlite_connection.commit()

    except sqlite3.Error as error:
        print("Не удалось изменить данные из таблицы.", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()