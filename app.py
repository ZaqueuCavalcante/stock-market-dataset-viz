import altair as alt
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ----------------------------------------------------------------------------------------------- #

@st.cache_data
def fetch_stock_info(symbol):
    stock = yf.Ticker(symbol)
    return stock.info

@st.cache_data
def fetch_quartely_financials(symbol):
    stock = yf.Ticker(symbol)
    return stock.quarterly_financials.T

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

symbols = ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'NVDA', 'META', 'TSLA']

symbol = st.selectbox('Nome da ação:', symbols)

info = fetch_stock_info(symbol)

st.title(info['longName'])
st.subheader(f'Market Cap: $ {info['marketCap']:,}')
st.subheader(f'Setor: {info['sector']}')

# ----------------------------------------------------------------------------------------------- #

weekly_price_history = fetch_weekly_price_history(symbol)

st.header('Histórico de preço semanal')

st.markdown('Registro dos preços de uma ação ao longo de semanas, incluindo informações como:');
st.markdown(
    '''
    - **Preço de Abertura (Open Price)**: O preço da ação no início da semana.
    - **Preço de Fechamento (Close Price)**: O preço da ação no final da semana.
    - **Máxima da Semana (High Price)**: O maior preço alcançado pela ação durante a semana.
    - **Mínima da Semana (Low Price)**: O menor preço registrado na semana.
    - **Volume de Negociação (Trading Volume)**: A quantidade total de ações negociadas na semana.
    '''
);
st.markdown('Esse histórico é útil para análise técnica e fundamentalista, ajudando investidores a identificar tendências de mercado e tomar decisões de compra ou venda.');

weekly_price_history = weekly_price_history.rename_axis('Date').reset_index()

candlesticks = go.Candlestick(
    showlegend=False,
    x=weekly_price_history['Date'],
    open=weekly_price_history['Open'],
    low=weekly_price_history['Low'],
    high=weekly_price_history['High'],
    close=weekly_price_history['Close'])

volume_bars = go.Bar(
    showlegend=False,
    x=weekly_price_history['Date'],
    y=weekly_price_history['Volume'],
    marker={
        "color": "rgba(128,128,128,0.5)",
    }
)

fig = go.Figure(candlesticks)
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(candlesticks, secondary_y=True)
fig.add_trace(volume_bars, secondary_y=False)
fig.update_layout(
    title="Histórico de preço semanal",
    height=600,
)
fig.update_yaxes(title="Preço $", secondary_y=True, showgrid=True)
fig.update_yaxes(title="Volume $", secondary_y=False, showgrid=False)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------------------------------- #

st.header('Faturamento')

st.markdown('**Total Revenue (Receita Total)**: É o valor bruto que uma empresa gera com suas operações, incluindo vendas de produtos e serviços. Ele não considera nenhum custo ou despesa, apenas a receita gerada antes de qualquer dedução.')
st.markdown('**Net Income (Lucro Líquido)**: É o que sobra depois que a empresa deduz todas as suas despesas da receita total, incluindo custos operacionais, impostos, juros e outras despesas. Representa o lucro real que a empresa teve em um determinado período e é um indicador-chave da sua rentabilidade.')

quartely_financials = fetch_quartely_financials(symbol)
anual_financials = fetch_annual_financials(symbol)

period = st.segmented_control(label='Período', options=['Trimestral', 'Anual'], default='Trimestral')

if (period == 'Trimestral'):
    quartely_financials = quartely_financials.rename_axis('Quarter').reset_index()
    quartely_financials['Quarter'] = quartely_financials['Quarter'].astype(str)
    revenue_chart = alt.Chart(quartely_financials).mark_bar().encode(
        x='Quarter:O',
        y='Total Revenue'
    )
    st.altair_chart(revenue_chart, use_container_width=True)
    net_income_chart = alt.Chart(quartely_financials).mark_bar(color='green').encode(
        x='Quarter:O',
        y='Net Income'
    )
    st.altair_chart(net_income_chart, use_container_width=True)

if (period == 'Anual'):
    anual_financials = anual_financials.rename_axis('Year').reset_index()
    anual_financials['Year'] = anual_financials['Year'].astype(str).transform(lambda year: year.split('-')[0])
    revenue_chart = alt.Chart(anual_financials).mark_bar().encode(
        x='Year:O',
        y='Total Revenue'
    )
    st.altair_chart(revenue_chart, use_container_width=True)
    net_income_chart = alt.Chart(anual_financials).mark_bar(color='green').encode(
        x='Year:O',
        y='Net Income'
    )
    st.altair_chart(net_income_chart, use_container_width=True)
