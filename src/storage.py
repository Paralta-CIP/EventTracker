import sqlite3 as sq


class Storage:
    def __init__(self):
        self.conn = sq.connect('../data.db')
        self.cursor = self.conn.cursor()

    def end(self):
        self.cursor.close()
        self.conn.close()

    def new_event(self, name):
        self.cursor.execute(f'create table {name} (id integer primary key AUTOINCREMENT,'
                            'date TEXT,'
                            'value integer)')
        self.conn.commit()

    def delete_event(self, name):
        self.cursor.execute(f'drop table {name}')
        self.conn.commit()

    def rename_event(self, old_name, new_name):
        self.cursor.execute(f'alter table {old_name} rename to {new_name}')
        self.conn.commit()

    def add(self, name, date, value: int = None):
        if value:
            self.cursor.execute(f"insert into {name} (date,value) values (?,?)", (date, value))
        else:
            self.cursor.execute(f"insert into {name} (date) values (?)", (date,))
        self.conn.commit()

    def edit_date(self, name, old_date, new_date):
        self.cursor.execute(f"update {name} set date=? where date=?", (old_date, new_date))
        self.conn.commit()

    def edit_value(self, name, date, value: int):
        self.cursor.execute(f"update {name} set value=? where date=?", (date, value))
        self.conn.commit()

    def remove(self, name, date):
        self.cursor.execute(f"delete from {name} where date=?", (date,))
        self.conn.commit()

    def all_event(self):
        self.cursor.execute("select name from sqlite_master where type='table'")
        value = [i[0] for i in self.cursor.fetchall()]
        value.pop(0)
        return value

    def get(self, name, *, date_start=None, date_end=None):
        if date_start and date_end:
            self.cursor.execute(f"select date,value from {name} "
                                "where date(date) >= date(?) and date(date) <= date(?) "
                                "order by date(date)", (date_start, date_end))
            return self.cursor.fetchall()
        elif date_start and not date_end:
            self.cursor.execute(f"select date,value from {name} "
                                "where date(date) >= date(?) "
                                "order by date(date)", (date_start,))
            return self.cursor.fetchall()
        elif not date_start and date_end:
            self.cursor.execute(f"select date,value from {name}  "
                                "where date(date) <= date(?) "
                                "order by date(date)", (date_end,))
            return self.cursor.fetchall()
        else:
            self.cursor.execute(f"select date,value from {name} order by date(date)")
            return self.cursor.fetchall()
