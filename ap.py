import streamlit as st
import pandas as pd
import yfinance as yf
import os
from fyers_apiv3 import fyersModel

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Fyers Trading Dashboard",
    page_icon="📈",
    layout="wide"
)

# =====================================================
# FYERS CONFIG
# =====================================================

CLIENT_ID = os.getenv("FYERS_CLIENT_ID") or st.secrets.get("FYERS_CLIENT_ID")
SECRET_KEY = os.getenv("FYERS_SECRET_KEY") or st.secrets.get("FYERS_SECRET_KEY")

REDIRECT_URI = "https://manoharr43-hub-norenrestapipy-ap-hk1emv.streamlit.app/"

if not CLIENT_ID or not SECRET_KEY:
    st.error("Fyers Client ID / Secret Key Missing")
    st.stop()

# =====================================================
# LOGIN SESSION
# =====================================================

def create_session():
    return fyersModel.SessionModel(
        client_id=CLIENT_ID,
        secret_key=SECRET_KEY,
        redirect_uri=REDIRECT_URI,
        response_type="code",
        grant_type="authorization_code"
    )

session = create_session()

st.title("📈 Fyers Trading Dashboard")

# =====================================================
# LOGIN
# =====================================================

params = st.query_params

if "access_token" not in st.session_state:

    code = params.get("code")

    if code:

        if isinstance(code, list):
            code = code[0]

        try:

            session.set_token(code)

            token_response = session.generate_token()

            if "access_token" in token_response:

                st.session_state["access_token"] = token_response["access_token"]

                st.success("✅ Login Successful")

                st.rerun()

            else:
                st.error(token_response)

        except Exception as e:
            st.error(f"Login Error: {e}")

    else:

        auth_url = session.generate_authcode()

        st.markdown(
            f"""
            ### Login Required

            [🔐 Login With Fyers]({auth_url})
            """
        )

        st.stop()

# =====================================================
# FYERS OBJECT
# =====================================================

fyers = fyersModel.FyersModel(
    client_id=CLIENT_ID,
    token=st.session_state["access_token"],
    is_async=False,
    log_path=""
)

# =====================================================
# SIDEBAR
# =====================================================

menu = st.sidebar.radio(
    "Select",
    [
        "Profile",
        "Funds",
        "Holdings",
        "Positions",
        "Scanner"
    ]
)

# =====================================================
# PROFILE
# =====================================================

if menu == "Profile":

    st.subheader("Profile")

    try:
        profile = fyers.get_profile()
        st.json(profile)
    except Exception as e:
        st.error(str(e))

# =====================================================
# FUNDS
# =====================================================

elif menu == "Funds":

    st.subheader("Funds")

    try:
        funds = fyers.funds()
        st.json(funds)
    except Exception as e:
        st.error(str(e))

# =====================================================
# HOLDINGS
# =====================================================

elif menu == "Holdings":

    st.subheader("Holdings")

    try:
        holdings = fyers.holdings()
        st.json(holdings)
    except Exception as e:
        st.error(str(e))

# =====================================================
# POSITIONS
# =====================================================

elif menu == "Positions":

    st.subheader("Positions")

    try:
        positions = fyers.positions()
        st.json(positions)
    except Exception as e:
        st.error(str(e))

# =====================================================
# NSE SCANNER
# =====================================================

elif menu == "Scanner":

    st.subheader("📊 NSE Scanner")

    stocks = [
        "RELIANCE.NS",
        "TCS.NS",
        "INFY.NS",
        "ICICIBANK.NS",
        "HDFCBANK.NS",
        "SBIN.NS",
        "LT.NS"
    ]

    results = []

    with st.spinner("Scanning Stocks..."):

        for stock in stocks:

            try:

                df = yf.download(
                    stock,
                    period="3mo",
                    progress=False,
                    auto_adjust=True
                )

                if len(df) < 20:
                    continue

                close = df["Close"]

                sma20 = close.rolling(20).mean()

                current = float(close.iloc[-1])
                ma20 = float(sma20.iloc[-1])

                signal = (
                    "Bullish"
                    if current > ma20
                    else "Bearish"
                )

                results.append([
                    stock,
                    round(current, 2),
                    round(ma20, 2),
                    signal
                ])

            except:
                pass

    result_df = pd.DataFrame(
        results,
        columns=[
            "Stock",
            "Price",
            "20 SMA",
            "Signal"
        ]
    )

    st.dataframe(
        result_df,
        use_container_width=True
    )

# =====================================================
# LOGOUT
# =====================================================

if st.sidebar.button("Logout"):

    st.session_state.clear()

    st.rerun()
