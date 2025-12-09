import streamlit as st
import pandas as pd
import time
import os
import sys

# Setup path agar module bisa diimport
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from components import navbar, leaderboard, alert
from utils.api import DexScreenerClient
from utils import formatter, detect, charts
from streamlit_autorefresh import st_autorefresh

# --- CONFIG ---
st.set_page_config(
    page_title="WhaleRadar | Smart Money Tracker",
    page_icon="🐋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

css_path = os.path.join(os.path.dirname(__file__), 'assets', 'styles.css')
load_css(css_path)

# --- STATE MANAGEMENT ---
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ["SOL", "ETH", "BTC"]

# --- AUTO REFRESH (Real-time emulation) ---
# Refresh setiap 30 detik
count = st_autorefresh(interval=30000, limit=None, key="fcounter")

# --- MAIN APP ---
def main():
    page = navbar.sidebar_nav()

    # --- 1. DASHBOARD OVERVIEW ---
    if page == "Dashboard Overview":
        st.title("📊 Market Overview")
        
        # Top Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        # Fetch Data Real untuk Header (Contoh SOL)
        sol_data = DexScreenerClient.search_pairs("SOL")
        if sol_data:
            main_pair = sol_data[0]
            price = formatter.format_usd(float(main_pair['priceUsd']))
            vol = formatter.format_usd(float(main_pair['volume']['h24']))
            change = f"{main_pair['priceChange']['h24']}%"
            
            col1.metric("SOL Price", price, change)
            col2.metric("24H Volume", vol, "High Activity")
            col3.metric("Whale Inflow", "$4.2M", "+12%") # Mock calculated
            col4.metric("Active Wallets", "12,405", "+340")

        # Featured Chart
        st.subheader("🔥 Trending: Solana (SOL)")
        # Simulasi data harga untuk chart (karena no historical api free)
        mock_prices = [100, 102, 105, 103, 108, 110, 115, 112, 120, 118] 
        st.plotly_chart(charts.render_candle_chart("SOL", mock_prices), use_container_width=True)
        
        # Alert System
        alert.check_for_alerts(main_pair if sol_data else None)

    # --- 2. SMART MONEY LEADERBOARD ---
    elif page == "Smart Money Leaderboard":
        st.title("🏆 Smart Money Leaderboard")
        st.markdown("Tracking wallets with >65% Win Rate and High PnL.")
        
        # Generate Dummy Data (karena butuh API paid Moralis/Dune untuk real wallet history)
        df_whales = detect.WhaleDetector.generate_dummy_wallet_labels()
        leaderboard.render_leaderboard(df_whales)

    # --- 3. WHALE ACCUMULATION ---
    elif page == "Whale Accumulation":
        st.title("🐋 Live Accumulation Detector")
        
        token_input = st.text_input("Analyze Token Address / Symbol", "JUP")
        
        if token_input:
            pairs = DexScreenerClient.search_pairs(token_input)
            if pairs:
                target = pairs[0]
                st.subheader(f"Analyzing: {target['baseToken']['name']} ({target['baseToken']['symbol']})")
                
                # Disini kita mengambil data 'txns' dari API response DexScreener
                # Note: API public hanya memberikan count, bukan list detail per trade
                # Jadi kita simulasikan visualisasi akumulasi
                
                c1, c2 = st.columns(2)
                c1.metric("Buys (24h)", target['txns']['h24']['buys'])
                c2.metric("Sells (24h)", target['txns']['h24']['sells'])
                
                buys = target['txns']['h24']['buys']
                sells = target['txns']['h24']['sells']
                
                # Mock Dataframes for visual
                data = {
                    'Type': ['buy']*buys + ['sell']*sells,
                    'Value (USD)': [random.randint(100, 5000) for _ in range(buys + sells)],
                    'Label': ['Trade'] * (buys + sells)
                }
                import random
                df_trades = pd.DataFrame(data)
                
                st.subheader("Buy vs Sell Pressure")
                st.plotly_chart(charts.render_volume_treemap(df_trades), use_container_width=True)
                
            else:
                st.error("Token not found")

    # --- 4. TOKEN EXPLORER ---
    elif page == "Token Explorer":
        st.title("🔎 Token Explorer (Top 10k)")
        
        # Mengambil data 'Trending' dari logika API kita
        trending_tokens = DexScreenerClient.get_top_boosted()
        
        if trending_tokens:
            display_data = []
            for t in trending_tokens:
                display_data.append({
                    "Name": t['baseToken']['name'],
                    "Symbol": t['baseToken']['symbol'],
                    "Price": f"${float(t['priceUsd']):.4f}",
                    "Liquidity": f"${t['liquidity']['usd']:,.0f}",
                    "FDV": f"${t.get('fdv', 0):,.0f}"
                })
            
            st.table(pd.DataFrame(display_data))
        else:
            st.info("Loading market data...")

    # --- 5. WALLET ANALYZER ---
    elif page == "Wallet Analyzer":
        st.title("🕵️ Wallet Profiler")
        
        wallet_addr = st.text_input("Enter Wallet Address", placeholder="0x...")
        
        if wallet_addr:
            st.info("Fetching on-chain data...")
            time.sleep(1) # Efek loading
            
            # Layout Hasil Analisis
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Balance", "$1,240,500")
            c2.metric("Unrealized PnL", "+$450,000", delta_color="normal")
            c3.metric("Win Rate", "78%")
            
            st.markdown("### 🏷️ Labels Detected")
            st.markdown("""
            <span style='background-color:#2a2; padding:5px; border-radius:5px;'>Whale</span>
            <span style='background-color:#22a; padding:5px; border-radius:5px;'>Diamond Hand</span>
            <span style='background-color:#a2a; padding:5px; border-radius:5px;'>Early Adopter</span>
            """, unsafe_allow_html=True)
            
            st.markdown("### Recent Activities")
            st.table(pd.DataFrame({
                "Token": ["PEPE", "SOL", "USDC"],
                "Action": ["BUY", "SELL", "TRANSFER"],
                "Value": ["$50,000", "$12,000", "$500"],
                "Time": ["5m ago", "1h ago", "1d ago"]
            }))

if __name__ == "__main__":
    main()
