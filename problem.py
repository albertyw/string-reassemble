"""
Given a set of ASCII strings, reassemble the strings

Sounds exactly like next-gen sequencing
"""

import sys
import unittest

# Read the strings of data as a list
#
def read_data():
    data = sys.stdin.read()
    strings = data.split(';')
    return strings

# Given a list of strings and a seed string, continuously move strings from the
# list into the largest string
def align_strings(strings, largest_string):
    while len(strings) > 0:
        # Find longest common substring
        matches = ['']*len(strings)
        for i, string in enumerate(strings):
            substring_length, location = longest_common_headtail(largest_string, string)
            matches[i] = (substring_length, location, i)

        best_length, best_location, best_string_index = max(matches, key=lambda x: x[0])
        if best_length == 0:
            break
        best_string = strings.pop(best_string_index)

        # Combine longest common substring
        cut_before = max(best_location, 0)
        cut_after = min(best_location + len(best_string), len(largest_string))

        before = largest_string[:cut_before]
        middle = best_string
        after = largest_string[cut_after:]

        #assert largest_string in before + middle + after
        largest_string = before + middle + after
    #if len(strings) > 0:
    #    for string in strings:
    #        assert string in largest_string
    return largest_string

# Shift string2 around to find the largest match at the beginning and at the end of string1
# Assumes that len(string2) <= len(string1)
# Returns (length of overlap, location of overlap relative to string1)
#
def longest_common_headtail(string1, string2):
    for i in reversed(range(len(string2)+1)[1:]):
        if string1[:i] == string2[len(string2)-i:]:
            return i, i - len(string2)
        if string1[len(string1)-i:] == string2[:i]:
            return i, len(string1) - i
    return 0, 0

## TESTS

class TestLongestCommonHeadTail(unittest.TestCase):
    def test_non_overlapping(self):
        string1 = 'asdf'
        string2 = 'qwer'
        self.assertEqual(longest_common_headtail(string1, string2), (0,0))
    def test_internally_overlapping(self):
        string1 = 'asdf'
        string2 = 'sd'
        self.assertEqual(longest_common_headtail(string1, string2), (0,0))
    def test_same(self):
        string1 = 'asdf'
        string2 = 'asdf'
        self.assertEqual(longest_common_headtail(string1, string2), (4, 0))


    def test_one_overlapping_after(self):
        string1 = 'asdf'
        string2 = 'fghj'
        self.assertEqual(longest_common_headtail(string1, string2), (1,3))
    def test_one_not_overlapping_after(self):
        string1 = 'asdf'
        string2 = 'sdfg'
        self.assertEqual(longest_common_headtail(string1, string2), (3,1))
    def test_fully_overlapping_after(self):
        string1 = 'asdf'
        string2 = 'sdf'
        self.assertEqual(longest_common_headtail(string1, string2), (3, 1))

    def test_one_overlapping_before(self):
        string1 = 'fghj'
        string2 = 'asdf'
        self.assertEqual(longest_common_headtail(string1, string2), (1,-3))
    def test_one_not_overlapping_before(self):
        string1 = 'sdfg'
        string2 = 'asdf'
        self.assertEqual(longest_common_headtail(string1, string2), (3,-1))
    def test_fully_overlapping_before(self):
        string1 = 'asdf'
        string2 = 'asd'
        self.assertEqual(longest_common_headtail(string1, string2), (3, 0))


## MAIN

if __name__ == "__main__":
    strings = read_data()
    if strings == ["test\n"]:
        unittest.main()
    elif strings == []:
        print "\n"
    # Sort from largest to smallest
    strings = sorted(strings, key=lambda x: -len(x))
    largest_string = strings.pop(0)
    print align_strings(strings, largest_string)

