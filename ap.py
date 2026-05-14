import streamlit as st
import pandas as pd
import sqlite3
import requests
from datetime import datetime, timedelta
import os

# -------------------------------
# Helper: Import Excel → SQLite
# -------------------------------
def import_excel_to_sqlite(excel_file, db_file="customers.db"):
    df = pd.read_excel(excel_file)
    conn = sqlite3.connect(db_file)
    df.to_sql("customers", conn, if_exists="replace", index=False)
    conn.close()
    return df

# -------------------------------
# Helper: Fetch Customers Due Tomorrow
# -------------------------------
def get_due_customers(db_file="customers.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%m/%d/%Y")
    cursor.execute("SELECT First_Name, Last_Name, Mobile_Number, Model_Name, License_Number, Next_Service_Date FROM customers WHERE Next_Service_Date=?", (tomorrow,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# -------------------------------
# Helper: Send SMS
# -------------------------------
def send_sms(mobile, message):
    url = "https://sms.airtel.in/api/send"   # Replace with BSNL/Jio URL
    payload = {
        "username": "YOUR_USER",
        "password": "YOUR_PASS",
        "senderid": "SERVCE",
        "message": message,
        "mobile": mobile
    }
    try:
        response = requests.post(url, data=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="🚗 Vehicle Service Reminder", layout="wide")
st.title("🔧 Vehicle Service Reminder App")

# Upload Excel
uploaded_file = st.file_uploader("Upload Festive Camp Data Excel", type=["xlsx"])

if uploaded_file:
    df = import_excel_to_sqlite(uploaded_file)
    st.success("✅ Excel data imported successfully!")
    st.dataframe(df.head())

    # Reminder Button
    if st.button("📩 Send Reminders for Tomorrow"):
        customers = get_due_customers()
        if customers:
            for first, last, mobile, model, license_no, service_date in customers:
                msg = f"Reminder: Dear {first} {last}, your vehicle {model} ({license_no}) service is due on {service_date}."
                result = send_sms(mobile, msg)
                st.write(f"Sent to {mobile}: {result}")
            st.success("✅ All reminders sent successfully!")
        else:
            st.warning("No customers found for tomorrow’s service date.")
else:
    st.info("Please upload your Excel file to begin.")
