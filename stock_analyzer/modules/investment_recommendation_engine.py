"""
Investment Recommendation Engine - Hệ thống khuyến nghị đầu tư toàn diện
Tích hợp tất cả các phân tích để đưa ra mức giá mục tiêu và khuyến nghị đầu tư

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
class PriceTarget:
    """Cấu trúc dữ liệu cho mức giá mục tiêu"""
    method: str           # 'DCF', 'P/E', 'P/B', 'TECHNICAL', 'COMPOSITE'
    target_price: float
    confidence: float     # 0-1
    time_horizon: str     # '3M', '6M', '12M'
    reasoning: List[str]
    key_assumptions: List[str]

@dataclass
class InvestmentRecommendation:
    """Cấu trúc dữ liệu cho khuyến nghị đầu tư"""
    symbol: str
    current_price: float
    recommendation: str   # 'STRONG_BUY', 'BUY', 'HOLD', 'SELL', 'STRONG_SELL'
    confidence: float     # 0-1
    price_targets: List[PriceTarget]
    entry_points: Dict[str, float]  # 'conservative', 'moderate', 'aggressive'
    exit_points: Dict[str, float]   # 'stop_loss', 'take_profit'
    risk_reward_ratio: float
    time_horizon: str
    portfolio_weight: Optional[float]  # Recommended portfolio allocation
    key_risks: List[str]
    key_catalysts: List[str]
    overall_reasoning: str

class InvestmentRecommendationEngine:
    """Hệ thống khuyến nghị đầu tư toàn diện"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Market constants for Vietnam
        self.market_constants = {
            'risk_free_rate': 0.06,    # 6% risk-free rate (Vietnam 10Y bond)
            'market_risk_premium': 0.08,  # 8% market risk premium
            'beta_adjustment': 1.2,    # Vietnam market beta adjustment
            'terminal_growth_rate': 0.03,  # 3% terminal growth
            'discount_rate_range': (0.10, 0.15)  # 10-15% discount rate range
        }
        
        # Valuation multiples by sector (Vietnam market)
        self.sector_multiples = {
            'Banking': {'PE_range': (8, 15), 'PB_range': (0.8, 1.5), 'PEG_range': (0.8, 1.2)},
            'Technology': {'PE_range': (15, 30), 'PB_range': (2, 5), 'PEG_range': (1, 2)},
            'Real Estate': {'PE_range': (8, 20), 'PB_range': (0.8, 2), 'PEG_range': (0.8, 1.5)},
            'Food & Beverage': {'PE_range': (12, 25), 'PB_range': (1.5, 4), 'PEG_range': (1, 1.8)},
            'Oil & Gas': {'PE_range': (6, 15), 'PB_range': (0.8, 2), 'PEG_range': (0.6, 1.2)},
            'Steel': {'PE_range': (8, 18), 'PB_range': (1, 2.5), 'PEG_range': (0.8, 1.3)},
            'Pharmaceutical': {'PE_range': (12, 25), 'PB_range': (1.5, 3), 'PEG_range': (1, 1.8)},
            'Securities': {'PE_range': (10, 20), 'PB_range': (1, 2.5), 'PEG_range': (0.8, 1.5)},
            'Insurance': {'PE_range': (8, 18), 'PB_range': (0.8, 2), 'PEG_range': (0.8, 1.4)},
            'Agriculture': {'PE_range': (10, 20), 'PB_range': (1, 2.5), 'PEG_range': (0.8, 1.5)}
        }
    
    def calculate_dcf_target(self, financial_data: Dict[str, Any], 
                           market_data: Dict[str, Any],
                           sector: str) -> Optional[PriceTarget]:
        """Tính toán giá mục tiêu bằng phương pháp DCF"""
        try:
            info = financial_data.get('info', {})
            
            # Extract key financial metrics
            free_cash_flow = info.get('freeCashflow', None)
            if not free_cash_flow or free_cash_flow <= 0:
                # Estimate FCF if not available
                net_income = info.get('netIncome', 0)
                depreciation = info.get('totalCash', 0) * 0.1  # Rough estimate
                capex = info.get('capitalExpenditure', 0)
                free_cash_flow = net_income + depreciation - capex
            
            if not free_cash_flow or free_cash_flow <= 0:
                return None
            
            # Growth assumptions
            if 'revenueGrowth' in info and info['revenueGrowth']:
                short_term_growth = min(info['revenueGrowth'], 0.15)  # Cap at 15%
            else:
                short_term_growth = 0.08  # Default 8%
            
            long_term_growth = self.market_constants['terminal_growth_rate']
            
            # Discount rate calculation (WACC approximation)
            discount_rate = 0.12  # 12% base rate
            if 'beta' in info:
                beta = info['beta']
                market_rp = self.market_constants['market_risk_premium']
                risk_free_rate = self.market_constants['risk_free_rate']
                discount_rate = risk_free_rate + beta * market_rp
            
            # DCF calculation
            forecast_years = 5
            projected_fcf = []
            current_fcf = free_cash_flow
            
            for year in range(1, forecast_years + 1):
                if year <= 2:
                    growth_rate = short_term_growth
                elif year <= 4:
                    growth_rate = short_term_growth * 0.7  # Gradual decline
                else:
                    growth_rate = long_term_growth
                
                current_fcf *= (1 + growth_rate)
                projected_fcf.append(current_fcf)
            
            # Terminal value
            terminal_fcf = projected_fcf[-1] * (1 + long_term_growth)
            terminal_value = terminal_fcf / (discount_rate - long_term_growth)
            
            # Present value calculation
            pv_fcf = sum([fcf / ((1 + discount_rate) ** year) 
                         for year, fcf in enumerate(projected_fcf, 1)])
            pv_terminal = terminal_value / ((1 + discount_rate) ** forecast_years)
            
            # Enterprise value to equity value
            total_debt = info.get('totalDebt', 0)
            cash = info.get('totalCash', 0)
            shares_outstanding = info.get('sharesOutstanding', 1)
            
            enterprise_value = pv_fcf + pv_terminal
            equity_value = enterprise_value - total_debt + cash
            target_price = equity_value / shares_outstanding if shares_outstanding > 0 else 0
            
            # Confidence calculation
            confidence_factors = []
            if info.get('revenueGrowth'):
                confidence_factors.append(0.8)
            if info.get('freeCashflow'):
                confidence_factors.append(0.9)
            if 'beta' in info:
                confidence_factors.append(0.7)
            
            confidence = np.mean(confidence_factors) if confidence_factors else 0.5
            
            reasoning = [
                f"DCF based on {forecast_years}-year forecast",
                f"Short-term growth: {short_term_growth:.1%}",
                f"Terminal growth: {long_term_growth:.1%}",
                f"Discount rate: {discount_rate:.1%}"
            ]
            
            assumptions = [
                f"FCF growth rate: {short_term_growth:.1%}",
                f"Terminal growth rate: {long_term_growth:.1%}",
                f"Discount rate: {discount_rate:.1%}"
            ]
            
            return PriceTarget(
                method='DCF',
                target_price=target_price,
                confidence=confidence,
                time_horizon='12M',
                reasoning=reasoning,
                key_assumptions=assumptions
            )
            
        except Exception as e:
            self.logger.error(f"Error calculating DCF target: {e}")
            return None
    
    def calculate_multiple_targets(self, financial_data: Dict[str, Any],
                                 market_data: Dict[str, Any],
                                 sector: str) -> List[PriceTarget]:
        """Tính toán giá mục tiêu bằng phương pháp multiples"""
        targets = []
        
        try:
            info = financial_data.get('info', {})
            current_price = market_data.get('current_price', 0)
            
            if sector not in self.sector_multiples:
                return targets
            
            multiples = self.sector_multiples[sector]
            
            # P/E based target
            eps = info.get('trailingEps', None)
            if eps and eps > 0:
                pe_range = multiples['PE_range']
                target_pe_conservative = pe_range[0]
                target_pe_aggressive = pe_range[1]
                
                pe_conservative_price = eps * target_pe_conservative
                pe_aggressive_price = eps * target_pe_aggressive
                
                # Confidence based on earnings quality
                confidence = 0.8 if info.get('profitMargins', 0) > 0.05 else 0.6
                
                targets.append(PriceTarget(
                    method='P/E',
                    target_price=pe_aggressive_price,
                    confidence=confidence,
                    time_horizon='6M',
                    reasoning=[
                        f"P/E multiple analysis using sector range {pe_range[0]}-{pe_range[1]}",
                        f"Current EPS: {eps:.2f}",
                        f"Target P/E: {target_pe_aggressive:.1f}x"
                    ],
                    key_assumptions=[
                        f"EPS will be maintained at {eps:.2f}",
                        f"Sector P/E multiple range: {pe_range[0]}-{pe_range[1]}x"
                    ]
                ))
            
            # P/B based target
            book_value = info.get('bookValue', None)
            if book_value and book_value > 0:
                pb_range = multiples['PB_range']
                target_pb_median = (pb_range[0] + pb_range[1]) / 2
                
                pb_target_price = book_value * target_pb_median
                
                # Confidence based on ROE
                roe = info.get('returnOnEquity', 0)
                confidence = 0.9 if roe > 0.15 else 0.7 if roe > 0.10 else 0.5
                
                targets.append(PriceTarget(
                    method='P/B',
                    target_price=pb_target_price,
                    confidence=confidence,
                    time_horizon='6M',
                    reasoning=[
                        f"P/B multiple analysis using sector range {pb_range[0]}-{pb_range[1]}",
                        f"Book value per share: {book_value:.2f}",
                        f"Target P/B: {target_pb_median:.1f}x"
                    ],
                    key_assumptions=[
                        f"Book value will grow at ROE rate",
                        f"Sector P/B multiple range: {pb_range[0]}-{pb_range[1]}x"
                    ]
                ))
            
            # PEG based target
            growth_rate = info.get('revenueGrowth', 0.08)
            if growth_rate and growth_rate > 0:
                peg_range = multiples['PEG_range']
                target_peg = peg_range[1]  # Use upper range for target
                
                if eps and eps > 0:
                    peg_target_price = eps * (target_peg * (1 + growth_rate))
                    
                    confidence = 0.8 if growth_rate > 0.10 else 0.6
                    
                    targets.append(PriceTarget(
                        method='PEG',
                        target_price=peg_target_price,
                        confidence=confidence,
                        time_horizon='12M',
                        reasoning=[
                            f"PEG analysis with growth rate {growth_rate:.1%}",
                            f"Target PEG: {target_peg:.1f}x"
                        ],
                        key_assumptions=[
                            f"Revenue growth will be {growth_rate:.1%}",
                            f"Target PEG multiple: {target_peg:.1f}x"
                        ]
                    ))
            
        except Exception as e:
            self.logger.error(f"Error calculating multiple targets: {e}")
        
        return targets
    
    def calculate_technical_targets(self, technical_data: Dict[str, Any],
                                  market_data: Dict[str, Any]) -> List[PriceTarget]:
        """Tính toán giá mục tiêu dựa trên phân tích kỹ thuật"""
        targets = []
        
        try:
            current_price = market_data.get('current_price', 0)
            if not current_price:
                return targets
            
            # Support and Resistance based targets
            support_resistance = technical_data.get('support_resistance', {})
            if support_resistance:
                resistance = support_resistance.get('resistance', current_price * 1.1)
                
                targets.append(PriceTarget(
                    method='TECHNICAL',
                    target_price=resistance,
                    confidence=0.7,
                    time_horizon='3M',
                    reasoning=[
                        f"Technical resistance level: {resistance:.2f}",
                        f"Current price: {current_price:.2f}",
                        f"Potential upside: {((resistance - current_price) / current_price * 100):.1f}%"
                    ],
                    key_assumptions=[
                        "Price will test resistance level",
                        "Technical patterns will play out"
                    ]
                ))
            
            # Moving Average targets
            latest_values = technical_data.get('latest_values', {})
            sma_20 = latest_values.get('SMA_20', None)
            sma_50 = latest_values.get('SMA_50', None)
            
            if sma_20 and sma_50:
                if current_price > sma_20 > sma_50:
                    # Bullish alignment
                    target_price = sma_20 * 1.05  # 5% above SMA20
                    
                    targets.append(PriceTarget(
                        method='TECHNICAL',
                        target_price=target_price,
                        confidence=0.6,
                        time_horizon='6M',
                        reasoning=[
                            f"Bullish moving average alignment",
                            f"Target: 5% above SMA20 ({sma_20:.2f})"
                        ],
                        key_assumptions=[
                            "Bullish trend will continue",
                            "Price will respect moving average support"
                        ]
                    ))
            
        except Exception as e:
            self.logger.error(f"Error calculating technical targets: {e}")
        
        return targets
    
    def calculate_composite_target(self, all_targets: List[PriceTarget],
                                 current_price: float) -> PriceTarget:
        """Tính toán giá mục tiêu tổng hợp"""
        if not all_targets:
            return PriceTarget(
                method='COMPOSITE',
                target_price=current_price,
                confidence=0.0,
                time_horizon='6M',
                reasoning=['No target price could be calculated'],
                key_assumptions=[]
            )
        
        # Weight targets by confidence and method reliability
        method_weights = {
            'DCF': 0.4,
            'P/E': 0.25,
            'P/B': 0.2,
            'PEG': 0.1,
            'TECHNICAL': 0.05
        }
        
        weighted_prices = []
        total_weight = 0
        
        for target in all_targets:
            method_weight = method_weights.get(target.method, 0.1)
            combined_weight = method_weight * target.confidence
            
            weighted_prices.append(target.target_price * combined_weight)
            total_weight += combined_weight
        
        if total_weight > 0:
            composite_price = sum(weighted_prices) / total_weight
            composite_confidence = np.mean([t.confidence for t in all_targets])
        else:
            composite_price = current_price
            composite_confidence = 0.0
        
        # Calculate upside potential
        upside_potential = (composite_price - current_price) / current_price if current_price > 0 else 0
        
        reasoning = [
            f"Composite target based on {len(all_targets)} methodologies",
            f"Weighted average with method-specific reliability",
            f"Upside potential: {upside_potential:.1%}"
        ]
        
        return PriceTarget(
            method='COMPOSITE',
            target_price=composite_price,
            confidence=composite_confidence,
            time_horizon='6M',
            reasoning=reasoning,
            key_assumptions=[
                "Multiple valuation methods converge",
                "Market conditions remain stable"
            ]
        )
    
    def calculate_entry_exit_points(self, current_price: float, 
                                  composite_target: PriceTarget,
                                  technical_data: Dict[str, Any]) -> Tuple[Dict[str, float], Dict[str, float]]:
        """Tính toán điểm entry và exit"""
        try:
            # Entry points based on risk tolerance
            upside_potential = (composite_target.target_price - current_price) / current_price
            
            entry_points = {
                'conservative': current_price * 0.95,  # 5% below current
                'moderate': current_price,              # Current price
                'aggressive': current_price * 1.02     # 2% above current
            }
            
            # Exit points
            stop_loss = current_price * 0.85  # 15% stop loss
            take_profit_1 = current_price + (composite_target.target_price - current_price) * 0.33
            take_profit_2 = current_price + (composite_target.target_price - current_price) * 0.67
            take_profit_3 = composite_target.target_price
            
            exit_points = {
                'stop_loss': stop_loss,
                'take_profit_1': take_profit_1,
                'take_profit_2': take_profit_2,
                'take_profit_3': take_profit_3
            }
            
            return entry_points, exit_points
            
        except Exception as e:
            self.logger.error(f"Error calculating entry/exit points: {e}")
            return {}, {}
    
    def calculate_risk_reward_ratio(self, current_price: float, 
                                  entry_price: float, target_price: float,
                                  stop_loss: float) -> float:
        """Tính toán tỷ lệ risk/reward"""
        try:
            potential_profit = target_price - entry_price
            potential_loss = entry_price - stop_loss
            
            if potential_loss <= 0:
                return 0.0
            
            risk_reward = potential_profit / potential_loss
            return max(0.0, risk_reward)
            
        except Exception as e:
            self.logger.error(f"Error calculating risk/reward ratio: {e}")
            return 0.0
    
    def generate_investment_recommendation(self, symbol: str,
                                         stock_info: Dict[str, Any],
                                         financial_data: Dict[str, Any],
                                         technical_data: Dict[str, Any],
                                         sentiment_data: Dict[str, Any]) -> InvestmentRecommendation:
        """Tạo khuyến nghị đầu tư toàn diện"""
        try:
            # Extract current market data
            current_price = stock_info.get('current_price', 0)
            sector = stock_info.get('sector', 'Unknown')
            
            # Calculate all price targets
            all_targets = []
            
            # DCF target
            dcf_target = self.calculate_dcf_target(financial_data, stock_info, sector)
            if dcf_target:
                all_targets.append(dcf_target)
            
            # Multiple-based targets
            multiple_targets = self.calculate_multiple_targets(financial_data, stock_info, sector)
            all_targets.extend(multiple_targets)
            
            # Technical targets
            technical_targets = self.calculate_technical_targets(technical_data, stock_info)
            all_targets.extend(technical_targets)
            
            # Composite target
            composite_target = self.calculate_composite_target(all_targets, current_price)
            
            # Entry and exit points
            entry_points, exit_points = self.calculate_entry_exit_points(
                current_price, composite_target, technical_data
            )
            
            # Calculate risk/reward ratio
            moderate_entry = entry_points.get('moderate', current_price)
            stop_loss = exit_points.get('stop_loss', current_price * 0.85)
            risk_reward_ratio = self.calculate_risk_reward_ratio(
                current_price, moderate_entry, composite_target.target_price, stop_loss
            )
            
            # Generate recommendation based on composite signals
            overall_score = 0
            
            # Technical score (0-40 points)
            tech_signals = technical_data.get('technical_signals', {})
            if tech_signals:
                tech_score = tech_signals.score if hasattr(tech_signals, 'score') else 0
                overall_score += max(0, min(40, tech_score + 20))
            
            # Financial score (0-35 points)
            if 'overall_score' in financial_data:
                fin_score = financial_data['overall_score']
                overall_score += fin_score * 0.35
            
            # Sentiment score (0-25 points)
            if sentiment_data and 'overall_sentiment' in sentiment_data:
                sentiment_score = sentiment_data['overall_sentiment']
                overall_score += max(0, min(25, (sentiment_score + 1) * 12.5))
            
            # Determine recommendation
            if overall_score >= 80:
                recommendation = 'STRONG_BUY'
            elif overall_score >= 65:
                recommendation = 'BUY'
            elif overall_score >= 50:
                recommendation = 'HOLD'
            elif overall_score >= 35:
                recommendation = 'WEAK_HOLD'
            else:
                recommendation = 'SELL'
            
            # Portfolio weight recommendation
            if recommendation in ['STRONG_BUY', 'BUY']:
                portfolio_weight = 0.05  # 5% of portfolio
            elif recommendation == 'HOLD':
                portfolio_weight = 0.03  # 3% of portfolio
            else:
                portfolio_weight = 0.01  # 1% of portfolio
            
            # Key risks and catalysts
            key_risks = []
            key_catalysts = []
            
            if sector in ['Banking']:
                key_risks.append('Interest rate risk')
                key_risks.append('Credit quality deterioration')
                key_catalysts.append('Economic growth acceleration')
                key_catalysts.append('NPL resolution improvements')
            
            if sentiment_data and sentiment_data.get('sentiment_label') == 'NEGATIVE':
                key_risks.append('Negative market sentiment')
            
            # Overall reasoning
            overall_reasoning = [
                f"Technical Score: {overall_score:.0f}/100",
                f"Current Price: {current_price:.2f}",
                f"Target Price: {composite_target.target_price:.2f} ({((composite_target.target_price - current_price) / current_price * 100):+.1f}%)",
                f"Confidence Level: {composite_target.confidence:.1%}",
                f"Risk/Reward Ratio: {risk_reward_ratio:.2f}"
            ]
            
            return InvestmentRecommendation(
                symbol=symbol,
                current_price=current_price,
                recommendation=recommendation,
                confidence=composite_target.confidence,
                price_targets=all_targets,
                entry_points=entry_points,
                exit_points=exit_points,
                risk_reward_ratio=risk_reward_ratio,
                time_horizon=composite_target.time_horizon,
                portfolio_weight=portfolio_weight,
                key_risks=key_risks,
                key_catalysts=key_catalysts,
                overall_reasoning='; '.join(overall_reasoning)
            )
            
        except Exception as e:
            self.logger.error(f"Error generating investment recommendation for {symbol}: {e}")
            return InvestmentRecommendation(
                symbol=symbol,
                current_price=0,
                recommendation='ERROR',
                confidence=0,
                price_targets=[],
                entry_points={},
                exit_points={},
                risk_reward_ratio=0,
                time_horizon='6M',
                portfolio_weight=0,
                key_risks=[f"Error in analysis: {str(e)}"],
                key_catalysts=[],
                overall_reasoning="Unable to generate recommendation due to error"
            )

def test_investment_recommendation_engine():
    """Test function cho Investment Recommendation Engine"""
    print("🧪 Testing Investment Recommendation Engine...")
    
    try:
        # Initialize engine
        engine = InvestmentRecommendationEngine()
        
        # Create mock data
        np.random.seed(42)
        
        # Stock info
        stock_info = {
            'current_price': 50000,
            'sector': 'Technology',
            'volume': 1000000
        }
        
        # Financial data
        financial_data = {
            'info': {
                'trailingPE': 20.0,
                'priceToBook': 3.0,
                'returnOnEquity': 0.18,
                'returnOnAssets': 0.12,
                'profitMargins': 0.15,
                'revenueGrowth': 0.12,
                'freeCashflow': 500000000,
                'totalDebt': 200000000,
                'totalCash': 300000000,
                'sharesOutstanding': 10000000,
                'bookValue': 25000,
                'trailingEps': 2500
            },
            'overall_score': 75.0
        }
        
        # Technical data
        technical_data = {
            'support_resistance': {
                'resistance': 60000,
                'support': 45000
            },
            'latest_values': {
                'SMA_20': 48000,
                'SMA_50': 47000,
                'signal': 'BUY',
                'confidence': 0.7,
                'score': 25
            },
            'technical_signals': type('Signals', (), {'score': 25})()
        }
        
        # Sentiment data
        sentiment_data = {
            'overall_sentiment': 0.3,
            'sentiment_label': 'POSITIVE',
            'confidence': 0.8
        }
        
        # Generate recommendation
        print("🎯 Generating investment recommendation...")
        recommendation = engine.generate_investment_recommendation(
            'FPT', stock_info, financial_data, technical_data, sentiment_data
        )
        
        # Display results
        print(f"\n📊 Investment Recommendation for {recommendation.symbol}:")
        print(f"   Current Price: {recommendation.current_price:,.0f} VND")
        print(f"   Recommendation: {recommendation.recommendation}")
        print(f"   Confidence: {recommendation.confidence:.1%}")
        print(f"   Risk/Reward Ratio: {recommendation.risk_reward_ratio:.2f}")
        print(f"   Time Horizon: {recommendation.time_horizon}")
        print(f"   Portfolio Weight: {recommendation.portfolio_weight:.1%}")
        
        print(f"\n💰 Price Targets:")
        for target in recommendation.price_targets:
            print(f"   {target.method}: {target.target_price:,.0f} VND (Confidence: {target.confidence:.1%})")
        
        print(f"\n📈 Entry Points:")
        for point, price in recommendation.entry_points.items():
            print(f"   {point.title()}: {price:,.0f} VND")
        
        print(f"\n📉 Exit Points:")
        for point, price in recommendation.exit_points.items():
            print(f"   {point.replace('_', ' ').title()}: {price:,.0f} VND")
        
        if recommendation.key_risks:
            print(f"\n⚠️ Key Risks:")
            for risk in recommendation.key_risks:
                print(f"   - {risk}")
        
        if recommendation.key_catalysts:
            print(f"\n🚀 Key Catalysts:")
            for catalyst in recommendation.key_catalysts:
                print(f"   - {catalyst}")
        
        print(f"\n📋 Overall Reasoning:")
        print(f"   {recommendation.overall_reasoning}")
        
        print(f"\n✅ Investment Recommendation Engine test completed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_investment_recommendation_engine()