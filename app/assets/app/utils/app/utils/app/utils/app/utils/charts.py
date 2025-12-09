import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def render_candle_chart(token_name, price_data):
    """
    Render chart sederhana. 
    Catatan: API DexScreener publik tidak memberikan OHLCV historical lengkap 
    tanpa endpoint berbayar tertentu, kita gunakan visualisasi price change simulasi 
    atau data yang ada.
    """
    # Mocking historical data for visual purpose if not available
    # In real app, fetch OHLCV from CoinGecko/GeckoTerminal
    
    fig = go.Figure()
    
    # Placeholder line chart karena keterbatasan API free historical
    fig.add_trace(go.Scatter(
        y=price_data, 
        mode='lines', 
        name='Price',
        line=dict(color='#00f2ea', width=2),
        fill='tozeroy',
        fillcolor='rgba(0, 242, 234, 0.1)'
    ))

    fig.update_layout(
        title=f"{token_name} Price Action",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    return fig

def render_volume_treemap(data):
    """Treemap untuk akumulasi"""
    if data.empty:
        return None
        
    fig = px.treemap(
        data, 
        path=['Label'], 
        values='Value (USD)',
        color='Type',
        color_discrete_map={'buy':'#00ff00', 'sell':'#ff0000'},
        title="Whale Transaction Distribution"
    )
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
    return fig
