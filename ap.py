import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(
page_title="📈 NSE Stock Scanner",
page_icon="📈",
layout="wide"
)

st.title("📈 NSE Stock Scanner V2")

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

with st.spinner("Scanning Stocks..."):

```
for stock in stocks:

    try:

        df = yf.download(
            stock,
            period="6mo",
            auto_adjust=True,
            progress=False
        )

        if df.empty:
            continue

        close = df["Close"].squeeze()

        if len(close) < 50:
            continue

        sma20 = close.rolling(20).mean()
        sma50 = close.rolling(50).mean()

        current = round(float(close.iloc[-1]), 2)
        ma20 = round(float(sma20.iloc[-1]), 2)
        ma50 = round(float(sma50.iloc[-1]), 2)

        if current > ma20 and ma20 > ma50:
            signal = "🟢 Strong Bullish"
        elif current > ma20:
            signal = "🟡 Bullish"
        else:
            signal = "🔴 Bearish"

        results.append({
            "Stock": stock,
            "Price": current,
            "SMA20": ma20,
            "SMA50": ma50,
            "Signal": signal
        })

    except Exception as e:

        st.warning(f"{stock}: {e}")
```

if results:

```
result_df = pd.DataFrame(results)

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
```

else:

```
st.error("No stocks found.")
```
