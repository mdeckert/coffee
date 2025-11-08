#!/usr/bin/env python3
"""
Smart migration script that handles different data patterns in old CSV
"""
import csv
import os
import shutil

OLD_LOG_FILE = "old_roast_log.csv"
NEW_LOG_FILE = "roast_log.csv"
BACKUP_FILE = "roast_log_before_migration.csv"

def parse_old_row_smart(fields):
    """Intelligently parse old CSV row based on field patterns"""
    # Common fields (always present)
    base_data = {
        'Date': fields[0],
        'Time': fields[1],
        'Bean Origin': fields[2],
        'Decaf': fields[3],
        'Batch Size (lbs)': fields[4],
    }

    # Detect pattern based on field analysis
    # Pattern 1 (Row 2): FC at [6]/[7], SC at [8]/[9], End at [12]/[13], Total at [15]
    # Pattern 2 (Rows 3-5): Extra data at [5]/[6], FC at [9]/[10], SC at [11]/[12], End at [15]/[16], Total at [18]

    # Check if field[6] is a time (MM:SS format) - indicates Pattern 1
    if ':' in fields[6] if len(fields) > 6 else False:
        # Pattern 1: Like Row 2
        return {
            **base_data,
            'Loading Temp': '',
            'Turnaround Temp': '',
            'Yellow Time': fields[5] if len(fields) > 5 else '',
            'Early Notes': '',
            'First Crack Time': fields[6] if len(fields) > 6 else '',
            'First Crack Temp': fields[7] if len(fields) > 7 else '',
            'Second Crack Time': fields[8] if len(fields) > 8 else '',
            'Second Crack Temp': fields[9] if len(fields) > 9 else '',
            'End Time': fields[12] if len(fields) > 12 else '',
            'End Temp': fields[13] if len(fields) > 13 else '',
            'Drop Temp': '',
            'Total Roast Time (min)': fields[15] if len(fields) > 15 else '',
            'Target Roast Level': fields[16] if len(fields) > 16 else '',
            'Actual Color': '',
            'Notes': fields[17] if len(fields) > 17 else '',
            'Tasting Notes (added later)': ''
        }
    else:
        # Pattern 2: Like Rows 3-5
        # Field [5] might be loading temp or note
        # Field [6] might be turnaround temp
        # FC data at [9]/[10], SC at [11]/[12], End at [15]/[16]
        yellow_or_loading = fields[5] if len(fields) > 5 else ''
        turnaround_or_temp = fields[6] if len(fields) > 6 else ''

        # Determine if field[5] is a note or a number
        loading_temp = ''
        yellow_time = ''
        early_notes = ''

        if yellow_or_loading:
            # If it contains letters, it's a note
            if any(c.isalpha() for c in yellow_or_loading):
                yellow_time = yellow_or_loading
            else:
                # It's a number, likely loading temp
                loading_temp = yellow_or_loading

        # Field [6] is likely turnaround temp if it's a number in range 100-130
        turnaround_temp = ''
        if turnaround_or_temp:
            try:
                temp_val = float(turnaround_or_temp)
                if 80 <= temp_val <= 130:
                    turnaround_temp = turnaround_or_temp
            except:
                # If field [7] exists and has text, field [6] might still be turnaround
                if len(fields) > 7 and any(c.isalpha() for c in fields[7]):
                    turnaround_temp = turnaround_or_temp
                    early_notes = fields[7] if len(fields) > 7 else ''

        return {
            **base_data,
            'Loading Temp': loading_temp,
            'Turnaround Temp': turnaround_temp,
            'Yellow Time': yellow_time,
            'Early Notes': early_notes,
            'First Crack Time': fields[9] if len(fields) > 9 else '',
            'First Crack Temp': fields[10] if len(fields) > 10 else '',
            'Second Crack Time': fields[11] if len(fields) > 11 else '',
            'Second Crack Temp': fields[12] if len(fields) > 12 else '',
            'End Time': fields[15] if len(fields) > 15 else '',
            'End Temp': fields[16] if len(fields) > 16 else '',
            'Drop Temp': '',
            'Total Roast Time (min)': fields[18] if len(fields) > 18 else '',
            'Target Roast Level': fields[19] if len(fields) > 19 else '',
            'Actual Color': '',
            'Notes': fields[20] if len(fields) > 20 else '',
            'Tasting Notes (added later)': ''
        }

def parse_and_fix_old_csv():
    """Parse the old CSV with smart pattern detection"""
    print(f"Reading {OLD_LOG_FILE} with smart parser...")

    with open(OLD_LOG_FILE, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header

        fixed_rows = []

        for i, fields in enumerate(reader, start=2):
            if not any(fields[:5]):  # Skip empty rows
                continue

            fixed_row = parse_old_row_smart(fields)

            print(f"\nRow {i}: {fixed_row['Date']} {fixed_row['Time']} - {fixed_row['Decaf']}")
            if fixed_row['Loading Temp']:
                print(f"  Loading: {fixed_row['Loading Temp']}°C")
            if fixed_row['Turnaround Temp']:
                print(f"  Turnaround: {fixed_row['Turnaround Temp']}°C")
            if fixed_row['Yellow Time']:
                print(f"  Yellow: {fixed_row['Yellow Time']}")
            print(f"  FC: {fixed_row['First Crack Time']} @ {fixed_row['First Crack Temp']}°C")
            print(f"  SC: {fixed_row['Second Crack Time']} @ {fixed_row['Second Crack Temp']}°C")
            print(f"  End: {fixed_row['End Time']} @ {fixed_row['End Temp']}°C")
            print(f"  Total: {fixed_row['Total Roast Time (min)']} min")
            print(f"  Level: {fixed_row['Target Roast Level']}")
            if fixed_row['Notes']:
                print(f"  Notes: {fixed_row['Notes']}")

            fixed_rows.append(fixed_row)

    return fixed_rows

def convert_to_new_format(old_rows):
    """Convert fixed old format rows to new format"""
    new_rows = []

    for old_row in old_rows:
        new_row = [
            old_row['Date'],
            old_row['Time'],
            old_row['Bean Origin'],
            old_row['Decaf'],
            old_row['Batch Size (lbs)'],
            old_row['Loading Temp'],
            old_row['Turnaround Temp'],
            old_row['Early Notes'],
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
        print(f"\n✓ Backup created: {BACKUP_FILE}")

    # Append to new log
    with open(NEW_LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        for row in new_rows:
            writer.writerow(row)

    print(f"✓ Appended {len(new_rows)} rows to {NEW_LOG_FILE}")

if __name__ == "__main__":
    # Parse and fix old data
    fixed_rows = parse_and_fix_old_csv()
    print(f"\n{'='*60}")
    print(f"✓ Successfully parsed {len(fixed_rows)} rows from old log")
    print('='*60)

    # Convert to new format
    new_rows = convert_to_new_format(fixed_rows)

    # Show summary
    print("\nReady to append to roast_log.csv:")
    regular_count = sum(1 for row in new_rows if row[3] == 'No')
    decaf_count = sum(1 for row in new_rows if row[3] == 'Yes')
    print(f"  - {regular_count} REGULAR roasts")
    print(f"  - {decaf_count} DECAF roasts")

    for i, row in enumerate(new_rows, 1):
        decaf_label = 'DECAF' if row[3] == 'Yes' else 'REGULAR'
        print(f"  {i}. {row[0]} {row[1]} - {row[2]} ({decaf_label})")

    print('='*60)

    # Proceed with migration
    response = input("\nProceed with migration? (yes/no): ").strip().lower()
    if response == 'yes':
        append_to_new_log(new_rows)
        print("\n✓ Migration complete!")
    else:
        print("\nMigration cancelled.")
