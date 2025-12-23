"""
Vietnam Stock Data Manager Simple - Quản lý dữ liệu thời gian thực cho cổ phiếu Việt Nam (Simple Version)
Tạo mock data để test functionality

Author: Roo - Investment Mode
Version: 2.0.0
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
import time
import sqlite3
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class VietnamStockDataManagerSimple:
    """Quản lý dữ liệu thời gian thực cho cổ phiếu Việt Nam (Simple Version)"""
    
    def __init__(self, cache_db_path: str = "stock_data_cache.db", 
                 max_workers: int = 5, cache_expiry_hours: int = 1):
        """
        Khởi tạo Vietnam Stock Data Manager Simple
        
        Args:
            cache_db_path: Đường dẫn đến database cache
            max_workers: Số lượng thread tối đa cho việc fetch dữ liệu song song
            cache_expiry_hours: Thời gian hết hạn cache (giờ)
        """
        self.cache_db_path = cache_db_path
        self.max_workers = max_workers
        self.cache_expiry_hours = cache_expiry_hours
        self.cache_expiry_seconds = cache_expiry_hours * 3600
        
        # Khởi tạo database cache
        self._init_cache_database()
        
        logger.info(f"Vietnam Stock Data Manager Simple initialized with cache: {cache_db_path}")
    
    def _init_cache_database(self):
        """Khởi tạo database cache SQLite"""
        try:
            conn = sqlite3.connect(self.cache_db_path)
            cursor = conn.cursor()
            
            # Tạo bảng cache cho dữ liệu giá
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS price_cache (
                    symbol TEXT PRIMARY KEY,
                    data TEXT,
                    last_updated REAL,
                    data_type TEXT DEFAULT 'price'
                )
            ''')
            
            # Tạo bảng cache cho dữ liệu tài chính
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS financial_cache (
                    symbol TEXT PRIMARY KEY,
                    data TEXT,
                    last_updated REAL,
                    data_type TEXT DEFAULT 'financial'
                )
            ''')
            
            # Tạo bảng cache cho thông tin công ty
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS info_cache (
                    symbol TEXT PRIMARY KEY,
                    data TEXT,
                    last_updated REAL,
                    data_type TEXT DEFAULT 'info'
                )
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info("Cache database initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing cache database: {e}")
            raise
    
    def _is_cache_valid(self, symbol: str, data_type: str) -> bool:
        """Kiểm tra xem cache có còn hợp lệ không"""
        try:
            conn = sqlite3.connect(self.cache_db_path)
            cursor = conn.cursor()
            
            table_name = f"{data_type}_cache"
            cursor.execute(f'''
                SELECT last_updated FROM {table_name} 
                WHERE symbol = ?
            ''', (symbol,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                last_updated = result[0]
                current_time = time.time()
                return (current_time - last_updated) < self.cache_expiry_seconds
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking cache validity for {symbol}: {e}")
            return False
    
    def _get_cache_data(self, symbol: str, data_type: str) -> Optional[Dict]:
        """Lấy dữ liệu từ cache"""
        try:
            conn = sqlite3.connect(self.cache_db_path)
            cursor = conn.cursor()
            
            table_name = f"{data_type}_cache"
            cursor.execute(f'''
                SELECT data FROM {table_name} 
                WHERE symbol = ?
            ''', (symbol,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return json.loads(result[0])
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting cache data for {symbol}: {e}")
            return None
    
    def _set_cache_data(self, symbol: str, data: Dict, data_type: str):
        """Lưu dữ liệu vào cache"""
        try:
            conn = sqlite3.connect(self.cache_db_path)
            cursor = conn.cursor()
            
            table_name = f"{data_type}_cache"
            current_time = time.time()
            
            cursor.execute(f'''
                INSERT OR REPLACE INTO {table_name} (symbol, data, last_updated, data_type)
                VALUES (?, ?, ?, ?)
            ''', (symbol, json.dumps(data), current_time, data_type))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error setting cache data for {symbol}: {e}")
    
    def _generate_mock_data(self, symbol: str, days: int = 30) -> pd.DataFrame:
        """Tạo dữ liệu giả để test"""
        # Sử dụng seed dựa trên symbol để có dữ liệu nhất quán
        np.random.seed(hash(symbol) % 1000)
        
        # Tạo dates
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Loại bỏ weekend
        dates = dates[dates.weekday < 5]
        
        # Tạo dữ liệu giá thực tế
        base_price = np.random.uniform(10000, 100000)  # 10K - 100K VND
        returns = np.random.normal(0.001, 0.02, len(dates))  # Daily returns
        prices = [base_price]
        
        for ret in returns:
            new_price = prices[-1] * (1 + ret)
            prices.append(max(new_price, 1000))  # Minimum price
        
        prices = prices[1:]  # Remove first price
        
        # Tạo OHLCV data
        data = []
        for i, (date, close_price) in enumerate(zip(dates, prices)):
            # Tạo realistic OHLC
            daily_range = np.random.uniform(0.01, 0.03) * close_price
            high = close_price + np.random.uniform(0, daily_range)
            low = close_price - np.random.uniform(0, daily_range)
            open_price = low + np.random.uniform(0, high - low)
            
            # Tạo volume realistic
            base_volume = np.random.uniform(500000, 5000000)
            volume = int(base_volume * np.random.uniform(0.5, 2.0))
            
            data.append({
                'Date': date,
                'Open': round(open_price, 2),
                'High': round(high, 2),
                'Low': round(low, 2),
                'Close': round(close_price, 2),
                'Volume': volume
            })
        
        df = pd.DataFrame(data)
        df.set_index('Date', inplace=True)
        return df
    
    def fetch_real_time_data(self, symbol: str, 
                           period: str = "1mo", 
                           interval: str = "1d",
                           force_refresh: bool = False) -> Optional[pd.DataFrame]:
        """
        Lấy dữ liệu thời gian thực cho một cổ phiếu (Mock version)
        
        Args:
            symbol: Mã cổ phiếu
            period: Khoảng thời gian (1d, 5d, 1mo, 3mo, 6mo, 1y)
            interval: Khoảng cách thời gian (1d, 5d, 1wk, 1mo)
            force_refresh: Bỏ qua cache và fetch mới
            
        Returns:
            DataFrame chứa dữ liệu OHLCV hoặc None nếu lỗi
        """
        try:
            # Kiểm tra cache
            if not force_refresh and self._is_cache_valid(symbol, 'price'):
                cached_data = self._get_cache_data(symbol, 'price')
                if cached_data:
                    df = pd.DataFrame(cached_data['data'])
                    df.index = pd.to_datetime(df.index)
                    return df
            
            # Tạo mock data
            days_map = {
                '1d': 5, '5d': 10, '1mo': 30, '3mo': 90, 
                '6mo': 180, '1y': 365
            }
            days = days_map.get(period, 30)
            
            data = self._generate_mock_data(symbol, days)
            
            # Lưu vào cache
            cache_data = {
                'symbol': symbol,
                'data': data.to_dict('index'),
                'period': period,
                'interval': interval,
                'last_fetched': datetime.now().isoformat()
            }
            
            # Convert datetime index to string for JSON serialization
            for key in cache_data['data']:
                if hasattr(key, 'isoformat'):
                    cache_data['data'][key.isoformat()] = cache_data['data'].pop(key)
            self._set_cache_data(symbol, cache_data, 'price')
            
            logger.info(f"Successfully generated mock data for {symbol}: {len(data)} records")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching real-time data for {symbol}: {e}")
            return None
    
    def fetch_financial_data(self, symbol: str, force_refresh: bool = False) -> Optional[Dict]:
        """
        Lấy dữ liệu tài chính cho một cổ phiếu (Mock version)
        
        Returns:
            Dictionary chứa dữ liệu tài chính hoặc None nếu lỗi
        """
        try:
            # Kiểm tra cache
            if not force_refresh and self._is_cache_valid(symbol, 'financial'):
                cached_data = self._get_cache_data(symbol, 'financial')
                if cached_data:
                    return cached_data
            
            # Tạo mock financial data
            np.random.seed(hash(symbol) % 1000)
            
            financial_data = {
                'symbol': symbol,
                'info': {
                    'marketCap': np.random.uniform(1000000000, 100000000000),  # 1B to 100B VND
                    'trailingPE': np.random.uniform(8, 30),
                    'priceToBook': np.random.uniform(0.5, 5),
                    'returnOnEquity': np.random.uniform(0.05, 0.25),
                    'returnOnAssets': np.random.uniform(0.02, 0.15),
                    'debtToEquity': np.random.uniform(0.1, 1.0),
                    'currentRatio': np.random.uniform(1.0, 3.0),
                    'profitMargins': np.random.uniform(0.05, 0.25),
                    'operatingMargins': np.random.uniform(0.1, 0.3),
                    'revenueGrowth': np.random.uniform(-0.1, 0.3)
                },
                'last_fetched': datetime.now().isoformat()
            }
            
            # Lưu vào cache
            self._set_cache_data(symbol, financial_data, 'financial')
            
            logger.info(f"Successfully generated mock financial data for {symbol}")
            return financial_data
            
        except Exception as e:
            logger.error(f"Error fetching financial data for {symbol}: {e}")
            return None
    
    def fetch_company_info(self, symbol: str, force_refresh: bool = False) -> Optional[Dict]:
        """
        Lấy thông tin công ty (Mock version)
        
        Returns:
            Dictionary chứa thông tin công ty hoặc None nếu lỗi
        """
        try:
            # Kiểm tra cache
            if not force_refresh and self._is_cache_valid(symbol, 'info'):
                cached_data = self._get_cache_data(symbol, 'info')
                if cached_data:
                    return cached_data
            
            # Tạo mock company info
            company_info = {
                'symbol': symbol,
                'info': {
                    'longName': f"{symbol} Corporation",
                    'sector': np.random.choice(['Technology', 'Banking', 'Real Estate', 'Food & Beverage', 'Oil & Gas']),
                    'industry': 'Conglomerate',
                    'fullTimeEmployees': np.random.randint(1000, 100000),
                    'website': f"https://{symbol.lower()}.com.vn"
                },
                'news': [
                    {
                        'title': f"{symbol} reports strong quarterly results",
                        'publisher': "Vietnam Finance News",
                        'publishedTime': datetime.now().isoformat()
                    }
                ],
                'last_fetched': datetime.now().isoformat()
            }
            
            # Lưu vào cache
            self._set_cache_data(symbol, company_info, 'info')
            
            logger.info(f"Successfully generated mock company info for {symbol}")
            return company_info
            
        except Exception as e:
            logger.error(f"Error fetching company info for {symbol}: {e}")
            return None
    
    def fetch_multiple_stocks_data(self, symbols: List[str], 
                                 data_type: str = 'price',
                                 period: str = "1mo",
                                 interval: str = "1d",
                                 max_workers: Optional[int] = None) -> Dict[str, Any]:
        """
        Lấy dữ liệu cho nhiều cổ phiếu song song
        
        Args:
            symbols: Danh sách mã cổ phiếu
            data_type: Loại dữ liệu ('price', 'financial', 'info')
            period, interval: Chỉ áp dụng cho data_type='price'
            max_workers: Số thread tối đa (mặc định sử dụng self.max_workers)
            
        Returns:
            Dictionary với key là symbol và value là dữ liệu
        """
        if max_workers is None:
            max_workers = self.max_workers
        
        results = {}
        failed_symbols = []
        
        def fetch_single_stock(stock_symbol: str):
            try:
                if data_type == 'price':
                    return stock_symbol, self.fetch_real_time_data(stock_symbol, period, interval)
                elif data_type == 'financial':
                    return stock_symbol, self.fetch_financial_data(stock_symbol)
                elif data_type == 'info':
                    return stock_symbol, self.fetch_company_info(stock_symbol)
                else:
                    raise ValueError(f"Unsupported data_type: {data_type}")
                    
            except Exception as e:
                logger.error(f"Error fetching {data_type} data for {stock_symbol}: {e}")
                return stock_symbol, None
        
        # Sử dụng ThreadPoolExecutor để fetch song song
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_symbol = {
                executor.submit(fetch_single_stock, symbol): symbol 
                for symbol in symbols
            }
            
            for future in as_completed(future_to_symbol):
                symbol, result = future.result()
                if result is not None:
                    results[symbol] = result
                else:
                    failed_symbols.append(symbol)
        
        logger.info(f"Successfully fetched {data_type} data for {len(results)}/{len(symbols)} symbols")
        if failed_symbols:
            logger.warning(f"Failed to fetch data for symbols: {failed_symbols}")
        
        return results
    
    def get_market_overview(self, symbols: List[str]) -> Dict[str, Any]:
        """
        Lấy tổng quan thị trường cho danh sách cổ phiếu
        
        Returns:
            Dictionary chứa thống kê tổng quan
        """
        try:
            # Fetch dữ liệu giá cho tất cả symbols
            price_data = self.fetch_multiple_stocks_data(symbols, 'price', '5d')
            
            market_stats = {
                'total_symbols': len(symbols),
                'successful_fetches': len(price_data),
                'failed_fetches': len(symbols) - len(price_data),
                'timestamp': datetime.now().isoformat(),
                'individual_stats': {}
            }
            
            for symbol, data in price_data.items():
                if data is not None and not data.empty:
                    current_price = data['Close'].iloc[-1]
                    prev_price = data['Close'].iloc[0] if len(data) > 1 else current_price
                    price_change = current_price - prev_price
                    price_change_pct = (price_change / prev_price) * 100 if prev_price != 0 else 0
                    
                    volume_avg = data['Volume'].mean()
                    volume_latest = data['Volume'].iloc[-1]
                    
                    market_stats['individual_stats'][symbol] = {
                        'current_price': current_price,
                        'price_change': price_change,
                        'price_change_pct': price_change_pct,
                        'volume_avg': volume_avg,
                        'volume_latest': volume_latest,
                        'volume_ratio': volume_latest / volume_avg if volume_avg > 0 else 0
                    }
            
            # Tính toán thống kê tổng quan
            if market_stats['individual_stats']:
                all_changes = [stats['price_change_pct'] for stats in market_stats['individual_stats'].values()]
                market_stats['market_summary'] = {
                    'avg_price_change_pct': np.mean(all_changes),
                    'max_gain_pct': np.max(all_changes),
                    'max_loss_pct': np.min(all_changes),
                    'positive_stocks': len([x for x in all_changes if x > 0]),
                    'negative_stocks': len([x for x in all_changes if x < 0]),
                    'neutral_stocks': len([x for x in all_changes if x == 0])
                }
            
            return market_stats
            
        except Exception as e:
            logger.error(f"Error getting market overview: {e}")
            return {'error': str(e)}
    
    def clear_cache(self, data_type: str = 'all'):
        """Xóa cache"""
        try:
            conn = sqlite3.connect(self.cache_db_path)
            cursor = conn.cursor()
            
            if data_type == 'all':
                cursor.execute('DELETE FROM price_cache')
                cursor.execute('DELETE FROM financial_cache')
                cursor.execute('DELETE FROM info_cache')
                logger.info("All cache cleared")
            else:
                table_name = f"{data_type}_cache"
                cursor.execute(f'DELETE FROM {table_name}')
                logger.info(f"{data_type} cache cleared")
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Lấy thống kê cache"""
        try:
            conn = sqlite3.connect(self.cache_db_path)
            cursor = conn.cursor()
            
            stats = {}
            
            for cache_type in ['price', 'financial', 'info']:
                table_name = f"{cache_type}_cache"
                cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
                count = cursor.fetchone()[0]
                
                cursor.execute(f'''
                    SELECT AVG(last_updated) FROM {table_name}
                ''')
                avg_age = cursor.fetchone()[0]
                
                stats[cache_type] = {
                    'count': count,
                    'avg_age_hours': (time.time() - avg_age) / 3600 if avg_age else 0
                }
            
            conn.close()
            return stats
            
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {}

def test_vietnam_stock_data_manager_simple():
    """Test function cho Vietnam Stock Data Manager Simple"""
    print("🧪 Testing Vietnam Stock Data Manager Simple...")
    
    try:
        # Khởi tạo
        data_manager = VietnamStockDataManagerSimple()
        
        # Test single stock
        print("\n📊 Testing single stock data fetch...")
        vcb_data = data_manager.fetch_real_time_data('VCB', period='5d')
        if vcb_data is not None:
            print(f"✅ VCB data: {len(vcb_data)} records")
            print(f"   Latest price: {vcb_data['Close'].iloc[-1]:.2f}")
        else:
            print("❌ Failed to fetch VCB data")
        
        # Test multiple stocks
        print("\n📈 Testing multiple stocks fetch...")
        test_symbols = ['VCB', 'BID', 'VNM', 'FPT', 'HPG']
        multiple_data = data_manager.fetch_multiple_stocks_data(test_symbols, 'price', '3d')
        print(f"✅ Fetched data for {len(multiple_data)} stocks")
        
        # Test financial data
        print("\n💰 Testing financial data fetch...")
        vcb_financial = data_manager.fetch_financial_data('VCB')
        if vcb_financial is not None:
            pe_ratio = vcb_financial['info']['trailingPE']
            print(f"✅ VCB P/E ratio: {pe_ratio:.2f}")
        
        # Test market overview
        print("\n🌍 Testing market overview...")
        overview = data_manager.get_market_overview(test_symbols)
        if 'market_summary' in overview:
            summary = overview['market_summary']
            print(f"   Average change: {summary['avg_price_change_pct']:.2f}%")
            print(f"   Positive stocks: {summary['positive_stocks']}/{len(test_symbols)}")
        
        # Test cache stats
        print("\n💾 Testing cache stats...")
        cache_stats = data_manager.get_cache_stats()
        for cache_type, stats in cache_stats.items():
            print(f"   {cache_type} cache: {stats['count']} items, avg age: {stats['avg_age_hours']:.1f}h")
        
        print("\n✅ Vietnam Stock Data Manager Simple test completed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_vietnam_stock_data_manager_simple()