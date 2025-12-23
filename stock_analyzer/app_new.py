import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import sys
import json
import plotly.graph_objects as go
from typing import Dict, List, Optional, Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from stock_analyzer.modules.core_analysis import run_analysis
from stock_analyzer.modules.investment_scanner import find_investment_opportunities
from stock_analyzer.modules.derivatives_utils import get_derivative_expiry_overview
from stock_analyzer.modules.smart_money_detector import detect_smart_money_activity

from stock_analyzer.ui_styling import apply_modern_styling, create_modern_header, create_modern_card, create_theme_toggle
from stock_analyzer.ui_components import create_modern_metric_container, create_smart_summary_card, create_progress_indicator, create_loading_skeleton

STOCK_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'stocks.csv')
SMART_MONEY_SEVERITY_OPTIONS = ["Cảnh báo sớm", "Mạnh", "Cực mạnh"]
SMART_MONEY_SIGNAL_TYPES = ["Breakout xác nhận", "Tích lũy mạnh", "Cảnh báo sớm"]
DEFAULT_DERIVATIVE_SETTINGS = {
    "months_ahead": 4,
    "reminder_window_days": 10,
    "show_all": False,
}
DEFAULT_SMART_MONEY_FILTERS = {
    "min_volume_ratio": 1.8,
    "min_price_change_pct": 1.0,
    "lookback_days": 60,
    "min_confidence": 60,
    "severity_filter": SMART_MONEY_SEVERITY_OPTIONS,
    "signal_types": SMART_MONEY_SIGNAL_TYPES[:-1],  # ưu tiên breakout & tích lũy
    "max_rsi": 80,
}
TREND_TRANSLATIONS = {
    "upward": "Tăng",
    "uptrend": "Tăng",
    "downward": "Giảm",
    "downtrend": "Giảm",
    "sideways": "Đi ngang",
    "neutral": "Trung tính",
    "n/a": "Không xác định",
}
SENTIMENT_TRANSLATIONS = {
    "positive": "Tích cực",
    "negative": "Tiêu cực",
    "neutral": "Trung tính",
    "n/a": "Không xác định",
}
ACTION_TRANSLATIONS = {
    "buy": "Mua",
    "sell": "Bán",
    "hold": "Nắm giữ",
}
NO_DATA_TEXT = "Không có dữ liệu"


def _translate_from_mapping(value: Optional[str], mapping: Dict[str, str], default: str = "Không xác định") -> str:
    if value is None:
        return default
    normalized = value.strip()
    if not normalized:
        return default
    lowered = normalized.lower()
    if lowered in mapping:
        return mapping[lowered]
    return default if normalized.upper() in {"N/A", "NA"} else normalized


def _translate_trend_label(value: Optional[str]) -> str:
    return _translate_from_mapping(value, TREND_TRANSLATIONS)


def _translate_sentiment_label(value: Optional[str]) -> str:
    return _translate_from_mapping(value, SENTIMENT_TRANSLATIONS)


def _translate_action_label(value: Optional[str]) -> str:
    return _translate_from_mapping(value, ACTION_TRANSLATIONS, default="Không xác định")


def _get_sentiment_icon(value: Optional[str]) -> str:
    lowered = (value or "").lower()
    if lowered == "positive":
        return "🟢"
    if lowered == "negative":
        return "🔴"
    if lowered == "neutral":
        return "⚪"
    return "⚪"


def _export_analysis_to_csv(ticker: str, results: Dict[str, Any]) -> bytes:
    """Exports analysis results to CSV format."""
    output = f"Báo cáo Phân tích Cổ phiếu: {ticker}\n"
    output += f"Ngày xuất: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    output += "="*80 + "\n\n"

    output += "1. PHÂN TÍCH KỸ THUẬT\n"
    output += "-"*80 + "\n"
    tech_data = results.get("technical_data")
    if tech_data is not None and not tech_data.empty:
        output += tech_data.tail(10).to_csv()
    output += "\n\n"

    output += "2. PHÂN TÍCH TÂM LÝ THỊ TRƯỜNG\n"
    output += "-"*80 + "\n"
    sentiment = results.get("sentiment_results", {})
    for key, value in sentiment.items():
        output += f"{key}: {value}\n"
    output += "\n\n"

    output += "3. DỰ ĐOÁN XU HƯỚNG\n"
    output += "-"*80 + "\n"
    trends = results.get("trend_predictions", {})
    for key, value in trends.items():
        output += f"{key}: {value}\n"
    output += "\n\n"

    output += "4. PHÂN TÍCH TÀI CHÍNH\n"
    output += "-"*80 + "\n"
    financial = results.get("financial_data", {})
    for key, value in financial.items():
        output += f"{key}: {value}\n"
    output += "\n\n"

    output += "5. KHUYẾN NGHỊ GIAO DỊch\n"
    output += "-"*80 + "\n"
    rec = results.get("final_recommendation", {})
    for key, value in rec.items():
        if isinstance(value, list):
            output += f"{key}:\n"
            for item in value:
                output += f"  - {item}\n"
        else:
            output += f"{key}: {value}\n"

    return output.encode('utf-8-sig')


@st.cache_data
def load_stock_list(file_path: str) -> List[str]:
    """Loads the list of valid stock tickers from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        return df['Ticker'].tolist()
    except FileNotFoundError:
        st.error(f"Lỗi: Tệp dữ liệu cổ phiếu không tìm thấy tại {file_path}")
        return []
    except Exception as e:
        st.error(f"Lỗi khi tải dữ liệu: {e}")
        return []


def _create_price_chart(tech_data: pd.DataFrame) -> go.Figure:
    """Creates an interactive price chart with Bollinger Bands."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=tech_data.index, y=tech_data['Close'],
        mode='lines', name='Giá đóng cửa',
        line=dict(color='#1f77d2', width=2)
    ))

    if 'BB_Upper' in tech_data.columns and 'BB_Lower' in tech_data.columns:
        fig.add_trace(go.Scatter(
            x=tech_data.index, y=tech_data['BB_Upper'],
            mode='lines', name='Dải BB Trên',
            line=dict(color='rgba(255, 0, 0, 0.3)', dash='dash')
        ))
        fig.add_trace(go.Scatter(
            x=tech_data.index, y=tech_data['BB_Lower'],
            mode='lines', name='Dải BB Dưới',
            line=dict(color='rgba(255, 0, 0, 0.3)', dash='dash'),
            fill='tonexty', fillcolor='rgba(255, 0, 0, 0.1)'
        ))

    fig.update_layout(
        title='Biểu đồ Giá Cổ Phiếu & Dải Bollinger',
        xaxis_title='Ngày',
        yaxis_title='Giá (VNĐ)',
        hovermode='x unified',
        template='plotly_white',
        height=500
    )
    return fig


def _create_rsi_chart(tech_data: pd.DataFrame) -> go.Figure:
    """Creates an interactive RSI chart."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=tech_data.index, y=tech_data['RSI'],
        mode='lines', name='RSI',
        line=dict(color='#ff7f0e', width=2)
    ))

    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Quá mua (70)")
    fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Quá bán (30)")
    fig.add_hrect(y0=0, y1=30, fillcolor="green", opacity=0.1, layer="below")
    fig.add_hrect(y0=70, y1=100, fillcolor="red", opacity=0.1, layer="below")

    fig.update_layout(
        title='Chỉ số RSI (Relative Strength Index)',
        xaxis_title='Ngày',
        yaxis_title='RSI',
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    return fig


def _create_macd_chart(tech_data: pd.DataFrame) -> go.Figure:
    """Creates an interactive MACD chart."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=tech_data.index, y=tech_data['MACD'],
        mode='lines', name='MACD',
        line=dict(color='#1f77d2', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=tech_data.index, y=tech_data['MACD_Signal'],
        mode='lines', name='Signal Line',
        line=dict(color='#ff7f0e', width=2)
    ))

    colors = ['green' if val >= 0 else 'red' for val in tech_data['MACD_Hist']]
    fig.add_trace(go.Bar(
        x=tech_data.index, y=tech_data['MACD_Hist'],
        name='Histogram', marker_color=colors, opacity=0.3
    ))

    fig.update_layout(
        title='MACD (Moving Average Convergence Divergence)',
        xaxis_title='Ngày',
        yaxis_title='Giá trị MACD',
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    return fig


def _display_technical_analysis(results: Dict[str, Any]) -> None:
    st.header("1. Tóm tắt Phân tích Kỹ thuật")
    tech_data = results["technical_data"]
    if not tech_data.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(_create_price_chart(tech_data), width='stretch')
        with col2:
            st.plotly_chart(_create_rsi_chart(tech_data), width='stretch')

        st.plotly_chart(_create_macd_chart(tech_data), width='stretch')

        st.subheader("📊 Dữ liệu Kỹ thuật Chi tiết")
        cols_to_display = ['Close', 'RSI', 'MACD', 'MACD_Signal', 'BB_Upper', 'BB_Middle', 'BB_Lower', 'OBV', 'AD_Line', 'ATR']
        cols_available = [col for col in cols_to_display if col in tech_data.columns]
        st.dataframe(tech_data[cols_available].tail(10), width='stretch')
    else:
        st.info("❌ Không có dữ liệu kỹ thuật.")


def _display_sentiment_analysis(results: Dict[str, Any]) -> None:
    st.header("2. Tóm tắt Phân tích Tâm lý Thị trường")
    sentiment_results = results["sentiment_results"]

    col1, col2, col3 = st.columns(3)
    with col1:
        sentiment_score = sentiment_results.get('sentiment_score', 0.0)
        st.metric(label="📊 Điểm Tâm lý", value=f"{sentiment_score:.2f}")
    with col2:
        sentiment_label = _translate_sentiment_label(sentiment_results.get('sentiment_category'))
        st.metric(label="📈 Trạng thái", value=sentiment_label)
    with col3:
        st.metric(label="📰 Tác động Tin tức", value=sentiment_results.get('news_impact', NO_DATA_TEXT))

    st.info(f"**Mức độ Lan truyền Mạng xã hội:** {sentiment_results.get('social_media_buzz', NO_DATA_TEXT)}")


def _display_advanced_predictions(results: Dict[str, Any]) -> None:
    st.header("3. Tóm tắt Phân tích Nâng cao & Dự đoán Xu hướng")
    trend_predictions = results["trend_predictions"]
    anomaly_detections_zscore = results.get('anomaly_detections_zscore', {})
    anomaly_detections_isolation = results.get('anomaly_detections_isolation', {})
    anomaly_detections_dbscan = results.get('anomaly_detections_dbscan', {})

    st.subheader("📈 Dự đoán Xu hướng")
    col_trend1, col_trend2 = st.columns(2)
    short_term_trend = trend_predictions.get('short_term_trend')
    medium_term_trend = trend_predictions.get('medium_term_trend')

    short_conf_display = trend_predictions.get('short_term_confidence', NO_DATA_TEXT)
    medium_conf_display = trend_predictions.get('medium_term_confidence', NO_DATA_TEXT)

    with col_trend1:
        st.metric(label="🔵 Xu hướng ngắn hạn",
                  value=_translate_trend_label(short_term_trend),
                  delta=f"Độ tin cậy: {short_conf_display}")
    with col_trend2:
        st.metric(label="🟢 Xu hướng trung hạn",
                  value=_translate_trend_label(medium_term_trend),
                  delta=f"Độ tin cậy: {medium_conf_display}")

    st.info(f"**📊 Dự báo giá (5 ngày tới):** {trend_predictions['price_forecast_next_5_days']}")

    st.subheader("⚠️ Phát hiện Bất thường")
    anomaly_detections_zscore = results.get('anomaly_detections_zscore', {})
    anomaly_detections_isolation = results.get('anomaly_detections_isolation', {})
    anomaly_detections_dbscan = results.get('anomaly_detections_dbscan', {})

    if anomaly_detections_zscore.get('anomalies_detected') == 'Yes':
        st.warning(f"**Phát hiện bất thường (Z-score):** {anomaly_detections_zscore['anomalies_detected']}")
        for anomaly in anomaly_detections_zscore['details']:
            st.write(f"  - 📅 Ngày: {anomaly['date']}, 🏷️ Loại: {anomaly['type']}")
    else:
        st.success("✅ Không phát hiện bất thường nào (Z-score).")

    if anomaly_detections_isolation.get('anomalies_detected') == 'Yes':
        st.warning(f"**Phát hiện bất thường (Isolation Forest):** {anomaly_detections_isolation['anomalies_detected']}")
        for anomaly in anomaly_detections_isolation['details']:
            st.write(f"  - 📅 Ngày: {anomaly['date']}, 🏷️ Loại: {anomaly['type']}")
    else:
        st.success("✅ Không phát hiện bất thường nào (Isolation Forest).")

    if anomaly_detections_dbscan.get('anomalies_detected') == 'Yes':
        st.warning(f"**Phát hiện bất thường (DBSCAN):** {anomaly_detections_dbscan['anomalies_detected']}")
        for anomaly in anomaly_detections_dbscan['details']:
            st.write(f"  - 📅 Ngày: {anomaly['date']}, 🏷️ Loại: {anomaly['type']}")
    else:
        st.success("✅ Không phát hiện bất thường nào (DBSCAN).")


def _display_financial_analysis(results: Dict[str, Any]) -> None:
    st.header("4. Tóm tắt Phân tích Báo cáo Tài chính")
    financial_data = results["financial_data"]
    financial_health = results["financial_health"]

    st.subheader("💰 Đánh giá Sức khỏe Tài chính Tổng thể")
    assessment = financial_health['overall_assessment']
    if "Strong" in assessment or "Mạnh" in assessment:
        st.success(f"**{assessment}** ✅")
    elif "Weak" in assessment or "Yếu" in assessment:
        st.error(f"**{assessment}** ⚠️")
    else:
        st.info(f"**{assessment}** ℹ️")

    st.subheader("📊 Các Tỷ lệ Tài chính Chính")
    financial_ratios_display = {}
    for key, value in financial_data.items():
        if value is None:
            financial_ratios_display[key] = NO_DATA_TEXT
        elif isinstance(value, (int, float)):
            financial_ratios_display[key] = f"{value:.2f}"
        else:
            financial_ratios_display[key] = value

    st.dataframe(
        pd.DataFrame.from_dict(financial_ratios_display, orient='index', columns=['Giá trị']),
        width='stretch'
    )

    st.subheader("📝 Bình luận về Sức khỏe Tài chính")
    if financial_health['comments']:
        for comment in financial_health['comments']:
            st.write(f"  • {comment}")
    else:
        st.info("ℹ️ Không có bình luận nào về sức khỏe tài chính.")


def _display_trade_recommendations(results: Dict[str, Any]) -> None:
    st.header("🎯 Khuyến nghị Giao dịch")
    final_recommendation = results["final_recommendation"]

    action = final_recommendation['action']
    action_label = _translate_action_label(action)
    action_color = "green" if action == "Buy" else "red" if action == "Sell" else "gray"
    action_emoji = "🟢" if action == "Buy" else "🔴" if action == "Sell" else "⚪"

    rec_col1, rec_col2, rec_col3 = st.columns(3)
    with rec_col1:
        st.metric(label=f"💡 Hành động {action_emoji}", value=action_label)
    with rec_col2:
        st.metric(label="📍 Điểm vào", value=final_recommendation['entry_point'])
    with rec_col3:
        st.metric(label="📍 Điểm ra", value=final_recommendation['exit_point'])

    st.markdown("---")

    tp_sl_col1, tp_sl_col2 = st.columns(2)
    with tp_sl_col1:
        st.metric(label="📈 Take-Profit", value=final_recommendation['take_profit'])
    with tp_sl_col2:
        st.metric(label="📉 Stop-Loss", value=final_recommendation['stop_loss'])

    st.subheader("💬 Lý do:")
    for i, reason in enumerate(final_recommendation['reasoning'], 1):
        st.write(f"{i}. {reason}")


def _display_backtesting_results(results: Dict[str, Any]) -> None:
    st.header("📊 Kiểm tra lại Chiến lược (Backtesting)")
    st.markdown("""
    Phần này hiển thị kết quả của việc kiểm tra lại một chiến lược giao dịch đơn giản dựa trên chỉ báo RSI trên dữ liệu lịch sử của cổ phiếu.
    - **📌 Chiến lược**: Mua khi RSI < 30, Bán khi RSI > 70.
    - **💰 Vốn ban đầu**: 100,000.
    - **⚙️ Phí giao dịch và trượt giá** được áp dụng theo cấu hình ở thanh bên.
    """)

    backtest_metrics = results.get("backtest_metrics")
    backtest_plot = results.get("backtest_plot")

    if backtest_plot:
        st.pyplot(backtest_plot)

    if backtest_metrics:
        st.subheader("📈 Các chỉ số Hiệu suất")
        col1, col2, col3, col4 = st.columns(4)
        metrics_dict = backtest_metrics if isinstance(backtest_metrics, dict) else json.loads(backtest_metrics)

        for i, (key, value) in enumerate(metrics_dict.items()):
            metric_cols = [col1, col2, col3, col4]
            with metric_cols[i % 4]:
                st.metric(label=key.replace('_', ' ').title(), value=f"{value}")
    else:
        st.info("⚠️ Không có dữ liệu backtesting")


def _generate_intelligent_summary(results: Dict[str, Any]) -> Dict[str, Any]:
    summary = {
        "score": 50.0,
        "insights": [],
        "risks": [],
        "key_signals": [],
        "system_hint": "Theo dõi thêm",
        "status": "Cân bằng",
        "latest_smart_money": None,
    }

    tech_data = results.get("technical_data")
    sentiment_results = results.get("sentiment_results", {})
    trend_predictions = results.get("trend_predictions", {})
    financial_health = results.get("financial_health", {})
    anomaly_detections = results.get("anomaly_detections", {})
    final_recommendation = results.get("final_recommendation", {})

    rsi_value = None
    if tech_data is not None and not tech_data.empty:
        if 'RSI' in tech_data.columns:
            rsi_value = float(tech_data['RSI'].iloc[-1])
            if rsi_value < 35:
                summary["insights"].append("RSI đang nằm vùng hỗ trợ, lực mua có thể quay lại.")
                summary["score"] += 8
            elif rsi_value > 70:
                summary["risks"].append("RSI vượt vùng quá mua, cần cảnh giác áp lực chốt lời.")
                summary["score"] -= 12
        if len(tech_data) >= 2:
            prev_close = tech_data['Close'].iloc[-2]
            if prev_close:
                price_change = ((tech_data['Close'].iloc[-1] - prev_close) / prev_close) * 100
                if price_change >= 1.5:
                    summary["insights"].append(f"Giá bật {price_change:.2f}% phiên gần nhất, dòng tiền đang đẩy giá.")
                    summary["score"] += 6
                elif price_change <= -1.5:
                    summary["risks"].append(f"Giá giảm {price_change:.2f}% phiên gần nhất, chú ý lực bán.")
                    summary["score"] -= 6

        smart_money_snapshot = detect_smart_money_activity(
            tech_data,
            min_volume_ratio=DEFAULT_SMART_MONEY_FILTERS["min_volume_ratio"],
            min_price_change_pct=DEFAULT_SMART_MONEY_FILTERS["min_price_change_pct"],
            lookback_days=DEFAULT_SMART_MONEY_FILTERS["lookback_days"],
        )
        if smart_money_snapshot["signals"]:
            latest_signal = smart_money_snapshot["signals"][0]
            summary["latest_smart_money"] = latest_signal
            if latest_signal["severity"] in {"Mạnh", "Cực mạnh"}:
                summary["insights"].append(
                    f"Tín hiệu tay to ngày {latest_signal['date']} ({latest_signal['severity']})."
                )
                summary["score"] += 5
            else:
                summary["risks"].append(
                    f"Tay to cảnh báo sớm xuất hiện ngày {latest_signal['date']}."
                )

    sentiment_category = sentiment_results.get("sentiment_category")
    sentiment_label = _translate_sentiment_label(sentiment_category)
    if sentiment_category == "Positive":
        summary["insights"].append("Tâm lý thị trường đang nghiêng về phía mua.")
        summary["score"] += 6
    elif sentiment_category == "Negative":
        summary["risks"].append("Tâm lý thị trường tiêu cực, cần bảo vệ thành quả.")
        summary["score"] -= 6

    short_term_trend = trend_predictions.get("short_term_trend")
    medium_term_trend = trend_predictions.get("medium_term_trend")
    if short_term_trend:
        if short_term_trend.lower().startswith("up"):
            summary["insights"].append("Xu hướng ngắn hạn hỗ trợ vị thế mua.")
            summary["score"] += 10
        elif short_term_trend.lower().startswith("down"):
            summary["risks"].append("Xu hướng ngắn hạn cho tín hiệu giảm.")
            summary["score"] -= 10
    if medium_term_trend:
        if medium_term_trend.lower().startswith("up"):
            summary["score"] += 5
        elif medium_term_trend.lower().startswith("down"):
            summary["risks"].append("Xu hướng trung hạn suy yếu.")
            summary["score"] -= 7

    assessment = financial_health.get("overall_assessment")
    if assessment:
        if "Mạnh" in assessment:
            summary["insights"].append("Nền tảng tài chính vững vàng.")
            summary["score"] += 10
        elif "Yếu" in assessment:
            summary["risks"].append("Sức khỏe tài chính yếu, hạn chế tỷ trọng.")
            summary["score"] -= 12

    if anomaly_detections.get("anomalies_detected") == "Yes":
        details = anomaly_detections.get("details", [])
        if details:
            summary["risks"].append(f"Phát hiện bất thường ngày {details[0]['date']}: {details[0]['type']}.")
        summary["score"] -= 8

    action = final_recommendation.get("action")
    action_label = _translate_action_label(action)
    if action == "Buy":
        summary["system_hint"] = "Ưu tiên tích lũy"
        summary["score"] += 5
    elif action == "Sell":
        summary["system_hint"] = "Cân nhắc hạ tỷ trọng"
        summary["score"] -= 5
    else:
        summary["system_hint"] = "Tiếp tục quan sát"

    key_signals = []
    if rsi_value is not None:
        key_signals.append({"label": "RSI hiện tại", "value": f"{rsi_value:.1f}"})
    if short_term_trend:
        key_signals.append({"label": "Xu hướng ngắn hạn", "value": _translate_trend_label(short_term_trend)})
    key_signals.append({"label": "Tâm lý thị trường", "value": sentiment_label})

    forecast = trend_predictions.get("price_forecast_next_5_days", {})
    if forecast:
        first_day, first_price = next(iter(forecast.items()))
        key_signals.append({"label": "Giá dự phóng gần nhất", "value": f"{first_day}: {first_price}"})

    summary["key_signals"] = key_signals

    score = max(0, min(100, int(round(summary["score"]))))
    summary["score"] = score
    if score >= 75:
        summary["status"] = "Thuận lợi"
    elif score >= 55:
        summary["status"] = "Khá tích cực"
    elif score >= 40:
        summary["status"] = "Cân bằng"
    else:
        summary["status"] = "Rủi ro cao"

    return summary


def display_results(ticker: str, results: Dict[str, Any]) -> None:
    """Displays the analysis results in the Streamlit app with modern UI."""
    if not results:
        return

    # === HEADER WITH EXPORT ===
    col_title, col_export = st.columns([4, 1])
    with col_title:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, var(--primary) 0%, var(--primary_dark) 100%); color: white; padding: 2rem; border-radius: var(--radius-xl); margin-bottom: 2rem; text-align: center;">
            <h1 style="margin: 0; font-size: 2.5rem; font-weight: 800;">📊 {ticker}</h1>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem;">Báo cáo Phân tích Cổ phiếu Thông minh</p>
        </div>
        """, unsafe_allow_html=True)
    with col_export:
        csv_data = _export_analysis_to_csv(ticker, results)
        st.download_button(
            label="📥 Xuất CSV",
            data=csv_data,
            file_name=f"analysis_{ticker}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    # === QUICK METRICS OVERVIEW ===
    tech_data = results.get("technical_data")

    st.markdown("### 📊 Tổng quan Thị trường")
    metric_cols = st.columns(4)

    with metric_cols[0]:
        close_price = f"{tech_data['Close'].iloc[-1]:.2f}" if tech_data is not None and not tech_data.empty else NO_DATA_TEXT
        st.metric("💹 Giá đóng cửa", close_price, help="Giá đóng cửa phiên gần nhất")

    with metric_cols[1]:
        if tech_data is not None and not tech_data.empty and 'RSI' in tech_data.columns:
            rsi_value = tech_data['RSI'].iloc[-1]
            rsi_status = "Quá bán" if rsi_value < 30 else "Quá mua" if rsi_value > 70 else "Trung tính"
            rsi_delta = f"{rsi_status} ({rsi_value:.1f})"
            st.metric("🔴 RSI", f"{rsi_value:.1f}", rsi_delta)
        else:
            st.metric("🔴 RSI", NO_DATA_TEXT)

    with metric_cols[2]:
        sentiment_data = results.get('sentiment_results', {})
        sentiment_label = _translate_sentiment_label(sentiment_data.get('sentiment_category'))
        sentiment_score = sentiment_data.get('sentiment_score', 0)
        st.metric("😊 Tâm lý Thị trường", sentiment_label, f"Điểm: {sentiment_score:.1f}")

    with metric_cols[3]:
        trend = _translate_trend_label(results.get('trend_predictions', {}).get('short_term_trend'))
        st.metric("📈 Xu hướng", trend, help="Xu hướng ngắn hạn")

    # === AI INTELLIGENT ANALYSIS - CENTER PIECE ===
    st.markdown("---")
    st.markdown("### 🤖 Phân tích AI Thông minh")

    summary = _generate_intelligent_summary(results)

    # AI Score - Hero Section
    ai_score_html = f"""
    <div style="text-align: center; margin: 2rem 0;">
        <div style="display: inline-flex; align-items: center; gap: 2rem; background: var(--bg_secondary); padding: 2rem; border-radius: var(--radius-xl); border: 2px solid var(--primary);">
            <div style="text-align: center;">
                <div style="font-size: 3rem; font-weight: 800; color: var(--primary); line-height: 1;">{summary['score']}</div>
                <div style="font-size: 0.9rem; color: var(--text_secondary); margin-top: 0.25rem;">Điểm AI</div>
            </div>
            <div style="width: 1px; height: 60px; background: var(--border_light);"></div>
            <div style="text-align: center;">
                <div style="font-size: 1.5rem; font-weight: 700; color: var(--text_primary); margin-bottom: 0.5rem;">{summary['status']}</div>
                <div style="font-size: 1rem; color: var(--text_secondary);">{summary['system_hint']}</div>
            </div>
        </div>
    </div>
    """
    st.markdown(ai_score_html, unsafe_allow_html=True)

    # Progress visualization
    progress_color = "var(--success)" if summary['score'] >= 75 else "var(--warning)" if summary['score'] >= 55 else "var(--error)"
    progress_html = f"""
    <div style="margin: 1rem 0 2rem 0;">
        <div style="background: var(--bg_secondary); border-radius: 50px; height: 12px; overflow: hidden; position: relative;">
            <div style="background: linear-gradient(90deg, {progress_color}, {progress_color}CC); height: 100%; width: {summary['score']}%; border-radius: 50px; transition: width 1s ease;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; margin-top: 0.5rem;">
            <span style="font-size: 0.8rem; color: var(--text_tertiary);">Rủi ro cao</span>
            <span style="font-size: 0.8rem; color: var(--text_tertiary);">Cân bằng</span>
            <span style="font-size: 0.8rem; color: var(--text_tertiary);">Thuận lợi</span>
        </div>
    </div>
    """
    st.markdown(progress_html, unsafe_allow_html=True)

    # Key Signals Grid
    if summary["key_signals"]:
        st.markdown("**📌 Chỉ báo Then chốt:**")
        signal_cols = st.columns(min(len(summary["key_signals"]), 4))
        for i, signal in enumerate(summary["key_signals"]):
            if i < 4:  # Limit to 4 signals for better layout
                with signal_cols[i]:
                    st.markdown(f"""
                    <div style="background: var(--bg_primary); border: 1px solid var(--border_light); border-radius: var(--radius-lg); padding: 1rem; text-align: center; height: 80px; display: flex; flex-direction: column; justify-content: center;">
                        <div style="font-size: 0.75rem; color: var(--text_secondary); margin-bottom: 0.25rem;">{signal['label']}</div>
                        <div style="font-weight: 700; color: var(--text_primary); font-size: 1.1rem;">{signal['value']}</div>
                    </div>
                    """, unsafe_allow_html=True)

    # === DECISION SUMMARY ===
    st.markdown("---")
    st.markdown("### 🎯 Khuyến nghị Giao dịch")

    final_recommendation = results["final_recommendation"]
    action = final_recommendation['action']
    action_label = _translate_action_label(action)
    action_emoji = "🟢" if action == "Buy" else "🔴" if action == "Sell" else "⚪"

    # Enhanced recommendation card
    rec_html = f"""
    <div style="background: linear-gradient(135deg,
        {'var(--success), var(--success_dark)' if action == 'Buy' else 'var(--error), var(--error_dark)' if action == 'Sell' else 'var(--info), var(--info_dark)'});
        color: white; padding: 2.5rem; border-radius: var(--radius-xl); text-align: center; margin: 2rem 0; box-shadow: var(--shadow-xl);">
        <div style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.9;">{action_emoji}</div>
        <h2 style="margin: 0 0 0.5rem 0; font-size: 2.5rem; font-weight: 800;">{action_label.upper()}</h2>
        <p style="margin: 0; font-size: 1.2rem; opacity: 0.9;">Khuyến nghị giao dịch chính</p>
    </div>
    """
    st.markdown(rec_html, unsafe_allow_html=True)

    # Trading levels in a modern card
    levels_html = f"""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 2rem 0;">
        <div style="background: var(--bg_secondary); padding: 1.5rem; border-radius: var(--radius-lg); border: 1px solid var(--border_light); text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📍</div>
            <div style="font-size: 0.9rem; color: var(--text_secondary); margin-bottom: 0.25rem;">Điểm vào</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: var(--text_primary);">{final_recommendation['entry_point']}</div>
        </div>
        <div style="background: var(--bg_secondary); padding: 1.5rem; border-radius: var(--radius-lg); border: 1px solid var(--border_light); text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📈</div>
            <div style="font-size: 0.9rem; color: var(--text_secondary); margin-bottom: 0.25rem;">Chốt lời (TP)</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: var(--success);">{final_recommendation['take_profit']}</div>
        </div>
        <div style="background: var(--bg_secondary); padding: 1.5rem; border-radius: var(--radius-lg); border: 1px solid var(--border_light); text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📉</div>
            <div style="font-size: 0.9rem; color: var(--text_secondary); margin-bottom: 0.25rem;">Dừng lỗ (SL)</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: var(--error);">{final_recommendation['stop_loss']}</div>
        </div>
    </div>
    """
    st.markdown(levels_html, unsafe_allow_html=True)

    # Reasoning in expandable section
    with st.expander("💬 Lý do khuyến nghị", expanded=False):
        for i, reason in enumerate(final_recommendation['reasoning'], 1):
            st.markdown(f"**{i}.** {reason}")

    # === OPPORTUNITIES & RISKS ===
    st.markdown("---")
    st.markdown("### ⚖️ Cơ hội & Rủi ro")

    opp_risk_cols = st.columns(2)

    with opp_risk_cols[0]:
        st.markdown("**✅ Cơ hội nổi bật**")
        if summary["insights"]:
            for i, item in enumerate(summary["insights"][:4], 1):
                st.markdown(f"<div style='background: var(--success); color: white; padding: 0.75rem; border-radius: var(--radius-md); margin-bottom: 0.5rem; border-left: 4px solid var(--success_dark);'>{i}. {item}</div>", unsafe_allow_html=True)
        else:
            st.info("Chưa ghi nhận điểm nhấn nổi bật")

    with opp_risk_cols[1]:
        st.markdown("**⚠️ Rủi ro cần chú ý**")
        if summary["risks"]:
            for i, item in enumerate(summary["risks"][:4], 1):
                st.markdown(f"<div style='background: var(--warning); color: white; padding: 0.75rem; border-radius: var(--radius-md); margin-bottom: 0.5rem; border-left: 4px solid var(--warning_dark);'>{i}. {item}</div>", unsafe_allow_html=True)
        else:
            st.success("Chưa xuất hiện rủi ro đáng kể")

    # Smart money highlight
    if summary["latest_smart_money"]:
        signal = summary["latest_smart_money"]
        smart_money_html = f"""
        <div style="background: linear-gradient(135deg, var(--accent) 0%, var(--accent_dark) 100%); color: white; padding: 1.5rem; border-radius: var(--radius-lg); margin: 2rem 0;">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="font-size: 2rem;">🔎</div>
                <div>
                    <h4 style="margin: 0 0 0.25rem 0; font-size: 1.1rem;">Tín hiệu Tay to gần nhất</h4>
                    <p style="margin: 0; opacity: 0.9; font-size: 0.9rem;">{signal['date']} • {signal['severity']} • Điểm {signal['score']:.0f}/100</p>
                    <p style="margin: 0.25rem 0 0 0; font-size: 0.85rem; opacity: 0.8;">{signal['description']}</p>
                </div>
            </div>
        </div>
        """
        st.markdown(smart_money_html, unsafe_allow_html=True)

    # === DETAILED ANALYSIS ===
    st.markdown("---")
    st.markdown("### 📈 Phân tích Chi tiết")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Kỹ thuật",
        "📰 Tâm lý",
        "🔮 Dự đoán",
        "💰 Tài chính",
        "📊 Backtesting"
    ])

    with tab1:
        _display_technical_analysis(results)

    with tab2:
        _display_sentiment_analysis(results)

    with tab3:
        _display_advanced_predictions(results)

    with tab4:
        _display_financial_analysis(results)

    with tab5:
        _display_backtesting_results(results)


def main_streamlit_app() -> None:
    st.set_page_config(page_title="Hệ thống Phân tích Cổ phiếu Thông minh 📈", initial_sidebar_state="expanded")
    apply_modern_styling()

    # Theme toggle button
    create_theme_toggle()

    # Create modern header
    create_modern_header(
        "📈 Hệ thống Phân tích Cổ phiếu Thông minh",
        "Công cụ phân tích toàn diện với giao diện hiện đại và dark mode"
    )

    # Welcome message with modern card
    welcome_content = """
    <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; margin-bottom: 2rem;'>
        <div style='background: var(--bg_secondary); padding: 1.5rem; border-radius: 12px; border: 1px solid var(--border_light);'>
            <h4 style='color: var(--primary); margin: 0 0 0.5rem 0; display: flex; align-items: center;'>
                <i class='fas fa-chart-line' style='margin-right: 0.5rem;'></i>
                Phân tích Toàn diện
            </h4>
            <p style='color: var(--text_secondary); margin: 0; font-size: 0.9rem;'>Chọn một mã cổ phiếu từ thanh bên để nhận báo cáo phân tích chi tiết</p>
        </div>
        <div style='background: var(--bg_secondary); padding: 1.5rem; border-radius: 12px; border: 1px solid var(--border_light);'>
            <h4 style='color: var(--primary); margin: 0 0 0.5rem 0; display: flex; align-items: center;'>
                <i class='fas fa-search' style='margin-right: 0.5rem;'></i>
                Quét Thị trường
            </h4>
            <p style='color: var(--text_secondary); margin: 0; font-size: 0.9rem;'>Sử dụng tính năng "Quét thị trường" để tìm kiếm cơ hội đầu tư</p>
        </div>
        <div style='background: var(--bg_secondary); padding: 1.5rem; border-radius: 12px; border: 1px solid var(--border_light);'>
            <h4 style='color: var(--primary); margin: 0 0 0.5rem 0; display: flex; align-items: center;'>
                <i class='fas fa-cogs' style='margin-right: 0.5rem;'></i>
                Tùy chỉnh
            </h4>
            <p style='color: var(--text_secondary); margin: 0; font-size: 0.9rem;'>Tùy chỉnh các thông số giao dịch theo nhu cầu của bạn</p>
        </div>
    </div>
    """
    create_modern_card(welcome_content, "👋 Chào mừng bạn đến với hệ thống!")

    # Main content area
    main_container = st.container()
    with main_container:
        valid_tickers = load_stock_list(STOCK_DATA_PATH)

        if not valid_tickers:
            st.error("Không thể tải danh sách mã cổ phiếu hợp lệ. Vui lòng kiểm tra tệp 'stocks.csv'.")
            return

        # Clear results if ticker has changed
        if 'selected_ticker' in st.session_state and st.session_state.get('ticker_selector') != st.session_state.get('selected_ticker'):
            clear_analysis_results()

        st.sidebar.header("Chọn Mã Cổ Phiếu")
        selected_ticker = st.sidebar.selectbox(
            "Chọn một mã cổ phiếu:",
            [""] + valid_tickers,
            key="ticker_selector",
            # on_change callback is removed in favor of direct state checking
        )

        st.sidebar.markdown("---")
        st.sidebar.header("⚙️ Cấu hình Phân tích")

        with st.sidebar.expander("📅 Chọn khoảng thời gian"):
            period_option = st.radio("Khoảng thời gian:", ["2 năm (mặc định)", "1 năm", "6 tháng", "3 tháng", "Tùy chỉnh"])

            if period_option == "Tùy chỉnh":
                end_date = st.date_input("Ngày kết thúc:", value=datetime.now())
                start_date = st.date_input("Ngày bắt đầu:", value=datetime.now() - timedelta(days=365))
            else:
                end_date = datetime.now()
                if period_option == "2 năm (mặc định)":
                    start_date = end_date - timedelta(days=365 * 2)
                elif period_option == "1 năm":
                    start_date = end_date - timedelta(days=365)
                elif period_option == "6 tháng":
                    start_date = end_date - timedelta(days=180)
                else:
                    start_date = end_date - timedelta(days=90)

        st.sidebar.header("💰 Cấu hình Giao dịch")
        commission_rate = st.sidebar.number_input("Tỷ lệ phí giao dịch (ví dụ: 0.0015 cho 0.15%)", min_value=0.0, max_value=0.1, value=0.0015, step=0.0001, format="%.4f")
        slippage_rate = st.sidebar.number_input("Tỷ lệ trượt giá ước tính (ví dụ: 0.0005 cho 0.05%)", min_value=0.0, max_value=0.1, value=0.0005, step=0.0001, format="%.4f")

        st.sidebar.markdown("---")
        st.sidebar.header("📊 Tùy chỉnh Chỉ báo Kỹ thuật")
        with st.sidebar.expander("🔧 Tham số Chỉ báo"):
            rsi_window = st.slider("Chu kỳ RSI", min_value=7, max_value=28, value=14, step=1)
            macd_fast = st.slider("Chu kỳ MACD nhanh", min_value=8, max_value=15, value=12, step=1)
            macd_slow = st.slider("Chu kỳ MACD chậm", min_value=20, max_value=30, value=26, step=1)
            bb_window = st.slider("Chu kỳ Bollinger Bands", min_value=15, max_value=30, value=20, step=1)
            bb_std_dev = st.slider("Độ lệch chuẩn Bollinger", min_value=1.0, max_value=4.0, value=2.0, step=0.1)

        st.sidebar.header("⏰ Nhắc nhở Phái sinh")
        with st.sidebar.expander("Lịch đáo hạn VN30F"):
            reminder_window_days = st.slider("Số ngày nhắc trước", min_value=3, max_value=30, value=10, step=1)
            months_ahead = st.slider("Số kỳ theo dõi", min_value=1, max_value=12, value=4, step=1)
            show_all_contracts = st.checkbox("Luôn hiển thị toàn bộ lịch", value=False)
        derivative_settings = {
            "months_ahead": months_ahead,
            "reminder_window_days": reminder_window_days,
            "show_all": show_all_contracts,
        }

        st.sidebar.header("⚠️ Bộ lọc Tay to")
        with st.sidebar.expander("Tùy chỉnh cảnh báo dòng tiền lớn"):
            min_volume_ratio = st.slider("Khối lượng/MA20 tối thiểu (x)", min_value=1.2, max_value=3.5, value=1.8, step=0.1)
            min_price_change_pct = st.slider("Biên độ tăng tối thiểu (%)", min_value=0.5, max_value=5.0, value=1.0, step=0.1)
            lookback_days = st.slider("Số phiên theo dõi", min_value=20, max_value=180, value=60, step=5)
            min_confidence = st.slider("Điểm tin cậy tối thiểu (%)", min_value=40, max_value=100, value=60, step=5)
            severity_filter = st.multiselect(
                "Quan tâm mức độ",
                SMART_MONEY_SEVERITY_OPTIONS,
                default=SMART_MONEY_SEVERITY_OPTIONS,
            )
            signal_type_filter = st.multiselect(
                "Loại tín hiệu",
                SMART_MONEY_SIGNAL_TYPES,
                default=DEFAULT_SMART_MONEY_FILTERS["signal_types"],
            )
            max_rsi = st.slider("Giới hạn RSI (lọc quá mua)", min_value=55, max_value=90, value=DEFAULT_SMART_MONEY_FILTERS["max_rsi"], step=1)
        if not severity_filter:
            severity_filter = SMART_MONEY_SEVERITY_OPTIONS
        if not signal_type_filter:
            signal_type_filter = SMART_MONEY_SIGNAL_TYPES
        smart_money_filters = {
            "min_volume_ratio": min_volume_ratio,
            "min_price_change_pct": min_price_change_pct,
            "lookback_days": lookback_days,
            "min_confidence": min_confidence,
            "severity_filter": severity_filter,
            "signal_types": signal_type_filter,
            "max_rsi": max_rsi,
        }


        col_analyze, col_clear = st.sidebar.columns(2)
        with col_analyze:
            analyze_disabled = not selected_ticker
            if st.button("🚀 Phân tích", key="analyze_button", disabled=analyze_disabled):
                # Show progress indicator
                progress_placeholder = st.empty()
                with progress_placeholder.container():
                    create_progress_indicator(1, 4, ["Tải dữ liệu", "Phân tích kỹ thuật", "Đánh giá tài chính", "Hoàn thành"])

                with st.spinner(f"Đang phân tích {selected_ticker}..."):
                    st.session_state['indicator_params'] = {
                        'rsi_window': rsi_window,
                        'macd_short_window': macd_fast,
                        'macd_long_window': macd_slow,
                        'bb_window': bb_window,
                        'bb_num_std_dev': int(bb_std_dev) if bb_std_dev == int(bb_std_dev) else bb_std_dev
                    }

                    # Update progress
                    progress_placeholder.empty()
                    with progress_placeholder.container():
                        create_progress_indicator(2, 4, ["Tải dữ liệu", "Phân tích kỹ thuật", "Đánh giá tài chính", "Hoàn thành"])

                    analysis_results = run_analysis(
                        selected_ticker,
                        commission_rate,
                        slippage_rate,
                        display_progress=st,
                        start_date=start_date if 'start_date' in locals() else None,
                        end_date=end_date if 'end_date' in locals() else None
                    )

                    # Update progress
                    progress_placeholder.empty()
                    with progress_placeholder.container():
                        create_progress_indicator(3, 4, ["Tải dữ liệu", "Phân tích kỹ thuật", "Đánh giá tài chính", "Hoàn thành"])

                    if analysis_results:
                        st.session_state['analysis_results'] = analysis_results
                        st.session_state['selected_ticker'] = selected_ticker

                        # Final progress update
                        progress_placeholder.empty()
                        with progress_placeholder.container():
                            create_progress_indicator(4, 4, ["Tải dữ liệu", "Phân tích kỹ thuật", "Đánh giá tài chính", "Hoàn thành"])

                        st.success(f"✅ Phân tích {selected_ticker} hoàn thành!")
                        st.rerun()
                    else:
                        progress_placeholder.empty()
                        st.session_state['analysis_results'] = None
                        st.session_state['selected_ticker'] = None
                        st.error(f"❌ Không thể hoàn tất phân tích cho {selected_ticker}. Vui lòng kiểm tra mã cổ phiếu hoặc thử lại sau.")

        with col_clear:
            if st.button("Xóa phân tích", key="clear_button"):
                clear_analysis_results() # Use the dedicated function to clear everything

        analysis_results = st.session_state.get('analysis_results')

        if analysis_results:
            current_ticker = st.session_state.get('selected_ticker', selected_ticker)
            display_results(current_ticker, analysis_results)
        elif not selected_ticker:
            # Display initial message when no ticker is selected
            st.info("Vui lòng chọn một mã cổ phiếu từ thanh bên để bắt đầu phân tích.")
        elif selected_ticker and 'analysis_results' not in st.session_state:
            # This case handles when a ticker is selected but no analysis has been run yet,
            # or if a previous analysis failed and was cleared.
            st.info(f"Nhấn 'Phân tích' để bắt đầu phân tích cho {selected_ticker}.")

        _render_protection_tools(analysis_results, derivative_settings, smart_money_filters)


        st.sidebar.markdown("---")
        st.sidebar.header("Tìm Kiếm Cơ Hội Đầu Tư")
        if st.sidebar.button("🔍 Bắt đầu quét", key="scan_button"):
            st.session_state['scanning'] = True

        if st.session_state.get('scanning', False):
            investment_opportunities = find_investment_opportunities(valid_tickers, commission_rate, slippage_rate)
            if investment_opportunities and (investment_opportunities['buy'] or investment_opportunities['sell'] or investment_opportunities['hold']):
                display_scanner_results(investment_opportunities)
                st.session_state['scanning'] = False
            else:
                st.info("❌ Không tìm thấy cơ hội đầu tư nào tại thời điểm này.")
                st.session_state['scanning'] = False

        st.sidebar.markdown("---")
        st.sidebar.header("ℹ️ Về Ứng Dụng")
        st.sidebar.info(
            "🔍 **Hệ thống Phân tích Cổ phiếu Thông minh** là một công cụ toàn diện được thiết kế để cung cấp phân tích chuyên sâu về thị trường chứng khoán.\n\n"
            "Tính năng chính:\n"
            "• 📈 Phân tích kỹ thuật\n"
            "• 📰 Phân tích tâm lý thị trường\n"
            "• 🔮 Dự đoán xu hướng nâng cao\n"
            "• 💰 Phân tích tài chính\n"
            "• 📊 Kiểm tra lại chiến lược\n"
            "• 🎯 Khuyến nghị giao dịch"
        )


def display_scanner_results(opportunities: Dict[str, Any]) -> None:
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #1f77d2;'>🔍 Kết Quả Quét Cơ Hội Đầu Tư</h2>", unsafe_allow_html=True)

    total_analyzed = opportunities.get('total_analyzed', 0)
    total_errors = opportunities.get('total_errors', 0)

    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
    with summary_col1:
        st.metric("📊 Tổng số cổ phiếu", total_analyzed)
    with summary_col2:
        st.metric("🟢 Cơ hội Mua", len(opportunities['buy']))
    with summary_col3:
        st.metric("🔴 Cơ hội Bán", len(opportunities['sell']))
    with summary_col4:
        st.metric("⚪ Cổ phiếu nên giữ", len(opportunities['hold']))

    st.markdown("---")

    buy_ops = opportunities['buy']
    sell_ops = opportunities['sell']
    hold_ops = opportunities['hold']

    if buy_ops:
        st.subheader("🟢 Cơ hội Mua - Ưu tiên cao nhất")
        display_opportunities_table(buy_ops, "buy")
    else:
        st.info("ℹ️ Không tìm thấy cơ hội mua tại thời điểm này.")

    if sell_ops:
        st.markdown("---")
        st.subheader("🔴 Cơ hội Bán")
        display_opportunities_table(sell_ops, "sell")

    if hold_ops:
        st.markdown("---")
        st.subheader("⚪ Danh mục nên giữ")
        display_opportunities_table(hold_ops, "hold")


def display_opportunities_table(opportunities: List[Dict[str, Any]], action_type: str) -> None:
    sort_by = st.selectbox(
        "Sắp xếp theo:",
        ["Độ tin cậy (cao nhất trước)", "Mã cổ phiếu (A-Z)"],
        key=f"sort_{action_type}"
    )

    if sort_by == "Độ tin cậy (cao nhất trước)":
        opportunities = sorted(opportunities, key=lambda x: x.get('confidence', 0), reverse=True)
    else:
        opportunities = sorted(opportunities, key=lambda x: x['ticker'])

    display_data = []
    for opp in opportunities:
        entry_val = opp.get('entry_point', NO_DATA_TEXT)
        tp_val = opp.get('take_profit', NO_DATA_TEXT)
        sl_val = opp.get('stop_loss', NO_DATA_TEXT)
        trend_label = _translate_trend_label(opp.get('trend'))
        sentiment_raw = opp.get('sentiment', NO_DATA_TEXT)
        sentiment_label = _translate_sentiment_label(sentiment_raw)

        try:
            entry_val = float(str(entry_val).replace(',', '.'))
            tp_val = float(str(tp_val).replace(',', '.'))
            sl_val = float(str(sl_val).replace(',', '.'))
        except:
            if isinstance(entry_val, str) and entry_val.strip().upper() == "N/A":
                entry_val = NO_DATA_TEXT
            if isinstance(tp_val, str) and tp_val.strip().upper() == "N/A":
                tp_val = NO_DATA_TEXT
            if isinstance(sl_val, str) and sl_val.strip().upper() == "N/A":
                sl_val = NO_DATA_TEXT

        display_data.append({
            "Mã CP": opp['ticker'],
            "Độ tin cậy": f"{opp.get('confidence', 0):.0f}%",
            "RSI": opp.get('rsi', NO_DATA_TEXT),
            "Xu hướng": trend_label,
            "Tâm lý": sentiment_label,
            "Điểm vào": entry_val,
            "Chốt lời (TP)": tp_val,
            "Dừng lỗ (SL)": sl_val
        })

    df = pd.DataFrame(display_data)
    st.dataframe(
        df,
        width='stretch',
        hide_index=True,
        column_config={
            "Độ tin cậy": st.column_config.ProgressColumn(
                "Độ tin cậy",
                min_value=0,
                max_value=100,
            ),
        }
    )

    expander_key = f"details_{action_type}"
    with st.expander("📋 Xem chi tiết từng cơ hội"):
        for opp in opportunities:
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])

                with col1:
                    st.markdown(f"**{opp['ticker']}** - Độ tin cậy: `{opp.get('confidence', 0):.0f}%`")

                with col2:
                    trend_label = _translate_trend_label(opp.get('trend'))
                    if opp.get('trend'):
                        st.caption(f"📈 {trend_label}")

                with col3:
                    sentiment = opp.get('sentiment', NO_DATA_TEXT)
                    sentiment_color = _get_sentiment_icon(sentiment)
                    st.caption(f"{sentiment_color} {_translate_sentiment_label(sentiment)}")

                reasoning = opp.get('reasoning', [])
                if reasoning:
                    st.write("**Lý do:**")
                    for i, reason in enumerate(reasoning[:3], 1):
                        st.write(f"  {i}. {reason}")

                col_ep, col_tp, col_sl = st.columns(3)
                with col_ep:
                    st.write(f"**Điểm vào:** {opp.get('entry_point', NO_DATA_TEXT)}")
                with col_tp:
                    st.write(f"**Chốt lời (TP):** {opp.get('take_profit', NO_DATA_TEXT)}")
                with col_sl:
                    st.write(f"**Dừng lỗ (SL):** {opp.get('stop_loss', NO_DATA_TEXT)}")

                st.divider()


def _display_derivatives_reminders(settings: Optional[Dict[str, Any]]) -> None:
    st.markdown("#### ⏰ Nhắc nhở đáo hạn phái sinh")
    merged_settings = {**DEFAULT_DERIVATIVE_SETTINGS, **(settings or {})}
    reminder_window = int(max(1, merged_settings.get("reminder_window_days", 10)))
    schedule = get_derivative_expiry_overview(
        months_ahead=int(max(1, merged_settings.get("months_ahead", 4)))
    )

    if not schedule:
        st.info("Không tìm thấy lịch đáo hạn phái sinh.")
        return

    upcoming_contracts = [item for item in schedule if item["days_remaining"] >= 0]
    if not upcoming_contracts:
        st.info("Tất cả các kỳ đáo hạn đã trôi qua. Vui lòng mở rộng phạm vi theo dõi.")
        return

    next_contract = upcoming_contracts[0]
    days_remaining = next_contract["days_remaining"]
    days_label = "Hôm nay" if days_remaining == 0 else f"Còn {days_remaining} ngày"
    st.metric(
        "Hợp đồng gần nhất",
        next_contract["code"],
        f"{days_label}",
        help=f"Đáo hạn {next_contract['expiry_date'].strftime('%d/%m/%Y')} ({next_contract['cycle']})",
    )

    urgent_contracts = [
        contract
        for contract in upcoming_contracts
        if contract["days_remaining"] <= reminder_window
    ]
    if urgent_contracts:
        for contract in urgent_contracts:
            due_in = contract["days_remaining"]
            due_label = "Đáo hạn hôm nay" if due_in == 0 else f"Còn {due_in} ngày"
            st.warning(
                f"**{contract['code']}** ({contract['month_label']}) - {contract['expiry_date'].strftime('%d/%m/%Y')} • {due_label}"
            )
    else:
        st.success(f"Chưa có hợp đồng nào nằm trong cửa sổ {reminder_window} ngày.")

    if merged_settings.get("show_all") or len(upcoming_contracts) > len(urgent_contracts):
        table_source = (
            upcoming_contracts
            if merged_settings.get("show_all")
            else [c for c in upcoming_contracts if c not in urgent_contracts]
        )
        if table_source:
            table_data = [
                {
                    "Mã hợp đồng": item["code"],
                    "Chu kỳ": item["cycle"],
                    "Ngày đáo hạn": item["expiry_date"].strftime("%d/%m/%Y"),
                    "Còn lại (ngày)": item["days_remaining"],
                }
                for item in table_source
            ]
            df = pd.DataFrame(table_data)
            st.dataframe(df, width='stretch', hide_index=True)


def _display_smart_money_alerts(
    technical_data: Optional[pd.DataFrame], filters: Optional[Dict[str, Any]]
) -> None:
    st.markdown("#### ⚠️ Cảnh báo 'tay to vào hàng'")
    merged_filters = {**DEFAULT_SMART_MONEY_FILTERS, **(filters or {})}
    severity_filter = merged_filters.get("severity_filter") or SMART_MONEY_SEVERITY_OPTIONS
    signal_type_filter = merged_filters.get("signal_types") or SMART_MONEY_SIGNAL_TYPES
    max_rsi = merged_filters.get("max_rsi")

    if technical_data is None or technical_data.empty:
        st.info("Chạy phân tích để kích hoạt bộ cảnh báo 'tay to'.")
        return

    detection = detect_smart_money_activity(
        technical_data,
        min_volume_ratio=merged_filters["min_volume_ratio"],
        min_price_change_pct=merged_filters["min_price_change_pct"],
        lookback_days=int(merged_filters["lookback_days"]),
    )

    filtered_signals = [
        signal
        for signal in detection["signals"]
        if signal["confidence"] >= merged_filters["min_confidence"]
        and signal["severity"] in severity_filter
        and (signal_type_filter is None or signal["type"] in signal_type_filter)
        and (max_rsi is None or signal["rsi"] is None or signal["rsi"] <= max_rsi)
    ]

    summary_text = (
        f"Ngưỡng quét: Khối lượng ≥ {merged_filters['min_volume_ratio']}x MA20 • "
        f"Biên độ ≥ {merged_filters['min_price_change_pct']:.1f}% • "
        f"Điểm đánh giá ≥ {merged_filters['min_confidence']}%"
    )
    st.caption(summary_text)

    col_total, col_last, col_window = st.columns(3)
    with col_total:
        st.metric("Phiên được quét", detection["total_sessions"])
    with col_last:
        st.metric("Tín hiệu gần nhất", filtered_signals[0]["date"] if filtered_signals else NO_DATA_TEXT)
    with col_window:
        st.metric("Số tín hiệu đạt chuẩn", len(filtered_signals))

    if not filtered_signals:
        st.success(
            f"Chưa xuất hiện tín hiệu 'tay to' đáp ứng bộ lọc hiện tại trong {detection['total_sessions']} phiên."
        )
        return

    st.warning(
        f"Phát hiện {len(filtered_signals)} tín hiệu dòng tiền lớn đạt chuẩn chuyên sâu."
    )

    df = pd.DataFrame(
        [
            {
                "Ngày": signal["date"],
                "Loại tín hiệu": signal.get("type", NO_DATA_TEXT),
                "Mức độ": signal["severity"],
                "Điểm đánh giá": f"{signal['score']:.1f}",
                "RSI": f"{signal['rsi']:.1f}" if signal.get("rsi") is not None else NO_DATA_TEXT,
                "Tăng/giảm (%)": f"{signal['price_change_pct']:.2f}",
                "Khối lượng/MA20": f"{signal['volume_ratio']:.2f}x",
                "Giá đóng cửa": f"{signal['close']:.2f}",
            }
            for signal in filtered_signals
        ]
    )
    st.dataframe(
        df,
        width='stretch',
        hide_index=True,
        column_config={
            "Điểm đánh giá": st.column_config.ProgressColumn("Điểm đánh giá", min_value=0, max_value=100),
            "Khối lượng/MA20": st.column_config.NumberColumn(format="%.2f x"),
        },
    )

    with st.expander("📋 Chi tiết cảnh báo"):
        for signal in filtered_signals:
            rsi_text = f"{signal['rsi']:.1f}" if signal.get("rsi") is not None else NO_DATA_TEXT
            note_text = signal.get("note", NO_DATA_TEXT)
            st.markdown(
                f"**{signal['date']}** · {signal.get('type', NO_DATA_TEXT)} · {signal['severity']} · {signal['confidence']:.0f}% tin cậy  \n"
                f"{signal['description']}  \n"
                f"RSI: {rsi_text} • Điểm: {signal['score']:.1f} • Ghi chú: {note_text}"
            )


def _render_protection_tools(
    analysis_results: Optional[Dict[str, Any]],
    derivative_settings: Dict[str, Any],
    smart_money_filters: Dict[str, Any],
) -> None:
    st.markdown("---")
    st.subheader("🛡️ Công cụ nhắc nhở & cảnh báo nâng cao")
    col_derivative, col_smart_money = st.columns(2)
    with col_derivative:
        _display_derivatives_reminders(derivative_settings)
    with col_smart_money:
        technical_data = (
            analysis_results.get("technical_data") if analysis_results else None
        )
        _display_smart_money_alerts(technical_data, smart_money_filters)


def clear_analysis_results() -> None:
    if 'analysis_results' in st.session_state:
        del st.session_state['analysis_results']
    if 'selected_ticker' in st.session_state:
        del st.session_state['selected_ticker']


if __name__ == "__main__":
    main_streamlit_app()