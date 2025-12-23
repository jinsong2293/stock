import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from stock_analyzer.modules.backtesting import Backtester, TradingStrategy
from stock_analyzer.modules.technical_analysis import perform_technical_analysis, calculate_rsi

# Define a more sophisticated strategy for backtesting
class AdvancedRsiMacdStrategy(TradingStrategy):
    def __init__(self, rsi_window=14, rsi_oversold=30, rsi_overbought=70,
                 macd_short_window=12, macd_long_window=26, macd_signal_window=9):
        self.rsi_window = rsi_window
        self.rsi_oversold = rsi_oversold
        self.rsi_overbought = rsi_overbought
        self.macd_short_window = macd_short_window
        self.macd_long_window = macd_long_window
        self.macd_signal_window = macd_signal_window

    def generate_signal(self, current_data):
        if len(current_data) < max(self.rsi_window, self.macd_long_window, self.macd_signal_window):
            return "Hold"
        
        # Perform technical analysis on the current data slice
        analyzed_data = perform_technical_analysis(
            current_data.copy(),
            rsi_window=self.rsi_window,
            macd_short_window=self.macd_short_window,
            macd_long_window=self.macd_long_window,
            macd_signal_window=self.macd_signal_window
        )
        
        last_rsi = analyzed_data['RSI'].iloc[-1]
        last_macd = analyzed_data['MACD'].iloc[-1]
        last_macd_signal = analyzed_data['MACD_Signal'].iloc[-1]
        
        # Simplified Buy signal: RSI oversold
        if last_rsi < self.rsi_oversold:
            return "Buy"
        # Simplified Sell signal: RSI overbought
        elif last_rsi > self.rsi_overbought:
            return "Sell"
        else:
            return "Hold"

def run_backtesting_test():
    print("Starting backtesting test...")

    # 1. Prepare dummy historical data (replace with real data from data_loader later)
    dates = pd.date_range(start=datetime.now() - timedelta(days=500), end=datetime.now(), freq='D')
    
    # Generate dummy prices with more pronounced trends and volatility
    np.random.seed(42) # for reproducibility
    base_prices = 100 + np.cumsum(np.random.randn(len(dates))) # Random walk
    
    # Add a long-term trend
    long_term_trend = np.linspace(-20, 20, len(dates))
    
    # Add some sinusoidal volatility
    seasonal_volatility = 10 * np.sin(np.linspace(0, 3 * np.pi, len(dates)))
    
    # Generate dummy prices with more pronounced trends and volatility
    # Increased random noise and added more distinct up/down trends
    dummy_prices = base_prices + long_term_trend + seasonal_volatility + np.random.randn(len(dates)) * 30 # Increased random noise
    
    # Introduce more frequent and sharper drops and rises to trigger RSI extremes
    for _ in range(10): # Increased number of random sharp events
        start_idx = np.random.randint(50, len(dates) - 50)
        end_idx = start_idx + np.random.randint(10, 40) # Increased duration of events
        
        if np.random.rand() > 0.5: # Upward spike
            dummy_prices[start_idx:end_idx] += np.linspace(0, 100, end_idx - start_idx) # Increased magnitude
        else: # Downward crash
            dummy_prices[start_idx:end_idx] -= np.linspace(0, 100, end_idx - start_idx) # Increased magnitude
    dummy_volume = np.random.randint(100000, 5000000, len(dates))

    dummy_df = pd.DataFrame({
        'Date': dates,
        'Open': dummy_prices - np.random.rand(len(dates)) * 2,
        'High': dummy_prices + np.random.rand(len(dates)) * 2,
        'Low': dummy_prices - np.random.rand(len(dates)) * 3,
        'Close': dummy_prices,
        'Volume': dummy_volume
    })
    dummy_df.set_index('Date', inplace=True)

    # 2. Define a strategy with customizable parameters
    # You can experiment with different parameters here
    strategy = AdvancedRsiMacdStrategy(
        rsi_window=14, rsi_oversold=30, rsi_overbought=70, # Reverted to original thresholds
        macd_short_window=12, macd_long_window=26, macd_signal_window=9
    )

    # 3. Initialize and run the backtester with commission and slippage
    # Experiment with different commission_rate and slippage_rate values
    commission_rate = 0.0015 # 0.15%
    slippage_rate = 0.0005   # 0.05%
    initial_capital = 100000

    backtester = Backtester(
        strategy, 
        dummy_df, 
        initial_capital=initial_capital,
        commission_rate=commission_rate,
        slippage_rate=slippage_rate
    )
    backtester.run_backtest()

    # 4. Get and print performance metrics
    metrics = backtester.get_performance_metrics()
    print("\nBacktest Performance Metrics:")
    for key, value in metrics.items():
        print(f"- {key.replace('_', ' ').title()}: {value}")

    # 5. Plot results (optional, uncomment to show plot)
    # backtester.plot_results()

if __name__ == "__main__":
    run_backtesting_test()
