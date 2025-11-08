#!/usr/bin/env python3
"""
Check roast predictions before and after data import
"""
import csv
import os

ROAST_LOG_FILE = "roast_log.csv"

def calculate_roast_quality_weight(roast_level, ideal=5):
    """
    Calculate quality weight for a roast based on its level rating.
    Roasts closer to the ideal rating (default 5) get higher weight.

    Weight = 1 / (|roast_level - ideal| + 1)

    Examples:
    - Rating 5 (perfect): weight = 1.0
    - Rating 4 or 6: weight = 0.5
    - Rating 3 or 7: weight = 0.33
    - Rating 1 or 10: weight = 0.2 or 0.167
    """
    if not roast_level:
        return 0.0
    try:
        level = float(roast_level)
        return 1.0 / (abs(level - ideal) + 1.0)
    except:
        return 0.0

def weighted_average(values, weights):
    """
    Calculate weighted average of values.
    Returns None if no valid values/weights.
    """
    if not values or not weights or len(values) != len(weights):
        return None

    # Filter out zero weights
    valid_pairs = [(v, w) for v, w in zip(values, weights) if w > 0]
    if not valid_pairs:
        return None

    values, weights = zip(*valid_pairs)
    total_weight = sum(weights)
    if total_weight == 0:
        return None

    return sum(v * w for v, w in zip(values, weights)) / total_weight

def parse_time_to_seconds(time_str):
    """Convert MM:SS to seconds"""
    if not time_str or ':' not in time_str:
        return None
    try:
        parts = time_str.split(':')
        return int(parts[0]) * 60 + int(parts[1])
    except:
        return None

def parse_temp(temp_str):
    """Parse temperature value"""
    if not temp_str:
        return None
    try:
        return float(temp_str)
    except:
        return None

def get_all_phase_estimates(is_decaf, log_file=ROAST_LOG_FILE):
    """Get estimated times and temps for all roast phases from historical data"""
    if not os.path.exists(log_file):
        return None

    try:
        with open(log_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = [r for r in reader if r.get('Decaf', '').lower() == ('yes' if is_decaf else 'no')]

            if not rows:
                return None

            recent_rows = rows[-5:]  # Last 5 roasts of this type

            # Collect data for each phase with quality weights
            turnaround_temps = []
            turnaround_weights = []
            fc_start_times = []
            fc_start_time_weights = []
            fc_start_temps = []
            fc_start_temp_weights = []
            fc_end_times = []
            fc_end_time_weights = []
            fc_end_temps = []
            fc_end_temp_weights = []
            sc_start_times = []
            sc_start_time_weights = []
            sc_start_temps = []
            sc_start_temp_weights = []
            end_times = []
            end_time_weights = []
            end_temps = []
            end_temp_weights = []

            for r in recent_rows:
                # Get quality weight for this roast
                roast_level = r.get('Roast Level (1-10)', '')
                weight = calculate_roast_quality_weight(roast_level)

                if weight > 0:
                    # Turnaround temp
                    tt = parse_temp(r.get('Turnaround Temp', ''))
                    if tt:
                        turnaround_temps.append(tt)
                        turnaround_weights.append(weight)

                    # FC start time (try new format first, then old)
                    fct = parse_time_to_seconds(r.get('First Crack Start Time', '')) or parse_time_to_seconds(r.get('First Crack Time', ''))
                    if fct:
                        fc_start_times.append(fct)
                        fc_start_time_weights.append(weight)

                    # FC start temp (try new format first, then old)
                    fctemp = parse_temp(r.get('First Crack Start Temp', '')) or parse_temp(r.get('First Crack Temp', ''))
                    if fctemp:
                        fc_start_temps.append(fctemp)
                        fc_start_temp_weights.append(weight)

                    # FC end time
                    fcet = parse_time_to_seconds(r.get('First Crack End Time', ''))
                    if fcet:
                        fc_end_times.append(fcet)
                        fc_end_time_weights.append(weight)

                    # FC end temp
                    fcemp = parse_temp(r.get('First Crack End Temp', ''))
                    if fcemp:
                        fc_end_temps.append(fcemp)
                        fc_end_temp_weights.append(weight)

                    # SC start time (try new format first, then old)
                    sct = parse_time_to_seconds(r.get('Second Crack Start Time', '')) or parse_time_to_seconds(r.get('Second Crack Time', ''))
                    if sct:
                        sc_start_times.append(sct)
                        sc_start_time_weights.append(weight)

                    # SC start temp (try new format first, then old)
                    sctemp = parse_temp(r.get('Second Crack Start Temp', '')) or parse_temp(r.get('Second Crack Temp', ''))
                    if sctemp:
                        sc_start_temps.append(sctemp)
                        sc_start_temp_weights.append(weight)

                    # End time
                    et = parse_time_to_seconds(r.get('End Time', ''))
                    if et:
                        end_times.append(et)
                        end_time_weights.append(weight)

                    # End temp
                    etemp = parse_temp(r.get('End Temp', ''))
                    if etemp:
                        end_temps.append(etemp)
                        end_temp_weights.append(weight)

            return {
                'num_roasts': len(recent_rows),
                'turnaround_temp': weighted_average(turnaround_temps, turnaround_weights),
                'fc_start_time': weighted_average(fc_start_times, fc_start_time_weights),
                'fc_start_temp': weighted_average(fc_start_temps, fc_start_temp_weights),
                'fc_end_time': weighted_average(fc_end_times, fc_end_time_weights),
                'fc_end_temp': weighted_average(fc_end_temps, fc_end_temp_weights),
                'sc_start_time': weighted_average(sc_start_times, sc_start_time_weights),
                'sc_start_temp': weighted_average(sc_start_temps, sc_start_temp_weights),
                'end_time': weighted_average(end_times, end_time_weights),
                'end_temp': weighted_average(end_temps, end_temp_weights),
                'raw_data': {
                    'fc_start_times': fc_start_times,
                    'fc_start_temps': fc_start_temps,
                    'fc_end_times': fc_end_times,
                    'fc_end_temps': fc_end_temps,
                    'sc_start_times': sc_start_times,
                    'sc_start_temps': sc_start_temps,
                    'end_times': end_times,
                    'end_temps': end_temps
                }
            }
    except Exception as e:
        print(f"Error: {e}")
        return None

def format_time(seconds):
    """Format seconds as MM:SS"""
    if seconds is None:
        return "N/A"
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def print_estimates(estimates, label):
    """Print phase estimates in a readable format"""
    print(f"\n{label}")
    print("="*60)
    if not estimates:
        print("No data available")
        return

    print(f"Based on last {estimates['num_roasts']} roasts:")
    print(f"  Turnaround Temp:  {estimates['turnaround_temp']:.1f}°C" if estimates['turnaround_temp'] else "  Turnaround Temp:  N/A")
    print(f"  FC Start:         {format_time(estimates['fc_start_time'])} @ {estimates['fc_start_temp']:.1f}°C" if estimates['fc_start_time'] and estimates['fc_start_temp'] else "  FC Start:         N/A")
    print(f"  FC End:           {format_time(estimates['fc_end_time'])} @ {estimates['fc_end_temp']:.1f}°C" if estimates['fc_end_time'] and estimates['fc_end_temp'] else "  FC End:           N/A")
    print(f"  SC Start:         {format_time(estimates['sc_start_time'])} @ {estimates['sc_start_temp']:.1f}°C" if estimates['sc_start_time'] and estimates['sc_start_temp'] else "  SC Start:         N/A")
    print(f"  Drop:             {format_time(estimates['end_time'])} @ {estimates['end_temp']:.1f}°C" if estimates['end_time'] and estimates['end_temp'] else "  Drop:             N/A")

def compare_estimates(before, after, tolerance=0.15):
    """Compare two sets of estimates and check if within tolerance"""
    if not before or not after:
        print("\nCannot compare - missing data")
        return True

    print(f"\n{'Metric':<20} {'Before':<15} {'After':<15} {'Change':<15} {'Status'}")
    print("="*80)

    all_within_tolerance = True

    metrics = [
        ('turnaround_temp', '°C', lambda x: f"{x:.1f}"),
        ('fc_start_time', 's', lambda x: format_time(x)),
        ('fc_start_temp', '°C', lambda x: f"{x:.1f}"),
        ('fc_end_time', 's', lambda x: format_time(x)),
        ('fc_end_temp', '°C', lambda x: f"{x:.1f}"),
        ('sc_start_time', 's', lambda x: format_time(x)),
        ('sc_start_temp', '°C', lambda x: f"{x:.1f}"),
        ('end_time', 's', lambda x: format_time(x)),
        ('end_temp', '°C', lambda x: f"{x:.1f}"),
    ]

    for metric, unit, formatter in metrics:
        b_val = before.get(metric)
        a_val = after.get(metric)

        if b_val is None or a_val is None:
            print(f"{metric:<20} {'N/A':<15} {'N/A':<15} {'N/A':<15} SKIP")
            continue

        change_pct = abs((a_val - b_val) / b_val) * 100
        status = "✓ OK" if change_pct <= tolerance * 100 else "✗ EXCEEDS"

        if change_pct > tolerance * 100:
            all_within_tolerance = False

        print(f"{metric:<20} {formatter(b_val):<15} {formatter(a_val):<15} {change_pct:>6.1f}%{'':<8} {status}")

    return all_within_tolerance

if __name__ == "__main__":
    print("CURRENT PREDICTIONS (before import)")
    print("\nRegular (Caffeinated) Roasts:")
    regular_before = get_all_phase_estimates(is_decaf=False)
    print_estimates(regular_before, "Regular Predictions")

    print("\n\nDecaf Roasts:")
    decaf_before = get_all_phase_estimates(is_decaf=True)
    print_estimates(decaf_before, "Decaf Predictions")
