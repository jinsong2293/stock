"""
Enhanced Main Application với tất cả performance improvements
Tích hợp cache system, parallel processing, responsive design
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional
import time
from datetime import datetime

# Import enhanced components
from stock_analyzer.config.settings import get_config, get_performance_config, get_cache_config
from stock_analyzer.utils.cache_manager import get_cache_manager, display_cache_stats, cleanup_cache
from stock_analyzer.utils.enhanced_scanner import EnhancedInvestmentScanner, create_progress_callback
from stock_analyzer.ui.responsive_components import (
    ResponsiveLayoutManager, 
    EnhancedLoadingStates, 
    ErrorHandlingUI,
    ProgressiveLoadingComponent
)

# Import existing modules
from stock_analyzer.modules.core_analysis import run_analysis
from stock_analyzer.modules.investment_scanner import find_investment_opportunities


class EnhancedStockAnalyzer:
    """
    Enhanced Stock Analyzer với tất cả performance improvements
    """
    
    def __init__(self):
        # Initialize configuration
        self.config = get_config()
        self.performance_config = get_performance_config()
        self.cache_config = get_cache_config()
        
        # Initialize components
        self.cache_manager = get_cache_manager() if self.cache_config['use_cache'] else None
        self.layout_manager = ResponsiveLayoutManager()
        self.enhanced_scanner = None
        
        # Session state management
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize session state variables"""
        if 'analysis_cache' not in st.session_state:
            st.session_state.analysis_cache = {}
        if 'scanner_cache' not in st.session_state:
            st.session_state.scanner_cache = {}
        if 'device_type' not in st.session_state:
            st.session_state.device_type = 'desktop'
        if 'sidebar_collapsed' not in st.session_state:
            st.session_state.sidebar_collapsed = False
    
    def run_enhanced_analysis(self, ticker: str, commission_rate: float, slippage_rate: float, 
                            start_date=None, end_date=None) -> Optional[Dict[str, Any]]:
        """
        Run analysis với caching và error handling
        """
        try:
            # Create cache key
            cache_params = {
                'ticker': ticker,
                'commission_rate': commission_rate,
                'slippage_rate': slippage_rate,
                'start_date': start_date.isoformat() if start_date else None,
                'end_date': end_date.isoformat() if end_date else None
            }
            
            # Try cache first
            if self.cache_manager:
                cached_result = self.cache_manager.get(ticker, 'full_analysis', cache_params)
                if cached_result:
                    st.success(f"📋 Loaded {ticker} from cache (instant load)")
                    return cached_result
            
            # Show progress for fresh analysis
            EnhancedLoadingStates.create_analysis_progress('full_analysis', 1, 5)
            
            # Run analysis
            with st.spinner(f"Analyzing {ticker}..."):
                result = run_analysis(
                    ticker, commission_rate, slippage_rate, 
                    display_progress=None, start_date=start_date, end_date=end_date
                )
            
            if result and self.cache_manager:
                # Cache the result
                self.cache_manager.set(ticker, 'full_analysis', cache_params, result)
                st.success(f"✅ Analysis completed and cached for {ticker}")
            
            return result
            
        except Exception as e:
            ErrorHandlingUI.display_user_friendly_error('analysis_failed', ticker, str(e))
            return None
    
    def run_enhanced_scanner(self, tickers: list, commission_rate: float, slippage_rate: float) -> Dict[str, Any]:
        """
        Run enhanced scanner với parallel processing
        """
        try:
            if not self.enhanced_scanner:
                perf_config = get_performance_config()
                self.enhanced_scanner = EnhancedInvestmentScanner(
                    max_workers=perf_config['max_workers'],
                    batch_size=perf_config['batch_size'],
                    use_cache=self.cache_config['use_cache']
                )
            
            # Create progress callback
            progress_callback = create_progress_callback()
            
            # Run enhanced scanner
            with st.spinner("Running enhanced scanner with parallel processing..."):
                results = self.enhanced_scanner.find_investment_opportunities_parallel(
                    tickers, commission_rate, slippage_rate, progress_callback
                )
            
            return results
            
        except Exception as e:
            ErrorHandlingUI.display_user_friendly_error('analysis_failed', details=str(e))
            return {'buy': [], 'sell': [], 'hold': [], 'total_analyzed': 0, 'total_errors': 1}
    
    def create_enhanced_sidebar(self):
        """
        Create enhanced sidebar với performance monitoring
        """
        with st.sidebar:
            # Enhanced header
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, var(--primary) 0%, var(--primary_dark) 100%); 
                color: white; 
                padding: 1rem; 
                border-radius: 0.5rem; 
                margin-bottom: 1rem;
                text-align: center;
            ">
                <h3 style="margin: 0;">📈 Stock Analyzer Pro</h3>
                <p style="margin: 0.25rem 0 0 0; font-size: 0.875rem; opacity: 0.9;">Enhanced Performance</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Performance monitoring section
            if st.expander("🚀 Performance Monitor", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Workers", self.performance_config['max_workers'])
                    st.metric("Batch Size", self.performance_config['batch_size'])
                with col2:
                    if self.cache_manager:
                        stats = self.cache_manager.get_cache_stats()
                        st.metric("Cache Hits", f"{stats.get('cache_hit_rate', 0):.1f}%")
                    else:
                        st.metric("Cache", "Disabled")
                
                # Cache management
                if self.cache_manager:
                    if st.button("🧹 Clear Expired Cache"):
                        expired_count, old_count = cleanup_cache()
                        st.success(f"Cleaned {expired_count} expired + {old_count} old entries")
                        st.rerun()
            
            st.markdown("---")
            
            # Enhanced ticker selection
            st.markdown("### 📊 Stock Selection")
            
            # File path cho stocks data
            STOCK_DATA_PATH = "stock_analyzer/data/stocks.csv"
            
            try:
                stocks_df = pd.read_csv(STOCK_DATA_PATH)
                valid_tickers = stocks_df['Ticker'].tolist()
                
                selected_ticker = st.selectbox(
                    "Choose Stock:",
                    [""] + valid_tickers,
                    key="enhanced_ticker_selector"
                )
                
            except Exception as e:
                st.error(f"Could not load stock list: {e}")
                selected_ticker = st.text_input("Enter Ticker:", key="enhanced_ticker_input")
                valid_tickers = [selected_ticker] if selected_ticker else []
            
            st.markdown("---")
            
            # Enhanced settings
            with st.expander("⚙️ Enhanced Settings", expanded=False):
                # Analysis settings
                rsi_window = st.slider("RSI Window", 7, 28, 14)
                macd_fast = st.slider("MACD Fast", 8, 15, 12)
                macd_slow = st.slider("MACD Slow", 20, 30, 26)
                
                # Risk management
                commission_rate = st.number_input(
                    "Commission Rate (%)", 
                    min_value=0.0, max_value=1.0, 
                    value=self.config.get_setting('DEFAULT_COMMISSION_RATE', 0.0015) * 100,
                    step=0.01
                ) / 100
                
                slippage_rate = st.number_input(
                    "Slippage Rate (%)", 
                    min_value=0.0, max_value=0.5, 
                    value=self.config.get_setting('DEFAULT_SLIPPAGE_RATE', 0.0005) * 100,
                    step=0.01
                ) / 100
                
                # Performance settings
                max_workers = st.slider("Max Workers", 1, 20, self.performance_config['max_workers'])
                batch_size = st.slider("Batch Size", 5, 50, self.performance_config['batch_size'])
                
                # Update performance config
                if st.button("💾 Apply Settings"):
                    self.performance_config.update({
                        'max_workers': max_workers,
                        'batch_size': batch_size
                    })
                    st.success("Settings updated!")
            
            return selected_ticker, commission_rate, slippage_rate, valid_tickers
    
    def create_enhanced_main_content(self, ticker: str, analysis_results: Optional[Dict[str, Any]]):
        """
        Create enhanced main content với responsive design
        """
        if not ticker:
            st.info("👆 Please select a stock to begin analysis")
            return
        
        if not analysis_results:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 Start Analysis", type="primary", use_container_width=True):
                    # This would trigger analysis
                    st.info("Analysis started...")
            return
        
        # Display analysis results với responsive design
        self._display_enhanced_results(ticker, analysis_results)
    
    def _display_enhanced_results(self, ticker: str, results: Dict[str, Any]):
        """
        Display analysis results với enhanced UI
        """
        # Enhanced header
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary_dark) 100%); 
            color: white; 
            padding: 2rem; 
            border-radius: 1rem; 
            margin-bottom: 2rem; 
            text-align: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        ">
            <h1 style="margin: 0; font-size: 2.5rem; font-weight: 800;">📊 {ticker}</h1>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem;">
                Enhanced Analysis Report
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick metrics với responsive grid
        tech_data = results.get('technical_data')
        if tech_data is not None and not tech_data.empty:
            metrics_data = [
                {'label': 'Current Price', 'value': f"${tech_data['Close'].iloc[-1]:.2f}", 'icon': '💰'},
                {'label': 'RSI', 'value': f"{tech_data['RSI'].iloc[-1]:.1f}", 'icon': '📈'},
                {'label': 'Volume', 'value': f"{tech_data['Volume'].iloc[-1]:,.0f}", 'icon': '📊'},
                {'label': 'MACD', 'value': f"{tech_data['MACD'].iloc[-1]:.3f}", 'icon': '📉'}
            ]
            
            self.layout_manager.create_responsive_metric_grid(metrics_data)
        
        # Enhanced tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Technical", "📰 Sentiment", "🔮 Predictions", "💰 Financial"])
        
        with tab1:
            self._display_technical_analysis(results)
        
        with tab2:
            self._display_sentiment_analysis(results)
        
        with tab3:
            self._display_predictions(results)
        
        with tab4:
            self._display_financial_analysis(results)
    
    def _display_technical_analysis(self, results: Dict[str, Any]):
        """Enhanced technical analysis display"""
        st.subheader("📊 Technical Analysis")
        
        tech_data = results.get('technical_data')
        if tech_data is not None and not tech_data.empty:
            # Create chart với lazy loading
            try:
                from stock_analyzer.app_new import _create_price_chart
                chart = ProgressiveLoadingComponent.create_lazy_chart(_create_price_chart, tech_data)
                if chart:
                    st.plotly_chart(chart, use_container_width=True)
            except Exception as e:
                ErrorHandlingUI.display_user_friendly_error('analysis_failed', details=str(e))
            
            # Enhanced data table
            st.subheader("📋 Technical Data")
            cols_to_show = ['Close', 'RSI', 'MACD', 'MACD_Signal', 'BB_Upper', 'BB_Lower']
            available_cols = [col for col in cols_to_show if col in tech_data.columns]
            
            if available_cols:
                display_data = tech_data[available_cols].tail(10)
                st.dataframe(display_data, use_container_width=True)
        else:
            st.info("No technical data available")
    
    def _display_sentiment_analysis(self, results: Dict[str, Any]):
        """Enhanced sentiment analysis display"""
        st.subheader("📰 Market Sentiment")
        
        sentiment_results = results.get('sentiment_results', {})
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sentiment_score = sentiment_results.get('sentiment_score', 0.0)
            st.metric("Sentiment Score", f"{sentiment_score:.2f}")
        
        with col2:
            sentiment_category = sentiment_results.get('sentiment_category', 'Neutral')
            st.metric("Sentiment", sentiment_category)
        
        with col3:
            news_impact = sentiment_results.get('news_impact', 'N/A')
            st.metric("News Impact", news_impact)
        
        # Sentiment breakdown
        if sentiment_results:
            st.markdown("### 📊 Sentiment Breakdown")
            st.json(sentiment_results)
    
    def _display_predictions(self, results: Dict[str, Any]):
        """Enhanced predictions display"""
        st.subheader("🔮 Trend Predictions")
        
        trend_predictions = results.get('trend_predictions', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            short_trend = trend_predictions.get('short_term_trend', 'N/A')
            short_conf = trend_predictions.get('short_term_confidence', 'N/A')
            st.metric("Short Term Trend", short_trend, short_conf)
        
        with col2:
            medium_trend = trend_predictions.get('medium_term_trend', 'N/A')
            medium_conf = trend_predictions.get('medium_term_confidence', 'N/A')
            st.metric("Medium Term Trend", medium_trend, medium_conf)
        
        # Price forecast
        price_forecast = trend_predictions.get('price_forecast_next_5_days', {})
        if price_forecast:
            st.markdown("### 📈 5-Day Price Forecast")
            forecast_df = pd.DataFrame(list(price_forecast.items()), columns=['Date', 'Predicted Price'])
            st.line_chart(forecast_df.set_index('Date'))
    
    def _display_financial_analysis(self, results: Dict[str, Any]):
        """Enhanced financial analysis display"""
        st.subheader("💰 Financial Analysis")
        
        financial_data = results.get('financial_data', {})
        financial_health = results.get('financial_health', {})
        
        # Financial health assessment
        assessment = financial_health.get('overall_assessment', 'Unknown')
        if "Strong" in assessment:
            st.success(f"**Financial Health: {assessment}** ✅")
        elif "Weak" in assessment:
            st.error(f"**Financial Health: {assessment}** ⚠️")
        else:
            st.info(f"**Financial Health: {assessment}** ℹ️")
        
        # Key financial metrics
        if financial_data:
            st.markdown("### 📊 Key Metrics")
            metrics_cols = st.columns(3)
            
            key_metrics = ['pe_ratio', 'pb_ratio', 'roe_percent', 'roa_percent', 'debt_to_equity_ratio']
            
            for i, metric in enumerate(key_metrics):
                if metric in financial_data:
                    with metrics_cols[i % 3]:
                        value = financial_data[metric]
                        if value is not None:
                            if isinstance(value, float):
                                st.metric(metric.replace('_', ' ').title(), f"{value:.2f}")
                            else:
                                st.metric(metric.replace('_', ' ').title(), str(value))
        
        # Financial comments
        comments = financial_health.get('comments', [])
        if comments:
            st.markdown("### 💬 Analysis Comments")
            for comment in comments:
                st.write(f"• {comment}")


def create_enhanced_main_app():
    """
    Create enhanced main application
    """
    st.set_page_config(
        page_title="Stock Analyzer Pro - Enhanced Performance",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize enhanced analyzer
    analyzer = EnhancedStockAnalyzer()
    
    # Create responsive layout
    col_sidebar, col_main = st.columns([1, 4])
    
    with col_sidebar:
        selected_ticker, commission_rate, slippage_rate, valid_tickers = analyzer.create_enhanced_sidebar()
    
    with col_main:
        # Main content area
        if selected_ticker:
            # Check for cached analysis
            cache_key = f"{selected_ticker}_{datetime.now().strftime('%Y-%m-%d')}"
            
            if cache_key in st.session_state.analysis_cache:
                st.success("📋 Loading from session cache")
                analysis_results = st.session_state.analysis_cache[cache_key]
            else:
                # Run analysis
                analysis_results = analyzer.run_enhanced_analysis(
                    selected_ticker, commission_rate, slippage_rate
                )
                
                if analysis_results:
                    # Cache in session
                    st.session_state.analysis_cache[cache_key] = analysis_results
            
            # Display results
            analyzer.create_enhanced_main_content(selected_ticker, analysis_results)
        else:
            # Welcome screen với enhanced design
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                padding: 3rem; 
                border-radius: 1rem; 
                text-align: center; 
                margin: 2rem 0;
            ">
                <h1 style="margin: 0; font-size: 3rem;">📈 Stock Analyzer Pro</h1>
                <p style="margin: 1rem 0; font-size: 1.2rem; opacity: 0.9;">
                    Enhanced Performance • Parallel Processing • Smart Caching
                </p>
                <p style="margin: 0; font-size: 1rem; opacity: 0.8;">
                    Choose a stock from the sidebar to begin your analysis
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced scanner section
            if valid_tickers:
                st.markdown("### 🚀 Enhanced Market Scanner")
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("🔍 Scan All Stocks (Enhanced)", type="primary", use_container_width=True):
                        with st.spinner("Running enhanced scanner..."):
                            scanner_results = analyzer.run_enhanced_scanner(
                                valid_tickers, commission_rate, slippage_rate
                            )
                            
                            # Display results
                            if scanner_results:
                                st.success(f"Scanner completed! Analyzed {scanner_results['total_analyzed']} stocks")
                                
                                col1, col2, col3, col4 = st.columns(4)
                                with col1:
                                    st.metric("Buy Signals", len(scanner_results['buy']))
                                with col2:
                                    st.metric("Sell Signals", len(scanner_results['sell']))
                                with col3:
                                    st.metric("Hold Signals", len(scanner_results['hold']))
                                with col4:
                                    st.metric("Execution Time", f"{scanner_results['execution_time']}s")
                                
                                # Cache stats
                                if scanner_results.get('cache_hits', 0) > 0:
                                    st.info(f"🚀 Cache hits: {scanner_results['cache_hits']} ({scanner_results['cache_hit_rate']}%)")
            
            # Performance stats
            with st.expander("📊 System Performance", expanded=False):
                if analyzer.cache_manager:
                    display_cache_stats()


if __name__ == "__main__":
    create_enhanced_main_app()