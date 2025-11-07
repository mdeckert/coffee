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
3. Press ENTER when you load beans → timer starts, enter loading temps
4. View expected timeline based on your historical data
5. Timer runs with audio alert 45s before expected first crack
6. Press ENTER at first crack START → log temperature and ROR
7. Get reminder to adjust power/fan at FC midpoint
8. Press ENTER at first crack END → log temperature and ROR
9. Press ENTER at second crack START → log temperature and ROR
10. Press ENTER when you drop beans → log end temp, notes
11. Data auto-saves with all details

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
- Real-time timer with intelligent milestone alerts
- Historical data analysis - predicts timing/temps based on past roasts
- Tracks all roast phases: FC start, FC end, second crack, drop
- ROR (Rate of Rise) tracking for precise heat management
- Power/fan adjustment reminders at optimal times
- Auto-logs all data to CSV with 26 data points per roast
- No switching between tools during your roast

**Usage:**
```bash
python3 roast.py
```

**Control Flow:**
1. Answer decaf y/n (bean origin and batch size are preset)
2. Complete pre-roast checklist
3. **Press ENTER** when you load beans, enter loading/turnaround temps
4. View expected timeline with predictions for all phases
5. Timer runs with audio alert before first crack
6. **Press ENTER** at first crack START, enter temp (and optionally ROR)
7. See reminder to adjust power/fan at FC midpoint
8. **Press ENTER** at first crack END, enter temp and ROR
9. **Press ENTER** at second crack START, enter temp and ROR
10. **Press ENTER** when dropping beans, enter end temp
11. Rate roast quality (1-10) and add notes
12. Done! All data saved automatically with historical tracking

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
3. **Load beans:** Press ENTER, enter loading/turnaround temps
4. **Review timeline:** See predicted times/temps for all phases
5. **Monitor roast:** Timer runs, alerts you before first crack
6. **First crack starts:** Press ENTER, log temp/ROR, see power/fan reminder
7. **First crack ends:** Press ENTER, log temp/ROR
8. **Second crack:** Press ENTER, log temp/ROR
9. **Drop beans:** Press ENTER, enter end temp, rate quality, add notes
10. **Done:** All data saved automatically to `roast_log.csv`

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
- **Audio alerts** remind you before first crack (45s advance warning)
- **Historical predictions** show expected timeline based on past roasts
- **Power/fan reminders** prompt adjustments at FC midpoint
- **ROR tracking** helps you manage heat rise rate
- **Stats show patterns** you might miss roast-to-roast
- **Decaf comparison** prevents treating decaf like regular beans
- **Phase tracking** (FC start/end, SC, drop) for precise control

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
Edit `roast.py` and search for `bean_origin = "Colombian"` to change the default origin.

### Adjust Alert Timings
Edit the `get_fc_approaching_time()` function in `roast.py` to change the first crack warning time (default: 45 seconds before).

### Change Audio Sounds
Edit the `beep()` function in `roast.py` - replace sound names with others from `/System/Library/Sounds/`
Available sounds: Ping, Glass, Bottle, Purr, Pop, Funk, Hero, Tink, etc.

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
2. **Historical predictions** - System learns from your roasts and predicts timing/temps
3. **Decaf tracking** - Understand how decaf differs from regular
4. **ROR tracking** - Monitor heat rise rate for better control
5. **Phase granularity** - Track FC start, FC end, SC separately for precision
6. **Consistency feedback** - Stats show if you're getting more consistent
7. **Pattern recognition** - See relationships between time/temp/results
8. **Smart reminders** - Prompts for power/fan adjustments at optimal times
9. **Reference guide** - No guessing about target temps and times

Good luck with your roasting! The more you log, the smarter the predictions become.
