import pandas as pd
import numpy as np
from typing import Tuple
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('technical_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def calculate_rsi(data: pd.DataFrame, window: int = 14) -> pd.Series:
    """Calculate Relative Strength Index (RSI)"""
    logger.info(f"Calculating RSI with window {window}")
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(data: pd.DataFrame, short_window: int = 12, long_window: int = 26, signal_window: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """Calculate Moving Average Convergence Divergence (MACD)"""
    logger.info(f"Calculating MACD with short_window {short_window}, long_window {long_window}, signal_window {signal_window}")
    short_ema = data['Close'].ewm(span=short_window, adjust=False).mean()
    long_ema = data['Close'].ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    histogram = macd - signal
    return macd, signal, histogram

def calculate_bollinger_bands(data: pd.DataFrame, window: int = 20, num_std_dev: int = 2) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """Calculate Bollinger Bands"""
    logger.info(f"Calculating Bollinger Bands with window {window}, num_std_dev {num_std_dev}")
    middle_band = data['Close'].rolling(window=window).mean()
    std_dev = data['Close'].rolling(window=window).std()
    upper_band = middle_band + (std_dev * num_std_dev)
    lower_band = middle_band - (std_dev * num_std_dev)
    return upper_band, middle_band, lower_band

def calculate_obv(data: pd.DataFrame) -> pd.Series:
    """Calculate On-Balance Volume (OBV) using vectorized operations"""
    logger.info("Calculating OBV")
    # Convert numpy array to pandas Series to use fillna and cumsum
    obv = pd.Series(np.sign(data['Close'].diff()), index=data.index).fillna(0) * data['Volume']
    obv = obv.cumsum()
    obv.iloc[0] = data['Volume'].iloc[0]
    return obv

def calculate_ad_line(data: pd.DataFrame) -> pd.Series:
    """Calculate Accumulation/Distribution Line (A/D Line)"""
    logger.info("Calculating A/D Line")
    high_low_diff = data['High'] - data['Low']
    clv = np.where(high_low_diff == 0, 0, ((data['Close'] - data['Low']) - (data['High'] - data['Close'])) / high_low_diff)
    clv = pd.Series(clv, index=data.index)
    ad_line = (clv * data['Volume']).cumsum()
    return ad_line

def calculate_atr(data: pd.DataFrame, window: int = 14) -> pd.Series:
    """Calculate Average True Range (ATR)"""
    logger.info(f"Calculating ATR with window {window}")
    high_low = data['High'] - data['Low']
    high_prev_close = np.abs(data['High'] - data['Close'].shift())
    low_prev_close = np.abs(data['Low'] - data['Close'].shift())
    tr = pd.DataFrame({'HL': high_low, 'HPC': high_prev_close, 'LPC': low_prev_close}).max(axis=1)
    atr = tr.ewm(span=window, adjust=False).mean()
    return atr



def perform_technical_analysis(df: pd.DataFrame, rsi_window: int = 14, macd_short_window: int = 12, macd_long_window: int = 26, macd_signal_window: int = 9, bb_window: int = 20, bb_num_std_dev: int = 2, atr_window: int = 14) -> pd.DataFrame:
    """
    Performs technical analysis on the given DataFrame.
    Adds technical indicators as new columns to the DataFrame.
    Returns the DataFrame with technical indicators.
    """
    if df.empty:
        logger.warning("No data for technical analysis.")
        print("No data for technical analysis.")
        return pd.DataFrame()

    logger.info("Starting technical analysis...")
    print("Performing technical analysis...")

    # Calculate RSI
    df['RSI'] = calculate_rsi(df, window=rsi_window)

    # Calculate MACD
    df['MACD'], df['MACD_Signal'], df['MACD_Hist'] = calculate_macd(df, short_window=macd_short_window, long_window=macd_long_window, signal_window=macd_signal_window)

    # Calculate Bollinger Bands
    df['BB_Upper'], df['BB_Middle'], df['BB_Lower'] = calculate_bollinger_bands(df, window=bb_window, num_std_dev=bb_num_std_dev)

    # Calculate OBV
    df['OBV'] = calculate_obv(df)

    # Calculate A/D Line
    df['AD_Line'] = calculate_ad_line(df)

    # Calculate ATR
    df['ATR'] = calculate_atr(df, window=atr_window)

    logger.info("Technical analysis complete.")
    print("Technical analysis complete.")
    return df

if __name__ == "__main__":
    # Example usage with dummy data
    from datetime import datetime, timedelta
    import numpy as np

    dates = pd.date_range(start=datetime.now() - timedelta(days=100), end=datetime.now(), freq='D')
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

    analyzed_df = perform_technical_analysis(dummy_df.copy())
    print("\nSample of technically analyzed data:")
    print(analyzed_df.tail())
