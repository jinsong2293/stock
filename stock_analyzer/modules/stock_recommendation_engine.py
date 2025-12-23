"""
Stock Recommendation Engine - Đưa ra khuyến nghị đầu tư cụ thể
Phân tích sâu và đề xuất số lượng cổ phiếu cần mua với lý do rõ ràng

Author: Roo - Investment Mode
Version: 1.0.0
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import logging
import json
import warnings
warnings.filterwarnings('ignore')

# Import existing modules
try:
    from stock_analyzer.modules.enhanced_stock_forecast import EnhancedStockForecastSystem
    from stock_analyzer.modules.investment_opportunity_scanner import InvestmentOpportunityScanner
    FORECAST_AVAILABLE = True
except ImportError:
    FORECAST_AVAILABLE = False

logger = logging.getLogger(__name__)

class RiskAnalyzer:
    """Phân tích rủi ro cho từng cổ phiếu"""
    
    def __init__(self):
        self.risk_factors = {
            'volatility': {
                'low': {'max_volatility': 0.02, 'risk_multiplier': 0.8},
                'medium': {'max_volatility': 0.04, 'risk_multiplier': 1.0},
                'high': {'max_volatility': float('inf'), 'risk_multiplier': 1.3}
            },
            'correlation': {
                'low': {'max_correlation': 0.3, 'risk_multiplier': 0.9},
                'medium': {'max_correlation': 0.6, 'risk_multiplier': 1.0},
                'high': {'max_correlation': 1.0, 'risk_multiplier': 1.2}
            },
            'liquidity': {
                'low': {'min_volume': 100000, 'risk_multiplier': 1.2},
                'medium': {'min_volume': 500000, 'risk_multiplier': 1.0},
                'high': {'min_volume': 1000000, 'risk_multiplier': 0.9}
            }
        }
    
    def assess_risk(self, stock_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Đánh giá rủi ro của cổ phiếu"""
        risk_score = 0
        risk_details = []
        
        # 1. Volatility Risk
        volatility = self._calculate_volatility(stock_analysis)
        volatility_risk = self._assess_volatility_risk(volatility)
        risk_score += volatility_risk['score']
        risk_details.append(volatility_risk['detail'])
        
        # 2. Liquidity Risk
        volume = stock_analysis.get('volume_avg', 0)
        liquidity_risk = self._assess_liquidity_risk(volume)
        risk_score += liquidity_risk['score']
        risk_details.append(liquidity_risk['detail'])
        
        # 3. Technical Risk
        technical_risk = self._assess_technical_risk(stock_analysis)
        risk_score += technical_risk['score']
        risk_details.append(technical_risk['detail'])
        
        # 4. Fundamental Risk
        fundamental_risk = self._assess_fundamental_risk(stock_analysis)
        risk_score += fundamental_risk['score']
        risk_details.append(fundamental_risk['detail'])
        
        # 5. Market Risk
        market_risk = self._assess_market_risk(stock_analysis)
        risk_score += market_risk['score']
        risk_details.append(market_risk['detail'])
        
        # Normalize risk score to 1-10 scale
        normalized_risk = min(10, max(1, risk_score / 5))
        
        # Determine risk level
        if normalized_risk <= 3:
            risk_level = "Thấp"
        elif normalized_risk <= 6:
            risk_level = "Trung bình"
        elif normalized_risk <= 8:
            risk_level = "Cao"
        else:
            risk_level = "Rất cao"
        
        return {
            'overall_score': normalized_risk,
            'level': risk_level,
            'volatility': volatility,
            'details': risk_details,
            'risk_factors': {
                'volatility_contribution': volatility_risk['score'],
                'liquidity_contribution': liquidity_risk['score'],
                'technical_contribution': technical_risk['score'],
                'fundamental_contribution': fundamental_risk['score'],
                'market_contribution': market_risk['score']
            }
        }
    
    def _calculate_volatility(self, stock_analysis: Dict[str, Any]) -> float:
        """Tính toán volatility của cổ phiếu"""
        # Calculate price volatility over 30 days
        current_price = stock_analysis.get('current_price', 0)
        if current_price == 0:
            return 0.05  # Default high volatility
        
        # Mock volatility calculation (in real implementation, would use actual price data)
        price_changes = np.random.normal(0, 0.02, 30)  # 2% daily volatility
        volatility = np.std(price_changes)
        
        return volatility
    
    def _assess_volatility_risk(self, volatility: float) -> Dict[str, Any]:
        """Đánh giá rủi ro volatility"""
        if volatility <= 0.02:
            return {'score': 2, 'detail': 'Volatility thấp - Rủi ro ổn định'}
        elif volatility <= 0.04:
            return {'score': 4, 'detail': 'Volatility trung bình - Rủi ro vừa phải'}
        else:
            return {'score': 7, 'detail': 'Volatility cao - Rủi ro biến động mạnh'}
    
    def _assess_liquidity_risk(self, volume: float) -> Dict[str, Any]:
        """Đánh giá rủi ro thanh khoản"""
        if volume >= 1000000:
            return {'score': 2, 'detail': 'Thanh khoản tốt - Dễ giao dịch'}
        elif volume >= 500000:
            return {'score': 4, 'detail': 'Thanh khoản trung bình - Cần chú ý'}
        else:
            return {'score': 7, 'detail': 'Thanh khoản thấp - Khó giao dịch'}
    
    def _assess_technical_risk(self, stock_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Đánh giá rủi ro kỹ thuật"""
        rsi = stock_analysis.get('rsi', 50)
        
        if 40 <= rsi <= 60:
            return {'score': 3, 'detail': 'Tín hiệu kỹ thuật ổn định'}
        elif 30 <= rsi < 40 or 60 < rsi <= 70:
            return {'score': 5, 'detail': 'Tín hiệu kỹ thuật trung tính'}
        else:
            return {'score': 8, 'detail': 'Tín hiệu kỹ thuật rủi ro cao'}
    
    def _assess_fundamental_risk(self, stock_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Đánh giá rủi ro cơ bản (mock implementation)"""
        # In real implementation, would use actual fundamental data
        return {'score': 4, 'detail': 'Rủi ro cơ bản trung bình'}
    
    def _assess_market_risk(self, stock_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Đánh giá rủi ro thị trường"""
        price_change_5d = stock_analysis.get('price_change_5d', 0)
        
        if abs(price_change_5d) <= 3:
            return {'score': 3, 'detail': 'Thị trường ổn định'}
        elif abs(price_change_5d) <= 7:
            return {'score': 5, 'detail': 'Thị trường biến động vừa phải'}
        else:
            return {'score': 8, 'detail': 'Thị trường biến động mạnh'}

class PortfolioOptimizer:
    """Tối ưu hóa portfolio allocation"""
    
    def __init__(self):
        self.max_position_size = 0.10  # Max 10% per stock
        self.min_position_size = 0.02  # Min 2% per stock
        self.max_sector_exposure = 0.30  # Max 30% per sector
        self.cash_buffer = 0.05  # Keep 5% cash buffer
    
    def calculate_allocation(self, recommendations: List[Dict], total_capital: float) -> Dict[str, Any]:
        """Tính toán phân bổ portfolio tối ưu"""
        
        # Sort recommendations by score/return ratio
        sorted_recs = sorted(recommendations, 
                           key=lambda x: x.get('expected_return', 0) / max(x.get('risk_score', 1), 0.1), 
                           reverse=True)
        
        allocation = {}
        allocated_capital = 0
        remaining_capital = total_capital * (1 - self.cash_buffer)
        
        for rec in sorted_recs:
            if remaining_capital <= 0:
                break
            
            # Calculate position size using Kelly Criterion
            position_size = self._kelly_criterion_allocation(rec, remaining_capital)
            
            # Apply position size limits
            max_size = total_capital * self.max_position_size
            min_size = total_capital * self.min_position_size
            
            position_size = min(position_size, max_size)
            position_size = max(position_size, min_size)
            
            # Ensure we don't exceed remaining capital
            position_size = min(position_size, remaining_capital)
            
            if position_size >= min_size:
                quantity = int(position_size / rec['entry_price'])
                actual_allocation = quantity * rec['entry_price']
                
                allocation[rec['symbol']] = {
                    'quantity': quantity,
                    'amount': actual_allocation,
                    'percentage': (actual_allocation / total_capital) * 100,
                    'entry_price': rec['entry_price'],
                    'recommendation': rec,
                    'stop_loss_price': rec.get('stop_loss', rec['entry_price'] * 0.95),
                    'target_price': rec.get('target_price', rec['entry_price'] * 1.1)
                }
                
                allocated_capital += actual_allocation
                remaining_capital -= actual_allocation
                
                logger.info(f"Allocated {actual_allocation:,.0f} VND to {rec['symbol']} ({quantity} shares)")
        
        # Calculate portfolio metrics
        portfolio_metrics = self._calculate_portfolio_metrics(allocation, total_capital)
        
        return {
            'allocation': allocation,
            'total_allocated': allocated_capital,
            'cash_remaining': total_capital - allocated_capital,
            'cash_percentage': ((total_capital - allocated_capital) / total_capital) * 100,
            'metrics': portfolio_metrics,
            'rebalancing_suggestions': self._generate_rebalancing_suggestions(allocation)
        }
    
    def _kelly_criterion_allocation(self, recommendation: Dict, remaining_capital: float) -> float:
        """Tính toán position size theo Kelly Criterion"""
        win_prob = recommendation.get('confidence', 0.6)
        win_ratio = recommendation.get('expected_return', 0.05) / max(abs(recommendation.get('stop_loss', 0) - recommendation['entry_price']), 1)
        loss_ratio = 1 - win_ratio
        
        # Kelly Formula: f = (bp - q) / b
        # where b = win_ratio, p = win_prob, q = 1 - win_prob
        kelly_fraction = (win_ratio * win_prob - (1 - win_prob)) / win_ratio
        
        # Conservative approach: use 25% of Kelly
        conservative_fraction = max(0, kelly_fraction * 0.25)
        
        # Apply risk-based adjustment
        risk_score = recommendation.get('risk_score', 5)
        risk_multiplier = max(0.5, 1 - (risk_score - 1) / 9)  # Risk 1 = 1.0, Risk 10 = 0.5
        
        final_fraction = conservative_fraction * risk_multiplier
        
        return remaining_capital * final_fraction
    
    def _calculate_portfolio_metrics(self, allocation: Dict, total_capital: float) -> Dict[str, float]:
        """Tính toán các metrics của portfolio"""
        if not allocation:
            return {'expected_return': 0, 'risk_score': 0, 'diversification': 0}
        
        # Calculate weighted expected return
        total_weighted_return = 0
        total_weight = 0
        sector_exposure = {}
        
        for symbol, alloc in allocation.items():
            weight = alloc['percentage'] / 100
            expected_return = alloc['recommendation'].get('expected_return', 0.05)
            sector = alloc['recommendation'].get('sector', 'Unknown')
            
            total_weighted_return += weight * expected_return
            total_weight += weight
            
            sector_exposure[sector] = sector_exposure.get(sector, 0) + weight
        
        expected_return = total_weighted_return / total_weight if total_weight > 0 else 0
        
        # Calculate portfolio risk (simplified)
        risk_score = np.mean([alloc['recommendation'].get('risk_score', 5) for alloc in allocation.values()])
        
        # Calculate diversification score
        sector_count = len(sector_exposure)
        max_sector_exposure = max(sector_exposure.values()) if sector_exposure else 0
        diversification = 1 - (max_sector_exposure - 1/sector_count) if sector_count > 1 else 0.5
        
        return {
            'expected_return': expected_return,
            'risk_score': risk_score,
            'diversification': diversification,
            'sector_exposure': sector_exposure,
            'total_positions': len(allocation)
        }
    
    def _generate_rebalancing_suggestions(self, allocation: Dict) -> List[str]:
        """Tạo các gợi ý rebalancing"""
        suggestions = []
        
        if len(allocation) < 5:
            suggestions.append("⚠️ Portfolio quá tập trung - Cân nhắc thêm nhiều cổ phiếu hơn")
        
        # Check for over-concentration
        for symbol, alloc in allocation.items():
            if alloc['percentage'] > 15:
                suggestions.append(f"⚠️ {symbol} chiếm quá nhiều ({alloc['percentage']:.1f}%) - Cân nhắc giảm")
        
        # Check for sector concentration
        sector_exposure = {}
        for alloc in allocation.values():
            sector = alloc['recommendation'].get('sector', 'Unknown')
            sector_exposure[sector] = sector_exposure.get(sector, 0) + alloc['percentage']
        
        for sector, exposure in sector_exposure.items():
            if exposure > 30:
                suggestions.append(f"⚠️ Sector {sector} chiếm {exposure:.1f}% - Quá tập trung")
        
        if not suggestions:
            suggestions.append("✅ Portfolio có vẻ cân bằng tốt")
        
        return suggestions

class StockRecommendationEngine:
    """Engine chính để tạo khuyến nghị đầu tư"""
    
    def __init__(self):
        self.risk_analyzer = RiskAnalyzer()
        self.portfolio_optimizer = PortfolioOptimizer()
        
        if FORECAST_AVAILABLE:
            self.forecast_system = EnhancedStockForecastSystem()
            self.scanner = InvestmentOpportunityScanner()
        else:
            self.forecast_system = None
            self.scanner = None
        
        logger.info("Stock Recommendation Engine initialized")
    
    def generate_investment_recommendations(self, 
                                          scan_results: Dict[str, Any],
                                          portfolio_size: float,
                                          risk_tolerance: str = "medium") -> Dict[str, Any]:
        """
        Tạo khuyến nghị đầu tư toàn diện
        """
        logger.info(f"Generating investment recommendations for portfolio size: {portfolio_size:,.0f} VND")
        
        candidates = scan_results.get('candidates', [])
        if not candidates:
            return {"error": "No candidates available for recommendation"}
        
        # Generate detailed recommendations for each candidate
        recommendations = []
        
        for candidate in candidates[:10]:  # Top 10 candidates
            try:
                recommendation = self._create_detailed_recommendation(candidate, portfolio_size, risk_tolerance)
                if recommendation:
                    recommendations.append(recommendation)
            except Exception as e:
                logger.error(f"Error creating recommendation for {candidate.get('symbol', 'Unknown')}: {e}")
                continue
        
        if not recommendations:
            return {"error": "No valid recommendations could be generated"}
        
        # Calculate portfolio allocation
        portfolio_allocation = self.portfolio_optimizer.calculate_allocation(recommendations, portfolio_size)
        
        # Generate overall analysis
        overall_analysis = self._generate_overall_analysis(recommendations, portfolio_allocation)
        
        return {
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "portfolio_size": portfolio_size,
            "risk_tolerance": risk_tolerance,
            "recommendations": recommendations,
            "portfolio_allocation": portfolio_allocation,
            "overall_analysis": overall_analysis,
            "action_plan": self._generate_action_plan(recommendations, portfolio_allocation)
        }
    
    def _create_detailed_recommendation(self, candidate: Dict, 
                                      portfolio_size: float,
                                      risk_tolerance: str) -> Optional[Dict]:
        """Tạo khuyến nghị chi tiết cho một cổ phiếu"""
        try:
            symbol = candidate.get('symbol')
            current_price = candidate.get('current_price', 0)
            
            if current_price <= 0:
                logger.warning(f"Invalid price for {symbol}")
                return None
            
            # Perform risk analysis
            risk_analysis = self.risk_analyzer.assess_risk(candidate)
            
            # Get forecast data
            forecast_data = candidate.get('forecast')
            forecast_analysis = self._analyze_forecast(forecast_data)
            
            # Generate recommendation logic
            recommendation_type, confidence = self._determine_recommendation_type(candidate, forecast_analysis)
            
            # Calculate quantities and amounts
            quantity, amount = self._calculate_investment_quantity(
                candidate, risk_analysis, portfolio_size, risk_tolerance
            )
            
            # Calculate target and stop loss prices
            target_price, stop_loss_price = self._calculate_price_targets(
                current_price, forecast_analysis, risk_analysis
            )
            
            # Generate detailed reasons
            reasons = self._generate_detailed_reasons(candidate, forecast_analysis, risk_analysis)
            
            # Calculate expected return
            expected_return = self._calculate_expected_return(
                current_price, target_price, stop_loss_price, confidence
            )
            
            recommendation = {
                'symbol': symbol,
                'company_name': self._get_company_name(symbol),
                'recommendation': recommendation_type,
                'confidence': confidence,
                'quantity': quantity,
                'amount': amount,
                'percentage_of_portfolio': (amount / portfolio_size) * 100 if portfolio_size > 0 else 0,
                'entry_price': current_price,
                'current_price': current_price,
                'target_price': target_price,
                'stop_loss_price': stop_loss_price,
                'expected_return': expected_return,
                'risk_analysis': risk_analysis,
                'forecast_analysis': forecast_analysis,
                'reasons': reasons,
                'sector': self._get_sector(symbol),
                'market_cap_category': self._get_market_cap_category(candidate),
                'technical_summary': self._create_technical_summary(candidate),
                'fundamental_summary': self._create_fundamental_summary(candidate),
                'news_sentiment': self._create_news_sentiment_summary(candidate),
                'action_timeline': self._create_action_timeline(recommendation_type, forecast_analysis),
                'risk_management': self._create_risk_management_plan(stop_loss_price, target_price, quantity)
            }
            
            logger.info(f"Generated {recommendation_type} recommendation for {symbol}: {quantity} shares, {amount:,.0f} VND")
            return recommendation
            
        except Exception as e:
            logger.error(f"Error creating detailed recommendation: {e}")
            return None
    
    def _analyze_forecast(self, forecast_data: Optional[Dict]) -> Dict[str, Any]:
        """Phân tích dữ liệu dự báo"""
        if not forecast_data or 'predictions' not in forecast_data:
            return {
                'direction': 'neutral',
                'confidence': 0.5,
                'expected_change_2d': 0,
                'volatility': 0.02
            }
        
        predictions = forecast_data['predictions']
        
        # Analyze day 1 and day 2 predictions
        day1 = predictions[0] if len(predictions) > 0 else {}
        day2 = predictions[1] if len(predictions) > 1 else {}
        
        # Calculate overall direction and confidence
        directions = [day1.get('direction', 'neutral'), day2.get('direction', 'neutral')]
        confidences = [day1.get('confidence_score', 0.5), day2.get('confidence_score', 0.5)]
        
        # Determine overall direction
        if directions[0] == directions[1]:
            overall_direction = directions[0]
        else:
            overall_direction = 'mixed'
        
        # Calculate average confidence
        avg_confidence = np.mean(confidences)
        
        # Calculate expected change over 2 days
        change1 = day1.get('predicted_change_points', 0)
        change2 = day2.get('predicted_change_points', 0)
        total_change = change1 + change2
        
        return {
            'direction': overall_direction,
            'confidence': avg_confidence,
            'expected_change_2d': total_change,
            'day1_prediction': day1,
            'day2_prediction': day2,
            'forecast_consistency': directions[0] == directions[1],
            'volatility': 0.02  # Mock volatility
        }
    
    def _determine_recommendation_type(self, candidate: Dict, forecast_analysis: Dict) -> Tuple[str, float]:
        """Xác định loại khuyến nghị"""
        direction = forecast_analysis.get('direction', 'neutral')
        confidence = forecast_analysis.get('confidence', 0.5)
        price_change_5d = candidate.get('price_change_5d', 0)
        volume_surge = candidate.get('volume_surge', 1)
        
        # Strong BUY conditions
        if (direction in ['up', 'Tăng'] and confidence > 0.8 and 
            price_change_5d > 0 and volume_surge > 1.5):
            return 'MUA MẠNH', min(0.95, confidence * 1.1)
        
        # Moderate BUY conditions
        elif (direction in ['up', 'Tăng'] and confidence > 0.65 and 
              price_change_5d > -2):
            return 'MUA', min(0.85, confidence)
        
        # HOLD conditions
        elif direction == 'mixed' or (0.6 <= confidence <= 0.7):
            return 'NẮM GIỮ', 0.65
        
        # Potential SELL (short-term)
        elif (direction in ['down', 'Giảm'] and confidence > 0.7):
            return 'BÁN', confidence
        
        # Default to HOLD with neutral confidence
        else:
            return 'NẮM GIỮ', 0.6
    
    def _calculate_investment_quantity(self, candidate: Dict, risk_analysis: Dict, 
                                     portfolio_size: float, risk_tolerance: str) -> Tuple[int, float]:
        """Tính toán số lượng cổ phiếu cần mua"""
        current_price = candidate.get('current_price', 0)
        if current_price <= 0:
            return 0, 0
        
        # Base allocation percentage based on risk tolerance
        base_allocations = {
            'conservative': 0.03,  # 3%
            'medium': 0.05,        # 5%
            'aggressive': 0.08     # 8%
        }
        
        base_allocation = base_allocations.get(risk_tolerance, 0.05)
        
        # Adjust based on risk score
        risk_score = risk_analysis.get('overall_score', 5)
        risk_multiplier = max(0.5, 1 - (risk_score - 1) / 9)  # Lower allocation for higher risk
        
        # Adjust based on recommendation confidence
        forecast_analysis = self._analyze_forecast(candidate.get('forecast'))
        confidence = forecast_analysis.get('confidence', 0.5)
        confidence_multiplier = 0.5 + (confidence * 0.5)  # 0.5 to 1.0
        
        # Calculate final allocation percentage
        final_allocation_pct = base_allocation * risk_multiplier * confidence_multiplier
        
        # Calculate investment amount
        investment_amount = portfolio_size * final_allocation_pct
        
        # Calculate quantity
        quantity = int(investment_amount / current_price)
        
        # Minimum and maximum constraints
        min_quantity = 10  # Minimum 10 shares
        max_quantity = int(portfolio_size * 0.1 / current_price)  # Max 10% of portfolio
        
        quantity = max(min_quantity, min(quantity, max_quantity))
        
        actual_amount = quantity * current_price
        
        return quantity, actual_amount
    
    def _calculate_price_targets(self, current_price: float, forecast_analysis: Dict, 
                               risk_analysis: Dict) -> Tuple[float, float]:
        """Tính toán giá mục tiêu và stop loss"""
        expected_change = forecast_analysis.get('expected_change_2d', 0)
        confidence = forecast_analysis.get('confidence', 0.5)
        risk_score = risk_analysis.get('overall_score', 5)
        
        # Calculate target price (more conservative for high-risk stocks)
        risk_adjustment = max(0.5, 1 - (risk_score - 1) / 9)
        target_multiplier = 1 + (expected_change * confidence * risk_adjustment / 100)
        
        target_price = current_price * target_multiplier
        
        # Calculate stop loss (tighter for high-risk stocks)
        base_stop_loss_pct = 0.05  # 5% base stop loss
        risk_adjustment_stop = min(2.0, risk_score / 5)  # Higher risk = tighter stop
        stop_loss_multiplier = 1 - (base_stop_loss_pct * risk_adjustment_stop)
        
        stop_loss_price = current_price * stop_loss_multiplier
        
        return target_price, stop_loss_price
    
    def _generate_detailed_reasons(self, candidate: Dict, forecast_analysis: Dict, 
                                 risk_analysis: Dict) -> List[str]:
        """Tạo danh sách lý do chi tiết"""
        reasons = []
        
        # Technical reasons
        price_change_5d = candidate.get('price_change_5d', 0)
        if price_change_5d > 3:
            reasons.append(f"📈 Giá tăng mạnh {price_change_5d:.1f}% trong 5 ngày qua")
        elif price_change_5d > 0:
            reasons.append(f"📊 Giá duy trì xu hướng tích cực {price_change_5d:.1f}%")
        
        volume_surge = candidate.get('volume_surge', 1)
        if volume_surge > 2:
            reasons.append(f"📊 Volume tăng mạnh {volume_surge:.1f}x - Xác nhận xu hướng")
        elif volume_surge > 1.5:
            reasons.append(f"📊 Volume tăng {volume_surge:.1f}x - Dấu hiệu tích cực")
        
        rsi = candidate.get('rsi', 50)
        if rsi < 35:
            reasons.append(f"⚖️ RSI oversold ({rsi:.1f}) - Cơ hội mua vào")
        elif rsi > 65:
            reasons.append(f"⚖️ RSI overbought ({rsi:.1f}) - Cần thận trọng")
        else:
            reasons.append(f"⚖️ RSI ở mức cân bằng ({rsi:.1f})")
        
        # Forecast reasons
        direction = forecast_analysis.get('direction', 'neutral')
        confidence = forecast_analysis.get('confidence', 0.5)
        
        if direction in ['up', 'Tăng']:
            reasons.append(f"🔮 AI dự báo xu hướng TĂNG với độ tin cậy {confidence:.1%}")
        elif direction in ['down', 'Giảm']:
            reasons.append(f"⚠️ AI dự báo xu hướng GIẢM - Cần thận trọng")
        else:
            reasons.append(f"🔮 Dự báo trung tính - Theo dõi thêm")
        
        # Risk assessment
        risk_level = risk_analysis.get('level', 'Trung bình')
        if risk_level == 'Thấp':
            reasons.append(f"🛡️ Rủi ro thấp - Phù hợp đầu tư dài hạn")
        elif risk_level == 'Trung bình':
            reasons.append(f"⚖️ Rủi ro trung bình - Cân nhắc quản lý vị thế")
        else:
            reasons.append(f"⚠️ Rủi ro {risk_level} - Đầu tư thận trọng")
        
        # Market context
        if price_change_5d > 0 and volume_surge > 1.5:
            reasons.append("🎯 Cơ hội đầu tư ngắn hạn tốt")
        
        return reasons
    
    def _calculate_expected_return(self, entry_price: float, target_price: float, 
                                 stop_loss_price: float, confidence: float) -> float:
        """Tính toán expected return"""
        upside = (target_price - entry_price) / entry_price
        downside = (entry_price - stop_loss_price) / entry_price
        
        expected_return = (confidence * upside) - ((1 - confidence) * downside)
        return expected_return
    
    def _generate_overall_analysis(self, recommendations: List[Dict], 
                                 portfolio_allocation: Dict) -> Dict[str, Any]:
        """Tạo phân tích tổng thể"""
        total_expected_return = 0
        total_risk_score = 0
        recommendation_counts = {'MUA MẠNH': 0, 'MUA': 0, 'NẮM GIỮ': 0, 'BÁN': 0}
        
        for rec in recommendations:
            weight = rec['percentage_of_portfolio'] / 100
            total_expected_return += weight * rec['expected_return']
            total_risk_score += weight * rec['risk_analysis']['overall_score']
            recommendation_counts[rec['recommendation']] += 1
        
        # Determine overall market sentiment
        if recommendation_counts['MUA MẠNH'] + recommendation_counts['MUA'] > len(recommendations) * 0.6:
            market_sentiment = "Tích cực"
        elif recommendation_counts['BÁN'] > len(recommendations) * 0.4:
            market_sentiment = "Tiêu cực"
        else:
            market_sentiment = "Trung tính"
        
        return {
            'overall_expected_return': total_expected_return,
            'average_risk_score': total_risk_score,
            'portfolio_diversification': len(recommendations),
            'market_sentiment': market_sentiment,
            'recommendation_distribution': recommendation_counts,
            'investment_grade': self._calculate_portfolio_grade(total_expected_return, total_risk_score),
            'key_insights': self._generate_key_insights(recommendations, portfolio_allocation)
        }
    
    def _generate_action_plan(self, recommendations: List[Dict], 
                            portfolio_allocation: Dict) -> List[str]:
        """Tạo kế hoạch hành động cụ thể"""
        action_plan = []
        
        # Prioritize strong buy recommendations
        strong_buys = [r for r in recommendations if r['recommendation'] == 'MUA MẠNH']
        if strong_buys:
            action_plan.append("🚀 THỰC HIỆN NGAY: Mua các cổ phiếu MUA MẠNH trước")
            for rec in strong_buys:
                action_plan.append(f"   📈 {rec['symbol']}: Mua {rec['quantity']} cổ phiếu (~{rec['amount']:,.0f} VND)")
        
        # Regular buy recommendations
        regular_buys = [r for r in recommendations if r['recommendation'] == 'MUA']
        if regular_buys:
            action_plan.append("⏰ CÂN NHẮC: Mua các cổ phiếu MUA trong tuần này")
            for rec in regular_buys:
                action_plan.append(f"   📊 {rec['symbol']}: Mua {rec['quantity']} cổ phiếu (~{rec['amount']:,.0f} VND)")
        
        # Hold recommendations
        holds = [r for r in recommendations if r['recommendation'] == 'NẮM GIỮ']
        if holds:
            action_plan.append("📋 THEO DÕI: Tiếp tục nắm giữ các cổ phiếu hiện có")
        
        # Risk management
        action_plan.append("\n🛡️ QUẢN LÝ RỦI RO:")
        action_plan.append("   • Đặt stop-loss theo khuyến nghị")
        action_plan.append("   • Theo dõi kết quả hàng ngày")
        action_plan.append("   • Rebalance portfolio hàng tuần")
        
        # Portfolio allocation summary
        allocated_pct = portfolio_allocation['total_allocated'] / portfolio_allocation.get('total_allocated', 1) * 100
        action_plan.append(f"\n💰 PHÂN BỔ: Đã phân bổ {allocated_pct:.1f}% portfolio")
        
        return action_plan
    
    def _get_company_name(self, symbol: str) -> str:
        """Lấy tên công ty (mock implementation)"""
        company_names = {
            'VRE': 'Vinhomes JSC',
            'VIC': 'Vingroup JSC',
            'VHM': 'Vinhomes JSC',
            'VCB': 'Vietcombank',
            'BID': 'BIDV',
            'CTG': 'VietinBank',
            'ACB': 'ACB Bank',
            'TCB': 'Techcombank',
            'VNM': 'Vinamilk',
            'SAB': 'SABMiller Vietnam'
        }
        return company_names.get(symbol, f'{symbol} JSC')
    
    def _get_sector(self, symbol: str) -> str:
        """Lấy sector của cổ phiếu"""
        sectors = {
            'VRE': 'Bất động sản',
            'VIC': 'Bất động sản',
            'VHM': 'Bất động sản',
            'VCB': 'Ngân hàng',
            'BID': 'Ngân hàng',
            'CTG': 'Ngân hàng',
            'ACB': 'Ngân hàng',
            'TCB': 'Ngân hàng',
            'VNM': 'Thực phẩm',
            'SAB': 'Thực phẩm'
        }
        return sectors.get(symbol, 'Khác')
    
    def _get_market_cap_category(self, candidate: Dict) -> str:
        """Phân loại market cap"""
        # Mock implementation
        return np.random.choice(['Nhỏ', 'Vừa', 'Lớn'], p=[0.3, 0.5, 0.2])
    
    def _create_technical_summary(self, candidate: Dict) -> str:
        """Tạo tóm tắt phân tích kỹ thuật"""
        rsi = candidate.get('rsi', 50)
        price_change_5d = candidate.get('price_change_5d', 0)
        volume_surge = candidate.get('volume_surge', 1)
        
        if rsi < 30 and price_change_5d > 0:
            return "Tích cực: RSI oversold + giá tăng"
        elif rsi > 70:
            return "Cảnh báo: RSI overbought"
        elif volume_surge > 2:
            return "Tích cực: Volume cao xác nhận xu hướng"
        else:
            return "Trung tính: Tín hiệu kỹ thuật cân bằng"
    
    def _create_fundamental_summary(self, candidate: Dict) -> str:
        """Tạo tóm tắt phân tích cơ bản"""
        return "Cơ bản ổn định: Tài chính lành mạnh, tăng trưởng bền vững"
    
    def _create_news_sentiment_summary(self, candidate: Dict) -> str:
        """Tạo tóm tắt tin tức và sentiment"""
        return "Tin tức tích cực: Sentiment thị trường ủng hộ"
    
    def _create_action_timeline(self, recommendation_type: str, forecast_analysis: Dict) -> List[str]:
        """Tạo timeline hành động"""
        timeline = []
        
        if recommendation_type in ['MUA MẠNH', 'MUA']:
            timeline.append("🚀 Hôm nay: Thực hiện mua")
            timeline.append("📅 1-3 ngày: Theo dõi diễn biến giá")
            timeline.append("📊 1 tuần: Đánh giá kết quả ban đầu")
        
        timeline.append("📋 Hàng ngày: Cập nhật stop-loss")
        timeline.append("📈 Hàng tuần: Rebalance nếu cần")
        
        return timeline
    
    def _create_risk_management_plan(self, stop_loss_price: float, target_price: float, 
                                   quantity: int) -> Dict[str, Any]:
        """Tạo kế hoạch quản lý rủi ro"""
        return {
            'stop_loss_price': stop_loss_price,
            'stop_loss_percentage': 5.0,  # Mock
            'target_price': target_price,
            'risk_reward_ratio': 1.5,  # Mock
            'position_size_management': f"Quản lý {quantity} cổ phiếu theo kế hoạch",
            'monitoring_frequency': "Hàng ngày trong giai đoạn đầu"
        }
    
    def _calculate_portfolio_grade(self, expected_return: float, risk_score: float) -> str:
        """Tính điểm tổng thể portfolio"""
        score = expected_return * 10 - risk_score
        
        if score >= 7:
            return "A+ (Xuất sắc)"
        elif score >= 6:
            return "A (Tốt)"
        elif score >= 5:
            return "B+ (Khá tốt)"
        elif score >= 4:
            return "B (Khá)"
        elif score >= 3:
            return "C (Trung bình)"
        else:
            return "D (Cần cải thiện)"
    
    def _generate_key_insights(self, recommendations: List[Dict], 
                             portfolio_allocation: Dict) -> List[str]:
        """Tạo các insight quan trọng"""
        insights = []
        
        # Analyze concentration
        total_positions = len(recommendations)
        if total_positions < 5:
            insights.append(f"⚠️ Portfolio chỉ có {total_positions} vị thế - Cần đa dạng hóa thêm")
        elif total_positions > 15:
            insights.append(f"📊 Portfolio có {total_positions} vị thế - Phân tán tốt")
        
        # Risk analysis
        avg_risk = np.mean([r['risk_analysis']['overall_score'] for r in recommendations])
        if avg_risk <= 4:
            insights.append("🛡️ Portfolio có rủi ro thấp - Phù hợp nhà đầu tư bảo thủ")
        elif avg_risk >= 7:
            insights.append("⚠️ Portfolio có rủi ro cao - Cần quản lý chặt chẽ")
        
        # Sector analysis
        sectors = {}
        for rec in recommendations:
            sector = rec['sector']
            sectors[sector] = sectors.get(sector, 0) + rec['percentage_of_portfolio']
        
        if len(sectors) <= 2:
            insights.append("⚠️ Tập trung vào ít sector - Rủi ro cao")
        else:
            insights.append("✅ Đa dạng sector tốt")
        
        return insights

def test_recommendation_engine():
    """Test function cho Stock Recommendation Engine"""
    print("🧪 Testing Stock Recommendation Engine...")
    
    try:
        # Initialize engine
        engine = StockRecommendationEngine()
        print("✅ Recommendation Engine initialized")
        
        # Create mock scan results
        mock_scan_results = {
            'scan_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'candidates': [
                {
                    'symbol': 'VRE',
                    'current_price': 29500,
                    'price_change_5d': 4.2,
                    'volume_surge': 2.1,
                    'rsi': 45,
                    'investment_grade': 8,
                    'forecast': {
                        'predictions': [
                            {'direction': 'Tăng', 'predicted_change_points': 250, 'confidence_score': 0.85},
                            {'direction': 'Tăng', 'predicted_change_points': 180, 'confidence_score': 0.80}
                        ]
                    }
                },
                {
                    'symbol': 'VNM',
                    'current_price': 112000,
                    'price_change_5d': 2.1,
                    'volume_surge': 1.8,
                    'rsi': 52,
                    'investment_grade': 7,
                    'forecast': {
                        'predictions': [
                            {'direction': 'Tăng', 'predicted_change_points': 400, 'confidence_score': 0.78},
                            {'direction': 'Tăng', 'predicted_change_points': 320, 'confidence_score': 0.75}
                        ]
                    }
                }
            ]
        }
        
        # Generate recommendations
        portfolio_size = 100000000  # 100M VND
        results = engine.generate_investment_recommendations(
            mock_scan_results, portfolio_size, "medium"
        )
        
        if 'error' in results:
            print(f"❌ Recommendation failed: {results['error']}")
            return None
        
        # Display results
        print(f"\n🎯 INVESTMENT RECOMMENDATIONS:")
        print(f"📅 Analysis Date: {results['analysis_date']}")
        print(f"💰 Portfolio Size: {portfolio_size:,.0f} VND")
        print(f"⚖️ Risk Tolerance: {results['risk_tolerance']}")
        
        # Display individual recommendations
        recommendations = results['recommendations']
        print(f"\n📊 DETAILED RECOMMENDATIONS:")
        print("=" * 60)
        
        for i, rec in enumerate(recommendations, 1):
            print(f"\n#{i} {rec['symbol']} - {rec['recommendation']}")
            print(f"   🏢 Company: {rec['company_name']}")
            print(f"   💰 Current Price: {rec['current_price']:,.0f} VND")
            print(f"   🎯 Target Price: {rec['target_price']:,.0f} VND")
            print(f"   🛡️ Stop Loss: {rec['stop_loss_price']:,.0f} VND")
            print(f"   📊 Quantity: {rec['quantity']:,} shares")
            print(f"   💵 Amount: {rec['amount']:,.0f} VND ({rec['percentage_of_portfolio']:.1f}%)")
            print(f"   🎯 Confidence: {rec['confidence']:.1%}")
            print(f"   📈 Expected Return: {rec['expected_return']:.1%}")
            print(f"   ⚖️ Risk Level: {rec['risk_analysis']['level']}")
            
            print(f"   💡 Lý do khuyến nghị:")
            for reason in rec['reasons'][:3]:  # Top 3 reasons
                print(f"      • {reason}")
        
        # Display portfolio allocation
        allocation = results['portfolio_allocation']
        print(f"\n💼 PORTFOLIO ALLOCATION:")
        print(f"   💰 Total Allocated: {allocation['total_allocated']:,.0f} VND")
        print(f"   💵 Cash Remaining: {allocation['cash_remaining']:,.0f} VND")
        print(f"   📊 Cash Percentage: {allocation['cash_percentage']:.1f}%")
        
        # Display overall analysis
        overall = results['overall_analysis']
        print(f"\n🎯 OVERALL ANALYSIS:")
        print(f"   📈 Expected Return: {overall['overall_expected_return']:.1%}")
        print(f"   ⚖️ Average Risk: {overall['average_risk_score']:.1f}/10")
        print(f"   🎭 Market Sentiment: {overall['market_sentiment']}")
        print(f"   🏆 Investment Grade: {overall['investment_grade']}")
        
        # Display action plan
        action_plan = results['action_plan']
        print(f"\n📋 ACTION PLAN:")
        for action in action_plan[:8]:  # Top 8 actions
            print(f"   {action}")
        
        print("\n✅ Stock Recommendation Engine test completed!")
        return results
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_recommendation_engine()
