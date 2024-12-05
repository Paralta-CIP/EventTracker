__program__ = 'EventRecorder'
__author__ = 'Paralta'
__version__ = '1.1'

import os
import traceback
from src import plot, settings, storage
from src.utils import printc, view_format


# Initialization
current_path = os.path.dirname(__file__)
os.chdir(current_path)
os.system('')
print(f'{__program__} (version {__version__}) launched.')

settings = settings.Settings()
storage = storage.Storage()

print("Type 'help' for command list.")

# Main loop
while True:
    s = input('>>').strip().lower()

    try:
        if s.startswith('new event'):
            name = s.removeprefix('new event ')
            if not name:
                printc('yellow', 'Incorrect command.')
                continue
            print(f"Create new event '{name}'? (Y/Enter)")
            c = input('>').upper()
            if c == 'Y':
                storage.new_event(name)
                printc('lime', 'Successful.')

        elif s.startswith('delete event'):
            name = s.removeprefix('delete event ')
            if not name:
                printc('yellow', 'Incorrect command.')
                continue
            print(f"Delete event '{name}'? (Y/Enter)")
            c = input('>').upper()
            if c == 'Y':
                storage.delete_event(name)
                printc('lime', 'Successful.')

        elif s.startswith('rename event'):
            ss = s.removeprefix('rename event ').split()
            if len(ss) != 2:
                printc('yellow', 'Incorrect command.')
                continue
            old_name, new_name = ss[0], ss[1]
            print(f"Rename event '{old_name}' to '{new_name}'? (Y/Enter)")
            c = input('>').upper()
            if c == 'Y':
                storage.rename_event(old_name, new_name)
                printc('lime', 'Successful.')

        elif s.startswith('all event'):
            for i in storage.all_event():
                print(i)

        elif s.startswith('add'):
            ss = s.removeprefix('add ').split()
            if len(ss) == 2:
                name, date = ss[0], ss[1]
                if len(date) != 10:
                    printc('yellow', 'Incorrect date format. Should be like 2024-03-01.')
                else:
                    print(f"add {date} to '{name}'? (Y/Enter)")
                    c = input('>').upper()
                    if c == 'Y':
                        storage.add(name, date)
                        printc('lime', 'Successful.')
            elif len(ss) == 3:
                name, date, value = ss[0], ss[1], int(ss[2])
                if len(date) != 10:
                    printc('yellow', 'Incorrect date format. Should be like 2024-03-01.')
                else:
                    print(f"add {date}({value}) to '{name}'? (Y/Enter)")
                    c = input('>')
                    if c == 'Y' or c == 'y':
                        storage.add(name, date, value)
                        printc('lime', 'Successful.')
            else:
                printc('yellow', 'Incorrect command.')

        elif s.startswith('edit date'):
            ss = s.removeprefix('edit date ').split()
            if len(ss) != 3:
                printc('yellow', 'Incorrect command.')
                continue
            name, old_date, new_date = ss[0], ss[1], ss[2]
            print(f"Change {old_date} in '{name}' to {new_date}? (Y/Enter)")
            c = input('>').upper()
            if c == 'Y':
                storage.edit_date(name, old_date, new_date)
                printc('lime', 'Successful.')

        elif s.startswith('edit value'):
            ss = s.removeprefix('edit value ').split()
            if len(ss) != 3:
                printc('yellow', 'Incorrect command.')
                continue
            name, date, value = ss[0], ss[1], int(ss[2])
            print(f"Set value of {date} in '{name}' to {value}? (Y/Enter)")
            c = input('>').upper()
            if c == 'Y':
                storage.edit_value(name, date, value)
                printc('lime', 'Successful.')

        elif s.startswith('remove'):
            ss = s.removeprefix('remove ').split()
            if len(ss) != 2:
                printc('yellow', 'Incorrect command.')
                continue
            name, date = ss[0], ss[1]
            print(f"Remove {date} in '{name}'? (Y/Enter)")
            c = input('>').upper()
            if c == 'Y':
                storage.remove(name, date)
                printc('lime', 'Successful.')

        elif s.startswith('view'):
            ss = s.removeprefix('view ').split()
            if len(ss) == 1:
                name = ss[0]
                view_format(storage.get(name))
            elif len(ss) == 3:
                name, date_start, date_end = ss[0], ss[1], ss[2]
                if date_start == '-' and date_end != '-':
                    view_format(storage.get(name, date_end=date_end))
                elif date_start != '-' and date_end == '-':
                    view_format(storage.get(name, date_start=date_start))
                elif date_start != '-' and date_end != '-':
                    view_format(storage.get(name, date_start=date_start, date_end=date_end))
                else:
                    printc('yellow', 'Incorrect command.')
            else:
                printc('yellow', 'Incorrect command.')

        elif s.startswith('plot frequency'):
            ss = s.removeprefix('plot frequency ').split()
            if len(ss) == 1:
                name = ss[0]
                plot.plot_freq(storage.get(name), name)
            elif len(ss) == 3:
                name, date_start, date_end = ss[0], ss[1], ss[2]
                if date_start == '-' and date_end != '-':
                    plot.plot_freq(storage.get(name, date_end=date_end), name)
                elif date_start != '-' and date_end == '-':
                    plot.plot_freq(storage.get(name, date_start=date_start), name)
                elif date_start != '-' and date_end != '-':
                    plot.plot_freq(storage.get(name, date_start=date_start, date_end=date_end), name)
                else:
                    printc('yellow', 'Incorrect command.')
            else:
                printc('yellow', 'Incorrect command.')

        elif s.startswith('plot interval'):
            ss = s.removeprefix('plot interval ').split()
            if len(ss) == 1:
                name = ss[0]
                plot.plot_int(storage.get(name), name)
            elif len(ss) == 3:
                name, date_start, date_end = ss[0], ss[1], ss[2]
                if date_start == '-' and date_end != '-':
                    plot.plot_int(storage.get(name, date_end=date_end), name)
                elif date_start != '-' and date_end == '-':
                    plot.plot_int(storage.get(name, date_start=date_start), name)
                elif date_start != '-' and date_end != '-':
                    plot.plot_int(storage.get(name, date_start=date_start, date_end=date_end), name)
                else:
                    printc('yellow', 'Incorrect command.')
            else:
                printc('yellow', 'Incorrect command.')

        elif s == 'help':
            language = settings.read_one_setting('language')
            if language == 'English':
                with open(r"help\English.txt", encoding='utf-8') as f:
                    print(f.read().replace('<cyan>', '\033[38;5;116m').replace('<lime>', '\033[38;5;83m')
                          .replace('<end>', '\033[0m'))
            elif language == 'Chinese':
                with open(r"help\Chinese.txt", encoding='utf-8') as f:
                    print(f.read().replace('<cyan>', '\033[38;5;116m').replace('<end>', '\033[0m'))

        elif s == 'settings':
            current_settings = settings.read_settings()
            for s in current_settings:
                print("Current settings:")
                print(f" - {s[0]} : {s[1]}")
            command = input("Change the settings (likes 'language=English', press enter to exit):")
            if not command:
                continue
            else:
                setting, value = [x.strip() for x in command.split('=')]
                try:
                    settings.set_settings(setting, value)
                except Exception as e:
                    printc('red', traceback.format_exc())
                    printc('red', 'Failed to change settings.')
                else:
                    printc('green', 'Settings changed.')

        elif s == 'exit':
            print(f'{__program__} now exits.')
            storage.end()
            break

        else:
            printc('yellow', 'Unknown command.')

    except Exception as e:
        printc('red', traceback.format_exc())
        printc('red', 'Something went wrong. Please contact the developer.')
