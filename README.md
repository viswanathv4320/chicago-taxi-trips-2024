---

## Data Cleaning

The raw dataset required several cleaning steps before analysis. Dollar signs were stripped and all financial columns cast to float. Timestamps were parsed as datetime. Commas were removed from Trip Seconds and Trip Miles. Around 17,000 rows where all financial columns were null were dropped, along with rows with zero or negative fares and trip totals. Outliers were capped at 99th percentile thresholds — trips over 60 miles, over 180 minutes, fares over $200, and speeds over 80 mph. Only 12,687 rows were removed as outliers, just 0.2% of the data.

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

7. Do Chicago's top pickup zones follow distinct demand archetypes, and can we classify them by behavior rather than just volume?
8. Is mobile payment adoption growing through 2024, and is it displacing cash or credit card usage?
9. What is the single best day and hour combination for a driver to maximize per-trip earnings?

---

## Key Findings

### Scale
The dataset covers 6.3 million trips and $180 million in total revenue across 2024, with an average fare of $23.06 and average trip length of 6.93 miles.

### Time Patterns
Night trips are the most lucrative, with the highest average fare ($25.74), longest distance (7.98 miles), and fastest speed (23.19 mph), consistent with airport and highway runs. Evening has the best tip rate at 14.99%, and weekday evenings are the most valuable slot overall, combining high volume with a 15.25% tip rate. Thursday is the busiest day of the week, and weekends drop off sharply, suggesting a strong business travel pattern.

### Seasonal Trends
Fall is the highest revenue season at $48.4 million total, which is surprising given it beats summer. Winter is the slowest, with shorter trips, lower fares ($21.82 average), and the weakest tip rate at 12.92%. May is the single busiest month with 605,000 trips, while January is the quietest at 415,000.

### Payment and Tipping
Credit card tip rate is 93.2% compared to Mobile at 84.5%, a significant behavioral gap. Cash tips are $0 across the board, as expected since cash tips are not recorded in the dataset. Weekday night business travelers tip more ($26.54 average fare) than weekend night riders ($23.92).

### Companies
Flash Cab leads in volume with 1.36 million trips but has the worst tip rate at just 7.88%, likely due to a cash-heavy clientele. 5 Star Taxi commands the highest average fare ($26.12) and covers the most miles per trip (8.40 miles), showing clear premium positioning. Taxicab Insurance Agency LLC and Sun Taxi have strong tip rates around 16.8 to 16.9% despite lower volumes.

### Trip Economics
Short trips are the most expensive per mile at $9.01 compared to $2.69 for long trips, due to the base fare effect. Short trips also tip the best at 14.98%, likely city center rides with tipped credit card payments. Long trips are clearly airport runs, averaging 27.93 mph, well above the city average.

### Geography — Zone Archetypes

Chicago taxi demand splits into four distinct behavioral archetypes. Airport zones (O'Hare and Midway) have the highest fares, are active 24/7, and handle long distance trips. O'Hare alone accounts for 1.37 million pickups. Business and commuter zones like the Loop peak on weekday mornings and afternoons and are almost dead on weekends — the Loop is 83% weekday trips, the strongest business signal of any zone. Nightlife and residential zones like Near North Side and Wrigleyville show strong evening demand with a more balanced weekday/weekend ratio. Tourism and events zones like the Near South Side and Museum Campus are afternoon and weekend driven with lower night activity.

### Outside the Box
Mobile payments grew from 15.47% share in January to 19.32% in December, a clear and consistent upward trend while cash steadily declined. Monday midnight is the single best driver shift at $40.25 average earnings per trip, driven by long late-night airport runs. Short trips earn $23.49 per minute versus $1.23 for long trips, the classic driver dilemma between quick city fares and high-value airport runs. O'Hare evening trips tip the best at 17.91%, making returning travelers the most generous tippers in the entire dataset. Trips with both extras and tolls average $77.60 total with a 19.45% tip rate, nearly four times a standard city ride. Strong taxi-zone loyalty also exists, with some taxis making 3,978 trips from a single community area.

---

## SQL Queries

Nine analytical queries written in MySQL, covering window functions, CTEs, and aggregations.

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

The first dashboard covers the market overview with a revenue zone map by Chicago community area, a zone archetype map, a month-over-month revenue trend line, an hourly demand heatmap, and average fare by time of day.

The second dashboard focuses on driver and company intelligence with a company scorecard comparing trip volume vs tip rate, a payment mix trend showing monthly share of Credit Card, Mobile, and Cash from January to December, a tip rate matrix by payment type and time of day, and a trip type economics comparison by fare per mile.

---

## Flask Web App

**[Live App → chicago-taxi-trips-2024.onrender.com](https://chicago-taxi-trips-2024.onrender.com)**

A data storytelling web app that presents the key findings as an interactive scrollable article. Built with Flask and Plotly and deployed on Render. The app features a header with live KPIs, a monthly revenue line chart, a trip volume heatmap by day and hour, a company performance bar chart, a payment type breakdown, and an embedded Tableau zone map.

---

## How to Run

To run the Flask web app, clone the repo, set up a virtual environment, install dependencies with `pip install -r requirements.txt`, and run `python app.py`. The app will be available at `http://127.0.0.1:5000`.

To run the full analysis, install the additional dependencies with `pip install pandas numpy matplotlib mysql-connector-python`, download the dataset from the Chicago Data Portal and place it in `data/`, run the cleaning notebook at `notebooks/eda.ipynb`, set up MySQL and create the `chicago_taxi` database, load the data with `python sql_queries.py`, and run the analysis with `python sql_analysis.py`.