import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Backtester:
    """
    A simple backtesting engine for evaluating trading strategies.
    """
    def __init__(self, strategy, historical_data, initial_capital=100000, commission_rate=0.0015, slippage_rate=0.0005):
        self.strategy = strategy
        self.historical_data = historical_data.copy()
        self.initial_capital = initial_capital
        self.commission_rate = commission_rate
        self.slippage_rate = slippage_rate
        
        self.capital = initial_capital
        self.holdings = 0
        self.portfolio_value = []
        self.trades = [] # List of dictionaries: {'date', 'type', 'price', 'shares', 'commission', 'slippage', 'pnl'}

    def _execute_trade(self, trade_signal, date, price):
        """Executes a trade based on the signal, accounting for commission and slippage."""
        if trade_signal == "Buy":
            # Calculate actual buy price with slippage
            actual_buy_price = price * (1 + self.slippage_rate)
            # Calculate maximum shares we can buy
            max_shares = int(self.capital / (actual_buy_price * (1 + self.commission_rate)))
            
            if max_shares >= 1:
                cost = max_shares * actual_buy_price
                commission = cost * self.commission_rate
                total_cost = cost + commission
                
                if self.capital >= total_cost:
                    self.capital -= total_cost
                    self.holdings += max_shares
                    self.trades.append({
                        'date': date,
                        'type': 'BUY',
                        'price': actual_buy_price,
                        'shares': max_shares,
                        'commission': commission,
                        'slippage': price * self.slippage_rate * max_shares,
                        'pnl': -total_cost # Negative PnL for cost
                    })
                    print(f"{date.strftime('%Y-%m-%d')}: BUY {max_shares:.0f} shares at {actual_buy_price:.2f} (Cost: {total_cost:.2f})")
                else:
                    print(f"{date.strftime('%Y-%m-%d')}: Not enough capital to BUY.")
            else:
                print(f"{date.strftime('%Y-%m-%d')}: Not enough capital to BUY a full share.")

        elif trade_signal == "Sell" and self.holdings > 0:
            # Calculate actual sell price with slippage
            actual_sell_price = price * (1 - self.slippage_rate)
            
            revenue = self.holdings * actual_sell_price
            commission = revenue * self.commission_rate
            total_revenue = revenue - commission
            
            # PnL calculation for sell trades is complex without tracking average cost basis.
            # For simplicity, we'll record the revenue from the sale.
            # The overall portfolio value will reflect the true PnL.
            pnl = total_revenue
            
            self.capital += total_revenue
            self.trades.append({
                'date': date,
                'type': 'SELL',
                'price': actual_sell_price,
                'shares': self.holdings,
                'commission': commission,
                'slippage': price * self.slippage_rate * self.holdings,
                'pnl': pnl
            })
            print(f"{date.strftime('%Y-%m-%d')}: SELL {self.holdings:.0f} shares at {actual_sell_price:.2f} (Revenue: {total_revenue:.2f}, PnL: {pnl:.2f})")
            self.holdings = 0
        elif trade_signal == "Sell" and self.holdings == 0:
            print(f"{date.strftime('%Y-%m-%d')}: No shares to SELL.")

    def run_backtest(self):
        """Runs the backtest simulation over the historical data."""
        print("\nStarting backtest...")
        for i, (date, row) in enumerate(self.historical_data.iterrows()):
            current_price = row['Close']
            
            # Get trade signal from the strategy
            trade_signal = self.strategy.generate_signal(self.historical_data.iloc[:i+1]) # Pass data up to current date
            
            self._execute_trade(trade_signal, date, current_price)
            
            # Record portfolio value
            current_portfolio_value = self.capital + (self.holdings * current_price)
            self.portfolio_value.append({'date': date, 'value': current_portfolio_value})
            
        print("Backtest complete.")
        
        # If still holding shares at the end, liquidate them
        if self.holdings > 0:
            last_date = self.historical_data.index[-1]
            last_price = self.historical_data['Close'].iloc[-1]
            self._execute_trade("Sell", last_date, last_price)
            self.portfolio_value[-1]['value'] = self.capital # Update final portfolio value after liquidation

    def get_performance_metrics(self):
        """Calculates and returns performance metrics."""
        if not self.portfolio_value:
            return {}

        portfolio_df = pd.DataFrame(self.portfolio_value).set_index('date')
        portfolio_df['returns'] = portfolio_df['value'].pct_change()
        
        total_return = (self.capital + (self.holdings * self.historical_data['Close'].iloc[-1] if self.holdings > 0 else 0)) / self.initial_capital - 1
        
        # Calculate drawdown
        peak = portfolio_df['value'].expanding(min_periods=1).max()
        drawdown = (portfolio_df['value'] / peak - 1)
        max_drawdown = drawdown.min()

        # Calculate Sharpe Ratio (requires risk-free rate, simplified here)
        # For a more accurate Sharpe, need daily returns and a risk-free rate
        daily_returns = portfolio_df['returns'].dropna()
        if not daily_returns.empty:
            sharpe_ratio = np.mean(daily_returns) / np.std(daily_returns) * np.sqrt(252) if np.std(daily_returns) != 0 else 0
        else:
            sharpe_ratio = 0

        return {
            "total_return": f"{total_return:.2%}",
            "final_capital": f"{self.capital + (self.holdings * self.historical_data['Close'].iloc[-1] if self.holdings > 0 else 0):.2f}",
            "max_drawdown": f"{max_drawdown:.2%}",
            "sharpe_ratio": f"{sharpe_ratio:.2f}",
            "num_trades": len([t for t in self.trades if t['type'] != 'HOLD'])
        }

    def plot_results(self):
        """Plots the portfolio value over time."""
        if not self.portfolio_value:
            print("No portfolio value data to plot.")
            return

        portfolio_df = pd.DataFrame(self.portfolio_value).set_index('date')
        
        plt.figure(figsize=(12, 6))
        plt.plot(portfolio_df.index, portfolio_df['value'], label='Portfolio Value')
        plt.title('Backtest Portfolio Value Over Time')
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value')
        plt.legend()
        plt.grid(True)
        plt.show()

class TradingStrategy:
    """
    Base class for a trading strategy.
    Users should inherit from this and implement the generate_signal method.
    """
    def generate_signal(self, current_data):
        """
        Generates a trading signal (Buy, Sell, Hold) based on the current data.
        This method should be overridden by specific strategies.
        
        Args:
            current_data (pd.DataFrame): Historical data up to the current point in time.
        
        Returns:
            str: "Buy", "Sell", or "Hold"
        """
        # Default: always hold
        return "Hold"

# Example of a simple strategy (e.g., RSI-based)
class RsiStrategy(TradingStrategy):
    def __init__(self, rsi_window=14, rsi_oversold=30, rsi_overbought=70):
        self.rsi_window = rsi_window
        self.rsi_oversold = rsi_oversold
        self.rsi_overbought = rsi_overbought

    def generate_signal(self, current_data):
        if len(current_data) < self.rsi_window:
            return "Hold"
        
        # Ensure technical analysis is performed on the data
        from stock_analyzer.modules.technical_analysis import calculate_rsi
        current_data['RSI'] = calculate_rsi(current_data.copy(), window=self.rsi_window)
        
        last_rsi = current_data['RSI'].iloc[-1]
        
        if last_rsi < self.rsi_oversold:
            return "Buy"
        elif last_rsi > self.rsi_overbought:
            return "Sell"
        else:
            return "Hold"

if __name__ == "__main__":
    # Example usage:
    # 1. Prepare dummy historical data
    from datetime import datetime, timedelta
    dates = pd.date_range(start=datetime.now() - timedelta(days=200), end=datetime.now(), freq='D')
    dummy_prices = 100 + np.cumsum(np.random.randn(len(dates)))
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

    # 2. Define a strategy
    rsi_strategy = RsiStrategy()

    # 3. Initialize and run the backtester
    backtester = Backtester(rsi_strategy, dummy_df, initial_capital=100000)
    backtester.run_backtest()

    # 4. Get and print performance metrics
    metrics = backtester.get_performance_metrics()
    print("\nBacktest Performance Metrics:")
    for key, value in metrics.items():
        print(f"- {key.replace('_', ' ').title()}: {value}")

    # 5. Plot results (optional)
    # backtester.plot_results() # This would open a matplotlib window
