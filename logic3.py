```python
#logic.py

import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import websockets
import asyncio

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
def moving_average_strategy(df, short_window, long_window, threshold):
    df['Short_MA'] = df['Close'].rolling(short_window).mean()
    df['Long_MA'] = df['Close'].rolling(long_window).mean()
    df['Signal'] = np.where((df['Short_MA'] > df['Long_MA']) & (df['Short_MA'] - df['Long_MA'] > threshold), 1, -1)
    return df

def machine_learning_strategy(df):
    # Feature engineering
    df['SMA_20'] = df['Close'].rolling(20).mean()
    df['SMA_50'] = df['Close'].rolling(50).mean()
    df['RSI'] = (df['Close'].diff().rolling(14).mean() / df['Close'].diff().abs().rolling(14).mean()) * 100
    df['Volume'] = df['Volume'].astype(float)
    
    # Prepare features and labels
    features = df[['SMA_20', 'SMA_50', 'RSI', 'Volume']]
    labels = df['Close'].pct_change().shift(-1).fillna(0)
    
    # Split data
    train_data = features.iloc[:-100]
    test_data = features.iloc[-100:]
    train_labels = labels.iloc[:-100]
    test_labels = labels.iloc[-100:]
    
    # Train model
    model = RandomForestClassifier()
    model.fit(train_data, train_labels)
    
    # Predict
    predictions = model.predict(test_data)
    
    # Generate signals
    df['ML_Signal'] = np.where(predictions > 0.5, 1, -1)
    return df

# Risk Management
def risk_management(portfolio, initial_balance, risk_tolerance):
    portfolio['Position Size'] = (initial_balance * risk_tolerance) / abs(portfolio['Close'].iloc[-1] - portfolio['Close'].iloc[-2])
    return portfolio

# Backtesting
def backtest_strategy(df, initial_balance):
    df['Returns'] = df['Close'].pct_change()
    df['Position'] = df['ML_Signal'].shift(1)
    df['Profit'] = df['Position'] * df['Returns']
    
    portfolio = pd.DataFrame()
    portfolio['Cumulative Returns'] = (1 + df['Profit']).cumprod()
    portfolio['Drawdown'] = (1 - portfolio['Cumulative Returns'].cummax()).cummin()
    
    plt.figure(figsize=(10,6))
    plt.plot(portfolio['Cumulative Returns'])
    plt.title('Cumulative Returns')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.show()
    
    return portfolio

# Real-Time Trading
async def real_time_trading():
    # Connect to WebSocket
    async with websockets.connect("wss://api.example.com/socket") as websocket:
        try:
            while True:
                # Receive real-time data
                data = await websocket.recv()
                data = json.loads(data)
                
                # Process data
                df = pd.DataFrame([data])
                df = preprocess_data(df)
                
                # Generate signal
                strategy_df = moving_average_strategy(df, 15, 40, 0.02)
                ml_strategy_df = machine_learning_strategy(df)
                
                # Execute trade
                if strategy_df['Signal'].iloc[-1] == 1 and ml_strategy_df['ML_Signal'].iloc[-1] == 1:
                    # Buy signal
                    print("Buy signal received")
                elif strategy_df['Signal'].iloc[-1] == -1 and ml_strategy_df['ML_Signal'].iloc[-1] == -1:
                    # Sell signal
                    print("Sell signal received")
                
                await asyncio.sleep(1)
        except:
            print("Connection closed")

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
            strategy_df = moving_average_strategy(df, 15, 40, 0.02)
            ml_strategy_df = machine_learning_strategy(df)
            portfolio = backtest_strategy(strategy_df, 100000)
            results[ticker] = portfolio
    
    # Calculate overall performance
    overall_portfolio = pd.DataFrame()
    overall_portfolio['Cumulative Returns'] = results['SPY']['Cumulative Returns']
    return overall_portfolio

if __name__ == "__main__":
    asyncio.run(real_time_trading())
    main()
```