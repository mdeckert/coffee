# Coffee Roasting Toolkit for Skywalker Roaster

Complete toolkit for tracking, timing, and analyzing your coffee roasts.

## Quick Start

### 1. Before Your Roast
Read the guide and optionally start the timer:
```bash
vi SKYWALKER_GUIDE.md          # Read roasting guidelines
python3 roast_timer.py         # Optional: Start timer with alerts
```

### 2. During Your Roast
Use the timer to get alerts at key stages (first crack, development phase, etc.)

### 3. After Your Roast
Log your roast data:
```bash
python3 roast_logger.py        # Log roast details
```

### 4. Analyze Your Progress
Review statistics and trends:
```bash
python3 roast_stats.py         # View statistics and comparisons
```

---

## Files in This Toolkit

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

### Each Roast Session
1. **Pre-roast:** Review guide, decide on regular or decaf profile
2. **During roast:**
   - Run `roast_timer.py` for alerts (optional but helpful)
   - Monitor temps and listen for cracks
   - Take notes on anything unusual
3. **Post-roast:**
   - Cool beans rapidly (4-5 min)
   - Run `roast_logger.py` to record data while fresh in memory
   - Note observations: color, smell, any issues

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

- `SKYWALKER_GUIDE.md` - Roasting reference guide
- `roast_logger.py` - Logging tool
- `roast_stats.py` - Analysis tool
- `roast_timer.py` - Timer with alerts
- `roast_log.csv` - Your roast data (created on first use)
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
