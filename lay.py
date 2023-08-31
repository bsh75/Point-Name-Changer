import re



def find_difference_position_and_substring(long_string, short_string):
    min_len = min(len(string1), len(string2))
    diff_start = 'None'
    for i in range(min_len):
        if (diff_start == 'None') and (string1[i] != string2[i]):
            diff_start = i
            print(diff_start)
        if (diff_start != 'None') and (string1[i] == string2[diff_start]):
            diff_end = i
            print(diff_end)

            return diff_start, string1[diff_start:diff_end]
    
    # If the loop doesn't find a difference within the common part of the strings
    # Return the length of the shorter string (or 0 if they are equal)
    # return min_len, ''


# string2 = 'FCU-4-03-TempCtlMdByp'
# string1 = 'TAU-CBD-FCU-4-03-TempCtlMdByp'

string2 = 'TAU-3-AHU01-FltrPressSw'
string1 = 'TAU-3-AHU01-FltrPressSw'

differences, bllah = find_difference_position_and_substring(string1, string2)

print(differences)
