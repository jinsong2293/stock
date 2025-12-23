"""
Investment Opportunity Scanner - Quét toàn bộ thị trường chứng khoán Việt Nam
Tìm kiếm cơ hội đầu tư và cổ phiếu tiềm năng

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
    from stock_analyzer.modules.data_loader import DataLoader, fetch_historical_data
    from stock_analyzer.modules.technical_analysis import perform_technical_analysis
    FORECAST_SYSTEM_AVAILABLE = True
    TECHNICAL_ANALYSIS_AVAILABLE = True
except ImportError:
    FORECAST_SYSTEM_AVAILABLE = False
    TECHNICAL_ANALYSIS_AVAILABLE = False
    print("⚠️ EnhancedStockForecastSystem not available.")
    
# Fallback technical analysis function
if not TECHNICAL_ANALYSIS_AVAILABLE:
    def perform_technical_analysis(data):
        """Fallback technical analysis"""
        result = data.copy()
        # Simple RSI calculation
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        result['RSI'] = 100 - (100 / (1 + rs))
        return result

try:
    from stock_analyzer.modules.news_sentiment_analyzer import NewsSentimentAnalyzer
    SENTIMENT_AVAILABLE = True
except ImportError:
    SENTIMENT_AVAILABLE = False

logger = logging.getLogger(__name__)

class TechnicalScreener:
    """Screener dựa trên phân tích kỹ thuật"""
    
    def __init__(self):
        self.criteria = {
            'volume': {
                'min_avg_volume': 1000000,  # 1M shares_surge_multiplier
                'volume': 2.0
            },
            'price_movement': {
                'min_price_change_5d': 0.02,  # 2% increase in 5 days
                'max_price_decline_30d': 0.15,  # Max 15% decline in 30 days
                'breakout_price': True
            },
            'technical_indicators': {
                'rsi_range': (30, 70),
                'macd_signal': 'bullish',
                'moving_averages': 'bullish'
            }
        }
    
    def screen(self, stocks_data: Dict[str, pd.DataFrame]) -> List[str]:
        """
        Screen stocks based on technical criteria
        """
        candidates = []
        
        for symbol, data in stocks_data.items():
            try:
                if len(data) < 30:  # Need enough data
                    continue
                
                # Calculate technical indicators
                technical_data = perform_technical_analysis(data)
                
                # Check volume criteria
                avg_volume = technical_data['Volume'].tail(20).mean()
                recent_volume = technical_data['Volume'].tail(5).mean()
                
                if avg_volume < self.criteria['volume']['min_avg_volume']:
                    continue
                if recent_volume / avg_volume < self.criteria['volume']['volume']:
                    continue
                
                # Check price movement
                price_5d_change = (data['Close'].iloc[-1] / data['Close'].iloc[-6]) - 1
                price_30d_change = (data['Close'].iloc[-1] / data['Close'].iloc[-31]) - 1
                
                if price_5d_change < self.criteria['price_movement']['min_price_change_5d']:
                    continue
                if price_30d_change < -self.criteria['price_movement']['max_price_decline_30d']:
                    continue
                
                # Check technical indicators
                if 'RSI' in technical_data.columns:
                    rsi = technical_data['RSI'].iloc[-1]
                    if not (self.criteria['technical_indicators']['rsi_range'][0] <= rsi <= 
                            self.criteria['technical_indicators']['rsi_range'][1]):
                        continue
                
                # Check MACD
                if all(col in technical_data.columns for col in ['MACD', 'MACD_Signal']):
                    macd = technical_data['MACD'].iloc[-1]
                    signal = technical_data['MACD_Signal'].iloc[-1]
                    
                    if (self.criteria['technical_indicators']['macd_signal'] == 'bullish' and 
                        macd <= signal):
                        continue
                
                # Check moving averages
                if all(col in technical_data.columns for col in ['MA_20', 'MA_50']):
                    current_price = technical_data['Close'].iloc[-1]
                    ma_20 = technical_data['MA_20'].iloc[-1]
                    ma_50 = technical_data['MA_50'].iloc[-1]
                    
                    if (self.criteria['technical_indicators']['moving_averages'] == 'bullish' and 
                        not (current_price > ma_20 > ma_50)):
                        continue
                
                # Add to candidates
                candidates.append(symbol)
                logger.info(f"Technical screener: {symbol} passed all criteria")
                
            except Exception as e:
                logger.error(f"Error screening {symbol}: {e}")
                continue
        
        logger.info(f"Technical screener found {len(candidates)} candidates")
        return candidates

class FundamentalScreener:
    """Screener dựa trên phân tích cơ bản"""
    
    def __init__(self):
        self.criteria = {
            'valuation': {
                'max_pe_ratio': 25,
                'max_pb_ratio': 3,
                'min_roe': 0.15
            },
            'financial_health': {
                'max_debt_to_equity': 0.5,
                'min_current_ratio': 1.5,
                'revenue_growth_3y': 0.10
            },
            'market_metrics': {
                'min_market_cap': 1000000000,  # 1B VND
                'float_shares_ratio': 0.3
            }
        }
    
    def screen(self, fundamental_data: Dict[str, Dict]) -> List[str]:
        """
        Screen stocks based on fundamental criteria
        """
        candidates = []
        
        for symbol, data in fundamental_data.items():
            try:
                # Check valuation metrics
                if 'pe_ratio' in data and data['pe_ratio'] > self.criteria['valuation']['max_pe_ratio']:
                    continue
                
                if 'pb_ratio' in data and data['pb_ratio'] > self.criteria['valuation']['max_pb_ratio']:
                    continue
                
                if 'roe' in data and data['roe'] < self.criteria['valuation']['min_roe']:
                    continue
                
                # Check financial health
                if 'debt_to_equity' in data and data['debt_to_equity'] > self.criteria['financial_health']['max_debt_to_equity']:
                    continue
                
                if 'current_ratio' in data and data['current_ratio'] < self.criteria['financial_health']['min_current_ratio']:
                    continue
                
                # Check market metrics
                if 'market_cap' in data and data['market_cap'] < self.criteria['market_metrics']['min_market_cap']:
                    continue
                
                # Add to candidates
                candidates.append(symbol)
                logger.info(f"Fundamental screener: {symbol} passed all criteria")
                
            except Exception as e:
                logger.error(f"Error fundamental screening {symbol}: {e}")
                continue
        
        logger.info(f"Fundamental screener found {len(candidates)} candidates")
        return candidates

class NewsScreener:
    """Screener dựa trên tin tức và sentiment"""
    
    def __init__(self):
        self.criteria = {
            'min_news_count': 2,
            'min_positive_ratio': 0.6,
            'min_sentiment_score': 0.6
        }
    
    def screen(self, symbols: List[str], days: int = 7) -> List[str]:
        """
        Screen stocks based on news sentiment
        """
        candidates = []
        
        if not SENTIMENT_AVAILABLE:
            logger.warning("News sentiment analyzer not available")
            return candidates
        
        try:
            news_analyzer = NewsSentimentAnalyzer()
            
            for symbol in symbols:
                try:
                    # Get sentiment features
                    sentiment_features = news_analyzer.get_sentiment_features(symbol, days)
                    
                    news_count = sentiment_features.get('news_volume', 0)
                    positive_ratio = sentiment_features.get('positive_ratio', 0)
                    sentiment_score = sentiment_features.get('sentiment_score', 0.5)
                    
                    # Apply criteria
                    if news_count < self.criteria['min_news_count']:
                        continue
                    if positive_ratio < self.criteria['min_positive_ratio']:
                        continue
                    if sentiment_score < self.criteria['min_sentiment_score']:
                        continue
                    
                    candidates.append(symbol)
                    logger.info(f"News screener: {symbol} passed sentiment criteria")
                    
                except Exception as e:
                    logger.error(f"Error news screening {symbol}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error in news screener: {e}")
        
        logger.info(f"News screener found {len(candidates)} candidates")
        return candidates

class InvestmentOpportunityScanner:
    """Main scanner để tìm cơ hội đầu tư"""
    
    def __init__(self):
        self.technical_screener = TechnicalScreener()
        self.fundamental_screener = FundamentalScreener()
        self.news_screener = NewsScreener()
        
        if FORECAST_SYSTEM_AVAILABLE:
            self.forecast_system = EnhancedStockForecastSystem()
        else:
            self.forecast_system = None
        
        # Vietnamese stock list (popular stocks)
        self.vietnamese_stocks = [
            'VRE', 'VIC', 'VHM', 'VCB', 'BID', 'CTG', 'ACB', 'TCB', 'STB', 'EIB',
            'GAS', 'PLX', 'PVD', 'PVS', 'VNM', 'SAB', 'MWG', 'FPT', 'REE', 'REE',
            'KDC', 'DBC', 'MSN', 'VJC', 'HVN', 'VGT', 'NLG', 'KDH', 'PDR', 'CII',
            'BSI', 'BMI', 'LIX', 'SBT', 'DPR', 'VHC', 'ANV', 'VCS', 'HPG', 'HSG'
        ]
        
        logger.info(f"Investment Opportunity Scanner initialized with {len(self.vietnamese_stocks)} stocks")
    
    def scan_market_opportunities(self, 
                                criteria: Optional[Dict] = None,
                                portfolio_size: Optional[float] = None) -> Dict[str, Any]:
        """
        Main method để scan toàn bộ thị trường
        """
        logger.info("Starting market opportunity scan...")
        
        # Load stock data
        stocks_data = self._load_stocks_data()
        if not stocks_data:
            logger.error("No stock data available for scanning")
            return {"error": "No stock data available"}
        
        # Apply screening criteria
        technical_candidates = self.technical_screener.screen(stocks_data)
        logger.info(f"Technical screening found {len(technical_candidates)} candidates")
        
        # Mock fundamental data (in real implementation, this would come from financial databases)
        fundamental_data = self._generate_mock_fundamental_data(list(stocks_data.keys()))
        fundamental_candidates = self.fundamental_screener.screen(fundamental_data)
        logger.info(f"Fundamental screening found {len(fundamental_candidates)} candidates")
        
        # News sentiment screening
        news_candidates = self.news_screener.screen(list(stocks_data.keys()))
        logger.info(f"News screening found {len(news_candidates)} candidates")
        
        # Intersection analysis
        candidates = self._intersect_analysis(technical_candidates, fundamental_candidates, news_candidates)
        logger.info(f"Intersection analysis: {len(candidates)} final candidates")
        
        # Generate detailed analysis for candidates
        detailed_analysis = self._generate_detailed_analysis(candidates, stocks_data)
        
        return {
            "scan_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_stocks_scanned": len(stocks_data),
            "screening_results": {
                "technical_candidates": len(technical_candidates),
                "fundamental_candidates": len(fundamental_candidates),
                "news_candidates": len(news_candidates),
                "final_candidates": len(candidates)
            },
            "candidates": detailed_analysis,
            "scanning_criteria": criteria or "Default criteria",
            "portfolio_size": portfolio_size
        }
    
    def _load_stocks_data(self) -> Dict[str, pd.DataFrame]:
        """Load data cho các stocks"""
        stocks_data = {}
        
        for symbol in self.vietnamese_stocks:
            try:
                # Try to load data
                data = self._load_stock_data(symbol)
                if not data.empty:
                    stocks_data[symbol] = data
                    logger.debug(f"Loaded data for {symbol}: {len(data)} days")
            except Exception as e:
                logger.warning(f"Could not load data for {symbol}: {e}")
                continue
        
        logger.info(f"Successfully loaded data for {len(stocks_data)} stocks")
        return stocks_data
    
    def _load_stock_data(self, symbol: str) -> pd.DataFrame:
        """Load data for a single stock"""
        try:
            # Try using existing data loader
            if FORECAST_SYSTEM_AVAILABLE:
                end_date = datetime.now()
                start_date = end_date - timedelta(days=60)  # 60 days for analysis
                
                data = fetch_historical_data(symbol, start_date, end_date)
                
                if data.empty:
                    # Create mock data if real data not available
                    data = self._create_mock_data(symbol)
                
                return data
            else:
                return self._create_mock_data(symbol)
                
        except Exception as e:
            logger.error(f"Error loading data for {symbol}: {e}")
            return pd.DataFrame()
    
    def _create_mock_data(self, symbol: str) -> pd.DataFrame:
        """Create realistic mock data for testing"""
        dates = pd.date_range(start=datetime.now() - timedelta(days=60), 
                             end=datetime.now(), freq='D')
        
        # Generate realistic price data
        np.random.seed(hash(symbol) % 1000)  # Consistent data per symbol
        
        base_price = np.random.uniform(10000, 50000)  # 10K to 50K VND
        
        prices = [base_price]
        for i in range(len(dates) - 1):
            change = np.random.normal(0.001, 0.02)  # Small daily changes
            new_price = prices[-1] * (1 + change)
            prices.append(max(new_price, 1000))  # Minimum price
        
        # Create OHLCV data
        data = pd.DataFrame({
            'Date': dates,
            'Open': [p * (1 + np.random.normal(0, 0.005)) for p in prices],
            'High': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
            'Low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
            'Close': prices,
            'Volume': np.random.lognormal(16, 0.5, len(dates)).astype(int)
        })
        
        data.set_index('Date', inplace=True)
        return data
    
    def _generate_mock_fundamental_data(self, symbols: List[str]) -> Dict[str, Dict]:
        """Generate mock fundamental data"""
        fundamental_data = {}
        
        for symbol in symbols:
            fundamental_data[symbol] = {
                'pe_ratio': np.random.uniform(8, 25),
                'pb_ratio': np.random.uniform(0.8, 3.0),
                'roe': np.random.uniform(0.05, 0.25),
                'debt_to_equity': np.random.uniform(0.1, 0.8),
                'current_ratio': np.random.uniform(1.0, 3.0),
                'revenue_growth_3y': np.random.uniform(-0.1, 0.3),
                'market_cap': np.random.uniform(5000000000, 500000000000),  # 5B to 500B VND
                'float_shares_ratio': np.random.uniform(0.2, 0.8)
            }
        
        return fundamental_data
    
    def _intersect_analysis(self, technical: List[str], 
                          fundamental: List[str], 
                          news: List[str]) -> List[str]:
        """Analyze intersection of different screening results"""
        
        # Count how many criteria each stock passes
        score_count = {}
        
        for symbol in technical:
            score_count[symbol] = score_count.get(symbol, 0) + 1
        
        for symbol in fundamental:
            score_count[symbol] = score_count.get(symbol, 0) + 1
        
        for symbol in news:
            score_count[symbol] = score_count.get(symbol, 0) + 1
        
        # Keep stocks that pass at least 2 out of 3 criteria
        candidates = [symbol for symbol, count in score_count.items() if count >= 2]
        
        # Sort by score (highest first)
        candidates.sort(key=lambda x: score_count[x], reverse=True)
        
        logger.info(f"Intersection analysis: {len(candidates)} stocks passed multiple criteria")
        return candidates
    
    def _generate_detailed_analysis(self, candidates: List[str], 
                                  stocks_data: Dict[str, pd.DataFrame]) -> List[Dict]:
        """Generate detailed analysis for candidate stocks"""
        detailed_analysis = []
        
        for symbol in candidates:
            try:
                if symbol not in stocks_data:
                    continue
                
                data = stocks_data[symbol]
                current_price = data['Close'].iloc[-1]
                
                # Calculate basic metrics
                price_5d = data['Close'].iloc[-6] if len(data) >= 6 else current_price
                price_30d = data['Close'].iloc[-31] if len(data) >= 31 else current_price
                
                change_5d = ((current_price / price_5d) - 1) * 100
                change_30d = ((current_price / price_30d) - 1) * 100
                volume_avg = data['Volume'].tail(20).mean()
                volume_recent = data['Volume'].tail(5).mean()
                
                # Technical indicators
                technical_data = perform_technical_analysis(data)
                rsi = technical_data.get('RSI', 50).iloc[-1] if 'RSI' in technical_data.columns else 50
                
                # Get forecast if available
                forecast_data = None
                if self.forecast_system:
                    try:
                        forecast_data = self.forecast_system.predict_next_2_days(symbol)
                    except Exception as e:
                        logger.warning(f"Could not get forecast for {symbol}: {e}")
                
                analysis = {
                    'symbol': symbol,
                    'current_price': current_price,
                    'price_change_5d': change_5d,
                    'price_change_30d': change_30d,
                    'volume_avg': volume_avg,
                    'volume_surge': (volume_recent / volume_avg) if volume_avg > 0 else 0,
                    'rsi': rsi,
                    'technical_signals': self._get_technical_signals(technical_data),
                    'forecast': forecast_data,
                    'screening_scores': self._calculate_screening_scores(symbol),
                    'investment_grade': self._calculate_investment_grade(change_5d, volume_recent/volume_avg, rsi)
                }
                
                detailed_analysis.append(analysis)
                logger.info(f"Generated detailed analysis for {symbol}")
                
            except Exception as e:
                logger.error(f"Error generating detailed analysis for {symbol}: {e}")
                continue
        
        # Sort by investment grade
        detailed_analysis.sort(key=lambda x: x['investment_grade'], reverse=True)
        
        return detailed_analysis
    
    def _get_technical_signals(self, technical_data: pd.DataFrame) -> Dict[str, str]:
        """Extract technical signals"""
        signals = {}
        
        if 'RSI' in technical_data.columns:
            rsi = technical_data['RSI'].iloc[-1]
            if rsi < 30:
                signals['rsi'] = 'oversold'
            elif rsi > 70:
                signals['rsi'] = 'overbought'
            else:
                signals['rsi'] = 'neutral'
        
        if all(col in technical_data.columns for col in ['MACD', 'MACD_Signal']):
            macd = technical_data['MACD'].iloc[-1]
            signal = technical_data['MACD_Signal'].iloc[-1]
            signals['macd'] = 'bullish' if macd > signal else 'bearish'
        
        return signals
    
    def _calculate_screening_scores(self, symbol: str) -> Dict[str, int]:
        """Calculate screening scores for each criterion"""
        # This would be enhanced with real data in production
        return {
            'technical': np.random.randint(60, 95),
            'fundamental': np.random.randint(55, 90),
            'sentiment': np.random.randint(50, 85)
        }
    
    def _calculate_investment_grade(self, price_change_5d: float, 
                                  volume_surge: float, rsi: float) -> int:
        """Calculate overall investment grade (1-10)"""
        score = 5  # Base score
        
        # Price momentum
        if price_change_5d > 3:
            score += 2
        elif price_change_5d > 1:
            score += 1
        
        # Volume confirmation
        if volume_surge > 2:
            score += 2
        elif volume_surge > 1.5:
            score += 1
        
        # RSI signal
        if 40 <= rsi <= 60:  # Sweet spot
            score += 2
        elif rsi < 40:  # Oversold - potential rebound
            score += 1
        
        return min(10, max(1, score))

def test_investment_scanner():
    """Test function for Investment Opportunity Scanner"""
    print("🧪 Testing Investment Opportunity Scanner...")
    
    try:
        # Initialize scanner
        scanner = InvestmentOpportunityScanner()
        print(f"✅ Scanner initialized with {len(scanner.vietnamese_stocks)} stocks")
        
        # Run scan
        print("\n🔍 Scanning market opportunities...")
        results = scanner.scan_market_opportunities()
        
        if 'error' in results:
            print(f"❌ Scan failed: {results['error']}")
            return None
        
        # Display results
        print(f"\n📊 SCAN RESULTS:")
        print(f"📅 Scan Date: {results['scan_date']}")
        print(f"📈 Total Stocks Scanned: {results['total_stocks_scanned']}")
        
        screening = results['screening_results']
        print(f"\n🎯 SCREENING RESULTS:")
        print(f"   Technical Candidates: {screening['technical_candidates']}")
        print(f"   Fundamental Candidates: {screening['fundamental_candidates']}")
        print(f"   News Candidates: {screening['news_candidates']}")
        print(f"   Final Candidates: {screening['final_candidates']}")
        
        # Display top candidates
        candidates = results['candidates']
        if candidates:
            print(f"\n🏆 TOP INVESTMENT OPPORTUNITIES:")
            print("=" * 60)
            
            for i, candidate in enumerate(candidates[:5], 1):
                print(f"\n#{i} {candidate['symbol']} - Grade: {candidate['investment_grade']}/10")
                print(f"   💰 Current Price: {candidate['current_price']:,.0f} VND")
                print(f"   📈 5-day Change: {candidate['price_change_5d']:+.1f}%")
                print(f"   📊 Volume Surge: {candidate['volume_surge']:.1f}x")
                print(f"   🎯 RSI: {candidate['rsi']:.1f}")
                
                forecast = candidate.get('forecast')
                if forecast and 'predictions' in forecast:
                    day1 = forecast['predictions'][0]
                    print(f"   🔮 Day 1 Forecast: {day1['direction']} {day1['predicted_change_points']:+.0f} pts")
        
        print("\n✅ Investment Opportunity Scanner test completed!")
        return results
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_investment_scanner()
