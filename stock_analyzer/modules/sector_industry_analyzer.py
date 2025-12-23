"""
Advanced Sector & Industry Analysis Engine
Comparative Analysis for Sector Rotation and Relative Strength
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import yfinance as yf
from scipy import stats
import warnings

logger = logging.getLogger(__name__)
warnings.filterwarnings('ignore')

class SectorPerformance(Enum):
    """Sector performance levels"""
    OUTPERFORMING = "outperforming"
    MATCHING = "matching"
    UNDERPERFORMING = "underperforming"
    WEAKEST = "weakest"
    STRONGEST = "strongest"

class RotationSignal(Enum):
    """Sector rotation signals"""
    STRONG_BUY = "strong_buy"
    BUY = "buy"
    HOLD = "hold"
    SELL = "sell"
    STRONG_SELL = "strong_sell"

@dataclass
class SectorData:
    """Sector performance data structure"""
    sector_name: str
    ticker: str
    performance_score: float
    relative_strength: float
    momentum_score: float
    fundamental_score: float
    technical_score: float
    overall_score: float
    rotation_signal: RotationSignal

class SectorIndustryAnalyzer:
    """
    Advanced Sector & Industry Analysis Engine
    Provides comparative analysis for sector rotation and relative strength
    """
    
    def __init__(self):
        self.sector_etfs = self._initialize_sector_etfs()
        self.industry_classifications = self._initialize_industry_classifications()
        self.performance_metrics = self._initialize_performance_metrics()
        self.rotation_criteria = self._initialize_rotation_criteria()
        
    def _initialize_sector_etfs(self) -> Dict[str, str]:
        """
        Initialize sector ETF mappings for analysis
        """
        return {
            # US Sector ETFs (XLP family)
            'technology': 'XLK',
            'healthcare': 'XLV',
            'financials': 'XLF',
            'consumer_discretionary': 'XLY',
            'consumer_staples': 'XLP',
            'energy': 'XLE',
            'industrials': 'XLI',
            'materials': 'XLB',
            'utilities': 'XLU',
            'real_estate': 'XLRE',
            'communication_services': 'XLC',
            
            # Alternative sector classifications
            'banking': 'XLF',
            'pharmaceuticals': 'XLV',
            'semiconductors': 'SOXX',
            'aerospace': 'XLI',
            'retail': 'XLY',
            'oil_gas': 'XLE',
            'telecommunications': 'XLC',
            'insurance': 'XLF',
            'biotechnology': 'IBB',
            'homebuilders': 'XHB'
        }
    
    def _initialize_industry_classifications(self) -> Dict[str, Dict[str, Any]]:
        """
        Initialize industry classification data
        """
        return {
            'technology': {
                'name': 'Technology',
                'description': 'Software, hardware, semiconductors, IT services',
                'growth_profile': 'high_growth',
                'interest_rate_sensitivity': 'medium',
                'economic_sensitivity': 'medium',
                'typical_performance': 'outperform_in_recovery'
            },
            'healthcare': {
                'name': 'Healthcare',
                'description': 'Pharmaceuticals, biotechnology, medical devices',
                'growth_profile': 'moderate_growth',
                'interest_rate_sensitivity': 'low',
                'economic_sensitivity': 'low',
                'typical_performance': 'defensive'
            },
            'financials': {
                'name': 'Financials',
                'description': 'Banks, insurance, asset management, real estate',
                'growth_profile': 'moderate_growth',
                'interest_rate_sensitivity': 'high',
                'economic_sensitivity': 'high',
                'typical_performance': 'interest_rate_plays'
            },
            'consumer_discretionary': {
                'name': 'Consumer Discretionary',
                'description': 'Retail, automotive, leisure, hotels, restaurants',
                'growth_profile': 'cyclical_growth',
                'interest_rate_sensitivity': 'high',
                'economic_sensitivity': 'high',
                'typical_performance': 'economic_sensitive'
            },
            'consumer_staples': {
                'name': 'Consumer Staples',
                'description': 'Food, beverages, household products, tobacco',
                'growth_profile': 'stable_growth',
                'interest_rate_sensitivity': 'low',
                'economic_sensitivity': 'low',
                'typical_performance': 'defensive'
            },
            'energy': {
                'name': 'Energy',
                'description': 'Oil, gas, renewable energy, equipment services',
                'growth_profile': 'commodity_cyclical',
                'interest_rate_sensitivity': 'medium',
                'economic_sensitivity': 'high',
                'typical_performance': 'commodity_cyclical'
            },
            'industrials': {
                'name': 'Industrials',
                'description': 'Aerospace, machinery, transportation, construction',
                'growth_profile': 'cyclical_growth',
                'interest_rate_sensitivity': 'medium',
                'economic_sensitivity': 'high',
                'typical_performance': 'economic_cyclical'
            },
            'materials': {
                'name': 'Materials',
                'description': 'Chemicals, metals, mining, paper, packaging',
                'growth_profile': 'commodity_cyclical',
                'interest_rate_sensitivity': 'medium',
                'economic_sensitivity': 'high',
                'typical_performance': 'commodity_cyclical'
            },
            'utilities': {
                'name': 'Utilities',
                'description': 'Electric, gas, water utilities, independent power producers',
                'growth_profile': 'stable_growth',
                'interest_rate_sensitivity': 'very_high',
                'economic_sensitivity': 'very_low',
                'typical_performance': 'defensive_income'
            },
            'real_estate': {
                'name': 'Real Estate',
                'description': 'REITs, real estate management, development',
                'growth_profile': 'stable_growth',
                'interest_rate_sensitivity': 'very_high',
                'economic_sensitivity': 'medium',
                'typical_performance': 'rate_sensitive'
            },
            'communication_services': {
                'name': 'Communication Services',
                'description': 'Telecom, media, entertainment, interactive media',
                'growth_profile': 'moderate_growth',
                'interest_rate_sensitivity': 'medium',
                'economic_sensitivity': 'medium',
                'typical_performance': 'mixed'
            }
        }
    
    def _initialize_performance_metrics(self) -> Dict[str, Dict[str, float]]:
        """
        Initialize performance metrics weights
        """
        return {
            'technical': {
                'price_momentum': 0.3,
                'relative_strength': 0.25,
                'volume_analysis': 0.15,
                'moving_averages': 0.2,
                'momentum_oscillators': 0.1
            },
            'fundamental': {
                'earnings_growth': 0.3,
                'revenue_growth': 0.2,
                'profit_margins': 0.2,
                'debt_ratios': 0.15,
                'roe_roa': 0.15
            },
            'relative_strength': {
                'vs_market': 0.4,
                'vs_sector': 0.3,
                'vs_peer_group': 0.3
            }
        }
    
    def _initialize_rotation_criteria(self) -> Dict[str, Dict[str, float]]:
        """
        Initialize sector rotation criteria
        """
        return {
            'economic_cycle': {
                'recession': ['consumer_staples', 'healthcare', 'utilities'],
                'early_recovery': ['industrials', 'materials', 'financials'],
                'mid_recovery': ['technology', 'consumer_discretionary', 'communication_services'],
                'late_cycle': ['energy', 'materials', 'industrials'],
                'peak': ['utilities', 'consumer_staples', 'healthcare']
            },
            'interest_rate_environment': {
                'rising_rates': ['financials', 'energy', 'industrials'],
                'falling_rates': ['utilities', 'real_estate', 'consumer_staples'],
                'stable_rates': ['technology', 'healthcare', 'communication_services']
            },
            'inflation_environment': {
                'high_inflation': ['energy', 'materials', 'real_estate'],
                'moderate_inflation': ['financials', 'industrials', 'consumer_discretionary'],
                'low_inflation': ['technology', 'healthcare', 'utilities']
            }
        }
    
    def analyze_sector_rotation(self, market: str = "US", 
                              lookback_period: int = 60) -> Dict[str, Any]:
        """
        Perform comprehensive sector rotation analysis
        """
        logger.info(f"Starting sector rotation analysis for {market}")
        
        rotation_analysis = {
            'market': market,
            'analysis_time': datetime.now().isoformat(),
            'lookback_period': lookback_period,
            'sector_performance': {},
            'rotation_signals': {},
            'economic_context': {},
            'best_performers': [],
            'worst_performers': [],
            'rotation_opportunities': [],
            'risk_sectors': [],
            'recommendations': []
        }
        
        try:
            # Fetch sector data
            rotation_analysis['sector_performance'] = self._fetch_sector_data(
                market, lookback_period
            )
            
            # Calculate relative strength
            rotation_analysis['rotation_signals'] = self._calculate_rotation_signals(
                rotation_analysis['sector_performance']
            )
            
            # Analyze economic context
            rotation_analysis['economic_context'] = self._analyze_economic_context()
            
            # Identify top and bottom performers
            rotation_analysis['best_performers'] = self._identify_best_performers(
                rotation_analysis['sector_performance']
            )
            rotation_analysis['worst_performers'] = self._identify_worst_performers(
                rotation_analysis['sector_performance']
            )
            
            # Generate rotation opportunities
            rotation_analysis['rotation_opportunities'] = self._identify_rotation_opportunities(
                rotation_analysis
            )
            
            # Identify risk sectors
            rotation_analysis['risk_sectors'] = self._identify_risk_sectors(
                rotation_analysis['sector_performance']
            )
            
            # Generate recommendations
            rotation_analysis['recommendations'] = self._generate_rotation_recommendations(
                rotation_analysis
            )
            
        except Exception as e:
            logger.error(f"Error in sector rotation analysis: {str(e)}")
            rotation_analysis['error'] = str(e)
        
        return rotation_analysis
    
    def _fetch_sector_data(self, market: str, lookback_period: int) -> Dict[str, SectorData]:
        """
        Fetch sector performance data
        """
        sector_data = {}
        
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=lookback_period)
            
            for sector_name, etf_ticker in self.sector_etfs.items():
                try:
                    # Fetch ETF data
                    etf = yf.Ticker(etf_ticker)
                    hist_data = etf.history(start=start_date, end=end_date)
                    
                    if hist_data.empty:
                        logger.warning(f"No data for {etf_ticker}")
                        continue
                    
                    # Calculate performance metrics
                    performance_score = self._calculate_performance_score(hist_data)
                    relative_strength = self._calculate_relative_strength(hist_data, market)
                    momentum_score = self._calculate_momentum_score(hist_data)
                    fundamental_score = self._calculate_fundamental_score(etf_ticker)
                    technical_score = self._calculate_technical_score(hist_data)
                    
                    # Calculate overall score
                    overall_score = (
                        performance_score * 0.25 +
                        relative_strength * 0.25 +
                        momentum_score * 0.2 +
                        fundamental_score * 0.15 +
                        technical_score * 0.15
                    )
                    
                    # Determine rotation signal
                    rotation_signal = self._determine_rotation_signal(overall_score)
                    
                    sector_data[sector_name] = SectorData(
                        sector_name=sector_name,
                        ticker=etf_ticker,
                        performance_score=performance_score,
                        relative_strength=relative_strength,
                        momentum_score=momentum_score,
                        fundamental_score=fundamental_score,
                        technical_score=technical_score,
                        overall_score=overall_score,
                        rotation_signal=rotation_signal
                    )
                    
                except Exception as e:
                    logger.warning(f"Error fetching data for {sector_name}: {str(e)}")
                    continue
            
        except Exception as e:
            logger.error(f"Error fetching sector data: {str(e)}")
        
        return sector_data
    
    def _calculate_performance_score(self, data: pd.DataFrame) -> float:
        """
        Calculate overall performance score
        """
        try:
            if len(data) < 10:
                return 50.0  # Neutral score for insufficient data
            
            # Calculate various performance metrics
            returns = data['Close'].pct_change().dropna()
            
            # Total return
            total_return = (data['Close'].iloc[-1] / data['Close'].iloc[0] - 1) * 100
            
            # Annualized return
            days = len(data)
            annualized_return = ((1 + total_return/100) ** (252/days) - 1) * 100
            
            # Volatility
            volatility = returns.std() * np.sqrt(252) * 100
            
            # Sharpe ratio (assuming 2% risk-free rate)
            risk_free_rate = 2.0
            sharpe_ratio = (annualized_return - risk_free_rate) / volatility if volatility > 0 else 0
            
            # Maximum drawdown
            cumulative = (1 + returns).cumprod()
            running_max = cumulative.expanding().max()
            drawdown = (cumulative - running_max) / running_max
            max_drawdown = drawdown.min() * 100
            
            # Combine metrics (normalize and weight)
            performance_score = (
                np.clip(total_return + 50, 0, 100) * 0.3 +  # Total return (30%)
                np.clip(annualized_return + 50, 0, 100) * 0.3 +  # Annualized return (30%)
                np.clip((sharpe_ratio + 2) * 20, 0, 100) * 0.2 +  # Sharpe ratio (20%)
                np.clip(100 + max_drawdown, 0, 100) * 0.2  # Max drawdown (20%)
            )
            
            return performance_score
            
        except Exception as e:
            logger.error(f"Error calculating performance score: {str(e)}")
            return 50.0
    
    def _calculate_relative_strength(self, data: pd.DataFrame, market: str) -> float:
        """
        Calculate relative strength vs market (simplified)
        """
        try:
            # In real implementation, would compare against market index
            # For now, use price momentum as proxy
            if len(data) < 20:
                return 50.0
            
            short_ma = data['Close'].rolling(10).mean()
            long_ma = data['Close'].rolling(20).mean()
            
            current_ratio = short_ma.iloc[-1] / long_ma.iloc[-1]
            
            # Convert to 0-100 scale
            relative_strength = np.clip((current_ratio - 0.95) * 1000, 0, 100)
            
            return relative_strength
            
        except Exception as e:
            logger.error(f"Error calculating relative strength: {str(e)}")
            return 50.0
    
    def _calculate_momentum_score(self, data: pd.DataFrame) -> float:
        """
        Calculate momentum score
        """
        try:
            if len(data) < 14:
                return 50.0
            
            # RSI calculation
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            current_rsi = rsi.iloc[-1]
            
            # Convert RSI to momentum score (oversold = high momentum score)
            momentum_score = 100 - current_rsi if not pd.isna(current_rsi) else 50
            
            return momentum_score
            
        except Exception as e:
            logger.error(f"Error calculating momentum score: {str(e)}")
            return 50.0
    
    def _calculate_fundamental_score(self, ticker: str) -> float:
        """
        Calculate fundamental score (simplified)
        """
        try:
            # In real implementation, would fetch fundamental data
            # For now, return neutral score
            return 50.0
            
        except Exception as e:
            logger.error(f"Error calculating fundamental score: {str(e)}")
            return 50.0
    
    def _calculate_technical_score(self, data: pd.DataFrame) -> float:
        """
        Calculate technical score
        """
        try:
            if len(data) < 20:
                return 50.0
            
            # Moving average analysis
            ma_20 = data['Close'].rolling(20).mean()
            ma_50 = data['Close'].rolling(50).mean()
            
            current_price = data['Close'].iloc[-1]
            current_ma20 = ma_20.iloc[-1]
            current_ma50 = ma_50.iloc[-1]
            
            # Price relative to moving averages
            ma20_ratio = current_price / current_ma20 if not pd.isna(current_ma20) else 1.0
            ma50_ratio = current_price / current_ma50 if not pd.isna(current_ma50) else 1.0
            
            # Technical score based on moving average position
            if ma20_ratio > 1.02 and ma50_ratio > 1.02:
                technical_score = 80.0  # Strong uptrend
            elif ma20_ratio > 1.0 and ma50_ratio > 1.0:
                technical_score = 65.0  # Uptrend
            elif ma20_ratio < 0.98 and ma50_ratio < 0.98:
                technical_score = 20.0  # Strong downtrend
            elif ma20_ratio < 1.0 and ma50_ratio < 1.0:
                technical_score = 35.0  # Downtrend
            else:
                technical_score = 50.0  # Sideways
            
            return technical_score
            
        except Exception as e:
            logger.error(f"Error calculating technical score: {str(e)}")
            return 50.0
    
    def _determine_rotation_signal(self, overall_score: float) -> RotationSignal:
        """
        Determine rotation signal based on overall score
        """
        if overall_score >= 80:
            return RotationSignal.STRONG_BUY
        elif overall_score >= 65:
            return RotationSignal.BUY
        elif overall_score >= 50:
            return RotationSignal.HOLD
        elif overall_score >= 35:
            return RotationSignal.SELL
        else:
            return RotationSignal.STRONG_SELL
    
    def _calculate_rotation_signals(self, sector_data: Dict[str, SectorData]) -> Dict[str, Any]:
        """
        Calculate rotation signals for all sectors
        """
        rotation_signals = {
            'strong_buy_sectors': [],
            'buy_sectors': [],
            'hold_sectors': [],
            'sell_sectors': [],
            'strong_sell_sectors': [],
            'sector_rankings': []
        }
        
        try:
            # Sort sectors by overall score
            sorted_sectors = sorted(
                sector_data.items(),
                key=lambda x: x[1].overall_score,
                reverse=True
            )
            
            rotation_signals['sector_rankings'] = [
                {
                    'sector': sector_name,
                    'score': sector_data.overall_score,
                    'signal': sector_data.rotation_signal.value,
                    'ticker': sector_data.ticker
                }
                for sector_name, sector_data in sorted_sectors
            ]
            
            # Categorize signals
            for sector_name, sector_data in sector_data.items():
                signal = sector_data.rotation_signal
                if signal == RotationSignal.STRONG_BUY:
                    rotation_signals['strong_buy_sectors'].append(sector_name)
                elif signal == RotationSignal.BUY:
                    rotation_signals['buy_sectors'].append(sector_name)
                elif signal == RotationSignal.HOLD:
                    rotation_signals['hold_sectors'].append(sector_name)
                elif signal == RotationSignal.SELL:
                    rotation_signals['sell_sectors'].append(sector_name)
                elif signal == RotationSignal.STRONG_SELL:
                    rotation_signals['strong_sell_sectors'].append(sector_name)
            
        except Exception as e:
            logger.error(f"Error calculating rotation signals: {str(e)}")
        
        return rotation_signals
    
    def _analyze_economic_context(self) -> Dict[str, Any]:
        """
        Analyze current economic context for rotation decisions
        """
        economic_context = {
            'cycle_phase': 'unknown',
            'interest_rate_trend': 'stable',
            'inflation_outlook': 'moderate',
            'preferred_sectors': [],
            'avoid_sectors': []
        }
        
        try:
            # In real implementation, would analyze actual economic data
            # For now, use simulated analysis
            
            economic_context['cycle_phase'] = 'mid_recovery'
            economic_context['interest_rate_trend'] = 'stable'
            economic_context['inflation_outlook'] = 'moderate'
            
            # Determine preferred sectors based on context
            if economic_context['cycle_phase'] == 'mid_recovery':
                economic_context['preferred_sectors'] = ['technology', 'consumer_discretionary']
                economic_context['avoid_sectors'] = ['utilities', 'consumer_staples']
            
        except Exception as e:
            logger.error(f"Error analyzing economic context: {str(e)}")
        
        return economic_context
    
    def _identify_best_performers(self, sector_data: Dict[str, SectorData]) -> List[Dict[str, Any]]:
        """
        Identify best performing sectors
        """
        try:
            # Sort by overall score and get top 3
            sorted_sectors = sorted(
                sector_data.items(),
                key=lambda x: x[1].overall_score,
                reverse=True
            )
            
            best_performers = [
                {
                    'sector': sector_name,
                    'score': sector_data.overall_score,
                    'performance_score': sector_data.performance_score,
                    'relative_strength': sector_data.relative_strength,
                    'momentum_score': sector_data.momentum_score,
                    'ticker': sector_data.ticker
                }
                for sector_name, sector_data in sorted_sectors[:3]
            ]
            
            return best_performers
            
        except Exception as e:
            logger.error(f"Error identifying best performers: {str(e)}")
            return []
    
    def _identify_worst_performers(self, sector_data: Dict[str, SectorData]) -> List[Dict[str, Any]]:
        """
        Identify worst performing sectors
        """
        try:
            # Sort by overall score and get bottom 3
            sorted_sectors = sorted(
                sector_data.items(),
                key=lambda x: x[1].overall_score
            )
            
            worst_performers = [
                {
                    'sector': sector_name,
                    'score': sector_data.overall_score,
                    'performance_score': sector_data.performance_score,
                    'relative_strength': sector_data.relative_strength,
                    'momentum_score': sector_data.momentum_score,
                    'ticker': sector_data.ticker
                }
                for sector_name, sector_data in sorted_sectors[:3]
            ]
            
            return worst_performers
            
        except Exception as e:
            logger.error(f"Error identifying worst performers: {str(e)}")
            return []
    
    def _identify_rotation_opportunities(self, rotation_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Identify sector rotation opportunities
        """
        opportunities = []
        
        try:
            sector_performance = rotation_analysis.get('sector_performance', {})
            rotation_signals = rotation_analysis.get('rotation_signals', {})
            economic_context = rotation_analysis.get('economic_context', {})
            
            # Strong buy opportunities in preferred sectors
            strong_buy_sectors = rotation_signals.get('strong_buy_sectors', [])
            preferred_sectors = economic_context.get('preferred_sectors', [])
            
            for sector in strong_buy_sectors:
                if sector in preferred_sectors:
                    opportunities.append({
                        'type': 'strong_rotation',
                        'sector': sector,
                        'action': 'increase_allocation',
                        'confidence': 'high',
                        'reason': 'Strong technical/fundamental signals align with economic cycle'
                    })
            
            # Momentum rotation opportunities
            best_performers = rotation_analysis.get('best_performers', [])
            for performer in best_performers[:2]:
                if performer['sector'] not in preferred_sectors:
                    opportunities.append({
                        'type': 'momentum_play',
                        'sector': performer['sector'],
                        'action': 'tactical_overweight',
                        'confidence': 'medium',
                        'reason': 'Strong momentum and relative strength'
                    })
            
        except Exception as e:
            logger.error(f"Error identifying rotation opportunities: {str(e)}")
        
        return opportunities
    
    def _identify_risk_sectors(self, sector_data: Dict[str, SectorData]) -> List[Dict[str, Any]]:
        """
        Identify sectors with high risk
        """
        risk_sectors = []
        
        try:
            for sector_name, sector_data in sector_data.items():
                if sector_data.rotation_signal in [RotationSignal.STRONG_SELL, RotationSignal.SELL]:
                    risk_sectors.append({
                        'sector': sector_name,
                        'risk_level': 'high' if sector_data.rotation_signal == RotationSignal.STRONG_SELL else 'medium',
                        'score': sector_data.overall_score,
                        'main_concerns': ['Weak technicals', 'Poor momentum', 'Economic headwinds']
                    })
            
        except Exception as e:
            logger.error(f"Error identifying risk sectors: {str(e)}")
        
        return risk_sectors
    
    def _generate_rotation_recommendations(self, rotation_analysis: Dict[str, Any]) -> List[str]:
        """
        Generate sector rotation recommendations
        """
        recommendations = []
        
        try:
            rotation_signals = rotation_analysis.get('rotation_signals', {})
            economic_context = rotation_analysis.get('economic_context', {})
            
            # Strong buy recommendations
            strong_buy_sectors = rotation_signals.get('strong_buy_sectors', [])
            if strong_buy_sectors:
                recommendations.append(f"Strong buy signals in: {', '.join(strong_buy_sectors[:3])}")
            
            # Sector overweight recommendations
            preferred_sectors = economic_context.get('preferred_sectors', [])
            if preferred_sectors:
                recommendations.append(f"Economic cycle favors: {', '.join(preferred_sectors)}")
            
            # Risk warnings
            sell_sectors = rotation_signals.get('sell_sectors', []) + rotation_signals.get('strong_sell_sectors', [])
            if sell_sectors:
                recommendations.append(f"Avoid or underweight: {', '.join(sell_sectors[:3])}")
            
            # Tactical recommendations
            best_performers = rotation_analysis.get('best_performers', [])
            if best_performers:
                recommendations.append(f"Momentum leaders: {', '.join([p['sector'] for p in best_performers[:2]])}")
            
        except Exception as e:
            logger.error(f"Error generating rotation recommendations: {str(e)}")
        
        return recommendations

# Global instance
sector_analyzer = SectorIndustryAnalyzer()

if __name__ == "__main__":
    # Example usage
    print("🧪 Testing Sector & Industry Analyzer...")
    
    try:
        # Test sector rotation analysis
        results = sector_analyzer.analyze_sector_rotation(market="US", lookback_period=60)
        
        print(f"✅ Sector rotation analysis completed")
        print(f"📊 Sectors analyzed: {len(results['sector_performance'])}")
        
        # Show rotation signals
        rotation_signals = results.get('rotation_signals', {})
        print(f"🚀 Strong Buy: {len(rotation_signals.get('strong_buy_sectors', []))} sectors")
        print(f"📈 Buy: {len(rotation_signals.get('buy_sectors', []))} sectors")
        print(f"⚖️ Hold: {len(rotation_signals.get('hold_sectors', []))} sectors")
        print(f"📉 Sell: {len(rotation_signals.get('sell_sectors', []))} sectors")
        print(f"🔴 Strong Sell: {len(rotation_signals.get('strong_sell_sectors', []))} sectors")
        
        # Show top performers
        best_performers = results.get('best_performers', [])
        if best_performers:
            print(f"🏆 Top 3 Performers:")
            for i, performer in enumerate(best_performers, 1):
                print(f"   {i}. {performer['sector']}: {performer['score']:.1f}")
        
        # Show worst performers
        worst_performers = results.get('worst_performers', [])
        if worst_performers:
            print(f"📉 Bottom 3 Performers:")
            for i, performer in enumerate(worst_performers, 1):
                print(f"   {i}. {performer['sector']}: {performer['score']:.1f}")
        
        # Show rotation opportunities
        opportunities = results.get('rotation_opportunities', [])
        if opportunities:
            print(f"🎯 Rotation Opportunities ({len(opportunities)}):")
            for opp in opportunities[:3]:
                print(f"   • {opp['sector']}: {opp['action']} ({opp['confidence']} confidence)")
        
        # Show recommendations
        recommendations = results.get('recommendations', [])
        if recommendations:
            print(f"💡 Recommendations ({len(recommendations)}):")
            for rec in recommendations:
                print(f"   • {rec}")
        
        # Show economic context
        economic_context = results.get('economic_context', {})
        print(f"🔄 Economic Context:")
        print(f"   Cycle Phase: {economic_context.get('cycle_phase', 'unknown')}")
        print(f"   Interest Rate Trend: {economic_context.get('interest_rate_trend', 'unknown')}")
        print(f"   Inflation Outlook: {economic_context.get('inflation_outlook', 'unknown')}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()