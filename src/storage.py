import sqlite3 as sq
from src.utils import log


class Storage:
    def __init__(self, path:str, dev=False):
        """
        :param path: Path of database.
        :param dev: Dev version. If True, test database will be connected.
        """
        if not dev:
            self.conn = sq.connect(path, autocommit=False)
        else:
            self.conn = sq.connect(".\\data.db", autocommit=False)
        self.cursor = self.conn.cursor()

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
                            'date TEXT UNIQUE,'
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
            self.cursor.execute(f"insert into {name} (date,value) values (?, ?)", (date, value))
        else:
            self.cursor.execute(f"insert into {name} (date) values (?)", (date,))
        self.conn.commit()

    @log
    def edit_date(self, name, old_date, new_date):
        self.cursor.execute(f"update {name} set date=? where date=?", (new_date, old_date))
        self.conn.commit()

    @log
    def edit_value(self, name, date, value: int):
        self.cursor.execute(f"update {name} set value=? where date=?", (date, value))
        self.conn.commit()

    @log
    def remove(self, name, date):
        self.cursor.execute(f"select * from {name} where date=?", (date,))
        if not self.cursor.fetchall():
            return 101
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

    def admin_execute(self, cmd:str):
        self.cursor.execute(cmd)
        return self.cursor.fetchall()

if __name__ == '__main__':
    storage = Storage('../data.db')
    storage.admin_execute("update b set value=2024-01-02 where date=2024-01-01")