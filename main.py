# This is a sample Python script.
from date_based_json_grouper import split_json_by_weeks


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # Use the function
    input_json_file = 'input/automation_saving_90days_data.json'
    split_json_by_weeks(input_json_file)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
