"""
Advanced Fundamental Analysis Engine
Comprehensive Financial Ratios, Earnings Analysis, and Company Valuation
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import yfinance as yf
from vnstock import Vnstock
import requests
import json

logger = logging.getLogger(__name__)

class FinancialHealth(Enum):
    """Financial health assessment levels"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"

@dataclass
class FinancialRatio:
    """Financial ratio data structure"""
    name: str
    value: float
    industry_average: Optional[float] = None
    score: Optional[float] = None
    interpretation: str = ""
    category: str = ""

class FundamentalAnalysisEngine:
    """
    Advanced Fundamental Analysis Engine for comprehensive financial evaluation
    """
    
    def __init__(self):
        self.industry_benchmarks = self._load_industry_benchmarks()
        self.ratio_weights = self._initialize_ratio_weights()
        
    def _load_industry_benchmarks(self) -> Dict[str, Dict[str, float]]:
        """
        Load industry benchmarks for financial ratios
        """
        return {
            "technology": {
                "pe_ratio": 25.0,
                "pb_ratio": 4.0,
                "roe": 0.15,
                "roa": 0.08,
                "debt_to_equity": 0.5,
                "current_ratio": 2.0,
                "quick_ratio": 1.5,
                "profit_margin": 0.15,
                "gross_margin": 0.40
            },
            "financial_services": {
                "pe_ratio": 12.0,
                "pb_ratio": 1.0,
                "roe": 0.12,
                "roa": 0.01,
                "debt_to_equity": 8.0,
                "current_ratio": 1.1,
                "quick_ratio": 1.0,
                "profit_margin": 0.25,
                "gross_margin": 0.50
            },
            "manufacturing": {
                "pe_ratio": 18.0,
                "pb_ratio": 2.0,
                "roe": 0.12,
                "roa": 0.06,
                "debt_to_equity": 1.0,
                "current_ratio": 1.8,
                "quick_ratio": 1.2,
                "profit_margin": 0.10,
                "gross_margin": 0.25
            },
            "retail": {
                "pe_ratio": 20.0,
                "pb_ratio": 3.0,
                "roe": 0.15,
                "roa": 0.08,
                "debt_to_equity": 1.2,
                "current_ratio": 1.5,
                "quick_ratio": 0.8,
                "profit_margin": 0.05,
                "gross_margin": 0.30
            },
            "utilities": {
                "pe_ratio": 15.0,
                "pb_ratio": 1.5,
                "roe": 0.10,
                "roa": 0.04,
                "debt_to_equity": 2.0,
                "current_ratio": 0.8,
                "quick_ratio": 0.7,
                "profit_margin": 0.12,
                "gross_margin": 0.35
            }
        }
    
    def _initialize_ratio_weights(self) -> Dict[str, float]:
        """
        Initialize weights for different financial ratios
        """
        return {
            # Valuation ratios (25%)
            "pe_ratio": 0.08,
            "pb_ratio": 0.07,
            "ps_ratio": 0.05,
            "ev_ebitda": 0.05,
            
            # Profitability ratios (30%)
            "roe": 0.10,
            "roa": 0.08,
            "profit_margin": 0.07,
            "gross_margin": 0.05,
            
            # Efficiency ratios (20%)
            "asset_turnover": 0.06,
            "inventory_turnover": 0.04,
            "receivables_turnover": 0.04,
            "working_capital": 0.06,
            
            # Liquidity ratios (15%)
            "current_ratio": 0.06,
            "quick_ratio": 0.05,
            "cash_ratio": 0.04,
            
            # Leverage ratios (10%)
            "debt_to_equity": 0.05,
            "debt_ratio": 0.03,
            "interest_coverage": 0.02
        }
    
    def perform_comprehensive_fundamental_analysis(self, ticker: str, 
                                                 sector: str = "manufacturing") -> Dict[str, Any]:
        """
        Perform comprehensive fundamental analysis
        """
        logger.info(f"Starting comprehensive fundamental analysis for {ticker}")
        
        analysis_results = {
            'ticker': ticker,
            'analysis_date': datetime.now().isoformat(),
            'sector': sector,
            'financial_ratios': {},
            'earnings_analysis': {},
            'growth_metrics': {},
            'valuation_metrics': {},
            'financial_health': {},
            'overall_score': 0.0,
            'recommendation': 'hold'
        }
        
        try:
            # Fetch financial data
            financial_data = self._fetch_financial_data(ticker)
            
            if not financial_data:
                logger.warning(f"No financial data available for {ticker}")
                return analysis_results
            
            # Calculate financial ratios
            analysis_results['financial_ratios'] = self._calculate_financial_ratios(
                financial_data, sector
            )
            
            # Analyze earnings
            analysis_results['earnings_analysis'] = self._analyze_earnings(financial_data)
            
            # Calculate growth metrics
            analysis_results['growth_metrics'] = self._calculate_growth_metrics(financial_data)
            
            # Calculate valuation metrics
            analysis_results['valuation_metrics'] = self._calculate_valuation_metrics(
                financial_data, ticker
            )
            
            # Assess financial health
            analysis_results['financial_health'] = self._assess_financial_health(
                analysis_results['financial_ratios']
            )
            
            # Calculate overall score
            analysis_results['overall_score'] = self._calculate_overall_score(
                analysis_results
            )
            
            # Generate recommendation
            analysis_results['recommendation'] = self._generate_recommendation(
                analysis_results['overall_score'], analysis_results
            )
            
        except Exception as e:
            logger.error(f"Error in fundamental analysis for {ticker}: {str(e)}")
            analysis_results['error'] = str(e)
        
        return analysis_results
    
    def _fetch_financial_data(self, ticker: str) -> Dict[str, Any]:
        """
        Fetch comprehensive financial data
        """
        financial_data = {
            'income_statement': {},
            'balance_sheet': {},
            'cash_flow': {},
            'key_metrics': {}
        }
        
        try:
            # Try Yahoo Finance first
            ticker_obj = yf.Ticker(ticker)
            
            # Get financial statements
            income_stmt = ticker_obj.financials
            balance_sheet = ticker_obj.balance_sheet
            cash_flow = ticker_obj.cashflow
            info = ticker_obj.info
            
            financial_data['income_statement'] = income_stmt
            financial_data['balance_sheet'] = balance_sheet
            financial_data['cash_flow'] = cash_flow
            financial_data['key_metrics'] = info
            
            # If Yahoo Finance fails, try VNStock
            if income_stmt.empty:
                financial_data = self._fetch_vnstock_data(ticker)
            
        except Exception as e:
            logger.warning(f"Error fetching financial data from Yahoo Finance: {str(e)}")
            try:
                financial_data = self._fetch_vnstock_data(ticker)
            except Exception as e2:
                logger.warning(f"Error fetching from VNStock: {str(e2)}")
        
        return financial_data
    
    def _fetch_vnstock_data(self, ticker: str) -> Dict[str, Any]:
        """
        Fetch financial data from VNStock
        """
        financial_data = {
            'income_statement': {},
            'balance_sheet': {},
            'cash_flow': {},
            'key_metrics': {}
        }
        
        try:
            vnstock_instance = Vnstock()
            stock_component = vnstock_instance.stock(symbol=ticker)
            
            # Get financial ratios
            financial_ratios = stock_component.financial_ratio()
            company_overview = stock_component.company_overview()
            
            financial_data['key_metrics'] = {
                'financial_ratios': financial_ratios,
                'company_overview': company_overview
            }
            
        except Exception as e:
            logger.error(f"Error fetching VNStock data: {str(e)}")
        
        return financial_data
    
    def _calculate_financial_ratios(self, financial_data: Dict[str, Any], 
                                  sector: str) -> Dict[str, FinancialRatio]:
        """
        Calculate comprehensive financial ratios
        """
        ratios = {}
        
        try:
            info = financial_data.get('key_metrics', {})
            
            # Valuation Ratios
            ratios['pe_ratio'] = FinancialRatio(
                name="Price-to-Earnings Ratio",
                value=info.get('trailingPE', 0) or info.get('forwardPE', 0) or 0,
                industry_average=self.industry_benchmarks.get(sector, {}).get('pe_ratio'),
                category="valuation"
            )
            
            ratios['pb_ratio'] = FinancialRatio(
                name="Price-to-Book Ratio",
                value=info.get('priceToBook', 0) or 0,
                industry_average=self.industry_benchmarks.get(sector, {}).get('pb_ratio'),
                category="valuation"
            )
            
            ratios['ps_ratio'] = FinancialRatio(
                name="Price-to-Sales Ratio",
                value=info.get('priceToSalesTrailing12Months', 0) or 0,
                category="valuation"
            )
            
            # Profitability Ratios
            ratios['roe'] = FinancialRatio(
                name="Return on Equity",
                value=info.get('returnOnEquity', 0) or 0,
                industry_average=self.industry_benchmarks.get(sector, {}).get('roe'),
                category="profitability"
            )
            
            ratios['roa'] = FinancialRatio(
                name="Return on Assets",
                value=info.get('returnOnAssets', 0) or 0,
                industry_average=self.industry_benchmarks.get(sector, {}).get('roa'),
                category="profitability"
            )
            
            ratios['profit_margin'] = FinancialRatio(
                name="Profit Margin",
                value=info.get('profitMargins', 0) or 0,
                industry_average=self.industry_benchmarks.get(sector, {}).get('profit_margin'),
                category="profitability"
            )
            
            ratios['gross_margin'] = FinancialRatio(
                name="Gross Margin",
                value=info.get('grossMargins', 0) or 0,
                industry_average=self.industry_benchmarks.get(sector, {}).get('gross_margin'),
                category="profitability"
            )
            
            # Liquidity Ratios
            ratios['current_ratio'] = FinancialRatio(
                name="Current Ratio",
                value=info.get('currentRatio', 0) or 0,
                industry_average=self.industry_benchmarks.get(sector, {}).get('current_ratio'),
                category="liquidity"
            )
            
            ratios['quick_ratio'] = FinancialRatio(
                name="Quick Ratio",
                value=info.get('quickRatio', 0) or 0,
                industry_average=self.industry_benchmarks.get(sector, {}).get('quick_ratio'),
                category="liquidity"
            )
            
            # Leverage Ratios
            ratios['debt_to_equity'] = FinancialRatio(
                name="Debt-to-Equity Ratio",
                value=info.get('debtToEquity', 0) or 0,
                industry_average=self.industry_benchmarks.get(sector, {}).get('debt_to_equity'),
                category="leverage"
            )
            
            # Efficiency Ratios
            ratios['asset_turnover'] = FinancialRatio(
                name="Asset Turnover",
                value=info.get('assetTurnover', 0) or 0,
                category="efficiency"
            )
            
            # Calculate scores for each ratio
            for ratio_name, ratio in ratios.items():
                ratio.score = self._calculate_ratio_score(ratio, sector)
                ratio.interpretation = self._interpret_ratio(ratio)
        
        except Exception as e:
            logger.error(f"Error calculating financial ratios: {str(e)}")
        
        return ratios
    
    def _calculate_ratio_score(self, ratio: FinancialRatio, sector: str) -> float:
        """
        Calculate score for a financial ratio (0-100)
        """
        try:
            if ratio.value == 0 or np.isnan(ratio.value):
                return 50.0  # Neutral score for missing data
            
            industry_avg = ratio.industry_average
            if industry_avg and industry_avg > 0:
                # Compare to industry average
                if ratio.name in ["Price-to-Earnings Ratio", "Price-to-Book Ratio", "Debt-to-Equity Ratio"]:
                    # Lower is better for these ratios
                    score = min(100, max(0, 100 * (industry_avg / ratio.value)))
                else:
                    # Higher is better for most ratios
                    score = min(100, max(0, 100 * (ratio.value / industry_avg)))
            else:
                # No industry benchmark, use absolute scoring
                score = self._calculate_absolute_score(ratio)
            
            return score
            
        except Exception as e:
            logger.error(f"Error calculating score for {ratio.name}: {str(e)}")
            return 50.0
    
    def _calculate_absolute_score(self, ratio: FinancialRatio) -> float:
        """
        Calculate absolute score without industry benchmark
        """
        value = ratio.value
        ratio_name = ratio.name
        
        if "Current Ratio" in ratio_name:
            if 1.5 <= value <= 3.0:
                return 100.0
            elif 1.0 <= value <= 4.0:
                return 75.0
            elif 0.8 <= value <= 5.0:
                return 50.0
            else:
                return 25.0
                
        elif "Return on Equity" in ratio_name:
            if value >= 0.15:
                return 100.0
            elif value >= 0.10:
                return 75.0
            elif value >= 0.05:
                return 50.0
            else:
                return 25.0
                
        elif "Return on Assets" in ratio_name:
            if value >= 0.08:
                return 100.0
            elif value >= 0.05:
                return 75.0
            elif value >= 0.02:
                return 50.0
            else:
                return 25.0
                
        elif "Profit Margin" in ratio_name:
            if value >= 0.15:
                return 100.0
            elif value >= 0.10:
                return 75.0
            elif value >= 0.05:
                return 50.0
            else:
                return 25.0
        
        # Default scoring
        return 50.0
    
    def _interpret_ratio(self, ratio: FinancialRatio) -> str:
        """
        Provide interpretation for financial ratio
        """
        value = ratio.value
        score = ratio.score or 50.0
        
        if score >= 80:
            return "Excellent"
        elif score >= 60:
            return "Good"
        elif score >= 40:
            return "Fair"
        elif score >= 20:
            return "Poor"
        else:
            return "Critical"
    
    def _analyze_earnings(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze earnings performance and trends
        """
        earnings_analysis = {
            'earnings_growth': 0.0,
            'earnings_quality': 'unknown',
            'consistency': 'unknown',
            'surprise_frequency': 0.0,
            'trend': 'stable'
        }
        
        try:
            info = financial_data.get('key_metrics', {})
            
            # Earnings growth
            earnings_growth = info.get('earningsGrowth', 0) or info.get('revenueGrowth', 0)
            earnings_analysis['earnings_growth'] = earnings_growth
            
            # Determine earnings trend
            if earnings_growth > 0.15:
                earnings_analysis['trend'] = 'strong_growth'
            elif earnings_growth > 0.05:
                earnings_analysis['trend'] = 'moderate_growth'
            elif earnings_growth > -0.05:
                earnings_analysis['trend'] = 'stable'
            else:
                earnings_analysis['trend'] = 'declining'
            
            # Earnings quality assessment
            profit_margin = info.get('profitMargins', 0)
            if profit_margin > 0.10:
                earnings_analysis['earnings_quality'] = 'high'
            elif profit_margin > 0.05:
                earnings_analysis['earnings_quality'] = 'medium'
            else:
                earnings_analysis['earnings_quality'] = 'low'
            
        except Exception as e:
            logger.error(f"Error analyzing earnings: {str(e)}")
        
        return earnings_analysis
    
    def _calculate_growth_metrics(self, financial_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate growth metrics
        """
        growth_metrics = {
            'revenue_growth': 0.0,
            'earnings_growth': 0.0,
            'book_value_growth': 0.0,
            'dividend_growth': 0.0
        }
        
        try:
            info = financial_data.get('key_metrics', {})
            
            growth_metrics['revenue_growth'] = info.get('revenueGrowth', 0) or 0
            growth_metrics['earnings_growth'] = info.get('earningsGrowth', 0) or 0
            growth_metrics['book_value_growth'] = info.get('bookValue', 0) or 0
            growth_metrics['dividend_growth'] = info.get('dividendYield', 0) or 0
            
        except Exception as e:
            logger.error(f"Error calculating growth metrics: {str(e)}")
        
        return growth_metrics
    
    def _calculate_valuation_metrics(self, financial_data: Dict[str, Any], ticker: str) -> Dict[str, float]:
        """
        Calculate valuation metrics
        """
        valuation_metrics = {
            'fair_value_estimate': 0.0,
            'intrinsic_value': 0.0,
            'mos_margin': 0.0,
            'valuation_score': 50.0
        }
        
        try:
            info = financial_data.get('key_metrics', {})
            
            # Get current price and financial metrics
            current_price = info.get('currentPrice', 0) or info.get('regularMarketPrice', 0)
            book_value = info.get('bookValue', 0)
            earnings_per_share = info.get('trailingEps', 0)
            
            # Calculate intrinsic value using multiple methods
            intrinsic_values = []
            
            # Book value method
            if book_value > 0:
                pb_ratio = info.get('priceToBook', 1.0)
                book_based_value = book_value * 1.5  # Conservative multiplier
                intrinsic_values.append(book_based_value)
            
            # Earnings method (P/E based)
            if earnings_per_share > 0:
                pe_ratio = info.get('trailingPE', 15.0)
                earnings_based_value = earnings_per_share * pe_ratio
                intrinsic_values.append(earnings_based_value)
            
            # Average intrinsic value
            if intrinsic_values:
                avg_intrinsic_value = np.mean(intrinsic_values)
                valuation_metrics['intrinsic_value'] = avg_intrinsic_value
                
                # Margin of Safety
                if current_price > 0 and avg_intrinsic_value > 0:
                    mos_margin = (avg_intrinsic_value - current_price) / current_price
                    valuation_metrics['mos_margin'] = mos_margin
                    
                    # Valuation score
                    if mos_margin > 0.3:
                        valuation_metrics['valuation_score'] = 90.0
                    elif mos_margin > 0.15:
                        valuation_metrics['valuation_score'] = 70.0
                    elif mos_margin > 0:
                        valuation_metrics['valuation_score'] = 60.0
                    else:
                        valuation_metrics['valuation_score'] = 30.0
        
        except Exception as e:
            logger.error(f"Error calculating valuation metrics: {str(e)}")
        
        return valuation_metrics
    
    def _assess_financial_health(self, financial_ratios: Dict[str, FinancialRatio]) -> Dict[str, Any]:
        """
        Assess overall financial health
        """
        health_assessment = {
            'overall_health': FinancialHealth.FAIR,
            'strengths': [],
            'weaknesses': [],
            'health_score': 50.0
        }
        
        try:
            total_score = 0.0
            total_weights = 0.0
            
            for ratio_name, ratio in financial_ratios.items():
                if ratio.score is not None and ratio_name in self.ratio_weights:
                    weight = self.ratio_weights[ratio_name]
                    total_score += ratio.score * weight
                    total_weights += weight
                    
                    # Track strengths and weaknesses
                    if ratio.score >= 75:
                        health_assessment['strengths'].append(f"{ratio.name}: {ratio.interpretation}")
                    elif ratio.score <= 40:
                        health_assessment['weaknesses'].append(f"{ratio.name}: {ratio.interpretation}")
            
            # Calculate overall health score
            if total_weights > 0:
                overall_score = total_score / total_weights
                health_assessment['health_score'] = overall_score
                
                # Determine health level
                if overall_score >= 80:
                    health_assessment['overall_health'] = FinancialHealth.EXCELLENT
                elif overall_score >= 65:
                    health_assessment['overall_health'] = FinancialHealth.GOOD
                elif overall_score >= 50:
                    health_assessment['overall_health'] = FinancialHealth.FAIR
                elif overall_score >= 30:
                    health_assessment['overall_health'] = FinancialHealth.POOR
                else:
                    health_assessment['overall_health'] = FinancialHealth.CRITICAL
        
        except Exception as e:
            logger.error(f"Error assessing financial health: {str(e)}")
        
        return health_assessment
    
    def _calculate_overall_score(self, analysis_results: Dict[str, Any]) -> float:
        """
        Calculate overall fundamental analysis score
        """
        try:
            financial_health = analysis_results.get('financial_health', {})
            health_score = financial_health.get('health_score', 50.0)
            
            # Weighted scoring components
            weights = {
                'financial_health': 0.4,
                'valuation': 0.3,
                'growth': 0.2,
                'earnings': 0.1
            }
            
            scores = {
                'financial_health': health_score,
                'valuation': analysis_results.get('valuation_metrics', {}).get('valuation_score', 50.0),
                'growth': self._calculate_growth_score(analysis_results.get('growth_metrics', {})),
                'earnings': self._calculate_earnings_score(analysis_results.get('earnings_analysis', {}))
            }
            
            overall_score = sum(scores[component] * weights[component] for component in weights)
            
            return overall_score
            
        except Exception as e:
            logger.error(f"Error calculating overall score: {str(e)}")
            return 50.0
    
    def _calculate_growth_score(self, growth_metrics: Dict[str, float]) -> float:
        """
        Calculate growth score
        """
        try:
            revenue_growth = growth_metrics.get('revenue_growth', 0)
            earnings_growth = growth_metrics.get('earnings_growth', 0)
            
            # Score based on growth rates
            if revenue_growth > 0.15 and earnings_growth > 0.15:
                return 90.0
            elif revenue_growth > 0.10 and earnings_growth > 0.10:
                return 75.0
            elif revenue_growth > 0.05 and earnings_growth > 0.05:
                return 60.0
            elif revenue_growth > 0:
                return 50.0
            else:
                return 25.0
                
        except Exception as e:
            logger.error(f"Error calculating growth score: {str(e)}")
            return 50.0
    
    def _calculate_earnings_score(self, earnings_analysis: Dict[str, Any]) -> float:
        """
        Calculate earnings score
        """
        try:
            trend = earnings_analysis.get('trend', 'stable')
            quality = earnings_analysis.get('earnings_quality', 'unknown')
            
            if trend == 'strong_growth' and quality == 'high':
                return 90.0
            elif trend in ['strong_growth', 'moderate_growth'] and quality in ['high', 'medium']:
                return 75.0
            elif trend == 'moderate_growth' or quality == 'medium':
                return 60.0
            elif trend == 'stable':
                return 50.0
            else:
                return 25.0
                
        except Exception as e:
            logger.error(f"Error calculating earnings score: {str(e)}")
            return 50.0
    
    def _generate_recommendation(self, overall_score: float, analysis_results: Dict[str, Any]) -> str:
        """
        Generate investment recommendation
        """
        try:
            financial_health = analysis_results.get('financial_health', {})
            health = financial_health.get('overall_health', FinancialHealth.FAIR)
            valuation_score = analysis_results.get('valuation_metrics', {}).get('valuation_score', 50.0)
            
            if overall_score >= 80 and health in [FinancialHealth.EXCELLENT, FinancialHealth.GOOD]:
                return "strong_buy"
            elif overall_score >= 70:
                return "buy"
            elif overall_score >= 60:
                return "hold"
            elif overall_score >= 40:
                return "weak_hold"
            else:
                return "sell"
                
        except Exception as e:
            logger.error(f"Error generating recommendation: {str(e)}")
            return "hold"

# Global instance
fundamental_analyzer = FundamentalAnalysisEngine()

if __name__ == "__main__":
    # Example usage
    print("🧪 Testing Fundamental Analysis Engine...")
    
    # Test ticker
    ticker = "AAPL"  # Use a well-known ticker for testing
    
    try:
        # Perform analysis
        results = fundamental_analyzer.perform_comprehensive_fundamental_analysis(ticker)
        
        print(f"✅ Fundamental analysis completed for {ticker}")
        print(f"📊 Overall Score: {results['overall_score']:.1f}/100")
        print(f"🎯 Recommendation: {results['recommendation']}")
        
        # Show key ratios
        ratios = results.get('financial_ratios', {})
        print(f"📈 Key Ratios ({len(ratios)} calculated):")
        for ratio_name, ratio in list(ratios.items())[:5]:
            print(f"   {ratio.name}: {ratio.value:.2f} (Score: {ratio.score:.1f})")
        
        # Show financial health
        health = results.get('financial_health', {})
        print(f"💪 Financial Health: {health.get('overall_health', 'unknown').value}")
        print(f"💪 Health Score: {health.get('health_score', 0):.1f}/100")
        
        # Show strengths and weaknesses
        strengths = health.get('strengths', [])
        weaknesses = health.get('weaknesses', [])
        if strengths:
            print(f"✅ Strengths: {len(strengths)} identified")
        if weaknesses:
            print(f"⚠️ Weaknesses: {len(weaknesses)} identified")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()