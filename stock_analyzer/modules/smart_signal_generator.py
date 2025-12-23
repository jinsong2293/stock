"""
Smart Signal Generation Module
Provides multi-signal confirmation and intelligent signal filtering
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class SignalType(Enum):
    """Signal types for classification"""
    BUY = 1
    SELL = -1
    HOLD = 0

class SignalStrength(Enum):
    """Signal strength levels"""
    VERY_WEAK = 1
    WEAK = 2
    MODERATE = 3
    STRONG = 4
    VERY_STRONG = 5

@dataclass
class TradingSignal:
    """Trading signal data structure"""
    timestamp: pd.Timestamp
    signal_type: SignalType
    strength: SignalStrength
    confidence: float
    source: str
    details: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for easier handling"""
        return {
            'timestamp': self.timestamp,
            'signal_type': self.signal_type.value,
            'strength': self.strength.value,
            'confidence': self.confidence,
            'source': self.source,
            'details': self.details
        }

class MultiSignalConfirmation:
    """
    Multi-signal confirmation system to reduce false signals
    """
    
    def __init__(self):
        self.signal_weights = {
            'rsi': 1.5,
            'macd': 1.8,
            'bollinger': 1.2,
            'williams': 1.0,
            'stochastic': 1.3,
            'cci': 0.8,
            'mfi': 1.1,
            'volume': 1.4
        }
        self.confirmation_threshold = 0.6  # 60% agreement for signal confirmation
        
    def generate_rsi_signals(self, df: pd.DataFrame, rsi_params: Dict[str, int]) -> List[TradingSignal]:
        """Generate signals from RSI with confirmation logic"""
        signals = []
        
        if 'RSI' not in df.columns:
            return signals
        
        rsi_window = rsi_params.get('window', 14)
        rsi = df['RSI']
        
        for i in range(1, len(rsi)):
            if pd.isna(rsi.iloc[i]) or pd.isna(rsi.iloc[i-1]):
                continue
            
            current_rsi = rsi.iloc[i]
            prev_rsi = rsi.iloc[i-1]
            timestamp = df.index[i]
            
            # Oversold bounce (buy signal)
            if prev_rsi <= 30 and current_rsi > 30:
                strength = self._calculate_rsi_strength(current_rsi, 'buy')
                confidence = self._calculate_rsi_confidence(current_rsi, strength)
                
                signal = TradingSignal(
                    timestamp=timestamp,
                    signal_type=SignalType.BUY,
                    strength=strength,
                    confidence=confidence,
                    source='RSI',
                    details={
                        'rsi_value': current_rsi,
                        'rsi_window': rsi_window,
                        'oversold_level': 30,
                        'signal_type': 'oversold_bounce'
                    }
                )
                signals.append(signal)
            
            # Overbought reversal (sell signal)
            elif prev_rsi >= 70 and current_rsi < 70:
                strength = self._calculate_rsi_strength(current_rsi, 'sell')
                confidence = self._calculate_rsi_confidence(current_rsi, strength)
                
                signal = TradingSignal(
                    timestamp=timestamp,
                    signal_type=SignalType.SELL,
                    strength=strength,
                    confidence=confidence,
                    source='RSI',
                    details={
                        'rsi_value': current_rsi,
                        'rsi_window': rsi_window,
                        'overbought_level': 70,
                        'signal_type': 'overbought_reversal'
                    }
                )
                signals.append(signal)
        
        return signals
    
    def generate_macd_signals(self, df: pd.DataFrame, macd_params: Dict[str, int]) -> List[TradingSignal]:
        """Generate signals from MACD with confirmation logic"""
        signals = []
        
        required_cols = ['MACD', 'MACD_Signal', 'MACD_Hist']
        if not all(col in df.columns for col in required_cols):
            return signals
        
        macd = df['MACD']
        signal_line = df['MACD_Signal']
        histogram = df['MACD_Hist']
        
        for i in range(1, len(macd)):
            if any(pd.isna([macd.iloc[i], macd.iloc[i-1], signal_line.iloc[i], signal_line.iloc[i-1]])):
                continue
            
            timestamp = df.index[i]
            
            # Bullish crossover (buy signal)
            if (macd.iloc[i-1] <= signal_line.iloc[i-1] and 
                macd.iloc[i] > signal_line.iloc[i] and 
                histogram.iloc[i] > 0):
                
                strength = self._calculate_macd_strength(histogram.iloc[i], 'buy')
                confidence = self._calculate_macd_confidence(histogram.iloc[i], strength)
                
                signal = TradingSignal(
                    timestamp=timestamp,
                    signal_type=SignalType.BUY,
                    strength=strength,
                    confidence=confidence,
                    source='MACD',
                    details={
                        'macd_value': macd.iloc[i],
                        'signal_value': signal_line.iloc[i],
                        'histogram_value': histogram.iloc[i],
                        'signal_type': 'bullish_crossover',
                        'parameters': macd_params
                    }
                )
                signals.append(signal)
            
            # Bearish crossover (sell signal)
            elif (macd.iloc[i-1] >= signal_line.iloc[i-1] and 
                  macd.iloc[i] < signal_line.iloc[i] and 
                  histogram.iloc[i] < 0):
                
                strength = self._calculate_macd_strength(histogram.iloc[i], 'sell')
                confidence = self._calculate_macd_confidence(histogram.iloc[i], strength)
                
                signal = TradingSignal(
                    timestamp=timestamp,
                    signal_type=SignalType.SELL,
                    strength=strength,
                    confidence=confidence,
                    source='MACD',
                    details={
                        'macd_value': macd.iloc[i],
                        'signal_value': signal_line.iloc[i],
                        'histogram_value': histogram.iloc[i],
                        'signal_type': 'bearish_crossover',
                        'parameters': macd_params
                    }
                )
                signals.append(signal)
        
        return signals
    
    def generate_bollinger_signals(self, df: pd.DataFrame, bb_params: Dict[str, Any]) -> List[TradingSignal]:
        """Generate signals from Bollinger Bands"""
        signals = []
        
        required_cols = ['Close', 'BB_Upper', 'BB_Middle', 'BB_Lower']
        if not all(col in df.columns for col in required_cols):
            return signals
        
        close = df['Close']
        upper = df['BB_Upper']
        middle = df['BB_Middle']
        lower = df['BB_Lower']
        
        for i in range(1, len(close)):
            if any(pd.isna([close.iloc[i], upper.iloc[i], lower.iloc[i], 
                           close.iloc[i-1], upper.iloc[i-1], lower.iloc[i-1]])):
                continue
            
            timestamp = df.index[i]
            current_close = close.iloc[i]
            prev_close = close.iloc[i-1]
            
            # Bounce from lower band (buy signal)
            if (prev_close <= lower.iloc[i-1] and current_close > lower.iloc[i] and
                current_close < middle.iloc[i]):  # Still below middle band
                
                bb_width = (upper.iloc[i] - lower.iloc[i]) / middle.iloc[i]
                strength = self._calculate_bb_strength(bb_width, 'buy')
                confidence = self._calculate_bb_confidence(current_close, lower.iloc[i], middle.iloc[i])
                
                signal = TradingSignal(
                    timestamp=timestamp,
                    signal_type=SignalType.BUY,
                    strength=strength,
                    confidence=confidence,
                    source='Bollinger',
                    details={
                        'close_price': current_close,
                        'lower_band': lower.iloc[i],
                        'middle_band': middle.iloc[i],
                        'upper_band': upper.iloc[i],
                        'bb_width': bb_width,
                        'signal_type': 'lower_band_bounce'
                    }
                )
                signals.append(signal)
            
            # Rejection from upper band (sell signal)
            elif (prev_close >= upper.iloc[i-1] and current_close < upper.iloc[i] and
                  current_close > middle.iloc[i]):  # Still above middle band
                
                bb_width = (upper.iloc[i] - lower.iloc[i]) / middle.iloc[i]
                strength = self._calculate_bb_strength(bb_width, 'sell')
                confidence = self._calculate_bb_confidence(current_close, upper.iloc[i], middle.iloc[i])
                
                signal = TradingSignal(
                    timestamp=timestamp,
                    signal_type=SignalType.SELL,
                    strength=strength,
                    confidence=confidence,
                    source='Bollinger',
                    details={
                        'close_price': current_close,
                        'upper_band': upper.iloc[i],
                        'middle_band': middle.iloc[i],
                        'lower_band': lower.iloc[i],
                        'bb_width': bb_width,
                        'signal_type': 'upper_band_rejection'
                    }
                )
                signals.append(signal)
        
        return signals
    
    def generate_volume_confirmation_signals(self, df: pd.DataFrame, signals: List[TradingSignal]) -> List[TradingSignal]:
        """Add volume confirmation to existing signals"""
        if 'Volume' not in df.columns:
            return signals
        
        confirmed_signals = []
        
        for signal in signals:
            # Get volume data around signal time
            signal_time = signal.timestamp
            if signal_time not in df.index:
                confirmed_signals.append(signal)
                continue
            
            # Calculate volume metrics
            volume_20 = df['Volume'].rolling(20).mean()
            current_volume = df.loc[signal_time, 'Volume']
            avg_volume = volume_20.loc[signal_time] if not pd.isna(volume_20.loc[signal_time]) else df['Volume'].mean()
            
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
            
            # Confirm signal if volume is above average
            if volume_ratio >= 1.2:  # 20% above average volume
                signal.details['volume_confirmation'] = True
                signal.details['volume_ratio'] = volume_ratio
                signal.confidence = min(1.0, signal.confidence * 1.1)  # Boost confidence
            else:
                signal.details['volume_confirmation'] = False
                signal.details['volume_ratio'] = volume_ratio
                signal.confidence = signal.confidence * 0.9  # Reduce confidence
            
            confirmed_signals.append(signal)
        
        return confirmed_signals
    
    def consolidate_signals(self, all_signals: List[TradingSignal]) -> List[TradingSignal]:
        """
        Consolidate multiple signals into confirmed signals
        """
        if not all_signals:
            return []
        
        # Group signals by date (allowing for small time differences)
        signal_groups = self._group_signals_by_time(all_signals)
        
        consolidated_signals = []
        
        for date, group_signals in signal_groups.items():
            if len(group_signals) == 1:
                # Single signal - lower confidence
                signal = group_signals[0]
                signal.confidence *= 0.7
                consolidated_signals.append(signal)
            else:
                # Multiple signals - analyze consensus
                consensus_signal = self._create_consensus_signal(group_signals)
                if consensus_signal:
                    consolidated_signals.append(consensus_signal)
        
        return sorted(consolidated_signals, key=lambda x: x.timestamp)
    
    def _group_signals_by_time(self, signals: List[TradingSignal]) -> Dict[pd.Timestamp, List[TradingSignal]]:
        """Group signals occurring close in time"""
        groups = {}
        
        for signal in signals:
            # Round to nearest day for grouping
            date_key = signal.timestamp.normalize()
            
            if date_key not in groups:
                groups[date_key] = []
            groups[date_key].append(signal)
        
        return groups
    
    def _create_consensus_signal(self, signals: List[TradingSignal]) -> Optional[TradingSignal]:
        """Create consensus signal from multiple signals"""
        if not signals:
            return None
        
        # Count buy vs sell signals
        buy_signals = [s for s in signals if s.signal_type == SignalType.BUY]
        sell_signals = [s for s in signals if s.signal_type == SignalType.SELL]
        
        # Determine consensus direction
        if len(buy_signals) > len(sell_signals):
            consensus_type = SignalType.BUY
            relevant_signals = buy_signals
        elif len(sell_signals) > len(buy_signals):
            consensus_type = SignalType.SELL
            relevant_signals = sell_signals
        else:
            # Tie - no consensus
            return None
        
        # Calculate weighted confidence
        total_weight = 0
        weighted_confidence = 0
        
        for signal in relevant_signals:
            weight = self.signal_weights.get(signal.source.lower(), 1.0)
            total_weight += weight
            weighted_confidence += signal.confidence * weight
        
        consensus_confidence = weighted_confidence / total_weight if total_weight > 0 else 0
        
        # Determine strength based on confidence
        if consensus_confidence >= 0.8:
            strength = SignalStrength.VERY_STRONG
        elif consensus_confidence >= 0.65:
            strength = SignalStrength.STRONG
        elif consensus_confidence >= 0.5:
            strength = SignalStrength.MODERATE
        elif consensus_confidence >= 0.35:
            strength = SignalStrength.WEAK
        else:
            strength = SignalStrength.VERY_WEAK
        
        # Boost confidence for multiple confirmations
        confirmation_boost = min(0.2, len(relevant_signals) * 0.05)
        final_confidence = min(1.0, consensus_confidence + confirmation_boost)
        
        # Only return if confidence meets threshold
        if final_confidence < self.confirmation_threshold:
            return None
        
        # Create consensus signal
        consensus_signal = TradingSignal(
            timestamp=signals[0].timestamp,  # Use first signal timestamp
            signal_type=consensus_type,
            strength=strength,
            confidence=final_confidence,
            source='CONSENSUS',
            details={
                'consensus_type': f'{len(relevant_signals)}/{len(signals)} signals agree',
                'contributing_sources': [s.source for s in relevant_signals],
                'individual_signals': [s.to_dict() for s in signals],
                'confirmation_boost': confirmation_boost,
                'weighted_confidence': consensus_confidence
            }
        )
        
        return consensus_signal
    
    def _calculate_rsi_strength(self, rsi_value: float, signal_type: str) -> SignalStrength:
        """Calculate signal strength based on RSI value"""
        if signal_type == 'buy':
            if rsi_value < 20:
                return SignalStrength.VERY_STRONG
            elif rsi_value < 25:
                return SignalStrength.STRONG
            elif rsi_value < 30:
                return SignalStrength.MODERATE
            else:
                return SignalStrength.WEAK
        else:  # sell signal
            if rsi_value > 80:
                return SignalStrength.VERY_STRONG
            elif rsi_value > 75:
                return SignalStrength.STRONG
            elif rsi_value > 70:
                return SignalStrength.MODERATE
            else:
                return SignalStrength.WEAK
    
    def _calculate_rsi_confidence(self, rsi_value: float, strength: SignalStrength) -> float:
        """Calculate confidence based on RSI value and strength"""
        base_confidence = 0.5
        
        # Adjust based on extreme levels
        if signal_type == 'buy':
            if rsi_value < 15:
                base_confidence = 0.85
            elif rsi_value < 20:
                base_confidence = 0.75
            elif rsi_value < 25:
                base_confidence = 0.65
        else:  # sell signal
            if rsi_value > 85:
                base_confidence = 0.85
            elif rsi_value > 80:
                base_confidence = 0.75
            elif rsi_value > 75:
                base_confidence = 0.65
        
        # Adjust based on strength
        strength_multiplier = strength.value / 5.0  # Normalize to 0-1
        final_confidence = base_confidence * strength_multiplier
        
        return min(1.0, final_confidence)
    
    def _calculate_macd_strength(self, histogram_value: float, signal_type: str) -> SignalStrength:
        """Calculate signal strength based on MACD histogram"""
        abs_histogram = abs(histogram_value)
        
        if abs_histogram > 0.5:  # Strong momentum
            return SignalStrength.VERY_STRONG
        elif abs_histogram > 0.3:
            return SignalStrength.STRONG
        elif abs_histogram > 0.15:
            return SignalStrength.MODERATE
        elif abs_histogram > 0.05:
            return SignalStrength.WEAK
        else:
            return SignalStrength.VERY_WEAK
    
    def _calculate_macd_confidence(self, histogram_value: float, strength: SignalStrength) -> float:
        """Calculate confidence based on MACD histogram"""
        abs_histogram = abs(histogram_value)
        
        # Base confidence on histogram magnitude
        base_confidence = min(0.8, abs_histogram * 2)
        
        # Adjust based on strength
        strength_multiplier = strength.value / 5.0
        final_confidence = base_confidence * strength_multiplier
        
        return min(1.0, final_confidence)
    
    def _calculate_bb_strength(self, bb_width: float, signal_type: str) -> SignalStrength:
        """Calculate signal strength based on Bollinger Band width"""
        # Narrow bands suggest stronger signals
        if bb_width < 0.05:  # Very narrow bands
            return SignalStrength.VERY_STRONG
        elif bb_width < 0.08:
            return SignalStrength.STRONG
        elif bb_width < 0.12:
            return SignalStrength.MODERATE
        elif bb_width < 0.15:
            return SignalStrength.WEAK
        else:
            return SignalStrength.VERY_WEAK
    
    def _calculate_bb_confidence(self, price: float, band: float, middle: float) -> float:
        """Calculate confidence based on position relative to bands"""
        distance_from_band = abs(price - band) / middle
        
        # Closer to band = higher confidence
        if distance_from_band < 0.01:
            base_confidence = 0.8
        elif distance_from_band < 0.02:
            base_confidence = 0.7
        elif distance_from_band < 0.03:
            base_confidence = 0.6
        else:
            base_confidence = 0.5
        
        return min(1.0, base_confidence)


class RiskAdjustedPositionSizing:
    """
    Risk-adjusted position sizing for optimal risk management
    """
    
    def __init__(self):
        self.default_risk_per_trade = 0.02  # 2% risk per trade
        self.max_position_size = 0.1  # Maximum 10% of portfolio
    
    def calculate_position_size(self, account_balance: float, entry_price: float, 
                           stop_loss: float, risk_per_trade: Optional[float] = None) -> int:
        """
        Calculate optimal position size based on risk management
        
        Args:
            account_balance: Total account balance
            entry_price: Entry price for the trade
            stop_loss: Stop loss price
            risk_per_trade: Risk percentage per trade (default 2%)
            
        Returns:
            Position size in shares
        """
        if risk_per_trade is None:
            risk_per_trade = self.default_risk_per_trade
        
        # Calculate risk amount
        risk_amount = account_balance * risk_per_trade
        
        # Calculate price risk per share
        price_risk = abs(entry_price - stop_loss)
        
        if price_risk <= 0:
            return 0
        
        # Calculate position size based on risk
        position_size = int(risk_amount / price_risk)
        
        # Apply maximum position size limit
        max_position_value = account_balance * self.max_position_size
        max_shares = int(max_position_value / entry_price)
        
        return min(position_size, max_shares)
    
    def calculate_dynamic_stop_loss(self, df: pd.DataFrame, signal_type: SignalType, 
                                 atr_period: int = 14) -> Tuple[float, float]:
        """
        Calculate dynamic stop loss based on ATR
        
        Args:
            df: Price data with ATR
            signal_type: BUY or SELL signal
            atr_period: ATR calculation period
            
        Returns:
            Tuple of (stop_loss_price, take_profit_price)
        """
        if 'ATR' not in df.columns:
            return None, None
        
        current_price = df['Close'].iloc[-1]
        atr = df['ATR'].iloc[-1]
        
        # Use 2x ATR for stop loss
        stop_distance = 2 * atr
        
        # Use 3x ATR for take profit (1.5:1 risk-reward)
        profit_distance = 3 * atr
        
        if signal_type == SignalType.BUY:
            stop_loss = current_price - stop_distance
            take_profit = current_price + profit_distance
        else:  # SELL signal
            stop_loss = current_price + stop_distance
            take_profit = current_price - profit_distance
        
        return stop_loss, take_profit
    
    def calculate_portfolio_risk_metrics(self, positions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate portfolio-level risk metrics
        
        Args:
            positions: List of position dictionaries
            
        Returns:
            Dictionary with risk metrics
        """
        if not positions:
            return {
                'total_value': 0,
                'total_risk': 0,
                'portfolio_beta': 0,
                'concentration_risk': 0,
                'recommendations': []
            }
        
        total_value = sum(pos.get('value', 0) for pos in positions)
        total_risk_amount = sum(pos.get('risk_amount', 0) for pos in positions)
        
        # Calculate concentration risk
        position_weights = [pos.get('value', 0) / total_value for pos in positions]
        concentration_risk = max(position_weights)
        
        # Generate recommendations
        recommendations = []
        if concentration_risk > 0.2:
            recommendations.append("High concentration risk - consider diversifying")
        
        if total_risk_amount / total_value > 0.1:
            recommendations.append("Portfolio risk is high - consider reducing position sizes")
        
        return {
            'total_value': total_value,
            'total_risk_amount': total_risk_amount,
            'portfolio_risk_percentage': (total_risk_amount / total_value) * 100,
            'concentration_risk': concentration_risk,
            'concentration_percentage': concentration_risk * 100,
            'recommendations': recommendations
        }


def generate_smart_signals(df: pd.DataFrame, optimized_params: Dict[str, Any], 
                         symbol: str) -> Dict[str, Any]:
    """
    Generate smart signals with multi-signal confirmation
    
    Args:
        df: Technical analysis DataFrame
        optimized_params: Optimized parameters for indicators
        symbol: Stock symbol
        
    Returns:
        Dictionary with signal analysis results
    """
    logger.info(f"Generating smart signals for {symbol}")
    
    results = {
        'symbol': symbol,
        'timestamp': pd.Timestamp.now().isoformat(),
        'raw_signals': [],
        'confirmed_signals': [],
        'signal_summary': {},
        'risk_metrics': {}
    }
    
    try:
        # Initialize signal generator
        signal_generator = MultiSignalConfirmation()
        
        # Generate signals from different indicators
        all_signals = []
        
        # RSI Signals
        rsi_params = optimized_params.get('rsi', {'window': 14})
        rsi_signals = signal_generator.generate_rsi_signals(df, rsi_params)
        all_signals.extend(rsi_signals)
        
        # MACD Signals
        macd_params = optimized_params.get('macd', {'short_window': 12, 'long_window': 26, 'signal_window': 9})
        macd_signals = signal_generator.generate_macd_signals(df, macd_params)
        all_signals.extend(macd_signals)
        
        # Bollinger Signals
        bb_params = optimized_params.get('bollinger', {'window': 20, 'num_std_dev': 2})
        bb_signals = signal_generator.generate_bollinger_signals(df, bb_params)
        all_signals.extend(bb_signals)
        
        # Add volume confirmation
        volume_confirmed_signals = signal_generator.generate_volume_confirmation_signals(df, all_signals)
        
        # Consolidate signals with confirmation logic
        confirmed_signals = signal_generator.consolidate_signals(volume_confirmed_signals)
        
        # Calculate risk metrics
        position_sizer = RiskAdjustedPositionSizing()
        
        # Get recent signals for risk calculation
        recent_signals = [s for s in confirmed_signals if s.timestamp >= df.index[-30]]  # Last 30 days
        
        if recent_signals:
            last_signal = recent_signals[-1]
            current_price = df['Close'].iloc[-1]
            
            # Calculate dynamic stops
            stop_loss, take_profit = position_sizer.calculate_dynamic_stop_loss(df, last_signal.signal_type)
            
            # Calculate position size (example with 100,000 account)
            example_balance = 100000
            if stop_loss:
                position_size = position_sizer.calculate_position_size(
                    example_balance, current_price, stop_loss
                )
            else:
                position_size = 0
            
            risk_metrics = {
                'last_signal': last_signal.to_dict(),
                'current_price': current_price,
                'suggested_stop_loss': stop_loss,
                'suggested_take_profit': take_profit,
                'suggested_position_size': position_size,
                'risk_amount': example_balance * 0.02 if stop_loss else 0,
                'risk_reward_ratio': 1.5 if stop_loss else None
            }
        else:
            risk_metrics = {
                'last_signal': None,
                'current_price': df['Close'].iloc[-1],
                'suggested_stop_loss': None,
                'suggested_take_profit': None,
                'suggested_position_size': 0,
                'risk_amount': 0,
                'risk_reward_ratio': None
            }
        
        # Signal summary
        signal_summary = {
            'total_signals_generated': len(all_signals),
            'volume_confirmed_signals': len(volume_confirmed_signals),
            'confirmed_signals': len(confirmed_signals),
            'confirmation_rate': len(confirmed_signals) / len(all_signals) if all_signals else 0,
            'signal_distribution': {
                'buy_signals': len([s for s in confirmed_signals if s.signal_type == SignalType.BUY]),
                'sell_signals': len([s for s in confirmed_signals if s.signal_type == SignalType.SELL]),
                'hold_signals': len([s for s in confirmed_signals if s.signal_type == SignalType.HOLD])
            },
            'average_confidence': np.mean([s.confidence for s in confirmed_signals]) if confirmed_signals else 0,
            'strength_distribution': {
                'very_weak': len([s for s in confirmed_signals if s.strength == SignalStrength.VERY_WEAK]),
                'weak': len([s for s in confirmed_signals if s.strength == SignalStrength.WEAK]),
                'moderate': len([s for s in confirmed_signals if s.strength == SignalStrength.MODERATE]),
                'strong': len([s for s in confirmed_signals if s.strength == SignalStrength.STRONG]),
                'very_strong': len([s for s in confirmed_signals if s.strength == SignalStrength.VERY_STRONG])
            }
        }
        
        results.update({
            'raw_signals': [s.to_dict() for s in all_signals],
            'confirmed_signals': [s.to_dict() for s in confirmed_signals],
            'signal_summary': signal_summary,
            'risk_metrics': risk_metrics
        })
        
        logger.info(f"Smart signal generation completed for {symbol}. Generated {len(confirmed_signals)} confirmed signals")
        
    except Exception as e:
        logger.error(f"Error in smart signal generation for {symbol}: {str(e)}")
        results['error'] = str(e)
    
    return results
