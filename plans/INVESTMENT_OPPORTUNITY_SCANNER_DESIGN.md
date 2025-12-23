# THIẾT KẾ HỆ THỐNG TÌM KIẾM CƠ HỘI ĐẦU TƯ

## TỔNG QUAN

Hệ thống Investment Opportunity Scanner và Stock Recommendation Engine sẽ mở rộng chức năng dự báo hiện tại để:
- Quét toàn bộ thị trường chứng khoán Việt Nam
- Phân tích và đề xuất các cổ phiếu cần mua
- Đưa ra lý do cụ thể và số lượng khuyến nghị
- Tối ưu hóa portfolio allocation

---

## KIẾN TRÚC HỆ THỐNG

### 1. Investment Opportunity Scanner
```python
class InvestmentOpportunityScanner:
    """
    Quét toàn bộ thị trường để tìm cơ hội đầu tư
    """
    
    def __init__(self):
        self.vietnamese_stocks = self._load_vietnamese_stocks()
        self.technical_screener = TechnicalScreener()
        self.fundamental_screener = FundamentalScreener()
        self.news_screener = NewsScreener()
    
    def scan_market_opportunities(self, criteria):
        """
        Scan thị trường theo criteria
        """
        # 1. Technical Screening
        technical_candidates = self.technical_screener.screen(criteria)
        
        # 2. Fundamental Screening  
        fundamental_candidates = self.fundamental_screener.screen(criteria)
        
        # 3. News Sentiment Screening
        sentiment_candidates = self.news_screener.screen(criteria)
        
        # 4. Intersection Analysis
        candidates = self._intersect_analysis(
            technical_candidates, 
            fundamental_candidates, 
            sentiment_candidates
        )
        
        return candidates
```

### 2. Stock Recommendation Engine
```python
class StockRecommendationEngine:
    """
    Phân tích và đưa ra khuyến nghị cổ phiếu
    """
    
    def __init__(self):
        self.forecast_system = EnhancedStockForecastSystem()
        self.risk_analyzer = RiskAnalyzer()
        self.portfolio_optimizer = PortfolioOptimizer()
    
    def generate_recommendations(self, candidates):
        """
        Tạo khuyến nghị cho từng cổ phiếu
        """
        recommendations = []
        
        for stock in candidates:
            # 1. Deep Technical Analysis
            technical_score = self._analyze_technical(stock)
            
            # 2. Fundamental Analysis
            fundamental_score = self._analyze_fundamental(stock)
            
            # 3. AI Forecast Integration
            forecast = self.forecast_system.predict_next_2_days(stock.symbol)
            
            # 4. Risk Assessment
            risk_score = self.risk_analyzer.assess_risk(stock)
            
            # 5. Generate Recommendation
            recommendation = self._create_recommendation(
                stock, technical_score, fundamental_score, 
                forecast, risk_score
            )
            
            recommendations.append(recommendation)
        
        return self._rank_recommendations(recommendations)
    
    def _create_recommendation(self, stock, tech_score, fund_score, forecast, risk):
        """
        Tạo recommendation object
        """
        return {
            'symbol': stock.symbol,
            'company_name': stock.name,
            'recommendation': 'BUY',  # BUY/SELL/HOLD
            'reason': self._generate_reason(tech_score, fund_score, forecast),
            'quantity': self._calculate_quantity(stock, risk),
            'entry_price': stock.current_price,
            'target_price': self._calculate_target_price(forecast),
            'stop_loss': self._calculate_stop_loss(stock, risk),
            'confidence': self._calculate_confidence(tech_score, fund_score, risk),
            'expected_return': self._calculate_expected_return(stock, forecast),
            'risk_level': risk.level,
            'sector': stock.sector,
            'market_cap': stock.market_cap,
            'technical_score': tech_score,
            'fundamental_score': fund_score
        }
```

### 3. Portfolio Allocation Calculator
```python
class PortfolioAllocationCalculator:
    """
    Tính toán allocation tối ưu cho portfolio
    """
    
    def calculate_allocation(self, recommendations, total_capital):
        """
        Tính allocation cho portfolio
        """
        allocation = {}
        
        # 1. Risk-based allocation
        for rec in recommendations:
            if rec.recommendation == 'BUY':
                # Position sizing based on Kelly Criterion
                position_size = self._kelly_criterion_allocation(rec, total_capital)
                
                # Maximum 10% per stock
                max_allocation = total_capital * 0.10
                position_size = min(position_size, max_allocation)
                
                allocation[rec.symbol] = {
                    'amount': position_size,
                    'quantity': int(position_size / rec.entry_price),
                    'percentage': (position_size / total_capital) * 100,
                    'rec': rec
                }
        
        # 2. Diversification check
        allocation = self._apply_diversification_limits(allocation)
        
        # 3. Rebalancing suggestions
        rebalancing = self._calculate_rebalancing_need(allocation)
        
        return {
            'allocation': allocation,
            'total_allocated': sum(item['amount'] for item in allocation.values()),
            'cash_remaining': total_capital - sum(item['amount'] for item in allocation.values()),
            'rebalancing_suggestions': rebalancing,
            'risk_metrics': self._calculate_portfolio_risk(allocation)
        }
    
    def _kelly_criterion_allocation(self, recommendation, total_capital):
        """
        Kelly Criterion for position sizing
        """
        win_prob = recommendation.confidence
        win_ratio = recommendation.expected_return / abs(recommendation.stop_loss - recommendation.entry_price)
        loss_ratio = 1 - win_ratio
        
        kelly_fraction = (win_prob * win_ratio - (1 - win_prob)) / win_ratio
        
        # Conservative approach: use 25% of Kelly
        conservative_fraction = max(0, kelly_fraction * 0.25)
        
        return total_capital * conservative_fraction
```

---

## SCREENING CRITERIA

### 1. Technical Screening Criteria
```python
TECHNICAL_CRITERIA = {
    'volume': {
        'min_avg_volume': 1000000,  # 1M shares
        'volume_surge_multiplier': 2.0  # Recent volume vs avg
    },
    'price_movement': {
        'min_price_change_5d': 0.02,  # 2% increase in 5 days
        'max_price_decline_30d': 0.15,  # Max 15% decline in 30 days
        'breakout_price': True  # Price breaking resistance
    },
    'technical_indicators': {
        'rsi_range': (30, 70),  # Not overbought/oversold
        'macd_signal': 'bullish',  # MACD line above signal
        'moving_averages': 'bullish'  # Price above MA
    }
}
```

### 2. Fundamental Screening Criteria
```python
FUNDAMENTAL_CRITERIA = {
    'valuation': {
        'max_pe_ratio': 25,  # P/E ratio
        'max_pb_ratio': 3,   # P/B ratio
        'min_roe': 0.15      # ROE 15%
    },
    'financial_health': {
        'max_debt_to_equity': 0.5,
        'min_current_ratio': 1.5,
        'revenue_growth_3y': 0.10  # 10% annual growth
    },
    'market_metrics': {
        'min_market_cap': 1000000000,  # 1B VND
        'float_shares_ratio': 0.3     # At least 30% free float
    }
}
```

---

## THIẾT KẾ UI/UX

### 1. Investment Dashboard Layout
```html
<div class="investment-dashboard">
    <header class="dashboard-header">
        <h1>🎯 Cơ Hội Đầu Tư Hôm Nay</h1>
        <div class="market-status">
            <span class="status-indicator"></span>
            <span class="market-summary">VNIndex: +1.2%</span>
        </div>
    </header>
    
    <div class="dashboard-grid">
        <section class="top-opportunities">
            <h2>🏆 Top Cổ Phiếu Khuyến Nghị</h2>
            <div class="recommendation-cards"></div>
        </section>
        
        <section class="portfolio-allocation">
            <h2>📊 Phân Bổ Portfolio</h2>
            <div class="allocation-chart"></div>
        </section>
        
        <section class="risk-monitor">
            <h2>⚠️ Giám Sát Rủi Ro</h2>
            <div class="risk-metrics"></div>
        </section>
    </div>
</div>
```

### 2. Recommendation Card Design
```html
<div class="recommendation-card">
    <div class="card-header">
        <div class="stock-info">
            <h3 class="symbol">VRE</h3>
            <p class="company-name">Vinhomes</p>
        </div>
        <div class="recommendation-badge BUY">MUA</div>
    </div>
    
    <div class="card-body">
        <div class="price-info">
            <div class="current-price">29,500 VND</div>
            <div class="target-price">Target: 31,800 VND</div>
        </div>
        
        <div class="reason-section">
            <h4>Lý do khuyến nghị:</h4>
            <ul>
                <li>✅ RSI oversold, sắp rebound</li>
                <li>✅ Volume tăng 300%</li>
                <li>✅ Tin tức tích cực về dự án</li>
                <li>✅ Forecast 2 ngày: Tăng 7.8%</li>
            </ul>
        </div>
        
        <div class="quantity-section">
            <div class="recommended-quantity">
                <span class="label">Số lượng khuyến nghị:</span>
                <span class="value">500 cổ phiếu</span>
            </div>
            <div class="amount-needed">
                <span class="label">Số tiền cần:</span>
                <span class="value">14,750,000 VND</span>
            </div>
        </div>
        
        <div class="risk-metrics">
            <div class="confidence">
                <span class="label">Độ tin cậy:</span>
                <span class="value high">85%</span>
            </div>
            <div class="risk-level">
                <span class="label">Rủi ro:</span>
                <span class="value medium">Trung bình</span>
            </div>
        </div>
    </div>
</div>
```

---

## TRIỂN KHAI PHASES

### Phase 1: Core Infrastructure (Priority: High)
1. **InvestmentOpportunityScanner** class
2. **StockRecommendationEngine** class  
3. Basic screening criteria implementation
4. Integration với existing forecast system

### Phase 2: Advanced Analysis (Priority: High)
1. **PortfolioAllocationCalculator** class
2. Multi-factor analysis integration
3. Risk assessment algorithms
4. Kelly Criterion implementation

### Phase 3: UI/UX Enhancement (Priority: Medium)
1. Vietnamese dashboard interface
2. Real-time recommendation updates
3. Portfolio tracking features
4. Risk monitoring tools

### Phase 4: Optimization (Priority: Low)
1. Performance optimization
2. Machine learning enhancement
3. News sentiment integration
4. Advanced backtesting

---

## API DESIGN

### Main Investment Scanner API
```python
def scan_investment_opportunities(
    criteria: Dict[str, Any],
    portfolio_size: float,
    risk_tolerance: str = "medium"
) -> Dict[str, Any]:
    """
    Main API endpoint cho investment scanning
    
    Args:
        criteria: Screening criteria
        portfolio_size: Total investment capital
        risk_tolerance: "conservative", "medium", "aggressive"
    
    Returns:
        Dict với recommendations và allocation
    """
    pass

def get_stock_recommendation(
    symbol: str,
    portfolio_context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Get detailed recommendation cho một cổ phiếu
    """
    pass

def calculate_portfolio_allocation(
    recommendations: List[Dict],
    total_capital: float,
    diversification_rules: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Calculate optimal portfolio allocation
    """
    pass
```

---

## KẾT LUẬN

Hệ thống Investment Opportunity Scanner sẽ cung cấp:
- **Quét thị trường tự động** để tìm cơ hội
- **Khuyến nghị cụ thể** với lý do rõ ràng
- **Số lượng tối ưu** dựa trên risk management
- **Portfolio allocation** tối ưu cho diversification
- **Vietnamese interface** thân thiện với người dùng

Hệ thống sẽ tích hợp hoàn hảo với forecast system hiện tại để tạo thành một platform đầu tư toàn diện.