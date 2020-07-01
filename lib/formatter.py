"""

"""
from lib.functions import lineno


class FormatIt(object):
    input = ''      # text to process
    output = []     # result after post processing
    line = ''       # In between buffer
    buffer = []     # Formatted result
    level = 0       # Number of tabs before text
    tab_size = 1    # Size of tabs in spaces
    indent = ''     # Calculated spaces as level * tab_size
    pos = 1         # Start position, passing openings curly bracket
    out = True      # Switch to prevent adding line
    # Reports have null and true as values, not accepted by Python so:
    null = None
    true = True

    def __init__(self, tab_size):
        self.tab_size = tab_size
        pass

    def print_output(self):
        for txt in self.output:
            print(txt)

    def put_line(self, string, clr):
        string.replace('":"', '" : "')
        if len(string) > 0:
            self.indent = self.level * self.tab_size * ' '
            self.buffer.append(self.indent + string)
            if clr:
                self.line = ''
        return

    def reset(self):
        self.output.clear()
        self.buffer.clear()
        self.line = ''

    def format_me(self, txt):
        self.input = str(txt)[1:-1]
        val_switch = False
        buff = ''
        move_out = True

        # 1st phase from chars in input to lines in buffer
        for char in self.input:
            if char in ('{', '['):
                if move_out:
                    self.put_line(self.line, 1)
                    move_out = False
                    self.put_line('PUSH', 1)
                continue
            elif char in ']}':
                if self.out:
                    self.put_line(self.line, 1)
                self.put_line('PULL', 1)
                continue
            elif char == ',':
                self.put_line(self.line, 1)
                continue
            else:
                move_out = True
                self.line += char
                continue
        print(self.buffer)
        # 2nd phase formatting to readable info (buffer to output)
        for counter in range(0, len(self.buffer)):
            cell = self.buffer[counter]
            if 'PUSH' in cell:
                self.level += 1
                continue
            if 'PULL' in cell:
                self.level -= 1
                continue
            cell = cell.replace('":', '" : ', 1)
            if 'values' in cell:
                val_switch = True
            else:
                if val_switch:
                    if 'date' in cell:
                        combi = cell.split(' : ', 1)
                        buff = combi[1]
                        continue
                    elif 'value' in cell:
                        combi = cell.split(' : ', 1)
                        cell = buff + ' : ' + combi[1]
                        buff = ''
                    else:
                        val_switch = False
            self.indent = self.level * self.tab_size * ' '
            cell = cell.replace('"', '')
            self.output.append(self.indent + cell)
