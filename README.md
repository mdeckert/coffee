# Coffee Roasting Toolkit for Skywalker Roaster

Complete toolkit for tracking, timing, and analyzing your coffee roasts.

## Quick Start

### RECOMMENDED: Use the Integrated Tool

```bash
python3 roast.py               # All-in-one timer + logger
```

**How it works:**
1. Answer: Decaf? (y/n) - that's it!
2. Complete pre-roast checklist (empty chaff, turn off cooling)
3. Press ENTER when you load beans → timer starts with audio alerts
4. Press ENTER at first crack START → log temperature
5. Press ENTER at first crack END → log temperature (when you lower heat)
6. Press ENTER when you drop beans → log end temps
7. Add notes and it auto-saves everything

### Analyze Your Progress

After logging roasts with roast.py:
```bash
python3 roast_stats.py         # View statistics and comparisons
```

---

## Files in This Toolkit

### ⚡ roast.py (RECOMMENDED)
**Integrated timer and logger - the easiest way to track your roasts**

**Features:**
- Real-time timer with automatic milestone alerts
- Three simple control points: Load beans, First crack, Drop beans
- Auto-logs all data to CSV
- No switching between tools during your roast

**Usage:**
```bash
python3 roast.py
```

**Control Flow:**
1. Enter bean info (origin, decaf/regular, batch size)
2. **Press ENTER** when you load beans (starts timer)
3. Timer runs with audio alerts at key times
4. **Press Ctrl+C** at first crack, enter temperature
5. Timer continues showing development time
6. **Press Ctrl+C** when dropping beans, enter temps
7. Add color notes and observations
8. Done! Data saved automatically

### 📊 roast_stats.py
**Statistical analysis of your roasting history**

**Features:**
- Compare decaf vs regular bean performance
- Track averages and consistency
- Identify trends over time
- Variance analysis

**Usage:**
```bash
python3 roast_stats.py
```

**Works with roast.py's CSV output** - analyzes all your logged roasts

---

### 📚 SKYWALKER_GUIDE.md
Complete roasting guide for Colombian beans with your Skywalker roaster.

**Contents:**
- Temperature and timing profiles for regular and decaf beans
- Medium-dark roast targets
- Troubleshooting tips
- Cooling and resting guidelines
- Quick reference card

**Usage:** Open in vi or any text editor to reference during roasting

---

## Typical Workflow

### First Time Setup
1. Read `SKYWALKER_GUIDE.md` to understand your target profile
2. Prepare your beans and roaster

### Each Roast Session
1. **Pre-roast:** Review `SKYWALKER_GUIDE.md`, prepare beans
2. **Start:** Run `python3 roast.py`, answer decaf y/n, complete checklist
3. **Load beans:** Press ENTER → timer starts with audio alerts
4. **First crack starts:** Press ENTER, log temperature
5. **First crack ends:** Press ENTER, log temperature (when you lower heat)
6. **Drop beans:** Press ENTER, log end temps and notes
7. **Done:** Data saved automatically to `roast_log.csv`

### Weekly/Monthly Review
1. Run `roast_stats.py` to analyze progress
2. Compare decaf vs regular performance
3. Check consistency metrics
4. Adjust technique based on data

---

## Tips for Success

### Data Collection
- **Log every roast** - even "bad" ones provide learning data
- **Be consistent** with timing - press ENTER at the same points each time
- **Add tasting notes** after rest period (edit CSV directly with vi)

### Using the Tools
- **Audio alerts** remind you to check key milestones
- **Stats show patterns** you might miss roast-to-roast
- **Decaf comparison** prevents treating decaf like regular beans
- **First crack tracking** helps dial in your temp reduction timing

---

## File Locations

All files in: `/Users/mdeckert/coffee/`

- `roast.py` - Integrated timer + logger (use this!)
- `roast_stats.py` - Analysis and statistics tool
- `SKYWALKER_GUIDE.md` - Roasting reference guide
- `roast_log.csv` - Your roast data (auto-created)
- `README.md` - This file

---

## Customization Ideas

### Change Bean Origin
Edit `roast.py` line 119 to change from "Colombian" to another origin.

### Adjust Alert Timings
Edit the `get_milestones()` function in `roast.py` (around line 278) to change when audio alerts sound.

### Change Audio Sound
Edit line 38 in `roast.py` - replace `Ping.aiff` with another sound from `/System/Library/Sounds/`

### Add Tasting Notes
After coffee has rested:
```bash
vi roast_log.csv
```
Find the roast row and add notes in the "Tasting Notes" column.

### Export Data
The CSV works with Excel, Google Sheets, or any analysis tool:
```bash
open roast_log.csv              # Opens in default app
```

---

## Troubleshooting

### Script won't run
Make sure it's executable:
```bash
chmod +x roast.py roast_stats.py
```

### Can't find roast_log.csv
It's created automatically when you complete your first roast with `roast.py`.

### Audio alerts not working
Check system volume. Alerts use macOS system sounds. Test with:
```bash
afplay /System/Library/Sounds/Ping.aiff
```

### Want to reset data
Backup or delete `roast_log.csv` to start fresh:
```bash
mv roast_log.csv roast_log_backup.csv
```

---

## What Makes This Useful for Learning

1. **Structured data** - Compare roasts objectively, not just by memory
2. **Decaf tracking** - Understand how decaf differs from regular
3. **Consistency feedback** - Stats show if you're getting more consistent
4. **Pattern recognition** - See relationships between time/temp/results
5. **Reference guide** - No guessing about target temps and times

Good luck with your roasting! The more you log, the more useful the stats become.
