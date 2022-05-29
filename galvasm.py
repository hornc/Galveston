#!/usr/bin/env python

import argparse
import re

ABOUT = """
Converts Galveston "assembly language" / markup
to Galveston binary ω-words.

"""

DEBUG = False

NUL = '{NUL}'
JMP = '{JMP}'
LF = '{LF}'
RESERVED = {
  '{NUL}': '\x00', 
  '{JMP}': '\x01',
   '{LF}': '\x0a'
   }

DIGITS = re.compile(r'[0-9]*')

ABS = re.compile(r'({([0-9]+)})')  # Deprecated. Use SYMBOL
SYMBOL = re.compile(r'({([A-Z0-9_]+)})')  # {} Symbol
LABEL = re.compile(r'(\[([[A-Z0-9_]+)\])')  # Deprecated. Use DECIMAL
DECIMAL = re.compile(r'(\(([[A-Z0-9_]+)\))')  # () Decimal representaion of symbol index in alphabet 
LABEL_DECIMAL = re.compile(r'(\(([[A-Z0-9_]+)\))')

TOKENS = re.compile(r'(\([A-Z0-9_]+\)|\[[A-Z0-9_]+\]|{[A-Z0-9_]+})')

INDEX_PAD = 6
L_FILL = ' '


def tokenise(s):
    tokens = TOKENS.split(s)
    return [t for t in tokens if t]


def replace_abs(s):
    """Replace all absolute refs with their byte values."""
    for m in LABEL.findall(s):  # Strips out line labels
        s = s.replace(m[0], '')
    for m in LABEL_DECIMAL.findall(s):  # Replace LABEL_TO_DECIMAL with padded symbol index
        i = m[1]
        if not DIGITS.match(i):
            pass
        s = s.replace(m[0], i.rjust(INDEX_PAD, L_FILL))
    for m in ABS.findall(s):
        s = s.replace(m[0], chr(int(m[1])))
    return s


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=ABOUT)
    parser.add_argument('file', help='Source Galveston assemly language / markup file to compile')
    parser.add_argument('--debug', '-d', help='Turn on debug output', action='store_true')
    args = parser.parse_args()

    DEBUG = args.debug
    fname = args.file
    source = []
    i = 0  # Symbol index
    labels = {}  # dict of label indexes

    with open(fname, 'r') as f:
        for line in f.readlines():
            line = line.strip('\n')
            tokens = tokenise(line)
            for token in tokens:
                if LABEL.match(token):
                    labels[token[1:-1]] = i
                    continue
                elif token in RESERVED:
                    source.append(RESERVED[token])
                    i += 1
                    continue
                elif SYMBOL.match(token):
                    i += 1
                elif DECIMAL.match(token):
                    i += INDEX_PAD
                else:
                    i += len(token)
                source.append(token)

    if DEBUG:
        print('LABELS:', labels)

    for token in source:
        if SYMBOL.match(token):
            print(chr(labels[token[1:-1]]), end='')
        elif DECIMAL.match(token):
            print(str(labels[token[1:-1]]).rjust(INDEX_PAD, L_FILL), end='')
        else:
            print(token, end='')


