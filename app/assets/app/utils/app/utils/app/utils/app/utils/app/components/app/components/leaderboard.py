import streamlit as st

def render_leaderboard(df):
    st.markdown("### 🏆 Smart Money Leaderboard")
    st.dataframe(
        df,
        column_config={
            "Win Rate": st.column_config.ProgressColumn(
                "Win Rate",
                format="%s",
                min_value=0,
                max_value=100,
            ),
            "Status": st.column_config.TextColumn("Status")
        },
        use_container_width=True,
        hide_index=True
    )
