import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Nifty50 SOM 2026", layout="wide")
st.title("Nifty50 - All 50 Stocks Dashboard")
st.caption("SOM SHEKHAR 2026 | Laptop OFF me bhi chalega | Tab Ready")

# NIFTY 50 - Pure 50 stocks (Oct 2026 list)
NIFTY50 = [
    "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS", "AXISBANK.NS",
    "BAJAJ-AUTO.NS", "BAJAJFINSV.NS", "BAJFINANCE.NS", "BEL.NS", "BHARTIARTL.NS",
    "BSE.NS", "CIPLA.NS", "COALINDIA.NS", "DRREDDY.NS", "EICHERMOT.NS",
    "ETERNAL.NS", "GRASIM.NS", "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS",
    "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "INDIGO.NS", "INFY.NS",
    "ITC.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LT.NS", "M&M.NS",
    "MARUTI.NS", "NESTLEIND.NS", "NTPC.NS", "ONGC.NS", "POWERGRID.NS",
    "RELIANCE.NS", "SBILIFE.NS", "SBIN.NS", "SHRIRAMFIN.NS", "SUNPHARMA.NS",
    "TATACONSUM.NS", "TATAMOTORS.NS", "TATASTEEL.NS", "TECHM.NS", "TITAN.NS",
    "TRENT.NS", "ULTRACEMCO.NS", "WIPRO.NS", "HEROMOTOCO.NS", "INDUSINDBK.NS"
]

@st.cache_data(ttl=90)
def get_all_data():
    data = []
    for sym in NIFTY50:
        try:
            tk = yf.Ticker(sym)
            h = tk.history(period="5d")
            if not h.empty:
                cmp_price = h['Close'].iloc[-1]
                prev = h['Close'].iloc[-2] if len(h) > 1 else cmp_price
                chg = ((cmp_price - prev)/prev)*100
                data.append({
                    "Stock": sym.replace(".NS",""),
                    "CMP": round(float(cmp_price),2),
                    "Change %": round(float(chg),2)
                })
        except:
            data.append({"Stock": sym.replace(".NS",""), "CMP": "NA", "Change %": 0})
    return pd.DataFrame(data)

with st.spinner("Nifty 50 data load ho raha hai..."):
    df = get_all_data()

# Color coding
def color_change(val):
    if isinstance(val, (int, float)):
        return 'color: green' if val > 0 else 'color: red'
    return ''

if not df.empty:
 st.dataframe(df, use_container_width=True)
    st.success(f"Total {len(df)} stocks loaded | Auto refresh: 90 sec")
else:
    st.error("Data nahi aaya, Refresh kijiye")

col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 Refresh Now"):
        st.cache_data.clear()
        st.rerun()
with col2:
    st.download_button("Download CSV", df.to_csv(index=False), "nifty50_som_2026.csv")
