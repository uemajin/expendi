CREATE TABLE IF NOT EXISTS
    users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        fullname TEXT NOT NULL,
        password_hs TEXT NOT NULL,
        salt_pw TEXT NOT NULL,
        photo BLOB NOT NULL
    )
