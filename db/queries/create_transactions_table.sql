CREATE TABLE IF NOT EXISTS
    transactions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    title TEXT,
    amount FLOAT,
    date DATE,
    category TEXT,
    transaction_type TEXT,
    currency TEXT
    )
