"""
Advanced Technical Analysis Module
Provides dynamic parameter optimization and advanced technical indicators
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
import logging
from sklearn.model_selection import ParameterGrid
from sklearn.metrics import accuracy_score, precision_score, recall_score
import warnings

logger = logging.getLogger(__name__)

class DynamicParameterOptimizer:
    """
    Dynamic parameter optimization for technical indicators
    """
    
    def __init__(self):
        self.optimization_history = {}
        self.default_parameters = {
            'rsi': {'window': 14},
            'macd': {'short_window': 12, 'long_window': 26, 'signal_window': 9},
            'bollinger': {'window': 20, 'num_std_dev': 2},
            'stochastic': {'k_window': 14, 'd_window': 3},
            'williams': {'window': 14}
        }
    
    def optimize_rsi_parameters(self, df: pd.DataFrame, symbol: str) -> Dict[str, Any]:
        """
        Optimize RSI parameters based on historical performance
        """
        logger.info(f"Optimizing RSI parameters for {symbol}")
        
        # Define parameter grid
        rsi_params = {'window': [7, 10, 12, 14, 16, 18, 20, 22, 25]}
        
        best_params = None
        best_score = -float('inf')
        results = []
        
        for params in ParameterGrid(rsi_params):
            try:
                # Calculate RSI with current parameters
                rsi = self._calculate_rsi(df, **params)
                
                # Generate signals based on RSI
                signals = self._generate_rsi_signals(rsi)
                
                # Calculate performance metrics
                performance = self._calculate_signal_performance(df['Close'], signals)
                
                # Use Sharpe-like ratio for optimization
                score = performance['sharpe_ratio'] if performance['sharpe_ratio'] != -float('inf') else -100
                
                results.append({
                    'params': params,
                    'score': score,
                    'performance': performance
                })
                
                if score > best_score:
                    best_score = score
                    best_params = params
                    
            except Exception as e:
                logger.warning(f"Error testing RSI params {params}: {str(e)}")
                continue
        
        optimization_result = {
            'best_params': best_params or self.default_parameters['rsi'],
            'best_score': best_score,
            'all_results': results,
            'optimization_type': 'RSI'
        }
        
        # Store optimization history
        self.optimization_history[f"{symbol}_rsi"] = optimization_result
        
        logger.info(f"RSI optimization completed for {symbol}. Best params: {best_params}, Score: {best_score:.3f}")
        
        return optimization_result
    
    def optimize_macd_parameters(self, df: pd.DataFrame, symbol: str) -> Dict[str, Any]:
        """
        Optimize MACD parameters based on historical performance
        """
        logger.info(f"Optimizing MACD parameters for {symbol}")
        
        # Define parameter grid
        macd_params = {
            'short_window': [8, 10, 12, 15, 18],
            'long_window': [20, 22, 26, 30, 35],
            'signal_window': [6, 8, 9, 10, 12]
        }
        
        # Ensure short < long
        valid_combinations = []
        for params in ParameterGrid(macd_params):
            if params['short_window'] < params['long_window']:
                valid_combinations.append(params)
        
        best_params = None
        best_score = -float('inf')
        results = []
        
        for params in valid_combinations:
            try:
                # Calculate MACD with current parameters
                macd_line, signal_line, histogram = self._calculate_macd(df, **params)
                
                # Generate signals based on MACD
                signals = self._generate_macd_signals(macd_line, signal_line, histogram)
                
                # Calculate performance metrics
                performance = self._calculate_signal_performance(df['Close'], signals)
                
                # Use Sharpe ratio for optimization
                score = performance['sharpe_ratio'] if performance['sharpe_ratio'] != -float('inf') else -100
                
                results.append({
                    'params': params,
                    'score': score,
                    'performance': performance
                })
                
                if score > best_score:
                    best_score = score
                    best_params = params
                    
            except Exception as e:
                logger.warning(f"Error testing MACD params {params}: {str(e)}")
                continue
        
        optimization_result = {
            'best_params': best_params or self.default_parameters['macd'],
            'best_score': best_score,
            'all_results': results,
            'optimization_type': 'MACD'
        }
        
        # Store optimization history
        self.optimization_history[f"{symbol}_macd"] = optimization_result
        
        logger.info(f"MACD optimization completed for {symbol}. Best params: {best_params}, Score: {best_score:.3f}")
        
        return optimization_result
    
    def _calculate_rsi(self, df: pd.DataFrame, window: int = 14) -> pd.Series:
        """Calculate RSI with custom window"""
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(self, df: pd.DataFrame, short_window: int = 12, 
                       long_window: int = 26, signal_window: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Calculate MACD with custom parameters"""
        exp1 = df['Close'].ewm(span=short_window).mean()
        exp2 = df['Close'].ewm(span=long_window).mean()
        macd_line = exp1 - exp2
        signal_line = macd_line.ewm(span=signal_window).mean()
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram
    
    def _generate_rsi_signals(self, rsi: pd.Series, oversold: float = 30, overbought: float = 70) -> pd.Series:
        """Generate trading signals based on RSI"""
        signals = pd.Series(0, index=rsi.index)
        
        # Buy signal when RSI crosses above oversold
        buy_signals = (rsi > oversold) & (rsi.shift(1) <= oversold)
        signals[buy_signals] = 1
        
        # Sell signal when RSI crosses below overbought
        sell_signals = (rsi < overbought) & (rsi.shift(1) >= overbought)
        signals[sell_signals] = -1
        
        return signals
    
    def _generate_macd_signals(self, macd_line: pd.Series, signal_line: pd.Series, 
                             histogram: pd.Series) -> pd.Series:
        """Generate trading signals based on MACD"""
        signals = pd.Series(0, index=macd_line.index)
        
        # Buy signal when MACD crosses above signal line
        buy_signals = (macd_line > signal_line) & (macd_line.shift(1) <= signal_line.shift(1))
        signals[buy_signals] = 1
        
        # Sell signal when MACD crosses below signal line
        sell_signals = (macd_line < signal_line) & (macd_line.shift(1) >= signal_line.shift(1))
        signals[sell_signals] = -1
        
        return signals
    
    def _calculate_signal_performance(self, prices: pd.Series, signals: pd.Series) -> Dict[str, float]:
        """Calculate performance metrics for trading signals"""
        try:
            # Calculate returns
            returns = prices.pct_change().dropna()
            
            # Align signals with returns
            aligned_signals = signals.shift(1).reindex(returns.index, fill_value=0)
            
            # Calculate strategy returns (signal * next day return)
            strategy_returns = aligned_signals * returns
            
            # Performance metrics
            total_return = (1 + strategy_returns).prod() - 1
            annual_return = (1 + strategy_returns.mean()) ** 252 - 1
            
            # Risk metrics
            volatility = strategy_returns.std() * np.sqrt(252)
            sharpe_ratio = annual_return / volatility if volatility != 0 else -float('inf')
            
            # Win rate
            winning_trades = (strategy_returns > 0).sum()
            total_trades = (strategy_returns != 0).sum()
            win_rate = winning_trades / total_trades if total_trades > 0 else 0
            
            # Maximum drawdown
            cumulative = (1 + strategy_returns).cumprod()
            running_max = cumulative.expanding().max()
            drawdown = (cumulative - running_max) / running_max
            max_drawdown = drawdown.min()
            
            return {
                'total_return': total_return,
                'annual_return': annual_return,
                'volatility': volatility,
                'sharpe_ratio': sharpe_ratio,
                'win_rate': win_rate,
                'max_drawdown': max_drawdown,
                'total_trades': total_trades
            }
            
        except Exception as e:
            logger.error(f"Error calculating signal performance: {str(e)}")
            return {
                'total_return': -float('inf'),
                'sharpe_ratio': -float('inf'),
                'win_rate': 0,
                'max_drawdown': -1
            }


class AdvancedTechnicalIndicators:
    """
    Advanced technical indicators for enhanced analysis
    """
    
    def __init__(self):
        self.indicators_cache = {}
    
    def calculate_williams_r(self, df: pd.DataFrame, window: int = 14) -> pd.Series:
        """
        Calculate Williams %R indicator
        """
        high_14 = df['High'].rolling(window=window).max()
        low_14 = df['Low'].rolling(window=window).min()
        williams_r = -100 * ((high_14 - df['Close']) / (high_14 - low_14))
        return williams_r
    
    def calculate_stochastic_oscillator(self, df: pd.DataFrame, k_window: int = 14, d_window: int = 3) -> Tuple[pd.Series, pd.Series]:
        """
        Calculate Stochastic Oscillator
        """
        high_k = df['High'].rolling(window=k_window).max()
        low_k = df['Low'].rolling(window=k_window).min()
        
        # %K calculation
        k_percent = 100 * ((df['Close'] - low_k) / (high_k - low_k))
        
        # %D calculation (smoothed %K)
        d_percent = k_percent.rolling(window=d_window).mean()
        
        return k_percent, d_percent
    
    def calculate_commodity_channel_index(self, df: pd.DataFrame, window: int = 20) -> pd.Series:
        """
        Calculate Commodity Channel Index (CCI)
        """
        # Typical Price
        tp = (df['High'] + df['Low'] + df['Close']) / 3
        
        # Simple Moving Average of TP
        sma_tp = tp.rolling(window=window).mean()
        
        # Mean Deviation
        mad = tp.rolling(window=window).apply(lambda x: np.abs(x - x.mean()).mean(), raw=True)
        
        # CCI
        cci = (tp - sma_tp) / (0.015 * mad)
        return cci
    
    def calculate_money_flow_index(self, df: pd.DataFrame, window: int = 14) -> pd.Series:
        """
        Calculate Money Flow Index (MFI)
        """
        # Typical Price
        tp = (df['High'] + df['Low'] + df['Close']) / 3
        
        # Raw Money Flow
        money_flow = tp * df['Volume']
        
        # Positive and Negative Money Flow
        positive_flow = money_flow.where(tp > tp.shift(), 0)
        negative_flow = money_flow.where(tp < tp.shift(), 0)
        
        # Money Flow Ratios
        positive_mf = positive_flow.rolling(window=window).sum()
        negative_mf = negative_flow.rolling(window=window).sum()
        
        mfi_ratio = positive_mf / negative_mf
        mfi = 100 - (100 / (1 + mfi_ratio))
        
        return mfi
    
    def calculate_ichimoku_cloud(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        """
        Calculate Ichimoku Cloud components
        """
        # Tenkan-sen (Conversion Line)
        tenkan_sen = (df['High'].rolling(window=9).max() + df['Low'].rolling(window=9).min()) / 2
        
        # Kijun-sen (Base Line)
        kijun_sen = (df['High'].rolling(window=26).max() + df['Low'].rolling(window=26).min()) / 2
        
        # Senkou Span A (Leading Span A)
        senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)
        
        # Senkou Span B (Leading Span B)
        senkou_span_b = ((df['High'].rolling(window=52).max() + df['Low'].rolling(window=52).min()) / 2).shift(26)
        
        # Chikou Span (Lagging Span)
        chikou_span = df['Close'].shift(-26)
        
        return {
            'tenkan_sen': tenkan_sen,
            'kijun_sen': kijun_sen,
            'senkou_span_a': senkou_span_a,
            'senkou_span_b': senkou_span_b,
            'chikou_span': chikou_span
        }
    
    def calculate_atr(self, df: pd.DataFrame, window: int = 14) -> pd.Series:
        """
        Calculate Average True Range (ATR)
        """
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())
        
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = true_range.rolling(window=window).mean()
        
        return atr
    
    def calculate_adx(self, df: pd.DataFrame, window: int = 14) -> Dict[str, pd.Series]:
        """
        Calculate Average Directional Index (ADX)
        """
        # True Range
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        
        # Directional Movement
        up_move = df['High'] - df['High'].shift()
        down_move = df['Low'].shift() - df['Low']
        
        plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
        minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)
        
        plus_dm = pd.Series(plus_dm, index=df.index)
        minus_dm = pd.Series(minus_dm, index=df.index)
        
        # Smoothed values
        tr_smooth = tr.rolling(window=window).mean()
        plus_dm_smooth = plus_dm.rolling(window=window).mean()
        minus_dm_smooth = minus_dm.rolling(window=window).mean()
        
        # Directional Indicators
        plus_di = 100 * (plus_dm_smooth / tr_smooth)
        minus_di = 100 * (minus_dm_smooth / tr_smooth)
        
        # ADX
        dx = 100 * (np.abs(plus_di - minus_di) / (plus_di + minus_di))
        adx = dx.rolling(window=window).mean()
        
        return {
            'adx': adx,
            'plus_di': plus_di,
            'minus_di': minus_di
        }


class MultiTimeframeAnalyzer:
    """
    Multi-timeframe analysis for better signal confirmation
    """
    
    def __init__(self):
        self.timeframes = {
            'daily': '1D',
            'weekly': '1W',
            'monthly': '1M'
        }
    
    def resample_data(self, df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
        """
        Resample data to different timeframe
        """
        if timeframe == 'weekly':
            agg_dict = {
                'Open': 'first',
                'High': 'max',
                'Low': 'min',
                'Close': 'last',
                'Volume': 'sum'
            }
            return df.resample('W').agg(agg_dict).dropna()
        elif timeframe == 'monthly':
            agg_dict = {
                'Open': 'first',
                'High': 'max',
                'Low': 'min',
                'Close': 'last',
                'Volume': 'sum'
            }
            return df.resample('M').agg(agg_dict).dropna()
        else:
            return df
    
    def analyze_multiple_timeframes(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Analyze multiple timeframes
        """
        results = {}
        
        for tf_name, tf_code in self.timeframes.items():
            if tf_name == 'daily':
                results[tf_name] = df.copy()
            else:
                results[tf_name] = self.resample_data(df, tf_name)
        
        return results
    
    def get_trend_consensus(self, multi_tf_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Get trend consensus across multiple timeframes
        """
        consensus = {
            'daily_trend': None,
            'weekly_trend': None,
            'monthly_trend': None,
            'overall_consensus': None,
            'strength': 0
        }
        
        trends = []
        weights = []
        
        for tf_name, data in multi_tf_data.items():
            if len(data) >= 20:  # Minimum data for trend analysis
                # Simple trend analysis: compare current price to moving average
                current_price = data['Close'].iloc[-1]
                ma_20 = data['Close'].rolling(20).mean().iloc[-1]
                
                if current_price > ma_20 * 1.02:  # 2% above MA
                    trend = 1  # Bullish
                elif current_price < ma_20 * 0.98:  # 2% below MA
                    trend = -1  # Bearish
                else:
                    trend = 0  # Neutral
                
                consensus[f'{tf_name}_trend'] = trend
                trends.append(trend)
                
                # Weight longer timeframes more heavily
                if tf_name == 'monthly':
                    weights.append(3)
                elif tf_name == 'weekly':
                    weights.append(2)
                else:
                    weights.append(1)
        
        # Calculate weighted consensus
        if trends and weights:
            weighted_score = sum(t * w for t, w in zip(trends, weights)) / sum(weights)
            
            if weighted_score > 0.3:
                consensus['overall_consensus'] = 'bullish'
            elif weighted_score < -0.3:
                consensus['overall_consensus'] = 'bearish'
            else:
                consensus['overall_consensus'] = 'neutral'
            
            consensus['strength'] = abs(weighted_score)
        
        return consensus


def perform_advanced_technical_analysis(df: pd.DataFrame, symbol: str, 
                                    optimize_params: bool = True) -> Dict[str, Any]:
    """
    Perform comprehensive advanced technical analysis
    
    Args:
        df: OHLCV DataFrame
        symbol: Stock symbol
        optimize_params: Whether to optimize parameters
        
    Returns:
        Dictionary with all advanced technical analysis results
    """
    logger.info(f"Starting advanced technical analysis for {symbol}")
    
    results = {
        'symbol': symbol,
        'timestamp': pd.Timestamp.now().isoformat(),
        'optimized_parameters': {},
        'advanced_indicators': {},
        'multi_timeframe_analysis': {},
        'signal_consensus': {}
    }
    
    try:
        # Initialize analyzers
        optimizer = DynamicParameterOptimizer()
        advanced_indicators = AdvancedTechnicalIndicators()
        multi_tf_analyzer = MultiTimeframeAnalyzer()
        
        # Parameter Optimization (if enabled)
        if optimize_params and len(df) > 252:  # Need at least 1 year of data
            logger.info("Optimizing technical indicator parameters...")
            
            # Optimize RSI
            rsi_optimization = optimizer.optimize_rsi_parameters(df, symbol)
            results['optimized_parameters']['rsi'] = rsi_optimization['best_params']
            
            # Optimize MACD
            macd_optimization = optimizer.optimize_macd_parameters(df, symbol)
            results['optimized_parameters']['macd'] = macd_optimization['best_params']
        else:
            # Use default parameters
            results['optimized_parameters'] = optimizer.default_parameters
            logger.info("Using default technical indicator parameters")
        
        # Calculate Advanced Indicators
        logger.info("Calculating advanced technical indicators...")
        
        # Williams %R
        williams_r = advanced_indicators.calculate_williams_r(df)
        results['advanced_indicators']['williams_r'] = williams_r
        
        # Stochastic Oscillator
        stoch_k, stoch_d = advanced_indicators.calculate_stochastic_oscillator(df)
        results['advanced_indicators']['stochastic_k'] = stoch_k
        results['advanced_indicators']['stochastic_d'] = stoch_d
        
        # Commodity Channel Index
        cci = advanced_indicators.calculate_commodity_channel_index(df)
        results['advanced_indicators']['cci'] = cci
        
        # Money Flow Index
        mfi = advanced_indicators.calculate_money_flow_index(df)
        results['advanced_indicators']['mfi'] = mfi
        
        # Ichimoku Cloud
        ichimoku = advanced_indicators.calculate_ichimoku_cloud(df)
        results['advanced_indicators']['ichimoku'] = ichimoku
        
        # ATR
        atr = advanced_indicators.calculate_atr(df)
        results['advanced_indicators']['atr'] = atr
        
        # ADX
        adx_components = advanced_indicators.calculate_adx(df)
        results['advanced_indicators']['adx'] = adx_components
        
        # Multi-Timeframe Analysis
        logger.info("Performing multi-timeframe analysis...")
        multi_tf_data = multi_tf_analyzer.analyze_multiple_timeframes(df)
        results['multi_timeframe_analysis'] = multi_tf_data
        
        # Trend Consensus
        consensus = multi_tf_analyzer.get_trend_consensus(multi_tf_data)
        results['signal_consensus'] = consensus
        
        logger.info(f"Advanced technical analysis completed for {symbol}")
        
    except Exception as e:
        logger.error(f"Error in advanced technical analysis for {symbol}: {str(e)}")
        results['error'] = str(e)
    
    return results
