import sqlite3
import matplotlib.pyplot as plt
import os

print("📊 Generating Business Dashboard...")

db_path = 'Local_Data_Lake/prime_video_warehouse.db'

if not os.path.exists(db_path):
    print("Error: Could not find the database. Run etl_processor.py first.")
    exit()

# Connect to your Data Warehouse
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query the data for the visualization
cursor.execute('''
    SELECT movie_title, buffering_events 
    FROM movie_buffering_metrics 
    ORDER BY buffering_events DESC
''')
data = cursor.fetchall()
conn.close()

if not data:
    print("No data found in the database.")
    exit()

# Separate the data into X and Y axes for the chart
movies = [row[0] for row in data]
issues = [row[1] for row in data]

# Build the Visual Dashboard
plt.figure(figsize=(10, 6))
plt.bar(movies, issues, color='#FF9900')  # Amazon Orange
plt.title('Prime Video Quality of Service: Buffering Issues by Movie', fontsize=14, fontweight='bold')
plt.xlabel('Movie Title', fontsize=12)
plt.ylabel('Total Buffering Events', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Save dashboard image to Local_Data_Lake
chart_path = 'Local_Data_Lake/buffering_report.png'
plt.tight_layout()
plt.savefig(chart_path, dpi=300)
print(f"📈 Dashboard image saved to {chart_path}")

# Display the dashboard
plt.show()

