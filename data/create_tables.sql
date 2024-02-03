CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    balance REAL,
    accounts INTEGER NOT NULL,
    chats INTEGER NOT NULL,
    subscribe INTEGER,
    time_sub INTEGER,
    text TEXT,
    delay INTEGER NOT NULL,
    notifications TEXT NOT NULL,
    newsletter TEXT NOT NULL,
    messages INTEGER,
    active_mailings INTEGER,
    FOREIGN KEY (subscribe) REFERENCES subscribes(id) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS subscribes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    time INTEGER NOT NULL
);


CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    account_name TEXT NOT NULL,
    chats BLOB
);


