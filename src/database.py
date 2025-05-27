import sqlite3
import pandas as pd
import os
import bcrypt

from .helper import read_query, process_image

class Database():

    def __init__(self):

        if not os.path.exists('db/files/data.db'):
            os.makedirs(os.path.dirname('db/files/data.db'), exist_ok=True)
            with open('db/files/data.db', 'w') as f:
                pass

        with sqlite3.connect('db/files/data.db') as conn:
            cur = conn.cursor()
            cur.execute(read_query("create_users_table"))
            cur.execute(read_query("create_transactions_table"))
            conn.commit()

    ### User Operations

    def load_all_users(self):
        with sqlite3.connect('db/files/data.db') as conn:
            cur = conn.cursor()
            cur.execute(read_query("load_users"))
            rows = cur.fetchall()
            return rows
    
    def check_user_exists(self, username):
        with sqlite3.connect('db/files/data.db') as conn:
            cur = conn.cursor()
            cur.execute(read_query("check_user_exists"), (username,))
            return False if cur.fetchone() is None else True
        
    def get_user_data(self, user_id):
        with sqlite3.connect('db/files/data.db') as conn:
            cur = conn.cursor()
            cur.execute(read_query("get_user_data"), (user_id,))
            row = cur.fetchone()
            if row:
                return {
                    'user_id': row[0],
                    'username': row[1],
                    'fullname': row[2],
                    'password_hash': row[3],
                    'salt': row[4],
                    'photo': row[5]
                }
            return None

    def create_user_profile(self, username, fullname, password, photo):

        photo_bytes = process_image(photo)

        # Hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        with sqlite3.connect('db/files/data.db') as conn:
            cur = conn.cursor()
            # Insert the user into the database
            cur.execute(read_query('insert_users'), (username, fullname, hashed_password, salt, photo_bytes))
            conn.commit()

    def update_user_profile(self, user_id, username, fullname, photo):
        with sqlite3.connect('db/files/data.db') as conn:
            cur = conn.cursor()
            cur.execute(read_query('update_users'), (username, fullname, photo, user_id))
            conn.commit()

    def delete_user_profile(self, user_id):
        with sqlite3.connect('db/files/data.db') as conn:
            cur = conn.cursor()
            # Delete the user from the database
            cur.execute(read_query("delete_transactions"), (user_id,))
            conn.commit()
            cur.execute(read_query("delete_users"), (user_id,))
            conn.commit()

    ### Transaction Operations

    def load_transactions(self, user_id):
        with sqlite3.connect('db/files/data.db') as conn:
            cur = conn.cursor()
            cur.execute(read_query("load_transactions"), (user_id,))
            rows = cur.fetchall()
            return pd.DataFrame(rows, columns=['transaction_id', 'user_id', 'name', 'amount', 'date', 'category', 'type'])

    def insert_transaction(self, user_id, transaction_name, amount, date, category, transaction_type):
        with sqlite3.connect('db/files/data.db') as conn:
            cur = conn.cursor()
            # Insert the transaction into the database
            cur.execute(read_query("insert_transactions"), (user_id, transaction_name, amount, date, category, transaction_type))
            conn.commit()

    def delete_transaction(self, transaction_id):
        with sqlite3.connect('db/files/data.db') as conn:
            cur = conn.cursor()
            cur.execute(read_query('delete_transactions'), (transaction_id,))
            conn.commit()

    def update_transaction(self, user_id, transaction_id, transaction_name, amount, date, category, transaction_type):
        with sqlite3.connect('db/files/data.db') as conn:
            cur = conn.cursor()
            cur.execute(read_query('update_transactions'), (user_id, transaction_name, amount, date, category, transaction_type, transaction_id))
            conn.commit()
