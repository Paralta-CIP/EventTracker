from typing import Literal, Callable
from re import match, sub
import traceback


COLORS = {'grey':'249', 'red':'203', 'orange':'208', 'yellow':'227', 'green':'34', 'lime':'119', 'blue':'39',
          'cyan':'86', 'purple':'99'}
PATTERNS = {'none':'', 'line':'\033[4m', 'inv':'\033[7m'}

def printc(color: int | Literal['grey', 'red', 'orange', 'yellow', 'green', 'lime', 'blue', 'cyan', 'purple'], *text,
           pat: Literal['none', 'line', 'inv'] = 'none', end='\n'):
    match color:
        case str():
            print('\033[38;5;' + COLORS[color] + 'm' + PATTERNS[pat], end='')
        case int():
            print('\033[38;5;' + str(color) + 'm' + PATTERNS[pat], end='')
        case _:
            raise ValueError("Wrong 'color' type")
    if text:
        for t in text[:-1]:
            print(t, end=' ')
        print(text[-1], end='')
        print('\033[0m', end=end)

def view_format(data):
    if data:
        if data[0][1]:
            for i in data:
                print(i[0], i[1])
        else:
            for i in data:
                print(i[0])

def operation(cmd:str, pattern:str, info:str, query:Callable):
    """
    :param info: Use % to replace args. Omit '(Y/Enter)'.
    """
    matched = match(pattern, cmd)
    if not matched:
        printc('yellow', 'Incorrect command.')
        return
    args = matched.groups()
    for a in args:
        info = sub(r"%", f"'{a}'", info, count=1)
    print(info, "(Y/Enter)")
    c = input('>').upper()
    if c == 'Y':
        query(*args)
        printc('lime', 'Successful.')

def get_data(cmd:str, cmd_name:str, get_method:Callable):
    matched = match(r'^'+cmd_name+r'\s+(\w+)$', cmd)
    if matched:
        name = matched.group(1)
        return get_method(name), name
    else:
        matched = match(r'^'+cmd_name+r'\s+(\w+)\s+(\d{4}-\d{2}-\d{2}|-)\s+(\d{4}-\d{2}-\d{2}|-)$', cmd)
        if matched:
            name, date_start, date_end = matched.groups()
            return get_method(name, date_start, date_end), name
        else:
            printc('yellow', 'Incorrect command.')
    return None, None
