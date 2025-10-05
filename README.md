# Coffee Roasting Toolkit for Skywalker Roaster

Complete toolkit for tracking, timing, and analyzing your coffee roasts.

## Quick Start

### RECOMMENDED: Use the Integrated Tool

```bash
python3 roast.py               # All-in-one timer + logger
```

**How it works:**
1. Answer setup questions (bean type, decaf/regular, etc.)
2. Press ENTER when you load beans → timer starts
3. Press Ctrl+C at first crack → log temperature
4. Press Ctrl+C when you drop beans → log end temps
5. Add notes and it auto-saves everything

### Alternative: Use Separate Tools

**Before your roast:**
```bash
vi SKYWALKER_GUIDE.md          # Read roasting guidelines
```

**During your roast:**
```bash
python3 roast_timer.py         # Timer with alerts
```

**After your roast:**
```bash
python3 roast_logger.py        # Manual logging
```

**Analyze your progress:**
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

### 🪵 roast_logger.py
Interactive logging tool for recording roast data.

**Features:**
- Records all roast parameters (temps, times, bean type)
- Tracks decaf vs regular beans separately
- Creates CSV log file for analysis
- View recent roast history

**Usage:**
```bash
python3 roast_logger.py
```

**Data logged:**
- Date, time, bean origin, decaf/regular
- Yellow phase, first crack, second crack timings
- Temperature at each stage
- Total roast time
- Target vs actual roast level
- Notes and observations

**Output:** Creates `roast_log.csv` in this directory

---

### 📊 roast_stats.py
Statistical analysis of your roasting history.

**Features:**
- Compare decaf vs regular bean performance
- Track averages and consistency
- Identify trends over time
- Variance analysis

**Usage:**
```bash
python3 roast_stats.py
```

**Metrics:**
- Average first crack time/temp
- Average total roast time
- Average development time
- Consistency measurements (standard deviation)
- Decaf vs regular comparisons

---

### ⏱️ roast_timer.py
Real-time timer with audio alerts for roast stages.

**Features:**
- Separate profiles for regular and decaf beans
- Audio alerts at key milestones
- Cooling timer (5 min recommended)
- Rest period timer
- Custom countdown timers

**Usage:**
```bash
python3 roast_timer.py
```

**Alerts at:**
- Yellowing/drying phase completion
- First crack window
- Development phase
- Target drop time zones
- Custom milestones

---

## Typical Workflow

### First Time Setup
1. Read `SKYWALKER_GUIDE.md` to understand your target profile
2. Prepare your beans and roaster

### Each Roast Session (with roast.py)
1. **Pre-roast:** Review `SKYWALKER_GUIDE.md`, prepare beans and roaster
2. **Start:** Run `python3 roast.py` and answer setup questions
3. **Load beans:** Press ENTER to start timer
4. **First crack:** Press Ctrl+C and log temperature
5. **Drop beans:** Press Ctrl+C and log end temps
6. **Add notes:** Enter observations while cooling beans
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
- **Be consistent** with measurements for better analysis
- **Add tasting notes** after rest period (edit CSV directly)

### Using the Tools
- **Timer alerts** help you catch first crack and avoid over-roasting
- **Stats show patterns** you might miss roast-to-roast
- **Decaf comparison** prevents treating decaf like regular beans

### Vi-Friendly Workflow
Since you like vi:
```bash
vi SKYWALKER_GUIDE.md          # Reference during roast
python3 roast_timer.py         # Timer in one terminal
python3 roast_logger.py        # Logger in another terminal
vi roast_log.csv               # Edit/review logged data
```

---

## File Locations

All files in: `/Users/mdeckert/coffee/`

- `roast.py` - **RECOMMENDED** Integrated timer + logger
- `SKYWALKER_GUIDE.md` - Roasting reference guide
- `roast_stats.py` - Analysis tool
- `roast_log.csv` - Your roast data (created on first use)
- `roast_logger.py` - Manual logging tool (use roast.py instead)
- `roast_timer.py` - Standalone timer (use roast.py instead)
- `README.md` - This file

---

## Customization Ideas

### Modify the Timer
Edit `roast_timer.py` to adjust alert times for your specific roaster's behavior.

### Add Tasting Notes
After coffee has rested and you've tasted it:
```bash
vi roast_log.csv
```
Find the roast row and add notes in the "Tasting Notes" column.

### Track Other Origins
The logger and stats work with any bean origin, not just Colombian. Just enter the origin when logging.

### Export Data
The CSV file works with Excel, Google Sheets, or any data analysis tool:
```bash
open roast_log.csv              # Opens in default app
```

---

## Troubleshooting

### Scripts won't run
Make sure they're executable:
```bash
chmod +x roast_logger.py roast_stats.py roast_timer.py
```

### Can't find roast_log.csv
It's created automatically when you log your first roast with `roast_logger.py`.

### Timer alerts not working
Audio alerts use system beep. If silent, check system volume and terminal bell settings.

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
