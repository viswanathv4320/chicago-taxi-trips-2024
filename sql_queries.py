import pandas as pd
import mysql.connector
from mysql.connector import Error

conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'mysql123',
    database = 'chicago_taxi'
)

cursor = conn.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS trips (
        trip_id VARCHAR(50),
        taxi_id VARCHAR(150),
        trip_start_timestamp DATETIME,
        trip_end_timestamp DATETIME,
        trip_seconds FLOAT,
        trip_miles FLOAT,
        pickup_census_tract VARCHAR(20),
        dropoff_census_tract VARCHAR(20),
        pickup_community_area INT,
        dropoff_community_area INT,
        fare FLOAT,
        tips FLOAT,
        tolls FLOAT,
        extras FLOAT,
        trip_total FLOAT,
        payment_type VARCHAR(20),
        company VARCHAR(60),
        pickup_centroid_latitude FLOAT,
        pickup_centroid_longitude FLOAT,
        dropoff_centroid_latitude FLOAT,
        dropoff_centroid_longitude FLOAT,
        trip_minutes FLOAT,
        trip_start_hour INT,
        trip_start_date DATE,
        trip_start_month VARCHAR(10),
        day_of_week VARCHAR(10),
        is_tipped INT,
        speed_mph FLOAT,
        season VARCHAR(10),
        time_of_day VARCHAR(12),
        is_weekend INT,
        fare_per_mile FLOAT,
        tip_pct FLOAT,
        trip_type VARCHAR(10)
    )
""")
print("Table created.")

cursor.execute("TRUNCATE TABLE trips")
print("Table cleared.")

# Load CSV
df = pd.read_csv('chicago_taxi_2024_cleaned.csv')

# Replace NaN with None so MySQL accepts nulls
df = df.astype(object).where(pd.notnull(df), None)

insert_query = """
    INSERT INTO trips VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s
    )
"""

chunk_size = 1000
total = len(df)
inserted = 0

for i in range(0, total, chunk_size):
    chunk = df.iloc[i:i+chunk_size]
    data = [tuple(x) for x in chunk.values]
    cursor.executemany(insert_query, data)
    conn.commit()
    inserted += len(data)
    if inserted % 100000 == 0:
        print(f"Inserted {inserted}/{total} records.")

print(f"Finished inserting {inserted} records.")
