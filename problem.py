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

def align_strings(strings, largest_string):
    while len(strings) > 0:
        # Find longest common substring
        max_length = 0
        best_location = None
        best_string_index = None
        for i, string in enumerate(strings):
            substring_length, location = longest_common_substring(largest_string, string)
            if substring_length > max_length:
                max_length = substring_length
                best_location = location
                best_string_index = i
        if best_string_index == None:
            break
        best_string = strings.pop(best_string_index)

        # Combine longest common substring
        #print max_length
        #print best_location
        #print largest_string
        #print best_string

        cut_before = max(best_location, 0)
        cut_after = min(best_location + len(best_string), len(largest_string))

        before = largest_string[:cut_before]
        middle = best_string
        after = largest_string[cut_after:]

        #print largest_string
        #print best_string
        #print 'before',before
        #print 'middle',middle
        #print 'after ',after

        if largest_string not in before + middle + after:
            qwerqwer
        largest_string = before + middle + after
        #print largest_string
        #print '---'
    if len(strings) > 0:
        for string in strings:
            assert string in largest_string
    return largest_string

# Simple dynamic programming longest common substring algorithm
#
"""
def longest_common_substring(string1, string2):
    matrix = [[0]*len(string2) for _ in string1]
    longest_length = 0
    substring = ''
    for i in range(len(string1)):
        for j in range(len(string2)):
            if string1[i] == string2[j]:
                if i == 0 or j == 0:
                    matrix[i][j] = 1
                else:
                    matrix[i][j] = matrix[i-1][j-1] + 1
                if matrix[i][j] > longest_length:
                    longest_length = matrix[i][j]
                    substring = string1[i-longest_length+1 : i+1]
                    location = i - j
            else:
                matrix[i][j] = 0
    return longest_length, location, substring
"""
# Shift string2 around to find the largest match at the beginning and at the end of string1
# Assumes that len(string2) <= len(string1)
#
def longest_common_substring(string1, string2):
    for i in reversed(range(len(string2))):
        if string1[:i] == string2[len(string2)-i:]:
            return i, i - len(string2)
        if string1[len(string1)-i:] == string2[:i]:
            return i, len(string1) - i
    return 0, 0

if __name__ == "__main__":
    strings = read_data()

    # Sort from largest to smallest
    strings = sorted(strings, key=lambda x: -len(x))
    #print strings
    largest_string = strings.pop(0)

    print align_strings(strings, largest_string)
