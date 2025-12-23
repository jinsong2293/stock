"""
Cache Manager cho Stock Analyzer
Hệ thống cache thông minh để tối ưu hiệu suất phân tích
"""

import hashlib
import json
import os
import sqlite3
import time
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union, Callable
import streamlit as st
import pandas as pd


class CacheManager:
    """
    Intelligent caching system với TTL và validation
    """
    
    def __init__(self, cache_dir: str = "cache", db_path: str = "cache/stock_analyzer.db"):
        self.cache_dir = cache_dir
        self.db_path = db_path
        self._ensure_cache_dir()
        self._init_database()
    
    def _ensure_cache_dir(self):
        """Tạo cache directory nếu chưa có"""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def _init_database(self):
        """Khởi tạo database cache"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_cache (
                cache_key TEXT PRIMARY KEY,
                ticker TEXT NOT NULL,
                analysis_type TEXT NOT NULL,
                data BLOB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                hit_count INTEGER DEFAULT 0,
                size_bytes INTEGER
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_ticker ON analysis_cache(ticker);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_expires ON analysis_cache(expires_at);
        """)
        
        conn.commit()
        conn.close()
    
    def _generate_cache_key(self, ticker: str, analysis_type: str, params: Dict[str, Any]) -> str:
        """Tạo unique cache key"""
        # Tạo hash từ parameters
        param_str = json.dumps(params, sort_keys=True, default=str)
        key_string = f"{ticker}_{analysis_type}_{param_str}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _get_ttl_seconds(self, analysis_type: str) -> int:
        """TTL theo loại phân tích"""
        ttl_map = {
            'technical_analysis': 1800,  # 30 minutes
            'sentiment_analysis': 7200,  # 2 hours
            'financial_analysis': 86400,  # 24 hours
            'market_data': 300,  # 5 minutes
            'full_analysis': 3600,  # 1 hour
            'trend_prediction': 3600,  # 1 hour
            'anomaly_detection': 7200,  # 2 hours
        }
        return ttl_map.get(analysis_type, 3600)  # Default 1 hour
    
    def get(self, ticker: str, analysis_type: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Lấy data từ cache"""
        cache_key = self._generate_cache_key(ticker, analysis_type, params)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT data, expires_at, hit_count 
            FROM analysis_cache 
            WHERE cache_key = ?
        """, (cache_key,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            data_blob, expires_at, hit_count = result
            
            # Kiểm tra expiration
            if expires_at:
                expires_timestamp = datetime.fromisoformat(expires_at)
                if datetime.now() > expires_timestamp:
                    # Cache expired, delete it
                    self.delete(cache_key)
                    return None
            
            # Update hit count
            self._update_hit_count(cache_key, hit_count + 1)
            
            # Deserialize data
            try:
                return json.loads(data_blob.decode('utf-8'))
            except (json.JSONDecodeError, UnicodeDecodeError):
                return None
        
        return None
    
    def set(self, ticker: str, analysis_type: str, params: Dict[str, Any], data: Dict[str, Any]) -> bool:
        """Lưu data vào cache"""
        cache_key = self._generate_cache_key(ticker, analysis_type, params)
        ttl_seconds = self._get_ttl_seconds(analysis_type)
        
        expires_at = datetime.now() + timedelta(seconds=ttl_seconds)
        
        # Serialize data
        try:
            data_blob = json.dumps(data, default=str).encode('utf-8')
        except (TypeError, ValueError):
            return False
        
        size_bytes = len(data_blob)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO analysis_cache 
                (cache_key, ticker, analysis_type, data, expires_at, size_bytes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (cache_key, ticker, analysis_type, data_blob, expires_at.isoformat(), size_bytes))
            
            conn.commit()
            return True
            
        except sqlite3.Error as e:
            st.error(f"Cache storage error: {e}")
            return False
        finally:
            conn.close()
    
    def delete(self, cache_key: str) -> bool:
        """Xóa cache entry"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM analysis_cache WHERE cache_key = ?", (cache_key,))
            conn.commit()
            return True
        except sqlite3.Error:
            return False
        finally:
            conn.close()
    
    def _update_hit_count(self, cache_key: str, hit_count: int):
        """Cập nhật hit count"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE analysis_cache 
                SET hit_count = ? 
                WHERE cache_key = ?
            """, (hit_count, cache_key))
            conn.commit()
        except sqlite3.Error:
            pass
        finally:
            conn.close()
    
    def clear_expired(self) -> int:
        """Xóa tất cả expired cache entries"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                DELETE FROM analysis_cache 
                WHERE expires_at IS NOT NULL AND expires_at < datetime('now')
            """)
            
            deleted_count = cursor.rowcount
            conn.commit()
            return deleted_count
        except sqlite3.Error:
            return 0
        finally:
            conn.close()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Lấy thống kê cache"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Total entries
            cursor.execute("SELECT COUNT(*) FROM analysis_cache")
            total_entries = cursor.fetchone()[0]
            
            # Active entries (not expired)
            cursor.execute("""
                SELECT COUNT(*) FROM analysis_cache 
                WHERE expires_at IS NULL OR expires_at >= datetime('now')
            """)
            active_entries = cursor.fetchone()[0]
            
            # Total size
            cursor.execute("SELECT SUM(size_bytes) FROM analysis_cache")
            total_size = cursor.fetchone()[0] or 0
            
            # Cache hit rate
            cursor.execute("""
                SELECT 
                    SUM(hit_count) as total_hits,
                    COUNT(*) as total_entries
                FROM analysis_cache
            """)
            stats = cursor.fetchone()
            total_hits = stats[0] or 0
            total_entries_for_rate = stats[1] or 1
            
            hit_rate = (total_hits / (total_hits + total_entries_for_rate)) * 100 if total_hits > 0 else 0
            
            # Analysis type breakdown
            cursor.execute("""
                SELECT analysis_type, COUNT(*) as count
                FROM analysis_cache 
                WHERE expires_at IS NULL OR expires_at >= datetime('now')
                GROUP BY analysis_type
            """)
            type_breakdown = dict(cursor.fetchall())
            
            return {
                'total_entries': total_entries,
                'active_entries': active_entries,
                'expired_entries': total_entries - active_entries,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'cache_hit_rate': round(hit_rate, 2),
                'type_breakdown': type_breakdown
            }
        except sqlite3.Error:
            return {}
        finally:
            conn.close()
    
    def cleanup_old_entries(self, max_age_days: int = 30) -> int:
        """Xóa cache entries cũ"""
        cutoff_date = datetime.now() - timedelta(days=max_age_days)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                DELETE FROM analysis_cache 
                WHERE created_at < ?
            """, (cutoff_date.isoformat(),))
            
            deleted_count = cursor.rowcount
            conn.commit()
            return deleted_count
        except sqlite3.Error:
            return 0
        finally:
            conn.close()


# Global cache instance
_cache_manager = None

def get_cache_manager() -> CacheManager:
    """Lấy global cache manager instance"""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager


def cached_analysis(ticker: str, analysis_type: str, params: Dict[str, Any], 
                   analysis_func: Callable, *args, **kwargs) -> Dict[str, Any]:
    """
    Decorator-like function để cache analysis results
    
    Args:
        ticker: Stock ticker
        analysis_type: Type of analysis
        params: Parameters for cache key
        analysis_func: Function to call if not cached
        *args, **kwargs: Arguments for analysis_func
    """
    cache_manager = get_cache_manager()
    
    # Try to get from cache first
    cached_result = cache_manager.get(ticker, analysis_type, params)
    if cached_result is not None:
        return {
            'data': cached_result,
            'from_cache': True,
            'cache_hit': True
        }
    
    # Cache miss, perform analysis
    try:
        result = analysis_func(*args, **kwargs)
        
        # Cache the result
        cache_manager.set(ticker, analysis_type, params, result)
        
        return {
            'data': result,
            'from_cache': False,
            'cache_hit': False
        }
    except Exception as e:
        return {
            'data': None,
            'from_cache': False,
            'cache_hit': False,
            'error': str(e)
        }


# Streamlit cache decorators
def streamlit_cached_analysis(ttl_seconds: int = 3600):
    """
    Streamlit cache decorator cho analysis functions
    """
    def decorator(func: Callable) -> Callable:
        return st.cache_data(ttl=ttl_seconds)(func)
    return decorator


# Cache management utilities
def display_cache_stats():
    """Hiển thị cache statistics trong Streamlit"""
    cache_manager = get_cache_manager()
    stats = cache_manager.get_cache_stats()
    
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Cache Entries", stats.get('total_entries', 0))
        
        with col2:
            st.metric("Active Entries", stats.get('active_entries', 0))
        
        with col3:
            st.metric("Cache Hit Rate", f"{stats.get('cache_hit_rate', 0):.1f}%")
        
        with col4:
            st.metric("Size (MB)", f"{stats.get('total_size_mb', 0):.2f}")
        
        # Type breakdown
        if stats.get('type_breakdown'):
            st.subheader("Cache by Analysis Type")
            type_data = pd.DataFrame(
                list(stats['type_breakdown'].items()),
                columns=['Analysis Type', 'Count']
            )
            st.bar_chart(type_data.set_index('Analysis Type'))


def cleanup_cache():
    """Cleanup cache - remove expired and old entries"""
    cache_manager = get_cache_manager()
    
    # Remove expired entries
    expired_count = cache_manager.clear_expired()
    
    # Remove entries older than 30 days
    old_count = cache_manager.cleanup_old_entries()
    
    return expired_count, old_count


if __name__ == "__main__":
    # Test cache manager
    cache_manager = CacheManager()
    
    # Test caching
    test_data = {'test': 'data', 'timestamp': datetime.now().isoformat()}
    cache_manager.set('AAA', 'test_analysis', {'param1': 'value1'}, test_data)
    
    # Test retrieval
    cached = cache_manager.get('AAA', 'test_analysis', {'param1': 'value1'})
    print("Cached data:", cached)
    
    # Test stats
    stats = cache_manager.get_cache_stats()
    print("Cache stats:", stats)