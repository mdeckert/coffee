#!/usr/bin/env python3
"""
Coffee Roast Statistics and Analysis
Analyze your roasting history to find patterns and improve consistency
"""

import csv
import os
from datetime import datetime
from collections import defaultdict

ROAST_LOG_FILE = "roast_log.csv"

def load_roasts():
    """Load all roasts from CSV"""
    if not os.path.exists(ROAST_LOG_FILE):
        print(f"No roast log found. Run roast_logger.py first to create logs.")
        return []

    with open(ROAST_LOG_FILE, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)

def parse_time(time_str):
    """Convert mm:ss to total minutes"""
    if not time_str or ':' not in time_str:
        return None
    try:
        parts = time_str.split(':')
        return float(parts[0]) + float(parts[1])/60
    except:
        return None

def parse_temp(temp_str):
    """Parse temperature string to float"""
    if not temp_str:
        return None
    try:
        return float(temp_str)
    except:
        return None

def compare_decaf_vs_regular(roasts):
    """Compare decaf vs regular bean performance"""
    print("\n=== DECAF vs REGULAR COMPARISON ===\n")

    decaf_roasts = [r for r in roasts if r['Decaf'].lower() == 'yes']
    regular_roasts = [r for r in roasts if r['Decaf'].lower() == 'no']

    if not decaf_roasts:
        print("No decaf roasts logged yet.")
    else:
        print(f"Decaf roasts: {len(decaf_roasts)}")
        analyze_group(decaf_roasts, "DECAF")

    print()

    if not regular_roasts:
        print("No regular roasts logged yet.")
    else:
        print(f"Regular roasts: {len(regular_roasts)}")
        analyze_group(regular_roasts, "REGULAR")

def analyze_group(roasts, label):
    """Analyze statistics for a group of roasts"""
    # First crack times
    fc_times = [parse_time(r['First Crack Time']) for r in roasts]
    fc_times = [t for t in fc_times if t is not None]

    # First crack temps
    fc_temps = [parse_temp(r['First Crack Temp']) for r in roasts]
    fc_temps = [t for t in fc_temps if t is not None]

    # Total times
    total_times = [parse_time(r['End Time']) for r in roasts]
    total_times = [t for t in total_times if t is not None]

    # End temps
    end_temps = [parse_temp(r['End Temp']) for r in roasts]
    end_temps = [t for t in end_temps if t is not None]

    print(f"\n{label} Statistics:")

    if fc_times:
        avg_fc = sum(fc_times) / len(fc_times)
        print(f"  Avg First Crack: {avg_fc:.1f} min (range: {min(fc_times):.1f}-{max(fc_times):.1f})")

    if fc_temps:
        avg_fc_temp = sum(fc_temps) / len(fc_temps)
        print(f"  Avg FC Temp: {avg_fc_temp:.0f}°F (range: {min(fc_temps):.0f}-{max(fc_temps):.0f})")

    if total_times:
        avg_total = sum(total_times) / len(total_times)
        print(f"  Avg Total Time: {avg_total:.1f} min (range: {min(total_times):.1f}-{max(total_times):.1f})")

    if end_temps:
        avg_end = sum(end_temps) / len(end_temps)
        print(f"  Avg End Temp: {avg_end:.0f}°F (range: {min(end_temps):.0f}-{max(end_temps):.0f})")

    if fc_times and total_times and len(fc_times) == len(total_times):
        dev_times = [total_times[i] - fc_times[i] for i in range(min(len(fc_times), len(total_times)))]
        if dev_times:
            avg_dev = sum(dev_times) / len(dev_times)
            print(f"  Avg Development Time: {avg_dev:.1f} min")

def show_trends(roasts):
    """Show roasting trends over time"""
    print("\n=== ROASTING TRENDS ===\n")

    if len(roasts) < 3:
        print("Need at least 3 roasts to show trends.")
        return

    # Last 5 roasts
    recent = roasts[-5:]

    print("Last 5 roasts:")
    for r in recent:
        date = r['Date']
        origin = r['Bean Origin']
        decaf = "(DECAF)" if r['Decaf'].lower() == 'yes' else ""
        total = r['Total Roast Time (min)'] or r['End Time']
        end_temp = r['End Temp']
        level = r['Actual Color'] or r['Target Roast Level']

        print(f"  {date}: {origin} {decaf}")
        print(f"    Time: {total} | End: {end_temp}°F | Result: {level}")

def consistency_check(roasts):
    """Check for consistency issues"""
    print("\n=== CONSISTENCY CHECK ===\n")

    if len(roasts) < 2:
        print("Need at least 2 roasts to check consistency.")
        return

    # Group by bean type (decaf vs regular)
    groups = defaultdict(list)
    for r in roasts:
        key = f"{r['Bean Origin']}_{r['Decaf']}"
        groups[key].append(r)

    for key, group_roasts in groups.items():
        if len(group_roasts) < 2:
            continue

        origin, is_decaf = key.rsplit('_', 1)
        label = f"{origin} {'(Decaf)' if is_decaf == 'Yes' else ''}"

        total_times = [parse_time(r['End Time']) for r in group_roasts]
        total_times = [t for t in total_times if t is not None]

        if len(total_times) >= 2:
            avg = sum(total_times) / len(total_times)
            variance = sum((t - avg)**2 for t in total_times) / len(total_times)
            std_dev = variance ** 0.5

            print(f"{label}: {len(group_roasts)} roasts")
            print(f"  Avg time: {avg:.1f} min")
            print(f"  Std deviation: {std_dev:.2f} min")

            if std_dev < 0.5:
                print(f"  ✓ Very consistent!")
            elif std_dev < 1.0:
                print(f"  ✓ Good consistency")
            else:
                print(f"  ⚠ High variability - review roast notes")
        print()

def main():
    roasts = load_roasts()

    if not roasts:
        print("No roasts found. Use roast_logger.py to start logging!")
        return

    print(f"\n=== COFFEE ROAST STATISTICS ===")
    print(f"Total roasts logged: {len(roasts)}")

    while True:
        print("\n1. Compare Decaf vs Regular")
        print("2. Show recent trends")
        print("3. Consistency check")
        print("4. Show all statistics")
        print("5. Exit")

        choice = input("\nChoice: ").strip()

        if choice == '1':
            compare_decaf_vs_regular(roasts)
        elif choice == '2':
            show_trends(roasts)
        elif choice == '3':
            consistency_check(roasts)
        elif choice == '4':
            compare_decaf_vs_regular(roasts)
            show_trends(roasts)
            consistency_check(roasts)
        elif choice == '5':
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
