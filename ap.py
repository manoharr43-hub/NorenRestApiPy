import streamlit as st
import pandas as pd
import yfinance as yf
import os
from fyers_apiv3 import fyersModel

# ==================================================
# CONFIG
# ==================================================

st.set_page_config(
    page_title="Fyers Trading Dashboard",
    page_icon="📈",
    layout="wide"
)

CLIENT_ID = os.getenv("FYERS_CLIENT_ID", st.secrets.get("FYERS_CLIENT_ID", ""))
SECRET_KEY = os.getenv("FYERS_SECRET_KEY", st.secrets.get("FYERS_SECRET_KEY", ""))

REDIRECT_URI = "https://manoharr43-hub-norenrestapipy-ap-hk1emv.streamlit.app/"

if not CLIENT_ID:
    st.error("FYERS_CLIENT_ID Missing")
    st.stop()

if not SECRET_KEY:
    st.error("FYERS_SECRET_KEY Missing")
    st.stop()

# ==================================================
# LOGIN SESSION
# ==================================================

def get_session():
    return fyersModel.SessionModel(
        client_id=CLIENT_ID,
        secret_key=SECRET_KEY,
        redirect_uri=REDIRECT_URI,
        response_type="code",
        grant_type="authorization_code"
    )

st.title("📈 Fyers Trading Dashboard")

# ==================================================
# LOGIN
# ==================================================

if "access_token" not in st.session_state:

    params = st.query_params

    code = params.get("code")

    if code:

        try:

            session = get_session()

            if isinstance(code, list):
                code = code[0]

            session.set_token(code)

            response = session.generate_token()

            if (
                isinstance(response, dict)
                and "access_token" in response
            ):

                st.session_state["access_token"] = response["access_token"]

                st.success("Login Successful")

                st.rerun()

            else:

                st.error(response)
                st.info("Please login again")

                st.stop()

        except Exception as e:

            st.error(f"Login Error: {e}")
            st.stop()

    else:

        session = get_session()

        auth_url = session.generate_authcode()

        st.markdown(
            f"""
            ### Login Required

            [🔐 Login With Fyers]({auth_url})
            """
        )

        st.stop()

# ==================================================
# FYERS OBJECT
# ==================================================

try:

    fyers = fyersModel.FyersModel(
        client_id=CLIENT_ID,
        token=st.session_state["access_token"],
        is_async=False,
        log_path=""
    )

except Exception as e:

    st.error(e)
    st.stop()

# ==================================================
# SIDEBAR
# ==================================================

menu = st.sidebar.radio(
    "Menu",
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

    st.subheader("Profile")

    try:
        st.json(fyers.get_profile())
    except Exception as e:
        st.error(e)

# ==================================================
# FUNDS
# ==================================================

elif menu == "Funds":

    st.subheader("Funds")

    try:
        st.json(fyers.funds())
    except Exception as e:
        st.error(e)

# ==================================================
# HOLDINGS
# ==================================================

elif menu == "Holdings":

    st.subheader("Holdings")

    try:

        data = fyers.holdings()

        st.json(data)

    except Exception as e:

        st.error(e)

# ==================================================
# POSITIONS
# ==================================================

elif menu == "Positions":

    st.subheader("Positions")

    try:

        data = fyers.positions()

        st.json(data)

    except Exception as e:

        st.error(e)

# ==================================================
# NSE SCANNER
# ==================================================

elif menu == "Scanner":

    st.subheader("📊 NSE Scanner")

    stocks = [
        "RELIANCE.NS",
        "TCS.NS",
        "INFY.NS",
        "HDFCBANK.NS",
        "ICICIBANK.NS",
        "SBIN.NS",
        "LT.NS"
    ]

    result = []

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

                result.append(
                    [
                        stock,
                        round(current, 2),
                        round(ma20, 2),
                        signal
                    ]
                )

            except:
                pass

    st.dataframe(
        pd.DataFrame(
            result,
            columns=[
                "Stock",
                "Price",
                "20 SMA",
                "Signal"
            ]
        ),
        use_container_width=True
    )

# ==================================================
# LOGOUT
# ==================================================

if st.sidebar.button("Logout"):

    st.session_state.clear()

    st.rerun()
