import os
import pandas as pd
import re

def get_all_files_in_directory(directory):
    all_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.htm') or file.endswith('.dsd'):
                file_path = os.path.join(root, file)
                all_files.append(file_path)

    return all_files

def find_difference_position_and_substring(long_string, short_string):
    min_len = min(len(long_string), len(short_string))
    diff_start = 'None'
    for i in range(min_len):
        if (diff_start == 'None') and (long_string[i] != short_string[i]):
            diff_start = i
            # print(diff_start)
        if (diff_start != 'None') and (long_string[i] == short_string[diff_start]):
            diff_end = i
            # print(diff_end)

            return diff_start, long_string[diff_start:diff_end]

def insert_substring(original_string, position, substring):
    return original_string[:position] + substring + original_string[position:]

def get_difference(plant_name, old_list, new_list):
    """Find a the plant name in old list, and then find the difference between old and new and add it to plant name"""
    for i in range(0, len(old_list)):
        if plant_name.strip() in old_list[i]:
            # print(plant_name)
            difference_i, difference = find_difference_position_and_substring(long_string=new_list[i], short_string=old_list[i])
            new_plant_name = insert_substring(plant_name, difference_i, difference)
            break
    return new_plant_name

def replace_popup_matches(contents, old_list, new_list):
    """Finds all sections of code that contain a popup sequence"""
    pattern = r'POPUPDISPLAYFILE="([^?]+)\?Plant=([^&]+)&amp;'
    matches = re.findall(pattern, contents)
    print(f"There are {len(matches)} popup matches")
    for match in matches:
        popupfilename, plant = match
        full_match = f'POPUPDISPLAYFILE="{popupfilename}?Plant={plant}&amp;'
        new_plant = get_difference(plant, old_list, new_list)
        new_full_match = f'POPUPDISPLAYFILE="{popupfilename}?Plant={new_plant}&amp;'
        contents = contents.replace(full_match, new_full_match)
        # print(f'swapped {plant} for {new_plant}')
    return contents


name_file = 'UOW_TAURANGA_Point Naming 20230817.xlsx'
df = pd.read_excel(name_file, sheet_name='SortedSideBySide')
# print(df)
old_list = df['Old']
new_list = df['New']
# print(type(old_list))
param_names_left = old_list
num_of_swaps = 0
deleted_dict = {}
added_dict = {}
non_ds_list = []

old_folder = 'abstract_BH_18082023/abstract'
old_file_list = get_all_files_in_directory(old_folder)
new_folder = 'abstract_new_names'
encodings_to_try = ['utf-8', 'iso-8859-1', 'ascii']

# old_file_list = ['abstract_BH_18082023/abstract/TAU_Level3_P1.htm', 'abstract_BH_18082023/abstract\TAU_Level3_P1_files\DS_datasource1.dsd']
# 'abstract_BH_18082023/abstract/TAU_Level3_P1.htm'
for filepath in old_file_list:
    print(filepath)

    with open(filepath, 'r') as file:
        contents = file.read()
    
    if 'zPseudo' in contents:
        print("\n\n\n\AAAAAAAAAAAAAAAAAAAARGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGHHHHHHHHHHH FUCK\n\n\n\n")

    contents = replace_popup_matches(contents, old_list, new_list)

    deleted_dict[filepath] = []
    added_dict[filepath] = []

    for i in range(0, len(old_list)):
        old_name = old_list[i]
        new_name = new_list[i]
        if old_name in contents:
            num_of_swaps += 1
            # print(old_name)
            if filepath.endswith('.dsd'):
                # print(f"SWAPPING {old_list[i]} with {new_list[i]} ")
                contents = contents.replace('>'+old_name+'<', '>'+new_name+'<')
                deleted_dict[filepath].append(old_name)
                added_dict[filepath].append(new_name)
                param_names_left = param_names_left[param_names_left != old_name]
            elif filepath.endswith('.htm'):
                contents = contents.replace(':'+old_name+';', ':'+new_name+';')
                deleted_dict[filepath].append(old_name)
                added_dict[filepath].append(new_name)
                param_names_left = param_names_left[param_names_left != old_name]
                # print("WAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

    with open(filepath.replace(old_folder, new_folder), 'w') as new_file:
        new_file.write(contents)

df['Leftovers'] = param_names_left

df.to_excel('leftovers' +name_file, sheet_name='SortedSideBySide', index=False)

    

print(num_of_swaps)
print(len(deleted_dict.keys()))


# print(len(df))
# print(old_list)
# test = 'zPseudo_U-3-SummerTime_-SummerTime-10'

# print(df['Old'])
# if test in df['Old'].values:
#     index = df[df['Old'] == test].index[0]
#     print(f"WORKED: {index}")
# else:
#     print(f"The element '{test}' does not exist in the DataFrame.")
