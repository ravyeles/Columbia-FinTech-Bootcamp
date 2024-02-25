from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import yfinance as yf
import alpaca_trade_api as tradeapi
import streamlit as st
import datetime

#Set Page Config
st.set_page_config(page_title='Stock Data', 
                   page_icon=':bar_chart:', 
                   layout='wide', 
                   initial_sidebar_state='auto')

#Fetch list of stocks to choose from
def fetch_stock_list():
    # Get a list of the top 500 stocks by market cap from alpaca
    alpaca = tradeapi.REST(
        alpaca_api_key,
        alpaca_secret_key,
        api_version="v2")
    # Get a list of the active equity stocks
    assets = alpaca.list_assets(status='active', asset_class='us_equity')
    return assets

# Fetch Stock Metrics
def fetch_stock_data(tickers, start_date, end_date):
    alpaca_api_key = 'PKURMS5ELMEHV4ZGBXTQ'
    alpaca_secret_key = 'NhYNWSU4szskB7qUMl2FXPqYoQZXwL50ahf54jds'
    timeframe = '1D'
    alpaca = tradeapi.REST(
        alpaca_api_key,
        alpaca_secret_key,
        api_version="v2")
    # Get current price data for tickers
    alpaca_df = alpaca.get_bars(
        tickers,
        timeframe,
        start = start_date,
        end = end_date
    ).df
    #Drop time from the index
    alpaca_df.index = alpaca_df.index.date
    #Rename the index to date
    alpaca_df.index.name = 'date'
    #Reorder the columns so that the order of columns is date, ticker, open, high, low, close, volume.
    alpaca_df = alpaca_df[['symbol', 'open', 'high', 'low', 'close', 'volume']]
    #calculate the daily returns
    alpaca_df['daily_return'] = alpaca_df['close'].pct_change()
    return(alpaca_df)


#set stock variables - provide a list of stock symbols to choose from. We will get the top 100 by market cap
full_tickers = fetch_stock_list()
default_tickers = full_tickers[0:2]

#set time variables - set default start date, end date, time horizon, and min and max start dates, end dates, and time horizons
default_start_date = datetime.date(2020, 1, 1)
default_end_date = datetime.date(2020, 12, 31)
default_time_horizon = datetime.timedelta(days=365)
min_date = datetime.date(2010, 1, 1)
max_date = datetime.date.today() - datetime.timedelta(days=1)
min_time_horizon = datetime.timedelta(days=1)
max_time_horizon = datetime.timedelta(days=365)

#set investment amount variables - set min max and default investment amounts
min_investment_amount = 100000.0
max_investment_amount = 1000000000.0
default_investment_amount = 1000000.0

#initialize main alpaca dataframe:
df = fetch_stock_data(full_tickers, min_date, max_date)

#Create the sidebar
st.sidebar.title('Portfolio Inputs')
st.sidebar.subheader('Select Stocks')
selected_stocks = st.sidebar.multiselect('Select stocks to display', 
                                         options=full_tickers,
                                         default=default_tickers)
st.sidebar.subheader('Select Date Range')
start_date = st.sidebar.date_input('Start Date', 
                                   value=default_start_date,
                                   min_value=min_date,
                                   max_value=max_date)
end_date = st.sidebar.date_input('End Date', 
                                 value=default_end_date,
                                 min_value=min_date,
                                 max_value=max_date)
investment_amount = st.sidebar.number_input('Enter the investment amount',
                                            value=default_investment_amount,
                                           min_value=min_investment_amount,
                                           max_value=max_investment_amount)

#Filter Dataframe based on user inputs:
df_selection = df.query(
    'date >= @start_date and date <= @end_date and symbol in @selected_stocks'
    )

#Set Page Details
st.title(':bar_chart: Portfolio Analyzer')
st.markdown("##")

#Top KPIs
avg_close = int(df_selection['close'].mean())
avg_volume =  int(df_selection['volume'].mean())
avg_return =  int(df_selection['daily_return'].mean())

#Create columns
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Average Close Price: ")
    st.subheader(f"USD: ${avg_close:,}")
with middle_column:
    st.subheader("Average Volume: ")
    st.subheader(f"{avg_volume:,}")
with right_column:
    st.subheader("Average Return: ")
    st.subheader(f"USD: ${avg_return:,}")
st.markdown("----")

#Returns by stock
st.subheader('Stock Returns')
stock_returns = df_selection.pivot_table(index='date', columns='symbol', values='daily_return')
stock_returns = stock_returns.cumsum()
st.line_chart(stock_returns)

#Display the stock data
#st.dataframe(df_selection)