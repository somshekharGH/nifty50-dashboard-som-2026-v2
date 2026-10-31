import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Nifty50 SOM Dashboard", layout="wide")
st.title("Nifty50 Dashboard - SOM SHEKHAR 2026")
st.write("Laptop OFF rahega tab bhi yaha data dikhega")

# Aapke desired stocks - yaha aap apne stocks add kar sakte hain
    STOCKS = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "ITC.NS", "LT.NS", "AXISBANK.NS", "KOTAKBANK.NS", "BAJFINANCE.NS", "MARUTI.NS", "SUNPHARMA.NS", "WIPRO.NS", "ULTRACEMCO.NS", "TITAN.NS", "ONGC.NS", "NTPC.NS", "POWERGRID.NS", "M&M.NS", "TATASTEEL.NS", "HCLTECH.NS", "BAJAJFINSV.NS", "ADANIENT.NS", "ADANIPORTS.NS"]
@st.cache_data(ttl=60)
def get_nifty_data():
    rows = []
    for symbol in STOCKS:
        try:
            t = yf.Ticker(symbol)
            hist = t.history(period="2d")
            if len(hist) >= 1:
                cmp = hist['Close'].iloc[-1]
                prev = hist['Close'].iloc[-2] if len(hist) > 1 else cmp
                change = ((cmp - prev)/prev)*100
                rows.append({"Stock": symbol.replace(".NS",""), "CMP": round(cmp,2), "Change %": round(change,2)})
        except:
            pass
    return pd.DataFrame(rows)

df = get_nifty_data()
if not df.empty:
    st.dataframe(df, use_container_width=True)
    st.success(f"Last Updated - Auto Refresh har 1 min me")
else:
    st.error("Data load nahi hua, thodi der baad refresh kijiye")

if st.button("Refresh Now"):
    st.cache_data.clear()
    st.rerun()
