import streamlit as st
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any

def find_investment_opportunities(all_tickers: List[str], commission_rate: float, slippage_rate: float) -> Dict[str, Any]:
    from stock_analyzer.modules.core_analysis import run_analysis
    
    potential_opportunities = {
        'buy': [],
        'sell': [],
        'hold': [],
        'total_analyzed': 0,
        'total_errors': 0
    }
    
    placeholder_status = st.empty()
    placeholder_progress = st.empty()
    placeholder_ticker = st.empty()
    
    total_tickers = len(all_tickers)
    processed_count = 0
    error_count = 0
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_ticker = {executor.submit(run_analysis, ticker, commission_rate, slippage_rate, None): ticker for ticker in all_tickers}
        
        for future in as_completed(future_to_ticker):
            ticker = future_to_ticker[future]
            try:
                with placeholder_ticker.container():
                    st.info(f"🔄 Đang phân tích: {ticker}")
                
                analysis_results = future.result()
                
                if analysis_results:
                    action = analysis_results['final_recommendation']['action']
                    confidence_score = calculate_confidence_score(analysis_results)
                    
                    opportunity_data = {
                        "ticker": ticker,
                        "action": action,
                        "entry_point": analysis_results['final_recommendation']['entry_point'],
                        "take_profit": analysis_results['final_recommendation']['take_profit'],
                        "stop_loss": analysis_results['final_recommendation']['stop_loss'],
                        "reasoning": analysis_results['final_recommendation'].get('reasoning', []),
                        "confidence": confidence_score,
                        "rsi": get_rsi_value(analysis_results),
                        "trend": analysis_results.get('trend_predictions', {}).get('short_term_trend', 'N/A'),
                        "sentiment": analysis_results.get('sentiment_results', {}).get('sentiment_category', 'N/A')
                    }
                    
                    if action == 'Buy':
                        potential_opportunities['buy'].append(opportunity_data)
                    elif action == 'Sell':
                        potential_opportunities['sell'].append(opportunity_data)
                    else:
                        potential_opportunities['hold'].append(opportunity_data)
                        
            except Exception as exc:
                error_count += 1
                pass
            finally:
                processed_count += 1
                with placeholder_progress.container():
                    progress_percent = processed_count / total_tickers
                    st.progress(progress_percent, text=f"Tiến độ: {processed_count}/{total_tickers}")
                
                with placeholder_status.container():
                    st.info(f"📊 Đã phân tích: {processed_count}/{total_tickers} | Lỗi: {error_count}")
    
    placeholder_ticker.empty()
    
    potential_opportunities['total_analyzed'] = processed_count - error_count
    potential_opportunities['total_errors'] = error_count
    
    return potential_opportunities

def calculate_confidence_score(analysis_results: Dict[str, Any]) -> float:
    reasoning = analysis_results['final_recommendation'].get('reasoning', [])
    score = len(reasoning) * 15
    return min(score, 95)

def get_rsi_value(analysis_results: Dict[str, Any]) -> str:
    try:
        tech_data = analysis_results.get('technical_data')
        if tech_data is not None and 'RSI' in tech_data.columns:
            return f"{tech_data['RSI'].iloc[-1]:.1f}"
    except:
        pass
    return "N/A"
