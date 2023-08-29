import json
from datetime import datetime, timedelta

DEFAULT_YEAR = '2023'

def detect_date_format(date_str):
    try:
        datetime.strptime(date_str, '%d %b')
        return '%d %b'
    except ValueError:
        return '%Y-%m-%d'


def split_json_by_weeks(input_file):
    # Load the data
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Sort the data by the date in "x"
    sorted_data = sorted(data, key=lambda x: datetime.strptime(x['x'], detect_date_format(x['x'])))

    # Separate the data into weeks
    weekly_data = {}
    for entry in sorted_data:
        date_str = entry['x']
        date_format = detect_date_format(date_str)

        if date_format == '%d %b':
            date_obj = datetime.strptime(date_str + ' ' + DEFAULT_YEAR, '%d %b %Y')
        else:
            date_obj = datetime.strptime(date_str, date_format)

        start_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
        end_week = start_week + timedelta(days=6)  # Sunday
        week_key = start_week.strftime('%Y-%m-%d')

        if week_key not in weekly_data:
            weekly_data[week_key] = []

            # Add a placeholder for the start of the week if the entry is not Monday
            if date_obj != start_week:
                placeholder_start = entry.copy()
                placeholder_start['x'] = start_week.strftime(date_format)
                weekly_data[week_key].append(placeholder_start)

        weekly_data[week_key].append(entry)

        # Add a placeholder for the end of the week if this is the last entry and it's not Sunday
        if entry == sorted_data[-1] and date_obj != end_week:
            placeholder_end = entry.copy()
            placeholder_end['x'] = end_week.strftime(date_format)
            weekly_data[week_key].append(placeholder_end)

    # Save the separated data into new JSON files
    for week, week_entries in weekly_data.items():
        with open(f'{input_file}_week_starting_{week}.json', 'w') as file:
            json.dump(week_entries, file, indent=4)
