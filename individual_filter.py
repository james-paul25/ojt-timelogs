import math
from datetime import time

import pandas as pd

file_path = "ojt_files/6140.xlsx"
required_hours = 320

# Header is on row 2
df = pd.read_excel(file_path, header=1)

# Keep only needed columns
df = df[['Date', 'Punch Time', 'Punch State']]

# Combine Date and Punch Time into a single datetime
df['DateTime'] = pd.to_datetime(
    df['Date'].astype(str) + ' ' + df['Punch Time'].astype(str)
)

# Sort by datetime
df = df.sort_values('DateTime')


def round_checkin(dt):
    if dt.time() < time(12, 0):
        return dt.replace(hour=8, minute=0, second=0)
    else:
        return dt.replace(hour=13, minute=0, second=0)


def round_checkout(dt):
    if dt.time() < time(13, 0):
        return dt.replace(hour=12, minute=0, second=0)
    else:
        return dt.replace(hour=17, minute=0, second=0)

daily_hours = []

# Process each date
for date, group in df.groupby('Date'):
    group = group.sort_values('DateTime')

    total_seconds = 0
    current_in = None

    for _, row in group.iterrows():
        state = str(row['Punch State']).strip().lower()

        if state == 'check in':
            current_in = round_checkin(row['DateTime'])

        elif state == 'check out' and current_in is not None:
            checkout = round_checkout(row['DateTime'])

            total_seconds += (
                checkout - current_in
            ).total_seconds()

            current_in = None

    hours = round(total_seconds / 3600, 2)

    daily_hours.append({
        'Date': pd.to_datetime(date).strftime('%Y-%m-%d'),
        'Hours Worked': hours
    })

summary = pd.DataFrame(daily_hours)

# Totals
total_days = len(summary)
total_hours = summary['Hours Worked'].sum()

# OJT requirement
required_hours = 320

remaining_hours = max(0, required_hours - total_hours)
remaining_days = math.ceil(remaining_hours / 8)

print("\n=== DAILY SUMMARY ===")
print(summary.to_string(index=False))

print("\n=== TOTALS ===")
print(f"Total Days Worked : {total_days}")
print(f"Total Hours Worked: {total_hours:.2f}")
print(f"Remaining Hours   : {remaining_hours:.2f}")
print(f"Remaining Days    : {remaining_days}")
