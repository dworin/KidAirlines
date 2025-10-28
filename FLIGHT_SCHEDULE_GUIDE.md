# KidAirlines Flight Schedule Guide

## Overview

KidAirlines now features **realistic flight times** based on actual distances and aircraft performance. This document explains the flight schedule system and provides examples.

## Flight Time Features

### Realistic Durations
- **Short-haul domestic** (1-3 hours): EWR-BWI, EWR-DTW, EWR-ORD, EWR-MIA, etc.
- **Cross-country** (5-6 hours): EWR-SFO
- **Transatlantic** (7-8 hours): EWR-LHR, EWR-CDG
- **Long-haul international** (11-19 hours): EWR-CAI, EWR-DPS (Bali)

### Wind Adjustments
- **Eastbound transatlantic**: ~7 hours (tailwinds)
- **Westbound transatlantic**: ~7.5-8 hours (headwinds)
- **Eastbound transcontinental**: ~5h 40m (jet stream assist)
- **Westbound transcontinental**: ~6h 10m (headwinds)

### Aircraft Capacity
Different aircraft types for different route lengths:
- **120 seats**: Regional jets (short-haul like EWR-BWI)
- **150 seats**: Narrow-body (domestic routes)
- **180 seats**: Large narrow-body (high-traffic domestic, cross-country)
- **220 seats**: Wide-body (transatlantic)
- **250 seats**: Large wide-body (ultra-long-haul to Bali, Cairo)

## Sample Daily Schedule from EWR

### Early Morning Departures (05:00-09:00)
```
KA130  EWR-BWI  06:30-07:30  (1h)        [Regional Service]
KA100  EWR-DTW  06:00-08:00  (2h)        [Morning Business Service]
KA110  EWR-ORD  07:00-09:30  (2.5h)      [Business Service]
KA140  EWR-MIA  07:30-10:30  (3h)        [Morning Service]
KA240  EWR-SFO  08:00-14:10  (6h 10m)    [Transcontinental]
KA120  EWR-PBI  08:00-11:00  (3h)        [Morning Service]
KA250  EWR-OMA  09:00-12:00  (3h)        [Morning Service]
```

### Midday Departures (10:00-15:00)
```
KA130  EWR-BWI  10:00-11:00  (1h)        [Shuttle Service]
KA100  EWR-DTW  12:00-14:00  (2h)        [Midday Service]
KA140  EWR-MIA  12:00-15:00  (3h)        [Afternoon Service]
KA110  EWR-ORD  13:30-16:00  (2.5h)      [Afternoon Service]
KA130  EWR-BWI  14:00-15:00  (1h)        [Shuttle Service]
KA240  EWR-SFO  14:00-20:10  (6h 10m)    [Afternoon Transcontinental]
KA120  EWR-PBI  14:00-17:00  (3h)        [Afternoon Service]
KA250  EWR-OMA  15:00-18:00  (3h)        [Afternoon Service]
```

### Evening Departures (17:00-22:00)
```
KA140  EWR-MIA  17:00-20:00  (3h)        [Evening Service]
KA130  EWR-BWI  18:00-19:00  (1h)        [Evening Shuttle]
KA100  EWR-DTW  18:00-20:00  (2h)        [Evening Service]
KA220  EWR-CDG  18:00-01:30  (7.5h)      [Overnight to Paris]
KA110  EWR-ORD  19:00-21:30  (2.5h)      [Evening Service]
KA230  EWR-LHR  19:00-02:00  (7h)        [Overnight to London]
KA210  EWR-CAI  19:30-06:30  (11h)       [Overnight to Cairo]
KA200  EWR-DPS  20:00-15:00+1 (19h)      [Ultra Long-Haul to Bali]
KA240  EWR-SFO  20:00-02:10  (6h 10m)    [Red-Eye Transcontinental]
KA120  EWR-PBI  20:00-23:00  (3h)        [Evening Service]
KA220  EWR-CDG  21:30-05:00  (7.5h)      [Late Night to Paris]
KA230  EWR-LHR  22:00-05:00  (7h)        [Late Night to London]
```

## Sample Inbound Schedule to EWR

### Morning Arrivals (06:00-12:00)
```
KA111  ORD-EWR  06:00-08:30  (2.5h)      [Early Morning Return]
KA210  CAI-EWR  23:00-06:30  (11h)       [Overnight from Cairo]
KA116  MIA-EWR  06:30-09:30  (3h)        [Morning Return]
KA121  PBI-EWR  07:00-10:00  (3h)        [Morning Return]
KA101  DTW-EWR  08:00-10:00  (2h)        [Morning Return]
KA231  LHR-EWR  09:00-16:30  (7.5h)      [Morning Departure, Afternoon Arrival]
KA221  CDG-EWR  10:00-18:00  (8h)        [Morning Departure, Evening Arrival]
KA116  MIA-EWR  11:00-14:00  (3h)        [Midday Return]
KA131  BWI-EWR  11:00-12:00  (1h)        [Shuttle Return]
```

### Afternoon Arrivals (13:00-19:00)
```
KA111  ORD-EWR  11:30-14:00  (2.5h)      [Afternoon Return]
KA200  DPS-EWR  22:00-16:00+1 (18h)      [Overnight from Bali]
KA101  DTW-EWR  14:00-16:00  (2h)        [Afternoon Return]
KA131  BWI-EWR  15:00-16:00  (1h)        [Shuttle Return]
KA121  PBI-EWR  13:00-16:00  (3h)        [Afternoon Return]
KA116  MIA-EWR  16:00-19:00  (3h)        [Evening Return]
KA231  LHR-EWR  12:00-19:30  (7.5h)      [Afternoon Trans-Atlantic]
KA111  ORD-EWR  17:00-19:30  (2.5h)      [Evening Return]
```

### Evening Arrivals (19:00-23:00)
```
KA131  BWI-EWR  19:00-20:00  (1h)        [Evening Shuttle]
KA221  CDG-EWR  13:30-21:30  (8h)        [Afternoon Trans-Atlantic]
KA121  PBI-EWR  19:00-22:00  (3h)        [Evening Return]
KA101  DTW-EWR  20:00-22:00  (2h)        [Late Return]
```

## Route Type Categories

### Ultra-Short-Haul (Under 1.5 hours)
- **EWR ↔ BWI** (Baltimore): 1 hour
- Service: 4 flights daily (shuttle-style)
- Aircraft: 120-seat regional jets
- Schedule: Every 3-4 hours from 06:30 to 19:00

### Short-Haul (1.5-3 hours)
- **EWR ↔ DTW** (Detroit): 2 hours
- **EWR ↔ ORD** (Chicago): 2.5 hours
- **EWR ↔ MIA** (Miami): 3 hours
- **EWR ↔ PBI** (West Palm Beach): 3 hours
- **EWR ↔ OMA** (Omaha): 3 hours
- Service: 2-3 flights daily
- Aircraft: 150-180 seats
- Schedule: Morning, afternoon, evening

### Transcontinental (5-7 hours)
- **EWR ↔ SFO** (San Francisco): 6h 10m eastbound, 5h 40m westbound
- Service: 3 flights daily
- Aircraft: 180-seat narrow-body
- Schedule: Morning, afternoon, red-eye

### Transatlantic (7-8 hours)
- **EWR ↔ LHR** (London): 7h eastbound, 7.5h westbound
- **EWR ↔ CDG** (Paris): 7.5h eastbound, 8h westbound
- Service: 2 flights daily
- Aircraft: 220-seat wide-body
- Schedule: Evening departures (arrive next morning), daytime returns

### Ultra-Long-Haul (10+ hours)
- **EWR ↔ CAI** (Cairo): 11h eastbound, 11h westbound
- **EWR ↔ DPS** (Bali): 19h eastbound, 18h westbound
- Service: 1 flight daily
- Aircraft: 250-seat large wide-body
- Schedule: Evening departures (overnight service)

## Special Features

### Overnight Flights
Long international flights depart in the evening and arrive the next morning:
- **EWR-DPS (Bali)**: Depart 20:00, arrive 15:00 next day
- **EWR-CAI (Cairo)**: Depart 19:30, arrive 06:30 next day (technically same day clock time due to time zones)
- **EWR-LHR (London)**: Depart 19:00/22:00, arrive 02:00/05:00 next day
- **EWR-CDG (Paris)**: Depart 18:00/21:30, arrive 01:30/05:00 next day

### Red-Eye Flights
Late-night domestic departures:
- **EWR-SFO**: Depart 20:00, arrive 02:10 (west coast red-eye)

### Business Travel Optimization
- Early morning departures to major business cities (Chicago, Detroit)
- Evening returns allow full business day at destination
- Multiple daily frequencies on key routes (BWI, ORD, MIA)

## Educational Value

This realistic scheduling teaches:
1. **Geography**: Different flight times show relative distances
2. **Time zones**: Why eastbound flights often "gain time"
3. **Wind patterns**: Jet stream effects on transatlantic/transcontinental routes
4. **Aircraft types**: Larger planes for longer routes
5. **Airline economics**: Frequency varies with distance and demand
6. **Time management**: Planning connections through hub

## Technical Implementation

The flight schedule is generated automatically in `src/database/db_init.py`:

```python
route_schedules = {
    route_id: [
        (departure_time, duration_in_minutes, capacity),
        # Multiple entries for multiple daily flights
    ]
}
```

The `calculate_arrival_time()` function handles:
- Converting departure time + duration to arrival time
- Next-day arrivals (when total > 24 hours)
- Proper time formatting (HH:MM)

---

**Note**: All times are simplified for the educational nature of this application. Real-world airline schedules also consider time zone changes, seasonal variations, and specific air traffic control routing.
