import pandas as pd
import sqlite3
import requests
import os
from datetime import datetime, timedelta

# -------------------------------
# Step 1: Import Excel → SQLite
# -------------------------------
def import_excel_to_sqlite(excel_file="Festive Camp Data.xlsx", db_file="customers.db"):
    if not os.path.exists(excel_file):
        raise FileNotFoundError(f"❌ Excel file not found: {excel_file}")
    
    df = pd.read_excel(excel_file)
    conn = sqlite3.connect(db_file)
    df.to_sql("customers", conn, if_exists="replace", index=False)
    conn.close()
    print("✅ Excel data imported into SQLite successfully.")

# -------------------------------
# Step 2: Fetch Customers Due Tomorrow
# -------------------------------
def get_due_customers(db_file="customers.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%m/%d/%Y")  # Match Excel format
    cursor.execute("SELECT First_Name, Last_Name, Mobile_Number, Model_Name, License_Number, Next_Service_Date FROM customers WHERE Next_Service_Date=?", (tomorrow,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# -------------------------------
# Step 3: SMS Gateway Integration
# -------------------------------
def send_sms(mobile, message):
    url = "https://sms.airtel.in/api/send"   # Replace with BSNL/Jio URL if needed
    payload = {
        "username": "YOUR_USER",
        "password": "YOUR_PASS",
        "senderid": "SERVCE",
        "message": message,
        "mobile": mobile
    }
    try:
        response = requests.post(url, data=payload)
        print("📩 SMS Response:", response.json())
    except Exception as e:
        print("❌ Error sending SMS:", e)

# -------------------------------
# Step 4: Reminder Logic
# -------------------------------
def send_reminders():
    customers = get_due_customers()
    for first, last, mobile, model, license_no, service_date in customers:
        message = f"Reminder: Dear {first} {last}, your vehicle {model} ({license_no}) service is due on {service_date}."
        send_sms(mobile, message)

# -------------------------------
# Step 5: Main Execution
# -------------------------------
if __name__ == "__main__":
    try:
        import_excel_to_sqlite()   # Run once to import Excel data
        send_reminders()           # Send reminders for tomorrow
    except FileNotFoundError as e:
        print(e)
        print("👉 Please upload 'Festive Camp Data.xlsx' into the app folder before running.")
