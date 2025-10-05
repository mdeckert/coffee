#!/usr/bin/env python3
"""
Integrated Coffee Roast Timer & Logger
Real-time tracking with simple Enter key control points
"""

import csv
import os
import time
from datetime import datetime

ROAST_LOG_FILE = "roast_log.csv"

def initialize_log():
    """Create log file with headers if it doesn't exist"""
    if not os.path.exists(ROAST_LOG_FILE):
        with open(ROAST_LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Date', 'Time', 'Bean Origin', 'Decaf', 'Batch Size (lbs)',
                'Loading Temp', 'Turnaround Temp', 'Early Notes',
                'Yellow Time', 'First Crack Start Time', 'First Crack Start Temp',
                'First Crack End Time', 'First Crack End Temp',
                'Second Crack Time', 'Second Crack Temp', 'End Time', 'End Temp',
                'Drop Temp', 'Total Roast Time (min)', 'Target Roast Level',
                'Actual Color', 'Notes', 'Tasting Notes (added later)'
            ])

def format_time(seconds):
    """Format seconds as MM:SS"""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def beep(count=1):
    """Make alert sound"""
    import subprocess
    for _ in range(count):
        # Use macOS system sound
        subprocess.run(['afplay', '/System/Library/Sounds/Ping.aiff'],
                      stdout=subprocess.DEVNULL,
                      stderr=subprocess.DEVNULL)
        if count > 1:
            time.sleep(0.3)

def clear_line():
    """Clear current line"""
    print('\r' + ' ' * 80 + '\r', end='', flush=True)

def display_timer(elapsed, label=""):
    """Display current timer"""
    clear_line()
    if label:
        print(f"⏱  {format_time(elapsed)} - {label}", end='', flush=True)
    else:
        print(f"⏱  {format_time(elapsed)}", end='', flush=True)

class RoastSession:
    def __init__(self, bean_origin, is_decaf, batch_size, target_level):
        self.bean_origin = bean_origin
        self.is_decaf = is_decaf
        self.batch_size = batch_size
        self.target_level = target_level

        self.start_time = None
        self.loading_temp = None
        self.turnaround_temp = None
        self.yellow_time = None
        self.fc_start_time = None
        self.fc_start_temp = None
        self.fc_end_time = None
        self.fc_end_temp = None
        self.sc_time = None
        self.sc_temp = None
        self.end_time = None
        self.end_temp = None
        self.drop_temp = None
        self.early_notes = None

    def elapsed(self):
        """Get elapsed time in seconds"""
        if self.start_time:
            return time.time() - self.start_time
        return 0

    def mark_yellow(self):
        """Mark yellowing phase complete"""
        self.yellow_time = self.elapsed()

    def mark_first_crack_start(self, temp):
        """Mark start of first crack"""
        self.fc_start_time = self.elapsed()
        self.fc_start_temp = temp

    def mark_first_crack_end(self, temp):
        """Mark end of first crack"""
        self.fc_end_time = self.elapsed()
        self.fc_end_temp = temp

    def mark_second_crack(self, temp):
        """Mark second crack"""
        self.sc_time = self.elapsed()
        self.sc_temp = temp

    def mark_end(self, end_temp, drop_temp):
        """Mark end of roast"""
        self.end_time = self.elapsed()
        self.end_temp = end_temp
        self.drop_temp = drop_temp

def run_roast_session():
    """Run an interactive roast session"""
    print("\n=== COFFEE ROAST SESSION ===\n")

    # Pre-roast reminders
    print("⚠️  PRE-ROAST CHECKLIST:")
    print("   □ Empty the chaff collector")
    print("   □ Turn OFF cooling mode")
    print("   □ Close the roast chamber")
    beep(1)
    print()
    input("Press ENTER when ready to continue...")
    print()

    # Setup
    bean_origin = "Colombian"  # Fixed origin
    is_decaf = input("Decaf? (y/n, default: n): ").strip().lower() == 'y'
    batch_size = "1"  # Fixed at 1 lb
    target_level = "Medium-Dark"  # Fixed at Medium-Dark

    session = RoastSession(bean_origin, is_decaf, batch_size, target_level)

    print(f"\n{bean_origin} {'DECAF' if is_decaf else 'REGULAR'} - {batch_size} lb")
    print(f"Target: {target_level}\n")

    # Control points
    input("Press ENTER when you LOAD THE BEANS and start the roast...")
    session.start_time = time.time()
    beep(1)
    print("\n🔥 ROAST STARTED!\n")

    # Run timer with milestone checks
    last_milestone = 0
    milestones = get_milestones(is_decaf)

    # Create a background timer thread
    import threading
    import sys

    stop_timer = threading.Event()

    def run_timer():
        last_milestone = 0
        while not stop_timer.is_set():
            elapsed = session.elapsed()

            # Check for milestone alerts
            for milestone_time, message in milestones:
                if elapsed >= milestone_time and last_milestone < milestone_time:
                    display_timer(elapsed, message)
                    beep(2)
                    last_milestone = milestone_time
                    time.sleep(1)

            # Display timer
            display_timer(elapsed)
            time.sleep(0.1)

    timer_thread = threading.Thread(target=run_timer, daemon=True)
    timer_thread.start()

    # Collect early data while timer runs
    print("Enter data while waiting for first crack:")
    session.loading_temp = input("Loading temp (°F): ").strip()
    session.turnaround_temp = input("Turnaround temp (°F): ").strip()
    session.early_notes = input("Early notes (optional): ").strip()

    print("\nWhen FIRST CRACK STARTS, press ENTER...")

    # Wait for first crack START
    input()  # User presses ENTER at first crack start

    # Mark the time immediately
    session.fc_start_time = session.elapsed()

    stop_timer.set()
    timer_thread.join(timeout=0.5)

    # First crack START control point
    clear_line()
    print(f"\n⏱  First Crack STARTED at {format_time(session.fc_start_time)}")

    fc_start_temp = input("Temperature at first crack start (°F): ").strip()
    session.fc_start_temp = fc_start_temp

    print("\n🔊 FIRST CRACK STARTED")
    beep(1)

    # Continue timer until first crack ENDS
    print("\nWhen FIRST CRACK ENDS (lower temp now), press ENTER...\n")
    time.sleep(1)

    stop_timer.clear()

    def run_fc_timer():
        while not stop_timer.is_set():
            elapsed = session.elapsed()
            fc_duration = elapsed - session.fc_start_time
            display_timer(elapsed, f"First Crack: {format_time(fc_duration)}")
            time.sleep(0.1)

    fc_timer_thread = threading.Thread(target=run_fc_timer, daemon=True)
    fc_timer_thread.start()

    # Wait for first crack END
    input()  # User presses ENTER when first crack ends

    # Mark the time immediately
    session.fc_end_time = session.elapsed()

    stop_timer.set()
    fc_timer_thread.join(timeout=0.5)

    # First crack END control point
    clear_line()
    print(f"\n⏱  First Crack ENDED at {format_time(session.fc_end_time)}")

    fc_end_temp = input("Temperature at first crack end (°F): ").strip()
    session.fc_end_temp = fc_end_temp

    print("\n🔊 FIRST CRACK ENDED - Development phase")
    beep(1)

    # Continue timer for development
    print("\nWhen you DROP THE BEANS, press ENTER...\n")
    time.sleep(1)

    stop_timer.clear()

    def run_dev_timer():
        while not stop_timer.is_set():
            elapsed = session.elapsed()
            dev_time = elapsed - session.fc_end_time
            display_timer(elapsed, f"Development: {format_time(dev_time)}")
            time.sleep(0.1)

    dev_timer_thread = threading.Thread(target=run_dev_timer, daemon=True)
    dev_timer_thread.start()

    # Wait for drop
    input()  # User presses ENTER when dropping beans
    stop_timer.set()
    dev_timer_thread.join(timeout=0.5)

    # Drop beans control point
    elapsed = session.elapsed()
    clear_line()
    print(f"\n⏱  Beans dropped at {format_time(elapsed)}")

    end_temp = input("End temperature (°F): ").strip()
    drop_temp = input("Drop/cooling tray temp (°F, or Enter to skip): ").strip()
    session.mark_end(end_temp, drop_temp)

    print("\n✓ ROAST COMPLETE!")
    beep(3)

    # Summary
    print(f"\n=== ROAST SUMMARY ===")
    print(f"First Crack Start: {format_time(session.fc_start_time)} @ {session.fc_start_temp}°F")
    print(f"First Crack End: {format_time(session.fc_end_time)} @ {session.fc_end_temp}°F")

    if session.fc_start_time and session.fc_end_time:
        fc_duration = session.fc_end_time - session.fc_start_time
        print(f"First Crack Duration: {format_time(fc_duration)}")

    print(f"Total Time: {format_time(session.end_time)} ({session.end_time/60:.1f} min)")
    print(f"End Temp: {session.end_temp}°F")

    if session.fc_end_time and session.end_time:
        dev_time = session.end_time - session.fc_end_time
        print(f"Development Time (after FC): {format_time(dev_time)} ({dev_time/60:.1f} min)")

    # Get additional notes
    print("\n")
    actual_color = input("Actual roast color/result: ").strip()
    notes = input("Notes (weather, adjustments, observations): ").strip()

    # Save to log
    save_roast(session, actual_color, notes)

    print("\n✓ Roast logged successfully!")
    print(f"Data saved to {ROAST_LOG_FILE}\n")

def get_milestones(is_decaf):
    """Get time milestones based on bean type"""
    if is_decaf:
        return [
            (240, "4:00 - Yellowing phase checkpoint"),
            (360, "6:00 - Approaching first crack zone (decaf)"),
            (480, "8:00 - Listen for first crack!"),
        ]
    else:
        return [
            (300, "5:00 - Yellowing should be complete"),
            (480, "8:00 - Approaching first crack zone"),
            (540, "9:00 - Listen for first crack!"),
        ]

def save_roast(session, actual_color, notes):
    """Save roast to CSV log"""
    initialize_log()

    with open(ROAST_LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        now = datetime.now()

        # Format times as MM:SS
        yellow_time = format_time(session.yellow_time) if session.yellow_time else ""
        fc_start_time = format_time(session.fc_start_time) if session.fc_start_time else ""
        fc_end_time = format_time(session.fc_end_time) if session.fc_end_time else ""
        sc_time = format_time(session.sc_time) if session.sc_time else ""
        end_time = format_time(session.end_time) if session.end_time else ""
        total_time = f"{session.end_time/60:.1f}" if session.end_time else ""

        writer.writerow([
            now.strftime('%Y-%m-%d'),
            now.strftime('%H:%M'),
            session.bean_origin,
            'Yes' if session.is_decaf else 'No',
            session.batch_size,
            session.loading_temp or '',
            session.turnaround_temp or '',
            session.early_notes or '',
            yellow_time,
            fc_start_time,
            session.fc_start_temp or '',
            fc_end_time,
            session.fc_end_temp or '',
            sc_time,
            session.sc_temp or '',
            end_time,
            session.end_temp or '',
            session.drop_temp or '',
            total_time,
            session.target_level,
            actual_color,
            notes,
            ''  # Tasting notes placeholder
        ])

def view_recent_roasts(n=5):
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
    while True:
        print("\n=== COFFEE ROAST TRACKER ===\n")
        print("1. Start new roast session")
        print("2. View recent roasts")
        print("3. Exit")

        choice = input("\nChoice: ").strip()

        if choice == '1':
            run_roast_session()
        elif choice == '2':
            n = input("How many recent roasts to show (default: 5): ").strip()
            view_recent_roasts(int(n) if n else 5)
        elif choice == '3':
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
