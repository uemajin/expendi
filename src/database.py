import sqlite3
import pandas as pd

from .helper import read_query

class Database():

    def __init__(self):
        self.conn = sqlite3.connect('db/files/data.db')
        self.cur = self.conn.cursor()
        self.cur.execute(read_query("create_users_table"))
        self.cur.execute(read_query("create_transactions_table"))
        self.conn.commit()

    ### User Operations

    def load_all_users(self):
        self.cur.execute(read_query("load_users"))
        rows = self.cur.fetchall()
        return rows

    def create_user_profile(self, username, fullname):
        self.cur.execute(read_query('insert_users'), (username, fullname))
        self.conn.commit()

    def update_user_profile(self, user_id, username, fullname):
        self.cur.execute(read_query('update_users'), (username, fullname, user_id))
        self.conn.commit()

    def delete_user_profile(self, user_id):
        self.cur.execute(read_query("delete_users"), (user_id,))
        self.conn.commit()

    ### Transaction Operations

    def load_transactions(self, user_id):
        self.cur.execute(read_query("load_transactions"), (user_id,))
        rows = self.cur.fetchall()
        return pd.DataFrame(rows, columns=['transaction_id', 'user_id', 'name', 'amount', 'date', 'category', 'type'])

    def insert_transaction(self, user_id, transaction_name, amount, date, category, transaction_type):
        self.cur.execute(read_query("insert_transactions"), (user_id, transaction_name, amount, date, category, transaction_type))
        self.conn.commit()

    def delete_transaction(self, transaction_id):
        self.cur.execute(read_query('delete_transactions'), (transaction_id,))
        self.conn.commit()

    def update_transaction(self, user_id, transaction_id, transaction_name, amount, date, category, transaction_type):
        self.cur.execute(read_query('update_transactions'), (user_id, transaction_name, amount, date, category, transaction_type, transaction_id))
        self.conn.commit()
