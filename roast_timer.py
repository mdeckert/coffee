#!/usr/bin/env python3
"""
Coffee Roast Timer with Alerts
Real-time timer with alerts for key roast stages
"""

import time
import sys
import os
from datetime import datetime, timedelta

def beep(count=1):
    """Make alert sound"""
    for _ in range(count):
        print('\a', end='', flush=True)
        time.sleep(0.2)

def clear_line():
    """Clear current line"""
    print('\r' + ' ' * 80 + '\r', end='', flush=True)

def format_time(seconds):
    """Format seconds as MM:SS"""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def roast_timer(bean_type='regular'):
    """Interactive roast timer with stage alerts"""

    # Time markers based on bean type (in seconds)
    if bean_type == 'decaf':
        markers = [
            (240, "4:00 - Yellow/Drying phase should be underway"),
            (360, "6:00 - Approaching first crack zone (decaf)"),
            (480, "8:00 - First crack window! Listen carefully"),
            (540, "9:00 - Development phase - monitor closely"),
            (600, "10:00 - Typical decaf drop zone for med-dark"),
            (660, "11:00 - Late development - check color/smell"),
        ]
    else:  # regular
        markers = [
            (300, "5:00 - Yellow/Drying phase should be complete"),
            (480, "8:00 - Approaching first crack zone"),
            (540, "9:00 - First crack window! Listen carefully"),
            (600, "10:00 - Development phase underway"),
            (660, "11:00 - Med-dark drop zone approaching"),
            (720, "12:00 - Check beans - likely near target"),
            (780, "13:00 - Late development - risk of over-roasting"),
        ]

    print(f"\n=== COFFEE ROAST TIMER ({bean_type.upper()}) ===\n")
    print("Timer starting... Press Ctrl+C to stop\n")

    start_time = time.time()
    last_marker = -1

    try:
        while True:
            elapsed = time.time() - start_time
            elapsed_int = int(elapsed)

            # Check for markers
            for marker_time, marker_msg in markers:
                if elapsed_int >= marker_time and last_marker < marker_time:
                    clear_line()
                    print(f"\n🔔 ALERT: {marker_msg}")
                    beep(2)
                    last_marker = marker_time

            # Display current time
            clear_line()
            print(f"⏱  {format_time(elapsed)}", end='', flush=True)

            time.sleep(0.1)

    except KeyboardInterrupt:
        elapsed = time.time() - start_time
        clear_line()
        print(f"\n\n⏹  Roast stopped at {format_time(elapsed)}")
        print(f"Total roast time: {elapsed/60:.1f} minutes\n")

def countdown_timer(minutes, label="Timer"):
    """Simple countdown timer"""
    print(f"\n=== {label.upper()} - {minutes} minutes ===\n")

    total_seconds = minutes * 60
    start_time = time.time()
    end_time = start_time + total_seconds

    try:
        while True:
            now = time.time()
            remaining = end_time - now

            if remaining <= 0:
                clear_line()
                print(f"\n🔔 {label} COMPLETE!")
                beep(3)
                break

            mins = int(remaining // 60)
            secs = int(remaining % 60)

            clear_line()
            print(f"⏱  {mins:02d}:{secs:02d} remaining", end='', flush=True)

            time.sleep(0.1)

    except KeyboardInterrupt:
        clear_line()
        print(f"\n\n⏹  Timer stopped\n")

def rest_timer():
    """Timer for coffee resting period"""
    print("\nCoffee resting timer")
    print("Recommended rest times:")
    print("  - Minimum: 12 hours")
    print("  - Optimal: 24-48 hours")
    print("  - Peak flavor: 2-7 days after roast")

    hours = input("\nSet timer for how many hours? (default: 24): ").strip()
    hours = float(hours) if hours else 24

    if hours > 2:
        print(f"\nRest timer set for {hours} hours")
        print(f"Coffee will be ready at: {(datetime.now() + timedelta(hours=hours)).strftime('%Y-%m-%d %I:%M %p')}")
        print("\n(This is just a notification - no active countdown)")
    else:
        countdown_timer(hours * 60, "Coffee Rest")

def main():
    print("\n=== COFFEE ROAST TIMER ===\n")
    print("1. Roast timer (Regular beans)")
    print("2. Roast timer (Decaf beans)")
    print("3. Cooling timer (5 minutes)")
    print("4. Rest period timer")
    print("5. Custom countdown")
    print("6. Exit")

    choice = input("\nChoice: ").strip()

    if choice == '1':
        roast_timer('regular')
    elif choice == '2':
        roast_timer('decaf')
    elif choice == '3':
        countdown_timer(5, "Cooling")
    elif choice == '4':
        rest_timer()
    elif choice == '5':
        mins = input("Minutes: ").strip()
        label = input("Label (optional): ").strip() or "Timer"
        if mins:
            countdown_timer(float(mins), label)
    elif choice == '6':
        return
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
