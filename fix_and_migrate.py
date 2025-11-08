#!/usr/bin/env python3
"""
Fix misaligned old roast log data and migrate to new format
"""
import csv
import os
import shutil

OLD_LOG_FILE = "old_roast_log.csv"
NEW_LOG_FILE = "roast_log.csv"
BACKUP_FILE = "roast_log_before_migration.csv"

def parse_and_fix_old_csv():
    """Parse the old CSV with custom logic to fix misalignment"""
    print(f"Reading and fixing {OLD_LOG_FILE}...")

    with open(OLD_LOG_FILE, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header

        fixed_rows = []

        for i, fields in enumerate(reader, start=2):
            if not any(fields[:5]):  # Skip empty rows
                continue

            # The old CSV has 18 header columns but 20 data fields (2 trailing empties)
            # And the data is shifted starting at column 10 (End Time)

            # Based on analysis:
            # fields[12] = End Time (labeled as "Drop Temp" in header)
            # fields[13] = End Temp (labeled as "Total Roast Time" in header)
            # fields[15] = Total Roast Time in minutes (labeled as "Actual Color")
            # fields[16] = Target Roast Level (labeled as "Notes")
            # fields[17] = Notes (labeled as "Tasting Notes")

            fixed_row = {
                'Date': fields[0],
                'Time': fields[1],
                'Bean Origin': fields[2],
                'Decaf': fields[3],
                'Batch Size (lbs)': fields[4],
                'Yellow Time': fields[5],
                'First Crack Time': fields[6],
                'First Crack Temp': fields[7],
                'Second Crack Time': fields[8],
                'Second Crack Temp': fields[9],
                'End Time': fields[12] if len(fields) > 12 else '',  # Shifted from Drop Temp
                'End Temp': fields[13] if len(fields) > 13 else '',  # Shifted from Total Roast Time
                'Drop Temp': '',  # Actually empty
                'Total Roast Time (min)': fields[15] if len(fields) > 15 else '',  # Shifted from Actual Color
                'Target Roast Level': fields[16] if len(fields) > 16 else '',  # Shifted from Notes
                'Actual Color': '',  # Actually empty
                'Notes': fields[17] if len(fields) > 17 else '',  # Shifted from Tasting Notes
                'Tasting Notes (added later)': ''  # Actually empty
            }

            print(f"\nRow {i}: {fixed_row['Date']} - {fixed_row['Decaf']}")
            print(f"  FC: {fixed_row['First Crack Time']} @ {fixed_row['First Crack Temp']}°C")
            print(f"  SC: {fixed_row['Second Crack Time']} @ {fixed_row['Second Crack Temp']}°C")
            print(f"  End: {fixed_row['End Time']} @ {fixed_row['End Temp']}°C")
            print(f"  Total: {fixed_row['Total Roast Time (min)']} min")
            print(f"  Level: {fixed_row['Target Roast Level']}")
            print(f"  Notes: {fixed_row['Notes']}")

            fixed_rows.append(fixed_row)

    return fixed_rows

def convert_to_new_format(old_rows):
    """Convert fixed old format rows to new format"""
    new_rows = []

    for old_row in old_rows:
        # Map old columns to new columns according to TECHNICAL.md:
        # V1 "First Crack Time" → V2 "First Crack Start Time"
        # V1 "First Crack Temp" → V2 "First Crack Start Temp"
        # V1 "Second Crack Time" → V2 "Second Crack Start Time"
        # V1 "Second Crack Temp" → V2 "Second Crack Start Temp"

        new_row = [
            old_row['Date'],
            old_row['Time'],
            old_row['Bean Origin'],
            old_row['Decaf'],
            old_row['Batch Size (lbs)'],
            '',  # Loading Temp (not in V1)
            '',  # Turnaround Temp (not in V1)
            '',  # Early Notes (not in V1)
            old_row['Yellow Time'],
            old_row['First Crack Time'],  # → First Crack Start Time
            old_row['First Crack Temp'],  # → First Crack Start Temp
            '',  # FC Start ROR (not in V1)
            '',  # First Crack End Time (not in V1)
            '',  # First Crack End Temp (not in V1)
            '',  # FC End ROR (not in V1)
            old_row['Second Crack Time'],  # → Second Crack Start Time
            old_row['Second Crack Temp'],  # → Second Crack Start Temp
            '',  # SC Start ROR (not in V1)
            old_row['End Time'],
            old_row['End Temp'],
            old_row['Drop Temp'],
            old_row['Total Roast Time (min)'],
            old_row['Target Roast Level'],
            '',  # Roast Level (1-10) (not in V1)
            old_row['Notes'],
            old_row['Tasting Notes (added later)']
        ]

        new_rows.append(new_row)

    return new_rows

def append_to_new_log(new_rows):
    """Append converted rows to the new roast log"""
    # Create backup first
    if os.path.exists(NEW_LOG_FILE):
        shutil.copy2(NEW_LOG_FILE, BACKUP_FILE)
        print(f"\nBackup created: {BACKUP_FILE}")

    # Append to new log
    with open(NEW_LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        for row in new_rows:
            writer.writerow(row)

    print(f"\n✓ Appended {len(new_rows)} rows to {NEW_LOG_FILE}")

if __name__ == "__main__":
    # Parse and fix old data
    fixed_rows = parse_and_fix_old_csv()
    print(f"\n✓ Fixed {len(fixed_rows)} rows from old log")

    # Convert to new format
    new_rows = convert_to_new_format(fixed_rows)
    print(f"✓ Converted {len(new_rows)} rows to new format")

    # Ask for confirmation before appending
    print("\n" + "="*60)
    print("Ready to append to roast_log.csv:")
    for i, row in enumerate(new_rows, 1):
        print(f"  {i}. {row[0]} {row[1]} - {row[2]} ({'DECAF' if row[3]=='Yes' else 'REGULAR'})")
    print("="*60)

    response = input("\nProceed with migration? (yes/no): ").strip().lower()
    if response == 'yes':
        append_to_new_log(new_rows)
        print("\n✓ Migration complete!")
    else:
        print("\nMigration cancelled.")
