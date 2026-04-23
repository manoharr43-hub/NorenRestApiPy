import streamlit as st
import pandas as pd
import pyotp
from NorenRestApiPy import NorenApi
from datetime import datetime

# =============================
# API CLASS
# =============================
class ShoonyaApiPy(NorenApi):
    def __init__(self):
        super().__init__(
            host='https://api.shoonya.com/NorenWClientTP/',
            websocket='wss://api.shoonya.com/NorenWSTP/'
        )

api = ShoonyaApiPy()

# =============================
# LOGIN
# =============================
def login():
    try:
        totp = pyotp.TOTP(st.secrets["shoonya"]["totp"]).now()

        ret = api.login(
            userid=st.secrets["shoonya"]["user_id"],
            password=st.secrets["shoonya"]["password"],
            twoFA=totp,
            vendor_code=st.secrets["shoonya"]["vendor_code"],
            api_secret=st.secrets["shoonya"]["api_secret"],
            imei=st.secrets["shoonya"]["imei"]
        )

        return ret
    except Exception as e:
        st.error(f"Login Error: {e}")
        return None

# =============================
# CONFIG
# =============================
st.set_page_config(page_title="🔥 Shoonya Live Terminal", layout="wide")
st.title("🚀 Shoonya Live Trading Terminal")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =============================
# LOGIN BUTTON
# =============================
if not st.session_state.logged_in:
    if st.button("🔐 Login to Shoonya"):
        res = login()
        if res:
            st.success("Login Successful ✅")
            st.session_state.logged_in = True
        else:
            st.error("Login Failed ❌")
    st.stop()

# =============================
# STOCK LIST (NSE TOKENS)
# =============================
stocks = {
    "RELIANCE": "2885",
    "TCS": "11536",
    "INFY": "1594",
    "HDFCBANK": "1333",
    "ICICIBANK": "4963",
    "SBIN": "3045"
}

live_data = {}

# =============================
# WEBSOCKET CALLBACK
# =============================
def event_handler_quote_update(message):
    token = message.get('tk')
    price = message.get('lp')

    for name, tk in stocks.items():
        if tk == token:
            live_data[name] = float(price)

# =============================
# START WEBSOCKET
# =============================
if st.button("▶ Start Live Feed"):

    api.start_websocket(
        order_update_callback=lambda x: None,
        subscribe_callback=event_handler_quote_update,
        socket_open_callback=lambda: print("Connected")
    )

    tokens = [f"NSE|{tk}" for tk in stocks.values()]
    api.subscribe(tokens)

    st.success("Live Feed Started 🚀")

# =============================
# EMA SIGNAL
# =============================
def get_signal(price_list):
    if len(price_list) < 50:
        return "WAIT"

    df = pd.DataFrame(price_list, columns=["Close"])

    e20 = df['Close'].ewm(span=20).mean()
    e50 = df['Close'].ewm(span=50).mean()

    if e20.iloc[-1] > e50.iloc[-1]:
        return "🚀 BUY"
    else:
        return "💀 SELL"

# =============================
# DISPLAY
# =============================
st.subheader("📊 LIVE SIGNALS")

table = []

for s in stocks:
    if s in live_data:
        price = live_data[s]

        if "history" not in st.session_state:
            st.session_state.history = {}

        if s not in st.session_state.history:
            st.session_state.history[s] = []

        st.session_state.history[s].append(price)

        signal = get_signal(st.session_state.history[s])

        table.append({
            "Stock": s,
            "Price": price,
            "Signal": signal,
            "Time": datetime.now().strftime("%H:%M:%S")
        })

df = pd.DataFrame(table)
st.dataframe(df, use_container_width=True)

# =============================
# PAPER TRADING MODE
# =============================
st.markdown("---")
st.subheader("🧪 Paper Trading")

if st.button("Simulate Trades"):

    trades = []

    for row in table:
        if row["Signal"] == "🚀 BUY":
            trades.append(f"BUY {row['Stock']} at {row['Price']}")
        elif row["Signal"] == "💀 SELL":
            trades.append(f"SELL {row['Stock']} at {row['Price']}")

    for t in trades:
        st.write(t)
