import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import sys
from typing import Dict, Optional, Any
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from stock_analyzer.modules.data_loader import fetch_historical_data, preprocess_data
from stock_analyzer.modules.technical_analysis import perform_technical_analysis
from stock_analyzer.modules.sentiment_analysis import analyze_market_sentiment
from stock_analyzer.modules.advanced_analysis import perform_advanced_analysis
from stock_analyzer.modules.financial_analysis import perform_financial_analysis
from stock_analyzer.modules.recommendation_engine import generate_recommendation

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('stock_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_analysis(selected_ticker: str, commission_rate: float, slippage_rate: float, display_progress: Optional[Any] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> Optional[Dict[str, Any]]:
    """
    Runs the full stock analysis for a given ticker and returns the results.
    Can optionally display progress using a Streamlit progress handler.
    Supports custom date ranges.
    """
    try:
        logger.info(f"Starting analysis for ticker: {selected_ticker}")
        
        if display_progress:
            st.write(f"Đang thực hiện phân tích chuyên sâu cho **{selected_ticker}**...")
        else:
            print(f"Đang thực hiện phân tích chuyên sâu cho {selected_ticker}...")

        if end_date is None:
            end_date = datetime.now()
        if start_date is None:
            start_date = end_date - timedelta(days=365 * 2)

        logger.info(f"Fetching historical data for {selected_ticker} from {start_date} to {end_date}")
        historical_data = fetch_historical_data(selected_ticker, start_date, end_date)
        if historical_data.empty:
            msg = f"❌ Không có dữ liệu lịch sử cho {selected_ticker}. Vui lòng kiểm tra mã cổ phiếu."
            logger.warning(msg)
            if display_progress:
                st.warning(msg)
            else:
                print(msg)
            return None

        logger.info(f"Preprocessing data for {selected_ticker}")
        processed_data = preprocess_data(historical_data)
        if processed_data.empty:
            msg = f"❌ Tiền xử lý dữ liệu thất bại cho {selected_ticker}."
            logger.error(msg)
            if display_progress:
                st.warning(msg)
            else:
                print(msg)
            return None

        if display_progress:
            st.success(f"✅ Đã tải dữ liệu thành công cho {selected_ticker}.")

        technical_params = {}
        if display_progress and hasattr(st, 'session_state') and 'indicator_params' in st.session_state:
            technical_params = st.session_state['indicator_params']
        
        logger.info(f"Performing technical analysis for {selected_ticker}")
        technical_analyzed_data = perform_technical_analysis(processed_data.copy(), **technical_params)
        if technical_analyzed_data.empty:
            msg = f"❌ Phân tích kỹ thuật thất bại cho {selected_ticker}."
            logger.error(msg)
            if display_progress:
                st.warning(msg)
            else:
                print(msg)
            return None
         
        if display_progress:
            st.info(f"✓ Phân tích kỹ thuật cho {selected_ticker} đã hoàn tất.")

        logger.info(f"Analyzing market sentiment for {selected_ticker}")
        sentiment_results = analyze_market_sentiment(selected_ticker, processed_data)
        if display_progress:
            st.info(f"✓ Phân tích tâm lý thị trường cho {selected_ticker} đã hoàn tất.")

        logger.info(f"Performing advanced analysis for {selected_ticker}")
        trend_predictions, anomaly_detections_zscore, anomaly_detections_isolation, anomaly_detections_dbscan = perform_advanced_analysis(technical_analyzed_data.copy())
        if display_progress:
            st.info(f"✓ Phân tích nâng cao cho {selected_ticker} đã hoàn tất.")

        logger.info(f"Performing financial analysis for {selected_ticker}")
        financial_data, financial_health = perform_financial_analysis(selected_ticker)
        if display_progress:
            st.info(f"✓ Phân tích tài chính cho {selected_ticker} đã hoàn tất.")

        logger.info(f"Generating recommendation for {selected_ticker}")
        final_recommendation = generate_recommendation(
            technical_analyzed_data.copy(),
            sentiment_results,
            trend_predictions,
            anomaly_detections_zscore,
            financial_health,
            commission_rate=commission_rate,
            slippage_rate=slippage_rate
        )
         
        if display_progress:
            st.success(f"✅ Phân tích hoàn tất cho {selected_ticker}!")

        logger.info(f"Analysis completed successfully for {selected_ticker}")
        return {
            "technical_data": technical_analyzed_data,
            "sentiment_results": sentiment_results,
            "trend_predictions": trend_predictions,
            "anomaly_detections_zscore": anomaly_detections_zscore,
            "anomaly_detections_isolation": anomaly_detections_isolation,
            "anomaly_detections_dbscan": anomaly_detections_dbscan,
            "financial_data": financial_data,
            "financial_health": financial_health,
            "final_recommendation": final_recommendation
        }
     
    except Exception as e:
        msg = f"❌ Lỗi không mong đợi khi phân tích {selected_ticker}: {str(e)}"
        logger.error(f"Unexpected error during analysis for {selected_ticker}: {str(e)}", exc_info=True)
        if display_progress:
            st.error(msg)
        else:
            print(msg)
        return None
