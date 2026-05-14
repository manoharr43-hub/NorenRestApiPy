import requests
import sqlite3
from datetime import datetime, timedelta

# -------------------------------
# Database Connection
# -------------------------------
def get_due_customers(db_path="customers.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    cursor.execute("SELECT owner_name, mobile, vehicle_no FROM customers WHERE service_date=?", (tomorrow,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# -------------------------------
# SMS Gateway Integration (Airtel/BSNL/Jio)
# -------------------------------
def send_sms(mobile, message):
    url = "https://sms.airtel.in/api/send"   # Replace with BSNL/Jio URL if needed
    payload = {
        "username": "YOUR_USER",     # Telco credentials
        "password": "YOUR_PASS",
        "senderid": "SERVCE",        # Approved DLT Sender ID
        "message": message,
        "mobile": mobile
    }
    try:
        response = requests.post(url, data=payload)
        print("SMS Response:", response.json())
    except Exception as e:
        print("Error sending SMS:", e)

# -------------------------------
# Reminder Logic
# -------------------------------
def send_reminders():
    customers = get_due_customers()
    for owner, mobile, vehicle in customers:
        message = f"Reminder: Dear {owner}, your vehicle {vehicle} service is due tomorrow!"
        send_sms(mobile, message)

# -------------------------------
# Main Execution
# -------------------------------
if __name__ == "__main__":
    send_reminders()
