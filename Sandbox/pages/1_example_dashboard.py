import streamlit as st
from alpaca_trade_api.rest import 
# Set Page Config
st.set_page_config(page_title='Select Stocks for Analysis', 
                   page_icon=':bar_chart:',  
                   layout='wide', 
                   initial_sidebar_state='auto')

# Create the Alpaca API object

#Fetch list of stocks to choose from
def fetch_stock_list():
    # Get a list of the top 500 stocks by market cap from alpaca
    alpaca = tradeapi.REST(
        alpaca_api_key,
        alpaca_secret_key,
        api_version="v2")
    # Get a list of the active equity stocks
    tickers = alpaca.list_assets(status='active', asset_class='us_equity')
    return tickers

full_tickers = fetch_stock_list()
default_tickers = full_tickers[0:2]

#Display a multi select dropdown for the user to select the stocks they want to analyze
selected_tickers = st.multiselect('Select the stocks you want to analyze', 
                                  full_tickers, 
                                  default_tickers)

#Display the selected stocks
st.write('You selected:', selected_tickers)
