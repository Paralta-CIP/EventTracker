import sqlite3 as sq
from paraltatools import printc

class Storage:
    def __init__(self):
        self.conn = sq.connect(r'data.db')
        self.cursor = self.conn.cursor()

    def end(self):
        self.cursor.close()
        self.conn.close()

    def new_event(self, name):
        self.cursor.execute(f'create table {name} (id integer primary key AUTOINCREMENT,'
                            f'date TEXT,'
                            f'value integer)')
        self.conn.commit()

    def delete_event(self, name):
        self.cursor.execute(f'drop table {name}')
        self.conn.commit()

    def rename_event(self, old_name, new_name):
        self.cursor.execute(f'alter table {old_name} rename to {new_name}')
        self.conn.commit()

    def add(self, name, date, value: int = None):
        if value:
            self.cursor.execute(f"insert into {name} (date,value) values ('{date}',{value})")
        else:
            self.cursor.execute(f"insert into {name} (date) values ('{date}')")
        self.conn.commit()

    def edit_date(self, name, old_date, new_date):
        self.cursor.execute(f"update {name} set date='{new_date}' where date='{old_date}'")
        self.conn.commit()

    def edit_value(self, name, date, value:int):
        self.cursor.execute(f"update {name} set value={value} where date='{date}'")
        self.conn.commit()

    def remove(self, name, date):
        self.cursor.execute(f"delete from {name} where date='{date}'")
        self.conn.commit()

    def all_event(self):
        self.cursor.execute(f"select name from sqlite_master where type='table'")
        value = [i[0] for i in self.cursor.fetchall()]
        value.pop(0)
        return value

    def get(self, name, *, date_start=None, date_end=None):
        if date_start and date_end:
            self.cursor.execute(f"select date,value from {name} "
                                f"where date(date) >= date('{date_start}') and date(date) <= date('{date_end}') "
                                f"order by date(date)")
            return self.cursor.fetchall()
        elif date_start and not date_end:
            self.cursor.execute(f"select date,value from {name} "
                                f"where date(date) >= date('{date_start}') "
                                f"order by date(date)")
            return self.cursor.fetchall()
        elif not date_start and date_end:
            self.cursor.execute(f"select date,value from {name} "
                                f"where date(date) <= date('{date_end}') "
                                f"order by date(date)")
            return self.cursor.fetchall()
        else:
            self.cursor.execute(f"select date,value from {name} order by date(date)")
            return self.cursor.fetchall()

if __name__ == '__main__':
    sto = Storage()
    # sto.add('test3','2024-11-1')

    # sto.cursor.execute('select date(date) from test3 order by date(date)')
    # print(sto.cursor.fetchall())
    print(sto.get('test'))
    sto.end()
