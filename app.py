import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="EasyCharts Pro - Nifty 200", layout="wide")

# Auto Refresh Every 60 Seconds
st_autorefresh(interval=60000, key="nifty200refresh")

# Custom CSS for Styling
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .header {background: linear-gradient(135deg, #0f172a, #1e40af); padding: 25px; border-radius: 12px; color: white; text-align: center;}
    .section {background: linear-gradient(135deg, #f97316, #fb923c); color: white; padding: 10px; border-radius: 8px; font-weight: bold; margin: 15px 0 5px 0; text-align: center;}
    .pre {background: linear-gradient(135deg, #22c55e, #16a34a); color: white;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header"><h1>EasyCharts Pro</h1><p>Nifty 200 Real-time Multi-Scanner</p></div>', unsafe_allow_html=True)

# Nifty 200 Full List
nifty200_symbols = [
    "ABB.NS", "ACC.NS", "ADANIENSOL.NS", "ADANIENT.NS", "ADANIGREEN.NS", "ADANIPORTS.NS", "ADANIPOWER.NS", "ATGL.NS", "AMBUJACEM.NS", "APOLLOHOSP.NS",
    "APOLLOTYRE.NS", "ASHOKLEY.NS", "ASIANPAINT.NS", "ASTRAL.NS", "AUROPHARMA.NS", "AVANTIFEED.NS", "AXISBANK.NS", "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS",
    "BAJAJHLDNG.NS", "BALKRISIND.NS", "BANDHANBNK.NS", "BANKBARODA.NS", "BANKINDIA.NS", "BATAINDIA.NS", "BEL.NS", "BERGEPAINT.NS", "BHARATFORG.NS", "BHEL.NS",
    "BPCL.NS", "BHARTIARTL.NS", "BIOCON.NS", "BOSCHLTD.NS", "BRITANNIA.NS", "CANBK.NS", "CGPOWER.NS", "CHOLAFIN.NS", "CIPLA.NS", "COALINDIA.NS",
    "COFORGE.NS", "COLPAL.NS", "CONCOR.NS", "CUMMINSIND.NS", "DLF.NS", "DABUR.NS", "DALBHARAT.NS", "DEEPAKNTR.NS", "DELHIVERY.NS", "DIVISLAB.NS",
    "DIXON.NS", "DMART.NS", "DRREDDY.NS", "EICHERMOT.NS", "ESCORTS.NS", "EXIDEIND.NS", "FEDERALBNK.NS", "FORTIS.NS", "GAIL.NS", "GLAND.NS",
    "GLENMARK.NS", "GMRINFRA.NS", "GODREJCP.NS", "GODREJPROP.NS", "GRASIM.NS", "GUJGASLTD.NS", "HAL.NS", "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS",
    "HAVELLS.NS", "HEROMOTOCO.NS", "HINDALCO.NS", "HINDCOPPER.NS", "HINDPETRO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "ICICIGI.NS", "ICICIPRULI.NS", "IDFCFIRSTB.NS",
    "ITC.NS", "INDIHOTEL.NS", "IOC.NS", "IRCTC.NS", "IRFC.NS", "IGL.NS", "INDUSTOWER.NS", "INDUSINDBK.NS", "NAUKRI.NS", "INFY.NS",
    "INDIGO.NS", "IPCALAB.NS", "JSWENERGY.NS", "JSWSTEEL.NS", "JINDALSTEL.NS", "JIOFIN.NS", "JUBLFOOD.NS", "KOTAKBANK.NS", "LTIM.NS", "LT.NS",
    "LICI.NS", "LAURUSLABS.NS", "LUPIN.NS", "MRF.NS", "M&M.NS", "M&MFIN.NS", "MANAPPURAM.NS", "MARICO.NS", "MARUTI.NS", "MAXHEALTH.NS",
    "METROPOLIS.NS", "MPHASIS.NS", "MUTHOOTFIN.NS", "NTPC.NS", "NATIONALUM.NS", "NAVINFLUOR.NS", "NESTLEIND.NS", "NMDC.NS", "NYKAA.NS", "OBEROIRLTY.NS",
    "ONGC.NS", "OIL.NS", "PAYTM.NS", "PIIND.NS", "PFC.NS", "POLYCAP.NS", "POONAWALLA.NS", "POWERGRID.NS", "PRESTIGE.NS", "PNB.NS",
    "RECLTD.NS", "RELIANCE.NS", "RVNL.NS", "SAIL.NS", "SBICARD.NS", "SBILIFE.NS", "SRF.NS", "MOTHERSON.NS", "SHREECEM.NS", "SHRIRAMFIN.NS",
    "SIEMENS.NS", "SJVN.NS", "SKFINDIA.NS", "SOLARINDS.NS", "SONACOMS.NS", "SBIN.NS", "SUNPHARMA.NS", "SUNTV.NS", "SYNGENE.NS", "TVSMOTOR.NS",
    "TATACOMM.NS", "TATACONSUM.NS", "TATAELXSI.NS", "TATAMOTORS.NS", "TATAPOWER.NS", "TATASTEEL.NS", "TCS.NS", "TECHM.NS", "TITAN.NS", "TORNTPHARM.NS",
    "TRENT.NS", "TRIDENT.NS", "TIINDIA.NS", "UPL.NS", "ULTRACEMCO.NS", "UNIONBANK.NS", "UNITDSPR.NS", "VBL.NS", "VEDL.NS", "VOLTAS.NS",
    "WIPRO.NS", "YESBANK.NS", "ZOMATO.NS", "ZYDUSLIFE.NS"
]

results = []

with st.spinner("⚡ Fetching and Analyzing Nifty 200 Market Data in 1-Second..."):
    # 200 സ്റ്റോക്കുകളുടെയും ഡാറ്റ സിംഗിൾ റിക്വസ്റ്റിൽ ഡൗൺലോഡ് ചെയ്യുന്നു (High Speed Batch Request)
    all_data = yf.download(nifty200_symbols, period="1mo", interval="1d", group_by="ticker", progress=False)

    for symbol in nifty200_symbols:
        try:
            if symbol not in all_data.columns.levels[0]:
                continue
                
            hist = all_data[symbol].dropna()
            if len(hist) < 6: 
                continue
            
            last_price = float(hist['Close'].iloc[-1])
            prev_close = float(hist['Close'].iloc[-2])
            vol = float(hist['Volume'].iloc[-1])
            
            avg_vol = float(hist['Volume'].iloc[-6:-1].mean())
            
            change = ((last_price - prev_close) / prev_close) * 100
            vol_ratio = vol / avg_vol if avg_vol > 0 else 1.0
            name = symbol.replace(".NS", "")
            
            results.append({
                "Stock": f"🚨 {name}" if vol_ratio > 2.0 else name,
                "LTP": round(last_price, 2),
                "%Chg": round(change, 2),
                "Volx": round(vol_ratio, 2),
                "Chart": f"https://www.tradingview.com/chart/?symbol=NSE:{name}",
                "PreBreakout": (0 < change < 1.5),
                "Score": round(abs(change) * 2 + (vol_ratio * 3), 1)
            })
        except:
            continue

if results:
    df = pd.DataFrame(results)
    st.info(f"🕒 Market Scan Time: {datetime.now().strftime('%I:%M:%S %p')} | Mode: Nifty 200")
    
    config = {"Chart": st.column_config.LinkColumn("View Chart")}
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown('<div class="section pre">🔵 Pre-Breakout</div>', unsafe_allow_html=True)
        pre_df = df[df["PreBreakout"]].sort_values("Score", ascending=False).head(12)
        st.dataframe(pre_df[["Stock","LTP","%Chg","Chart"]], column_config=config, use_container_width=True, hide_index=True)

    with c2:
        st.markdown('<div class="section">🟢 Live Breakout</div>', unsafe_allow_html=True)
        live_df = df[df["%Chg"] > 2.5].sort_values("%Chg", ascending=False).head(12)
        st.dataframe(live_df[["Stock","LTP","%Chg","Chart"]], column_config=config, use_container_width=True, hide_index=True)

    with c3:
        st.markdown('<div class="section">🔥 Volume Spike</div>', unsafe_allow_html=True)
        vol_df = df.sort_values("Volx", ascending=False).head(12)
        st.dataframe(vol_df[["Stock","LTP","Volx","Chart"]], column_config=config, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown('<div class="section">🟠 All Momentum Stocks (Nifty 200)</div>', unsafe_allow_html=True)
    st.dataframe(df.sort_values("Score", ascending=False).head(20)[["Stock","LTP","%Chg","Volx","Chart"]], column_config=config, use_container_width=True, hide_index=True)