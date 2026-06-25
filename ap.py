```python
import streamlit as st
import pandas as pd
import yfinance as yf
import os
from fyers_apiv3 import fyersModel

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="📈 Fyers Trading Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==================================================
# CONFIG
# ==================================================

try:
    CLIENT_ID = os.getenv("FYERS_CLIENT_ID") or st.secrets["FYERS_CLIENT_ID"]
    SECRET_KEY = os.getenv("FYERS_SECRET_KEY") or st.secrets["FYERS_SECRET_KEY"]
except Exception:
    st.error("FYERS credentials not found in Streamlit Secrets")
    st.stop()

REDIRECT_URI = "https://manoharr43-hub-norenrestapipy-ap-hk1emv.streamlit.app/"

# ==================================================
# SESSION MODEL
# ==================================================

def get_session():
    return fyersModel.SessionModel(
        client_id=CLIENT_ID,
        secret_key=SECRET_KEY,
        redirect_uri=REDIRECT_URI,
        response_type="code",
        grant_type="authorization_code"
    )

# ==================================================
# TITLE
# ==================================================

st.title("📈 FYERS Trading Dashboard")

# ==================================================
# LOGIN FLOW
# ==================================================

if "access_token" not in st.session_state:

    params = st.query_params

    auth_code = (
        params.get("auth_code")
        or params.get("code")
    )

    if auth_code:

        try:

            if isinstance(auth_code, list):
                auth_code = auth_code[0]

            session = get_session()

            session.set_token(auth_code)

            token_response = session.generate_token()

            if (
                isinstance(token_response, dict)
                and "access_token" in token_response
            ):

                st.session_state["access_token"] = token_response["access_token"]

                st.success("✅ Login Successful")

                st.rerun()

            else:

                st.error("Token Generation Failed")
                st.json(token_response)
                st.stop()

        except Exception as e:

            st.error(f"Login Error: {e}")
            st.stop()

    else:

        try:

            session = get_session()

            auth_url = session.generate_authcode()

            st.markdown("## 🔐 Login Required")

            st.link_button(
                "Login With FYERS",
                auth_url
            )

            st.stop()

        except Exception as e:

            st.error(f"Auth URL Error: {e}")
            st.stop()

# ==================================================
# CREATE FYERS OBJECT
# ==================================================

try:

    fyers = fyersModel.FyersModel(
        client_id=CLIENT_ID,
        token=st.session_state["access_token"],
        is_async=False,
        log_path=""
    )

except Exception as e:

    st.error(f"FYERS Connection Error: {e}")
    st.stop()

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.success("🟢 Logged In")

menu = st.sidebar.radio(
    "Select Menu",
    [
        "Profile",
        "Funds",
        "Holdings",
        "Positions",
        "Scanner"
    ]
)

# ==================================================
# PROFILE
# ==================================================

if menu == "Profile":

    st.subheader("👤 Profile")

    try:

        profile = fyers.get_profile()

        st.json(profile)

    except Exception as e:

        st.error(e)

# ==================================================
# FUNDS
# ==================================================

elif menu == "Funds":

    st.subheader("💰 Funds")

    try:

        funds = fyers.funds()

        st.json(funds)

    except Exception as e:

        st.error(e)

# ==================================================
# HOLDINGS
# ==================================================

elif menu == "Holdings":

    st.subheader("📦 Holdings")

    try:

        holdings = fyers.holdings()

        st.json(holdings)

    except Exception as e:

        st.error(e)

# ==================================================
# POSITIONS
# ==================================================

elif menu == "Positions":

    st.subheader("📊 Positions")

    try:

        positions = fyers.positions()

        st.json(positions)

    except Exception as e:

        st.error(e)

# ==================================================
# STOCK SCANNER
# ==================================================

elif menu == "Scanner":

    st.subheader("🚀 NSE Scanner")

    stocks = [
        "RELIANCE.NS",
        "TCS.NS",
        "INFY.NS",
        "HDFCBANK.NS",
        "ICICIBANK.NS",
        "SBIN.NS",
        "LT.NS",
        "AXISBANK.NS",
        "ITC.NS",
        "BHARTIARTL.NS"
    ]

    @st.cache_data(ttl=300)
    def get_data(symbol):

        return yf.download(
            symbol,
            period="6mo",
            progress=False,
            auto_adjust=True
        )

    results = []

    with st.spinner("Scanning Stocks..."):

        for stock in stocks:

            try:

                df = get_data(stock)

                if len(df) < 50:
                    continue

                close = df["Close"]

                sma20 = close.rolling(20).mean()
                sma50 = close.rolling(50).mean()

                current = float(close.iloc[-1])

                ma20 = float(sma20.iloc[-1])
                ma50 = float(sma50.iloc[-1])

                if current > ma20 and ma20 > ma50:

                    signal = "🟢 Strong Bullish"

                elif current > ma20:

                    signal = "🟡 Bullish"

                else:

                    signal = "🔴 Bearish"

                results.append([
                    stock,
                    round(current, 2),
                    round(ma20, 2),
                    round(ma50, 2),
                    signal
                ])

            except Exception as e:

                st.warning(f"{stock}: {e}")

    result_df = pd.DataFrame(
        results,
        columns=[
            "Stock",
            "Price",
            "SMA20",
            "SMA50",
            "Signal"
        ]
    )

    st.dataframe(
        result_df,
        use_container_width=True
    )

    csv = result_df.to_csv(index=False)

    st.download_button(
        "⬇ Download CSV",
        csv,
        file_name="scanner_results.csv",
        mime="text/csv"
    )

# ==================================================
# LOGOUT
# ==================================================

if st.sidebar.button("🚪 Logout"):

    st.session_state.clear()

    st.rerun()
```
