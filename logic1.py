```python
#logic.py

import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime, timedelta

# Data Collection
def get_data(ticker, start_date, end_date):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&start_date={start_date}&end_date={end_date}&apikey=YOUR_API_KEY"
    response = requests.get(url)
    data = json.loads(response.text)
    return data

# Preprocessing
def preprocess_data(data):
    df = pd.DataFrame(data['Time Series (Daily)']).transpose()
    df.index = pd.to_datetime(df.index)
    df = df.dropna()
    df['Close'] = df['Close'].astype(float)
    return df

# Trading Strategy
def moving_average_strategy(df, short_window, long_window):
    df['Short_MA'] = df['Close'].rolling(short_window).mean()
    df['Long_MA'] = df['Close'].rolling(long_window).mean()
    df['Signal'] = np.where(df['Short_MA'] > df['Long_MA'], 1, -1)
    return df

# Backtesting
def backtest_strategy(df, initial_balance):
    df['Returns'] = df['Close'].pct_change()
    df['Position'] = df['Signal'].shift(1)
    df['Profit'] = df['Position'] * df['Returns']
    
    portfolio = pd.DataFrame()
    portfolio['Cumulative Returns'] = (1 + df['Profit']).cumprod()
    return portfolio

# Main Function
def main():
    start_date = (datetime.now() - timedelta(days=365*5)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    tickers = ['SPY', 'AAPL', 'MSFT']
    results = {}
    
    for ticker in tickers:
        data = get_data(ticker, start_date, end_date)
        df = preprocess_data(data)
        if not df.empty:
            strategy_df = moving_average_strategy(df, 20, 50)
            portfolio = backtest_strategy(strategy_df, 100000)
            results[ticker] = portfolio
    
    # Calculate overall performance
    overall_portfolio = pd.DataFrame()
    overall_portfolio['Cumulative Returns'] = results['SPY']['Cumulative Returns']
    return overall_portfolio

if __name__ == "__main__":
    main()
```