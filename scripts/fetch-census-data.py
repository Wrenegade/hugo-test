#!/usr/bin/env python3
"""
Pre-fetch Census ACS unemployment data for all years and save as static JSON.

Usage:
    python3 scripts/fetch-census-data.py

Outputs JSON files to static/data/:
    unemployment_2019.json
    unemployment_2020.json
    unemployment_2021.json
    unemployment_2022.json
    unemployment_2023.json

Each file contains:
{
    "year": 2023,
    "fetched": "2026-03-17T...",
    "nationalAvg": 5.12,
    "counties": {
        "01001": { "name": "Autauga County", "state": "01", "rate": 3.45, "unemployed": 1234, "laborForce": 35789 },
        ...
    }
}
"""

import json
import os
import sys
from datetime import datetime, timezone
from urllib.request import urlopen
from urllib.error import URLError

CENSUS_KEY = os.environ.get(
    "CENSUS_API_KEY",
    "59718e1cb53e0c767125daecc83e2d6dccd77d64"
)

YEARS = [2019, 2020, 2021, 2022, 2023]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "static", "data")


def fetch_year(year):
    """Fetch ACS 5-year unemployment data for a given year."""
    url = (
        f"https://api.census.gov/data/{year}/acs/acs5"
        f"?get=B23025_001E,B23025_005E,NAME"
        f"&for=county:*&in=state:*"
        f"&key={CENSUS_KEY}"
    )
    print(f"  Fetching {year}... ", end="", flush=True)
    try:
        with urlopen(url, timeout=30) as resp:
            rows = json.loads(resp.read().decode())
    except (URLError, Exception) as e:
        print(f"FAILED: {e}")
        return None

    # Parse rows — first row is header
    counties = {}
    total_unemployed = 0
    total_labor = 0

    for row in rows[1:]:
        labor_force = int(row[0]) if row[0] and row[0] != "null" else 0
        unemployed = int(row[1]) if row[1] and row[1] != "null" else 0
        name = row[2] or ""
        state_fips = row[3]
        county_fips = row[4]
        fips = state_fips + county_fips

        if labor_force == 0:
            continue

        rate = round(unemployed / labor_force * 100, 4)
        county_name = name.split(",")[0].strip()

        counties[fips] = {
            "name": county_name,
            "state": state_fips,
            "rate": rate,
            "unemployed": unemployed,
            "laborForce": labor_force,
        }

        total_unemployed += unemployed
        total_labor += labor_force

    national_avg = round(total_unemployed / total_labor * 100, 4) if total_labor else 0

    result = {
        "year": year,
        "fetched": datetime.now(timezone.utc).isoformat(),
        "nationalAvg": national_avg,
        "counties": counties,
    }

    print(f"OK — {len(counties)} counties, national avg {national_avg}%")
    return result


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Fetching Census ACS unemployment data into {OUTPUT_DIR}/\n")

    for year in YEARS:
        data = fetch_year(year)
        if data is None:
            print(f"  Skipping {year} due to error.")
            continue

        out_path = os.path.join(OUTPUT_DIR, f"unemployment_{year}.json")
        with open(out_path, "w") as f:
            json.dump(data, f, separators=(",", ":"))

        size_kb = os.path.getsize(out_path) / 1024
        print(f"  Wrote {out_path} ({size_kb:.0f} KB)\n")

    print("Done!")


if __name__ == "__main__":
    main()
