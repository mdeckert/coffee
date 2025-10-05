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
                'Yellow Time', 'First Crack Start Time', 'First Crack Start Temp', 'FC Start ROR',
                'First Crack End Time', 'First Crack End Temp', 'FC End ROR',
                'Second Crack Start Time', 'Second Crack Start Temp', 'SC Start ROR',
                'End Time', 'End Temp', 'Drop Temp', 'Total Roast Time (min)', 'Target Roast Level',
                'Roast Level (1-10)', 'Notes', 'Tasting Notes (added later)'
            ])

def format_time(seconds):
    """Format seconds as MM:SS"""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def parse_temp_ror(input_str):
    """Parse temp input with optional ROR. Format: '133:17' = 133°C with ROR 17"""
    if not input_str:
        return None, None

    if ':' in input_str:
        parts = input_str.split(':')
        try:
            temp = parts[0].strip()
            ror = parts[1].strip()
            return temp, ror
        except:
            return input_str, None
    else:
        return input_str, None

def beep(sound='Ping'):
    """Make alert sound with different sounds for different phases"""
    import subprocess
    # Use macOS system sound
    subprocess.run(['afplay', f'/System/Library/Sounds/{sound}.aiff'],
                  stdout=subprocess.DEVNULL,
                  stderr=subprocess.DEVNULL)

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
        self.fc_start_ror = None
        self.fc_end_time = None
        self.fc_end_temp = None
        self.fc_end_ror = None
        self.sc_start_time = None
        self.sc_start_temp = None
        self.sc_start_ror = None
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

    def mark_second_crack_start(self, temp):
        """Mark second crack start"""
        self.sc_start_time = self.elapsed()
        self.sc_start_temp = temp

    def mark_end(self, end_temp, drop_temp):
        """Mark end of roast"""
        self.end_time = self.elapsed()
        self.end_temp = end_temp
        self.drop_temp = drop_temp

def get_fc_midpoint_temp(is_decaf):
    """Calculate FC midpoint temp from historical data"""
    if not os.path.exists(ROAST_LOG_FILE):
        # Default values if no history
        return 186 if is_decaf else 192

    try:
        with open(ROAST_LOG_FILE, 'r') as f:
            reader = csv.DictReader(f)
            rows = [r for r in reader if r.get('Decaf', '').lower() == ('yes' if is_decaf else 'no')]

            if not rows:
                return 186 if is_decaf else 192

            # Get FC start and end temps from recent roasts
            fc_starts = []
            fc_ends = []
            for r in rows[-5:]:  # Last 5 roasts of this type
                fc_start = r.get('First Crack Start Temp') or r.get('First Crack Temp', '')
                fc_end = r.get('First Crack End Temp', '')
                if fc_start:
                    try:
                        fc_starts.append(float(fc_start))
                    except:
                        pass
                if fc_end:
                    try:
                        fc_ends.append(float(fc_end))
                    except:
                        pass

            if fc_starts and fc_ends:
                avg_start = sum(fc_starts) / len(fc_starts)
                avg_end = sum(fc_ends) / len(fc_ends)
                return int((avg_start + avg_end) / 2)
            elif fc_starts:
                # If we only have start temps, add ~8°C for estimated midpoint
                return int(sum(fc_starts) / len(fc_starts) + 4)
            else:
                return 186 if is_decaf else 192
    except:
        return 186 if is_decaf else 192

def get_fc_start_estimates(is_decaf):
    """Get estimated FC start time and temp from historical data"""
    if not os.path.exists(ROAST_LOG_FILE):
        # Default values if no history
        default_time = 480 if is_decaf else 540  # 8:00 for decaf, 9:00 for regular
        default_temp = 186 if is_decaf else 192
        return default_time, default_temp

    try:
        with open(ROAST_LOG_FILE, 'r') as f:
            reader = csv.DictReader(f)
            rows = [r for r in reader if r.get('Decaf', '').lower() == ('yes' if is_decaf else 'no')]

            if not rows:
                default_time = 480 if is_decaf else 540
                default_temp = 186 if is_decaf else 192
                return default_time, default_temp

            # Get FC start times and temps from recent roasts
            fc_start_times = []
            fc_start_temps = []
            for r in rows[-5:]:  # Last 5 roasts of this type
                fc_start_time = r.get('First Crack Start Time') or r.get('First Crack Time', '')
                if fc_start_time and ':' in fc_start_time:
                    try:
                        parts = fc_start_time.split(':')
                        seconds = int(parts[0]) * 60 + int(parts[1])
                        fc_start_times.append(seconds)
                    except:
                        pass

                fc_start_temp = r.get('First Crack Start Temp') or r.get('First Crack Temp', '')
                if fc_start_temp:
                    try:
                        fc_start_temps.append(float(fc_start_temp))
                    except:
                        pass

            avg_time = int(sum(fc_start_times) / len(fc_start_times)) if fc_start_times else (480 if is_decaf else 540)
            avg_temp = int(sum(fc_start_temps) / len(fc_start_temps)) if fc_start_temps else (186 if is_decaf else 192)

            return avg_time, avg_temp
    except:
        default_time = 480 if is_decaf else 540
        default_temp = 186 if is_decaf else 192
        return default_time, default_temp

def get_fc_approaching_time(is_decaf):
    """Calculate when to alert for approaching FC (45s before avg FC start)"""
    fc_start_time, _ = get_fc_start_estimates(is_decaf)
    return fc_start_time - 45

def run_roast_session():
    """Run an interactive roast session"""
    print("\n=== COFFEE ROAST SESSION ===\n")

    # Pre-roast reminders
    print("⚠️  PRE-ROAST CHECKLIST:")
    print("   □ Empty the chaff collector")
    print("   □ Turn OFF cooling mode")
    print("   □ Close the roast chamber")
    beep('Tink')
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

    # Calculate FC midpoint from historical data
    fc_midpoint = get_fc_midpoint_temp(is_decaf)

    # Display target settings
    if is_decaf:
        print("🎯 TARGET SETTINGS (DECAF):")
        print("   Load: 200°C, Power: 80, Fan: 60")
        print(f"   At ~{fc_midpoint}°C (FC midpoint): Power: 30, Fan: 90")
    else:
        print("🎯 TARGET SETTINGS (REGULAR):")
        print("   Load: 215°C, Power: 85, Fan: 60")
        print(f"   At ~{fc_midpoint}°C (FC midpoint): Power: 35, Fan: 85")
    print()

    # Control points
    input("Press ENTER when you LOAD THE BEANS and start the roast...")
    session.start_time = time.time()
    beep('Hero')
    print("\n🔥 ROAST STARTED! (Timer running in background)\n")

    # Collect data right after loading (timer keeps running, just not displaying)
    session.loading_temp = input("Loading temp (°C): ").strip()
    session.turnaround_temp = input("Turnaround temp (°C): ").strip()
    session.early_notes = input("Early notes (optional): ").strip()

    # Get FC estimates from historical data
    fc_est_time, fc_est_temp = get_fc_start_estimates(is_decaf)
    print(f"\nPress ENTER when FIRST CRACK STARTS... (expected ~{format_time(fc_est_time)} @ {fc_est_temp}°C)")

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
                    beep('Ping')
                    last_milestone = milestone_time
                    time.sleep(1)

            # Display timer
            display_timer(elapsed)
            time.sleep(0.1)

    timer_thread = threading.Thread(target=run_timer, daemon=True)
    timer_thread.start()

    # Wait for first crack START
    input()  # User presses ENTER at first crack start

    # Mark the time immediately
    session.fc_start_time = session.elapsed()

    stop_timer.set()
    timer_thread.join(timeout=0.5)

    # First crack START control point
    clear_line()
    print(f"\n⏱  First Crack STARTED at {format_time(session.fc_start_time)}")

    fc_start_input = input("Temperature at first crack start (°C or °C:ROR): ").strip()
    session.fc_start_temp, session.fc_start_ror = parse_temp_ror(fc_start_input)

    print("\n🔊 FIRST CRACK STARTED")
    beep('Glass')

    # Show power/fan adjustment reminder at FC midpoint
    if is_decaf:
        print(f"\n⚡ At ~{fc_midpoint}°C (FC midpoint): Power: 30, Fan: 90")
    else:
        print(f"\n⚡ At ~{fc_midpoint}°C (FC midpoint): Power: 35, Fan: 85")

    # Continue timer until first crack ENDS
    print("\nWhen FIRST CRACK ENDS, press ENTER...\n")
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

    fc_end_input = input("Temperature at first crack end (°C or °C:ROR): ").strip()
    session.fc_end_temp, session.fc_end_ror = parse_temp_ror(fc_end_input)

    print("\n🔊 FIRST CRACK ENDED - Development phase")
    beep('Bottle')

    # Reminder to handle prior roast
    print("\n⚠️  REMINDER: Take care of prior roast beans now!")
    beep('Purr')

    # Continue timer for development - wait for either second crack or drop
    print("\nPress ENTER at SECOND CRACK START (or just drop beans if no 2nd crack)...\n")
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

    # Wait for second crack or drop
    input()  # User presses ENTER

    # Mark the time immediately
    event_time = session.elapsed()

    stop_timer.set()
    dev_timer_thread.join(timeout=0.5)
    clear_line()

    # Ask if this was second crack or drop
    print(f"\n⏱  Event at {format_time(event_time)}")
    was_second_crack = input("Was this SECOND CRACK? (y/n): ").strip().lower() == 'y'

    if was_second_crack:
        # Second crack control point
        print("\n🔊 SECOND CRACK STARTED")
        sc_input = input("Temperature at second crack start (°C or °C:ROR): ").strip()
        session.sc_start_time = event_time
        session.sc_start_temp, session.sc_start_ror = parse_temp_ror(sc_input)
        beep('Pop')

        # Continue to drop
        print("\nWhen you DROP THE BEANS, press ENTER...\n")
        time.sleep(1)

        stop_timer.clear()

        def run_final_timer():
            while not stop_timer.is_set():
                elapsed = session.elapsed()
                sc_time = elapsed - session.sc_start_time
                display_timer(elapsed, f"After 2nd crack: {format_time(sc_time)}")
                time.sleep(0.1)

        final_timer_thread = threading.Thread(target=run_final_timer, daemon=True)
        final_timer_thread.start()

        # Wait for drop
        input()
        session.end_time = session.elapsed()
        stop_timer.set()
        final_timer_thread.join(timeout=0.5)
        clear_line()
        print(f"\n⏱  Beans dropped at {format_time(session.end_time)}")
    else:
        # This was the drop
        session.end_time = event_time
        print(f"\n⏱  Beans dropped at {format_time(session.end_time)}")

    # Get end temp
    end_temp = input("End temperature (°C): ").strip()
    session.end_temp = end_temp

    print("\n✓ ROAST COMPLETE!")
    beep('Funk')

    # Summary
    print(f"\n=== ROAST SUMMARY ===")
    print(f"First Crack Start: {format_time(session.fc_start_time)} @ {session.fc_start_temp}°C")
    print(f"First Crack End: {format_time(session.fc_end_time)} @ {session.fc_end_temp}°C")

    if session.fc_start_time and session.fc_end_time:
        fc_duration = session.fc_end_time - session.fc_start_time
        print(f"First Crack Duration: {format_time(fc_duration)}")

    print(f"Total Time: {format_time(session.end_time)} ({session.end_time/60:.1f} min)")
    print(f"End Temp: {session.end_temp}°C")

    if session.fc_end_time and session.end_time:
        dev_time = session.end_time - session.fc_end_time
        print(f"Development Time (after FC): {format_time(dev_time)} ({dev_time/60:.1f} min)")

    # Get additional notes
    print("\n")
    print("Roast level (1=too light, 5=perfect, 10=burnt):")
    roast_level = input("Rating (1-10): ").strip()
    notes = input("Notes (weather, adjustments, observations): ").strip()

    # Save to log
    save_roast(session, roast_level, notes)

    print("\n✓ Roast logged successfully!")
    print(f"Data saved to {ROAST_LOG_FILE}\n")

def get_milestones(is_decaf):
    """Get time milestones based on bean type and historical data"""
    fc_approaching = get_fc_approaching_time(is_decaf)

    if is_decaf:
        return [
            (270, "4:30 - Yellowing phase checkpoint"),
            (fc_approaching, f"{format_time(fc_approaching)} - Approaching first crack zone!"),
            (600, "10:00 - Listen for 2nd crack! Check sample port for color/oil"),
        ]
    else:
        return [
            (330, "5:30 - Yellowing should be complete"),
            (fc_approaching, f"{format_time(fc_approaching)} - Approaching first crack zone!"),
            (600, "10:00 - Listen for 2nd crack! Check sample port for color/oil"),
        ]

def save_roast(session, roast_level, notes):
    """Save roast to CSV log"""
    initialize_log()

    with open(ROAST_LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        now = datetime.now()

        # Format times as MM:SS
        yellow_time = format_time(session.yellow_time) if session.yellow_time else ""
        fc_start_time = format_time(session.fc_start_time) if session.fc_start_time else ""
        fc_end_time = format_time(session.fc_end_time) if session.fc_end_time else ""
        sc_start_time = format_time(session.sc_start_time) if session.sc_start_time else ""
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
            session.fc_start_ror or '',
            fc_end_time,
            session.fc_end_temp or '',
            session.fc_end_ror or '',
            sc_start_time,
            session.sc_start_temp or '',
            session.sc_start_ror or '',
            end_time,
            session.end_temp or '',
            session.drop_temp or '',
            total_time,
            session.target_level,
            roast_level,
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
        print(f"  First Crack: {row[6]} @ {row[7]}°C")
        print(f"  End: {row[10]} @ {row[11]}°C (drop {row[12]}°C)")
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
