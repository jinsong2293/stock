"""
Advanced Feature Engineering System - Tích hợp features từ nhiều nguồn
Kết hợp technical analysis, macro economic và news sentiment features

Author: Roo - Architect Mode
Version: 1.0.0
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import logging
import warnings
warnings.filterwarnings('ignore')

# Import các module hiện có
from stock_analyzer.modules.technical_analysis import (
    calculate_rsi, calculate_macd, calculate_bollinger_bands,
    calculate_obv, calculate_ad_line, calculate_atr, perform_technical_analysis
)
from stock_analyzer.modules.macro_economic_analyzer import macro_economic_analyzer
from stock_analyzer.modules.news_sentiment_analyzer import NewsSentimentAnalyzer

logger = logging.getLogger(__name__)

class AdvancedFeatureEngineer:
    """
    Hệ thống tạo đặc trưng nâng cao từ nhiều nguồn dữ liệu
    """
    
    def __init__(self):
        self.news_analyzer = NewsSentimentAnalyzer()
        self.feature_config = self._initialize_feature_config()
        self.feature_weights = self._initialize_feature_weights()
        
    def _initialize_feature_config(self) -> Dict[str, Dict[str, Any]]:
        """
        Cấu hình các features và tham số
        """
        return {
            # Technical Features
            'technical': {
                'rsi_windows': [14, 21, 30],
                'ma_windows': [5, 10, 20, 50, 100],
                'macd_windows': [(12, 26, 9), (8, 21, 5)],
                'bollinger_windows': [20, 30],
                'atr_windows': [14, 21],
                'volume_windows': [10, 20, 50]
            },
            
            # Macro Features
            'macro': {
                'indicators': [
                    'fed_funds_rate', 'treasury_10y', 'cpi', 'gdp_growth',
                    'unemployment_rate', 'vix', 'dollar_index'
                ],
                'transformation': ['level', 'change', 'momentum']
            },
            
            # Sentiment Features
            'sentiment': {
                'windows': [3, 7, 14],
                'metrics': [
                    'sentiment_score', 'weighted_sentiment', 'sentiment_trend',
                    'sentiment_volatility', 'news_volume', 'positive_ratio',
                    'negative_ratio', 'sentiment_momentum', 'sentiment_acceleration'
                ]
            }
        }
    
    def _initialize_feature_weights(self) -> Dict[str, float]:
        """
        Trọng số cho các loại features
        """
        return {
            'technical': 0.5,
            'macro': 0.3,
            'sentiment': 0.2
        }
    
    def create_technical_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Tạo technical features từ price data
        """
        logger.info("Tạo technical features...")
        df = data.copy()
        
        # Sử dụng technical analysis module hiện có
        df = perform_technical_analysis(df)
        
        # Additional technical features
        df['Returns'] = df['Close'].pct_change()
        df['Returns_2'] = df['Close'].pct_change(2)
        df['Returns_5'] = df['Close'].pct_change(5)
        df['Returns_10'] = df['Close'].pct_change(10)
        
        # Log returns
        df['Log_Returns'] = np.log(df['Close'] / df['Close'].shift(1))
        
        # Price ratios
        df['High_Low_Ratio'] = df['High'] / df['Low']
        df['Open_Close_Ratio'] = df['Open'] / df['Close']
        
        # Volume features
        df['Volume_MA_5'] = df['Volume'].rolling(window=5).mean()
        df['Volume_MA_20'] = df['Volume'].rolling(window=20).mean()
        df['Volume_Ratio'] = df['Volume'] / df['Volume_MA_20']
        df['Volume_Price_Trend'] = df['Volume'] * df['Returns']
        
        # Volatility features
        df['Price_Volatility_5'] = df['Returns'].rolling(window=5).std()
        df['Price_Volatility_20'] = df['Returns'].rolling(window=20).std()
        df['Volume_Volatility'] = df['Volume'].rolling(window=20).std()
        
        # Multiple RSI periods
        for window in self.feature_config['technical']['rsi_windows']:
            df[f'RSI_{window}'] = calculate_rsi(df, window=window)
        
        # Multiple Moving Averages
        for window in self.feature_config['technical']['ma_windows']:
            df[f'MA_{window}'] = df['Close'].rolling(window=window).mean()
            df[f'MA_Distance_{window}'] = (df['Close'] - df[f'MA_{window}']) / df[f'MA_{window}']
        
        # Price position relative to moving averages
        for window in [20, 50, 100]:
            if f'MA_{window}' in df.columns:
                df[f'Price_Above_MA_{window}'] = (df['Close'] > df[f'MA_{window}']).astype(int)
        
        # MACD variations
        for short, long, signal in self.feature_config['technical']['macd_windows']:
            macd, macd_signal, macd_hist = calculate_macd(
                df, short_window=short, long_window=long, signal_window=signal
            )
            df[f'MACD_{short}_{long}_{signal}'] = macd
            df[f'MACD_Signal_{short}_{long}_{signal}'] = macd_signal
            df[f'MACD_Hist_{short}_{long}_{signal}'] = macd_hist
        
        # Bollinger Bands variations
        for window in self.feature_config['technical']['bollinger_windows']:
            bb_upper, bb_middle, bb_lower = calculate_bollinger_bands(df, window=window)
            df[f'BB_Upper_{window}'] = bb_upper
            df[f'BB_Middle_{window}'] = bb_middle
            df[f'BB_Lower_{window}'] = bb_lower
            df[f'BB_Position_{window}'] = (df['Close'] - bb_lower) / (bb_upper - bb_lower)
            df[f'BB_Width_{window}'] = (bb_upper - bb_lower) / bb_middle
        
        # ATR variations
        for window in self.feature_config['technical']['atr_windows']:
            df[f'ATR_{window}'] = calculate_atr(df, window=window)
            df[f'Price_ATR_Ratio_{window}'] = df['Close'] / df[f'ATR_{window}']
        
        # Support and Resistance levels
        df['Support_20'] = df['Low'].rolling(window=20).min()
        df['Resistance_20'] = df['High'].rolling(window=20).max()
        df['Support_Distance'] = (df['Close'] - df['Support_20']) / df['Close']
        df['Resistance_Distance'] = (df['Resistance_20'] - df['Close']) / df['Close']
        
        # Trend features
        df['Price_Trend_5'] = (df['Close'] / df['Close'].shift(5) - 1) * 100
        df['Price_Trend_20'] = (df['Close'] / df['Close'].shift(20) - 1) * 100
        df['Volume_Trend'] = df['Volume'] / df['Volume'].rolling(window=20).mean()
        
        logger.info(f"Tạo được {len(df.columns)} technical features")
        return df
    
    def create_macro_features(self, market_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Tạo macro economic features
        """
        logger.info("Tạo macro economic features...")
        
        features = {}
        
        try:
            # Lấy macro economic analysis
            macro_analysis = macro_economic_analyzer.analyze_macro_economic_factors(
                market="US", asset_class="equities"
            )
            
            # Economic score
            features['macro_economic_score'] = macro_analysis.get('economic_score', 50.0)
            
            # Economic cycle phase (encoded)
            cycle_phase = macro_analysis.get('economic_cycle', {}).get('current_phase', 'unknown')
            cycle_encoding = {
                'recession': -2,
                'recovery': -1,
                'expansion': 1,
                'peak': 2,
                'unknown': 0
            }
            features['economic_cycle_encoded'] = cycle_encoding.get(cycle_phase.value, 0)
            features['cycle_score'] = macro_analysis.get('economic_cycle', {}).get('cycle_score', 0.0)
            
            # Factor impacts
            factor_impact = macro_analysis.get('factor_impact', {})
            features['total_impact_score'] = factor_impact.get('total_impact_score', 0.0)
            features['risk_level_encoded'] = {
                'low': -1, 'medium': 0, 'high': 1
            }.get(factor_impact.get('risk_level', 'medium'), 0)
            
            # Market correlation
            market_correlation = macro_analysis.get('market_correlation', {})
            features['market_sentiment_impact'] = market_correlation.get('market_sentiment_impact', 0.0)
            features['volatility_outlook_encoded'] = {
                'low': -1, 'normal': 0, 'high': 1
            }.get(market_correlation.get('volatility_outlook', 'normal'), 0)
            
            # Economic indicators
            indicators = macro_analysis.get('economic_indicators', {})
            for indicator_name, indicator in indicators.items():
                features[f'{indicator_name}_value'] = indicator.value
                features[f'{indicator_name}_change_pct'] = indicator.change_percent
                features[f'{indicator_name}_impact_score'] = indicator.impact_score
            
            # Leading indicators
            leading_indicators = macro_analysis.get('economic_cycle', {}).get('leading_indicators', {})
            features['yield_curve_spread'] = leading_indicators.get('yield_curve_spread', 0.0)
            features['employment_gap'] = leading_indicators.get('employment_gap', 0.0)
            
            # Confidence score
            features['macro_confidence'] = macro_analysis.get('economic_cycle', {}).get('confidence', 0.5)
            
        except Exception as e:
            logger.error(f"Lỗi tạo macro features: {e}")
            # Fallback values
            features = {
                'macro_economic_score': 50.0,
                'economic_cycle_encoded': 0,
                'cycle_score': 0.0,
                'total_impact_score': 0.0,
                'risk_level_encoded': 0,
                'market_sentiment_impact': 0.0,
                'volatility_outlook_encoded': 0
            }
        
        logger.info(f"Tạo được {len(features)} macro features")
        return features
    
    def create_sentiment_features(self, symbol: str, days: int = 7) -> Dict[str, float]:
        """
        Tạo sentiment features từ tin tức
        """
        logger.info(f"Tạo sentiment features cho {symbol}...")
        
        try:
            # Lấy sentiment features từ news analyzer
            sentiment_features = self.news_analyzer.get_sentiment_features(symbol, days)
            
            # Thêm các features phái sinh
            features = sentiment_features.copy()
            
            # Sentiment momentum features
            for window in [3, 7]:
                # Moving average của sentiment
                sentiment_data = [article['sentiment_score'] for article in 
                                self.news_analyzer.get_financial_news(symbol, days) or []]
                if len(sentiment_data) >= window:
                    sentiment_ma = np.mean(sentiment_data[-window:])
                    features[f'sentiment_ma_{window}'] = sentiment_ma
                    features[f'sentiment_ma_distance_{window}'] = (
                        sentiment_features['sentiment_score'] - sentiment_ma
                    )
            
            # Sentiment regime features
            if sentiment_features['sentiment_score'] > 0.7:
                features['sentiment_regime'] = 2  # Very positive
            elif sentiment_features['sentiment_score'] > 0.6:
                features['sentiment_regime'] = 1  # Positive
            elif sentiment_features['sentiment_score'] < 0.3:
                features['sentiment_regime'] = -2  # Very negative
            elif sentiment_features['sentiment_score'] < 0.4:
                features['sentiment_regime'] = -1  # Negative
            else:
                features['sentiment_regime'] = 0  # Neutral
            
            # News impact score (kết hợp volume và sentiment)
            features['news_impact_score'] = (
                sentiment_features['news_volume'] * 
                abs(sentiment_features['sentiment_score'] - 0.5) * 2
            )
            
            # Sentiment persistence
            recent_news = self.news_analyzer.get_financial_news(symbol, days=3) or []
            if len(recent_news) >= 2:
                sentiments = [article.get('sentiment_score', 0.5) for article in recent_news]
                features['sentiment_persistence'] = 1 - np.std(sentiments)
            else:
                features['sentiment_persistence'] = 0.5
                
        except Exception as e:
            logger.error(f"Lỗi tạo sentiment features: {e}")
            features = {
                'sentiment_score': 0.5,
                'weighted_sentiment': 0.5,
                'sentiment_trend_encoded': 0,
                'sentiment_volatility': 0.0,
                'news_volume': 0,
                'positive_ratio': 0.33,
                'negative_ratio': 0.33,
                'neutral_ratio': 0.33,
                'sentiment_momentum': 0.0,
                'sentiment_acceleration': 0.0,
                'sentiment_regime': 0,
                'news_impact_score': 0.0,
                'sentiment_persistence': 0.5
            }
        
        logger.info(f"Tạo được {len(features)} sentiment features")
        return features
    
    def create_combined_features(self, technical_data: pd.DataFrame, 
                               macro_features: Dict[str, float], 
                               sentiment_features: Dict[str, float]) -> pd.DataFrame:
        """
        Kết hợp tất cả features thành một DataFrame
        """
        logger.info("Kết hợp tất cả features...")
        
        # Bắt đầu với technical features
        combined_df = technical_data.copy()
        
        # Thêm macro features (lấy giá trị cuối cùng)
        for feature_name, value in macro_features.items():
            combined_df[f'macro_{feature_name}'] = value
        
        # Thêm sentiment features
        for feature_name, value in sentiment_features.items():
            combined_df[f'sentiment_{feature_name}'] = value
        
        # Tạo interaction features (chỉ với dữ liệu đủ)
        if len(combined_df) > 10:
            combined_df = self._create_interaction_features(combined_df)
        
        # Tạo lag features (giới hạn)
        if len(combined_df) > 5:
            combined_df = self._create_lag_features(combined_df, max_lags=2)
        
        # Tạo rolling statistics (giới hạn)
        if len(combined_df) > 5:
            combined_df = self._create_rolling_statistics(combined_df, windows=[5])
        
        # Xử lý NaN tạm thời trong quá trình tạo features
        combined_df = combined_df.fillna(method='ffill').fillna(method='bfill')
        
        logger.info(f"Kết hợp thành công {len(combined_df.columns)} features")
        return combined_df
    
    def _create_interaction_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Tạo interaction features giữa các biến
        """
        # Technical-Macro interactions
        if 'RSI' in df.columns and 'macro_economic_score' in df.columns:
            df['rsi_macro_interaction'] = df['RSI'] * df['macro_economic_score'] / 100
        
        if 'MACD' in df.columns and 'sentiment_sentiment_score' in df.columns:
            df['macd_sentiment_interaction'] = df['MACD'] * df['sentiment_sentiment_score']
        
        # Volume-Sentiment interactions
        if 'Volume_Ratio' in df.columns and 'sentiment_news_volume' in df.columns:
            df['volume_sentiment_interaction'] = (
                df['Volume_Ratio'] * np.log1p(df['sentiment_news_volume'])
            )
        
        # Macro-Sentiment interactions
        if 'macro_economic_score' in df.columns and 'sentiment_sentiment_score' in df.columns:
            df['macro_sentiment_interaction'] = (
                df['macro_economic_score'] * df['sentiment_sentiment_score'] / 100
            )
        
        return df
    
    def _create_lag_features(self, df: pd.DataFrame, max_lags: int = 3) -> pd.DataFrame:
        """
        Tạo lag features cho các biến quan trọng
        """
        important_features = [
            'Close', 'Returns', 'Volume'
        ]
        
        for feature in important_features:
            if feature in df.columns:
                for lag in range(1, max_lags + 1):
                    df[f'{feature}_lag_{lag}'] = df[feature].shift(lag)
        
        return df
    
    def _create_rolling_statistics(self, df: pd.DataFrame, windows: List[int] = [5, 10]) -> pd.DataFrame:
        """
        Tạo rolling statistics cho các biến chính
        """
        for window in windows:
            # Rolling means
            if 'Returns' in df.columns:
                df[f'Returns_MA_{window}'] = df['Returns'].rolling(window=window).mean()
            
            # Rolling standard deviations
            if 'Returns' in df.columns:
                df[f'Returns_Std_{window}'] = df['Returns'].rolling(window=window).std()
        
        return df
    
    def prepare_features(self, symbol: str, historical_data: pd.DataFrame, 
                        days_history: int = 30) -> pd.DataFrame:
        """
        Chuẩn bị toàn bộ features cho mô hình dự báo
        """
        logger.info(f"Chuẩn bị features cho {symbol} với {len(historical_data) if historical_data is not None else 0} ngày lịch sử")
        
        try:
            # Kiểm tra dữ liệu đầu vào
            if historical_data is None or historical_data.empty:
                logger.warning(f"Dữ liệu lịch sử trống cho {symbol}")
                return pd.DataFrame()
            
            # Kiểm tra các cột bắt buộc
            required_columns = ['Close']
            if not all(col in historical_data.columns for col in required_columns):
                logger.error(f"Thiếu các cột bắt buộc: {required_columns} trong dữ liệu")
                return pd.DataFrame()
            
            # Lọc dữ liệu theo số ngày yêu cầu
            if len(historical_data) > days_history:
                historical_data = historical_data.tail(days_history)
            
            # Kiểm tra lại dữ liệu sau khi lọc
            if len(historical_data) < 5:
                logger.warning(f"Không đủ dữ liệu sau khi lọc cho {symbol} ({len(historical_data)} ngày)")
                return pd.DataFrame()
            
            # Tạo technical features
            technical_features = self.create_technical_features(historical_data)
            
            # Kiểm tra technical features
            if technical_features is None or technical_features.empty:
                logger.warning(f"Không thể tạo technical features cho {symbol}")
                return pd.DataFrame()
            
            # Tạo macro features
            macro_features = self.create_macro_features({})
            
            # Tạo sentiment features
            sentiment_features = self.create_sentiment_features(symbol, days=7)
            
            # Kết hợp tất cả features
            combined_features = self.create_combined_features(
                technical_features, macro_features, sentiment_features
            )
            
            # Kiểm tra combined features
            if combined_features is None or combined_features.empty:
                logger.warning(f"Không thể kết hợp features cho {symbol}")
                return pd.DataFrame()
            
            # Xử lý NaN values một cách thông minh
            logger.info("Xử lý NaN values...")
            
            # Thay thế NaN values với giá trị phù hợp
            numeric_columns = combined_features.select_dtypes(include=[np.number]).columns
            combined_features[numeric_columns] = combined_features[numeric_columns].fillna(
                combined_features[numeric_columns].median()
            )
            
            # Loại bỏ các hàng có quá nhiều NaN
            nan_threshold = 0.5  # Cho phép tối đa 50% NaN values
            combined_features = combined_features.dropna(thresh=int(len(combined_features.columns) * (1 - nan_threshold)))
            
            # Kiểm tra lần cuối
            if combined_features.empty or len(combined_features) < 5:
                logger.warning(f"Không đủ dữ liệu sau khi xử lý NaN cho {symbol} ({len(combined_features)} samples)")
                return pd.DataFrame()
            
            logger.info(f"Hoàn thành chuẩn bị features: {len(combined_features.columns)} features, "
                       f"{len(combined_features)} samples")
            
            return combined_features
            
        except Exception as e:
            logger.error(f"Lỗi trong quá trình chuẩn bị features: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return pd.DataFrame()
    
    def get_feature_importance_info(self) -> Dict[str, Any]:
        """
        Trả về thông tin về feature importance và weights
        """
        return {
            'feature_weights': self.feature_weights,
            'feature_config': self.feature_config,
            'total_features_expected': (
                len(self.feature_config['technical']['rsi_windows']) +
                len(self.feature_config['technical']['ma_windows']) * 2 +
                len(self.feature_config['technical']['macd_windows']) * 3 +
                len(self.feature_config['technical']['bollinger_windows']) * 3 +
                len(self.feature_config['technical']['atr_windows']) +
                len(self.feature_config['macro']['indicators']) * 3 +
                len(self.feature_config['sentiment']['metrics']) +
                len(self.feature_config['technical']['volume_windows'])
            )
        }

def test_advanced_feature_engineer():
    """
    Test function cho Advanced Feature Engineer
    """
    print("🧪 Testing Advanced Feature Engineer...")
    
    try:
        # Tạo dummy data
        from datetime import datetime, timedelta
        dates = pd.date_range(start=datetime.now() - timedelta(days=100), 
                             end=datetime.now(), freq='D')
        np.random.seed(42)
        dummy_prices = 100 + np.cumsum(np.random.randn(len(dates)) * 0.02)
        dummy_volume = np.random.randint(1000000, 5000000, len(dates))
        
        dummy_data = pd.DataFrame({
            'Date': dates,
            'Open': dummy_prices - np.random.rand(len(dates)) * 2,
            'High': dummy_prices + np.random.rand(len(dates)) * 2,
            'Low': dummy_prices - np.random.rand(len(dates)) * 3,
            'Close': dummy_prices,
            'Volume': dummy_volume
        })
        dummy_data.set_index('Date', inplace=True)
        
        # Test feature engineer
        feature_engineer = AdvancedFeatureEngineer()
        
        print("🔧 Tạo features...")
        features_df = feature_engineer.prepare_features("TEST", dummy_data, days_history=50)
        
        print(f"✅ Tạo thành công {len(features_df.columns)} features")
        print(f"📊 Số samples: {len(features_df)}")
        
        # Hiển thị một số features quan trọng
        important_features = [col for col in features_df.columns if any(keyword in col.lower() 
                            for keyword in ['rsi', 'macd', 'sentiment', 'macro', 'ma_'])]
        print(f"🎯 Features quan trọng ({len(important_features)}):")
        for feature in important_features[:10]:
            print(f"  {feature}: {features_df[feature].iloc[-1]:.4f}")
        
        # Feature info
        feature_info = feature_engineer.get_feature_importance_info()
        print(f"📈 Total expected features: {feature_info['total_features_expected']}")
        
        print("✅ Advanced Feature Engineer test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_advanced_feature_engineer()