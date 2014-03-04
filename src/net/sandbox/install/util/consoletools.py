#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import curses
import sys


class console_colors(object):
    (
        BLACK,
        RED,
        GREEN,
        YELLOW,
        BLUE,
        MAGENTA,
        CYAN,
        LIGHT_GRAY,
        DARK_GRAY,
        BRIGHT_RED,
        BRIGHT_GREEN,
        BRIGHT_YELLOW,
        BRIGHT_BLUE,
        BRIGHT_MAGENTA,
        BRIGHT_CYAN,
        WHITE,
    ) = range(16)
    
    @classmethod
    def rgb(cls, red, green, blue):
        """
        Calculate the palette index of a color in the 6x6x6 color cube.
     
        The red, green and blue arguments may range from 0 to 5.
        """
        return 16 + (red * 36) + (green * 6) + blue
 
    @classmethod
    def gray(cls, value):
        """
        Calculate the palette index of a color in the grayscale ramp.
     
        The value argument may range from 0 to 23.
        """
        return 232 + value

class console(object):
    '''
    Provides utility methods for dealing with console.
    '''
    from pyparsing import Literal, Word, nums, Combine, Optional, delimitedList, oneOf, alphas
    ESCAPE_SEQ = Combine(Literal('\x1b') + '[' + Optional(delimitedList(Word(nums), ';')) + oneOf(list(alphas)))

    def __init__(self, out=sys.stdout):
        '''
        Constructor
        '''
        self.out = out
        self.remaining_line = ''
        
    def width(self):
        """
        Gets the width of console in characters
        """
        try:
            curses.setupterm()  # @UndefinedVariable
            return curses.tigetnum('cols')  # @UndefinedVariable
        except Exception:
            return 80
        
    def height(self):
        """
        Gets the height of console in characters
        """
        try:
            curses.setupterm()  # @UndefinedVariable
            return curses.tigetnum('lines')  # @UndefinedVariable
        except Exception:
            return 24
        
    def colorize_text(self, text, fg=None, bg=None):
        result = ''
        if fg: result += '\x1b[38;5;%dm' % fg
        if bg: result += '\x1b[48;5;%dm' % bg
        result += text
        result += '\x1b[0m'
        return result
        
    def uncolorize_text(self, colorized_string):
        from pyparsing import Suppress
        return Suppress(self.ESCAPE_SEQ).transformString(colorized_string)
    
    def writeln(self, message):
        print(message, file=self.out)
        self.remaining_line = ''
        self.out.flush()
        
    def write(self, message):
        lines = message.splitlines()
        for line in lines:
            print(line, end='', file=self.out)
        if len(lines) == 0 or message.endswith('\n'):
            self.remaining_line = ''
        elif message.count('\n') > 0:
            self.remaining_line = lines[-1]
        else:
            self.remaining_line += lines[-1]
        self.out.flush()
            
    def erease_last_line(self):
        print('\b', end='', file=self.out)
        
    def write_right(self, right_text, newline=True):
        left_text = self.remaining_line
        nocolor_left_text = self.uncolorize_text(left_text)
        nocolor_right_text = self.uncolorize_text(right_text)
        spaces = ' ' * (self.width() - len(nocolor_left_text) - len(nocolor_right_text))
        erease = '\b' * len(nocolor_left_text)
        message = erease + left_text + spaces + right_text
        print(message, end='', file=self.out)
        if newline:
            print('\n', end='', file=self.out)
        if newline or nocolor_right_text.endswith('\n'):
            self.remaining_line = ''
        self.out.flush()
    
if __name__ == '__main__':
    # test uncolorize_text
    console = console()
    console.write("Message 1")
    console.writeln("Message 2")
    console.write("Message 3")
    console.write_right("RIGHT")
    console.writeln("Message 4")
    
    # test write
