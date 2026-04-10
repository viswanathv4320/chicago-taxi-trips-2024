import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql123",
    database="chicago_taxi"
)

cursor = conn.cursor()

# Query 1: Monthly Revenue Trend with MoM % Change
# Shows total trips, revenue, and how each month grew or shrank vs the prior month
q1 = """
WITH monthly AS (
    SELECT
        trip_start_month,
        COUNT(*) AS total_trips,
        ROUND(SUM(fare), 2) AS total_fare,
        ROUND(SUM(trip_total), 2) AS total_revenue,
        ROUND(AVG(fare), 2) AS avg_fare
    FROM trips
    GROUP BY trip_start_month
)
SELECT
    trip_start_month,
    total_trips,
    total_fare,
    total_revenue,
    avg_fare,
    ROUND(
        (total_revenue - LAG(total_revenue) OVER (ORDER BY trip_start_month))
        / LAG(total_revenue) OVER (ORDER BY trip_start_month) * 100, 2
    ) AS mom_revenue_change_pct
FROM monthly
ORDER BY trip_start_month;
"""

# Query 2: Peak Hour Profitability
# Which hours generate the most revenue and best tips
q2 = """
SELECT
    trip_start_hour,
    COUNT(*) AS total_trips,
    ROUND(AVG(fare), 2) AS avg_fare,
    ROUND(AVG(tip_pct), 2) AS avg_tip_pct,
    ROUND(SUM(trip_total), 2) AS total_revenue,
    RANK() OVER (ORDER BY SUM(trip_total) DESC) AS revenue_rank
FROM trips
GROUP BY trip_start_hour
ORDER BY total_revenue DESC;
"""

# Query 3: Company Performance Scorecard
# Market share, avg fare, tip %, efficiency ranked by total revenue
q3 = """
WITH company_stats AS (
    SELECT
        company,
        COUNT(*) AS total_trips,
        ROUND(SUM(trip_total), 2) AS total_revenue,
        ROUND(AVG(fare), 2) AS avg_fare,
        ROUND(AVG(tip_pct), 2) AS avg_tip_pct,
        ROUND(AVG(trip_miles), 2) AS avg_miles
    FROM trips
    GROUP BY company
)
SELECT
    company,
    total_trips,
    total_revenue,
    avg_fare,
    avg_tip_pct,
    avg_miles,
    ROUND(total_trips * 100.0 / SUM(total_trips) OVER (), 2) AS market_share_pct,
    RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank
FROM company_stats
ORDER BY total_revenue DESC
LIMIT 10;
"""

# Query 4: Tipping Behavior by Payment Type and Time of Day
# Breaks down tip % across payment methods and time slots
q4 = """
SELECT
    payment_type,
    time_of_day,
    COUNT(*) AS total_trips,
    ROUND(AVG(tip_pct), 2) AS avg_tip_pct,
    ROUND(SUM(tips), 2) AS total_tips,
    ROUND(AVG(fare), 2) AS avg_fare,
    ROUND(SUM(CASE WHEN is_tipped = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS tip_rate_pct
FROM trips
WHERE payment_type IN ('Credit Card', 'Mobile')
GROUP BY payment_type, time_of_day
ORDER BY payment_type, avg_tip_pct DESC;
"""

# Query 5: Seasonal Demand and Revenue Shifts
# How trips and revenue shift across seasons, with avg speed as proxy for trip type
q5 = """
SELECT
    season,
    COUNT(*) AS total_trips,
    ROUND(SUM(trip_total), 2) AS total_revenue,
    ROUND(AVG(fare), 2) AS avg_fare,
    ROUND(AVG(trip_miles), 2) AS avg_miles,
    ROUND(AVG(speed_mph), 2) AS avg_speed,
    ROUND(AVG(tip_pct), 2) AS avg_tip_pct,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS trip_share_pct
FROM trips
GROUP BY season
ORDER BY total_revenue DESC;
"""

# Query 6: Trip Type Economics
# Short vs Medium vs Long — fare per mile, tip %, speed, revenue contribution
q6 = """
WITH trip_economics AS (
    SELECT
        trip_type,
        COUNT(*) AS total_trips,
        ROUND(AVG(fare_per_mile), 2) AS avg_fare_per_mile,
        ROUND(AVG(tip_pct), 2) AS avg_tip_pct,
        ROUND(AVG(speed_mph), 2) AS avg_speed,
        ROUND(AVG(trip_minutes), 2) AS avg_minutes,
        ROUND(SUM(trip_total), 2) AS total_revenue
    FROM trips
    WHERE fare_per_mile IS NOT NULL
    GROUP BY trip_type
)
SELECT
    trip_type,
    total_trips,
    avg_fare_per_mile,
    avg_tip_pct,
    avg_speed,
    avg_minutes,
    total_revenue,
    ROUND(total_revenue * 100.0 / SUM(total_revenue) OVER (), 2) AS revenue_share_pct
FROM trip_economics
ORDER BY avg_fare_per_mile DESC;
"""

# Query 7: Zone Performance by Archetype
# Revenue, avg fare, and time-of-day breakdown for top pickup zones
q7 = """
SELECT
    pickup_community_area,
    CASE
        WHEN pickup_community_area IN (76, 56) THEN 'Airport'
        WHEN pickup_community_area IN (32, 28) THEN 'Business'
        WHEN pickup_community_area IN (8, 6, 7) THEN 'Nightlife'
        WHEN pickup_community_area IN (33, 77) THEN 'Tourism'
        ELSE 'Other'
    END AS zone_archetype,
    COUNT(*) AS total_trips,
    ROUND(SUM(trip_total), 2) AS total_revenue,
    ROUND(AVG(fare), 2) AS avg_fare,
    ROUND(AVG(trip_miles), 2) AS avg_miles,
    ROUND(AVG(tip_pct), 2) AS avg_tip_pct,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS trip_share_pct
FROM trips
WHERE pickup_community_area IN (76, 56, 32, 28, 8, 6, 7, 33, 77)
GROUP BY pickup_community_area, zone_archetype
ORDER BY total_revenue DESC;
"""

# Query 8: Payment Type Market Share Trend MoM
# Is Mobile growing? Is Cash declining? Track share shift through 2024
q8 = """
WITH monthly_payments AS (
    SELECT
        trip_start_month,
        payment_type,
        COUNT(*) AS trips
    FROM trips
    WHERE payment_type IN ('Credit Card', 'Mobile', 'Cash')
    GROUP BY trip_start_month, payment_type
),
monthly_totals AS (
    SELECT
        trip_start_month,
        SUM(trips) AS total_trips
    FROM monthly_payments
    GROUP BY trip_start_month
)
SELECT
    mp.trip_start_month,
    mp.payment_type,
    mp.trips,
    ROUND(mp.trips * 100.0 / mt.total_trips, 2) AS market_share_pct,
    ROUND(
        (mp.trips - LAG(mp.trips) OVER (PARTITION BY mp.payment_type ORDER BY mp.trip_start_month))
        * 100.0 / LAG(mp.trips) OVER (PARTITION BY mp.payment_type ORDER BY mp.trip_start_month),
    2) AS mom_change_pct
FROM monthly_payments mp
JOIN monthly_totals mt ON mp.trip_start_month = mt.trip_start_month
ORDER BY mp.trip_start_month, mp.payment_type;
"""

# Query 9: Best Driver Shift — Day + Hour Earnings Optimization
# Which day/hour combination maximizes avg earnings per trip?
q9 = """
SELECT
    day_of_week,
    trip_start_hour,
    COUNT(*) AS total_trips,
    ROUND(AVG(fare), 2) AS avg_fare,
    ROUND(AVG(tips), 2) AS avg_tip,
    ROUND(AVG(trip_total), 2) AS avg_earnings,
    ROUND(AVG(trip_miles), 2) AS avg_miles,
    RANK() OVER (ORDER BY AVG(trip_total) DESC) AS earnings_rank
FROM trips
GROUP BY day_of_week, trip_start_hour
HAVING COUNT(*) >= 1000
ORDER BY avg_earnings DESC
LIMIT 20;
"""

# Run all queries and display results
queries = {
    "Q1 Monthly Revenue Trend": q1,
    "Q2 Peak Hour Profitability": q2,
    "Q3 Company Performance Scorecard": q3,
    "Q4 Tipping Behavior": q4,
    "Q5 Seasonal Demand": q5,
    "Q6 Trip Type Economics": q6,
    "Q7 Zone Performance by Archetype": q7,
    "Q8 Payment Type Market Share Trend": q8,
    "Q9 Best Driver Shift": q9,
}

for name, query in queries.items():
    print(f" {name}")
    df_result = pd.read_sql(query, conn)
    print(df_result.to_string(index=False))

conn.close()