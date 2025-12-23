"""
Risk Reward Analyzer - Phân tích rủi ro và lợi nhuận toàn diện
Tính toán VaR, Beta, Volatility, Sharpe Ratio, Maximum Drawdown và các chỉ số rủi ro khác

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
class RiskMetrics:
    """Cấu trúc dữ liệu cho các chỉ số rủi ro"""
    volatility: float           # Standard deviation of returns
    beta: float                 # Market beta
    sharpe_ratio: float         # Risk-adjusted return
    max_drawdown: float         # Maximum peak-to-trough decline
    var_95: float              # Value at Risk (95% confidence)
    var_99: float              # Value at Risk (99% confidence)
    downside_deviation: float   # Downside risk measure
    sortino_ratio: float        # Sortino ratio (downside risk adjusted)
    calmar_ratio: float         # Calmar ratio (return/max drawdown)
    risk_score: int            # Overall risk score (1-10)

@dataclass
class RiskRewardAnalysis:
    """Cấu trúc dữ liệu phân tích rủi ro/lợi nhuận"""
    symbol: str
    current_price: float
    risk_metrics: RiskMetrics
    risk_level: str            # 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH'
    reward_potential: float    # Expected return
    risk_reward_ratio: float
    recommendation: str         # Risk-adjusted recommendation
    key_risks: List[str]
    risk_mitigation: List[str]
    confidence_level: float

class RiskRewardAnalyzer:
    """Phân tích rủi ro và lợi nhuận toàn diện"""
    
    def __init__(self, risk_free_rate: float = 0.06):
        """
        Khởi tạo Risk Reward Analyzer
        
        Args:
            risk_free_rate: Tỷ lệ phi rủi ro (default: 6% - Vietnam 10Y bond)
        """
        self.risk_free_rate = risk_free_rate
        self.logger = logging.getLogger(__name__)
        
        # Risk thresholds for Vietnamese market
        self.risk_thresholds = {
            'volatility': {'low': 0.15, 'medium': 0.25, 'high': 0.35},
            'beta': {'low': 0.8, 'medium': 1.2, 'high': 1.5},
            'var_95': {'low': 0.03, 'medium': 0.05, 'high': 0.08},
            'max_drawdown': {'low': 0.10, 'medium': 0.20, 'high': 0.30}
        }
    
    def calculate_returns(self, price_data: pd.DataFrame) -> pd.Series:
        """Tính toán daily returns"""
        try:
            returns = price_data['Close'].pct_change().dropna()
            return returns
        except Exception as e:
            self.logger.error(f"Error calculating returns: {e}")
            return pd.Series()
    
    def calculate_volatility(self, returns: pd.Series, period: int = 252) -> float:
        """Tính toán volatility (annualized)"""
        try:
            if len(returns) < 2:
                return 0.0
            
            # Calculate annualized volatility
            daily_vol = returns.std()
            annualized_vol = daily_vol * np.sqrt(period)
            return annualized_vol
            
        except Exception as e:
            self.logger.error(f"Error calculating volatility: {e}")
            return 0.0
    
    def calculate_beta(self, stock_returns: pd.Series, market_returns: pd.Series) -> float:
        """Tính toán beta so với thị trường"""
        try:
            if len(stock_returns) < 2 or len(market_returns) < 2:
                return 1.0  # Default beta
            
            # Align the series
            aligned_data = pd.DataFrame({
                'stock': stock_returns,
                'market': market_returns
            }).dropna()
            
            if len(aligned_data) < 10:  # Need minimum data points
                return 1.0
            
            # Calculate covariance and variance
            covariance = aligned_data['stock'].cov(aligned_data['market'])
            market_variance = aligned_data['market'].var()
            
            if market_variance == 0:
                return 1.0
            
            beta = covariance / market_variance
            return beta
            
        except Exception as e:
            self.logger.error(f"Error calculating beta: {e}")
            return 1.0
    
    def calculate_sharpe_ratio(self, returns: pd.Series, period: int = 252) -> float:
        """Tính toán Sharpe Ratio"""
        try:
            if len(returns) < 2:
                return 0.0
            
            # Calculate excess returns
            excess_returns = returns - (self.risk_free_rate / period)
            
            # Calculate Sharpe ratio
            if excess_returns.std() == 0:
                return 0.0
            
            sharpe_ratio = excess_returns.mean() / excess_returns.std() * np.sqrt(period)
            return sharpe_ratio
            
        except Exception as e:
            self.logger.error(f"Error calculating Sharpe ratio: {e}")
            return 0.0
    
    def calculate_max_drawdown(self, price_data: pd.Series) -> float:
        """Tính toán Maximum Drawdown"""
        try:
            if len(price_data) < 2:
                return 0.0
            
            # Calculate cumulative returns
            cumulative = (1 + price_data.pct_change()).cumprod()
            
            # Calculate running maximum
            running_max = cumulative.expanding().max()
            
            # Calculate drawdown
            drawdown = (cumulative - running_max) / running_max
            
            # Return maximum drawdown (most negative value)
            max_drawdown = drawdown.min()
            return abs(max_drawdown)  # Return as positive value
            
        except Exception as e:
            self.logger.error(f"Error calculating max drawdown: {e}")
            return 0.0
    
    def calculate_var(self, returns: pd.Series, confidence_level: float = 0.95) -> float:
        """Tính toán Value at Risk"""
        try:
            if len(returns) < 2:
                return 0.0
            
            # Sort returns in ascending order
            sorted_returns = returns.sort_values()
            
            # Calculate VaR using historical simulation
            var_index = int((1 - confidence_level) * len(sorted_returns))
            
            if var_index >= len(sorted_returns):
                var_index = len(sorted_returns) - 1
            
            var = abs(sorted_returns.iloc[var_index])
            return var
            
        except Exception as e:
            self.logger.error(f"Error calculating VaR: {e}")
            return 0.0
    
    def calculate_downside_deviation(self, returns: pd.Series, target_return: float = 0.0) -> float:
        """Tính toán Downside Deviation"""
        try:
            if len(returns) < 2:
                return 0.0
            
            # Calculate downside returns (returns below target)
            downside_returns = returns[returns < target_return]
            
            if len(downside_returns) == 0:
                return 0.0
            
            # Calculate downside deviation
            downside_deviation = np.sqrt((downside_returns ** 2).mean())
            return downside_deviation
            
        except Exception as e:
            self.logger.error(f"Error calculating downside deviation: {e}")
            return 0.0
    
    def calculate_sortino_ratio(self, returns: pd.Series, period: int = 252) -> float:
        """Tính toán Sortino Ratio"""
        try:
            if len(returns) < 2:
                return 0.0
            
            # Calculate excess returns
            excess_returns = returns - (self.risk_free_rate / period)
            
            # Calculate downside deviation
            downside_deviation = self.calculate_downside_deviation(excess_returns)
            
            if downside_deviation == 0:
                return 0.0
            
            sortino_ratio = excess_returns.mean() / downside_deviation * np.sqrt(period)
            return sortino_ratio
            
        except Exception as e:
            self.logger.error(f"Error calculating Sortino ratio: {e}")
            return 0.0
    
    def calculate_calmar_ratio(self, returns: pd.Series, price_data: pd.Series) -> float:
        """Tính toán Calmar Ratio"""
        try:
            if len(returns) < 2:
                return 0.0
            
            # Calculate annualized return
            total_return = (price_data.iloc[-1] / price_data.iloc[0]) - 1
            years = len(price_data) / 252  # Assuming daily data
            annualized_return = (1 + total_return) ** (1/years) - 1 if years > 0 else 0
            
            # Calculate max drawdown
            max_drawdown = self.calculate_max_drawdown(price_data)
            
            if max_drawdown == 0:
                return 0.0
            
            calmar_ratio = annualized_return / max_drawdown
            return calmar_ratio
            
        except Exception as e:
            self.logger.error(f"Error calculating Calmar ratio: {e}")
            return 0.0
    
    def calculate_risk_score(self, risk_metrics: Dict[str, float]) -> int:
        """Tính toán overall risk score (1-10)"""
        try:
            score = 5  # Base score
            
            # Volatility component (30% weight)
            volatility = risk_metrics.get('volatility', 0)
            if volatility > 0.35:
                score += 2
            elif volatility > 0.25:
                score += 1
            elif volatility < 0.15:
                score -= 1
            
            # Beta component (25% weight)
            beta = risk_metrics.get('beta', 1)
            if beta > 1.5:
                score += 2
            elif beta > 1.2:
                score += 1
            elif beta < 0.8:
                score -= 1
            
            # VaR component (25% weight)
            var_95 = risk_metrics.get('var_95', 0)
            if var_95 > 0.08:
                score += 2
            elif var_95 > 0.05:
                score += 1
            elif var_95 < 0.03:
                score -= 1
            
            # Max Drawdown component (20% weight)
            max_drawdown = risk_metrics.get('max_drawdown', 0)
            if max_drawdown > 0.30:
                score += 2
            elif max_drawdown > 0.20:
                score += 1
            elif max_drawdown < 0.10:
                score -= 1
            
            # Ensure score is between 1 and 10
            score = max(1, min(10, score))
            return score
            
        except Exception as e:
            self.logger.error(f"Error calculating risk score: {e}")
            return 5  # Default medium risk
    
    def determine_risk_level(self, risk_metrics: Dict[str, float]) -> str:
        """Xác định mức độ rủi ro"""
        try:
            risk_score = self.calculate_risk_score(risk_metrics)
            
            if risk_score <= 3:
                return 'LOW'
            elif risk_score <= 5:
                return 'MEDIUM'
            elif risk_score <= 7:
                return 'HIGH'
            else:
                return 'VERY_HIGH'
                
        except Exception as e:
            self.logger.error(f"Error determining risk level: {e}")
            return 'MEDIUM'
    
    def calculate_reward_potential(self, price_data: pd.Series, 
                                 technical_signals: Optional[Dict] = None) -> float:
        """Tính toán tiềm năng lợi nhuận"""
        try:
            if len(price_data) < 20:
                return 0.0
            
            # Calculate momentum indicators
            current_price = price_data.iloc[-1]
            
            # Short-term momentum (5-day)
            short_momentum = (current_price / price_data.iloc[-6] - 1) if len(price_data) >= 6 else 0
            
            # Medium-term momentum (20-day)
            medium_momentum = (current_price / price_data.iloc[-21] - 1) if len(price_data) >= 21 else 0
            
            # Long-term momentum (60-day)
            long_momentum = (current_price / price_data.iloc[-61] - 1) if len(price_data) >= 61 else 0
            
            # Technical signal adjustment
            signal_adjustment = 0
            if technical_signals:
                overall_signal = technical_signals.get('overall_signal', 'HOLD')
                if overall_signal == 'STRONG_BUY':
                    signal_adjustment = 0.15
                elif overall_signal == 'BUY':
                    signal_adjustment = 0.08
                elif overall_signal == 'SELL':
                    signal_adjustment = -0.10
                elif overall_signal == 'STRONG_SELL':
                    signal_adjustment = -0.15
            
            # Weighted momentum
            reward_potential = (short_momentum * 0.5 + medium_momentum * 0.3 + long_momentum * 0.2) + signal_adjustment
            
            # Cap extreme values
            reward_potential = max(-0.5, min(0.5, reward_potential))
            
            return reward_potential
            
        except Exception as e:
            self.logger.error(f"Error calculating reward potential: {e}")
            return 0.0
    
    def identify_key_risks(self, risk_metrics: Dict[str, float], 
                         sector: str = 'Unknown') -> List[str]:
        """Xác định các rủi ro chính"""
        risks = []
        
        try:
            # Volatility risk
            if risk_metrics.get('volatility', 0) > 0.30:
                risks.append("High price volatility")
            
            # Beta risk
            beta = risk_metrics.get('beta', 1)
            if beta > 1.5:
                risks.append("High market sensitivity (Beta > 1.5)")
            elif beta < 0.8:
                risks.append("Low market correlation (Beta < 0.8)")
            
            # VaR risk
            if risk_metrics.get('var_95', 0) > 0.06:
                risks.append("High potential daily loss (VaR > 6%)")
            
            # Drawdown risk
            if risk_metrics.get('max_drawdown', 0) > 0.25:
                risks.append("High maximum drawdown risk")
            
            # Sector-specific risks
            if sector == 'Banking':
                risks.extend([
                    "Interest rate risk",
                    "Credit risk",
                    "Regulatory risk"
                ])
            elif sector == 'Technology':
                risks.extend([
                    "Technology disruption risk",
                    "Competition risk",
                    "Intellectual property risk"
                ])
            elif sector == 'Real Estate':
                risks.extend([
                    "Interest rate sensitivity",
                    "Market cycle risk",
                    "Regulatory policy risk"
                ])
            elif sector == 'Oil & Gas':
                risks.extend([
                    "Commodity price volatility",
                    "Geopolitical risk",
                    "Environmental regulation risk"
                ])
            
        except Exception as e:
            self.logger.error(f"Error identifying key risks: {e}")
        
        return risks
    
    def suggest_risk_mitigation(self, risk_metrics: Dict[str, float], 
                              risk_level: str) -> List[str]:
        """Đề xuất các biện pháp giảm thiểu rủi ro"""
        mitigation = []
        
        try:
            if risk_level in ['HIGH', 'VERY_HIGH']:
                mitigation.append("Consider position sizing (limit to 2-3% of portfolio)")
                mitigation.append("Use stop-loss orders (8-12% below entry)")
            
            if risk_metrics.get('volatility', 0) > 0.25:
                mitigation.append("Dollar-cost average entry strategy")
                mitigation.append("Consider options strategies for downside protection")
            
            if risk_metrics.get('beta', 1) > 1.3:
                mitigation.append("Hedge market exposure with index puts")
                mitigation.append("Reduce position during high market volatility")
            
            if risk_metrics.get('max_drawdown', 0) > 0.20:
                mitigation.append("Implement trailing stops")
                mitigation.append("Regular portfolio rebalancing")
            
            if risk_metrics.get('var_95', 0) > 0.05:
                mitigation.append("Monitor daily VaR limits")
                mitigation.append("Consider reducing position size")
            
            # General recommendations
            mitigation.extend([
                "Diversify across sectors and asset classes",
                "Regular monitoring of key risk metrics",
                "Stay informed about company and sector developments"
            ])
            
        except Exception as e:
            self.logger.error(f"Error suggesting risk mitigation: {e}")
        
        return mitigation
    
    def perform_comprehensive_analysis(self, symbol: str, 
                                     price_data: pd.DataFrame,
                                     market_data: Optional[pd.Series] = None,
                                     sector: str = 'Unknown',
                                     technical_signals: Optional[Dict] = None) -> RiskRewardAnalysis:
        """Thực hiện phân tích rủi ro/lợi nhuận toàn diện"""
        try:
            if price_data.empty or len(price_data) < 10:
                return RiskRewardAnalysis(
                    symbol=symbol,
                    current_price=0,
                    risk_metrics=RiskMetrics(0, 1, 0, 0, 0, 0, 0, 0, 0, 5),
                    risk_level='UNKNOWN',
                    reward_potential=0,
                    risk_reward_ratio=0,
                    recommendation='INSUFFICIENT_DATA',
                    key_risks=['Insufficient price data'],
                    risk_mitigation=['Collect more historical data'],
                    confidence_level=0
                )
            
            current_price = price_data['Close'].iloc[-1]
            
            # Calculate returns
            returns = self.calculate_returns(price_data)
            
            # Calculate risk metrics
            volatility = self.calculate_volatility(returns)
            
            # Calculate beta (using mock market data if not provided)
            if market_data is not None and not market_data.empty:
                market_returns = market_data.pct_change().dropna()
                beta = self.calculate_beta(returns, market_returns)
            else:
                # Use sector-based beta estimation
                sector_betas = {
                    'Banking': 1.1, 'Technology': 1.3, 'Real Estate': 1.2,
                    'Food & Beverage': 0.9, 'Oil & Gas': 1.4, 'Steel': 1.3,
                    'Pharmaceutical': 0.8, 'Securities': 1.5, 'Insurance': 1.0,
                    'Agriculture': 1.1
                }
                beta = sector_betas.get(sector, 1.0)
            
            sharpe_ratio = self.calculate_sharpe_ratio(returns)
            max_drawdown = self.calculate_max_drawdown(price_data['Close'])
            var_95 = self.calculate_var(returns, 0.95)
            var_99 = self.calculate_var(returns, 0.99)
            downside_deviation = self.calculate_downside_deviation(returns)
            sortino_ratio = self.calculate_sortino_ratio(returns)
            calmar_ratio = self.calculate_calmar_ratio(returns, price_data['Close'])
            
            # Compile risk metrics
            risk_metrics_dict = {
                'volatility': volatility,
                'beta': beta,
                'var_95': var_95,
                'var_99': var_99,
                'max_drawdown': max_drawdown,
                'sharpe_ratio': sharpe_ratio,
                'sortino_ratio': sortino_ratio,
                'calmar_ratio': calmar_ratio,
                'downside_deviation': downside_deviation
            }
            
            # Calculate risk score and level
            risk_score = self.calculate_risk_score(risk_metrics_dict)
            risk_level = self.determine_risk_level(risk_metrics_dict)
            
            # Create risk metrics object
            risk_metrics = RiskMetrics(
                volatility=volatility,
                beta=beta,
                sharpe_ratio=sharpe_ratio,
                max_drawdown=max_drawdown,
                var_95=var_95,
                var_99=var_99,
                downside_deviation=downside_deviation,
                sortino_ratio=sortino_ratio,
                calmar_ratio=calmar_ratio,
                risk_score=risk_score
            )
            
            # Calculate reward potential
            reward_potential = self.calculate_reward_potential(price_data['Close'], technical_signals)
            
            # Calculate risk/reward ratio
            risk_reward_ratio = reward_potential / max(volatility, 0.01) if volatility > 0 else 0
            
            # Determine recommendation
            if risk_score <= 3 and reward_potential > 0.1:
                recommendation = 'BUY'
            elif risk_score <= 5 and reward_potential > 0.05:
                recommendation = 'MODERATE_BUY'
            elif risk_score <= 6:
                recommendation = 'HOLD'
            else:
                recommendation = 'AVOID'
            
            # Identify risks and mitigation
            key_risks = self.identify_key_risks(risk_metrics_dict, sector)
            risk_mitigation = self.suggest_risk_mitigation(risk_metrics_dict, risk_level)
            
            # Calculate confidence level
            data_points = len(returns)
            confidence_level = min(0.95, data_points / 252)  # Maximum 95% confidence
            
            result = RiskRewardAnalysis(
                symbol=symbol,
                current_price=current_price,
                risk_metrics=risk_metrics,
                risk_level=risk_level,
                reward_potential=reward_potential,
                risk_reward_ratio=risk_reward_ratio,
                recommendation=recommendation,
                key_risks=key_risks,
                risk_mitigation=risk_mitigation,
                confidence_level=confidence_level
            )
            
            self.logger.info(f"Risk-reward analysis completed for {symbol}: {risk_level} risk, {recommendation} recommendation")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in comprehensive risk-reward analysis for {symbol}: {e}")
            return RiskRewardAnalysis(
                symbol=symbol,
                current_price=0,
                risk_metrics=RiskMetrics(0, 1, 0, 0, 0, 0, 0, 0, 0, 5),
                risk_level='ERROR',
                reward_potential=0,
                risk_reward_ratio=0,
                recommendation='ERROR',
                key_risks=[f"Analysis error: {str(e)}"],
                risk_mitigation=['Fix data and re-run analysis'],
                confidence_level=0
            )

def test_risk_reward_analyzer():
    """Test function cho Risk Reward Analyzer"""
    print("🧪 Testing Risk Reward Analyzer...")
    
    try:
        # Initialize analyzer
        analyzer = RiskRewardAnalyzer()
        
        # Create mock price data
        np.random.seed(42)
        dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
        dates = dates[dates.weekday < 5]  # Remove weekends
        
        # Generate realistic stock price data
        n_days = len(dates)
        returns = np.random.normal(0.0008, 0.02, n_days)  # Daily returns with drift
        prices = [100]  # Starting price
        
        for ret in returns:
            new_price = prices[-1] * (1 + ret)
            prices.append(max(new_price, 50))  # Minimum price
        
        prices = prices[1:]
        
        # Create price DataFrame
        price_data = pd.DataFrame({
            'Date': dates,
            'Close': prices
        })
        price_data.set_index('Date', inplace=True)
        
        # Mock market data
        market_returns = np.random.normal(0.0005, 0.015, n_days)
        market_prices = [1000]
        for ret in market_returns:
            market_prices.append(market_prices[-1] * (1 + ret))
        market_prices = market_prices[1:]
        
        market_data = pd.Series(market_prices, index=dates)
        
        # Perform analysis
        print("🔍 Performing comprehensive risk-reward analysis...")
        result = analyzer.perform_comprehensive_analysis(
            'FPT', price_data, market_data, 'Technology'
        )
        
        # Display results
        print(f"\n📊 Risk-Reward Analysis for {result.symbol}:")
        print(f"   Current Price: {result.current_price:.2f}")
        print(f"   Risk Level: {result.risk_level}")
        print(f"   Recommendation: {result.recommendation}")
        print(f"   Confidence Level: {result.confidence_level:.1%}")
        
        print(f"\n📈 Risk Metrics:")
        metrics = result.risk_metrics
        print(f"   Volatility: {metrics.volatility:.1%}")
        print(f"   Beta: {metrics.beta:.2f}")
        print(f"   Sharpe Ratio: {metrics.sharpe_ratio:.2f}")
        print(f"   Sortino Ratio: {metrics.sortino_ratio:.2f}")
        print(f"   Max Drawdown: {metrics.max_drawdown:.1%}")
        print(f"   VaR (95%): {metrics.var_95:.1%}")
        print(f"   VaR (99%): {metrics.var_99:.1%}")
        print(f"   Calmar Ratio: {metrics.calmar_ratio:.2f}")
        print(f"   Risk Score: {metrics.risk_score}/10")
        
        print(f"\n💰 Reward Analysis:")
        print(f"   Reward Potential: {result.reward_potential:.1%}")
        print(f"   Risk/Reward Ratio: {result.risk_reward_ratio:.2f}")
        
        if result.key_risks:
            print(f"\n⚠️ Key Risks:")
            for risk in result.key_risks[:5]:
                print(f"   - {risk}")
        
        if result.risk_mitigation:
            print(f"\n🛡️ Risk Mitigation:")
            for mitigation in result.risk_mitigation[:5]:
                print(f"   - {mitigation}")
        
        print(f"\n✅ Risk Reward Analyzer test completed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_risk_reward_analyzer()