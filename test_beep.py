#!/usr/bin/env python3
"""
Test the beep/bell sound
"""

import time

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

print("Testing beep sounds...\n")

print("Single beep:")
beep(1)
time.sleep(1)

print("\nDouble beep:")
beep(2)
time.sleep(1)

print("\nTriple beep:")
beep(3)

print("\nDone!")
