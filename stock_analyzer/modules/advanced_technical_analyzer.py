"""
Advanced Technical Analyzer - Phân tích kỹ thuật nâng cao với đầy đủ chỉ báo
Bao gồm MA, RSI, MACD, Bollinger Bands, Volume analysis và nhiều chỉ báo khác

Author: Roo - Investment Mode
Version: 2.0.0
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

@dataclass
class TechnicalSignals:
    """Cấu trúc dữ liệu cho các tín hiệu kỹ thuật"""
    overall_signal: str  # 'BUY', 'SELL', 'HOLD'
    confidence: float    # 0-1
    signals: Dict[str, str]  # Các tín hiệu riêng lẻ
    score: int           # Điểm tổng hợp (-100 đến 100)

class AdvancedTechnicalAnalyzer:
    """Phân tích kỹ thuật nâng cao với đầy đủ chỉ báo"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def calculate_moving_averages(self, data: pd.DataFrame, 
                                periods: List[int] = [5, 10, 20, 50, 200]) -> pd.DataFrame:
        """Tính toán Moving Averages"""
        result = data.copy()
        
        for period in periods:
            result[f'SMA_{period}'] = data['Close'].rolling(window=period).mean()
            result[f'EMA_{period}'] = data['Close'].ewm(span=period).mean()
        
        return result
    
    def calculate_rsi(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Tính toán RSI (Relative Strength Index)"""
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, data: pd.DataFrame, 
                      fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Tính toán MACD (Moving Average Convergence Divergence)"""
        ema_fast = data['Close'].ewm(span=fast).mean()
        ema_slow = data['Close'].ewm(span=slow).mean()
        
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal).mean()
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram
    
    def calculate_bollinger_bands(self, data: pd.DataFrame, 
                                 period: int = 20, std_dev: float = 2) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Tính toán Bollinger Bands"""
        middle = data['Close'].rolling(window=period).mean()
        std = data['Close'].rolling(window=period).std()
        
        upper = middle + (std * std_dev)
        lower = middle - (std * std_dev)
        
        return upper, middle, lower
    
    def calculate_stochastic(self, data: pd.DataFrame, 
                           k_period: int = 14, d_period: int = 3) -> Tuple[pd.Series, pd.Series]:
        """Tính toán Stochastic Oscillator"""
        lowest_low = data['Low'].rolling(window=k_period).min()
        highest_high = data['High'].rolling(window=k_period).max()
        
        k_percent = 100 * ((data['Close'] - lowest_low) / (highest_high - lowest_low))
        d_percent = k_percent.rolling(window=d_period).mean()
        
        return k_percent, d_percent
    
    def calculate_williams_r(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Tính toán Williams %R"""
        highest_high = data['High'].rolling(window=period).max()
        lowest_low = data['Low'].rolling(window=period).min()
        
        williams_r = -100 * ((highest_high - data['Close']) / (highest_high - lowest_low))
        return williams_r
    
    def calculate_cci(self, data: pd.DataFrame, period: int = 20) -> pd.Series:
        """Tính toán Commodity Channel Index"""
        typical_price = (data['High'] + data['Low'] + data['Close']) / 3
        sma_tp = typical_price.rolling(window=period).mean()
        mean_deviation = typical_price.rolling(window=period).apply(
            lambda x: np.mean(np.abs(x - np.mean(x)))
        )
        
        cci = (typical_price - sma_tp) / (0.015 * mean_deviation)
        return cci
    
    def calculate_obv(self, data: pd.DataFrame) -> pd.Series:
        """Tính toán On-Balance Volume"""
        obv = np.where(data['Close'] > data['Close'].shift(1), data['Volume'],
                      np.where(data['Close'] < data['Close'].shift(1), -data['Volume'], 0))
        return pd.Series(obv, index=data.index).cumsum()
    
    def calculate_ad_line(self, data: pd.DataFrame) -> pd.Series:
        """Tính toán Accumulation/Distribution Line"""
        clv = ((data['Close'] - data['Low']) - (data['High'] - data['Close'])) / (data['High'] - data['Low'])
        clv = clv.fillna(0)  # Fill NaN values when High = Low
        ad_line = (clv * data['Volume']).cumsum()
        return ad_line
    
    def calculate_atr(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Tính toán Average True Range"""
        high_low = data['High'] - data['Low']
        high_close = np.abs(data['High'] - data['Close'].shift())
        low_close = np.abs(data['Low'] - data['Close'].shift())
        
        true_range = np.maximum(high_low, np.maximum(high_close, low_close))
        atr = true_range.rolling(window=period).mean()
        return atr
    
    def calculate_volume_sma(self, data: pd.DataFrame, periods: List[int] = [10, 20, 50]) -> pd.DataFrame:
        """Tính toán Volume Moving Averages"""
        result = pd.DataFrame(index=data.index)
        
        for period in periods:
            result[f'Volume_SMA_{period}'] = data['Volume'].rolling(window=period).mean()
            result[f'Volume_Ratio_{period}'] = data['Volume'] / result[f'Volume_SMA_{period}']
        
        return result
    
    def calculate_price_oscillators(self, data: pd.DataFrame) -> Dict[str, pd.Series]:
        """Tính toán các Price Oscillators"""
        oscillators = {}
        
        # Momentum
        oscillators['Momentum'] = data['Close'] / data['Close'].shift(10) - 1
        
        # Rate of Change
        oscillators['ROC'] = (data['Close'] - data['Close'].shift(12)) / data['Close'].shift(12) * 100
        
        # Price oscillator
        short_ma = data['Close'].rolling(10).mean()
        long_ma = data['Close'].rolling(30).mean()
        oscillators['Price_Oscillator'] = (short_ma - long_ma) / long_ma * 100
        
        return oscillators
    
    def analyze_support_resistance(self, data: pd.DataFrame, window: int = 20) -> Dict[str, float]:
        """Phân tích Support và Resistance levels"""
        highs = data['High'].rolling(window=window).max()
        lows = data['Low'].rolling(window=window).min()
        
        current_price = data['Close'].iloc[-1]
        
        # Find recent resistance (highest high in recent period)
        resistance = highs.iloc[-1] if not pd.isna(highs.iloc[-1]) else current_price * 1.1
        
        # Find recent support (lowest low in recent period)
        support = lows.iloc[-1] if not pd.isna(lows.iloc[-1]) else current_price * 0.9
        
        # Calculate distance to resistance and support
        distance_to_resistance = (resistance - current_price) / current_price
        distance_to_support = (current_price - support) / current_price
        
        return {
            'resistance': resistance,
            'support': support,
            'distance_to_resistance': distance_to_resistance,
            'distance_to_support': distance_to_support,
            'current_price': current_price
        }
    
    def generate_technical_signals(self, data: pd.DataFrame) -> TechnicalSignals:
        """Tạo tổng hợp các tín hiệu kỹ thuật"""
        signals = {}
        score = 0
        
        # RSI Analysis
        if 'RSI' in data.columns:
            rsi = data['RSI'].iloc[-1]
            if rsi < 30:
                signals['RSI'] = 'OVERSOLD'
                score += 20
            elif rsi > 70:
                signals['RSI'] = 'OVERBOUGHT'
                score -= 20
            else:
                signals['RSI'] = 'NEUTRAL'
        
        # MACD Analysis
        if all(col in data.columns for col in ['MACD', 'MACD_Signal']):
            macd = data['MACD'].iloc[-1]
            macd_signal = data['MACD_Signal'].iloc[-1]
            macd_prev = data['MACD'].iloc[-2]
            signal_prev = data['MACD_Signal'].iloc[-2]
            
            if macd > macd_signal and macd_prev <= signal_prev:
                signals['MACD'] = 'BULLISH_CROSSOVER'
                score += 15
            elif macd < macd_signal and macd_prev >= signal_prev:
                signals['MACD'] = 'BEARISH_CROSSOVER'
                score -= 15
            elif macd > macd_signal:
                signals['MACD'] = 'BULLISH'
                score += 10
            else:
                signals['MACD'] = 'BEARISH'
                score -= 10
        
        # Bollinger Bands Analysis
        if all(col in data.columns for col in ['BB_Upper', 'BB_Lower']):
            current_price = data['Close'].iloc[-1]
            bb_upper = data['BB_Upper'].iloc[-1]
            bb_lower = data['BB_Lower'].iloc[-1]
            
            if current_price > bb_upper:
                signals['BB'] = 'UPPER_BREAKOUT'
                score -= 10  # Overbought
            elif current_price < bb_lower:
                signals['BB'] = 'LOWER_BREAKOUT'
                score += 10  # Oversold
            else:
                signals['BB'] = 'MIDDLE_RANGE'
        
        # Moving Average Analysis
        if all(col in data.columns for col in ['SMA_20', 'SMA_50']):
            sma_20 = data['SMA_20'].iloc[-1]
            sma_50 = data['SMA_50'].iloc[-1]
            current_price = data['Close'].iloc[-1]
            
            if current_price > sma_20 > sma_50:
                signals['MA'] = 'BULLISH_ALIGNMENT'
                score += 15
            elif current_price < sma_20 < sma_50:
                signals['MA'] = 'BEARISH_ALIGNMENT'
                score -= 15
            elif current_price > sma_20:
                signals['MA'] = 'ABOVE_SMA20'
                score += 5
            else:
                signals['MA'] = 'BELOW_SMA20'
                score -= 5
        
        # Volume Analysis
        if 'Volume_Ratio_20' in data.columns:
            volume_ratio = data['Volume_Ratio_20'].iloc[-1]
            if volume_ratio > 1.5:
                signals['Volume'] = 'HIGH_VOLUME'
                score += 10
            elif volume_ratio < 0.5:
                signals['Volume'] = 'LOW_VOLUME'
                score -= 5
            else:
                signals['Volume'] = 'NORMAL_VOLUME'
        
        # Stochastic Analysis
        if 'Stoch_K' in data.columns:
            stoch_k = data['Stoch_K'].iloc[-1]
            if stoch_k < 20:
                signals['Stochastic'] = 'OVERSOLD'
                score += 10
            elif stoch_k > 80:
                signals['Stochastic'] = 'OVERBOUGHT'
                score -= 10
            else:
                signals['Stochastic'] = 'NEUTRAL'
        
        # Determine overall signal
        if score > 30:
            overall_signal = 'STRONG_BUY'
        elif score > 15:
            overall_signal = 'BUY'
        elif score < -30:
            overall_signal = 'STRONG_SELL'
        elif score < -15:
            overall_signal = 'SELL'
        else:
            overall_signal = 'HOLD'
        
        confidence = min(abs(score) / 50, 1.0)  # Normalize confidence
        
        return TechnicalSignals(
            overall_signal=overall_signal,
            confidence=confidence,
            signals=signals,
            score=score
        )
    
    def perform_comprehensive_analysis(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Thực hiện phân tích kỹ thuật toàn diện"""
        try:
            result = data.copy()
            
            # Basic calculations
            result = self.calculate_moving_averages(result)
            result['RSI'] = self.calculate_rsi(result)
            result['MACD'], result['MACD_Signal'], result['MACD_Hist'] = self.calculate_macd(result)
            result['BB_Upper'], result['BB_Middle'], result['BB_Lower'] = self.calculate_bollinger_bands(result)
            result['Stoch_K'], result['Stoch_D'] = self.calculate_stochastic(result)
            result['Williams_R'] = self.calculate_williams_r(result)
            result['CCI'] = self.calculate_cci(result)
            result['OBV'] = self.calculate_obv(result)
            result['AD_Line'] = self.calculate_ad_line(result)
            result['ATR'] = self.calculate_atr(result)
            
            # Volume analysis
            volume_data = self.calculate_volume_sma(result)
            for col in volume_data.columns:
                result[col] = volume_data[col]
            
            # Price oscillators
            oscillators = self.calculate_price_oscillators(result)
            for name, series in oscillators.items():
                result[name] = series
            
            # Support and Resistance
            support_resistance = self.analyze_support_resistance(result)
            
            # Technical signals
            signals = self.generate_technical_signals(result)
            
            # Calculate latest values for summary
            latest_values = {
                'price': result['Close'].iloc[-1],
                'rsi': result['RSI'].iloc[-1] if 'RSI' in result.columns else None,
                'macd': result['MACD'].iloc[-1] if 'MACD' in result.columns else None,
                'volume_ratio': result['Volume_Ratio_20'].iloc[-1] if 'Volume_Ratio_20' in result.columns else None,
                'signal': signals.overall_signal,
                'confidence': signals.confidence,
                'score': signals.score
            }
            
            analysis_result = {
                'data': result,
                'latest_values': latest_values,
                'technical_signals': signals,
                'support_resistance': support_resistance,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            self.logger.info(f"Comprehensive technical analysis completed with {len(result.columns)} indicators")
            return analysis_result
            
        except Exception as e:
            self.logger.error(f"Error in comprehensive technical analysis: {e}")
            return {'error': str(e)}

def test_advanced_technical_analyzer():
    """Test function cho Advanced Technical Analyzer"""
    print("🧪 Testing Advanced Technical Analyzer...")
    
    try:
        # Tạo dữ liệu test
        np.random.seed(42)
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        dates = dates[dates.weekday < 5]  # Remove weekends
        
        # Generate realistic stock data
        n_days = len(dates)
        returns = np.random.normal(0.001, 0.02, n_days)
        prices = [100]  # Starting price
        
        for ret in returns:
            new_price = prices[-1] * (1 + ret)
            prices.append(max(new_price, 50))  # Minimum price
        
        prices = prices[1:]
        
        # Create OHLCV data
        data = []
        for i, (date, close_price) in enumerate(zip(dates, prices)):
            daily_range = np.random.uniform(0.01, 0.03) * close_price
            high = close_price + np.random.uniform(0, daily_range)
            low = close_price - np.random.uniform(0, daily_range)
            open_price = low + np.random.uniform(0, high - low)
            volume = int(np.random.uniform(100000, 2000000))
            
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
        
        # Initialize analyzer
        analyzer = AdvancedTechnicalAnalyzer()
        
        # Perform comprehensive analysis
        print("🔍 Performing comprehensive technical analysis...")
        analysis = analyzer.perform_comprehensive_analysis(df)
        
        if 'error' in analysis:
            print(f"❌ Analysis failed: {analysis['error']}")
            return
        
        # Display results
        latest = analysis['latest_values']
        signals = analysis['technical_signals']
        sr = analysis['support_resistance']
        
        print(f"📊 Technical Analysis Results:")
        print(f"   Current Price: {latest['price']:.2f}")
        print(f"   RSI: {latest['rsi']:.2f}" if latest['rsi'] else "   RSI: N/A")
        print(f"   MACD: {latest['macd']:.2f}" if latest['macd'] else "   MACD: N/A")
        print(f"   Volume Ratio: {latest['volume_ratio']:.2f}" if latest['volume_ratio'] else "   Volume Ratio: N/A")
        print(f"   \n🎯 Overall Signal: {latest['signal']}")
        print(f"   Confidence: {latest['confidence']:.2f}")
        print(f"   Technical Score: {latest['score']}")
        
        print(f"\n🛡️ Support & Resistance:")
        print(f"   Support Level: {sr['support']:.2f}")
        print(f"   Resistance Level: {sr['resistance']:.2f}")
        print(f"   Distance to Support: {sr['distance_to_support']:.2%}")
        print(f"   Distance to Resistance: {sr['distance_to_resistance']:.2%}")
        
        print(f"\n📈 Technical Signals:")
        for indicator, signal in signals.signals.items():
            print(f"   {indicator}: {signal}")
        
        print(f"\n📋 Indicators Calculated: {len(analysis['data'].columns)}")
        print(f"✅ Advanced Technical Analyzer test completed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_advanced_technical_analyzer()