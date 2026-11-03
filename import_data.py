import pandas as pd

from database.db import get_connection, create_table

# Create database table
create_table()

# Read CSV dataset
df = pd.read_csv("data/enquiries.csv")

# Connect to database
conn = get_connection()

# Import records
for _, row in df.iterrows():

    conn.execute("""
        INSERT OR IGNORE INTO enquiries
        (
            enquiry_id,
            patient_name,
            enquiry_text,
            enquiry_date,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        int(row["enquiry_id"]),
        row["patient_name"],
        row["enquiry_text"],
        row["enquiry_date"],
        row["status"]
    ))

conn.commit()

conn.close()

print("Successfully imported healthcare enquiries!")