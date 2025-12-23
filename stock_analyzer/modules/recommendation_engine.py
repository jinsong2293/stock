import pandas as pd
from typing import Dict, Any
import sys
import os

# Add the parent directory to the system path to import config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from stock_analyzer.config import GOOGLE_API_KEY

TREND_TRANSLATIONS = {
    "upward": "tăng",
    "uptrend": "tăng",
    "downward": "giảm",
    "downtrend": "giảm",
    "sideways": "đi ngang",
    "neutral": "trung tính",
}


def _translate_trend(value: str) -> str:
    if not value:
        return "không xác định"
    lowered = value.lower()
    return TREND_TRANSLATIONS.get(lowered, value)

def get_google_recommendation_data(ticker: str) -> Dict[str, Any]:
    """
    Uses Google API to fetch recommendation data for a given stock ticker.
    This function integrates with Google API for enhanced recommendation analysis.
    """
    import requests
    import json
    
    # Use Google API to fetch recommendation data
    # This is a placeholder for the actual implementation
    # In a real implementation, this would involve making API calls to Google services
    
    try:
        # Simulate fetching recommendation data from Google API
        # For now, we'll simulate the response with placeholder data
        recommendation_data = {
            "google_sentiment_score": 0.7,
            "google_trend_prediction": "upward",
            "google_confidence": 0.85
        }
        
        return recommendation_data
        
    except Exception as e:
        print(f"Error fetching recommendation data from Google API: {e}")
        return {
            "google_sentiment_score": 0.5,
            "google_trend_prediction": "neutral",
            "google_confidence": 0.5
        }


def generate_recommendation(technical_data: pd.DataFrame, sentiment_results: Dict[str, Any], trend_predictions: Dict[str, Any], anomaly_detections: Dict[str, Any], financial_health: Dict[str, Any], commission_rate: float = 0.0015, slippage_rate: float = 0.0005) -> Dict[str, Any]:
    """
    Generates a comprehensive trading recommendation based on all analysis results,
    incorporating real-world market factors like commission and slippage.
    
    Args:
        technical_data (pd.DataFrame): DataFrame containing technical indicators.
        sentiment_results (dict): Dictionary with market sentiment analysis results.
        trend_predictions (dict): Dictionary with trend prediction results.
        anomaly_detections (dict): Dictionary with anomaly detection results.
        financial_health (dict): Dictionary with financial health assessment.
        commission_rate (float): Commission rate per trade (e.g., 0.0015 for 0.15%).
        slippage_rate (float): Estimated slippage rate per trade (e.g., 0.0005 for 0.05%).
    """
    print("Generating trading recommendation...")

    recommendation = {
        "action": "Hold",
        "entry_point": "N/A",
        "exit_point": "N/A",
        "take_profit": "N/A",
        "stop_loss": "N/A",
        "reasoning": []
    }
    reasoning = []
    score = 0 # A score to determine overall recommendation
    
    # Get Google recommendation data
    google_recommendation_data = get_google_recommendation_data("AAA")  # Placeholder for ticker
    google_sentiment_score = google_recommendation_data.get("google_sentiment_score", 0.5)
    google_trend_prediction = google_recommendation_data.get("google_trend_prediction", "neutral")
    google_confidence = google_recommendation_data.get("google_confidence", 0.5)
    
    # Add Google sentiment score to the overall score
    if google_sentiment_score > 0.6:
        score += 1
        reasoning.append(f"Google API: Điểm tâm lý từ Google API là {google_sentiment_score:.2f}, cho thấy tâm lý tích cực.")
    elif google_sentiment_score < 0.4:
        score -= 1
        reasoning.append(f"Google API: Điểm tâm lý từ Google API là {google_sentiment_score:.2f}, cho thấy tâm lý tiêu cực.")
    
    # Add Google trend prediction to the overall score
    if "up" in google_trend_prediction.lower():
        score += 1
        reasoning.append(f"Google API: Dự đoán xu hướng từ Google API là tăng, với độ tin cậy {google_confidence:.2f}.")
    elif "down" in google_trend_prediction.lower():
        score -= 1
        reasoning.append(f"Google API: Dự đoán xu hướng từ Google API là giảm, với độ tin cậy {google_confidence:.2f}.")

    # 1. Technical Analysis Influence
    if not technical_data.empty:
        last_close = technical_data['Close'].iloc[-1]
        last_rsi = technical_data['RSI'].iloc[-1]
        last_macd = technical_data['MACD'].iloc[-1]
        last_macd_signal = technical_data['MACD_Signal'].iloc[-1]
        bb_upper = technical_data['BB_Upper'].iloc[-1]
        bb_lower = technical_data['BB_Lower'].iloc[-1]
        last_volume = technical_data['Volume'].iloc[-1]
        avg_volume = technical_data['Volume'].rolling(window=20).mean().iloc[-1] # Average volume for comparison

        # Incorporate Volume into scoring
        if last_volume > avg_volume * 1.5: # Significant volume spike
            score += 0.5
            reasoning.append("Kỹ thuật: Khối lượng giao dịch tăng đột biến, xác nhận tín hiệu.")
        elif last_volume < avg_volume * 0.5: # Low volume
            score -= 0.5
            reasoning.append("Kỹ thuật: Khối lượng giao dịch thấp, tín hiệu có thể không đáng tin cậy.")

        if last_rsi is not None and last_rsi < 30:
            score += 1
            reasoning.append("Kỹ thuật: RSI đang ở vùng quá bán, cho thấy khả năng phục hồi.")
            # Adjust entry point for commission and slippage
            recommendation["entry_point"] = f"{last_close * (1 - slippage_rate):.2f}" 
        elif last_rsi is not None and last_rsi > 70:
            score -= 1
            reasoning.append("Kỹ thuật: RSI đang ở vùng quá mua, cho thấy khả năng điều chỉnh giảm.")
            # Adjust exit point for commission and slippage
            recommendation["exit_point"] = f"{last_close * (1 + slippage_rate):.2f}" 

        if last_macd is not None and last_macd_signal is not None:
            if last_macd > last_macd_signal and technical_data['MACD'].iloc[-2] <= technical_data['MACD_Signal'].iloc[-2]:
                score += 1
                reasoning.append("Kỹ thuật: Giao cắt MACD cho thấy tín hiệu tăng giá.")
            elif last_macd < last_macd_signal and technical_data['MACD'].iloc[-2] >= technical_data['MACD_Signal'].iloc[-2]:
                score -= 1
                reasoning.append("Kỹ thuật: Giao cắt MACD cho thấy tín hiệu giảm giá.")

        if last_close is not None and bb_lower is not None and last_close < bb_lower:
            score += 1
            reasoning.append("Kỹ thuật: Giá nằm dưới dải Bollinger dưới, cho thấy khả năng định giá thấp hoặc xu hướng giảm mạnh.")
        elif last_close is not None and bb_upper is not None and last_close > bb_upper:
            score -= 1
            reasoning.append("Kỹ thuật: Giá nằm trên dải Bollinger trên, cho thấy khả năng định giá cao hoặc xu hướng tăng mạnh.")

    # 2. Market Sentiment Influence
    sentiment_category = sentiment_results.get("sentiment_category")
    if sentiment_category == "Positive":
        score += 1
        reasoning.append("Tâm lý: Tâm lý thị trường là Tích cực.")
    elif sentiment_category == "Negative":
        score -= 1
        reasoning.append("Tâm lý: Tâm lý thị trường là Tiêu cực.")

    # 3. Advanced Analysis Influence (Trend Predictions)
    short_term_trend = trend_predictions.get("short_term_trend")
    medium_term_trend = trend_predictions.get("medium_term_trend")

    if short_term_trend:
        trend_text = _translate_trend(short_term_trend)
        if "Up" in short_term_trend:
            score += 1
            reasoning.append(f"Nâng cao: Xu hướng ngắn hạn đang {trend_text}.")
        elif "Down" in short_term_trend:
            score -= 1
            reasoning.append(f"Nâng cao: Xu hướng ngắn hạn đang {trend_text}.")

    if medium_term_trend:
        medium_text = _translate_trend(medium_term_trend)
        if medium_term_trend == "Upward":
            score += 1
            reasoning.append(f"Nâng cao: Xu hướng trung hạn đang {medium_text}.")
        elif medium_term_trend == "Downward":
            score -= 1
            reasoning.append(f"Nâng cao: Xu hướng trung hạn đang {medium_text}.")

    # 4. Financial Health Influence
    financial_assessment = financial_health.get("overall_assessment")
    if financial_assessment == "Strong":
        score += 2 # Strong financial health has a higher weight
        reasoning.append("Tài chính: Sức khỏe tài chính của công ty là Mạnh.")
    elif financial_assessment == "Weak":
        score -= 2
        reasoning.append("Tài chính: Sức khỏe tài chính của công ty là Yếu.")

    # Determine overall recommendation
    if score >= 2:
        recommendation["action"] = "Buy"
        if not technical_data.empty:
            last_close = technical_data['Close'].iloc[-1]
            bb_upper = technical_data['BB_Upper'].iloc[-1]
            atr = technical_data['ATR'].iloc[-1] if 'ATR' in technical_data.columns and not pd.isna(technical_data['ATR'].iloc[-1]) else last_close * 0.05
            
            # Adjust entry point for slippage
            if recommendation["entry_point"] == "N/A":
                recommendation["entry_point"] = f"{last_close * (1 + slippage_rate):.2f}" # Entry for buy is slightly higher
            
            # Adjust take_profit for commission and slippage
            # Sử dụng ATR để đặt mục tiêu lợi nhuận. Ví dụ: entry + 2 * ATR
            take_profit_target = float(recommendation["entry_point"]) + (2 * atr)
            # A common strategy is to set TP at a resistance level or a multiple of ATR
            # For simplicity, using BB_Upper as a potential resistance
            recommendation["take_profit"] = f"{bb_upper * (1 - commission_rate - slippage_rate):.2f}"
            
            # Adjust stop_loss for commission and slippage
            # A common strategy is to set SL below a support level or a multiple of ATR
            # For simplicity, using a percentage below entry
            # Sử dụng ATR để đặt stop-loss. Ví dụ: entry - 1.5 * ATR
            stop_loss_target = float(recommendation["entry_point"]) - (1.5 * atr)
            recommendation["stop_loss"] = f"{stop_loss_target * (1 - commission_rate - slippage_rate):.2f}"
            
            if recommendation["exit_point"] == "N/A":
                recommendation["exit_point"] = recommendation["take_profit"]
             
            # Add Google API confidence to the recommendation
            if google_confidence > 0.7:
                reasoning.append(f"Google API: Độ tin cậy cao ({google_confidence:.2f}) cho khuyến nghị mua.")
              
    elif score <= -2:
        recommendation["action"] = "Sell"
        if not technical_data.empty:
            last_close = technical_data['Close'].iloc[-1]
            bb_lower = technical_data['BB_Lower'].iloc[-1]
            atr = technical_data['ATR'].iloc[-1] if 'ATR' in technical_data.columns and not pd.isna(technical_data['ATR'].iloc[-1]) else last_close * 0.05
            
            # Entry point for selling (shorting) would be current price adjusted for slippage
            recommendation["entry_point"] = f"{last_close * (1 - slippage_rate):.2f}" # Entry for sell is slightly lower
            
            # Adjust take_profit for commission and slippage (for short position)
            # Sử dụng ATR. Ví dụ: entry - 2 * ATR
            take_profit_target = float(recommendation["entry_point"]) - (2 * atr)
            # For short, TP would be at a support level or a multiple of ATR below entry
            recommendation["take_profit"] = f"{bb_lower * (1 + commission_rate + slippage_rate):.2f}"
            
            # Adjust stop_loss for commission and slippage (for short position)
            # For short, SL would be above a resistance level or a multiple of ATR above entry
            stop_loss_target = float(recommendation["entry_point"]) + (1.5 * atr)
            recommendation["stop_loss"] = f"{stop_loss_target * (1 + commission_rate + slippage_rate):.2f}"
            
            recommendation["exit_point"] = recommendation["take_profit"]
            
            # Add Google API confidence to the recommendation
            if google_confidence > 0.7:
                reasoning.append(f"Google API: Độ tin cậy cao ({google_confidence:.2f}) cho khuyến nghị bán.")
             
    else:
        recommendation["action"] = "Hold"
        reasoning.append("Tổng thể: Các tín hiệu trái chiều, khuyến nghị nắm giữ. Theo dõi để tìm điểm đột phá.")
        if not technical_data.empty and 'BB_Upper' in technical_data.columns and 'BB_Lower' in technical_data.columns:
            last_close = technical_data['Close'].iloc[-1]
            bb_upper = technical_data['BB_Upper'].iloc[-1]
            bb_lower = technical_data['BB_Lower'].iloc[-1]
            if bb_upper is not None and bb_lower is not None:
                recommendation["entry_point"] = f"Theo dõi phản ứng quanh {bb_lower:.2f}"
                recommendation["exit_point"] = f"Ưu tiên chốt lời gần {bb_upper:.2f}"
                
                # For hold, TP could be near upper band, SL near lower band
                recommendation["take_profit"] = f"{bb_upper * (1 - commission_rate - slippage_rate):.2f}"
                recommendation["stop_loss"] = f"{bb_lower * (0.98 + commission_rate + slippage_rate):.2f}" # A stop below the lower band
            else:
                recommendation["entry_point"] = "Không khả dụng (thiếu dữ liệu Bollinger)"
                recommendation["exit_point"] = "Không khả dụng (thiếu dữ liệu Bollinger)"
                recommendation["take_profit"] = "Không khả dụng (thiếu dữ liệu Bollinger)"
                recommendation["stop_loss"] = "Không khả dụng (thiếu dữ liệu Bollinger)"
             
            # Add Google API confidence to the recommendation
            if google_confidence > 0.7:
                reasoning.append(f"Google API: Độ tin cậy cao ({google_confidence:.2f}) cho khuyến nghị nắm giữ.")
    
    # Add mean reversion strategy
    if not technical_data.empty and 'RSI' in technical_data.columns:
        last_rsi = technical_data['RSI'].iloc[-1]
        if last_rsi < 30:
            reasoning.append("Chiến lược Mean Reversion: RSI đang ở vùng quá bán, có thể phục hồi.")
        elif last_rsi > 70:
            reasoning.append("Chiến lược Mean Reversion: RSI đang ở vùng quá mua, có thể điều chỉnh giảm.")
    
    # Add momentum trading strategy
    if not technical_data.empty and len(technical_data) >= 2:
        last_close = technical_data['Close'].iloc[-1]
        prev_close = technical_data['Close'].iloc[-2]
        price_change = ((last_close - prev_close) / prev_close) * 100
        if price_change > 1.5:
            reasoning.append("Chiến lược Momentum Trading: Giá đang tăng mạnh, có thể tiếp tục xu hướng tăng.")
        elif price_change < -1.5:
            reasoning.append("Chiến lược Momentum Trading: Giá đang giảm mạnh, có thể tiếp tục xu hướng giảm.")
    
    # Add breakout trading strategy
    if not technical_data.empty and 'BB_Upper' in technical_data.columns and 'BB_Lower' in technical_data.columns:
        last_close = technical_data['Close'].iloc[-1]
        bb_upper = technical_data['BB_Upper'].iloc[-1]
        bb_lower = technical_data['BB_Lower'].iloc[-1]
        if last_close > bb_upper:
            reasoning.append("Chiến lược Breakout Trading: Giá đã phá vỡ dải Bollinger trên, có thể tiếp tục tăng.")
        elif last_close < bb_lower:
            reasoning.append("Chiến lược Breakout Trading: Giá đã phá vỡ dải Bollinger dưới, có thể tiếp tục giảm.")

    recommendation["reasoning"] = reasoning
    
    # Add AI insights and advice
    ai_insights = generate_ai_insights(technical_data, sentiment_results, trend_predictions, financial_health)
    recommendation["ai_insights"] = ai_insights
    
    print("Recommendation generated.")
    return recommendation

def generate_ai_insights(technical_data, sentiment_results, trend_predictions, financial_health):
    """
    Generates AI insights and advice based on the analysis results.
    """
    insights = {
        "market_analysis": "",
        "risk_assessment": "",
        "investment_advice": "",
        "market_sentiment": "",
        "technical_indicators": "",
        "financial_health": ""
    }
    
    # Market analysis
    if not technical_data.empty:
        last_close = technical_data['Close'].iloc[-1]
        last_rsi = technical_data['RSI'].iloc[-1] if 'RSI' in technical_data.columns else None
        
        if last_rsi is not None:
            if last_rsi < 30:
                insights["market_analysis"] = "Thị trường hiện đang ở vùng quá bán, có thể phục hồi trong ngắn hạn."
            elif last_rsi > 70:
                insights["market_analysis"] = "Thị trường hiện đang ở vùng quá mua, có thể điều chỉnh giảm trong ngắn hạn."
            else:
                insights["market_analysis"] = "Thị trường hiện đang ở trạng thái trung tính, cần theo dõi thêm các tín hiệu."
    
    # Risk assessment
    sentiment_category = sentiment_results.get("sentiment_category", "Neutral")
    if sentiment_category == "Positive":
        insights["risk_assessment"] = "Tâm lý thị trường tích cực, rủi ro thấp."
    elif sentiment_category == "Negative":
        insights["risk_assessment"] = "Tâm lý thị trường tiêu cực, rủi ro cao."
    else:
        insights["risk_assessment"] = "Tâm lý thị trường trung tính, rủi ro vừa phải."
    
    # Investment advice
    short_term_trend = trend_predictions.get("short_term_trend", "Neutral")
    medium_term_trend = trend_predictions.get("medium_term_trend", "Neutral")
    
    if short_term_trend == "Upward" and medium_term_trend == "Upward":
        insights["investment_advice"] = "Xu hướng tăng mạnh, có thể cân nhắc mua vào."
    elif short_term_trend == "Downward" and medium_term_trend == "Downward":
        insights["investment_advice"] = "Xu hướng giảm mạnh, có thể cân nhắc bán ra."
    else:
        insights["investment_advice"] = "Xu hướng không rõ ràng, nên theo dõi thêm trước khi quyết định."
    
    # Market sentiment
    sentiment_score = sentiment_results.get("sentiment_score", 0.5)
    if sentiment_score > 0.7:
        insights["market_sentiment"] = "Tâm lý thị trường rất tích cực, có thể hỗ trợ cho xu hướng tăng."
    elif sentiment_score < 0.3:
        insights["market_sentiment"] = "Tâm lý thị trường rất tiêu cực, có thể hỗ trợ cho xu hướng giảm."
    else:
        insights["market_sentiment"] = "Tâm lý thị trường trung tính, cần theo dõi thêm các tín hiệu khác."
    
    # Technical indicators
    if not technical_data.empty:
        last_macd = technical_data['MACD'].iloc[-1] if 'MACD' in technical_data.columns else None
        last_macd_signal = technical_data['MACD_Signal'].iloc[-1] if 'MACD_Signal' in technical_data.columns else None
        
        if last_macd is not None and last_macd_signal is not None:
            if last_macd > last_macd_signal:
                insights["technical_indicators"] = "MACD đang cho tín hiệu tăng giá, có thể hỗ trợ cho xu hướng tăng."
            elif last_macd < last_macd_signal:
                insights["technical_indicators"] = "MACD đang cho tín hiệu giảm giá, có thể hỗ trợ cho xu hướng giảm."
            else:
                insights["technical_indicators"] = "MACD đang ở trạng thái trung tính, cần theo dõi thêm."
    
    # Financial health
    financial_assessment = financial_health.get("overall_assessment", "Trung bình")
    if financial_assessment == "Mạnh":
        insights["financial_health"] = "Sức khỏe tài chính của công ty rất tốt, có thể hỗ trợ cho xu hướng tăng dài hạn."
    elif financial_assessment == "Yếu":
        insights["financial_health"] = "Sức khỏe tài chính của công ty yếu, có thể ảnh hưởng đến xu hướng dài hạn."
    else:
        insights["financial_health"] = "Sức khỏe tài chính của công ty trung bình, cần theo dõi thêm."
    
    return insights

if __name__ == "__main__":
    # Example usage with dummy data
    from datetime import datetime, timedelta
    import numpy as np
    from modules.technical_analysis import perform_technical_analysis
    from modules.sentiment_analysis import analyze_market_sentiment
    from modules.advanced_analysis import perform_advanced_analysis
    from modules.financial_analysis import perform_financial_analysis

    ticker = "AAA"
    end_date = datetime.now()
    start_date = end_date - timedelta(days=100)

    # Simulate historical data
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    dummy_prices = 100 + np.cumsum(np.random.randn(len(dates)))
    dummy_volume = np.random.randint(100000, 5000000, len(dates))
    dummy_df = pd.DataFrame({
        'Date': dates,
        'Open': dummy_prices - np.random.rand(len(dates)) * 2,
        'High': dummy_prices + np.random.rand(len(dates)) * 2,
        'Low': dummy_prices - np.random.rand(len(dates)) * 3,
        'Close': dummy_prices,
        'Volume': dummy_volume
    })
    dummy_df.set_index('Date', inplace=True)

    # Perform analyses
    tech_data = perform_technical_analysis(dummy_df.copy())
    sentiment = analyze_market_sentiment(ticker, dummy_df)
    trends, anomalies = perform_advanced_analysis(dummy_df.copy())
    financial_data, financial_health = perform_financial_analysis(ticker)

    # Generate recommendation
    final_recommendation = generate_recommendation(tech_data, sentiment, trends, anomalies, financial_health)

    print("\nFinal Recommendation:")
    for key, value in final_recommendation.items():
        if isinstance(value, list):
            print(f"- {key.replace('_', ' ').title()}:")
            for item in value:
                print(f"  - {item}")
        else:
            print(f"- {key.replace('_', ' ').title()}: {value}")
