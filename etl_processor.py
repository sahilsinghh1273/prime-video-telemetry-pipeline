import os
import sqlite3 # Built-in Python SQL database

print("🚀 Starting ETL Processing & Database Load...\n")

file_path = "Local_Data_Lake/raw_streaming_logs.jsonl"

if not os.path.exists(file_path):
    print("Error: Could not find the data lake file.")
    exit()

with open(file_path, "r") as file:
    raw_logs = file.readlines()

# 1. TRANSFORM: Clean the data
buffering_events = {}
total_events = 0

for line in raw_logs:
    if "|" not in line or "User:" not in line:
        continue
        
    total_events += 1
    parts = line.split("|")
    try:
        event_part = parts[1].split("Event:")[1].strip()
        movie_part = parts[2].split("Movie:")[1].strip()
        
        if event_part == "BUFFERING":
            if movie_part in buffering_events:
                buffering_events[movie_part] += 1
            else:
                buffering_events[movie_part] = 1
    except IndexError:
        continue

# 2. LOAD: Connect to local Data Warehouse (SQLite)
# This creates a database file right next to your logs
db_path = 'Local_Data_Lake/prime_video_warehouse.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create a relational table (Data Schema design)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS movie_buffering_metrics (
        movie_title TEXT,
        buffering_events INTEGER,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Clear old data to prevent duplicates when rerunning the script
cursor.execute('DELETE FROM movie_buffering_metrics')

# Insert the transformed data into the SQL table
for movie, count in buffering_events.items():
    cursor.execute('''
        INSERT INTO movie_buffering_metrics (movie_title, buffering_events)
        VALUES (?, ?)
    ''', (movie, count))

conn.commit()

# 3. ANALYZE: Run a SQL query just like you would in Amazon Redshift
print(f"✅ Processed {total_events} raw events and loaded into SQLite.")
print("\n📊 SQL QUERY RESULTS: Top 3 Worst Performing Movies")
print("-" * 45)

# This SQL query filters and ranks the data
cursor.execute('''
    SELECT movie_title, buffering_events 
    FROM movie_buffering_metrics 
    ORDER BY buffering_events DESC 
    LIMIT 3
''')

for row in cursor.fetchall():
    print(f"Movie: {row[0].ljust(20)} | Issues: {row[1]}")

conn.close()
print("-" * 45)
print("Pipeline Complete.")