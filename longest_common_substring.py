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
