"""
Given a set of ASCII strings, reassemble the strings

Sounds exactly like next-gen sequencing
"""

import sys

# Read the strings of data as a list
#
def read_data():
    data = sys.stdin.read()
    strings = data.split(';')
    return strings

def align_strings(strings):
    return 'asdf'




if __name__ == "__main__":
    strings = read_data()

    # Sort from largest to smallest
    strings = sorted(strings, key=lambda x: -len(x))

    print align_strings(strings)
