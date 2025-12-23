"""
Enhanced Investment Scanner với Parallel Processing
Cải thiện hiệu suất scanning bằng cách sử dụng parallel processing và intelligent batching
"""

import asyncio
import concurrent.futures
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd
import streamlit as st
from datetime import datetime

# Import cache manager
try:
    from stock_analyzer.utils.cache_manager import get_cache_manager, cached_analysis
except ImportError:
    # Fallback if cache manager not available
    get_cache_manager = None
    cached_analysis = None


class EnhancedInvestmentScanner:
    """
    Enhanced investment scanner với parallel processing và intelligent batching
    """
    
    def __init__(self, max_workers: int = 10, batch_size: int = 20, use_cache: bool = True):
        self.max_workers = max_workers
        self.batch_size = batch_size
        self.use_cache = use_cache
        self.cache_manager = get_cache_manager() if use_cache and get_cache_manager else None
        
    def find_investment_opportunities_parallel(
        self, 
        all_tickers: List[str], 
        commission_rate: float, 
        slippage_rate: float,
        progress_callback=None
    ) -> Dict[str, Any]:
        """
        Enhanced parallel scanning với progress tracking và error handling
        """
        potential_opportunities = {
            'buy': [],
            'sell': [],
            'hold': [],
            'total_analyzed': 0,
            'total_errors': 0,
            'execution_time': 0,
            'cache_hits': 0,
            'errors': []
        }
        
        start_time = time.time()
        
        # Process tickers in batches
        total_tickers = len(all_tickers)
        processed_count = 0
        error_count = 0
        cache_hits = 0
        
        # Split tickers into batches
        ticker_batches = [
            all_tickers[i:i + self.batch_size] 
            for i in range(0, len(all_tickers), self.batch_size)
        ]
        
        total_batches = len(ticker_batches)
        
        for batch_idx, ticker_batch in enumerate(ticker_batches):
            if progress_callback:
                progress_callback(batch_idx, total_batches, f"Processing batch {batch_idx + 1}/{total_batches}")
            
            # Process batch in parallel
            batch_results = self._process_batch_parallel(
                ticker_batch, commission_rate, slippage_rate
            )
            
            # Aggregate results
            for result in batch_results:
                if result['success']:
                    processed_count += 1
                    opportunity = result['opportunity']
                    
                    if opportunity['action'] == 'Buy':
                        potential_opportunities['buy'].append(opportunity)
                    elif opportunity['action'] == 'Sell':
                        potential_opportunities['sell'].append(opportunity)
                    else:
                        potential_opportunities['hold'].append(opportunity)
                        
                    if result.get('from_cache'):
                        cache_hits += 1
                else:
                    error_count += 1
                    potential_opportunities['errors'].append({
                        'ticker': result['ticker'],
                        'error': result['error']
                    })
        
        # Update final results
        potential_opportunities['total_analyzed'] = processed_count
        potential_opportunities['total_errors'] = error_count
        potential_opportunities['execution_time'] = round(time.time() - start_time, 2)
        potential_opportunities['cache_hits'] = cache_hits
        potential_opportunities['cache_hit_rate'] = round(
            (cache_hits / processed_count * 100) if processed_count > 0 else 0, 2
        )
        
        return potential_opportunities
    
    def _process_batch_parallel(
        self, 
        ticker_batch: List[str], 
        commission_rate: float, 
        slippage_rate: float
    ) -> List[Dict[str, Any]]:
        """
        Process a batch of tickers in parallel
        """
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_ticker = {
                executor.submit(
                    self._analyze_single_ticker, 
                    ticker, commission_rate, slippage_rate
                ): ticker 
                for ticker in ticker_batch
            }
            
            # Collect results
            for future in as_completed(future_to_ticker):
                ticker = future_to_ticker[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({
                        'ticker': ticker,
                        'success': False,
                        'error': str(e),
                        'opportunity': None
                    })
        
        return results
    
    def _analyze_single_ticker(
        self, 
        ticker: str, 
        commission_rate: float, 
        slippage_rate: float
    ) -> Dict[str, Any]:
        """
        Analyze single ticker với cache support
        """
        try:
            # Try cache first if enabled
            if self.use_cache and self.cache_manager:
                cache_result = self._get_cached_analysis(ticker, commission_rate, slippage_rate)
                if cache_result:
                    return {
                        'ticker': ticker,
                        'success': True,
                        'opportunity': cache_result,
                        'from_cache': True
                    }
            
            # Perform fresh analysis
            analysis_results = self._perform_analysis(ticker, commission_rate, slippage_rate)
            
            if analysis_results:
                opportunity = self._create_opportunity_from_analysis(ticker, analysis_results)
                
                # Cache result if cache is enabled
                if self.use_cache and self.cache_manager:
                    self._cache_analysis(ticker, commission_rate, slippage_rate, analysis_results)
                
                return {
                    'ticker': ticker,
                    'success': True,
                    'opportunity': opportunity,
                    'from_cache': False
                }
            else:
                return {
                    'ticker': ticker,
                    'success': False,
                    'error': 'No analysis results',
                    'opportunity': None
                }
                
        except Exception as e:
            return {
                'ticker': ticker,
                'success': False,
                'error': str(e),
                'opportunity': None
            }
    
    def _get_cached_analysis(self, ticker: str, commission_rate: float, slippage_rate: float) -> Optional[Dict[str, Any]]:
        """
        Get analysis from cache
        """
        if not self.cache_manager:
            return None
            
        params = {
            'commission_rate': commission_rate,
            'slippage_rate': slippage_rate,
            'timestamp': datetime.now().strftime('%Y-%m-%d')
        }
        
        cached = self.cache_manager.get(ticker, 'full_analysis', params)
        if cached:
            return cached
        return None
    
    def _cache_analysis(self, ticker: str, commission_rate: float, slippage_rate: float, analysis_results: Dict[str, Any]):
        """
        Cache analysis results
        """
        if not self.cache_manager:
            return
            
        params = {
            'commission_rate': commission_rate,
            'slippage_rate': slippage_rate,
            'timestamp': datetime.now().strftime('%Y-%m-%d')
        }
        
        self.cache_manager.set(ticker, 'full_analysis', params, analysis_results)
    
    def _perform_analysis(self, ticker: str, commission_rate: float, slippage_rate: float) -> Optional[Dict[str, Any]]:
        """
        Perform analysis using the existing run_analysis function
        """
        try:
            from stock_analyzer.modules.core_analysis import run_analysis
            
            # Create analysis parameters
            from datetime import datetime, timedelta
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            
            # Run analysis (synchronous version for now)
            results = run_analysis(
                ticker,
                commission_rate,
                slippage_rate,
                display_progress=None,  # No progress for individual analysis
                start_date=start_date,
                end_date=end_date
            )
            
            return results
            
        except Exception as e:
            st.error(f"Error analyzing {ticker}: {e}")
            return None
    
    def _create_opportunity_from_analysis(self, ticker: str, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create opportunity object from analysis results
        """
        try:
            final_recommendation = analysis_results.get('final_recommendation', {})
            trend_predictions = analysis_results.get('trend_predictions', {})
            sentiment_results = analysis_results.get('sentiment_results', {})
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence_score(analysis_results)
            
            opportunity = {
                'ticker': ticker,
                'action': final_recommendation.get('action', 'Hold'),
                'entry_point': final_recommendation.get('entry_point', 'N/A'),
                'take_profit': final_recommendation.get('take_profit', 'N/A'),
                'stop_loss': final_recommendation.get('stop_loss', 'N/A'),
                'reasoning': final_recommendation.get('reasoning', []),
                'confidence': confidence_score,
                'rsi': self._get_rsi_value(analysis_results),
                'trend': trend_predictions.get('short_term_trend', 'N/A'),
                'sentiment': sentiment_results.get('sentiment_category', 'N/A'),
                'financial_health': analysis_results.get('financial_health', {}).get('overall_assessment', 'N/A'),
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            return opportunity
            
        except Exception as e:
            st.error(f"Error creating opportunity for {ticker}: {e}")
            return {
                'ticker': ticker,
                'action': 'Hold',
                'entry_point': 'N/A',
                'take_profit': 'N/A',
                'stop_loss': 'N/A',
                'reasoning': [f'Error creating opportunity: {str(e)}'],
                'confidence': 0,
                'rsi': 'N/A',
                'trend': 'N/A',
                'sentiment': 'N/A',
                'financial_health': 'N/A',
                'analysis_timestamp': datetime.now().isoformat()
            }
    
    def _calculate_confidence_score(self, analysis_results: Dict[str, Any]) -> float:
        """
        Calculate confidence score based on multiple factors
        """
        try:
            confidence = 50.0  # Base confidence
            
            # Factor 1: Number of reasoning points
            reasoning = analysis_results.get('final_recommendation', {}).get('reasoning', [])
            confidence += len(reasoning) * 5
            
            # Factor 2: Financial health
            financial_health = analysis_results.get('financial_health', {})
            if financial_health.get('overall_assessment') == 'Strong':
                confidence += 15
            elif financial_health.get('overall_assessment') == 'Weak':
                confidence -= 15
            
            # Factor 3: Technical indicators strength
            tech_data = analysis_results.get('technical_data')
            if tech_data is not None and not tech_data.empty:
                if 'RSI' in tech_data.columns:
                    rsi = tech_data['RSI'].iloc[-1]
                    if rsi < 30 or rsi > 70:  # Strong signal
                        confidence += 10
                    elif 30 <= rsi <= 70:  # Neutral
                        confidence += 5
            
            # Factor 4: Sentiment alignment
            sentiment_results = analysis_results.get('sentiment_results', {})
            sentiment_category = sentiment_results.get('sentiment_category', 'Neutral')
            final_action = analysis_results.get('final_recommendation', {}).get('action', 'Hold')
            
            if (sentiment_category == 'Positive' and final_action == 'Buy') or \
               (sentiment_category == 'Negative' and final_action == 'Sell'):
                confidence += 10
            elif sentiment_category == 'Neutral':
                confidence += 5
            
            # Ensure confidence is within bounds
            return max(0, min(100, confidence))
            
        except Exception:
            return 50.0  # Default confidence
    
    def _get_rsi_value(self, analysis_results: Dict[str, Any]) -> str:
        """
        Get RSI value from analysis results
        """
        try:
            tech_data = analysis_results.get('technical_data')
            if tech_data is not None and 'RSI' in tech_data.columns:
                return f"{tech_data['RSI'].iloc[-1]:.1f}"
        except:
            pass
        return "N/A"


def create_progress_callback():
    """
    Create Streamlit progress callback
    """
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    def callback(batch_idx: int, total_batches: int, message: str):
        progress = (batch_idx + 1) / total_batches
        progress_bar.progress(progress)
        status_text.text(f"{message} - {int(progress * 100)}%")
    
    return callback


# Enhanced scanner function that replaces the original
def enhanced_find_investment_opportunities(
    all_tickers: List[str], 
    commission_rate: float, 
    slippage_rate: float,
    max_workers: int = 10,
    batch_size: int = 20,
    use_cache: bool = True
) -> Dict[str, Any]:
    """
    Enhanced version of find_investment_opportunities với parallel processing
    """
    scanner = EnhancedInvestmentScanner(
        max_workers=max_workers,
        batch_size=batch_size,
        use_cache=use_cache
    )
    
    return scanner.find_investment_opportunities_parallel(
        all_tickers, commission_rate, slippage_rate
    )


if __name__ == "__main__":
    # Test the enhanced scanner
    test_tickers = ["AAA", "BBB", "CCC", "DDD", "EEE"]
    scanner = EnhancedInvestmentScanner(max_workers=5, batch_size=3)
    
    results = scanner.find_investment_opportunities_parallel(
        test_tickers, 0.0015, 0.0005
    )
    
    print("Enhanced Scanner Results:")
    print(f"Total analyzed: {results['total_analyzed']}")
    print(f"Total errors: {results['total_errors']}")
    print(f"Execution time: {results['execution_time']} seconds")
    print(f"Buy opportunities: {len(results['buy'])}")
    print(f"Sell opportunities: {len(results['sell'])}")
    print(f"Hold opportunities: {len(results['hold'])}")
    print(f"Cache hits: {results['cache_hits']}")
    print(f"Cache hit rate: {results['cache_hit_rate']}%")