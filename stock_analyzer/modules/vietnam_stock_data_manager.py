"""
Vietnam Stock Data Manager - Quản lý dữ liệu thời gian thực cho cổ phiếu Việt Nam
Tích hợp với yfinance và tạo hệ thống cache để tối ưu hiệu suất

Author: Roo - Investment Mode
Version: 2.0.0
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
import time
import sqlite3
import json
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class VietnamStockDataManager:
    """Quản lý dữ liệu thời gian thực cho cổ phiếu Việt Nam"""
    
    def __init__(self, cache_db_path: str = "stock_data_cache.db", 
                 max_workers: int = 5, cache_expiry_hours: int = 1):
        """
        Khởi tạo Vietnam Stock Data Manager
        
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
        
        # Mapping các mã cổ phiếu cho yfinance
        self.yfinance_mapping = self._init_yfinance_mapping()
        
        logger.info(f"Vietnam Stock Data Manager initialized with cache: {cache_db_path}")
    
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
            
            # Tạo bảng metadata
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cache_metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    last_updated REAL
                )
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info("Cache database initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing cache database: {e}")
            raise
    
    def _init_yfinance_mapping(self) -> Dict[str, str]:
        """Khởi tạo mapping các mã cổ phiếu cho yfinance"""
        return {
            # HOSE stocks
            'VCB': 'VCB.VN', 'BID': 'BID.VN', 'CTG': 'CTG.VN', 'ACB': 'ACB.VN',
            'TCB': 'TCB.VN', 'STB': 'STB.VN', 'EIB': 'EIB.VN', 'MBB': 'MBB.VN',
            'VPB': 'VPB.VN', 'SHB': 'SHB.VN',
            
            # Large cap stocks
            'VIC': 'VIC.VN', 'VHM': 'VHM.VN', 'VRE': 'VRE.VN',
            'VJC': 'VJC.VN', 'HVN': 'HVN.VN', 'VNM': 'VNM.VN',
            'SAB': 'SAB.VN', 'MSN': 'MSN.VN',
            
            # Technology & Retail
            'FPT': 'FPT.VN', 'MWG': 'MWG.VN',
            
            # Oil & Gas
            'GAS': 'GAS.VN', 'PLX': 'PLX.VN', 'PVD': 'PVD.VN', 'PVS': 'PVS.VN',
            
            # Steel & Construction
            'HPG': 'HPG.VN', 'HSG': 'HSG.VN', 'CII': 'CII.VN', 'CTD': 'CTD.VN',
            
            # Healthcare
            'DHG': 'DHG.VN', 'IMP': 'IMP.VN', 'TRA': 'TRA.VN',
            
            # Securities
            'SSI': 'SSI.VN', 'VND': 'VND.VN', 'HCM': 'HCM.VN', 'VCI': 'VCI.VN',
            
            # Insurance
            'BVH': 'BVH.VN', 'BMI': 'BMI.VN',
            
            # Agriculture & Food
            'VHC': 'VHC.VN', 'ANV': 'ANV.VN', 'VCS': 'VCS.VN',
            'SBT': 'SBT.VN', 'DPR': 'DPR.VN', 'DBC': 'DBC.VN',
            
            # Others
            'REE': 'REE.VN', 'NLG': 'NLG.VN', 'KDH': 'KDH.VN', 'PDR': 'PDR.VN',
            'BCM': 'BCM.VN', 'DXG': 'DXG.VN', 'NTL': 'NTL.VN',
            'DGW': 'DGW.VN', 'GIL': 'GIL.VN', 'TCM': 'TCM.VN', 'MSH': 'MSH.VN',
            'DCM': 'DCM.VN', 'LAS': 'LAS.VN', 'PET': 'PET.VN', 'VTO': 'VTO.VN',
        }
    
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
    
    def get_yfinance_symbol(self, symbol: str) -> str:
        """Lấy symbol yfinance từ symbol Việt Nam"""
        return self.yfinance_mapping.get(symbol, f"{symbol}.VN")
    
    def fetch_real_time_data(self, symbol: str, 
                           period: str = "1mo", 
                           interval: str = "1d",
                           force_refresh: bool = False) -> Optional[pd.DataFrame]:
        """
        Lấy dữ liệu thời gian thực cho một cổ phiếu
        
        Args:
            symbol: Mã cổ phiếu
            period: Khoảng thời gian (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Khoảng cách thời gian (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
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
            
            # Fetch từ yfinance
            yf_symbol = self.get_yfinance_symbol(symbol)
            ticker = yf.Ticker(yf_symbol)
            
            # Lấy dữ liệu
            data = ticker.history(period=period, interval=interval)
            
            if data.empty:
                logger.warning(f"No data available for {symbol}")
                return None
            
            # Làm sạch dữ liệu
            data = data.dropna()
            data = data.round(2)
            
            # Lưu vào cache
            cache_data = {
                'symbol': symbol,
                'data': data.to_dict('index'),
                'period': period,
                'interval': interval,
                'last_fetched': datetime.now().isoformat()
            }
            self._set_cache_data(symbol, cache_data, 'price')
            
            logger.info(f"Successfully fetched real-time data for {symbol}: {len(data)} records")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching real-time data for {symbol}: {e}")
            return None
    
    def fetch_financial_data(self, symbol: str, force_refresh: bool = False) -> Optional[Dict]:
        """
        Lấy dữ liệu tài chính cho một cổ phiếu
        
        Returns:
            Dictionary chứa dữ liệu tài chính hoặc None nếu lỗi
        """
        try:
            # Kiểm tra cache
            if not force_refresh and self._is_cache_valid(symbol, 'financial'):
                cached_data = self._get_cache_data(symbol, 'financial')
                if cached_data:
                    return cached_data
            
            # Fetch từ yfinance
            yf_symbol = self.get_yfinance_symbol(symbol)
            ticker = yf.Ticker(yf_symbol)
            
            # Lấy thông tin tài chính
            info = ticker.info
            
            # Lấy dữ liệu tài chính nếu có
            try:
                financials = ticker.financials
                quarterly_financials = ticker.quarterly_financials
                balance_sheet = ticker.balance_sheet
                quarterly_balance_sheet = ticker.quarterly_balance_sheet
                cashflow = ticker.cashflow
                quarterly_cashflow = ticker.quarterly_cashflow
            except:
                financials = quarterly_financials = balance_sheet = quarterly_balance_sheet = None
                cashflow = quarterly_cashflow = None
            
            financial_data = {
                'symbol': symbol,
                'info': info,
                'financials': financials.to_dict() if financials is not None and not financials.empty else {},
                'quarterly_financials': quarterly_financials.to_dict() if quarterly_financials is not None and not quarterly_financials.empty else {},
                'balance_sheet': balance_sheet.to_dict() if balance_sheet is not None and not balance_sheet.empty else {},
                'quarterly_balance_sheet': quarterly_balance_sheet.to_dict() if quarterly_balance_sheet is not None and not quarterly_balance_sheet.empty else {},
                'cashflow': cashflow.to_dict() if cashflow is not None and not cashflow.empty else {},
                'quarterly_cashflow': quarterly_cashflow.to_dict() if quarterly_cashflow is not None and not quarterly_cashflow.empty else {},
                'last_fetched': datetime.now().isoformat()
            }
            
            # Lưu vào cache
            self._set_cache_data(symbol, financial_data, 'financial')
            
            logger.info(f"Successfully fetched financial data for {symbol}")
            return financial_data
            
        except Exception as e:
            logger.error(f"Error fetching financial data for {symbol}: {e}")
            return None
    
    def fetch_company_info(self, symbol: str, force_refresh: bool = False) -> Optional[Dict]:
        """
        Lấy thông tin công ty
        
        Returns:
            Dictionary chứa thông tin công ty hoặc None nếu lỗi
        """
        try:
            # Kiểm tra cache
            if not force_refresh and self._is_cache_valid(symbol, 'info'):
                cached_data = self._get_cache_data(symbol, 'info')
                if cached_data:
                    return cached_data
            
            # Fetch từ yfinance
            yf_symbol = self.get_yfinance_symbol(symbol)
            ticker = yf.Ticker(yf_symbol)
            info = ticker.info
            
            # Lấy tin tức
            try:
                news = ticker.news
            except:
                news = []
            
            company_info = {
                'symbol': symbol,
                'info': info,
                'news': news,
                'last_fetched': datetime.now().isoformat()
            }
            
            # Lưu vào cache
            self._set_cache_data(symbol, company_info, 'info')
            
            logger.info(f"Successfully fetched company info for {symbol}")
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
        
        def fetch_single_stock(symbol):
            try:
                if data_type == 'price':
                    return symbol, self.fetch_real_time_data(symbol, period, interval)
                elif data_type == 'financial':
                    return symbol, self.fetch_financial_data(symbol)
                elif data_type == 'info':
                    return symbol, self.fetch_company_info(symbol)
                else:
                    raise ValueError(f"Unsupported data_type: {data_type}")
                    
            except Exception as e:
                logger.error(f"Error fetching {data_type} data for {symbol}: {e}")
                return symbol, None
        
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

def test_vietnam_stock_data_manager():
    """Test function cho Vietnam Stock Data Manager"""
    print("🧪 Testing Vietnam Stock Data Manager...")
    
    try:
        # Khởi tạo
        data_manager = VietnamStockDataManager()
        
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
        
        print("\n✅ Vietnam Stock Data Manager test completed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_vietnam_stock_data_manager()