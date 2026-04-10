# Chicago Taxi Trips 2024 — Data Analysis Project

A full end-to-end data analysis project using 6.3 million Chicago taxi trips from 2024. Covers data cleaning, exploratory data analysis, SQL querying, and an interactive Tableau dashboard.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Dataset](#dataset)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Data Cleaning](#data-cleaning)
- [Key Business Questions](#key-business-questions)
- [Key Findings](#key-findings)
- [SQL Queries](#sql-queries)
- [Tableau Dashboard](#tableau-dashboard)
- [How to Run](#how-to-run)

---

## Project Overview

This project analyzes the City of Chicago's publicly available taxi trip dataset for the full year 2024. The goal is to uncover patterns in rider behavior, revenue trends, company performance, and tipping habits — and present them through SQL queries and an interactive Tableau dashboard.

---

## Dataset

- **Source:** [Chicago Data Portal — Taxi Trips](https://data.cityofchicago.org/Transportation/Taxi-Trips-2024/ajtu-isnz)
- **Size:** 6,334,213 trips after cleaning
- **Period:** January 1, 2024 — December 31, 2024
- **Columns:** 23 raw → 34 after feature engineering

---

## Tech Stack

- **Python** — data cleaning and EDA (pandas, numpy, matplotlib)
- **MySQL** — schema design and analytical queries
- **Tableau Public** — interactive dashboard
- **GitHub** — version control

---

## Project Structure

```
chicago_taxi_trips/
├── data/
│   └── chicago_taxi_2024_cleaned.csv
├── notebooks/
│   └── eda.ipynb
├── sql_queries.py
├── sql_analysis.py
└── README.md
```

---

## Data Cleaning

The raw dataset required several cleaning steps before analysis:

- Stripped `$` symbols and cast all financial columns (`Fare`, `Tips`, `Tolls`, `Extras`, `Trip Total`) to float
- Parsed `Trip Start Timestamp` and `Trip End Timestamp` as datetime
- Removed commas from `Trip Seconds` and `Trip Miles` and cast to numeric
- Dropped ~17,000 rows where all financial columns were null
- Removed rows with zero or negative fares, trip seconds, and trip totals
- Capped outliers based on 99th percentile thresholds:
  - Trip Miles > 60, Trip Minutes > 180, Fare > $200, Trip Total > $250, Speed MPH > 80, Tips > $100
- Only 12,687 rows removed as outliers (0.2% of data)

**Engineered Features:**

| Feature | Description |
|---|---|
| `Trip Minutes` | Trip duration in minutes |
| `Trip Start Hour` | Hour of day (0–23) |
| `Trip Start Date` | Date of trip |
| `Trip Start Month` | Year-month string (e.g. 2024-05) |
| `Day of Week` | Day name |
| `Season` | Winter / Spring / Summer / Fall |
| `Time of Day` | Morning / Afternoon / Evening / Night |
| `Is Weekend` | 1 if Saturday or Sunday |
| `Is Tipped` | 1 if tip > $0 |
| `Speed MPH` | Derived average speed |
| `Fare Per Mile` | Cost efficiency metric |
| `Tip Pct` | Tip as % of fare |
| `Trip Type` | Short (<2mi) / Medium (2–8mi) / Long (>8mi) |

---

## Key Business Questions

1. How did Chicago taxi revenue grow or decline month over month throughout 2024, and which months saw the biggest swings?
2. Which hours of the day generate the most revenue, and do high-volume hours actually translate to higher earnings or just more trips?
3. Which taxi companies dominate the market, and is the highest-volume company also the most profitable — or do smaller companies earn more per trip?
4. Do credit card riders tip more than mobile payment riders, and does the time of day influence how generously people tip?
5. How does rider demand and spending change across the four seasons, and which season is most valuable to the industry?
6. Are short city trips or long airport runs more economically efficient — which generates more revenue per mile and attracts better tips?

**Outside the Box**

7. Do Chicago's top pickup zones follow distinct demand archetypes — and can we classify them by behavior rather than just volume?
8. Is mobile payment adoption growing through 2024, and is it displacing cash or credit card usage?
9. What is the single best day and hour combination for a driver to maximize per-trip earnings?

---

## Key Findings

### Scale
- **6.3M trips** and **$180M in total revenue** across 2024
- Average fare of **$23.06** and average trip length of **6.93 miles**

### Time Patterns
- **Night trips are the most lucrative** — highest avg fare ($25.74), longest distance (7.98 mi), fastest speed (23.19 mph), consistent with airport and highway runs
- **Evening has the best tip rate** at 14.99% — riders are most generous after dinner and evening outings
- **Weekday evenings are the most valuable slot overall** — combining high volume with a 15.25% tip rate
- **Thursday is the busiest day** of the week; weekends drop off sharply, suggesting a strong business travel pattern
- **Afternoon dominates volume** with 2.1M trips, but Night trips punch above their weight on revenue per trip

### Seasonal Trends
- **Fall is the highest revenue season** at $48.4M total — surprising, beats Summer
- **Winter is the slowest** season — shorter trips (6.58 mi avg), lower fares ($21.82), and the weakest tip rate (12.92%)
- **May is the single busiest month** (605k trips); January is the quietest (415k)

### Payment and Tipping
- **Credit card tip rate is 93.2%** vs Mobile at 84.5% — a significant behavioral gap
- **Cash tips are $0.00** across the board — expected, as cash tips are not recorded in the dataset
- Weekday night business travelers tip more ($26.54 avg fare) than weekend night riders ($23.92)

### Companies
- **Flash Cab leads in volume** (1.36M trips) but has the worst tip rate at just 7.88% — likely cash-heavy clientele
- **5 Star Taxi commands the highest avg fare** ($26.12) and covers the most miles per trip (8.40) — clear premium positioning
- **Taxicab Insurance Agency LLC and Sun Taxi** have strong tip rates (~16.8–16.9%) despite lower volumes

### Trip Economics
- **Short trips are the most expensive per mile** at $9.01/mi vs $2.69/mi for long trips — the base fare effect
- **Short trips also tip the best** at 14.98% — likely city center rides with tipped credit card payments
- **Long trips are clearly airport runs** — averaging 27.93 mph, well above the city average

### Geography — Zone Archetypes

Chicago taxi demand splits into 4 distinct behavioral archetypes:

- **Airport zones** (76 O'Hare, 56 Midway) — highest fares ($39.93 and $34.72), active 24/7, long distance trips. O'Hare alone accounts for 1.37M pickups. Midway skews more leisure/balanced than O'Hare's business-heavy profile
- **Business/commuter zones** (32 Loop, 28 Near West Side) — peak demand on weekday mornings and afternoons, almost dead on weekends. The Loop is 83% weekday trips — the strongest business signal of any zone
- **Nightlife/residential zones** (8 Near North Side, 6 Lake View/Wrigleyville, 7 Lincoln Park) — strong evening demand, more balanced weekday/weekend ratio. Near North Side is the second busiest zone overall with 1.34M trips
- **Tourism/events zones** (33 Near South Side/Museum Campus, 77 Edgewater) — afternoon and weekend driven, lower night activity

### Outside the Box

- **Mobile payments grew from 15.47% share in January to 19.32% in December** — a clear and consistent upward trend through 2024, while Cash steadily declined
- **Monday midnight is the single best driver shift** — $40.25 avg earnings per trip, driven by long late-night airport and highway runs
- **Short trips earn $23.49 per minute vs $1.23 for long trips** — the classic driver dilemma between quick city fares and high-value airport runs
- **O'Hare evening trips tip the best** at 17.91% — returning travelers are the most generous tippers in the entire dataset
- **Trips with both extras and tolls average $77.60 total** with a 19.45% tip rate — nearly 4x a standard city ride
- **Strong taxi-zone loyalty exists** — some taxis made 3,978 trips from a single community area, suggesting experienced drivers deliberately stake out high-value zones

---

## SQL Queries

Nine analytical queries written in MySQL covering window functions, CTEs, and aggregations:

| # | Query | Technique |
|---|---|---|
| 1 | Monthly Revenue Trend with MoM % Change | CTE + LAG window function |
| 2 | Peak Hour Profitability | RANK window function |
| 3 | Company Performance Scorecard | CTE + SUM OVER market share |
| 4 | Tipping Behavior by Payment Type and Time of Day | CASE WHEN + GROUP BY |
| 5 | Seasonal Demand and Revenue Shifts | COUNT OVER aggregation |
| 6 | Trip Type Economics | CTE + revenue share % |
| 7 | Zone Performance by Archetype | CASE WHEN classification + window functions |
| 8 | Payment Type Market Share Trend MoM | LAG with PARTITION BY across multiple groups |
| 9 | Best Driver Shift — Day + Hour Optimization | RANK + HAVING filter |

---

## Tableau Dashboard

**[View on Tableau Public →](https://public.tableau.com/app/profile/viswanath.vadlamani/viz/ChicagoTaxiTrips2024TableauDashboard/MarketOverview)**

### Dashboard 1 — Market Overview
- Revenue zone map by Chicago community area (colored by total revenue)
- Zone archetype map (Airport / Business / Nightlife / Tourism classification)
- Month-over-month revenue trend line with average reference line
- Hourly demand heatmap (Day × Hour) showing peak demand patterns
- Average fare by time of day (Morning / Afternoon / Evening / Night)

### Dashboard 2 — Driver & Company Intelligence
- Company scorecard — dual axis chart comparing trip volume vs tip rate
- Payment mix trend — monthly share of Credit Card / Mobile / Cash (Jan–Dec)
- Tip rate matrix — payment type × time of day heatmap
- Trip type economics — fare per mile comparison (Short / Medium / Long trips)

---

## How to Run

1. Clone the repo and set up a virtual environment
2. Install dependencies: `pip install pandas numpy matplotlib mysql-connector-python`
3. Download the dataset from the Chicago Data Portal and place it in `data/`
4. Run the cleaning notebook: `notebooks/eda.ipynb`
5. Set up MySQL and create the `chicago_taxi` database
6. Load data into MySQL: `python sql_queries.py`
7. Run the analysis queries: `python sql_analysis.py`
