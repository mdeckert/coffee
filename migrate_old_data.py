#!/usr/bin/env python3
"""
Migrate old roast log data to new format
"""
import csv
import os

OLD_LOG_FILE = "old_roast_log.csv"
NEW_LOG_FILE = "roast_log.csv"
BACKUP_FILE = "roast_log_before_migration.csv"

def parse_old_csv():
    """Parse the old CSV and extract data"""
    print(f"Reading {OLD_LOG_FILE}...")

    with open(OLD_LOG_FILE, 'r') as f:
        reader = csv.DictReader(f)
        rows = []

        for i, row in enumerate(reader, start=2):
            print(f"\nRow {i}: {row}")
            rows.append(row)

    return rows

def convert_to_new_format(old_rows):
    """Convert old format rows to new format"""
    new_rows = []

    # New format columns:
    # Date,Time,Bean Origin,Decaf,Batch Size (lbs),Loading Temp,Turnaround Temp,Early Notes,
    # Yellow Time,First Crack Start Time,First Crack Start Temp,FC Start ROR,
    # First Crack End Time,First Crack End Temp,FC End ROR,
    # Second Crack Start Time,Second Crack Start Temp,SC Start ROR,
    # End Time,End Temp,Drop Temp,Total Roast Time (min),Target Roast Level,
    # Roast Level (1-10),Notes,Tasting Notes (added later)

    for old_row in old_rows:
        # Map old columns to new columns
        new_row = {
            'Date': old_row.get('Date', ''),
            'Time': old_row.get('Time', ''),
            'Bean Origin': old_row.get('Bean Origin', ''),
            'Decaf': old_row.get('Decaf', ''),
            'Batch Size (lbs)': old_row.get('Batch Size (lbs)', ''),
            'Loading Temp': '',  # Not available in old format
            'Turnaround Temp': '',  # Not available in old format
            'Early Notes': '',  # Not available in old format
            'Yellow Time': old_row.get('Yellow Time', ''),
            'First Crack Start Time': old_row.get('First Crack Time', ''),  # Map to Start
            'First Crack Start Temp': old_row.get('First Crack Temp', ''),  # Map to Start
            'FC Start ROR': '',  # Not available in old format
            'First Crack End Time': '',  # Not available in old format
            'First Crack End Temp': '',  # Not available in old format
            'FC End ROR': '',  # Not available in old format
            'Second Crack Start Time': old_row.get('Second Crack Time', ''),  # Map to Start
            'Second Crack Start Temp': old_row.get('Second Crack Temp', ''),  # Map to Start
            'SC Start ROR': '',  # Not available in old format
            'End Time': old_row.get('End Time', ''),
            'End Temp': old_row.get('End Temp', ''),
            'Drop Temp': old_row.get('Drop Temp', ''),
            'Total Roast Time (min)': old_row.get('Total Roast Time (min)', ''),
            'Target Roast Level': old_row.get('Target Roast Level', ''),
            'Roast Level (1-10)': '',  # Map from Actual Color if needed
            'Notes': old_row.get('Notes', ''),
            'Tasting Notes (added later)': old_row.get('Tasting Notes (added later)', '')
        }

        print(f"\nConverted row:")
        print(f"  Date: {new_row['Date']}")
        print(f"  Decaf: {new_row['Decaf']}")
        print(f"  FC Start: {new_row['First Crack Start Time']} @ {new_row['First Crack Start Temp']}°C")
        print(f"  SC Start: {new_row['Second Crack Start Time']} @ {new_row['Second Crack Start Temp']}°C")
        print(f"  End: {new_row['End Time']} @ {new_row['End Temp']}°C")
        print(f"  Total Time: {new_row['Total Roast Time (min)']}")

        new_rows.append(new_row)

    return new_rows

if __name__ == "__main__":
    # Parse old data
    old_rows = parse_old_csv()
    print(f"\nFound {len(old_rows)} rows in old log")

    # Convert to new format
    new_rows = convert_to_new_format(old_rows)
    print(f"\nConverted {len(new_rows)} rows to new format")
