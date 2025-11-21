import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="HighRoller.pw – Live Bonus Hunter", layout="wide", initial_sidebar_state="expanded")
st.markdown("<h1 style='text-align: center; color: gold;'>🔥 HIGHROLLER.PW – #1 Crypto Bonus Hunter 2025 🔥</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:20px;'>Live bonuses • Arbitrage calculator • No-KYC filter • Updated every 6 hours</p>", unsafe_allow_html=True)

# Google Sheet pull
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
gc = gspread.authorize(creds)
sheet = gc.open("HighRollerBonuses").sheet1
df = pd.DataFrame(sheet.get_all_records())

# Sidebar filters
st.sidebar.header("Filters")
no_kyc = st.sidebar.checkbox("No-KYC Casinos Only")
min_bonus = st.sidebar.slider("Min Bonus %", 50, 500, 100)

# Display table
st.dataframe(df.style.set_properties(**{'background-color': 'black', 'color': 'gold'}), use_container_width=True)

# Arbitrage Calculator
st.markdown("### 🎰 Bonus Arbitrage EV Calculator")
col1, col2 = st.columns(2)
with col1:
    deposit = st.number_input("Deposit Amount ($)", 100, 100000, 1000)
    bonus_perc = st.slider("Bonus Percentage", 50, 500, 200)
with col2:
    wagering = st.number_input("Wagering Requirement (x)", 1, 100, 30)
    house_edge = st.slider("Game House Edge (%)", 0.5, 5.0, 1.0, 0.1)/100

bonus_amount = deposit * (bonus_perc / 100)
total_wagered = (deposit + bonus_amount) * wagering
ev = bonus_amount - (total_wagered * house_edge)

st.metric("Expected Value (EV)", f"${ev:,.2f}", delta=f"{(ev/deposit)*100:.1f}% ROI" if deposit else None)

if ev > 0:
    st.success("🎉 POSITIVE EV – ABUSE THIS BONUS NOW")
else:
    st.error("Negative EV – skip or use low-edge games")

# Email capture
st.text_input("Get bonus drop alerts →", placeholder="your@email.com")