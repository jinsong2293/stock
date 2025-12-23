"""
Advanced Multi-dimensional Analysis Engine
Technical Analysis Matrix with Multi-timeframe and Multi-indicator Analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import warnings

logger = logging.getLogger(__name__)
warnings.filterwarnings('ignore')

class TimeFrame(Enum):
    """Supported timeframes for analysis"""
    TICK = "tick"
    M1 = "1m"
    M5 = "5m"
    M15 = "15m"
    M30 = "30m"
    H1 = "1h"
    H4 = "4h"
    D1 = "1d"
    W1 = "1w"
    M1_MONTH = "1M"

class IndicatorCategory(Enum):
    """Categories of technical indicators"""
    TREND = "trend"
    MOMENTUM = "momentum"
    VOLATILITY = "volatility"
    VOLUME = "volume"
    PATTERN = "pattern"
    MARKET_STRUCTURE = "market_structure"

@dataclass
class IndicatorConfig:
    """Configuration for technical indicators"""
    name: str
    category: IndicatorCategory
    function: str
    params: Dict[str, Any]
    weight: float = 1.0
    enabled: bool = True

class TechnicalAnalysisMatrix:
    """
    Advanced Technical Analysis Matrix with multi-timeframe and multi-indicator support
    """
    
    def __init__(self):
        self.indicators = self._initialize_indicators()
        self.timeframes = [tf.value for tf in TimeFrame]
        self.matrix_results = {}
        
    def _initialize_indicators(self) -> Dict[str, IndicatorConfig]:
        """Initialize technical indicators configuration"""
        indicators = {}
        
        # Trend Indicators
        indicators.update({
            'SMA_20': IndicatorConfig('SMA_20', IndicatorCategory.TREND, 'SMA', {'timeperiod': 20}),
            'SMA_50': IndicatorConfig('SMA_50', IndicatorCategory.TREND, 'SMA', {'timeperiod': 50}),
            'SMA_200': IndicatorConfig('SMA_200', IndicatorCategory.TREND, 'SMA', {'timeperiod': 200}),
            'EMA_12': IndicatorConfig('EMA_12', IndicatorCategory.TREND, 'EMA', {'timeperiod': 12}),
            'EMA_26': IndicatorConfig('EMA_26', IndicatorCategory.TREND, 'EMA', {'timeperiod': 26}),
            'MACD': IndicatorConfig('MACD', IndicatorCategory.TREND, 'MACD', {
                'fastperiod': 12, 'slowperiod': 26, 'signalperiod': 9
            }),
            'ADX': IndicatorConfig('ADX', IndicatorCategory.TREND, 'ADX', {'timeperiod': 14}),
            'PARABOLIC_SAR': IndicatorConfig('PARABOLIC_SAR', IndicatorCategory.TREND, 'SARsar', {}),
            'AROON_UP': IndicatorConfig('AROON_UP', IndicatorCategory.TREND, 'AROON', {'timeperiod': 14, 'output': 'up'}),
            'AROON_DOWN': IndicatorConfig('AROON_DOWN', IndicatorCategory.TREND, 'AROON', {'timeperiod': 14, 'output': 'down'}),
        })
        
        # Momentum Indicators
        indicators.update({
            'RSI': IndicatorConfig('RSI', IndicatorCategory.MOMENTUM, 'RSI', {'timeperiod': 14}),
            'STOCH_K': IndicatorConfig('STOCH_K', IndicatorCategory.MOMENTUM, 'STOCH', {
                'fastk_period': 14, 'slowk_period': 3, 'slowd_period': 3
            }),
            'STOCH_D': IndicatorConfig('STOCH_D', IndicatorCategory.MOMENTUM, 'STOCH', {
                'fastk_period': 14, 'slowk_period': 3, 'slowd_period': 3
            }),
            'WILLIAMS_R': IndicatorConfig('WILLIAMS_R', IndicatorCategory.MOMENTUM, 'WILLR', {'timeperiod': 14}),
            'CCI': IndicatorConfig('CCI', IndicatorCategory.MOMENTUM, 'CCI', {'timeperiod': 20}),
            'ROC': IndicatorConfig('ROC', IndicatorCategory.MOMENTUM, 'ROC', {'timeperiod': 12}),
            'MOM': IndicatorConfig('MOM', IndicatorCategory.MOMENTUM, 'MOM', {'timeperiod': 10}),
            'ULTIMATE_OSC': IndicatorConfig('ULTIMATE_OSC', IndicatorCategory.MOMENTUM, 'ULTOSC', {}),
        })
        
        # Volatility Indicators
        indicators.update({
            'BOLLINGER_UPPER': IndicatorConfig('BOLLINGER_UPPER', IndicatorCategory.VOLATILITY, 'BBANDS', {
                'timeperiod': 20, 'nbdevup': 2, 'nbdevdn': 2
            }),
            'BOLLINGER_MIDDLE': IndicatorConfig('BOLLINGER_MIDDLE', IndicatorCategory.VOLATILITY, 'BBANDS', {
                'timeperiod': 20, 'nbdevup': 2, 'nbdevdn': 2
            }),
            'BOLLINGER_LOWER': IndicatorConfig('BOLLINGER_LOWER', IndicatorCategory.VOLATILITY, 'BBANDS', {
                'timeperiod': 20, 'nbdevup': 2, 'nbdevdn': 2
            }),
            'ATR': IndicatorConfig('ATR', IndicatorCategory.VOLATILITY, 'ATR', {'timeperiod': 14}),
            'NATR': IndicatorConfig('NATR', IndicatorCategory.VOLATILITY, 'NATR', {'timeperiod': 14}),
            'TRANGE': IndicatorConfig('TRANGE', IndicatorCategory.VOLATILITY, 'TRANGE', {}),
        })
        
        # Volume Indicators
        indicators.update({
            'OBV': IndicatorConfig('OBV', IndicatorCategory.VOLUME, 'OBV', {}),
            'AD': IndicatorConfig('AD', IndicatorCategory.VOLUME, 'AD', {}),
            'ADOSC': IndicatorConfig('ADOSC', IndicatorCategory.VOLUME, 'ADOSC', {}),
            'MFI': IndicatorConfig('MFI', IndicatorCategory.VOLUME, 'MFI', {'timeperiod': 14}),
            'VOLUME_SMA': IndicatorConfig('VOLUME_SMA', IndicatorCategory.VOLUME, 'SMA', {
                'timeperiod': 20, 'field': 'volume'
            }),
        })
        
        # Market Structure Indicators
        indicators.update({
            'ICHIMOKU_CONV': IndicatorConfig('ICHIMOKU_CONV', IndicatorCategory.MARKET_STRUCTURE, 'ICHIMOKU', {
                'conversion_period': 9, 'base_period': 26, 'lagging_span2': 52
            }),
            'ICHIMOKU_BASE': IndicatorConfig('ICHIMOKU_BASE', IndicatorCategory.MARKET_STRUCTURE, 'ICHIMOKU', {
                'conversion_period': 9, 'base_period': 26, 'lagging_span2': 52
            }),
            'ICHIMOKU_SPAN_A': IndicatorConfig('ICHIMOKU_SPAN_A', IndicatorCategory.MARKET_STRUCTURE, 'ICHIMOKU', {
                'conversion_period': 9, 'base_period': 26, 'lagging_span2': 52
            }),
            'ICHIMOKU_SPAN_B': IndicatorConfig('ICHIMOKU_SPAN_B', IndicatorCategory.MARKET_STRUCTURE, 'ICHIMOKU', {
                'conversion_period': 9, 'base_period': 26, 'lagging_span2': 52
            }),
        })
        
        return indicators
    
    def calculate_multi_timeframe_matrix(self, df: pd.DataFrame, symbol: str, 
                                       timeframes: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Calculate technical analysis matrix across multiple timeframes
        """
        if timeframes is None:
            timeframes = ['1d']  # Default to daily only
            
        logger.info(f"Calculating multi-timeframe matrix for {symbol}")
        
        matrix_results = {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'timeframes': {},
            'cross_timeframe_signals': {},
            'matrix_consensus': {
                'overall_score': 0.5,
                'confidence': 0.0,
                'primary_bias': 'neutral'
            }
        }
        
        for tf in timeframes:
            try:
                if tf == '1d':
                    tf_data = df.copy()
                else:
                    tf_data = self._resample_data(df, tf)
                
                if len(tf_data) > 20:  # Minimum data requirement
                    tf_results = self._calculate_single_timeframe(tf_data, tf)
                    matrix_results['timeframes'][tf] = tf_results
                else:
                    logger.warning(f"Insufficient data for timeframe {tf}: {len(tf_data)} rows")
                    
            except Exception as e:
                logger.error(f"Error processing timeframe {tf}: {str(e)}")
                continue
        
        # Always calculate consensus if we have at least one timeframe
        if len(matrix_results['timeframes']) > 0:
            matrix_results['cross_timeframe_signals'] = self._analyze_cross_timeframe_signals(
                matrix_results['timeframes']
            )
            matrix_results['matrix_consensus'] = self._calculate_matrix_consensus(
                matrix_results['timeframes'], matrix_results['cross_timeframe_signals']
            )
        
        self.matrix_results[symbol] = matrix_results
        return matrix_results
    
    def _calculate_single_timeframe(self, df: pd.DataFrame, timeframe: str) -> Dict[str, Any]:
        """
        Calculate all indicators for a single timeframe
        """
        results = {
            'timeframe': timeframe,
            'data_points': len(df),
            'indicators': {},
            'signals': {},
            'score': 0.0
        }
        
        try:
            # Calculate each indicator
            for indicator_name, config in self.indicators.items():
                if not config.enabled:
                    continue
                    
                try:
                    indicator_values = self._calculate_indicator(df, config)
                    if indicator_values is not None and len(indicator_values) > 0:
                        results['indicators'][indicator_name] = {
                            'values': indicator_values.tolist(),
                            'current_value': float(indicator_values.iloc[-1]) if len(indicator_values) > 0 else 0.0,
                            'category': config.category.value,
                            'weight': config.weight
                        }
                        
                        # Generate signals for this indicator
                        signals = self._generate_indicator_signals(indicator_name, config, indicator_values, df)
                        if signals:
                            results['signals'][indicator_name] = signals
                            
                except Exception as e:
                    logger.warning(f"Error calculating {indicator_name}: {str(e)}")
                    continue
            
            # Calculate timeframe score
            results['score'] = self._calculate_timeframe_score(results['signals'])
            
        except Exception as e:
            logger.error(f"Error in single timeframe calculation: {str(e)}")
            
        return results
    
    def _calculate_indicator(self, df: pd.DataFrame, config: IndicatorConfig) -> Optional[pd.Series]:
        """
        Calculate a specific technical indicator using pandas/numpy
        """
        try:
            func_name = config.function
            
            if func_name == 'SMA':
                return df['Close'].rolling(window=config.params['timeperiod']).mean()
            elif func_name == 'EMA':
                return df['Close'].ewm(span=config.params['timeperiod']).mean()
            elif func_name == 'MACD':
                fastperiod = config.params['fastperiod']
                slowperiod = config.params['slowperiod']
                signalperiod = config.params['signalperiod']
                
                ema_fast = df['Close'].ewm(span=fastperiod).mean()
                ema_slow = df['Close'].ewm(span=slowperiod).mean()
                macd_line = ema_fast - ema_slow
                signal_line = macd_line.ewm(span=signalperiod).mean()
                
                return macd_line
            elif func_name == 'RSI':
                delta = df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=config.params['timeperiod']).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=config.params['timeperiod']).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs))
                return rsi
            elif func_name == 'BBANDS':
                period = config.params['timeperiod']
                nbdevup = config.params['nbdevup']
                nbdevdn = config.params['nbdevdn']
                
                sma = df['Close'].rolling(window=period).mean()
                std = df['Close'].rolling(window=period).std()
                
                upper = sma + (std * nbdevup)
                middle = sma
                lower = sma - (std * nbdevdn)
                
                return pd.DataFrame({
                    'upper': upper,
                    'middle': middle,
                    'lower': lower
                }, index=df.index)
            elif func_name == 'ATR':
                period = config.params['timeperiod']
                
                high_low = df['High'] - df['Low']
                high_close = np.abs(df['High'] - df['Close'].shift())
                low_close = np.abs(df['Low'] - df['Close'].shift())
                
                true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
                atr = true_range.rolling(window=period).mean()
                
                return atr
            elif func_name == 'ADX':
                period = config.params['timeperiod']
                
                high_low = df['High'] - df['Low']
                high_close = np.abs(df['High'] - df['Close'].shift())
                low_close = np.abs(df['Low'] - df['Close'].shift())
                
                tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
                
                up_move = df['High'] - df['High'].shift()
                down_move = df['Low'].shift() - df['Low']
                
                plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
                minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)
                
                plus_dm = pd.Series(plus_dm, index=df.index)
                minus_dm = pd.Series(minus_dm, index=df.index)
                
                tr_smooth = tr.rolling(window=period).mean()
                plus_dm_smooth = plus_dm.rolling(window=period).mean()
                minus_dm_smooth = minus_dm.rolling(window=period).mean()
                
                plus_di = 100 * (plus_dm_smooth / tr_smooth)
                minus_di = 100 * (minus_dm_smooth / tr_smooth)
                
                dx = 100 * (np.abs(plus_di - minus_di) / (plus_di + minus_di))
                adx = dx.rolling(window=period).mean()
                
                return adx
            elif func_name == 'STOCH':
                period = config.params['fastk_period']
                
                low_min = df['Low'].rolling(window=period).min()
                high_max = df['High'].rolling(window=period).max()
                
                k_percent = 100 * ((df['Close'] - low_min) / (high_max - low_min))
                d_percent = k_percent.rolling(window=3).mean()
                
                return pd.DataFrame({
                    'slowk': k_percent,
                    'slowd': d_percent
                }, index=df.index)
            elif func_name == 'WILLR':
                period = config.params['timeperiod']
                
                high_14 = df['High'].rolling(window=period).max()
                low_14 = df['Low'].rolling(window=period).min()
                
                williams_r = -100 * ((high_14 - df['Close']) / (high_14 - low_14))
                
                return williams_r
            elif func_name == 'CCI':
                period = config.params['timeperiod']
                
                typical_price = (df['High'] + df['Low'] + df['Close']) / 3
                sma_tp = typical_price.rolling(window=period).mean()
                mad = typical_price.rolling(window=period).apply(lambda x: np.abs(x - x.mean()).mean(), raw=True)
                
                cci = (typical_price - sma_tp) / (0.015 * mad)
                
                return cci
            elif func_name == 'OBV':
                obv = np.where(df['Close'] > df['Close'].shift(), df['Volume'], 
                             np.where(df['Close'] < df['Close'].shift(), -df['Volume'], 0))
                
                return pd.Series(np.cumsum(obv), index=df.index)
            elif func_name == 'MFI':
                period = config.params['timeperiod']
                
                typical_price = (df['High'] + df['Low'] + df['Close']) / 3
                money_flow = typical_price * df['Volume']
                
                positive_flow = np.where(typical_price > typical_price.shift(), money_flow, 0)
                negative_flow = np.where(typical_price < typical_price.shift(), money_flow, 0)
                
                positive_mf = pd.Series(positive_flow, index=df.index).rolling(window=period).sum()
                negative_mf = pd.Series(negative_flow, index=df.index).rolling(window=period).sum()
                
                mfi_ratio = positive_mf / negative_mf
                mfi = 100 - (100 / (1 + mfi_ratio))
                
                return mfi
            else:
                logger.warning(f"Unknown indicator function: {func_name}")
                return None
                
        except Exception as e:
            logger.error(f"Error calculating indicator {config.name}: {str(e)}")
            return None
    
    def _generate_indicator_signals(self, indicator_name: str, config: IndicatorConfig, 
                                  indicator_values: pd.Series, price_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate trading signals for a specific indicator
        """
        signals = {
            'bullish_signals': 0,
            'bearish_signals': 0,
            'neutral_signals': 0,
            'signal_strength': 0.0,
            'signal_type': 'neutral'
        }
        
        try:
            if len(indicator_values) < 2:
                return signals
            
            current_value = indicator_values.iloc[-1]
            previous_value = indicator_values.iloc[-2] if len(indicator_values) > 1 else current_value
            
            # RSI Signals
            if 'RSI' in indicator_name:
                if current_value < 30:
                    signals['bullish_signals'] = 1
                    signals['signal_strength'] = max(0, (30 - current_value) / 30)
                elif current_value > 70:
                    signals['bearish_signals'] = 1
                    signals['signal_strength'] = max(0, (current_value - 70) / 30)
                else:
                    signals['neutral_signals'] = 1
                    
            # MACD Signals
            elif 'MACD' in indicator_name and len(indicator_values) > 1:
                if current_value > previous_value and current_value > 0:
                    signals['bullish_signals'] = 1
                    signals['signal_strength'] = min(1.0, abs(current_value) / 100)
                elif current_value < previous_value and current_value < 0:
                    signals['bearish_signals'] = 1
                    signals['signal_strength'] = min(1.0, abs(current_value) / 100)
                else:
                    signals['neutral_signals'] = 1
                    
            # Bollinger Bands Signals
            elif 'BOLLINGER' in indicator_name:
                current_price = price_data['Close'].iloc[-1]
                if 'upper' in indicator_name.columns if isinstance(indicator_values, pd.DataFrame) else False:
                    upper = indicator_values['upper'].iloc[-1]
                    if current_price >= upper * 0.98:
                        signals['bearish_signals'] = 1
                        signals['signal_strength'] = min(1.0, (current_price - upper) / upper * 10)
                elif 'lower' in indicator_values.columns if isinstance(indicator_values, pd.DataFrame) else False:
                    lower = indicator_values['lower'].iloc[-1]
                    if current_price <= lower * 1.02:
                        signals['bullish_signals'] = 1
                        signals['signal_strength'] = min(1.0, (lower - current_price) / lower * 10)
                else:
                    signals['neutral_signals'] = 1
                    
            # Default signal determination
            if signals['bullish_signals'] > signals['bearish_signals']:
                signals['signal_type'] = 'bullish'
            elif signals['bearish_signals'] > signals['bullish_signals']:
                signals['signal_type'] = 'bearish'
            else:
                signals['signal_type'] = 'neutral'
                
        except Exception as e:
            logger.error(f"Error generating signals for {indicator_name}: {str(e)}")
            
        return signals
    
    def _analyze_cross_timeframe_signals(self, timeframe_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze signals across multiple timeframes
        """
        cross_tf_analysis = {
            'alignment_score': 0.0,
            'trend_alignment': {},
            'momentum_alignment': {},
            'overall_bias': 'neutral'
        }
        
        try:
            bullish_count = 0
            bearish_count = 0
            total_signals = 0
            
            for tf, results in timeframe_results.items():
                if 'signals' in results:
                    for indicator, signals in results['signals'].items():
                        if signals['signal_type'] == 'bullish':
                            bullish_count += 1
                        elif signals['signal_type'] == 'bearish':
                            bearish_count += 1
                        total_signals += 1
            
            # Calculate alignment score
            if total_signals > 0:
                max_count = max(bullish_count, bearish_count)
                alignment_score = max_count / total_signals
                cross_tf_analysis['alignment_score'] = alignment_score
                
                if bullish_count > bearish_count:
                    cross_tf_analysis['overall_bias'] = 'bullish'
                elif bearish_count > bullish_count:
                    cross_tf_analysis['overall_bias'] = 'bearish'
                    
        except Exception as e:
            logger.error(f"Error in cross-timeframe analysis: {str(e)}")
            
        return cross_tf_analysis
    
    def _calculate_matrix_consensus(self, timeframe_results: Dict[str, Any], 
                                  cross_tf_signals: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate overall consensus across the matrix
        """
        consensus = {
            'overall_score': 0.0,
            'confidence': 0.0,
            'primary_bias': 'neutral',
            'timeframe_weights': {},
            'category_scores': {}
        }
        
        try:
            total_score = 0.0
            total_weight = 0.0
            category_scores = {}
            
            # Weight timeframes (longer timeframes have higher weight)
            timeframe_weights = {'1d': 0.5, '4h': 0.3, '1h': 0.2}
            
            for tf, results in timeframe_results.items():
                weight = timeframe_weights.get(tf, 0.1)
                tf_score = results.get('score', 0.0)
                
                total_score += tf_score * weight
                total_weight += weight
                
                consensus['timeframe_weights'][tf] = weight
            
            # Calculate overall score
            if total_weight > 0:
                consensus['overall_score'] = total_score / total_weight
                
            # Determine primary bias
            if consensus['overall_score'] > 0.6:
                consensus['primary_bias'] = 'bullish'
            elif consensus['overall_score'] < 0.4:
                consensus['primary_bias'] = 'bearish'
            else:
                consensus['primary_bias'] = 'neutral'
                
            # Calculate confidence based on alignment
            consensus['confidence'] = cross_tf_signals.get('alignment_score', 0.0)
            
        except Exception as e:
            logger.error(f"Error calculating matrix consensus: {str(e)}")
            
        return consensus
    
    def _resample_data(self, df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
        """
        Resample data to different timeframe
        """
        try:
            if timeframe == '1h':
                agg_dict = {
                    'Open': 'first',
                    'High': 'max',
                    'Low': 'min',
                    'Close': 'last',
                    'Volume': 'sum'
                }
                return df.resample('1H').agg(agg_dict).dropna()
            elif timeframe == '4h':
                agg_dict = {
                    'Open': 'first',
                    'High': 'max',
                    'Low': 'min',
                    'Close': 'last',
                    'Volume': 'sum'
                }
                return df.resample('4H').agg(agg_dict).dropna()
            elif timeframe == '15m':
                agg_dict = {
                    'Open': 'first',
                    'High': 'max',
                    'Low': 'min',
                    'Close': 'last',
                    'Volume': 'sum'
                }
                return df.resample('15T').agg(agg_dict).dropna()
            else:
                return df
                
        except Exception as e:
            logger.error(f"Error resampling data to {timeframe}: {str(e)}")
            return df
    
    def _calculate_timeframe_score(self, signals: Dict[str, Any]) -> float:
        """
        Calculate overall score for a timeframe based on signals
        """
        if not signals:
            return 0.5  # Neutral score if no signals
            
        total_score = 0.0
        total_weight = 0.0
        
        for indicator, signal_data in signals.items():
            signal_type = signal_data.get('signal_type', 'neutral')
            strength = signal_data.get('signal_strength', 0.0)
            
            if signal_type == 'bullish':
                score = 0.5 + strength * 0.5
            elif signal_type == 'bearish':
                score = 0.5 - strength * 0.5
            else:
                score = 0.5
                
            total_score += score
            total_weight += 1.0
        
        return total_score / total_weight if total_weight > 0 else 0.5
    
    def get_matrix_summary(self, symbol: str) -> Dict[str, Any]:
        """
        Get summary of the technical analysis matrix
        """
        if symbol not in self.matrix_results:
            return {"error": f"No matrix results found for {symbol}"}
        
        results = self.matrix_results[symbol]
        summary = {
            'symbol': symbol,
            'timeframes_analyzed': len(results.get('timeframes', {})),
            'overall_consensus': results.get('matrix_consensus', {}),
            'top_signals': [],
            'recommendation': 'hold'
        }
        
        try:
            # Collect all signals
            all_signals = []
            for tf, tf_results in results.get('timeframes', {}).items():
                for indicator, signals in tf_results.get('signals', {}).items():
                    signal_strength = signals.get('signal_strength', 0.0)
                    signal_type = signals.get('signal_type', 'neutral')
                    if signal_strength > 0.5:  # Only strong signals
                        all_signals.append({
                            'timeframe': tf,
                            'indicator': indicator,
                            'type': signal_type,
                            'strength': signal_strength
                        })
            
            # Sort by strength and get top signals
            all_signals.sort(key=lambda x: x['strength'], reverse=True)
            summary['top_signals'] = all_signals[:10]
            
            # Generate recommendation
            overall_bias = results.get('matrix_consensus', {}).get('primary_bias', 'neutral')
            confidence = results.get('matrix_consensus', {}).get('confidence', 0.0)
            
            if overall_bias == 'bullish' and confidence > 0.7:
                summary['recommendation'] = 'buy'
            elif overall_bias == 'bearish' and confidence > 0.7:
                summary['recommendation'] = 'sell'
            else:
                summary['recommendation'] = 'hold'
                
        except Exception as e:
            logger.error(f"Error generating matrix summary: {str(e)}")
            
        return summary

# Global instance
technical_matrix = TechnicalAnalysisMatrix()

if __name__ == "__main__":
    # Example usage
    from stock_analyzer.modules.enhanced_data_loader import fetch_historical_data, preprocess_data
    from datetime import datetime, timedelta
    
    print("🧪 Testing Technical Analysis Matrix...")
    
    # Test data
    ticker = "AAA"
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    try:
        # Fetch and preprocess data
        raw_data = fetch_historical_data(ticker, start_date, end_date)
        processed_data = preprocess_data(raw_data, ticker)
        
        if not processed_data.empty:
            # Calculate matrix
            matrix_results = technical_matrix.calculate_multi_timeframe_matrix(
                processed_data, ticker, timeframes=['1d', '4h', '1h']
            )
            
            print(f"✅ Matrix calculated for {len(matrix_results['timeframes'])} timeframes")
            
            # Get summary
            summary = technical_matrix.get_matrix_summary(ticker)
            print(f"📊 Overall Score: {summary['overall_consensus']['overall_score']:.2f}")
            print(f"🎯 Primary Bias: {summary['overall_consensus']['primary_bias']}")
            print(f"💡 Recommendation: {summary['recommendation']}")
            print(f"📈 Top Signals: {len(summary['top_signals'])} strong signals found")
            
        else:
            print("❌ No data available for testing")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()