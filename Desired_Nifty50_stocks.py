import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="Nifty50 SOM Pro", layout="wide")
st.title("Nifty50 Dashboard - SOM SHEKHAR 2026")
st.caption("CMP | Daily RSI | Weekly RSI | Bullish/Bearish | 52W High Low")

# Nifty 50 stocks
STOCKS = ["ADANIENT.NS","ADANIPORTS.NS","APOLLOHOSP.NS","ASIANPAINT.NS","AXISBANK.NS","BAJAJ-AUTO.NS","BAJAJFINSV.NS","BAJFINANCE.NS","BEL.NS","BHARTIARTL.NS","CIPLA.NS","COALINDIA.NS","DRREDDY.NS","EICHERMOT.NS","ETERNAL.NS","GRASIM.NS","HCLTECH.NS","HDFCBANK.NS","HDFCLIFE.NS","HINDALCO.NS","HINDUNILVR.NS","ICICIBANK.NS","INDIGO.NS","INFY.NS","ITC.NS","JSWSTEEL.NS","KOTAKBANK.NS","LT.NS","M&M.NS","MARUTI.NS","NESTLEIND.NS","NTPC.NS","ONGC.NS","POWERGRID.NS","RELIANCE.NS","SBILIFE.NS","SBIN.NS","SHRIRAMFIN.NS","SUNPHARMA.NS","TATACONSUM.NS","TATAMOTORS.NS","TATASTEEL.NS","TECHM.NS","TITAN.NS","TRENT.NS","ULTRACEMCO.NS","WIPRO.NS","HEROMOTOCO.NS","INDUSINDBK.NS"]

def calc_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

@st.cache_data(ttl=300)
def get_data():
    rows = []
    for sym in STOCKS:
        try:
            tk = yf.Ticker(sym)
            daily = tk.history(period="1y")
            if daily.empty: continue
            
            weekly = daily['Close'].resample('W').last()
            
            d_rsi = calc_rsi(daily['Close']).iloc[-1]
            w_rsi = calc_rsi(weekly).iloc[-1]
            
            cmp_price = daily['Close'].iloc[-1]
            high_52 = daily['High'].max()
            low_52 = daily['Low'].min()
            
            # Logic aapke hisab se
            if d_rsi > 60 and w_rsi > 60:
                signal = "🟢 BULLISH"
            elif d_rsi < 40 and w_rsi < 40:
                signal = "🔴 BEARISH"
            elif 40 <= d_rsi <= 60 and 40 <= w_rsi <= 60:
                signal = "🟡 NEUTRAL"
            else:
                signal = "⚪ NEUTRAL"
            
            rows.append({
                "Stock": sym.replace(".NS",""),
                "CMP": round(cmp_price,2),
                "Daily RSI": round(d_rsi,1),
                "Weekly RSI": round(w_rsi,1),
                "Signal": signal,
                "52W High": round(high_52,2),
                "52W Low": round(low_52,2)
            })
        except:
            continue
    return pd.DataFrame(rows)

with st.spinner("50 stocks ka data + RSI nikal raha hun... 1 min lagega"):
    df = get_data()

if not df.empty:
    # Filter
    f = st.selectbox("Filter:", ["All","BULLISH Only","BEARISH Only","NEUTRAL Only"])
    if f == "BULLISH Only":
        df = df[df['Signal'].str.contains("BULLISH")]
    elif f == "BEARISH Only":
        df = df[df['Signal'].str.contains("BEARISH")]
    elif f == "NEUTRAL Only":
        df = df[df['Signal'].str.contains("NEUTRAL")]

    st.dataframe(df, use_container_width=True, height=800)
    st.success(f"Total {len(df)} stocks loaded")
else:
    st.error("Data load nahi hua")

if st.button("Refresh"):
    st.cache_data.clear()
    st.rerun()

st.download_button("Download CSV", df.to_csv(index=False), "nifty50_rsi_dashboard.csv")
