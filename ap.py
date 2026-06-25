import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(
    page_title="NSE Stock Scanner",
    page_icon="📈",
    layout="wide"
)

st.title("📈 NSE Stock Scanner")

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

results = []

with st.spinner("Scanning stocks..."):

    for stock in stocks:

        try:

            df = yf.download(
                stock,
                period="6mo",
                progress=False,
                auto_adjust=True
            )

            if len(df) < 50:
                continue

            close = df["Close"]

            sma20 = close.rolling(20).mean()
            sma50 = close.rolling(50).mean()

            current = float(close.iloc[-1])
            ma20 = float(sma20.iloc[-1])
            ma50 = float(sma50.iloc[-1])

            if current > ma20 and ma20 > ma50:
                signal = "Strong Bullish"
            elif current > ma20:
                signal = "Bullish"
            else:
                signal = "Bearish"

            results.append(
                [
                    stock,
                    round(current, 2),
                    round(ma20, 2),
                    round(ma50, 2),
                    signal
                ]
            )

        except Exception as e:
            st.warning(f"{stock}: {e}")

df_result = pd.DataFrame(
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
    df_result,
    use_container_width=True
)

csv = df_result.to_csv(index=False)

st.download_button(
    "⬇ Download CSV",
    csv,
    file_name="scanner_results.csv",
    mime="text/csv"
)
