"""
Given a set of ASCII strings, reassemble the strings
Reads STDIN as ';' separated strings and outputs to STDOUT the joined string

Sounds like next-gen sequencing


An input that would result in arbitrary output:
input: '34567;6734'
output could be either '3456734' or '6734567'


Big-O analysis
The time complexity of the longest_common_headtail method is O(n^2) where n is
the min length of the two input strings.  This comes from n string comparisons
where each comparison is itself O(n).

The time complexity of the align_strings method is O(n^2*m^2) where m is the
number of strings being compared and n is the length of the largest string,
assuming that string comparisons are linear time.  This comes from having to
call longest_common_headtail O(m^3) times but longest_common_headtail uses
dynamic programming to lower align_strings' time complexity from O(n^2*m^3).


There are several strategies to decrease runtime which haven't been implemented
in order to keep the code readable.

align_strings can be changed to update memoizer with combined_string, though
that isn't implemented here because it would decrease the readability of the
code.  Implementing better memoization would make this run faster but not reduce
the overall asymptotic time complexity.

Going even further, it is possible to only search for substrings in all pairs
only once, then combine strings in order of the largest to smallest overlap
while updating the memoization dictionary.  This would separate substring search
from concatenation.  However, again, this would not reduce asymptotic
time complexity.

As a deeper rewrite, it is possible to adapt more specialized substring
algorithms for this problem for lower time complexities.  Knuth-Morris-Pratt
could be adapted to make string comparisons linear time allowing the
longest_common_headtail method be O(n) time, therefore making align_strings
be O(n*m^2).
"""

import sys
import unittest


class StringConnector():

    def __init__(self):
        self.memoizer = {}

    # Read the strings of data as a list
    #
    def read_data(self):
        data = sys.stdin.read()
        strings = data.split(';')
        return strings

    # Given a list of strings, continuously combine strings
    def align_strings(self, strings):
        # Uniquify and sort strings
        strings = list(set(strings))
        strings = sorted(strings, key=lambda x: -len(x))

        # Find longest common substring and their index in strings
        longest_string = strings[0]
        while len(strings) > 1:
            best_length = 0
            for i, string1 in enumerate(strings):
                for j, string2 in enumerate(strings[i+1:], start=i+1):
                    substring_length, location = self.longest_common_headtail(
                        string1, string2, best_length + 1)
                    if substring_length > best_length:
                        best_length = substring_length
                        best_location = location
                        string1_index = i
                        string2_index = j
            if best_length == 0:
                break
            string1 = strings[string1_index]
            string2 = strings.pop(string2_index)

            # Combine longest common substring and add back into strings
            cut_before = max(best_location, 0)
            cut_after = min(best_location + len(string2), len(string1))

            combined_string = string1[:cut_before] + string2 + string1[cut_after:]
            strings[string1_index] = combined_string
            for i in reversed(range(len(strings))):
                if strings[i] in combined_string and i != string1_index:
                    strings.pop(i)
            if len(combined_string) > len(longest_string):
                longest_string = combined_string

        return longest_string

    # Shift string2 to find the largest match at the beginning and at the end of string1
    # Returns (length of overlap, location of overlap relative to string1)
    #
    def longest_common_headtail(self, string1, string2, min_length=1):
        max_length = min(len(string2), len(string1))
        if string1 in self.memoizer and string2 in self.memoizer[string1]:
            if self.memoizer[string1][string2][0:2] != (0, 0):
                return self.memoizer[string1][string2][0:2]
            max_length = self.memoizer[string1][string2][2]
        lengths = range(len(string2))[min_length:max_length + 1]
        answer = (0, 0)
        for i in reversed(lengths):
            if string1[:i] == string2[len(string2) - i:]:
                answer = (i, i - len(string2))
                break
            if string1[len(string1) - i:] == string2[:i]:
                answer = (i, len(string1) - i)
                break
        if string1 not in self.memoizer:
            self.memoizer[string1] = {}
        self.memoizer[string1][string2] = answer + (min_length,)
        return answer


# TESTS


class TestLongestCommonHeadTail(unittest.TestCase):

    def setUp(self):
        connector = StringConnector()

    def test_non_overlapping(self):
        string1 = 'asdf'
        string2 = 'qwer'
        self.assertEqual(
            connector.longest_common_headtail(string1, string2), (0, 0))

    def test_internally_overlapping(self):
        string1 = 'asdf'
        string2 = 'sd'
        self.assertEqual(
            connector.longest_common_headtail(string1, string2), (0, 0))

    def test_same(self):
        string1 = 'asdf'
        string2 = 'asdf'
        self.assertEqual(
            connector.longest_common_headtail(string1, string2), (0, 0))

    def test_one_overlapping_after(self):
        string1 = 'asdf'
        string2 = 'fghj'
        self.assertEqual(
            connector.longest_common_headtail(string1, string2), (1, 3))

    def test_one_not_overlapping_after(self):
        string1 = 'asdf'
        string2 = 'sdfg'
        self.assertEqual(
            connector.longest_common_headtail(string1, string2), (3, 1))

    def test_fully_overlapping_after(self):
        string1 = 'asdf'
        string2 = 'sdf'
        self.assertEqual(
            connector.longest_common_headtail(string1, string2), (0, 0))

    def test_one_overlapping_before(self):
        string1 = 'fghj'
        string2 = 'asdf'
        self.assertEqual(
            connector.longest_common_headtail(string1, string2), (1, -3))

    def test_one_not_overlapping_before(self):
        string1 = 'sdfg'
        string2 = 'asdf'
        self.assertEqual(
            connector.longest_common_headtail(string1, string2), (3, -1))

    def test_fully_overlapping_before(self):
        string1 = 'asdf'
        string2 = 'asd'
        self.assertEqual(
            connector.longest_common_headtail(string1, string2), (0, 0))

    def test_min_length(self):
        string1 = 'asdf'
        string2 = 'fgh'
        self.assertEqual(
            connector.longest_common_headtail(string1, string2, 2), (0, 0))

    def test_allow_min_length(self):
        string1 = 'asdf'
        string2 = 'sdfg'
        self.assertEqual(
            connector.longest_common_headtail(string1, string2, 3), (3, 1))

    def test_allow_high_min_length(self):
        string1 = 'asdf'
        string2 = 'sdfgh'
        self.assertEqual(
            connector.longest_common_headtail(string1, string2, 10), (0, 0))


class TestAlignStrings(unittest.TestCase):

    def setUp(self):
        connector = StringConnector()

    def test_single_string(self):
        self.assertEqual(connector.align_strings(['asdf']), 'asdf')

    def test_two_strings(self):
        self.assertEqual(connector.align_strings(['asdf', 'sdfg']), 'asdfg')

    def test_multiple_strings(self):
        self.assertEqual(
            connector.align_strings(['asdf', 'sdfg', 'dfgh']), 'asdfgh')

    def test_internal_strings(self):
        self.assertEqual(connector.align_strings(['sd', 'asdf']), 'asdf')

    def test_short_strings(self):
        self.assertEqual(connector.align_strings(['as', 'sd', 'df']), 'asdf')

    def test_longest_substring(self):
        self.assertEqual(
            connector.align_strings(['fd', 'dff', 'asdf']), 'asdffd')

    def test_different_longest_substring(self):
        self.assertEqual(
            connector.align_strings(['fffd', 'dfff', 'asdf']), 'asdfffd')

    def test_redundant_strings(self):
        self.assertEqual(
            connector.align_strings(['asdfgh', 'fghjkl', 'ghf']), 'asdfghjkl')


# MAIN


if __name__ == "__main__":
    connector = StringConnector()
    strings = connector.read_data()
    if strings == ["test\n"]:
        unittest.main()
    elif strings == []:
        print "\n"
    print connector.align_strings(strings)
