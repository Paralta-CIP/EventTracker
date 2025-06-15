__program__ = 'EventRecorder'
__author__ = 'Paralta'
__version__ = '1.1'
__dev__ = True

import os
import traceback
import logging
from datetime import date
from re import match
from src import plot
from src.settings import Settings
from src.storage import Storage
from src.utils import printc, view_format, operation, get_data
from src.stat import avg_freq, avg_int

# TODO: Check legality of date.
# TODO: Automatically delete log.

# Initialization
current_path = os.path.dirname(__file__)
os.chdir(current_path)
os.system('')
logging.basicConfig(filename=f'./{date.today()}.log', level=logging.INFO, format="%(message)s")
settings = Settings()
path = settings.read_one_setting('path')
storage = Storage(path, dev=__dev__)

print(f'{__program__} (version {__version__}) launched.')
print('Type "help" for command list.')

# Main loop
while True:
    cmd = input('>>').strip().lower()
    logging.info(f"Input : {cmd}")

    try:
        if cmd.startswith('new event'):
            operation(cmd, r'^new event\s+([A-Za-z_]\w*)$', "Create new event %?", storage.new_event)

        elif cmd.startswith('delete event'):
            operation(cmd, r'^delete event\s+([A-Za-z_]\w*)$', "Delete event %?", storage.delete_event)

        elif cmd.startswith('rename event'):
            operation(cmd, r'^rename event\s+([A-Za-z_]\w*)\s+([A-Za-z_]\w*)$', "Rename event % to %?", storage.rename_event)

        elif cmd == 'all event':
            for i in storage.all_event():
                print(i)

        elif cmd.startswith('add'):
            if not match(r'.*\b\d{4}-\d{2}-\d{2}\b', cmd):
                printc('yellow', 'Incorrect date format. Should be like 2024-03-01.')
                continue
            operation(cmd, r'^add\s+([A-Za-z_]\w*)\s+(\d{4}-\d{2}-\d{2})$', "Add % for %?", storage.add)

        elif cmd.startswith('edit'):
            if not match(r'.*\b\d{4}-\d{2}-\d{2}\b', cmd):
                printc('yellow', 'Incorrect date format. Should be like 2024-03-01.')
                continue
            operation(cmd, r'^edit\s+([A-Za-z_]\w*)\s+(\d{4}-\d{2}-\d{2})\s+(\d{4}-\d{2}-\d{2})$',
                      "Edit % for % with %?", storage.edit_date)

        elif cmd.startswith('remove'):
            if not match(r'.*\b\d{4}-\d{2}-\d{2}\b', cmd):
                printc('yellow', 'Incorrect date format. Should be like 2024-03-01.')
                continue
            operation(cmd, r'^remove\s+([A-Za-z_]\w*)\s+(\d{4}-\d{2}-\d{2})$', "Remove % for %?", storage.remove)

        elif cmd.startswith('view'):
            data, name = get_data(cmd, 'view', storage.get)
            if data:
                view_format(data)
            elif name:
                printc('orange', 'Data is empty.')

        elif cmd.startswith('avg freq'):
            data, name = get_data(cmd, 'avg freq', storage.get)
            if data:
                result = avg_freq(data)
                print(f'Event "{name}" occurs {result} times a month on average.')
            elif name:
                printc('orange', 'Data is empty.')

        elif cmd.startswith('avg int'):
            data, name = get_data(cmd, 'avg int', storage.get)
            if data:
                result = avg_int(data)
                print(f'Event "{name}" occurs every {result} days on average.')
            elif name:
                printc('orange', 'Data is empty.')

        elif cmd.startswith('plot freq'):
            data, name = get_data(cmd, 'plot freq', storage.get)
            if data:
                plot.plot_freq(data, name)
            elif name:
                printc('orange', 'Data is empty.')

        elif cmd.startswith('plot int'):
            data, name = get_data(cmd, 'plot int', storage.get)
            if data:
                plot.plot_int(data, name)
            elif name:
                printc('orange', 'Data is empty.')

        elif cmd == 'help':
            language = settings.read_one_setting('language')
            if language == 'English':
                with open(r"help\English.txt", encoding='utf-8') as f:
                    print(f.read().replace('<cyan>', '\033[38;5;116m').replace('<lime>', '\033[38;5;83m')
                          .replace('<end>', '\033[0m'))
            elif language == 'Chinese':
                with open(r"help\Chinese.txt", encoding='utf-8') as f:
                    print(f.read().replace('<cyan>', '\033[38;5;116m').replace('<end>', '\033[0m'))

        elif cmd == 'settings':
            current_settings = settings.read_settings()
            print("Current settings:")
            for cmd in current_settings:
                print(f" - {cmd[0]} : {cmd[1]}")
            change = input('Change the settings (like "language=English", press enter to exit):')
            if not change:
                continue
            else:
                matched = match(r'^(\w+)\s*=\s*(\w+)$', change)
                setting, value = matched.groups()
                try:
                    settings.set_settings(setting, value)
                except Exception as e:
                    printc('red', traceback.format_exc())
                    logging.error(traceback.format_exc())
                    printc('red', 'Failed to change settings.')
                else:
                    if setting == 'path':
                        storage = Storage(value)
                    printc('green', 'Settings changed.')

        elif cmd == 'exit':
            print(f'{__program__} now exits.')
            storage.end()
            break

        else:
            printc('yellow', 'Unknown command.')

    except Exception as err:
        text = str(err)
        if text.startswith("no such table"):
            printc('red', "No such event.")
        elif text.endswith("already exists"):
            printc('red', "Event already exists.")
        elif text.startswith("UNIQUE"):
            printc('red', "Date already exists.")
        elif text.startswith("there is already"):
            printc('red', "Event with this name already exists.")
        else:
            printc('orange', err)
            printc('red', 'Something went wrong. Please send the log file to the developer.')
        logging.error(traceback.format_exc().strip())
        storage.undo()
