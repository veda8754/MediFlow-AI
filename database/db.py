import sqlite3
import csv
from pathlib import Path

# Database location
BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "mediflow.db"


# Create database connection
def get_connection():

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


# Create enquiries table
def create_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enquiries (

            enquiry_id INTEGER PRIMARY KEY,

            patient_name TEXT,

            enquiry_text TEXT NOT NULL,

            enquiry_date TEXT,

            category TEXT,

            sentiment TEXT,

            priority TEXT,

            ai_response TEXT,

            status TEXT DEFAULT 'Open',

            requires_followup INTEGER DEFAULT 0

        )
    """)

    conn.commit()

    conn.close()


if __name__ == "__main__":

    create_table()

    print("MediFlow AI database created successfully!")

# Automatically initialise database with sample enquiries
def initialize_database():

    create_table()

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM enquiries")

    count = cursor.fetchone()[0]

    # Import sample data only if the database is empty
    if count == 0:

        csv_path = BASE_DIR / "data" / "enquiries.csv"

        with open(csv_path, "r", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            for row in reader:

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
# Fetch all enquiries
def get_all_enquiries():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM enquiries")

    records = cursor.fetchall()

    conn.close()

    return [dict(row) for row in records]


# Fetch a single enquiry
def get_enquiry(enquiry_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM enquiries WHERE enquiry_id = ?",
        (enquiry_id,)
    )

    record = cursor.fetchone()

    conn.close()

    return dict(record) if record else None


# Update AI classification and response
def update_enquiry(enquiry_id, classification, response):

    conn = get_connection()

    conn.execute("""
        UPDATE enquiries
        SET category = ?,
            sentiment = ?,
            priority = ?,
            ai_response = ?,
            requires_followup = ?
        WHERE enquiry_id = ?
    """, (
        classification["category"],
        classification["sentiment"],
        classification["priority"],
        response,
        int(classification["requires_followup"]),
        enquiry_id
    ))

    conn.commit()

    conn.close()


# Update enquiry status
def update_status(enquiry_id, status):

    conn = get_connection()

    conn.execute("""
        UPDATE enquiries
        SET status = ?
        WHERE enquiry_id = ?
    """, (status, enquiry_id))

    conn.commit()

    conn.close()