#!/usr/bin/env python3
"""
Demonstrate the weighted averaging algorithm
"""

def calculate_roast_quality_weight(roast_level, ideal=5):
    """Calculate quality weight based on distance from ideal rating"""
    if not roast_level:
        return 0.0
    try:
        level = float(roast_level)
        return 1.0 / (abs(level - ideal) + 1.0)
    except:
        return 0.0

def weighted_average(values, weights):
    """Calculate weighted average"""
    if not values or not weights or len(values) != len(weights):
        return None

    valid_pairs = [(v, w) for v, w in zip(values, weights) if w > 0]
    if not valid_pairs:
        return None

    values, weights = zip(*valid_pairs)
    total_weight = sum(weights)
    if total_weight == 0:
        return None

    return sum(v * w for v, w in zip(values, weights)) / total_weight

# Example: 5 roasts with different quality levels and FC start times
print("=" * 60)
print("WEIGHTED AVERAGING DEMONSTRATION")
print("=" * 60)

# Example roast data
roasts = [
    {"rating": 3, "fc_start_time": 400},  # Too light, FC happened early
    {"rating": 5, "fc_start_time": 440},  # Perfect!
    {"rating": 5, "fc_start_time": 438},  # Perfect!
    {"rating": 7, "fc_start_time": 480},  # Too dark, FC happened late
    {"rating": 8, "fc_start_time": 500},  # Way too dark, FC happened very late
]

print("\nRoast Data:")
print(f"{'Roast':<8} {'Rating':<10} {'FC Time':<12} {'Weight':<10}")
print("-" * 60)

fc_times = []
weights = []

for i, roast in enumerate(roasts, 1):
    weight = calculate_roast_quality_weight(roast["rating"])
    fc_times.append(roast["fc_start_time"])
    weights.append(weight)

    print(f"#{i:<7} {roast['rating']:<10} {roast['fc_start_time']} sec{'':<7} {weight:.3f}")

print("\n" + "=" * 60)
print("COMPARISON: Simple Average vs Weighted Average")
print("=" * 60)

# Simple average (equal weight to all roasts)
simple_avg = sum(fc_times) / len(fc_times)

# Weighted average (favors roasts closer to rating 5)
weighted_avg = weighted_average(fc_times, weights)

print(f"\nSimple Average (treats all roasts equally):")
print(f"  FC Start Time: {simple_avg:.1f} seconds ({int(simple_avg//60)}:{int(simple_avg%60):02d})")

print(f"\nWeighted Average (favors perfect roasts):")
print(f"  FC Start Time: {weighted_avg:.1f} seconds ({int(weighted_avg//60)}:{int(weighted_avg%60):02d})")

print(f"\nDifference: {abs(weighted_avg - simple_avg):.1f} seconds")

print("\n" + "=" * 60)
print("EXPLANATION")
print("=" * 60)
print("""
The weighted average gives more influence to roasts rated closer to 5 (perfect).
In this example:
- Roasts #2 and #3 (rating 5) get full weight (1.0)
- Roast #1 (rating 3) gets weight 0.33
- Roast #4 (rating 7) gets weight 0.33
- Roast #5 (rating 8) gets weight 0.25

This means the two perfect roasts dominate the prediction, pulling it
toward their FC start times (438-440 sec) and away from the outliers
(400 sec and 480-500 sec from the imperfect roasts).
""")
