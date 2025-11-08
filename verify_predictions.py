#!/usr/bin/env python3
"""
Verify predictions after migration
"""
import sys
sys.path.insert(0, '.')
from check_predictions import get_all_phase_estimates, print_estimates, compare_estimates

# Before migration (we know from earlier run)
regular_before = None  # No data before
decaf_before = {
    'num_roasts': 2,
    'turnaround_temp': 101.0,
    'fc_start_time': 439.0,  # 07:19
    'fc_start_temp': 186.5,
    'fc_end_time': 516.0,  # 08:36
    'fc_end_temp': 199.5,
    'sc_start_time': 694.0,  # 11:34
    'sc_start_temp': 214.5,
    'end_time': 760.0,  # 12:40
    'end_temp': 217.5
}

# After migration
print("="*70)
print("PREDICTIONS AFTER MIGRATION")
print("="*70)

print("\n\nRegular (Caffeinated) Roasts:")
regular_after = get_all_phase_estimates(is_decaf=False)
print_estimates(regular_after, "Regular Predictions")

print("\n\nDecaf Roasts:")
decaf_after = get_all_phase_estimates(is_decaf=True)
print_estimates(decaf_after, "Decaf Predictions")

# Compare
print("\n\n" + "="*70)
print("VERIFICATION: Changes should be within 15% tolerance")
print("="*70)

print("\n" + "-"*70)
print("REGULAR ROASTS: Before vs After")
print("-"*70)
if regular_before is None:
    print("No previous data for regular roasts - this is NEW data ✓")
    print("Successfully added predictions for caffeinated roasts!")
else:
    compare_estimates(regular_before, regular_after, tolerance=0.15)

print("\n" + "-"*70)
print("DECAF ROASTS: Before vs After")
print("-"*70)
all_ok = compare_estimates(decaf_before, decaf_after, tolerance=0.15)

print("\n" + "="*70)
if all_ok:
    print("✓ VERIFICATION PASSED: All changes within 15% tolerance")
else:
    print("⚠ WARNING: Some changes exceed 15% tolerance")
    print("  This may indicate incorrect data import")
print("="*70)
