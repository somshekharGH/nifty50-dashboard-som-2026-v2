import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Nifty50 SOM Dashboard", layout="wide")

st.markdown("<h1 style='text-align:center;color:#0d47a1;'>Nifty50 - SOM SHEKHAR 2026</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>CMP | Daily RSI | Weekly RSI | Bullish/Bearish | 52W High Low</p>", unsafe_allow_html=True)

STOCKS = ["RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS","SBIN.NS","BHARTIARTL.NS","ITC.NS","LT.NS","AXISBANK.NS","KOTAKBANK.NS","BAJFINANCE.NS","MARUTI.NS","SUNPHARMA.NS","WIPRO.NS","ULTRACEMCO.NS","TITAN.NS","ONGC.NS","NTPC.NS","POWERGRID.NS","M&M.NS","TATASTEEL.NS","HCLTECH.NS","BAJAJFINSV.NS","ADANIENT.NS","ADANIPORTS.NS","ASIANPAINT.NS","NESTLEIND.NS","GRASIM.NS","JSWSTEEL.NS","HINDALCO.NS","CIPLA.NS","DRREDDY.NS","EICHERMOT.NS","BRITANNIA.NS","DIVISLAB.NS","HINDUNILVR.NS","SBILIFE.NS","HDFCLIFE.NS","COALINDIA.NS","BAJAJ-AUTO.NS","HEROMOTOCO.NS","INDUSINDBK.NS","TATAMOTORS.NS","TATACONSUM.NS","TECHM.NS","APOLLOHOSP.NS","BEL.NS","TRENT.NS"]

def calc_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

@st.cache_data(ttl=600)
def load():
    data = []
    for s in STOCKS:
        try:
            hist = yf.Ticker(s).history(period="1y")
            if len(hist) < 20: continue
            weekly_close = hist['Close'].resample('W').last()
            d_rsi = calc_rsi(hist['Close']).iloc[-1]
            w_rsi = calc_rsi(weekly_close).iloc[-1]
            cmp = hist['Close'].iloc[-1]
            high = hist['High'].max()
            low = hist['Low'].min()
            if d_rsi > 60 and w_rsi > 60:
                sig = "🟢 BULLISH"
            elif d_rsi < 40 and w_rsi < 40:
                sig = "🔴 BEARISH"
            else:
                sig = "⚪ NEUTRAL"
            data.append([s.replace(".NS",""), round(cmp,2), round(d_rsi,1), round(w_rsi,1), sig, round(high,2), round(low,2)])
        except:
            continue
    df = pd.DataFrame(data, columns=["Stock","CMP","Daily RSI","Weekly RSI","Signal","52W High","52W Low"])
    return df

df = load()

# Top Counts
c1,c2,c3,c4 = st.columns(4)
c1.metric("Total Stocks", len(df))
c2.metric("Bullish", len(df[df['Signal'].str.contains("BULLISH")]))
c3.metric("Bearish", len(df[df['Signal'].str.contains("BEARISH")]))
c4.metric("Neutral", len(df[df['Signal'].str.contains("NEUTRAL")]))

# Filter
choice = st.selectbox("Filter karo:", ["All","BULLISH","BEARISH","NEUTRAL"])
if choice != "All":
    df = df[df['Signal'].str.contains(choice)]

st.dataframe(df, use_container_width=True, height=700)

st.button("Refresh Data")
