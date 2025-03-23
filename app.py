import altair as alt
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
from streamlit_searchbox import st_searchbox

# ----------------------------------------------------------------------------------------------- #

@st.cache_data
def fetch_stock_info(symbol):
    stock = yf.Ticker(symbol)
    return stock.info

@st.cache_data
def fetch_quartely_financials(symbol):
    stock = yf.Ticker(symbol)
    return stock.quartely_financials.T

@st.cache_data
def fetch_annual_financials(symbol):
    stock = yf.Ticker(symbol)
    return stock.financials.T

@st.cache_data
def fetch_weekly_price_history(symbol):
    stock = yf.Ticker(symbol)
    return stock.history(period='1y', interval='1wk')

# ----------------------------------------------------------------------------------------------- #

st.title('Stock Market Dashboard')

symbols = ['MSFT', 'GOOGL', 'AMZN', 'TSLA']
symbol = st.selectbox('Nome da ação:', symbols)

info = fetch_stock_info(symbol)

st.title(info["longName"])
st.subheader(f'Market Cap: $ {info["marketCap"]:,}')
st.subheader(f'Setor: {info["sector"]}')

# ----------------------------------------------------------------------------------------------- #

weekly_price_history = fetch_weekly_price_history(symbol)

st.header('Histórico de preço semanal')

weekly_price_history = weekly_price_history.rename_axis('Date').reset_index()
candle_stick_chart = go.Figure(
    data=[go.Candlestick(x=weekly_price_history['Date'],
    open=weekly_price_history['Open'],
    low=weekly_price_history['Low'],
    high=weekly_price_history['High'],
    close=weekly_price_history['Close'])]
)

st.plotly_chart(candle_stick_chart, use_container_width=True)
