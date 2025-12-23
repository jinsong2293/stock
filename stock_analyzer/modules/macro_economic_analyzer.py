"""
Advanced Macro-economic Factor Analysis Engine
Analysis of Economic Indicators Impact on Stock Markets
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import requests
import json
import yfinance as yf
from scipy import stats
import warnings

logger = logging.getLogger(__name__)
warnings.filterwarnings('ignore')

class EconomicCycle(Enum):
    """Economic cycle phases"""
    RECESSION = "recession"
    RECOVERY = "recovery"
    EXPANSION = "expansion"
    PEAK = "peak"
    UNKNOWN = "unknown"

class InterestRateTrend(Enum):
    """Interest rate trend directions"""
    RISING = "rising"
    FALLING = "falling"
    STABLE = "stable"

@dataclass
class EconomicIndicator:
    """Economic indicator data structure"""
    name: str
    value: float
    previous_value: float
    change_percent: float
    impact_score: float
    significance: str
    description: str

class MacroEconomicAnalyzer:
    """
    Advanced Macro-economic Factor Analysis Engine
    Analyzes impact of economic indicators on stock market performance
    """
    
    def __init__(self):
        self.economic_indicators = self._initialize_indicators()
        self.correlation_weights = self._initialize_correlation_weights()
        self.cycle_indicators = self._initialize_cycle_indicators()
        
    def _initialize_indicators(self) -> Dict[str, Dict[str, Any]]:
        """
        Initialize economic indicators configuration
        """
        return {
            # Interest Rates
            'fed_funds_rate': {
                'name': 'Fed Funds Rate',
                'category': 'interest_rates',
                'impact_weight': 0.25,
                'description': 'Federal Reserve policy rate',
                'data_source': 'federal_reserve'
            },
            'treasury_10y': {
                'name': '10-Year Treasury Yield',
                'category': 'interest_rates', 
                'impact_weight': 0.20,
                'description': 'Long-term government bond yield',
                'data_source': 'treasury'
            },
            
            # Inflation
            'cpi': {
                'name': 'Consumer Price Index',
                'category': 'inflation',
                'impact_weight': 0.20,
                'description': 'Measure of inflation',
                'data_source': 'bls'
            },
            'ppi': {
                'name': 'Producer Price Index',
                'category': 'inflation',
                'impact_weight': 0.15,
                'description': 'Producer price inflation',
                'data_source': 'bls'
            },
            
            # Growth
            'gdp_growth': {
                'name': 'GDP Growth Rate',
                'category': 'growth',
                'impact_weight': 0.20,
                'description': 'Economic growth rate',
                'data_source': 'bea'
            },
            'unemployment_rate': {
                'name': 'Unemployment Rate',
                'category': 'growth',
                'impact_weight': 0.15,
                'description': 'Labor market health',
                'data_source': 'bls'
            },
            
            # Market Indicators
            'vix': {
                'name': 'VIX Volatility Index',
                'category': 'market_sentiment',
                'impact_weight': 0.18,
                'description': 'Market fear index',
                'data_source': 'cboe'
            },
            'dollar_index': {
                'name': 'US Dollar Index',
                'category': 'currency',
                'impact_weight': 0.12,
                'description': 'US Dollar strength',
                'data_source': 'ice'
            }
        }
    
    def _initialize_correlation_weights(self) -> Dict[str, float]:
        """
        Initialize correlation weights for different asset classes
        """
        return {
            'equities': {
                'interest_rates': -0.6,  # Higher rates = lower equity prices
                'inflation': -0.3,       # High inflation = negative for equities
                'growth': 0.8,           # Strong growth = positive for equities
                'market_sentiment': 0.7, # VIX correlation
                'currency': -0.4         # Dollar strength impact
            },
            'bonds': {
                'interest_rates': -0.9,  # Bond prices fall when rates rise
                'inflation': -0.7,       # Inflation erodes bond value
                'growth': -0.2,          # Growth impact on bonds
                'market_sentiment': -0.3,
                'currency': 0.1
            },
            'commodities': {
                'interest_rates': 0.1,
                'inflation': 0.8,        # Commodities hedge inflation
                'growth': 0.5,           # Growth supports commodities
                'market_sentiment': -0.2,
                'currency': -0.6         # Dollar strength hurts commodities
            }
        }
    
    def _initialize_cycle_indicators(self) -> Dict[str, Dict[str, Any]]:
        """
        Initialize economic cycle indicators
        """
        return {
            'yield_curve': {
                'name': 'Yield Curve Slope',
                'description': '10Y - 2Y Treasury spread',
                'recession_threshold': -0.5,  # Inverted yield curve
                'expansion_threshold': 1.0    # Steep yield curve
            },
            'employment_gap': {
                'name': 'Employment Gap',
                'description': 'Actual vs Natural unemployment rate',
                'recession_threshold': 1.0,   # High unemployment gap
                'expansion_threshold': -0.5   # Low unemployment gap
            },
            'capacity_utilization': {
                'name': 'Capacity Utilization',
                'description': 'Industrial capacity usage',
                'recession_threshold': 75,    # Low utilization
                'expansion_threshold': 85     # High utilization
            }
        }
    
    def analyze_macro_economic_factors(self, market: str = "US", 
                                     asset_class: str = "equities") -> Dict[str, Any]:
        """
        Perform comprehensive macro-economic factor analysis
        """
        logger.info(f"Starting macro-economic analysis for {market} {asset_class}")
        
        analysis_results = {
            'market': market,
            'asset_class': asset_class,
            'analysis_time': datetime.now().isoformat(),
            'economic_indicators': {},
            'economic_cycle': {},
            'factor_impact': {},
            'market_correlation': {},
            'economic_score': 0.0,
            'recommendations': [],
            'risk_factors': [],
            'opportunities': []
        }
        
        try:
            # Fetch current economic indicators
            analysis_results['economic_indicators'] = self._fetch_economic_indicators(market)
            
            # Analyze economic cycle
            analysis_results['economic_cycle'] = self._analyze_economic_cycle(
                analysis_results['economic_indicators']
            )
            
            # Calculate factor impacts
            analysis_results['factor_impact'] = self._calculate_factor_impacts(
                analysis_results['economic_indicators'], asset_class
            )
            
            # Analyze market correlations
            analysis_results['market_correlation'] = self._analyze_market_correlations(
                analysis_results['economic_indicators']
            )
            
            # Generate overall economic score
            analysis_results['economic_score'] = self._calculate_economic_score(
                analysis_results
            )
            
            # Generate recommendations and insights
            analysis_results['recommendations'] = self._generate_recommendations(
                analysis_results
            )
            analysis_results['risk_factors'] = self._identify_risk_factors(
                analysis_results
            )
            analysis_results['opportunities'] = self._identify_opportunities(
                analysis_results
            )
            
        except Exception as e:
            logger.error(f"Error in macro-economic analysis: {str(e)}")
            analysis_results['error'] = str(e)
        
        return analysis_results
    
    def _fetch_economic_indicators(self, market: str) -> Dict[str, EconomicIndicator]:
        """
        Fetch current economic indicators (simulated data)
        """
        indicators = {}
        
        try:
            # In real implementation, fetch from economic data APIs
            # For now, use simulated realistic data
            
            # Interest Rates
            indicators['fed_funds_rate'] = EconomicIndicator(
                name='Fed Funds Rate',
                value=5.25,  # Current Fed rate
                previous_value=4.75,
                change_percent=10.53,
                impact_score=0.8,
                significance='high',
                description='Federal Reserve policy rate at 5.25%'
            )
            
            indicators['treasury_10y'] = EconomicIndicator(
                name='10-Year Treasury Yield',
                value=4.35,
                previous_value=4.15,
                change_percent=4.82,
                impact_score=0.7,
                significance='high',
                description='10-year Treasury yield at 4.35%'
            )
            
            # Inflation
            indicators['cpi'] = EconomicIndicator(
                name='CPI YoY',
                value=3.2,
                previous_value=3.7,
                change_percent=-13.51,
                impact_score=0.9,
                significance='very_high',
                description='Consumer inflation at 3.2% year-over-year'
            )
            
            # Growth
            indicators['gdp_growth'] = EconomicIndicator(
                name='GDP Growth Rate',
                value=2.1,
                previous_value=2.0,
                change_percent=5.0,
                impact_score=0.8,
                significance='high',
                description='GDP growth at 2.1% quarterly'
            )
            
            indicators['unemployment_rate'] = EconomicIndicator(
                name='Unemployment Rate',
                value=3.8,
                previous_value=3.9,
                change_percent=-2.56,
                impact_score=0.6,
                significance='medium',
                description='Unemployment rate at 3.8%'
            )
            
            # Market Indicators
            indicators['vix'] = EconomicIndicator(
                name='VIX Index',
                value=18.5,
                previous_value=16.2,
                change_percent=14.20,
                impact_score=0.5,
                significance='medium',
                description='Volatility index at 18.5'
            )
            
            indicators['dollar_index'] = EconomicIndicator(
                name='US Dollar Index',
                value=104.2,
                previous_value=103.8,
                change_percent=0.39,
                impact_score=0.4,
                significance='low',
                description='Dollar index at 104.2'
            )
            
        except Exception as e:
            logger.error(f"Error fetching economic indicators: {str(e)}")
        
        return indicators
    
    def _analyze_economic_cycle(self, indicators: Dict[str, EconomicIndicator]) -> Dict[str, Any]:
        """
        Analyze current economic cycle phase
        """
        cycle_analysis = {
            'current_phase': EconomicCycle.UNKNOWN,
            'cycle_score': 0.0,
            'leading_indicators': {},
            'confidence': 0.0
        }
        
        try:
            # Analyze yield curve (10Y - 2Y spread)
            treasury_10y = indicators.get('treasury_10y', EconomicIndicator('', 4.35, 4.15, 4.82, 0.7, '', ''))
            fed_rate = indicators.get('fed_funds_rate', EconomicIndicator('', 5.25, 4.75, 10.53, 0.8, '', ''))
            
            # Approximate 2Y yield (normally would fetch separately)
            treasury_2y = treasury_10y.value - 0.5  # Rough approximation
            yield_curve_spread = treasury_10y.value - treasury_2y
            
            # Analyze employment gap
            unemployment = indicators.get('unemployment_rate', EconomicIndicator('', 3.8, 3.9, -2.56, 0.6, '', ''))
            natural_unemployment = 4.0  # Approximate NAIRU
            employment_gap = unemployment.value - natural_unemployment
            
            # Determine cycle phase
            cycle_score = 0.0
            
            # Yield curve analysis
            if yield_curve_spread < self.cycle_indicators['yield_curve']['recession_threshold']:
                cycle_score -= 0.4  # Inverted yield curve
            elif yield_curve_spread > self.cycle_indicators['yield_curve']['expansion_threshold']:
                cycle_score += 0.3  # Steep yield curve
            
            # Employment analysis
            if employment_gap > self.cycle_indicators['employment_gap']['recession_threshold']:
                cycle_score -= 0.3  # High unemployment gap
            elif employment_gap < self.cycle_indicators['employment_gap']['expansion_threshold']:
                cycle_score += 0.2  # Low unemployment gap
            
            # GDP growth analysis
            gdp = indicators.get('gdp_growth', EconomicIndicator('', 2.1, 2.0, 5.0, 0.8, '', ''))
            if gdp.value < 0:
                cycle_score -= 0.5  # Negative growth
            elif gdp.value > 3:
                cycle_score += 0.3  # Strong growth
            
            cycle_analysis['cycle_score'] = cycle_score
            
            # Determine phase
            if cycle_score < -0.4:
                cycle_analysis['current_phase'] = EconomicCycle.RECESSION
            elif cycle_score < -0.1:
                cycle_analysis['current_phase'] = EconomicCycle.RECOVERY
            elif cycle_score > 0.3:
                cycle_analysis['current_phase'] = EconomicCycle.PEAK
            elif cycle_score > 0.1:
                cycle_analysis['current_phase'] = EconomicCycle.EXPANSION
            else:
                cycle_analysis['current_phase'] = EconomicCycle.UNKNOWN
            
            # Leading indicators
            cycle_analysis['leading_indicators'] = {
                'yield_curve_spread': yield_curve_spread,
                'employment_gap': employment_gap,
                'yield_curve_signal': 'inverted' if yield_curve_spread < 0 else 'normal',
                'employment_signal': 'tight' if employment_gap < 0 else 'loose'
            }
            
            # Confidence based on indicator consistency
            positive_signals = sum(1 for score in [cycle_score] if score > 0)
            negative_signals = sum(1 for score in [cycle_score] if score < 0)
            cycle_analysis['confidence'] = abs(positive_signals - negative_signals) / max(1, positive_signals + negative_signals)
            
        except Exception as e:
            logger.error(f"Error analyzing economic cycle: {str(e)}")
        
        return cycle_analysis
    
    def _calculate_factor_impacts(self, indicators: Dict[str, EconomicIndicator], 
                                asset_class: str) -> Dict[str, Any]:
        """
        Calculate impact of economic factors on asset class
        """
        factor_impacts = {
            'total_impact_score': 0.0,
            'factor_breakdown': {},
            'risk_level': 'medium',
            'key_drivers': []
        }
        
        try:
            if asset_class not in self.correlation_weights:
                logger.warning(f"No correlation weights for {asset_class}")
                return factor_impacts
            
            correlations = self.correlation_weights[asset_class]
            total_weighted_impact = 0.0
            total_weights = 0.0
            
            factor_breakdown = {}
            
            for indicator_name, indicator in indicators.items():
                # Map indicator to category
                category = self._get_indicator_category(indicator_name)
                
                if category in correlations:
                    correlation = correlations[category]
                    impact = correlation * indicator.change_percent / 100 * indicator.impact_score
                    
                    factor_breakdown[indicator_name] = {
                        'impact_score': impact,
                        'correlation': correlation,
                        'weight': self.economic_indicators[indicator_name]['impact_weight'],
                        'change_percent': indicator.change_percent
                    }
                    
                    total_weighted_impact += impact * self.economic_indicators[indicator_name]['impact_weight']
                    total_weights += self.economic_indicators[indicator_name]['impact_weight']
            
            # Calculate total impact score
            if total_weights > 0:
                factor_impacts['total_impact_score'] = total_weighted_impact / total_weights
            
            factor_impacts['factor_breakdown'] = factor_breakdown
            
            # Determine risk level
            abs_impact = abs(factor_impacts['total_impact_score'])
            if abs_impact > 0.5:
                factor_impacts['risk_level'] = 'high'
            elif abs_impact > 0.3:
                factor_impacts['risk_level'] = 'medium'
            else:
                factor_impacts['risk_level'] = 'low'
            
            # Identify key drivers (top 3 by absolute impact)
            sorted_factors = sorted(
                factor_breakdown.items(), 
                key=lambda x: abs(x[1]['impact_score']), 
                reverse=True
            )
            factor_impacts['key_drivers'] = [name for name, _ in sorted_factors[:3]]
            
        except Exception as e:
            logger.error(f"Error calculating factor impacts: {str(e)}")
        
        return factor_impacts
    
    def _get_indicator_category(self, indicator_name: str) -> str:
        """
        Map indicator name to category
        """
        for category, indicators in self.economic_indicators.items():
            if category == indicator_name:
                return indicators['category']
        return 'unknown'
    
    def _analyze_market_correlations(self, indicators: Dict[str, EconomicIndicator]) -> Dict[str, Any]:
        """
        Analyze correlations between economic indicators and market
        """
        correlations = {
            'market_sentiment_impact': 0.0,
            'volatility_outlook': 'normal',
            'sector_rotations': [],
            'correlation_matrix': {}
        }
            # VIX analysis for market sentiment        
        try:

            vix = indicators.get('vix', EconomicIndicator('', 18.5, 16.2, 14.20, 0.5, '', ''))
            
            if vix.value < 15:
                correlations['market_sentiment_impact'] = 0.7  # Low fear = positive
                correlations['volatility_outlook'] = 'low'
            elif vix.value > 25:
                correlations['market_sentiment_impact'] = -0.8  # High fear = negative
                correlations['volatility_outlook'] = 'high'
            else:
                correlations['market_sentiment_impact'] = 0.0  # Neutral
                correlations['volatility_outlook'] = 'normal'
            
            # Interest rate impact analysis
            fed_rate = indicators.get('fed_funds_rate', EconomicIndicator('', 5.25, 4.75, 10.53, 0.8, '', ''))
            
            if fed_rate.change_percent > 5:
                correlations['sector_rotations'] = [
                    'Financials: Positive (higher rates)',
                    'Utilities: Negative (rate sensitivity)',
                    'REITs: Negative (rate sensitivity)'
                ]
            elif fed_rate.change_percent < -5:
                correlations['sector_rotations'] = [
                    'Utilities: Positive (lower rates)',
                    'REITs: Positive (lower rates)',
                    'Technology: Positive (growth受益)'
                ]
            
        except Exception as e:
            logger.error(f"Error analyzing market correlations: {str(e)}")
        
        return correlations
    
    def _calculate_economic_score(self, analysis_results: Dict[str, Any]) -> float:
        """
        Calculate overall economic score
        """
        try:
            # Component scores
            cycle_score = analysis_results.get('economic_cycle', {}).get('cycle_score', 0.0)
            factor_score = analysis_results.get('factor_impact', {}).get('total_impact_score', 0.0)
            sentiment_score = analysis_results.get('market_correlation', {}).get('market_sentiment_impact', 0.0)
            
            # Weighted combination
            weights = {
                'cycle': 0.4,
                'factors': 0.4,
                'sentiment': 0.2
            }
            
            economic_score = (
                cycle_score * weights['cycle'] +
                factor_score * weights['factors'] +
                sentiment_score * weights['sentiment']
            )
            
            # Normalize to 0-100 scale
            return max(0, min(100, (economic_score + 1) * 50))
            
        except Exception as e:
            logger.error(f"Error calculating economic score: {str(e)}")
            return 50.0  # Neutral score
    
    def _generate_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """
        Generate investment recommendations based on macro analysis
        """
        recommendations = []
        
        try:
            economic_score = analysis_results.get('economic_score', 50.0)
            cycle_phase = analysis_results.get('economic_cycle', {}).get('current_phase', EconomicCycle.UNKNOWN)
            factor_impacts = analysis_results.get('factor_impact', {})
            
            # Score-based recommendations
            if economic_score > 70:
                recommendations.append("Economic environment favorable for risk assets")
                recommendations.append("Consider increasing equity allocation")
            elif economic_score < 30:
                recommendations.append("Economic headwinds present - defensive positioning recommended")
                recommendations.append("Consider increasing cash and bond allocation")
            else:
                recommendations.append("Mixed economic signals - maintain balanced allocation")
            
            # Cycle-based recommendations
            if cycle_phase == EconomicCycle.RECESSION:
                recommendations.append("In recession: Focus on quality stocks and defensive sectors")
            elif cycle_phase == EconomicCycle.RECOVERY:
                recommendations.append("In recovery: Cyclical sectors may outperform")
            elif cycle_phase == EconomicCycle.EXPANSION:
                recommendations.append("In expansion: Growth stocks and technology may benefit")
            elif cycle_phase == EconomicCycle.PEAK:
                recommendations.append("At cycle peak: Consider defensive positioning and profit-taking")
            
            # Factor-based recommendations
            key_drivers = factor_impacts.get('key_drivers', [])
            if 'fed_funds_rate' in key_drivers:
                recommendations.append("Interest rates are key driver - monitor Fed policy closely")
            if 'cpi' in key_drivers:
                recommendations.append("Inflation is key driver - consider inflation hedges")
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
        
        return recommendations
    
    def _identify_risk_factors(self, analysis_results: Dict[str, Any]) -> List[str]:
        """
        Identify key risk factors from macro analysis
        """
        risk_factors = []
        
        try:
            indicators = analysis_results.get('economic_indicators', {})
            
            # Interest rate risks
            fed_rate = indicators.get('fed_funds_rate', EconomicIndicator('', 5.25, 4.75, 10.53, 0.8, '', ''))
            if fed_rate.change_percent > 10:
                risk_factors.append("Rapid interest rate increases pose risk to equity valuations")
            
            # Inflation risks
            cpi = indicators.get('cpi', EconomicIndicator('', 3.2, 3.7, -13.51, 0.9, '', ''))
            if cpi.value > 4:
                risk_factors.append("High inflation may force aggressive Fed tightening")
            
            # Growth risks
            gdp = indicators.get('gdp_growth', EconomicIndicator('', 2.1, 2.0, 5.0, 0.8, '', ''))
            if gdp.value < 1:
                risk_factors.append("Weak economic growth may pressure corporate earnings")
            
            # Volatility risks
            vix = indicators.get('vix', EconomicIndicator('', 18.5, 16.2, 14.20, 0.5, '', ''))
            if vix.value > 25:
                risk_factors.append("High market volatility indicates uncertainty and risk aversion")
            
        except Exception as e:
            logger.error(f"Error identifying risk factors: {str(e)}")
        
        return risk_factors
    
    def _identify_opportunities(self, analysis_results: Dict[str, Any]) -> List[str]:
        """
        Identify investment opportunities from macro analysis
        """
        opportunities = []
        
        try:
            economic_score = analysis_results.get('economic_score', 50.0)
            cycle_phase = analysis_results.get('economic_cycle', {}).get('current_phase', EconomicCycle.UNKNOWN)
            
            # Score-based opportunities
            if economic_score > 60:
                opportunities.append("Favorable macro environment supports risk-taking")
            
            # Cycle-based opportunities
            if cycle_phase == EconomicCycle.RECOVERY:
                opportunities.append("Recovery phase: Consider cyclical and value stocks")
            elif cycle_phase == EconomicCycle.EXPANSION:
                opportunities.append("Expansion phase: Growth stocks and technology may outperform")
            
            # Specific factor opportunities
            indicators = analysis_results.get('economic_indicators', {})
            dollar_index = indicators.get('dollar_index', EconomicIndicator('', 104.2, 103.8, 0.39, 0.4, '', ''))
            
            if dollar_index.change_percent > 2:
                opportunities.append("Strong dollar may benefit US-focused multinationals")
            elif dollar_index.change_percent < -2:
                opportunities.append("Weak dollar may benefit exporters and commodity producers")
            
        except Exception as e:
            logger.error(f"Error identifying opportunities: {str(e)}")
        
        return opportunities

# Global instance
macro_economic_analyzer = MacroEconomicAnalyzer()

if __name__ == "__main__":
    # Example usage
    print("🧪 Testing Macro-Economic Analyzer...")
    
    try:
        # Test comprehensive macro analysis
        results = macro_economic_analyzer.analyze_macro_economic_factors(
            market="US", asset_class="equities"
        )
        
        print(f"✅ Macro-economic analysis completed")
        print(f"📊 Economic Score: {results['economic_score']:.1f}/100")
        
        # Show economic cycle
        cycle = results.get('economic_cycle', {})
        print(f"🔄 Economic Cycle: {cycle.get('current_phase', 'unknown').value}")
        print(f"🔄 Cycle Score: {cycle.get('cycle_score', 0):.2f}")
        
        # Show factor impacts
        factors = results.get('factor_impact', {})
        print(f"📈 Total Impact Score: {factors.get('total_impact_score', 0):.2f}")
        print(f"⚠️ Risk Level: {factors.get('risk_level', 'unknown')}")
        
        # Show key drivers
        key_drivers = factors.get('key_drivers', [])
        if key_drivers:
            print(f"🎯 Key Drivers: {', '.join(key_drivers[:3])}")
        
        # Show market correlations
        correlations = results.get('market_correlation', {})
        print(f"📊 Market Sentiment Impact: {correlations.get('market_sentiment_impact', 0):.2f}")
        print(f"📈 Volatility Outlook: {correlations.get('volatility_outlook', 'unknown')}")
        
        # Show recommendations
        recommendations = results.get('recommendations', [])
        if recommendations:
            print(f"💡 Recommendations ({len(recommendations)}):")
            for rec in recommendations[:3]:
                print(f"   • {rec}")
        
        # Show risk factors
        risk_factors = results.get('risk_factors', [])
        if risk_factors:
            print(f"⚠️ Risk Factors ({len(risk_factors)}):")
            for risk in risk_factors[:3]:
                print(f"   • {risk}")
        
        # Show opportunities
        opportunities = results.get('opportunities', [])
        if opportunities:
            print(f"🚀 Opportunities ({len(opportunities)}):")
            for opp in opportunities[:3]:
                print(f"   • {opp}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()