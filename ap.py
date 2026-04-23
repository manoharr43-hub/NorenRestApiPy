import streamlit as st
import pandas as pd
import pyotp
import requests
from datetime import datetime

# =============================
# SIMPLE API (NO INSTALL ISSUE)
# =============================
class ShoonyaApi:

    def __init__(self):
        self.host = "https://api.shoonya.com/NorenWClientTP/"

    def login(self, user, pwd, totp, vc, apikey, imei):
        url = self.host + "QuickAuth"

        data = {
            "uid": user,
            "pwd": pwd,
            "factor2": totp,
            "vc": vc,
            "appkey": apikey,
            "imei": imei
        }

        res = requests.post(url, data=data)
        return res.json()

# =============================
# CONFIG
# =============================
st.set_page_config(page_title="🔥 Shoonya Scanner", layout="wide")

st.title("🚀 Shoonya Live Scanner (Safe Version)")

# =============================
# SESSION
# =============================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =============================
# LOGIN FUNCTION
# =============================
def do_login():
    try:
        totp = pyotp.TOTP(st.secrets["shoonya"]["totp"]).now()

        api = ShoonyaApi()

        res = api.login(
            st.secrets["shoonya"]["user_id"],
            st.secrets["shoonya"]["password"],
            totp,
            st.secrets["shoonya"]["vendor_code"],
            st.secrets["shoonya"]["api_secret"],
            st.secrets["shoonya"]["imei"]
        )

        return res
    except Exception as e:
        st.error(f"Login Error: {e}")
        return None

# =============================
# LOGIN UI
# =============================
if not st.session_state.logged_in:

    st.warning("🔐 Please Login to Shoonya")

    if st.button("Login Now"):
        res = do_login()

        if res and res.get("stat") == "Ok":
            st.success("Login Successful ✅")
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Login Failed ❌")

    st.stop()

# =============================
# AFTER LOGIN
# =============================
st.success("✅ Connected to Shoonya")

# =============================
# DUMMY LIVE DATA (SAFE)
# =============================
stocks = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "SBIN"]

data = []

import random

for s in stocks:
    price = round(random.uniform(100, 3000), 2)

    signal = "WAIT"
    if price % 2 == 0:
        signal = "🚀 BUY"
    else:
        signal = "💀 SELL"

    data.append({
        "Stock": s,
        "Price": price,
        "Signal": signal,
        "Time": datetime.now().strftime("%H:%M:%S")
    })

df = pd.DataFrame(data)

# =============================
# DISPLAY
# =============================
st.subheader("📊 Live Signals (Demo)")

st.dataframe(df, use_container_width=True)

# =============================
# PAPER TRADE
# =============================
st.markdown("---")
st.subheader("🧪 Paper Trading")

if st.button("Simulate Trades"):

    for row in data:
        if row["Signal"] == "🚀 BUY":
            st.write(f"BUY {row['Stock']} @ {row['Price']}")
        else:
            st.write(f"SELL {row['Stock']} @ {row['Price']}")
