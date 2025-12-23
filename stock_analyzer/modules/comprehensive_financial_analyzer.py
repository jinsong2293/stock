"""
Comprehensive Financial Analyzer - Phân tích tài chính cơ bản toàn diện
Bao gồm P/E, P/B, ROE, ROA, biên lợi nhuận, tăng trưởng doanh thu và so sánh ngành

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
class FinancialMetrics:
    """Cấu trúc dữ liệu cho các chỉ số tài chính"""
    valuation_metrics: Dict[str, float]
    profitability_metrics: Dict[str, float]
    efficiency_metrics: Dict[str, float]
    growth_metrics: Dict[str, float]
    liquidity_metrics: Dict[str, float]
    leverage_metrics: Dict[str, float]
    sector_comparison: Dict[str, float]
    overall_score: float
    investment_grade: str

class ComprehensiveFinancialAnalyzer:
    """Phân tích tài chính cơ bản toàn diện"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Industry benchmarks for Vietnamese stocks (approximate values)
        self.industry_benchmarks = {
            'Banking': {
                'PE': 12.0, 'PB': 1.2, 'ROE': 0.15, 'ROA': 0.015, 
                'NIM': 0.03, 'NPL': 0.03, 'CAR': 0.12
            },
            'Technology': {
                'PE': 25.0, 'PB': 4.0, 'ROE': 0.20, 'ROA': 0.12,
                'Gross_Margin': 0.40, 'Operating_Margin': 0.15
            },
            'Real Estate': {
                'PE': 15.0, 'PB': 1.5, 'ROE': 0.12, 'ROA': 0.08,
                'Gross_Margin': 0.30, 'Operating_Margin': 0.15
            },
            'Food & Beverage': {
                'PE': 20.0, 'PB': 3.0, 'ROE': 0.18, 'ROA': 0.10,
                'Gross_Margin': 0.35, 'Operating_Margin': 0.12
            },
            'Oil & Gas': {
                'PE': 10.0, 'PB': 1.5, 'ROE': 0.15, 'ROA': 0.10,
                'Gross_Margin': 0.25, 'Operating_Margin': 0.08
            },
            'Steel': {
                'PE': 12.0, 'PB': 1.8, 'ROE': 0.15, 'ROA': 0.08,
                'Gross_Margin': 0.20, 'Operating_Margin': 0.10
            },
            'Pharmaceutical': {
                'PE': 18.0, 'PB': 2.5, 'ROE': 0.16, 'ROA': 0.10,
                'Gross_Margin': 0.45, 'Operating_Margin': 0.15
            },
            'Securities': {
                'PE': 15.0, 'PB': 2.0, 'ROE': 0.15, 'ROA': 0.12,
                'ROE': 0.15, 'Current_Ratio': 1.5
            },
            'Insurance': {
                'PE': 12.0, 'PB': 1.5, 'ROE': 0.12, 'ROA': 0.08,
                'Combined_Ratio': 0.95, 'Loss_Ratio': 0.70
            },
            'Agriculture': {
                'PE': 15.0, 'PB': 2.0, 'ROE': 0.15, 'ROA': 0.08,
                'Gross_Margin': 0.25, 'Operating_Margin': 0.10
            }
        }
    
    def calculate_valuation_metrics(self, financial_data: Dict[str, Any], 
                                  market_data: Dict[str, Any]) -> Dict[str, float]:
        """Tính toán các chỉ số định giá"""
        metrics = {}
        
        try:
            # P/E Ratio
            if 'trailingPE' in financial_data.get('info', {}):
                metrics['PE_Ratio'] = financial_data['info']['trailingPE']
            elif 'forwardPE' in financial_data.get('info', {}):
                metrics['PE_Ratio'] = financial_data['info']['forwardPE']
            else:
                metrics['PE_Ratio'] = None
            
            # P/B Ratio
            if 'priceToBook' in financial_data.get('info', {}):
                metrics['PB_Ratio'] = financial_data['info']['priceToBook']
            else:
                metrics['PB_Ratio'] = None
            
            # P/S Ratio (Price to Sales)
            if 'priceToSalesTrailing12Months' in financial_data.get('info', {}):
                metrics['PS_Ratio'] = financial_data['info']['priceToSalesTrailing12Months']
            else:
                metrics['PS_Ratio'] = None
            
            # P/CF Ratio (Price to Cash Flow)
            if 'priceToCashFlowTrailing12Months' in financial_data.get('info', {}):
                metrics['PCF_Ratio'] = financial_data['info']['priceToCashFlowTrailing12Months']
            else:
                metrics['PCF_Ratio'] = None
            
            # EV/EBITDA
            if 'enterpriseValue' in financial_data.get('info', {}) and 'ebitda' in financial_data.get('info', {}):
                ev = financial_data['info']['enterpriseValue']
                ebitda = financial_data['info']['ebitda']
                if ebitda and ebitda > 0:
                    metrics['EV_EBITDA'] = ev / ebitda
                else:
                    metrics['EV_EBITDA'] = None
            else:
                metrics['EV_EBITDA'] = None
            
            # Market Cap
            if 'marketCap' in financial_data.get('info', {}):
                metrics['Market_Cap'] = financial_data['info']['marketCap']
            else:
                metrics['Market_Cap'] = None
            
            # Enterprise Value
            if 'enterpriseValue' in financial_data.get('info', {}):
                metrics['Enterprise_Value'] = financial_data['info']['enterpriseValue']
            else:
                metrics['Enterprise_Value'] = None
            
        except Exception as e:
            self.logger.error(f"Error calculating valuation metrics: {e}")
        
        return metrics
    
    def calculate_profitability_metrics(self, financial_data: Dict[str, Any]) -> Dict[str, float]:
        """Tính toán các chỉ số khả năng sinh lời"""
        metrics = {}
        
        try:
            info = financial_data.get('info', {})
            
            # Return on Equity (ROE)
            if 'returnOnEquity' in info:
                metrics['ROE'] = info['returnOnEquity']
            elif 'netIncome' in info and 'totalStockholderEquity' in info:
                metrics['ROE'] = info['netIncome'] / info['totalStockholderEquity'] if info['totalStockholderEquity'] else None
            else:
                metrics['ROE'] = None
            
            # Return on Assets (ROA)
            if 'returnOnAssets' in info:
                metrics['ROA'] = info['returnOnAssets']
            elif 'netIncome' in info and 'totalAssets' in info:
                metrics['ROA'] = info['netIncome'] / info['totalAssets'] if info['totalAssets'] else None
            else:
                metrics['ROA'] = None
            
            # Return on Invested Capital (ROIC)
            if 'netIncome' in info and 'totalDebt' in info and 'totalStockholderEquity' in info:
                if info['totalDebt'] and info['totalStockholderEquity']:
                    invested_capital = info['totalDebt'] + info['totalStockholderEquity']
                    metrics['ROIC'] = info['netIncome'] / invested_capital
                else:
                    metrics['ROIC'] = None
            else:
                metrics['ROIC'] = None
            
            # Profit Margins
            if 'profitMargins' in info:
                metrics['Net_Margin'] = info['profitMargins']
            else:
                metrics['Net_Margin'] = None
            
            if 'operatingMargins' in info:
                metrics['Operating_Margin'] = info['operatingMargins']
            else:
                metrics['Operating_Margin'] = None
            
            if 'grossMargins' in info:
                metrics['Gross_Margin'] = info['grossMargins']
            else:
                metrics['Gross_Margin'] = None
            
            # EBITDA Margin
            if 'ebitdaMargins' in info:
                metrics['EBITDA_Margin'] = info['ebitdaMargins']
            else:
                metrics['EBITDA_Margin'] = None
            
            # Earnings Per Share
            if 'trailingEps' in info:
                metrics['EPS'] = info['trailingEps']
            else:
                metrics['EPS'] = None
            
            # Dividend Yield
            if 'dividendYield' in info:
                metrics['Dividend_Yield'] = info['dividendYield']
            else:
                metrics['Dividend_Yield'] = None
            
        except Exception as e:
            self.logger.error(f"Error calculating profitability metrics: {e}")
        
        return metrics
    
    def calculate_efficiency_metrics(self, financial_data: Dict[str, Any]) -> Dict[str, float]:
        """Tính toán các chỉ số hiệu quả hoạt động"""
        metrics = {}
        
        try:
            info = financial_data.get('info', {})
            
            # Asset Turnover
            if 'totalRevenue' in info and 'totalAssets' in info:
                if info['totalAssets'] and info['totalRevenue']:
                    metrics['Asset_Turnover'] = info['totalRevenue'] / info['totalAssets']
                else:
                    metrics['Asset_Turnover'] = None
            else:
                metrics['Asset_Turnover'] = None
            
            # Inventory Turnover (if available)
            if 'inventory' in info and 'costOfGoodsSold' in info:
                if info['inventory'] and info['costOfGoodsSold']:
                    metrics['Inventory_Turnover'] = info['costOfGoodsSold'] / info['inventory']
                else:
                    metrics['Inventory_Turnover'] = None
            else:
                metrics['Inventory_Turnover'] = None
            
            # Receivables Turnover
            if 'totalRevenue' in info and 'netReceivables' in info:
                if info['netReceivables'] and info['totalRevenue']:
                    metrics['Receivables_Turnover'] = info['totalRevenue'] / info['netReceivables']
                else:
                    metrics['Receivables_Turnover'] = None
            else:
                metrics['Receivables_Turnover'] = None
            
            # Working Capital Turnover
            if 'totalRevenue' in info and 'workingCapital' in info:
                if info['workingCapital'] and info['totalRevenue']:
                    metrics['Working_Capital_Turnover'] = info['totalRevenue'] / info['workingCapital']
                else:
                    metrics['Working_Capital_Turnover'] = None
            else:
                metrics['Working_Capital_Turnover'] = None
            
        except Exception as e:
            self.logger.error(f"Error calculating efficiency metrics: {e}")
        
        return metrics
    
    def calculate_growth_metrics(self, financial_data: Dict[str, Any]) -> Dict[str, float]:
        """Tính toán các chỉ số tăng trưởng"""
        metrics = {}
        
        try:
            info = financial_data.get('info', {})
            
            # Revenue Growth
            if 'revenueGrowth' in info:
                metrics['Revenue_Growth'] = info['revenueGrowth']
            else:
                metrics['Revenue_Growth'] = None
            
            # Earnings Growth
            if 'earningsGrowth' in info:
                metrics['Earnings_Growth'] = info['earningsGrowth']
            else:
                metrics['Earnings_Growth'] = None
            
            # Book Value Growth
            if 'bookValue' in info and 'priceToBook' in info:
                # Approximation using market metrics
                metrics['Book_Value_Growth'] = info['bookValue'] * 0.05  # Assume 5% growth
            else:
                metrics['Book_Value_Growth'] = None
            
            # EPS Growth
            if 'trailingEps' in info:
                # Assume some growth rate based on industry
                metrics['EPS_Growth'] = 0.10  # Default 10%
            else:
                metrics['EPS_Growth'] = None
            
            # Dividend Growth
            if 'dividendYield' in info and 'payoutRatio' in info:
                # Approximate dividend growth
                metrics['Dividend_Growth'] = 0.05  # Default 5%
            else:
                metrics['Dividend_Growth'] = None
            
        except Exception as e:
            self.logger.error(f"Error calculating growth metrics: {e}")
        
        return metrics
    
    def calculate_liquidity_metrics(self, financial_data: Dict[str, Any]) -> Dict[str, float]:
        """Tính toán các chỉ số thanh khoản"""
        metrics = {}
        
        try:
            info = financial_data.get('info', {})
            
            # Current Ratio
            if 'currentRatio' in info:
                metrics['Current_Ratio'] = info['currentRatio']
            else:
                metrics['Current_Ratio'] = None
            
            # Quick Ratio
            if 'quickRatio' in info:
                metrics['Quick_Ratio'] = info['quickRatio']
            else:
                metrics['Quick_Ratio'] = None
            
            # Cash Ratio
            if 'totalCash' in info and 'totalDebt' in info:
                if info['totalDebt']:
                    metrics['Cash_Ratio'] = info['totalCash'] / info['totalDebt']
                else:
                    metrics['Cash_Ratio'] = None
            else:
                metrics['Cash_Ratio'] = None
            
            # Operating Cash Flow Ratio
            if 'operatingCashFlow' in info and 'totalDebt' in info:
                if info['totalDebt']:
                    metrics['OCF_Ratio'] = info['operatingCashFlow'] / info['totalDebt']
                else:
                    metrics['OCF_Ratio'] = None
            else:
                metrics['OCF_Ratio'] = None
            
        except Exception as e:
            self.logger.error(f"Error calculating liquidity metrics: {e}")
        
        return metrics
    
    def calculate_leverage_metrics(self, financial_data: Dict[str, Any]) -> Dict[str, float]:
        """Tính toán các chỉ số đòn bẩy tài chính"""
        metrics = {}
        
        try:
            info = financial_data.get('info', {})
            
            # Debt to Equity Ratio
            if 'debtToEquity' in info:
                metrics['Debt_To_Equity'] = info['debtToEquity']
            elif 'totalDebt' in info and 'totalStockholderEquity' in info:
                if info['totalStockholderEquity']:
                    metrics['Debt_To_Equity'] = info['totalDebt'] / info['totalStockholderEquity']
                else:
                    metrics['Debt_To_Equity'] = None
            else:
                metrics['Debt_To_Equity'] = None
            
            # Debt to Assets Ratio
            if 'totalDebt' in info and 'totalAssets' in info:
                if info['totalAssets']:
                    metrics['Debt_To_Assets'] = info['totalDebt'] / info['totalAssets']
                else:
                    metrics['Debt_To_Assets'] = None
            else:
                metrics['Debt_To_Assets'] = None
            
            # Interest Coverage Ratio
            if 'ebit' in info and 'interestExpense' in info:
                if info['interestExpense'] and info['interestExpense'] != 0:
                    metrics['Interest_Coverage'] = info['ebit'] / abs(info['interestExpense'])
                else:
                    metrics['Interest_Coverage'] = None
            else:
                metrics['Interest_Coverage'] = None
            
            # Financial Leverage Ratio
            if 'totalAssets' in info and 'totalStockholderEquity' in info:
                if info['totalStockholderEquity']:
                    metrics['Financial_Leverage'] = info['totalAssets'] / info['totalStockholderEquity']
                else:
                    metrics['Financial_Leverage'] = None
            else:
                metrics['Financial_Leverage'] = None
            
        except Exception as e:
            self.logger.error(f"Error calculating leverage metrics: {e}")
        
        return metrics
    
    def compare_with_sector(self, metrics: Dict[str, Dict[str, float]], 
                          sector: str) -> Dict[str, float]:
        """So sánh các chỉ số với trung bình ngành"""
        comparison = {}
        
        try:
            if sector not in self.industry_benchmarks:
                self.logger.warning(f"No benchmarks available for sector: {sector}")
                return comparison
            
            benchmarks = self.industry_benchmarks[sector]
            
            # Compare valuation metrics
            if 'valuation_metrics' in metrics:
                for metric, value in metrics['valuation_metrics'].items():
                    if value is not None and metric in benchmarks:
                        benchmark_value = benchmarks[metric]
                        if benchmark_value and benchmark_value != 0:
                            comparison[f'{metric}_vs_Sector'] = (value - benchmark_value) / benchmark_value
            
            # Compare profitability metrics
            if 'profitability_metrics' in metrics:
                for metric, value in metrics['profitability_metrics'].items():
                    if value is not None and metric in benchmarks:
                        benchmark_value = benchmarks[metric]
                        if benchmark_value and benchmark_value != 0:
                            comparison[f'{metric}_vs_Sector'] = (value - benchmark_value) / benchmark_value
            
        except Exception as e:
            self.logger.error(f"Error comparing with sector: {e}")
        
        return comparison
    
    def calculate_overall_score(self, metrics: Dict[str, Dict[str, float]], 
                              sector: str) -> Tuple[float, str]:
        """Tính toán điểm tổng hợp và xếp hạng đầu tư"""
        score = 0
        total_weights = 0
        
        try:
            # Valuation Score (30% weight)
            if 'valuation_metrics' in metrics:
                val_metrics = metrics['valuation_metrics']
                val_score = 0
                val_count = 0
                
                if val_metrics.get('PE_Ratio') and val_metrics['PE_Ratio'] > 0:
                    if val_metrics['PE_Ratio'] < 15:  # Good PE
                        val_score += 20
                    elif val_metrics['PE_Ratio'] < 25:
                        val_score += 10
                    val_count += 1
                
                if val_metrics.get('PB_Ratio') and val_metrics['PB_Ratio'] > 0:
                    if val_metrics['PB_Ratio'] < 2:  # Good PB
                        val_score += 20
                    elif val_metrics['PB_Ratio'] < 3:
                        val_score += 10
                    val_count += 1
                
                if val_count > 0:
                    score += (val_score / val_count) * 0.3
                    total_weights += 0.3
            
            # Profitability Score (35% weight)
            if 'profitability_metrics' in metrics:
                prof_metrics = metrics['profitability_metrics']
                prof_score = 0
                prof_count = 0
                
                if prof_metrics.get('ROE') and prof_metrics['ROE'] > 0:
                    if prof_metrics['ROE'] > 0.15:  # Good ROE
                        prof_score += 25
                    elif prof_metrics['ROE'] > 0.10:
                        prof_score += 15
                    prof_count += 1
                
                if prof_metrics.get('ROA') and prof_metrics['ROA'] > 0:
                    if prof_metrics['ROA'] > 0.08:  # Good ROA
                        prof_score += 20
                    elif prof_metrics['ROA'] > 0.05:
                        prof_score += 12
                    prof_count += 1
                
                if prof_metrics.get('Net_Margin') and prof_metrics['Net_Margin'] > 0:
                    if prof_metrics['Net_Margin'] > 0.10:
                        prof_score += 15
                    elif prof_metrics['Net_Margin'] > 0.05:
                        prof_score += 8
                    prof_count += 1
                
                if prof_count > 0:
                    score += (prof_score / prof_count) * 0.35
                    total_weights += 0.35
            
            # Growth Score (20% weight)
            if 'growth_metrics' in metrics:
                growth_metrics = metrics['growth_metrics']
                growth_score = 0
                growth_count = 0
                
                if growth_metrics.get('Revenue_Growth') and growth_metrics['Revenue_Growth'] > 0:
                    if growth_metrics['Revenue_Growth'] > 0.15:
                        growth_score += 25
                    elif growth_metrics['Revenue_Growth'] > 0.05:
                        growth_score += 15
                    growth_count += 1
                
                if growth_count > 0:
                    score += (growth_score / growth_count) * 0.20
                    total_weights += 0.20
            
            # Financial Health Score (15% weight)
            health_score = 0
            health_count = 0
            
            # Liquidity check
            if 'liquidity_metrics' in metrics:
                current_ratio = metrics['liquidity_metrics'].get('Current_Ratio')
                if current_ratio and current_ratio > 1.5:
                    health_score += 15
                elif current_ratio and current_ratio > 1.0:
                    health_score += 10
                health_count += 1
            
            # Leverage check
            if 'leverage_metrics' in metrics:
                debt_to_equity = metrics['leverage_metrics'].get('Debt_To_Equity')
                if debt_to_equity and debt_to_equity < 0.5:
                    health_score += 15
                elif debt_to_equity and debt_to_equity < 1.0:
                    health_score += 10
                health_count += 1
            
            if health_count > 0:
                score += (health_score / health_count) * 0.15
                total_weights += 0.15
            
            # Normalize score if not all weights were used
            if total_weights > 0:
                score = score / total_weights
            
            # Determine investment grade
            if score >= 80:
                grade = "STRONG_BUY"
            elif score >= 65:
                grade = "BUY"
            elif score >= 50:
                grade = "HOLD"
            elif score >= 35:
                grade = "WEAK_HOLD"
            else:
                grade = "SELL"
            
        except Exception as e:
            self.logger.error(f"Error calculating overall score: {e}")
            score = 0
            grade = "UNKNOWN"
        
        return score, grade
    
    def perform_comprehensive_analysis(self, financial_data: Dict[str, Any], 
                                     market_data: Dict[str, Any],
                                     sector: str) -> FinancialMetrics:
        """Thực hiện phân tích tài chính toàn diện"""
        try:
            # Calculate all metric categories
            valuation_metrics = self.calculate_valuation_metrics(financial_data, market_data)
            profitability_metrics = self.calculate_profitability_metrics(financial_data)
            efficiency_metrics = self.calculate_efficiency_metrics(financial_data)
            growth_metrics = self.calculate_growth_metrics(financial_data)
            liquidity_metrics = self.calculate_liquidity_metrics(financial_data)
            leverage_metrics = self.calculate_leverage_metrics(financial_data)
            
            # Compile all metrics
            all_metrics = {
                'valuation_metrics': valuation_metrics,
                'profitability_metrics': profitability_metrics,
                'efficiency_metrics': efficiency_metrics,
                'growth_metrics': growth_metrics,
                'liquidity_metrics': liquidity_metrics,
                'leverage_metrics': leverage_metrics
            }
            
            # Compare with sector
            sector_comparison = self.compare_with_sector(all_metrics, sector)
            
            # Calculate overall score and grade
            overall_score, investment_grade = self.calculate_overall_score(all_metrics, sector)
            
            result = FinancialMetrics(
                valuation_metrics=valuation_metrics,
                profitability_metrics=profitability_metrics,
                efficiency_metrics=efficiency_metrics,
                growth_metrics=growth_metrics,
                liquidity_metrics=liquidity_metrics,
                leverage_metrics=leverage_metrics,
                sector_comparison=sector_comparison,
                overall_score=overall_score,
                investment_grade=investment_grade
            )
            
            self.logger.info(f"Comprehensive financial analysis completed with score: {overall_score}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in comprehensive financial analysis: {e}")
            return FinancialMetrics(
                valuation_metrics={},
                profitability_metrics={},
                efficiency_metrics={},
                growth_metrics={},
                liquidity_metrics={},
                leverage_metrics={},
                sector_comparison={},
                overall_score=0,
                investment_grade="ERROR"
            )

def test_comprehensive_financial_analyzer():
    """Test function cho Comprehensive Financial Analyzer"""
    print("🧪 Testing Comprehensive Financial Analyzer...")
    
    try:
        # Tạo mock financial data
        np.random.seed(42)
        
        financial_data = {
            'info': {
                'trailingPE': np.random.uniform(10, 30),
                'priceToBook': np.random.uniform(1, 4),
                'returnOnEquity': np.random.uniform(0.05, 0.25),
                'returnOnAssets': np.random.uniform(0.02, 0.15),
                'profitMargins': np.random.uniform(0.05, 0.20),
                'operatingMargins': np.random.uniform(0.10, 0.25),
                'grossMargins': np.random.uniform(0.20, 0.50),
                'revenueGrowth': np.random.uniform(-0.1, 0.3),
                'currentRatio': np.random.uniform(1.0, 3.0),
                'debtToEquity': np.random.uniform(0.1, 1.0),
                'totalRevenue': np.random.uniform(1000000, 100000000),
                'totalAssets': np.random.uniform(5000000, 500000000),
                'totalStockholderEquity': np.random.uniform(2000000, 200000000),
                'marketCap': np.random.uniform(1000000000, 100000000000)
            }
        }
        
        market_data = {
            'current_price': 50000,
            'volume': 1000000
        }
        
        # Initialize analyzer
        analyzer = ComprehensiveFinancialAnalyzer()
        
        # Perform comprehensive analysis
        print("🔍 Performing comprehensive financial analysis...")
        result = analyzer.perform_comprehensive_analysis(financial_data, market_data, 'Technology')
        
        # Display results
        print(f"📊 Financial Analysis Results:")
        print(f"   Investment Grade: {result.investment_grade}")
        print(f"   Overall Score: {result.overall_score:.1f}/100")
        
        print(f"\n💰 Valuation Metrics:")
        for metric, value in result.valuation_metrics.items():
            if value is not None:
                print(f"   {metric}: {value:.2f}")
        
        print(f"\n📈 Profitability Metrics:")
        for metric, value in result.profitability_metrics.items():
            if value is not None:
                print(f"   {metric}: {value:.2%}" if 'Ratio' not in metric and 'Margin' not in metric else f"   {metric}: {value:.2f}")
        
        print(f"\n📊 Growth Metrics:")
        for metric, value in result.growth_metrics.items():
            if value is not None:
                print(f"   {metric}: {value:.2%}")
        
        print(f"\n💧 Liquidity Metrics:")
        for metric, value in result.liquidity_metrics.items():
            if value is not None:
                print(f"   {metric}: {value:.2f}")
        
        print(f"\n🏦 Leverage Metrics:")
        for metric, value in result.leverage_metrics.items():
            if value is not None:
                print(f"   {metric}: {value:.2f}")
        
        print(f"\n🏭 Sector Comparison:")
        for metric, value in result.sector_comparison.items():
            if value is not None:
                print(f"   {metric}: {value:+.1%}")
        
        print(f"\n✅ Comprehensive Financial Analyzer test completed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_comprehensive_financial_analyzer()