from typing import Literal


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
    if data[0][1]:
        for i in data:
            print(i[0], i[1])
    else:
        for i in data:
            print(i[0])
