import streamlit as st
import pandas as pd
import sqlite3
import requests
from datetime import datetime, timedelta

# -------------------------------
# Step 1: Import Excel → SQLite
# -------------------------------
def import_excel_to_sqlite(uploaded_file, db_file="customers.db"):
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    conn = sqlite3.connect(db_file)
    df.to_sql("customers", conn, if_exists="replace", index=False)
    conn.close()
    return df

# -------------------------------
# Step 2: Fetch All Customers (No Date Filter)
# -------------------------------
def get_all_customers(db_file="customers.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT "Zonal Office", "Area Office", "Dealer Name", "Asset Number",
               "Model Name", "License Number", "Mobile Number",
               "First Name", "Last Name", "Last Service Date",
               "Last Service Type", "Sale Date", "FSC 4 Date",
               "FSC 5 Date", "Next Service Date", "Turn Up Flag"
        FROM customers
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

# -------------------------------
# Step 3: Fetch Customers Due Tomorrow
# -------------------------------
def get_due_customers(db_file="customers.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%m/%d/%Y")
    cursor.execute("""
        SELECT "First Name", "Last Name", "Mobile Number", "Model Name", "License Number", "Next Service Date"
        FROM customers WHERE "Next Service Date"=?""", (tomorrow,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# -------------------------------
# Step 4: SMS Gateway Integration
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
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# -------------------------------
# Step 5: Streamlit UI
# -------------------------------
st.set_page_config(page_title="🚗 Vehicle Service Reminder", layout="wide")
st.title("🔧 Vehicle Service Reminder App")

uploaded_file = st.file_uploader("Upload Festive Camp Data Excel", type=["xlsx"])

if uploaded_file:
    df = import_excel_to_sqlite(uploaded_file)
    st.success("✅ Excel data imported successfully!")
    st.dataframe(df.head())

    if st.button("📋 Show All Customers"):
        customers = get_all_customers()
        st.write("Total Customers:", len(customers))
        st.dataframe(df)  # Show full table

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
