import streamlit as st
import pandas as pd
import yfinance as yf

# -------------------------------
# Streamlit Page Config
# -------------------------------
st.set_page_config(
    page_title="NSE Stock Scanner",
    page_icon="📈",
    layout="wide"
)

st.title("📈 NSE Stock Scanner")

# -------------------------------
# Stock List
# -------------------------------
stocks = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS",
    "ICICIBANK.NS", "SBIN.NS", "LT.NS", "AXISBANK.NS",
    "ITC.NS", "BHARTIARTL.NS"
]

# -------------------------------
# Helper Functions
# -------------------------------
@st.cache_data(ttl=300)
def get_data(stock):
    return yf.download(
        stock,
        period="6mo",
        auto_adjust=True,
        progress=False
    )

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# -------------------------------
# Scanner Logic
# -------------------------------
results = []

with st.spinner("🔍 Scanning Stocks..."):
    for stock in stocks:
        try:
            df = get_data(stock)

            if df.empty or len(df) < 50:
                continue

            close = df["Close"]

            sma20 = close.rolling(20).mean()
            sma50 = close.rolling(50).mean()
            rsi = calculate_rsi(close).iloc[-1]

            # ✅ Use .values[-1] to avoid Series error
            current = round(float(close.values[-1]), 2)
            ma20 = round(float(sma20.values[-1]), 2)
            ma50 = round(float(sma50.values[-1]), 2)
            rsi_val = round(float(rsi), 2)

            # Signal Logic
            if current > ma20 and ma20 > ma50 and rsi_val > 60:
                signal = "🔥 Strong Bullish"
            elif current > ma20:
                signal = "📈 Bullish"
            elif rsi_val < 40:
                signal = "⚠️ Strong Bearish"
            else:
                signal = "📉 Bearish"

            results.append({
                "Stock": stock,
                "Price": current,
                "SMA20": ma20,
                "SMA50": ma50,
                "RSI": rsi_val,
                "Signal": signal
            })

        except Exception as e:
            st.warning(f"{stock}: {e}")

# -------------------------------
# Display Results
# -------------------------------
if results:
    result_df = pd.DataFrame(results)

    st.dataframe(
        result_df,
        use_container_width=True
    )

    # Download CSV
    csv = result_df.to_csv(index=False)
    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name="scanner_results.csv",
        mime="text/csv"
    )
else:
    st.error("No stock data found.")
