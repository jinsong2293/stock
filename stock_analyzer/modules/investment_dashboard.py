"""
Investment Dashboard - Hiển thị khuyến nghị đầu tư trực quan
Giao diện tiếng Việt để hiển thị cơ hội đầu tư và khuyến nghị cụ thể

Author: Roo - Investment Mode
Version: 1.0.0
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
import json
import warnings
warnings.filterwarnings('ignore')

# Import investment modules
try:
    from stock_analyzer.modules.investment_opportunity_scanner import InvestmentOpportunityScanner
    from stock_analyzer.modules.stock_recommendation_engine import StockRecommendationEngine
    INVESTMENT_MODULES_AVAILABLE = True
except ImportError:
    INVESTMENT_MODULES_AVAILABLE = False

logger = logging.getLogger(__name__)

class InvestmentDashboard:
    """Dashboard chính để hiển thị khuyến nghị đầu tư"""
    
    def __init__(self):
        if INVESTMENT_MODULES_AVAILABLE:
            self.scanner = InvestmentOpportunityScanner()
            self.recommendation_engine = StockRecommendationEngine()
        else:
            self.scanner = None
            self.recommendation_engine = None
        
        logger.info("Investment Dashboard initialized")
    
    def generate_investment_dashboard(self, 
                                    portfolio_size: float,
                                    risk_tolerance: str = "medium",
                                    investment_focus: str = "balanced") -> Dict[str, Any]:
        """
        Tạo dashboard đầu tư toàn diện
        """
        logger.info(f"Generating investment dashboard for portfolio: {portfolio_size:,.0f} VND")
        
        if not INVESTMENT_MODULES_AVAILABLE:
            return {"error": "Investment modules not available"}
        
        try:
            # 1. Scan market opportunities
            scan_results = self.scanner.scan_market_opportunities()
            
            if 'error' in scan_results:
                return {"error": f"Market scan failed: {scan_results['error']}"}
            
            # 2. Generate investment recommendations
            recommendations = self.recommendation_engine.generate_investment_recommendations(
                scan_results, portfolio_size, risk_tolerance
            )
            
            if 'error' in recommendations:
                return {"error": f"Recommendation generation failed: {recommendations['error']}"}
            
            # 3. Create visual dashboard data
            dashboard_data = self._create_dashboard_data(recommendations, scan_results)
            
            # 4. Generate Vietnamese UI data
            ui_data = self._create_vietnamese_ui_data(recommendations, dashboard_data)
            
            return {
                "dashboard_metadata": {
                    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "portfolio_size": portfolio_size,
                    "risk_tolerance": risk_tolerance,
                    "investment_focus": investment_focus,
                    "total_candidates": scan_results['total_stocks_scanned'],
                    "qualified_opportunities": len(recommendations.get('recommendations', []))
                },
                "market_summary": self._create_market_summary(scan_results),
                "top_opportunities": self._format_top_opportunities(recommendations),
                "portfolio_recommendations": self._format_portfolio_recommendations(recommendations),
                "risk_analysis": self._create_risk_analysis(recommendations),
                "action_plan": self._create_executable_action_plan(recommendations),
                "ui_components": ui_data
            }
            
        except Exception as e:
            logger.error(f"Error generating investment dashboard: {e}")
            return {"error": f"Dashboard generation failed: {e}"}
    
    def _create_dashboard_data(self, recommendations: Dict, scan_results: Dict) -> Dict[str, Any]:
        """Tạo dữ liệu cho dashboard"""
        
        # Portfolio metrics
        allocation = recommendations.get('portfolio_allocation', {})
        overall_analysis = recommendations.get('overall_analysis', {})
        
        dashboard_data = {
            "portfolio_metrics": {
                "total_recommended": allocation.get('total_allocated', 0),
                "cash_remaining": allocation.get('cash_remaining', 0),
                "expected_return": overall_analysis.get('overall_expected_return', 0),
                "average_risk": overall_analysis.get('average_risk_score', 0),
                "investment_grade": overall_analysis.get('investment_grade', 'N/A'),
                "diversification_score": overall_analysis.get('portfolio_diversification', 0)
            },
            
            "market_sentiment": overall_analysis.get('market_sentiment', 'Trung tính'),
            "recommendation_distribution": overall_analysis.get('recommendation_distribution', {}),
            
            "top_stocks": recommendations.get('recommendations', [])[:5],
            
            "sector_allocation": self._calculate_sector_allocation(recommendations.get('recommendations', [])),
            
            "risk_metrics": {
                "risk_level_distribution": self._analyze_risk_distribution(recommendations.get('recommendations', [])),
                "concentration_risk": self._analyze_concentration_risk(allocation.get('allocation', {})),
                "correlation_analysis": "Thấp"  # Simplified for now
            }
        }
        
        return dashboard_data
    
    def _create_vietnamese_ui_data(self, recommendations: Dict, dashboard_data: Dict) -> Dict[str, Any]:
        """Tạo dữ liệu UI tiếng Việt"""
        
        recommendations_list = recommendations.get('recommendations', [])
        
        # Main dashboard cards
        ui_cards = []
        
        for rec in recommendations_list:
            # Risk level Vietnamese translation
            risk_vietnamese = {
                'Thấp': 'low',
                'Trung bình': 'medium', 
                'Cao': 'high',
                'Rất cao': 'very_high'
            }
            
            risk_level = rec.get('risk_analysis', {}).get('level', 'Trung bình')
            risk_level_en = risk_vietnamese.get(risk_level, 'medium')
            
            # Recommendation type Vietnamese
            rec_type_vietnamese = {
                'MUA MẠNH': 'strong_buy',
                'MUA': 'buy',
                'NẮM GIỮ': 'hold',
                'BÁN': 'sell'
            }
            
            rec_type_en = rec_type_vietnamese.get(rec.get('recommendation', 'NẮM GIỮ'), 'hold')
            
            card = {
                "id": rec.get('symbol', 'unknown'),
                "title": f"{rec.get('symbol', '')} - {rec.get('company_name', '')}",
                "recommendation": rec_type_en,
                "recommendation_vietnamese": rec.get('recommendation', 'NẮM GIỮ'),
                "current_price": rec.get('current_price', 0),
                "target_price": rec.get('target_price', 0),
                "stop_loss": rec.get('stop_loss_price', 0),
                "quantity": rec.get('quantity', 0),
                "investment_amount": rec.get('amount', 0),
                "percentage": rec.get('percentage_of_portfolio', 0),
                "confidence": rec.get('confidence', 0),
                "expected_return": rec.get('expected_return', 0),
                "risk_level": risk_level_en,
                "risk_level_vietnamese": risk_level,
                "sector": rec.get('sector', 'Khác'),
                "reasons": rec.get('reasons', [])[:3],  # Top 3 reasons
                "technical_summary": rec.get('technical_summary', ''),
                "action_timeline": rec.get('action_timeline', [])
            }
            
            ui_cards.append(card)
        
        # Portfolio summary
        portfolio_summary = {
            "total_allocated": dashboard_data['portfolio_metrics']['total_recommended'],
            "cash_remaining": dashboard_data['portfolio_metrics']['cash_remaining'],
            "expected_return": dashboard_data['portfolio_metrics']['expected_return'],
            "investment_grade": dashboard_data['portfolio_metrics']['investment_grade'],
            "market_sentiment": dashboard_data['market_sentiment']
        }
        
        # Action plan in Vietnamese
        action_plan_vn = []
        for action in recommendations.get('action_plan', []):
            if isinstance(action, str):
                # Convert to actionable format
                if 'MUA MẠNH' in action:
                    action_plan_vn.append({
                        "type": "urgent_action",
                        "priority": "high",
                        "description": action,
                        "action_required": True
                    })
                elif 'MUA' in action:
                    action_plan_vn.append({
                        "type": "planned_action", 
                        "priority": "medium",
                        "description": action,
                        "action_required": True
                    })
                elif 'NẮM GIỮ' in action:
                    action_plan_vn.append({
                        "type": "monitoring",
                        "priority": "low",
                        "description": action,
                        "action_required": False
                    })
                else:
                    action_plan_vn.append({
                        "type": "info",
                        "priority": "low",
                        "description": action,
                        "action_required": False
                    })
        
        return {
            "investment_cards": ui_cards,
            "portfolio_summary": portfolio_summary,
            "action_plan": action_plan_vn,
            "key_metrics": {
                "total_opportunities": len(ui_cards),
                "strong_buy_count": len([c for c in ui_cards if c['recommendation'] == 'strong_buy']),
                "buy_count": len([c for c in ui_cards if c['recommendation'] == 'buy']),
                "average_confidence": np.mean([c['confidence'] for c in ui_cards]) if ui_cards else 0
            }
        }
    
    def _create_market_summary(self, scan_results: Dict) -> Dict[str, Any]:
        """Tạo tóm tắt thị trường"""
        screening = scan_results.get('screening_results', {})
        
        return {
            "scan_date": scan_results.get('scan_date', ''),
            "total_stocks_analyzed": scan_results.get('total_stocks_scanned', 0),
            "qualified_opportunities": screening.get('final_candidates', 0),
            "screening_breakdown": {
                "technical_filter": f"{screening.get('technical_candidates', 0)} cổ phiếu",
                "fundamental_filter": f"{screening.get('fundamental_candidates', 0)} cổ phiếu", 
                "sentiment_filter": f"{screening.get('news_candidates', 0)} cổ phiếu"
            },
            "market_quality_score": self._calculate_market_quality_score(screening),
            "trending_sectors": self._identify_trending_sectors(scan_results.get('candidates', []))
        }
    
    def _format_top_opportunities(self, recommendations: Dict) -> List[Dict]:
        """Định dạng top opportunities"""
        opportunities = []
        
        for rec in recommendations.get('recommendations', [])[:5]:
            opportunity = {
                "rank": len(opportunities) + 1,
                "symbol": rec.get('symbol', ''),
                "company_name": rec.get('company_name', ''),
                "current_price": rec.get('current_price', 0),
                "recommendation": rec.get('recommendation', ''),
                "confidence": rec.get('confidence', 0),
                "expected_return": rec.get('expected_return', 0),
                "risk_level": rec.get('risk_analysis', {}).get('level', ''),
                "quantity": rec.get('quantity', 0),
                "investment_amount": rec.get('amount', 0),
                "key_reasons": rec.get('reasons', [])[:2]
            }
            opportunities.append(opportunity)
        
        return opportunities
    
    def _format_portfolio_recommendations(self, recommendations: Dict) -> Dict[str, Any]:
        """Định dạng portfolio recommendations"""
        allocation = recommendations.get('portfolio_allocation', {})
        
        return {
            "total_allocation": allocation.get('total_allocated', 0),
            "cash_position": allocation.get('cash_remaining', 0),
            "cash_percentage": allocation.get('cash_percentage', 0),
            "position_count": len(allocation.get('allocation', {})),
            "allocation_breakdown": [
                {
                    "symbol": symbol,
                    "amount": alloc.get('amount', 0),
                    "percentage": alloc.get('percentage', 0),
                    "quantity": alloc.get('quantity', 0)
                }
                for symbol, alloc in allocation.get('allocation', {}).items()
            ],
            "diversification_score": self._calculate_diversification_score(allocation.get('allocation', {})),
            "sector_distribution": self._calculate_sector_distribution(recommendations.get('recommendations', []))
        }
    
    def _create_risk_analysis(self, recommendations: Dict) -> Dict[str, Any]:
        """Tạo phân tích rủi ro"""
        recs = recommendations.get('recommendations', [])
        
        if not recs:
            return {"error": "No recommendations for risk analysis"}
        
        # Risk distribution
        risk_distribution = {}
        for rec in recs:
            risk_level = rec.get('risk_analysis', {}).get('level', 'Trung bình')
            risk_distribution[risk_level] = risk_distribution.get(risk_level, 0) + 1
        
        # Risk metrics
        risk_scores = [rec.get('risk_analysis', {}).get('overall_score', 5) for rec in recs]
        
        return {
            "overall_risk_score": np.mean(risk_scores),
            "risk_distribution": risk_distribution,
            "highest_risk_stock": max(recs, key=lambda x: x.get('risk_analysis', {}).get('overall_score', 0)),
            "lowest_risk_stock": min(recs, key=lambda x: x.get('risk_analysis', {}).get('overall_score', 10)),
            "concentration_risk": self._assess_concentration_risk(recs),
            "recommendations": self._generate_risk_management_tips(recs)
        }
    
    def _create_executable_action_plan(self, recommendations: Dict) -> Dict[str, Any]:
        """Tạo kế hoạch hành động thực thi"""
        
        # Prioritize actions
        urgent_actions = []
        planned_actions = []
        monitoring_tasks = []
        
        for rec in recommendations.get('recommendations', []):
            rec_type = rec.get('recommendation', '')
            
            if rec_type == 'MUA MẠNH':
                urgent_actions.append({
                    "action": f"Mua {rec.get('quantity', 0)} cổ phiếu {rec.get('symbol', '')}",
                    "amount": rec.get('amount', 0),
                    "deadline": "Ngay lập tức",
                    "priority": "Cao",
                    "reason": "Cơ hội đầu tư tốt nhất"
                })
            elif rec_type == 'MUA':
                planned_actions.append({
                    "action": f"Cân nhắc mua {rec.get('quantity', 0)} cổ phiếu {rec.get('symbol', '')}",
                    "amount": rec.get('amount', 0),
                    "deadline": "Trong tuần này",
                    "priority": "Trung bình",
                    "reason": "Cơ hội tốt"
                })
            else:
                monitoring_tasks.append({
                    "action": f"Theo dõi {rec.get('symbol', '')}",
                    "deadline": "Hàng ngày",
                    "priority": "Thấp",
                    "reason": "Nắm giữ hiện tại"
                })
        
        return {
            "urgent_actions": urgent_actions,
            "planned_actions": planned_actions,
            "monitoring_tasks": monitoring_tasks,
            "total_urgent_amount": sum(action['amount'] for action in urgent_actions),
            "total_planned_amount": sum(action['amount'] for action in planned_actions),
            "implementation_timeline": self._create_implementation_timeline(urgent_actions, planned_actions)
        }
    
    def _calculate_sector_allocation(self, recommendations: List[Dict]) -> Dict[str, float]:
        """Tính toán phân bổ theo sector"""
        sector_allocation = {}
        total_amount = 0
        
        for rec in recommendations:
            sector = rec.get('sector', 'Khác')
            amount = rec.get('amount', 0)
            total_amount += amount
            sector_allocation[sector] = sector_allocation.get(sector, 0) + amount
        
        # Convert to percentages
        if total_amount > 0:
            sector_allocation = {k: (v / total_amount) * 100 for k, v in sector_allocation.items()}
        
        return sector_allocation
    
    def _analyze_risk_distribution(self, recommendations: List[Dict]) -> Dict[str, int]:
        """Phân tích phân phối rủi ro"""
        distribution = {}
        for rec in recommendations:
            risk_level = rec.get('risk_analysis', {}).get('level', 'Trung bình')
            distribution[risk_level] = distribution.get(risk_level, 0) + 1
        return distribution
    
    def _analyze_concentration_risk(self, allocation: Dict) -> Dict[str, Any]:
        """Phân tích rủi ro tập trung"""
        if not allocation:
            return {"status": "Không có vị thế", "concentration_level": "Thấp"}
        
        amounts = [alloc.get('amount', 0) for alloc in allocation.values()]
        total_amount = sum(amounts)
        
        if total_amount == 0:
            return {"status": "Không có phân bổ", "concentration_level": "Thấp"}
        
        # Calculate concentration metrics
        max_position_pct = max(amounts) / total_amount * 100
        hhi_index = sum((amount / total_amount) ** 2 for amount in amounts) * 10000
        
        if max_position_pct > 20:
            concentration_level = "Cao"
        elif max_position_pct > 10:
            concentration_level = "Trung bình"
        else:
            concentration_level = "Thấp"
        
        return {
            "max_position_percentage": max_position_pct,
            "concentration_level": concentration_level,
            "hhi_index": hhi_index,
            "status": "Cần cân bằng lại" if concentration_level == "Cao" else "Tốt"
        }
    
    def _calculate_market_quality_score(self, screening: Dict) -> str:
        """Tính điểm chất lượng thị trường"""
        total_stocks = 100  # Assume 100 stocks in market
        qualified = screening.get('final_candidates', 0)
        quality_ratio = qualified / total_stocks
        
        if quality_ratio >= 0.15:
            return "Tuyệt vời (15%+ cổ phiếu chất lượng)"
        elif quality_ratio >= 0.10:
            return "Tốt (10-15% cổ phiếu chất lượng)"
        elif quality_ratio >= 0.05:
            return "Trung bình (5-10% cổ phiếu chất lượng)"
        else:
            return "Thấp (<5% cổ phiếu chất lượng)"
    
    def _identify_trending_sectors(self, candidates: List[Dict]) -> List[str]:
        """Xác định các sector đang xu hướng"""
        sector_counts = {}
        for candidate in candidates:
            # Mock sector assignment based on symbol
            symbol = candidate.get('symbol', '')
            if symbol in ['VRE', 'VIC', 'VHM']:
                sector = 'Bất động sản'
            elif symbol in ['VCB', 'BID', 'CTG', 'ACB', 'TCB']:
                sector = 'Ngân hàng'
            elif symbol in ['VNM', 'SAB']:
                sector = 'Thực phẩm'
            else:
                sector = 'Khác'
            
            sector_counts[sector] = sector_counts.get(sector, 0) + 1
        
        # Return top 3 sectors
        trending = sorted(sector_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        return [f"{sector} ({count} cổ phiếu)" for sector, count in trending]
    
    def _calculate_diversification_score(self, allocation: Dict) -> float:
        """Tính điểm đa dạng hóa"""
        if not allocation:
            return 0.0
        
        # Simple diversification score based on number of positions
        position_count = len(allocation)
        
        if position_count >= 10:
            return 0.9
        elif position_count >= 5:
            return 0.7
        elif position_count >= 3:
            return 0.5
        else:
            return 0.3
    
    def _calculate_sector_distribution(self, recommendations: List[Dict]) -> Dict[str, int]:
        """Tính phân phối theo sector"""
        sector_dist = {}
        for rec in recommendations:
            sector = rec.get('sector', 'Khác')
            sector_dist[sector] = sector_dist.get(sector, 0) + 1
        return sector_dist
    
    def _assess_concentration_risk(self, recommendations: List[Dict]) -> str:
        """Đánh giá rủi ro tập trung"""
        if len(recommendations) <= 3:
            return "Cao - Quá ít vị thế"
        elif len(recommendations) >= 10:
            return "Thấp - Đa dạng tốt"
        else:
            return "Trung bình - Cần thêm vị thế"
    
    def _generate_risk_management_tips(self, recommendations: List[Dict]) -> List[str]:
        """Tạo tips quản lý rủi ro"""
        tips = []
        
        # Check position size
        total_amount = sum(rec.get('amount', 0) for rec in recommendations)
        if total_amount > 0:
            max_position = max(rec.get('amount', 0) for rec in recommendations)
            if max_position / total_amount > 0.2:
                tips.append("⚠️ Có vị thế quá lớn - Cân nhắc giảm")
        
        # Check risk levels
        high_risk_count = len([r for r in recommendations if r.get('risk_analysis', {}).get('level', '') == 'Cao'])
        if high_risk_count > len(recommendations) * 0.3:
            tips.append("⚠️ Quá nhiều cổ phiếu rủi ro cao")
        
        # General tips
        tips.extend([
            "✅ Đặt stop-loss cho tất cả vị thế",
            "✅ Theo dõi portfolio hàng ngày",
            "✅ Rebalance định kỳ hàng tuần"
        ])
        
        return tips
    
    def _create_implementation_timeline(self, urgent_actions: List, planned_actions: List) -> List[Dict]:
        """Tạo timeline triển khai"""
        timeline = []
        
        # Today
        if urgent_actions:
            timeline.append({
                "date": "Hôm nay",
                "actions": [f"Thực hiện: {action['action']}" for action in urgent_actions],
                "priority": "Cao"
            })
        
        # This week
        if planned_actions:
            timeline.append({
                "date": "Tuần này",
                "actions": [f"Lên kế hoạch: {action['action']}" for action in planned_actions],
                "priority": "Trung bình"
            })
        
        # Ongoing
        timeline.append({
            "date": "Liên tục",
            "actions": [
                "Theo dõi portfolio hàng ngày",
                "Cập nhật stop-loss",
                "Đánh giá hiệu suất"
            ],
            "priority": "Thấp"
        })
        
        return timeline
    
    def export_dashboard_data(self, dashboard_data: Dict, filename: str = None) -> str:
        """Export dữ liệu dashboard ra file JSON"""
        if not filename:
            filename = f"investment_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(dashboard_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Dashboard data exported to {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error exporting dashboard data: {e}")
            return ""

def test_investment_dashboard():
    """Test function cho Investment Dashboard"""
    print("🧪 Testing Investment Dashboard...")
    
    try:
        # Initialize dashboard
        dashboard = InvestmentDashboard()
        print("✅ Investment Dashboard initialized")
        
        # Generate dashboard
        portfolio_size = 50000000  # 50M VND
        results = dashboard.generate_investment_dashboard(
            portfolio_size, "medium", "balanced"
        )
        
        if 'error' in results:
            print(f"❌ Dashboard generation failed: {results['error']}")
            return None
        
        # Display results
        print(f"\n🎯 INVESTMENT DASHBOARD:")
        print(f"📅 Generated: {results['dashboard_metadata']['generated_at']}")
        print(f"💰 Portfolio Size: {portfolio_size:,.0f} VND")
        print(f"⚖️ Risk Tolerance: {results['dashboard_metadata']['risk_tolerance']}")
        
        # Market summary
        market = results['market_summary']
        print(f"\n📊 MARKET SUMMARY:")
        print(f"   📈 Total Stocks Analyzed: {market['total_stocks_analyzed']}")
        print(f"   🎯 Qualified Opportunities: {market['qualified_opportunities']}")
        print(f"   🏆 Market Quality: {market['market_quality_score']}")
        
        # Top opportunities
        opportunities = results['top_opportunities']
        if opportunities:
            print(f"\n🏆 TOP INVESTMENT OPPORTUNITIES:")
            print("=" * 60)
            
            for opp in opportunities:
                print(f"\n#{opp['rank']} {opp['symbol']} - {opp['recommendation']}")
                print(f"   💰 Price: {opp['current_price']:,.0f} VND")
                print(f"   📊 Quantity: {opp['quantity']:,} shares")
                print(f"   💵 Amount: {opp['investment_amount']:,.0f} VND")
                print(f"   🎯 Confidence: {opp['confidence']:.1%}")
                print(f"   💡 Reasons: {', '.join(opp['key_reasons'])}")
        
        # Portfolio recommendations
        portfolio = results['portfolio_recommendations']
        print(f"\n💼 PORTFOLIO RECOMMENDATIONS:")
        print(f"   💰 Total Allocated: {portfolio['total_allocation']:,.0f} VND")
        print(f"   💵 Cash Position: {portfolio['cash_position']:,.0f} VND")
        print(f"   📊 Cash Percentage: {portfolio['cash_percentage']:.1f}%")
        print(f"   📈 Diversification Score: {portfolio['diversification_score']:.1f}")
        
        # Risk analysis
        risk = results['risk_analysis']
        print(f"\n⚖️ RISK ANALYSIS:")
        print(f"   🎯 Overall Risk Score: {risk['overall_risk_score']:.1f}/10")
        print(f"   📊 Risk Distribution: {risk['risk_distribution']}")
        print(f"   ⚠️ Concentration Risk: {risk['concentration_risk']}")
        
        # Action plan
        action_plan = results['action_plan']
        print(f"\n📋 ACTION PLAN:")
        print(f"   🚀 Urgent Actions: {len(action_plan['urgent_actions'])}")
        print(f"   ⏰ Planned Actions: {len(action_plan['planned_actions'])}")
        print(f"   📊 Monitoring Tasks: {len(action_plan['monitoring_tasks'])}")
        
        if action_plan['urgent_actions']:
            print(f"   💰 Total Urgent Amount: {action_plan['total_urgent_amount']:,.0f} VND")
        
        print("\n✅ Investment Dashboard test completed!")
        
        # Export data
        export_file = dashboard.export_dashboard_data(results)
        if export_file:
            print(f"📁 Dashboard data exported to: {export_file}")
        
        return results
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_investment_dashboard()
