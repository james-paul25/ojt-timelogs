import pandas as pd
import glob
import os

REQUIRED_HOURS = 320

excel_files = glob.glob("ojt_files/*.xlsx")


for file in sorted(excel_files):
    try:
        # df = pd.read_excel(file)
        df = pd.read_excel(file, skiprows=1)
        df.columns = df.columns.str.strip()

        df["DateTime"] = pd.to_datetime(
            df["Date"].astype(str) + " " + df["Punch Time"].astype(str)
        )

        df = df.sort_values("DateTime")

        total_hours = 0

        for _, day_data in df.groupby(df["DateTime"].dt.date):

            punches = day_data["DateTime"].tolist()

            for i in range(0, len(punches) - 1, 2):
                hours = (
                    punches[i + 1] - punches[i]
                ).total_seconds() / 3600

                if hours > 0:
                    total_hours += hours

        rendered = round(total_hours, 2)
        remaining = round(max(0, REQUIRED_HOURS - rendered), 2)
        progress = round((rendered / REQUIRED_HOURS) * 100, 2)

        employee = os.path.splitext(os.path.basename(file))[0]

        print("=" * 40)
        print(employee)
        print(f"Total Rendered: {rendered} hrs")
        print(f"Remaining:      {remaining} hrs")
        print(f"Total: {rendered}/{REQUIRED_HOURS} hrs")
        print(f"Progress:       {progress}%")
        print("=" * 40)
        print()

    except Exception as e:
        print(f"Error processing {file}: {e}")