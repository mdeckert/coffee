# Technical Documentation - Coffee Roast Logger

## CSV Data Format Evolution

### Version 1 (Legacy Format) - 18 Columns

**File**: `old_roast_log.csv`

**Format**: Simple tracking of key milestone times and temperatures

```
Date,Time,Bean Origin,Decaf,Batch Size (lbs),Yellow Time,First Crack Time,First Crack Temp,Second Crack Time,Second Crack Temp,End Time,End Temp,Drop Temp,Total Roast Time (min),Target Roast Level,Actual Color,Notes,Tasting Notes (added later)
```

#### Column Definitions (V1)

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| Date | YYYY-MM-DD | Roast date | 2025-10-05 |
| Time | HH:MM | Roast start time | 12:51 |
| Bean Origin | String | Coffee origin | Colombian |
| Decaf | Yes/No | Decaf or regular | No |
| Batch Size (lbs) | Number | Batch size in pounds | 1 |
| Yellow Time | MM:SS | Time when yellowing complete | 06:33 |
| First Crack Time | MM:SS | When first crack occurred | 06:33 |
| First Crack Temp | Number (°C) | Temperature at first crack | 190 |
| Second Crack Time | MM:SS | When second crack occurred | 08:07 |
| Second Crack Temp | Number (°C) | Temperature at second crack | 205 |
| End Time | MM:SS | When beans dropped | 10:38 |
| End Temp | Number (°C) | Temperature when dropped | 221 |
| Drop Temp | Number (°C) | Temperature after drop | - |
| Total Roast Time (min) | Decimal | Total duration in minutes | 10.6 |
| Target Roast Level | String | Intended roast level | Medium-Dark |
| Actual Color | Number | Color rating | - |
| Notes | String | Observations during roast | A bit too dark and shiny |
| Tasting Notes | String | Added after rest period | - |

#### Limitations of V1
- Single timestamp for first crack (doesn't capture duration)
- Single timestamp for second crack (doesn't capture duration)
- No ROR (Rate of Rise) data
- No loading temperature tracking
- No turnaround temperature tracking
- No distinction between crack start and end
- Limited pre-roast setup tracking

---

### Version 2 (Current Format) - 26 Columns

**File**: `roast_log.csv`

**Format**: Comprehensive tracking with phase granularity and ROR data

```
Date,Time,Bean Origin,Decaf,Batch Size (lbs),Loading Temp,Turnaround Temp,Early Notes,Yellow Time,First Crack Start Time,First Crack Start Temp,FC Start ROR,First Crack End Time,First Crack End Temp,FC End ROR,Second Crack Start Time,Second Crack Start Temp,SC Start ROR,End Time,End Temp,Drop Temp,Total Roast Time (min),Target Roast Level,Roast Level (1-10),Notes,Tasting Notes (added later)
```

#### Column Definitions (V2)

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| Date | YYYY-MM-DD | Roast date | 2025-11-07 |
| Time | HH:MM | Roast start time | 15:06 |
| Bean Origin | String | Coffee origin | Colombian |
| Decaf | Yes/No | Decaf or regular | Yes |
| Batch Size (lbs) | Number | Batch size in pounds | 1 |
| **Loading Temp** | Number (°C) | Temperature when beans loaded | 200 |
| **Turnaround Temp** | Number (°C) | Lowest temp after loading | 95 |
| **Early Notes** | String | Pre-roast observations | power/far reversed |
| Yellow Time | MM:SS | Time when yellowing complete | - |
| **First Crack Start Time** | MM:SS | When FC begins | 07:33 |
| **First Crack Start Temp** | Number (°C) | Temperature at FC start | 183 |
| **FC Start ROR** | Number (°C/min) | Rate of rise at FC start | 13 |
| **First Crack End Time** | MM:SS | When FC ends | 08:29 |
| **First Crack End Temp** | Number (°C) | Temperature at FC end | 196 |
| **FC End ROR** | Number (°C/min) | Rate of rise at FC end | 12 |
| **Second Crack Start Time** | MM:SS | When SC begins | 11:37 |
| **Second Crack Start Temp** | Number (°C) | Temperature at SC start | 212 |
| **SC Start ROR** | Number (°C/min) | Rate of rise at SC start | 5 |
| End Time | MM:SS | When beans dropped | 12:52 |
| End Temp | Number (°C) | Temperature when dropped | 215 |
| Drop Temp | Number (°C) | Temperature after drop (unused) | - |
| Total Roast Time (min) | Decimal | Total duration in minutes | 12.9 |
| Target Roast Level | String | Intended roast level | Medium-Dark |
| **Roast Level (1-10)** | Number | Quality rating (1=bad, 10=perfect) | 5 |
| Notes | String | Observations during roast | good |
| Tasting Notes | String | Added after rest period | - |

**New columns in V2** are shown in **bold** above.

#### Improvements in V2
- **Phase granularity**: Separate tracking of crack start/end times
- **ROR tracking**: Rate of Rise data at each phase for heat management
- **Pre-roast data**: Loading temp, turnaround temp, early notes
- **Quality rating**: Numerical 1-10 scale for objective comparison
- **FC duration**: Can calculate first crack duration (FC End - FC Start)
- **SC duration**: Can calculate second crack duration (End - SC Start)
- **Historical analysis**: More data points enable better predictions

---

## Data Collection Process (V2)

### Real-time Data Entry Points

1. **Load Beans** → Enter:
   - Loading Temp
   - Turnaround Temp
   - Early Notes (optional)

2. **First Crack Starts** → Enter:
   - First Crack Start Time (auto-recorded)
   - First Crack Start Temp
   - FC Start ROR (optional, format: `temp:ror` like `183:13`)

3. **First Crack Ends** → Enter:
   - First Crack End Time (auto-recorded)
   - First Crack End Temp
   - FC End ROR (format: `temp:ror`)

4. **Second Crack Starts** → Enter:
   - Second Crack Start Time (auto-recorded)
   - Second Crack Start Temp
   - SC Start ROR (format: `temp:ror`)

5. **Drop Beans** → Enter:
   - End Time (auto-recorded)
   - End Temp

6. **Post-Roast** → Enter:
   - Roast Level (1-10)
   - Notes

### Temperature/ROR Input Format

Temperatures can be entered in two formats:
- **Simple**: `190` (just temperature in °C)
- **With ROR**: `190:15` (temp:ROR where ROR is °C/min)

The system parses both formats automatically.

---

## Historical Data Analysis

### Predictive Features

The system analyzes the last 5 roasts of each bean type (decaf/regular) to predict:

1. **Turnaround Time**: ~1:00 (not tracked in CSV, uses typical value)
2. **Yellow Time**: Average of historical yellow times
3. **FC Start Time**: Average of historical first crack start times
4. **FC Start Temp**: Average of historical first crack start temps
5. **FC End Time**: Average of historical first crack end times
6. **FC End Temp**: Average of historical first crack end temps
7. **SC Start Time**: Average of historical second crack start times
8. **SC Start Temp**: Average of historical second crack start temps
9. **End Time**: Average of historical drop times
10. **End Temp**: Average of historical drop temps

### FC Midpoint Calculation

Used for power/fan adjustment reminders:
- **Midpoint Time** = (FC Start Time + FC End Time) / 2
- **Midpoint Temp** = (FC Start Temp + FC End Temp) / 2

Example for decaf:
- FC Start: 07:33 @ 183°C
- FC End: 08:29 @ 196°C
- **Midpoint**: 08:01 @ 189°C ← Adjust power/fan here

---

## Migration from V1 to V2

### Backward Compatibility

The code reads both formats:
```python
# Try new format first, then fall back to old format
fc_start_time = r.get('First Crack Start Time', '') or r.get('First Crack Time', '')
fc_start_temp = r.get('First Crack Start Temp', '') or r.get('First Crack Temp', '')
```

### Data Mapping

| V1 Column | V2 Column | Mapping Notes |
|-----------|-----------|---------------|
| Yellow Time | Yellow Time | Direct copy |
| First Crack Time | First Crack Start Time | V1 time becomes V2 start time |
| First Crack Temp | First Crack Start Temp | V1 temp becomes V2 start temp |
| - | First Crack End Time | Not available in V1 |
| - | First Crack End Temp | Not available in V1 |
| Second Crack Time | Second Crack Start Time | V1 time becomes V2 start time |
| Second Crack Temp | Second Crack Start Temp | V1 temp becomes V2 start temp |
| End Time | End Time | Direct copy |
| End Temp | End Temp | Direct copy |

### Missing Data in V1

When reading V1 format, these fields are unavailable:
- Loading Temp
- Turnaround Temp
- Early Notes
- FC Start ROR
- First Crack End Time/Temp/ROR
- SC Start ROR
- Roast Level (1-10)

---

## Audio Alert System

### Alert Timing

| Alert | Timing | Sound | Purpose |
|-------|--------|-------|---------|
| Pre-roast checklist | Before loading | Tink | Reminder to empty chaff, disable cooling |
| Beans loaded | At load time | Hero | Confirms timer started |
| FC Approaching | 45s before predicted FC | Ping | Prepare for first crack |
| FC Started | User input | Glass | Confirms FC logged |
| Power/Fan Reminder | After FC start data | Purr | Remind to adjust at midpoint |
| FC Ended | User input | Bottle | Confirms FC end logged |
| Handle prior roast | After FC end | Purr | Reminder for previous batch |
| SC Started | User input | Pop | Confirms SC logged |
| Beans dropped | At drop time | Funk | Roast complete |

### Alert Calculation

**FC Approaching Alert**:
```python
fc_approaching_time = avg_fc_start_time - 45  # 45 seconds before
```

Example:
- Decaf FC Start averages 7:19 (439s)
- Alert triggers at 6:34 (394s)
- Gives 45s warning to prepare

---

## File Structure

```
/Users/mdeckert/coffee/
├── roast.py                    # Main integrated timer + logger
├── roast_stats.py              # Statistical analysis tool
├── roast_log.csv               # Current data (V2 format)
├── old_roast_log.csv           # Legacy data (V1 format)
├── roast_log_backup.csv        # Backup before migration
├── README.md                   # User documentation
├── SKYWALKER_GUIDE.md          # Roasting technique guide
└── TECHNICAL.md                # This file
```

---

## Code Architecture

### Key Functions

#### Data Analysis
- `get_all_phase_estimates(is_decaf)` - Analyzes last 5 roasts for predictions
- `get_fc_start_estimates(is_decaf)` - Estimates FC start time/temp
- `get_fc_midpoint_temp(is_decaf)` - Calculates FC midpoint temp
- `get_fc_approaching_time(is_decaf)` - Calculates alert timing

#### Session Management
- `RoastSession` - Stores current roast data
- `run_roast_session()` - Main interactive session loop
- `save_roast()` - Writes data to CSV

#### User Interface
- `display_timer(elapsed, label)` - Shows running timer
- `beep(sound)` - Plays audio alerts
- `get_milestones(is_decaf)` - Returns alert timing configuration

#### Data Parsing
- `parse_temp_ror(input_str)` - Parses "temp:ror" format
- `format_time(seconds)` - Formats seconds as MM:SS

---

## Future Enhancement Ideas

### Possible V3 Features
- **Yellow phase tracking**: Add Yellow Start/End times and temps
- **Drying phase**: Track drying phase completion
- **ROR trends**: Calculate ROR at more frequent intervals
- **Crash detection**: Alert if ROR drops below threshold
- **Flick detection**: Alert if ROR spikes above threshold
- **Bean moisture**: Track green bean moisture content
- **Altitude compensation**: Adjust predictions based on elevation
- **Weather data**: Log ambient temp/humidity automatically
- **Export formats**: JSON, Excel, PDF reports
- **Graphing**: Automatic roast curve visualization

### Database Migration
Consider migrating from CSV to SQLite for:
- Better query performance
- Relational data (beans table, roasts table, etc.)
- Atomic transactions
- Full-text search on notes
- Complex statistical queries

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Oct 2025 | Initial CSV format (18 columns) |
| 2.0 | Nov 2025 | Enhanced format with FC/SC granularity, ROR tracking (26 columns) |

---

## Support

For questions or issues:
1. Review README.md for usage instructions
2. Review SKYWALKER_GUIDE.md for roasting technique
3. Check TECHNICAL.md (this file) for data format details
