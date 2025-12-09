import streamlit as st

def sidebar_nav():
    with st.sidebar:
        st.markdown("## 🐋 WhaleRadar")
        st.caption("Advanced Smart Money Tracker")
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["Dashboard Overview", "Smart Money Leaderboard", "Whale Accumulation", "Token Explorer", "Wallet Analyzer"],
            index=0
        )
        
        st.markdown("---")
        st.info("Status: 🟢 System Operational")
        st.markdown("Updates: Real-time (10s)")
        
        return page
