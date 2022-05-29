#!/usr/bin/env python3
import argparse
import gzip
import sys
from argparse import RawTextHelpFormatter

"""
Galveston, an experimental ω-word explorer.
"""
version = '0.1α'
QUOTE = """
Still climbing after knowledge infinite,
And always moving as the restless spheres,
Will us to wear ourselves, and never rest,
Until we reach the ripest fruit of all, 
That perfect bliss and sole felicity, 
The sweet fruition of an earthly crown.
"""

NUL = 0
OUT = 1
JMP = 2


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=f'Galveston (v{version})\n{QUOTE}', formatter_class=RawTextHelpFormatter)
    parser.add_argument('file', help='Galveston source [.glv|.glv.gz]')
    args = parser.parse_args()

    src = args.file
    open_ = open
    if src.endswith('gz') or src.endswith('.glvz'):
        open_ = gzip.open
    MODE = 'm'
    state = OUT
    with open_(src, 'r') as f:
        data = f.read()

    enable = True
    i = 0
    c = 0
    while c < 2:
        while enable or ord(s) != 0:
            enable = False
            s = data[i]
            if not s:
                c += 1
                s = b'\x00'
            elif state == JMP:
                i = ord(s) - 1
                state = OUT
            elif ord(s) == 1:  # JMP convention
                c = 0
                state = JMP
            elif ord(s) != 0:
                c = 0
                print(s, end='')
            i += 1

        c += 1
        try:
            i = int(input(f'\n({i}):> '))
        except ValueError:
            pass
        enable = True

