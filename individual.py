import pandas as pd

file_path = "ojt_files/6140.xlsx"
HOURS_REQUIRED = 320

df = pd.read_excel(file_path, header=1)
df = df[['Date', 'Punch Time', 'Punch State']]
df['DateTime'] = pd.to_datetime(
    df['Date'].astype(str) + ' ' + df['Punch Time'].astype(str)
)

df = df.sort_values('DateTime')

daily_hours = []

for date, group in df.groupby('Date'):
    group = group.sort_values('DateTime')

    total_seconds = 0
    current_in = None

    for _, row in group.iterrows():
        state = str(row['Punch State']).strip().lower()

        if state == 'check in':
            current_in = row['DateTime']

        elif state == 'check out' and current_in is not None:
            total_seconds += (
                row['DateTime'] - current_in
            ).total_seconds()
            current_in = None

    hours = round(total_seconds / 3600, 2)

    daily_hours.append({
        'Date': pd.to_datetime(date).strftime('%Y-%m-%d'),
        'Hours Worked': hours
    })

summary = pd.DataFrame(daily_hours)

print("\nDaily:")
print(summary.to_string(index=False))

print("\nTotals:")
print(f"Hours Required     : {HOURS_REQUIRED:.2f}")
print(f"Total Days Worked : {len(summary)}")
print(f"Total Hours Worked: {summary['Hours Worked'].sum():.2f}")

total_hours = summary['Hours Worked'].sum()
hours_left = max(0.0, HOURS_REQUIRED - total_hours)
hours_left = round(hours_left, 2)

percent_complete = round((total_hours / HOURS_REQUIRED) * 100, 2) if HOURS_REQUIRED > 0 else 0.0

print(f"Hours Remaining    : {hours_left:.2f}")
print(f"Percent Complete   : {percent_complete:.2f}%")