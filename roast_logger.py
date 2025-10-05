#!/usr/bin/env python3
"""
Coffee Roast Logger for Skywalker Roaster
Quick logging tool for tracking roast batches
"""

import csv
import os
from datetime import datetime

ROAST_LOG_FILE = "roast_log.csv"

def initialize_log():
    """Create log file with headers if it doesn't exist"""
    if not os.path.exists(ROAST_LOG_FILE):
        with open(ROAST_LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Date', 'Time', 'Bean Origin', 'Decaf', 'Batch Size (lbs)',
                'Yellow Time', 'First Crack Time', 'First Crack Temp',
                'Second Crack Time', 'Second Crack Temp', 'End Time', 'End Temp',
                'Drop Temp', 'Total Roast Time (min)', 'Target Roast Level',
                'Actual Color', 'Notes', 'Tasting Notes (added later)'
            ])
        print(f"Created {ROAST_LOG_FILE}")

def log_roast():
    """Interactive roast logging"""
    print("\n=== COFFEE ROAST LOGGER ===\n")

    # Basic info
    bean_origin = input("Bean origin (default: Colombian): ").strip() or "Colombian"
    is_decaf = input("Decaf? (y/n, default: n): ").strip().lower() == 'y'
    batch_size = input("Batch size in lbs (default: 1): ").strip() or "1"

    print("\n--- Timing & Temperature ---")
    print("(Press Enter to skip any field)")

    yellow_time = input("Yellow/Drying phase time (mm:ss): ").strip()
    fc_time = input("First crack start time (mm:ss): ").strip()
    fc_temp = input("First crack temp (°F): ").strip()
    sc_time = input("Second crack time (mm:ss, if reached): ").strip()
    sc_temp = input("Second crack temp (°F, if reached): ").strip()
    end_time = input("End/drop time (mm:ss): ").strip()
    end_temp = input("End temp (°F): ").strip()
    drop_temp = input("Drop temp (°F): ").strip()

    # Calculate total time if end time provided
    total_time = ""
    if end_time:
        try:
            parts = end_time.split(':')
            total_minutes = float(parts[0]) + float(parts[1])/60
            total_time = f"{total_minutes:.1f}"
        except:
            total_time = input("Total roast time (minutes): ").strip()

    target_level = input("\nTarget roast level (default: Medium-Dark): ").strip() or "Medium-Dark"
    actual_color = input("Actual color/result: ").strip()
    notes = input("Notes (airflow, weather, observations): ").strip()

    # Write to CSV
    with open(ROAST_LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        now = datetime.now()
        writer.writerow([
            now.strftime('%Y-%m-%d'),
            now.strftime('%H:%M'),
            bean_origin,
            'Yes' if is_decaf else 'No',
            batch_size,
            yellow_time,
            fc_time,
            fc_temp,
            sc_time,
            sc_temp,
            end_time,
            end_temp,
            drop_temp,
            total_time,
            target_level,
            actual_color,
            notes,
            ''  # Tasting notes placeholder
        ])

    print(f"\n✓ Roast logged successfully to {ROAST_LOG_FILE}")

def view_recent(n=5):
    """View recent roasts"""
    if not os.path.exists(ROAST_LOG_FILE):
        print("No roast log found yet.")
        return

    with open(ROAST_LOG_FILE, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    if len(rows) <= 1:
        print("No roasts logged yet.")
        return

    print(f"\n=== LAST {min(n, len(rows)-1)} ROASTS ===\n")
    headers = rows[0]
    recent = rows[-n:] if len(rows) > n else rows[1:]

    for row in recent:
        print(f"Date: {row[0]} {row[1]} | {row[2]} {'(DECAF)' if row[3]=='Yes' else ''}")
        print(f"  First Crack: {row[6]} @ {row[7]}°F")
        print(f"  End: {row[10]} @ {row[11]}°F (drop {row[12]}°F)")
        print(f"  Total: {row[13]} min | Level: {row[14]} → {row[15]}")
        if row[16]:
            print(f"  Notes: {row[16]}")
        print()

def main():
    initialize_log()

    while True:
        print("\n1. Log new roast")
        print("2. View recent roasts")
        print("3. Exit")

        choice = input("\nChoice: ").strip()

        if choice == '1':
            log_roast()
        elif choice == '2':
            n = input("How many recent roasts to show (default: 5): ").strip()
            view_recent(int(n) if n else 5)
        elif choice == '3':
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
