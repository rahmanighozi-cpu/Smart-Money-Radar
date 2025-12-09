import streamlit as st
import time

def check_for_alerts(token_data):
    """Logic sederhana untuk memicu notifikasi"""
    # Jika volume 24 jam naik drastis
    if token_data:
        change = float(token_data.get('priceChange', {}).get('h24', 0))
        if change > 10:
            st.toast(f"🚨 ALERT: {token_data['baseToken']['symbol']} Pumped {change}% in 24h!", icon="🚀")
        
        # Simulate whale buy alert random (demo purpose)
        if int(time.time()) % 20 == 0:
            st.toast(f"🐋 WHALE DETECTED: Buying $50k of {token_data['baseToken']['symbol']}", icon="💸")
