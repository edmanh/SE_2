"""

"""

import sqlite3 as sqlite
from sqlite3 import Error
# from lib.functions import lineno


class SqliteDb:
    conn = None

    def __init__(self, my_db, slogger):
        print(f'db = {my_db}')
        self.slogger = slogger
        self.conn = None
        try:
            conn = sqlite.connect(my_db)
            self.slogger.info('db connected')
            self.conn = conn
            self.cur = conn.cursor()
        except Error as e:
            self.slogger.info('Database probleem: {}'.format(e))
            print('connection error: {}'.format(e))
            quit()

    def close(self):
        self.conn.close()

    def exec_select(self, query):
        print(f'{__name__}-31: query = {query}')
        self.cur.execute(query)
        names = [colname[0] for colname in self.cur.description]
        return names, self.cur.fetchall()

    def exec_update(self, query):
        self.cur.execute(query)
        self.conn.commit()
        return self.cur.rowcount

    def exec_create(self, query):
        self.slogger.info('Creating with: {}'.format(query))
        self.cur.execute(query)
        self.conn.commit()

    def exec_insert(self, query):
        self.cur.execute(query)
        self.conn.commit()
        return self.cur.rowcount

    def exec_check_table(self, table):
        rowcnt = 0
        self.cur.execute('SELECT count(name) FROM sqlite_master WHERE type="table" AND name="{}"'.format(table))
        if self.cur.fetchone()[0] == 1:
            self.cur.execute('SELECT count(*) FROM settings')
            row = self.cur.fetchone()
            rowcnt = row[0]
            return rowcnt
        else:
            return rowcnt

    def exec_executemany(self, query, llist):
        self.cur.executemany(query, llist)
        self.conn.commit()
        return self.cur.rowcount
