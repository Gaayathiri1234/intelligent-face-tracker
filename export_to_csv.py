import sqlite3
import csv
import os

DB_PATH = "logs/faces.db"

def export_table_to_csv(table_name, csv_filename):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    column_names = [description[0] for description in cursor.description]

    os.makedirs("exports", exist_ok=True)
    with open(os.path.join("exports", csv_filename), mode="w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(column_names)
        writer.writerows(rows)

    conn.close()
    print(f"✅ Exported {table_name} → exports/{csv_filename}")

# Export both tables
export_table_to_csv("face_logs", "face_logs.csv")
export_table_to_csv("visitor_stats", "visitor_stats.csv")
