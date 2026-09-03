import cdsapi
import os
import calendar
import time

# ============================================================
# CONFIGURATION
# ============================================================

DATASET = "reanalysis-era5-single-levels"

# Where downloaded ERA5 files will be stored
OUTPUT_DIR = r"C:\Users\DP\Documents\Programming Languages\SIH\2026\Project\Flood-Prediction_SIH\ERA5_Data"

# Variables required for the project
VARIABLES = [
    "10m_u_component_of_wind",
    "10m_v_component_of_wind",
    "2m_dewpoint_temperature",
    "2m_temperature",
    "surface_pressure",
    "total_precipitation",
    "surface_runoff",
    "convective_precipitation",
    "large_scale_precipitation"
]

# Geographic area:
# North, West, South, East
AREA = [29, 89, 24, 97]

# All 24 hours
TIMES = [
    "00:00", "01:00", "02:00", "03:00",
    "04:00", "05:00", "06:00", "07:00",
    "08:00", "09:00", "10:00", "11:00",
    "12:00", "13:00", "14:00", "15:00",
    "16:00", "17:00", "18:00", "19:00",
    "20:00", "21:00", "22:00", "23:00"
]

# Start and end period
START_YEAR = 2015
START_MONTH = 1

END_YEAR = 2026
END_MONTH = 8


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# CREATE CDS API CLIENT
# ============================================================

print("Connecting to Copernicus Climate Data Store...")

client = cdsapi.Client()

print("CDS API connection successful.")
print()


# ============================================================
# DOWNLOAD MONTH BY MONTH
# ============================================================

for year in range(START_YEAR, END_YEAR + 1):

    # Determine which months to download for this year
    first_month = START_MONTH if year == START_YEAR else 1
    last_month = END_MONTH if year == END_YEAR else 12

    for month in range(first_month, last_month + 1):

        month_string = f"{month:02d}"

        # Number of days in this particular month
        number_of_days = calendar.monthrange(year, month)[1]

        days = [
            f"{day:02d}"
            for day in range(1, number_of_days + 1)
        ]

        # Output filename
        filename = f"ERA5_{year}_{month_string}.zip"
        output_file = os.path.join(OUTPUT_DIR, filename)

        print("=" * 70)
        print(f"Preparing: {year}-{month_string}")
        print(f"Days: {number_of_days}")
        print(f"Output: {output_file}")

        # ----------------------------------------------------
        # Skip if already downloaded
        # ----------------------------------------------------

        if os.path.exists(output_file):
            print("Already downloaded. Skipping...")
            continue

        # ----------------------------------------------------
        # CDS request
        # ----------------------------------------------------

        request = {
            "product_type": ["reanalysis"],

            "variable": VARIABLES,

            "year": [str(year)],

            "month": [month_string],

            "day": days,

            "time": TIMES,

            "data_format": "grib",

            "download_format": "zip",

            "area": AREA
        }

        # ----------------------------------------------------
        # Download
        # ----------------------------------------------------

        try:

            print(f"Starting download for {year}-{month_string}...")

            client.retrieve(
                DATASET,
                request
            ).download(output_file)

            print(f"SUCCESS: {year}-{month_string}")
            print(f"Saved to: {output_file}")

        except Exception as error:

            print(f"ERROR downloading {year}-{month_string}")
            print(error)

            print("Waiting 30 seconds before continuing...")
            time.sleep(30)

            continue


print()
print("=" * 70)
print("ALL REQUESTED ERA5 DATA DOWNLOADS COMPLETED")
print("=" * 70)
print(f"Data location: {OUTPUT_DIR}")