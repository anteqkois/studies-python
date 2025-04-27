import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- KONFIGURACJA ---
BINANCE_URL = "https://api.binance.com/api/v3/klines"

# --- FUNKCJE POMOCNICZE ---
def get_binance_klines(symbol, interval, limit=500):
    url = f"{BINANCE_URL}?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    
    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
    df['SMA_20'] = df['close'].rolling(window=20).mean()
    return df

# --- APLIKACJA STREAMLIT ---
# Szerokie okno na start oraz inne ustawienia
st.set_page_config(layout="wide", page_title="Wizualizacja ceny kryptowalut", page_icon="📈")

# Opcję do modyfikacji
symbol = st.sidebar.text_input("Symbol", value="BTCUSDT")
interval = st.sidebar.selectbox("Interwał", options=[
    "1m", "5m", "15m", "30m", "1h", "2h", "4h", "1d", "1w"
], index=4)

chart_type = st.sidebar.radio("Typ Wykresu", options=["Świece", "Linia"])
show_sma = st.sidebar.checkbox("Pokaż SMA 20", value=True)

# Ładowanie danych
with st.spinner("Ładowanie danych..."):
    df = get_binance_klines(symbol.upper(), interval)

# Wykres
fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.02,
    row_heights=[0.85, 0.15],
    subplot_titles=(f"Cena {symbol}", "Wolumen"),
)

if chart_type == "Linia":
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['close'], mode='lines', name='Cena zamknięcia'))
else:
    fig.add_trace(go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name='Świece'
    ))

if show_sma:
    fig.add_trace(go.Scatter(
        x=df['timestamp'], 
        y=df['SMA_20'], 
        mode='lines', 
        name='SMA 20',
        line=dict(color="orange")
    ))

fig.add_trace(go.Bar(
    x=df['timestamp'],
    y=df['volume'],
    name='Wolumen',
    marker_color='blue',
    opacity=0.5
), row=2, col=1)

fig.update_layout(
    title=f"Wykres {symbol} - {interval}",
    xaxis_title="Czas",
    yaxis_title="Cena",
    xaxis_rangeslider_visible=False
)

st.plotly_chart(fig, use_container_width=True)

if st.checkbox("Pokaż surowe dane"):
    st.dataframe(df)
