import sqlite3 as sq
import logging
from functools import wraps


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = f"Call : {func.__name__}("
        if len(args) != 1 and not kwargs:
            info += ', '.join(args[1:])
        elif len(args) != 1 and kwargs:
            info += ', '.join(args[1:]) + ', ' + ', '.join(f'{key}={val}' for key, val in kwargs.items())
        elif len(args) == 1 and kwargs:
            info += ', '.join(f'{key}={val}' for key, val in kwargs.items())
        info += ')'
        logging.info(info)
        return func(*args, **kwargs)
    return wrapper

class Storage:
    def __init__(self, path:str, dev=False):
        if not dev:
            self.conn = sq.connect(path, autocommit=False)
        else:
            self.conn = sq.connect(".\\data.db", autocommit=False)
        self.cursor = self.conn.cursor()
        self.cache = False

    @log
    def undo(self):
        self.conn.rollback()

    @log
    def end(self):
        self.cursor.close()
        self.conn.close()

    @log
    def new_event(self, name):
        self.cursor.execute(f'create table {name} (id integer primary key AUTOINCREMENT,'
                            'date TEXT,'
                            'value integer)')
        self.conn.commit()

    @log
    def delete_event(self, name):
        self.cursor.execute(f'drop table {name}')
        self.conn.commit()

    @log
    def rename_event(self, old_name, new_name):
        self.cursor.execute(f'alter table {old_name} rename to {new_name}')
        self.conn.commit()

    @log
    def add(self, name, date, value: int = None):
        if value:
            self.cursor.execute(f"insert into {name} (date,value) values (?,?)", (date, value))
        else:
            self.cursor.execute(f"insert into {name} (date) values (?)", (date,))
        self.conn.commit()

    @log
    def edit_date(self, name, old_date, new_date):
        self.cursor.execute(f"update {name} set date=? where date=?", (old_date, new_date))
        self.conn.commit()

    @log
    def edit_value(self, name, date, value: int):
        self.cursor.execute(f"update {name} set value=? where date=?", (date, value))
        self.conn.commit()

    @log
    def remove(self, name, date):
        self.cursor.execute(f"delete from {name} where date=?", (date,))
        self.conn.commit()

    @log
    def all_event(self):
        self.cursor.execute("select name from sqlite_master where type='table'")
        value = [i[0] for i in self.cursor.fetchall()]
        value.pop(0)
        return value

    @log
    def get(self, name, date_start=None, date_end=None):
        if not date_start and not date_end:
            self.cursor.execute(f"select date,value from {name} order by date(date)")
            return self.cursor.fetchall()
        elif date_start != '-' and date_end != '-':
            self.cursor.execute(f"select date,value from {name} "
                                "where date(date) >= date(?) and date(date) <= date(?) "
                                "order by date(date)", (date_start, date_end))
            return self.cursor.fetchall()
        elif date_start != '-' and date_end == '-':
            self.cursor.execute(f"select date,value from {name} "
                                "where date(date) >= date(?) "
                                "order by date(date)", (date_start,))
            return self.cursor.fetchall()
        elif date_start == '-' and date_end != '-':
            self.cursor.execute(f"select date,value from {name}  "
                                "where date(date) <= date(?) "
                                "order by date(date)", (date_end,))
            return self.cursor.fetchall()
