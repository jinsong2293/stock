"""
Enhanced Data Loader Module
Advanced Multi-source Data Integration with Real-time Processing Capabilities
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Tuple, Optional, Dict, List, Any
import yfinance as yf
from vnstock import Vnstock
import requests
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from dataclasses import dataclass
import time
from stock_analyzer.modules.data_validation import validate_and_clean_data

logger = logging.getLogger(__name__)

@dataclass
class DataSourceConfig:
    """Configuration for different data sources"""
    name: str
    priority: int
    enabled: bool = True
    rate_limit: float = 1.0  # seconds between requests
    timeout: int = 30
    max_retries: int = 3

class EnhancedDataLoader:
    """
    Enhanced Data Loader with multi-source integration and real-time capabilities
    """
    
    def __init__(self):
        self.data_sources = {
            'yfinance': DataSourceConfig('yfinance', priority=1, rate_limit=0.5),
            'vnstock': DataSourceConfig('vnstock', priority=2, rate_limit=1.0),
            'alpha_vantage': DataSourceConfig('alpha_vantage', priority=3, rate_limit=12.0),
            'polygon': DataSourceConfig('polygon', priority=4, rate_limit=1.0)
        }
        self.cache = {}
        self.last_request_time = {}
        
    async def fetch_real_time_data(self, tickers: List[str]) -> Dict[str, Any]:
        """
        Fetch real-time data for multiple tickers concurrently
        """
        async with aiohttp.ClientSession() as session:
            tasks = []
            for ticker in tickers:
                task = self._fetch_single_realtime(session, ticker)
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return dict(zip(tickers, results))
    
    async def _fetch_single_realtime(self, session: aiohttp.ClientSession, ticker: str) -> Dict[str, Any]:
        """
        Fetch real-time data for a single ticker
        """
        try:
            # Using Yahoo Finance API for real-time data
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_realtime_data(data, ticker)
                else:
                    logger.warning(f"Failed to fetch real-time data for {ticker}: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Error fetching real-time data for {ticker}: {str(e)}")
            return None
    
    def _parse_realtime_data(self, data: Dict[str, Any], ticker: str) -> Dict[str, Any]:
        """
        Parse real-time data from Yahoo Finance API
        """
        try:
            result = data['chart']['result'][0]
            meta = result['meta']
            
            return {
                'ticker': ticker,
                'current_price': meta.get('regularMarketPrice'),
                'previous_close': meta.get('previousClose'),
                'open': meta.get('regularMarketOpen'),
                'day_high': meta.get('regularMarketDayHigh'),
                'day_low': meta.get('regularMarketDayLow'),
                'volume': meta.get('regularMarketVolume'),
                'market_cap': meta.get('marketCap'),
                'timestamp': datetime.now(),
                'source': 'yfinance_realtime'
            }
        except Exception as e:
            logger.error(f"Error parsing real-time data for {ticker}: {str(e)}")
            return None
    
    def fetch_historical_data_enhanced(self, ticker: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """
        Enhanced historical data fetching with multiple sources and fallback
        """
        logger.info(f"Fetching enhanced historical data for {ticker}")
        
        # Check cache first
        cache_key = f"{ticker}_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}"
        if cache_key in self.cache:
            logger.info(f"Using cached data for {ticker}")
            return self.cache[cache_key]
        
        # Try multiple data sources in order of priority
        for source_name in sorted(self.data_sources.keys(), key=lambda x: self.data_sources[x].priority):
            source = self.data_sources[source_name]
            if not source.enabled:
                continue
                
            try:
                logger.info(f"Trying {source_name} for {ticker}")
                df = self._fetch_from_source(source_name, ticker, start_date, end_date)
                
                if not df.empty and len(df) > 0:
                    logger.info(f"Successfully fetched {len(df)} data points from {source_name}")
                    
                    # Cache the result
                    self.cache[cache_key] = df
                    
                    # Add metadata
                    df.attrs['data_source'] = source_name
                    df.attrs['fetch_time'] = datetime.now()
                    df.attrs['ticker'] = ticker
                    
                    return df
                    
            except Exception as e:
                logger.warning(f"Failed to fetch from {source_name}: {str(e)}")
                continue
        
        logger.error(f"All data sources failed for {ticker}")
        return pd.DataFrame()
    
    def _fetch_from_source(self, source_name: str, ticker: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """
        Fetch data from a specific source
        """
        if source_name == 'yfinance':
            return self._fetch_yfinance_data(ticker, start_date, end_date)
        elif source_name == 'vnstock':
            return self._fetch_vnstock_data(ticker, start_date, end_date)
        elif source_name == 'alpha_vantage':
            return self._fetch_alpha_vantage_data(ticker, start_date, end_date)
        elif source_name == 'polygon':
            return self._fetch_polygon_data(ticker, start_date, end_date)
        else:
            raise ValueError(f"Unknown data source: {source_name}")
    
    def _fetch_yfinance_data(self, ticker: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """
        Enhanced Yahoo Finance data fetching with multiple ticker formats
        """
        suffixes = ['.VN', '.HN', '.HM', '.HA', '']
        
        for suffix in suffixes:
            try:
                yf_ticker = f"{ticker}{suffix}"
                logger.info(f"Trying Yahoo Finance with ticker: {yf_ticker}")
                
                df = yf.download(
                    yf_ticker, 
                    start=start_date, 
                    end=end_date, 
                    progress=False, 
                    auto_adjust=True,
                    timeout=30
                )
                
                if not df.empty and len(df) > 0:
                    # Handle multi-index columns if present
                    if isinstance(df.columns, pd.MultiIndex):
                        df.columns = [col[0] for col in df.columns]
                    
                    required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
                    if all(col in df.columns for col in required_cols):
                        return df[required_cols]
                        
            except Exception as e:
                logger.warning(f"Yahoo Finance failed for {yf_ticker}: {str(e)}")
                continue
        
        return pd.DataFrame()
    
    def _fetch_vnstock_data(self, ticker: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """
        Enhanced VNStock data fetching
        """
        try:
            logger.info(f"Fetching from VNStock for {ticker}")
            
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')
            
            vnstock_instance = Vnstock()
            stock_component = vnstock_instance.stock(symbol=ticker)
            df_vnstock = stock_component.quote.history(start_date_str, end_date_str)
            
            if not df_vnstock.empty:
                # Rename columns to standard format
                column_mapping = {
                    'Mở cửa': 'Open',
                    'Cao nhất': 'High',
                    'Thấp nhất': 'Low',
                    'Đóng cửa': 'Close',
                    'Khối lượng': 'Volume'
                }
                
                df_vnstock.rename(columns=column_mapping, inplace=True)
                
                # Handle date column
                if 'Ngày' in df_vnstock.columns:
                    df_vnstock['Date'] = pd.to_datetime(df_vnstock['Ngày'])
                    df_vnstock = df_vnstock.set_index('Date')
                    df_vnstock.drop(columns=['Ngày'], inplace=True)
                
                required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
                return df_vnstock[required_cols]
                
        except Exception as e:
            logger.warning(f"VNStock failed for {ticker}: {str(e)}")
        
        return pd.DataFrame()
    
    def _fetch_alpha_vantage_data(self, ticker: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """
        Alpha Vantage data fetching (requires API key)
        """
        try:
            # This would require an Alpha Vantage API key
            # For now, return empty DataFrame as placeholder
            logger.info(f"Alpha Vantage not configured for {ticker}")
            return pd.DataFrame()
        except Exception as e:
            logger.warning(f"Alpha Vantage failed for {ticker}: {str(e)}")
            return pd.DataFrame()
    
    def _fetch_polygon_data(self, ticker: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """
        Polygon.io data fetching (requires API key)
        """
        try:
            # This would require a Polygon.io API key
            # For now, return empty DataFrame as placeholder
            logger.info(f"Polygon not configured for {ticker}")
            return pd.DataFrame()
        except Exception as e:
            logger.warning(f"Polygon failed for {ticker}: {str(e)}")
        return pd.DataFrame()
    
    def fetch_market_overview(self) -> Dict[str, Any]:
        """
        Fetch overall market data and indices
        """
        try:
            # Fetch major indices
            indices = {
                '^GSPC': 'S&P 500',
                '^DJI': 'Dow Jones',
                '^IXIC': 'NASDAQ',
                '^VIX': 'VIX',
                '^TNX': '10Y Treasury'
            }
            
            market_data = {}
            
            for symbol, name in indices.items():
                try:
                    ticker = yf.Ticker(symbol)
                    info = ticker.info
                    hist = ticker.history(period="2d")
                    
                    if not hist.empty:
                        current_price = hist['Close'].iloc[-1]
                        previous_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
                        change = current_price - previous_close
                        change_pct = (change / previous_close) * 100 if previous_close != 0 else 0
                        
                        market_data[symbol] = {
                            'name': name,
                            'price': current_price,
                            'change': change,
                            'change_pct': change_pct,
                            'volume': hist['Volume'].iloc[-1] if 'Volume' in hist.columns else None
                        }
                        
                except Exception as e:
                    logger.warning(f"Failed to fetch data for {symbol}: {str(e)}")
                    continue
            
            return market_data
            
        except Exception as e:
            logger.error(f"Error fetching market overview: {str(e)}")
            return {}
    
    def batch_fetch_data(self, tickers: List[str], start_date: datetime, end_date: datetime) -> Dict[str, pd.DataFrame]:
        """
        Fetch data for multiple tickers in parallel
        """
        logger.info(f"Batch fetching data for {len(tickers)} tickers")
        
        results = {}
        
        # Use ThreadPoolExecutor for concurrent processing
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_ticker = {
                executor.submit(self.fetch_historical_data_enhanced, ticker, start_date, end_date): ticker 
                for ticker in tickers
            }
            
            for future in as_completed(future_to_ticker):
                ticker = future_to_ticker[future]
                try:
                    df = future.result()
                    if not df.empty:
                        results[ticker] = df
                        logger.info(f"Successfully fetched data for {ticker}")
                    else:
                        logger.warning(f"No data available for {ticker}")
                except Exception as e:
                    logger.error(f"Error fetching data for {ticker}: {str(e)}")
        
        return results
    
    def get_data_quality_report(self, df: pd.DataFrame, ticker: str) -> Dict[str, Any]:
        """
        Generate comprehensive data quality report
        """
        if df.empty:
            return {"error": "No data available for quality assessment"}
        
        report = {
            'ticker': ticker,
            'total_records': len(df),
            'date_range': {
                'start': df.index.min().strftime('%Y-%m-%d') if hasattr(df.index, 'min') else 'N/A',
                'end': df.index.max().strftime('%Y-%m-%d') if hasattr(df.index, 'max') else 'N/A'
            },
            'missing_values': {},
            'data_types': {},
            'statistical_summary': {},
            'data_source': df.attrs.get('data_source', 'unknown'),
            'fetch_time': df.attrs.get('fetch_time', 'N/A')
        }
        
        # Missing values analysis
        for col in df.columns:
            missing_count = df[col].isnull().sum()
            missing_pct = (missing_count / len(df)) * 100
            report['missing_values'][col] = {
                'count': int(missing_count),
                'percentage': round(missing_pct, 2)
            }
        
        # Data types
        for col in df.columns:
            report['data_types'][col] = str(df[col].dtype)
        
        # Statistical summary for numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            report['statistical_summary'][col] = {
                'mean': round(df[col].mean(), 4),
                'std': round(df[col].std(), 4),
                'min': round(df[col].min(), 4),
                'max': round(df[col].max(), 4),
                'median': round(df[col].median(), 4)
            }
        
        # Data quality score
        total_cells = len(df) * len(df.columns)
        total_missing = df.isnull().sum().sum()
        quality_score = ((total_cells - total_missing) / total_cells) * 100 if total_cells > 0 else 0
        report['overall_quality_score'] = round(quality_score, 2)
        
        return report

# Global instance
enhanced_data_loader = EnhancedDataLoader()

# Backward compatibility functions
def fetch_historical_data(ticker: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """
    Backward compatible function for historical data fetching
    """
    return enhanced_data_loader.fetch_historical_data_enhanced(ticker, start_date, end_date)

def preprocess_data(df: pd.DataFrame, symbol: str = "UNKNOWN") -> pd.DataFrame:
    """
    Enhanced preprocessing with additional feature engineering
    """
    if df.empty:
        print("⚠️ Không có dữ liệu để tiền xử lý.")
        return df

    # Ensure column names are standardized
    df.rename(columns={
        'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume',
        'Open': 'Open', 'High': 'High', 'Low': 'Low', 'Close': 'Close', 'Volume': 'Volume'
    }, inplace=True)

    # Ensure required columns exist
    required_ohlcv_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    missing_columns = [col for col in required_ohlcv_columns if col not in df.columns]

    if missing_columns:
        print(f"❌ Các cột OHLCV bắt buộc bị thiếu: {missing_columns}")
        return pd.DataFrame()

    try:
        print(f"🔍 Bắt đầu validation và cleaning dữ liệu cho {symbol}...")
        
        # Apply comprehensive data validation and cleaning
        cleaned_df, validation_report, cleaning_log = validate_and_clean_data(df, symbol)
        
        # Add enhanced features
        enhanced_df = add_enhanced_features(cleaned_df)
        
        # Display validation results
        quality_score = validation_report['data_quality_score']
        print(f"📊 Data Quality Score: {quality_score:.1f}/100")
        
        if quality_score >= 80:
            print("✅ Dữ liệu chất lượng cao - Phù hợp cho phân tích chuyên sâu")
        elif quality_score >= 60:
            print("⚠️ Dữ liệu chất lượng trung bình - Cần cẩn trọng khi phân tích")
        else:
            print("❌ Dữ liệu chất lượng thấp - Kết quả phân tích có thể không đáng tin cậy")
        
        # Display key issues if any
        if validation_report['issues']:
            print(f"⚠️ Vấn đề dữ liệu ({len(validation_report['issues'])}):")
            for issue in validation_report['issues'][:3]:
                print(f"   • {issue}")
            if len(validation_report['issues']) > 3:
                print(f"   • ... và {len(validation_report['issues']) - 3} vấn đề khác")
        
        # Display cleaning actions
        if cleaning_log:
            print(f"🧹 Cleaning actions ({len(cleaning_log)}):")
            for log_item in cleaning_log[:5]:
                print(f"   • {log_item}")
            if len(cleaning_log) > 5:
                print(f"   • ... và {len(cleaning_log) - 5} hành động khác")
        
        # Final data shape and quality
        print(f"📈 Dữ liệu cuối cùng: {enhanced_df.shape[0]} rows, {enhanced_df.shape[1]} columns")
        print("✅ Validation và cleaning hoàn tất.")
        
        return enhanced_df
    
    except Exception as e:
        print(f"❌ Lỗi khi tiền xử lý dữ liệu: {e}")
        return pd.DataFrame()

def add_enhanced_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add enhanced technical features for advanced analysis
    """
    enhanced_df = df.copy()
    
    try:
        # Price-based features
        enhanced_df['Price_Range'] = enhanced_df['High'] - enhanced_df['Low']
        enhanced_df['Body_Size'] = abs(enhanced_df['Close'] - enhanced_df['Open'])
        enhanced_df['Upper_Shadow'] = enhanced_df['High'] - enhanced_df[['Open', 'Close']].max(axis=1)
        enhanced_df['Lower_Shadow'] = enhanced_df[['Open', 'Close']].min(axis=1) - enhanced_df['Low']
        
        # Volume-based features
        enhanced_df['Volume_MA_20'] = enhanced_df['Volume'].rolling(20).mean()
        enhanced_df['Volume_Ratio'] = enhanced_df['Volume'] / enhanced_df['Volume_MA_20']
        enhanced_df['Price_Volume'] = enhanced_df['Close'] * enhanced_df['Volume']
        
        # Volatility features
        enhanced_df['Returns'] = enhanced_df['Close'].pct_change()
        enhanced_df['Log_Returns'] = np.log(enhanced_df['Close'] / enhanced_df['Close'].shift(1))
        enhanced_df['Volatility_20'] = enhanced_df['Returns'].rolling(20).std()
        
        # Momentum features
        enhanced_df['Price_Momentum_5'] = enhanced_df['Close'] / enhanced_df['Close'].shift(5) - 1
        enhanced_df['Price_Momentum_10'] = enhanced_df['Close'] / enhanced_df['Close'].shift(10) - 1
        enhanced_df['Price_Momentum_20'] = enhanced_df['Close'] / enhanced_df['Close'].shift(20) - 1
        
        # Relative features
        enhanced_df['High_Low_Ratio'] = enhanced_df['High'] / enhanced_df['Low']
        enhanced_df['Close_Open_Ratio'] = enhanced_df['Close'] / enhanced_df['Open']
        
        # Time-based features
        if hasattr(enhanced_df.index, 'dayofweek'):
            enhanced_df['DayOfWeek'] = enhanced_df.index.dayofweek
            enhanced_df['Month'] = enhanced_df.index.month
            enhanced_df['Quarter'] = enhanced_df.index.quarter
        
        # Remove infinite and NaN values
        enhanced_df = enhanced_df.replace([np.inf, -np.inf], np.nan)
        
        # Forward fill and backward fill for missing values
        enhanced_df = enhanced_df.fillna(method='ffill').fillna(method='bfill')
        
        logger.info(f"Added {enhanced_df.shape[1] - df.shape[1]} enhanced features")
        
    except Exception as e:
        logger.error(f"Error adding enhanced features: {str(e)}")
        return df
    
    return enhanced_df

if __name__ == "__main__":
    # Example usage
    loader = EnhancedDataLoader()
    
    # Test single ticker
    ticker = "AAA"
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    print("Testing enhanced data loader...")
    historical_data = fetch_historical_data(ticker, start_date, end_date)
    
    if not historical_data.empty:
        print(f"✅ Successfully fetched {len(historical_data)} records")
        
        # Generate quality report
        quality_report = loader.get_data_quality_report(historical_data, ticker)
        print(f"📊 Data Quality Score: {quality_report['overall_quality_score']:.1f}/100")
        
        # Test preprocessing
        processed_data = preprocess_data(historical_data, ticker)
        print(f"📈 Enhanced data shape: {processed_data.shape}")
        
        # Test market overview
        market_data = loader.fetch_market_overview()
        print(f"📊 Market overview: {len(market_data)} indices fetched")
        
    else:
        print("❌ Failed to fetch data")