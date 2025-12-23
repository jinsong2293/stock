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
from stock_analyzer.modules.enhanced_stock_forecast import EnhancedStockForecastSystem

# Cấu hình ứng dụng
st.set_page_config(
    page_title="Hệ thống Dự báo Chứng khoán Việt Nam 📈", 
    initial_sidebar_state="expanded",
    layout="wide",
    page_icon="🇻🇳"
)

# Đường dẫn dữ liệu
STOCK_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'stocks.csv')
NO_DATA_TEXT = "Không có dữ liệu"

# Tùy chỉnh CSS cho giao diện Việt Nam
st.markdown("""
<style>
    .main > div {
        padding-top: 1rem;
    }
    .stButton > button {
        min-height: 48px;
        font-size: 16px;
        border-radius: 8px;
        font-weight: 600;
    }
    .metric-card {
        background: linear-gradient(135deg, #1f77d2 0%, #0d4a8a 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        margin: 0.5rem 0;
    }
    .vietnam-flag {
        color: #da020e;
        font-size: 1.2em;
    }
    .prediction-card {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    .confidence-high { color: #28a745; font-weight: bold; }
    .confidence-medium { color: #ffc107; font-weight: bold; }
    .confidence-low { color: #dc3545; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

def load_stock_list(file_path: str) -> List[str]:
    """Tải danh sách mã cổ phiếu hợp lệ từ file CSV."""
    try:
        df = pd.read_csv(file_path)
        return df['Ticker'].tolist()
    except FileNotFoundError:
        st.error(f"❌ Lỗi: Không tìm thấy tệp dữ liệu cổ phiếu tại {file_path}")
        return []
    except Exception as e:
        st.error(f"❌ Lỗi khi tải dữ liệu: {e}")
        return []

def _create_price_chart(tech_data: pd.DataFrame) -> go.Figure:
    """Tạo biểu đồ giá tương tác với Dải Bollinger."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=tech_data.index, y=tech_data['Close'],
        mode='lines', name='Giá đóng cửa', 
        line=dict(color='#1f77d2', width=3),
        hovertemplate='<b>Ngày:</b> %{x}<br><b>Giá:</b> %{y:,.0f} VND<extra></extra>'
    ))
    
    if 'BB_Upper' in tech_data.columns and 'BB_Lower' in tech_data.columns:
        fig.add_trace(go.Scatter(
            x=tech_data.index, y=tech_data['BB_Upper'],
            mode='lines', name='Dải Bollinger Trên', 
            line=dict(color='rgba(255, 0, 0, 0.6)', dash='dash', width=2),
            hovertemplate='<b>Dải trên:</b> %{y:,.0f} VND<extra></extra>'
        ))
        fig.add_trace(go.Scatter(
            x=tech_data.index, y=tech_data['BB_Lower'],
            mode='lines', name='Dải Bollinger Dưới',
            line=dict(color='rgba(255, 0, 0, 0.6)', dash='dash', width=2),
            fill='tonexty', fillcolor='rgba(255, 0, 0, 0.1)',
            hovertemplate='<b>Dải dưới:</b> %{y:,.0f} VND<extra></extra>'
        ))
    
    fig.update_layout(
        title='📈 Biểu đồ Giá Cổ phiếu & Dải Bollinger', 
        xaxis_title='📅 Thời gian', 
        yaxis_title='💰 Giá (VND)',
        hovermode='x unified', 
        template='plotly_white',
        height=500,
        font=dict(family="Arial", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def _create_rsi_chart(tech_data: pd.DataFrame) -> go.Figure:
    """Tạo biểu đồ RSI tương tác."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=tech_data.index, y=tech_data['RSI'],
        mode='lines', name='RSI', 
        line=dict(color='#ff7f0e', width=3),
        hovertemplate='<b>RSI:</b> %{y:.1f}<extra></extra>'
    ))
    
    fig.add_hline(y=70, line_dash="dash", line_color="#dc3545", 
                  annotation_text="🔴 Vùng quá mua (70)", annotation_position="top right")
    fig.add_hline(y=30, line_dash="dash", line_color="#28a745", 
                  annotation_text="🟢 Vùng quá bán (30)", annotation_position="bottom right")
    fig.add_hrect(y0=0, y1=30, fillcolor="rgba(40, 167, 69, 0.1)", layer="below")
    fig.add_hrect(y0=70, y1=100, fillcolor="rgba(220, 53, 69, 0.1)", layer="below")
    
    fig.update_layout(
        title='📊 Chỉ số RSI (Sức mạnh tương đối)',
        xaxis_title='📅 Thời gian',
        yaxis_title='📈 Giá trị RSI',
        hovermode='x unified',
        template='plotly_white',
        height=400,
        font=dict(family="Arial", size=12)
    )
    return fig

def _create_macd_chart(tech_data: pd.DataFrame) -> go.Figure:
    """Tạo biểu đồ MACD tương tác."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=tech_data.index, y=tech_data['MACD'],
        mode='lines', name='MACD', 
        line=dict(color='#1f77d2', width=3),
        hovertemplate='<b>MACD:</b> %{y:.3f}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=tech_data.index, y=tech_data['MACD_Signal'],
        mode='lines', name='Đường tín hiệu',
        line=dict(color='#ff7f0e', width=3),
        hovertemplate='<b>Tín hiệu:</b> %{y:.3f}<extra></extra>'
    ))
    
    colors = ['#28a745' if val >= 0 else '#dc3545' for val in tech_data['MACD_Hist']]
    fig.add_trace(go.Bar(
        x=tech_data.index, y=tech_data['MACD_Hist'],
        name='Histogram', marker_color=colors, opacity=0.6,
        hovertemplate='<b>Histogram:</b> %{y:.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='📉 MACD (Phân kỳ hội tụ trung bình động)',
        xaxis_title='📅 Thời gian',
        yaxis_title='💹 Giá trị MACD',
        hovermode='x unified',
        template='plotly_white',
        height=400,
        font=dict(family="Arial", size=12)
    )
    return fig

def _display_technical_analysis(results: Dict[str, Any]) -> None:
    """Hiển thị phân tích kỹ thuật."""
    st.header("📊 1. Tóm tắt Phân tích Kỹ thuật")
    st.markdown("*Phân tích chi tiết các chỉ báo kỹ thuật để đánh giá xu hướng giá*")
    
    tech_data = results["technical_data"]
    if not tech_data.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(_create_price_chart(tech_data), width='stretch')
        with col2:
            st.plotly_chart(_create_rsi_chart(tech_data), width='stretch')
        
        st.plotly_chart(_create_macd_chart(tech_data), width='stretch')

        st.subheader("📋 Dữ liệu Kỹ thuật Chi tiết")
        cols_to_display = ['Close', 'RSI', 'MACD', 'MACD_Signal', 'BB_Upper', 'BB_Middle', 'BB_Lower', 'OBV', 'AD_Line', 'ATR']
        cols_available = [col for col in cols_to_display if col in tech_data.columns]
        
        # Định dạng lại dữ liệu hiển thị
        display_data = tech_data[cols_available].tail(10).copy()
        for col in cols_available:
            if col in ['Close', 'BB_Upper', 'BB_Middle', 'BB_Lower']:
                display_data[col] = display_data[col].apply(lambda x: f"{x:,.0f} VND")
            elif col in ['RSI', 'MACD', 'MACD_Signal']:
                display_data[col] = display_data[col].apply(lambda x: f"{x:.2f}")
            elif col in ['OBV', 'AD_Line', 'ATR']:
                display_data[col] = display_data[col].apply(lambda x: f"{x:,.0f}")
        
        st.dataframe(display_data, width='stretch')
    else:
        st.error("❌ Không có dữ liệu kỹ thuật để hiển thị.")

def _display_sentiment_analysis(results: Dict[str, Any]) -> None:
    """Hiển thị phân tích tâm lý thị trường."""
    st.header("😊 2. Tóm tắt Phân tích Tâm lý Thị trường")
    st.markdown("*Đánh giá tâm lý và cảm xúc của nhà đầu tư đối với cổ phiếu*")
    
    sentiment_results = results["sentiment_results"]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        sentiment_score = sentiment_results.get('sentiment_score', 0.0)
        if sentiment_score > 0.6:
            emoji = "😊"
            color = "#28a745"
        elif sentiment_score < 0.4:
            emoji = "😔"
            color = "#dc3545"
        else:
            emoji = "😐"
            color = "#ffc107"
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>{emoji} Điểm Tâm lý</h3>
            <h2 style="color: {color}; margin: 0;">{sentiment_score:.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        sentiment_label = sentiment_results.get('sentiment_category', 'N/A')
        if sentiment_label == 'Positive':
            emoji = "🟢"
            label = "Tích cực"
            color = "#28a745"
        elif sentiment_label == 'Negative':
            emoji = "🔴"
            label = "Tiêu cực"
            color = "#dc3545"
        else:
            emoji = "🟡"
            label = "Trung tính"
            color = "#ffc107"
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>📈 Trạng thái</h3>
            <h2 style="color: {color}; margin: 0;">{emoji} {label}</h2>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        news_impact = sentiment_results.get('news_impact', NO_DATA_TEXT)
        st.markdown(f"""
        <div class="metric-card">
            <h3>📰 Tác động Tin tức</h3>
            <h2 style="margin: 0;">{news_impact}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.info(f"**📱 Mức độ Lan truyền Mạng xã hội:** {sentiment_results.get('social_media_buzz', NO_DATA_TEXT)}")

def _display_advanced_predictions(results: Dict[str, Any]) -> None:
    """Hiển thị dự đoán xu hướng nâng cao."""
    st.header("🔮 3. Tóm tắt Dự đoán Xu hướng Nâng cao")
    st.markdown("*Sử dụng AI và thuật toán học máy để dự đoán xu hướng tương lai*")
    
    trend_predictions = results["trend_predictions"]

    st.subheader("📈 Dự đoán Xu hướng")
    col_trend1, col_trend2 = st.columns(2)
    short_term_trend = trend_predictions.get('short_term_trend')
    medium_term_trend = trend_predictions.get('medium_term_trend')

    short_conf_display = trend_predictions.get('short_term_confidence', NO_DATA_TEXT)
    medium_conf_display = trend_predictions.get('medium_term_confidence', NO_DATA_TEXT)

    with col_trend1:
        if short_term_trend:
            if 'up' in short_term_trend.lower():
                emoji = "📈"
                color = "#28a745"
                trend_text = "Tăng"
            elif 'down' in short_term_trend.lower():
                emoji = "📉"
                color = "#dc3545"
                trend_text = "Giảm"
            else:
                emoji = "➡️"
                color = "#ffc107"
                trend_text = "Đi ngang"
        else:
            emoji = "❓"
            color = "#6c757d"
            trend_text = NO_DATA_TEXT
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>🔵 Xu hướng Ngắn hạn</h3>
            <h2 style="color: {color}; margin: 0;">{emoji} {trend_text}</h2>
            <p>Độ tin cậy: {short_conf_display}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_trend2:
        if medium_term_trend:
            if 'up' in medium_term_trend.lower():
                emoji = "📈"
                color = "#28a745"
                trend_text = "Tăng"
            elif 'down' in medium_term_trend.lower():
                emoji = "📉"
                color = "#dc3545"
                trend_text = "Giảm"
            else:
                emoji = "➡️"
                color = "#ffc107"
                trend_text = "Đi ngang"
        else:
            emoji = "❓"
            color = "#6c757d"
            trend_text = NO_DATA_TEXT
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>🟢 Xu hướng Trung hạn</h3>
            <h2 style="color: {color}; margin: 0;">{emoji} {trend_text}</h2>
            <p>Độ tin cậy: {medium_conf_display}</p>
        </div>
        """, unsafe_allow_html=True)

    price_forecast = trend_predictions.get('price_forecast_next_5_days', {})
    if price_forecast:
        st.success(f"**🎯 Dự báo giá (5 ngày tới):**")
        for date, price in price_forecast.items():
            st.write(f"• **{date}:** {price}")

def _display_financial_analysis(results: Dict[str, Any]) -> None:
    """Hiển thị phân tích tài chính."""
    st.header("💰 4. Tóm tắt Phân tích Báo cáo Tài chính")
    st.markdown("*Đánh giá sức khỏe tài chính và khả năng sinh lời của công ty*")
    
    financial_data = results["financial_data"]
    financial_health = results["financial_health"]

    st.subheader("🏥 Đánh giá Sức khỏe Tài chính Tổng thể")
    assessment = financial_health.get('overall_assessment', 'N/A')
    if "Strong" in assessment or "Mạnh" in assessment:
        emoji = "💪"
        color = "#28a745"
        status = "Mạnh mẽ"
    elif "Weak" in assessment or "Yếu" in assessment:
        emoji = "⚠️"
        color = "#dc3545"
        status = "Yếu kém"
    else:
        emoji = "😐"
        color = "#ffc107"
        status = "Trung bình"
    
    st.markdown(f"""
    <div class="metric-card">
        <h2>{emoji} {status}</h2>
        <p>{assessment}</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📊 Các Chỉ số Tài chính Quan trọng")
    financial_ratios_display = {}
    for key, value in financial_data.items():
        if value is None:
            financial_ratios_display[key] = NO_DATA_TEXT
        elif isinstance(value, (int, float)):
            if 'ratio' in key.lower() or 'rate' in key.lower():
                financial_ratios_display[key] = f"{value:.2%}"
            else:
                financial_ratios_display[key] = f"{value:,.0f}"
        else:
            financial_ratios_display[key] = value

    # Tạo DataFrame với styling
    df_display = pd.DataFrame.from_dict(financial_ratios_display, orient='index', columns=['Giá trị'])
    df_display.index.name = 'Chỉ số'
    
    st.dataframe(df_display, width='stretch')

def _display_trade_recommendations(results: Dict[str, Any]) -> None:
    """Hiển thị khuyến nghị giao dịch."""
    st.header("🎯 5. Khuyến nghị Giao dịch")
    st.markdown("*Đưa ra khuyến nghị cụ thể về hành động giao dịch*")
    
    final_recommendation = results["final_recommendation"]
    action = final_recommendation.get('action', 'Hold')
    
    if action == "Buy":
        emoji = "🟢"
        color = "#28a745"
        text = "MUA"
        bg_color = "linear-gradient(135deg, #28a745 0%, #20c997 100%)"
    elif action == "Sell":
        emoji = "🔴"
        color = "#dc3545"
        text = "BÁN"
        bg_color = "linear-gradient(135deg, #dc3545 0%, #c82333 100%)"
    else:
        emoji = "🟡"
        color = "#ffc107"
        text = "NẮM GIỮ"
        bg_color = "linear-gradient(135deg, #ffc107 0%, #fd7e14 100%)"
    
    st.markdown(f"""
    <div style="background: {bg_color}; color: white; padding: 2rem; border-radius: 15px; text-align: center; margin: 1rem 0;">
        <h1 style="font-size: 3rem; margin: 0;">{emoji}</h1>
        <h2 style="margin: 0.5rem 0; font-size: 2.5rem; font-weight: 800;">{text}</h2>
        <p style="margin: 0; font-size: 1.2rem; opacity: 0.9;">Khuyến nghị chính</p>
    </div>
    """, unsafe_allow_html=True)

    # Các mức giá quan trọng
    col1, col2, col3 = st.columns(3)
    with col1:
        entry_point = final_recommendation.get('entry_point', NO_DATA_TEXT)
        st.metric(label="🎯 Điểm vào", value=entry_point, help="Giá khuyến nghị để mở vị thế")
    with col2:
        take_profit = final_recommendation.get('take_profit', NO_DATA_TEXT)
        st.metric(label="📈 Chốt lời (TP)", value=take_profit, help="Giá mục tiêu để chốt lời")
    with col3:
        stop_loss = final_recommendation.get('stop_loss', NO_DATA_TEXT)
        st.metric(label="📉 Dừng lỗ (SL)", value=stop_loss, help="Giá cắt lỗ để hạn chế rủi ro")

    # Lý do khuyến nghị
    st.subheader("💡 Lý do Khuyến nghị")
    reasoning = final_recommendation.get('reasoning', [])
    if reasoning:
        for i, reason in enumerate(reasoning, 1):
            st.write(f"**{i}.** {reason}")
    else:
        st.info("ℹ️ Chưa có lý do cụ thể.")

def _display_2day_forecast(results: Dict[str, Any], ticker: str) -> None:
    """Hiển thị dự báo 2 ngày tới với hệ thống nâng cao."""
    st.header("🎯 6. Dự báo Xu hướng 2 ngày tới")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 12px; margin: 1rem 0;">
        <h3>🤖 Hệ thống Dự báo Tiên tiến</h3>
        <p><strong>Sử dụng công nghệ AI & Machine Learning:</strong></p>
        <ul style="margin: 0; padding-left: 1.5rem;">
            <li><strong>🤖 Ensemble Learning:</strong> Kết hợp LSTM, Prophet, XGBoost, ARIMA</li>
            <li><strong>📊 Phân tích Kỹ thuật:</strong> RSI, MACD, Bollinger Bands, Moving Averages</li>
            <li><strong>📰 Sentiment Analysis:</strong> Phân tích cảm xúc từ tin tức tài chính</li>
            <li><strong>🏛️ Kinh tế Vĩ mô:</strong> Chỉ báo kinh tế và xu hướng thị trường</li>
            <li><strong>🧠 Feature Engineering:</strong> Tạo 127 đặc trưng từ dữ liệu đa chiều</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize forecast system
    with st.spinner("🔄 Đang khởi tạo hệ thống dự báo AI..."):
        forecast_system = EnhancedStockForecastSystem()
    
    # Generate forecast
    with st.spinner("🤖 Đang phân tích và dự đoán bằng AI..."):
        try:
            forecast_result = forecast_system.predict_next_2_days(ticker)
        except Exception as e:
            st.error(f"❌ Lỗi tạo dự báo: {e}")
            return
    
    if 'error' in forecast_result:
        st.error(f"❌ {forecast_result['error']}")
        return
    
    # Display forecast results
    predictions = forecast_result.get('predictions', [])
    
    if predictions:
        st.subheader("📊 Kết quả Dự báo AI")
        
        # Main forecast metrics
        col1, col2, col3 = st.columns(3)
        
        day_1 = predictions[0]
        day_2 = predictions[1] if len(predictions) > 1 else {}
        
        with col1:
            current_price = day_1.get('current_price', 0)
            st.markdown(f"""
            <div class="metric-card">
                <h3>💰 Giá Hiện tại</h3>
                <h2 style="margin: 0; color: #1f77d2;">{current_price:,.0f} VND</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            day_1_price = day_1.get('predicted_price', 0)
            day_1_change = day_1.get('predicted_change_points', 0)
            day_1_direction = day_1.get('direction', 'neutral').upper()
            direction_emoji = "🟢" if day_1_direction == "UP" else "🔴" if day_1_direction == "DOWN" else "⚪"
            
            change_color = "#28a745" if day_1_change > 0 else "#dc3545" if day_1_change < 0 else "#6c757d"
            
            st.markdown(f"""
            <div class="metric-card">
                <h3>{direction_emoji} Ngày mai ({day_1.get('date', '')})</h3>
                <h2 style="margin: 0; color: #1f77d2;">{day_1_price:,.0f} VND</h2>
                <p style="margin: 0; color: {change_color}; font-weight: bold;">{day_1_change:+.2f} điểm</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            day_2_price = day_2.get('predicted_price', 0)
            day_2_change = day_2.get('predicted_change_points', 0)
            day_2_direction = day_2.get('direction', 'neutral').upper()
            direction_emoji = "🟢" if day_2_direction == "UP" else "🔴" if day_2_direction == "DOWN" else "⚪"
            
            change_color = "#28a745" if day_2_change > 0 else "#dc3545" if day_2_change < 0 else "#6c757d"
            
            st.markdown(f"""
            <div class="metric-card">
                <h3>{direction_emoji} Ngày kia ({day_2.get('date', '')})</h3>
                <h2 style="margin: 0; color: #1f77d2;">{day_2_price:,.0f} VND</h2>
                <p style="margin: 0; color: {change_color}; font-weight: bold;">{day_2_change:+.2f} điểm</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Confidence scores
        st.subheader("🎯 Độ tin cậy của AI")
        confidence_col1, confidence_col2 = st.columns(2)
        
        with confidence_col1:
            day_1_confidence = day_1.get('confidence_score', 0)
            
            # Phân loại confidence
            if day_1_confidence >= 0.8:
                conf_class = "confidence-high"
                conf_text = "Rất cao"
                conf_color = "#28a745"
            elif day_1_confidence >= 0.6:
                conf_class = "confidence-medium"
                conf_text = "Cao"
                conf_color = "#ffc107"
            else:
                conf_class = "confidence-low"
                conf_text = "Trung bình"
                conf_color = "#dc3545"
            
            st.markdown(f"""
            <div class="metric-card">
                <h3>🤖 AI Confidence - Ngày mai</h3>
                <h2 style="margin: 0; color: {conf_color};">{day_1_confidence:.1%}</h2>
                <p style="margin: 0; color: {conf_color}; font-weight: bold;">{conf_text}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Confidence bar
            st.progress(day_1_confidence)
        
        with confidence_col2:
            day_2_confidence = day_2.get('confidence_score', 0)
            
            # Phân loại confidence
            if day_2_confidence >= 0.8:
                conf_class = "confidence-high"
                conf_text = "Rất cao"
                conf_color = "#28a745"
            elif day_2_confidence >= 0.6:
                conf_class = "confidence-medium"
                conf_text = "Cao"
                conf_color = "#ffc107"
            else:
                conf_class = "confidence-low"
                conf_text = "Trung bình"
                conf_color = "#dc3545"
            
            st.markdown(f"""
            <div class="metric-card">
                <h3>🤖 AI Confidence - Ngày kia</h3>
                <h2 style="margin: 0; color: {conf_color};">{day_2_confidence:.1%}</h2>
                <p style="margin: 0; color: {conf_color}; font-weight: bold;">{conf_text}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Confidence bar
            st.progress(day_2_confidence)
        
        # Detailed prediction table
        st.subheader("📋 Bảng Chi tiết Dự báo")
        
        forecast_data = []
        for pred in predictions:
            direction_text = "Tăng" if pred.get('direction', '').upper() == "UP" else "Giảm" if pred.get('direction', '').upper() == "DOWN" else "Đi ngang"
            forecast_data.append({
                "Ngày": pred.get('date', ''),
                "Hướng": direction_text,
                "Điểm thay đổi": f"{pred.get('predicted_change_points', 0):+.2f}",
                "% thay đổi": f"{pred.get('change_percentage', 0):+.2f}%",
                "Giá dự báo": f"{pred.get('predicted_price', 0):,.0f} VND",
                "Độ tin cậy": f"{pred.get('confidence_score', 0):.1%}"
            })
        
        if forecast_data:
            forecast_df = pd.DataFrame(forecast_data)
            st.dataframe(forecast_df, hide_index=True, width='stretch')
        
        # Market context
        market_context = forecast_result.get('market_context', {})
        if market_context:
            st.subheader("📊 Bối cảnh Thị trường")
            
            context_col1, context_col2, context_col3 = st.columns(3)
            
            with context_col1:
                st.metric("🔧 Điểm Kỹ thuật", f"{market_context.get('technical_score', 0):.1f}/100", help="Đánh giá dựa trên các chỉ báo kỹ thuật")
                st.metric("📈 Điểm Xu hướng", f"{market_context.get('trend_score', 0):.1f}/100", help="Đánh giá xu hướng giá")
            
            with context_col2:
                st.metric("📊 Điểm Khối lượng", f"{market_context.get('volume_score', 0):.1f}/100", help="Đánh giá dựa trên khối lượng giao dịch")
                st.metric("😊 Điểm Sentiment", f"{market_context.get('sentiment_score', 0):.1f}/100", help="Đánh giá tâm lý thị trường")
            
            with context_col3:
                st.metric("🎯 Điểm Tổng thể", f"{market_context.get('overall_score', 0):.1f}/100", help="Điểm tổng hợp từ tất cả các yếu tố")
                
                macro_score = market_context.get('macro_economic_score')
                if macro_score is not None:
                    st.metric("🏛️ Điểm Kinh tế Vĩ mô", f"{macro_score:.1f}/100", help="Đánh giá dựa trên các chỉ báo kinh tế")
        
        # Export functionality
        st.subheader("📥 Xuất dữ liệu Dự báo")
        
        json_str = json.dumps(forecast_result, indent=2, default=str, ensure_ascii=False)
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Tải JSON đầy đủ",
                data=json_str,
                file_name=f"du_bao_{ticker}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                width='stretch'
            )
        
        with col2:
            # Show JSON preview
            with st.expander("🔍 Xem JSON Preview", expanded=False):
                st.json(forecast_result, expanded=False)
    
    else:
        st.warning("⚠️ Không có dữ liệu dự báo để hiển thị.")

def _export_analysis_to_csv(ticker: str, results: Dict[str, Any]) -> bytes:
    """Xuất kết quả phân tích sang định dạng CSV."""
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
    
    output += "5. KHUYẾN NGHỊ GIAO DỊCH\n"
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

def display_results(ticker: str, results: Dict[str, Any]) -> None:
    """Hiển thị kết quả phân tích trong ứng dụng Streamlit."""
    if not results:
        return

    # Header với xuất dữ liệu
    col_title, col_export = st.columns([4, 1])
    with col_title:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #da020e 0%, #ffff00 50%, #da020e 100%); color: white; padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center; border: 3px solid #da020e;">
            <div class="vietnam-flag">🇻🇳</div>
            <h1 style="margin: 0.5rem 0; font-size: 2.8rem; font-weight: 900; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">{ticker}</h1>
            <p style="margin: 0; font-size: 1.3rem; opacity: 0.95; font-weight: 600;">Báo cáo Phân tích Cổ phiếu Toàn diện</p>
            <p style="margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.9;">Với Dự báo AI 2 ngày tới</p>
        </div>
        """, unsafe_allow_html=True)
    with col_export:
        csv_data = _export_analysis_to_csv(ticker, results)
        st.download_button(
            label="📥 Xuất Báo cáo",
            data=csv_data,
            file_name=f"bao_cao_{ticker}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            width='stretch',
            help="Tải xuống báo cáo phân tích đầy đủ"
        )

    # Tổng quan nhanh
    tech_data = results.get("technical_data")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        close_price = f"{tech_data['Close'].iloc[-1]:,.0f} VND" if tech_data is not None and not tech_data.empty else NO_DATA_TEXT
        st.metric("💹 Giá Đóng cửa", close_price)

    with col2:
        if tech_data is not None and not tech_data.empty and 'RSI' in tech_data.columns:
            rsi_value = tech_data['RSI'].iloc[-1]
            if rsi_value < 30:
                status = "Quá bán 🟢"
                delta_color = "inverse"
            elif rsi_value > 70:
                status = "Quá mua 🔴"
                delta_color = "inverse"
            else:
                status = "Trung tính 🟡"
                delta_color = "normal"
            st.metric("🔴 RSI", f"{rsi_value:.1f}", status, delta_color=delta_color)
        else:
            st.metric("🔴 RSI", NO_DATA_TEXT)

    with col3:
        sentiment_data = results.get('sentiment_results', {})
        sentiment_label = sentiment_data.get('sentiment_category', NO_DATA_TEXT)
        sentiment_score = sentiment_data.get('sentiment_score')
        
        if sentiment_score:
            if sentiment_score > 0.6:
                emoji = "😊"
                status = "Tích cực"
            elif sentiment_score < 0.4:
                emoji = "😔"
                status = "Tiêu cực"
            else:
                emoji = "😐"
                status = "Trung tính"
            st.metric(f"{emoji} Tâm lý", status, f"Điểm: {sentiment_score:.1f}")
        else:
            st.metric("😊 Tâm lý", NO_DATA_TEXT)

    with col4:
        trend = results.get('trend_predictions', {}).get('short_term_trend', NO_DATA_TEXT)
        if trend:
            if 'up' in trend.lower():
                emoji = "📈"
            elif 'down' in trend.lower():
                emoji = "📉"
            else:
                emoji = "➡️"
            st.metric(f"{emoji} Xu hướng", trend)
        else:
            st.metric("📈 Xu hướng", NO_DATA_TEXT)

    st.markdown("---")

    # Tóm tắt khuyến nghị
    st.subheader("🎯 Tóm tắt Khuyến nghị")

    final_recommendation = results["final_recommendation"]
    action = final_recommendation.get('action', 'Hold')
    
    if action == "Buy":
        emoji = "🟢"
        color = "#28a745"
        text = "MUA"
        bg_color = "linear-gradient(135deg, #28a745 0%, #20c997 100%)"
    elif action == "Sell":
        emoji = "🔴"
        color = "#dc3545"
        text = "BÁN"
        bg_color = "linear-gradient(135deg, #dc3545 0%, #c82333 100%)"
    else:
        emoji = "🟡"
        color = "#ffc107"
        text = "NẮM GIỮ"
        bg_color = "linear-gradient(135deg, #ffc107 0%, #fd7e14 100%)"

    st.markdown(f"""
    <div style="background: {bg_color}; color: white; padding: 2rem; border-radius: 15px; text-align: center; margin-bottom: 2rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        <div style="font-size: 4rem; margin-bottom: 1rem;">{emoji}</div>
        <h2 style="margin: 0; font-size: 2.5rem; font-weight: 900; text-transform: uppercase;">{text}</h2>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">Khuyến nghị Giao dịch Chính</p>
    </div>
    """, unsafe_allow_html=True)

    # Các mức giá quan trọng
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎯 Điểm vào", final_recommendation.get('entry_point', NO_DATA_TEXT), help="Giá khuyến nghị để mở vị thế")
    with col2:
        st.metric("📈 Chốt lời", final_recommendation.get('take_profit', NO_DATA_TEXT), help="Giá mục tiêu để chốt lời")
    with col3:
        st.metric("📉 Dừng lỗ", final_recommendation.get('stop_loss', NO_DATA_TEXT), help="Giá cắt lỗ để hạn chế rủi ro")

    st.markdown("---")

    # Chi tiết phân tích
    st.subheader("📊 Phân tích Chi tiết")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Kỹ thuật",
        "😊 Tâm lý", 
        "🔮 Dự đoán",
        "💰 Tài chính",
        "🎯 Giao dịch",
        "🤖 AI 2 ngày",
        "🎯 Quét Cơ hội Đầu tư"
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
        _display_trade_recommendations(results)
        
    with tab6:
        _display_2day_forecast(results, ticker)
        
    with tab7:
        _display_investment_scanner_tab()

def clear_analysis_results() -> None:
    """Xóa kết quả phân tích khỏi session state."""
    if 'analysis_results' in st.session_state:
        del st.session_state['analysis_results']
    if 'selected_ticker' in st.session_state:
        del st.session_state['selected_ticker']
    if 'scanner_results' in st.session_state:
        del st.session_state['scanner_results']

# ===== COMPREHENSIVE INVESTMENT SCANNER FUNCTIONS =====

def _display_scanner_summary(scan_summary: Dict[str, Any], results: Optional[List[Dict[str, Any]]] = None) -> None:
    """Hiển thị tổng quan kết quả quét thị trường với giao diện trực quan."""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
        <h2 style="margin: 0; font-size: 2rem; font-weight: bold;">📊 Tổng quan Thị trường Chứng khoán</h2>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">Phân tích toàn diện cơ hội đầu tư</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics chính
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_stocks = scan_summary.get('total_stocks', 0)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 12px; text-align: center;">
            <h3 style="margin: 0; font-size: 2.5rem; font-weight: bold;">{total_stocks}</h3>
            <p style="margin: 0; font-size: 1rem; opacity: 0.9;">🎯 Tổng cổ phiếu</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_score = scan_summary.get('averages', {}).get('overall_score', 0)
        score_color = "#28a745" if avg_score > 75 else "#ffc107" if avg_score > 60 else "#dc3545"
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 1.5rem; border-radius: 12px; text-align: center;">
            <h3 style="margin: 0; font-size: 2.5rem; font-weight: bold; color: {score_color};">{avg_score:.1f}</h3>
            <p style="margin: 0; font-size: 1rem; opacity: 0.9;">📈 Điểm TB</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_upside = scan_summary.get('averages', {}).get('upside_potential', 0)
        upside_color = "#28a745" if avg_upside > 10 else "#ffc107" if avg_upside > 5 else "#dc3545"
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 1.5rem; border-radius: 12px; text-align: center;">
            <h3 style="margin: 0; font-size: 2.5rem; font-weight: bold; color: {upside_color};">{avg_upside:+.1f}%</h3>
            <p style="margin: 0; font-size: 1rem; opacity: 0.9;">🚀 Tiềm năng TB</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        buy_opportunities = scan_summary.get('top_buy_opportunities', 0)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; padding: 1.5rem; border-radius: 12px; text-align: center;">
            <h3 style="margin: 0; font-size: 2.5rem; font-weight: bold;">{buy_opportunities}</h3>
            <p style="margin: 0; font-size: 1rem; opacity: 0.9;">🟢 Cơ hội Mua</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Phân bố khuyến nghị với biểu đồ trực quan tương tác
    st.subheader("🎯 Phân bố Khuyến nghị Thị trường (Bấm vào cột để xem chi tiết)")
    rec_dist = scan_summary.get('recommendation_distribution', {})
    if rec_dist:
        # Tạo DataFrame cho biểu đồ
        rec_df = pd.DataFrame(list(rec_dist.items()), columns=['Khuyến nghị', 'Số lượng'])
        
        # Tạo cột cho màu sắc
        color_map = {
            'MUA MẠNH': '#28a745',
            'MUA': '#20c997', 
            'NẮM GIỮ': '#ffc107',
            'BÁN': '#dc3545'
        }
        
        rec_df['Màu'] = rec_df['Khuyến nghị'].map(color_map)
        
        # Hiển thị biểu đồ cột tương tác
        fig = go.Figure(data=[go.Bar(
            x=rec_df['Khuyến nghị'],
            y=rec_df['Số lượng'],
            marker_color=rec_df['Màu'],
            text=rec_df['Số lượng'],
            textposition='auto',
            customdata=rec_df['Khuyến nghị'],  # Thêm data cho click
            hovertemplate='<b>%{x}</b><br>Số lượng: %{y}<br>Khuyến nghị: %{customdata}<br><extra></extra>'
        )])
        
        fig.update_layout(
            title="Phân bố Khuyến nghị - Bấm vào cột để xem chi tiết",
            xaxis_title="Khuyến nghị",
            yaxis_title="Số lượng cổ phiếu",
            template="plotly_white",
            height=400
        )
        
        # Hiển thị biểu đồ với selection mode
        chart_result = st.plotly_chart(
            fig, 
            use_container_width=True, 
            on_select="rerun",
            selection_mode=["points"]
        )
        
        # Xử lý click vào cột
        if chart_result and chart_result.selection and chart_result.selection.get('points'):
            selected_point = chart_result.selection['points'][0]
            selected_recommendation = selected_point['customdata']
            
            # Lọc và hiển thị cổ phiếu theo khuyến nghị được chọn
            filtered_stocks = _filter_stocks_by_recommendation(results, selected_recommendation)
            
            if filtered_stocks:
                st.success(f"📊 **Chi tiết {selected_recommendation}** - Tìm thấy {len(filtered_stocks)} cổ phiếu:")
                
                # Tạo bảng chi tiết cho khuyến nghị được chọn
                _display_recommendation_details(filtered_stocks, selected_recommendation)
            else:
                st.warning(f"⚠️ Không tìm thấy cổ phiếu nào cho khuyến nghị {selected_recommendation}")
        
        # Hiển thị tổng quan các khuyến nghị bằng metrics
        st.markdown("**📈 Tổng quan các khuyến nghị:**")
        cols = st.columns(len(rec_dist))
        for i, (rec, count) in enumerate(rec_dist.items()):
            with cols[i]:
                color = color_map.get(rec, '#6c757d')
                emoji = '🟢' if 'MUA' in rec else '🔴' if 'BÁN' in rec else '🟡'
                st.markdown(f"""
                <div style="background: {color}; color: white; padding: 1rem; border-radius: 10px; text-align: center;">
                    <h4 style="margin: 0; font-size: 1.5rem;">{emoji} {rec}</h4>
                    <p style="margin: 0; font-size: 1.8rem; font-weight: bold;">{count}</p>
                    <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">cổ phiếu</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Phân bố theo ngành
    st.subheader("🏭 Phân bố theo Ngành Nghề")
    sector_dist = scan_summary.get('sector_distribution', {})
    if sector_dist:
        # Tạo pie chart
        fig = go.Figure(data=[go.Pie(
            labels=list(sector_dist.keys()),
            values=list(sector_dist.values()),
            hole=0.3,
            textinfo='label+percent',
            textfont_size=12,
        )])
        
        fig.update_layout(
            title="Phân bố Cổ phiếu theo Ngành",
            template="plotly_white",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

def _display_scanner_results_table(scanner_results: List[Dict[str, Any]]) -> None:
    """Hiển thị bảng kết quả quét thị trường."""
    st.subheader("🏆 Top Cơ hội Đầu tư")
    
    if not scanner_results:
        st.warning("⚠️ Không có kết quả để hiển thị.")
        return
    
    # Chuẩn bị dữ liệu hiển thị
    display_data = []
    
    for i, result in enumerate(scanner_results):
        # Handle both dict and StockAnalysisResult objects
        if hasattr(result, 'symbol'):  # StockAnalysisResult object
            display_data.append({
                'Mã': result.symbol,
                'Công ty': result.company_name,
                'Ngành': result.sector,
                'Giá hiện tại': f"{result.current_price:,.0f} VND",
                'Thay đổi %': f"{result.price_change_pct:+.1f}%",
                'Khuyến nghị': result.recommendation,
                'Điểm tổng': f"{result.overall_score:.1f}",
                'Tiềm năng': f"{result.upside_potential:+.1f}%",
                'Rủi ro': result.risk_level,
                'P/E': f"{result.pe_ratio:.1f}"
            })
        else:  # Dictionary
            display_data.append({
                'Mã': result.get('symbol', f'STOCK_{i+1}'),
                'Công ty': result.get('company_name', f'Công ty {i+1}'),
                'Ngành': result.get('sector', 'Khác'),
                'Giá hiện tại': f"{result.get('current_price', 50000):,.0f} VND",
                'Thay đổi %': f"{result.get('price_change_pct', 0):+.1f}%",
                'Khuyến nghị': result.get('recommendation', 'NẮM GIỮ'),
                'Điểm tổng': f"{result.get('overall_score', 50):.1f}",
                'Tiềm năng': f"{result.get('upside_potential', 0):+.1f}%",
                'Rủi ro': result.get('risk_level', 'TRUNG BÌNH'),
                'P/E': f"{result.get('pe_ratio', 15):.1f}"
            })
    
    # Tạo DataFrame và hiển thị
    df = pd.DataFrame(display_data)
    
    # Hiển thị bảng
    st.dataframe(df, width='stretch', hide_index=True)
    
    # Download button
    csv = df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 Tải xuống CSV",
        data=csv,
        file_name=f"investment_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        width='stretch'
    )



def perform_investment_scan(criteria: Any) -> Dict[str, Any]:
    """Thực hiện quét thị trường tìm cơ hội đầu tư."""
    try:
        # Import scanner module at runtime to optimize startup
        from stock_analyzer.modules.comprehensive_investment_scanner import ComprehensiveInvestmentScanner
        
        with st.spinner("🔍 Đang quét thị trường và phân tích cơ hội đầu tư..."):
            scanner = ComprehensiveInvestmentScanner(max_workers=3)
            results = scanner.scan_market_opportunities(criteria)
            return results
    except Exception as e:
        st.error(f"❌ Lỗi khi quét thị trường: {e}")
        return {'error': str(e)}

def _filter_stocks_by_recommendation(results: List[Dict[str, Any]], recommendation: str) -> List[Dict[str, Any]]:
    """Lọc cổ phiếu theo khuyến nghị được chọn"""
    filtered_stocks = []
    
    for stock in results:
        # Handle both dict and StockAnalysisResult objects
        if hasattr(stock, 'recommendation'):  # StockAnalysisResult object
            if stock.recommendation == recommendation:
                filtered_stocks.append(stock)
        else:  # Dictionary
            if stock.get('recommendation', '') == recommendation:
                filtered_stocks.append(stock)
    
    return filtered_stocks

def _display_recommendation_details(filtered_stocks: List[Dict[str, Any]], recommendation: str) -> None:
    """Hiển thị chi tiết cổ phiếu theo khuyến nghị"""
    if not filtered_stocks:
        return
    
    # Màu sắc theo khuyến nghị
    color_map = {
        'MUA MẠNH': '#28a745',
        'MUA': '#20c997',
        'NẮM GIỮ': '#ffc107',
        'BÁN': '#dc3545'
    }
    
    color = color_map.get(recommendation, '#6c757d')
    
    # Header cho section chi tiết
    st.markdown(f"""
    <div style="background: {color}; color: white; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
        <h3 style="margin: 0; font-size: 1.5rem;">📊 Chi tiết Khuyến nghị: {recommendation}</h3>
        <p style="margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.9;">Tổng cộng {len(filtered_stocks)} cổ phiếu</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chuẩn bị dữ liệu hiển thị
    display_data = []
    
    for stock in filtered_stocks:
        # Handle both dict and StockAnalysisResult objects
        if hasattr(stock, 'symbol'):  # StockAnalysisResult object
            display_data.append({
                'Mã': stock.symbol,
                'Công ty': stock.company_name,
                'Ngành': stock.sector,
                'Giá hiện tại': f"{stock.current_price:,.0f} VND",
                'Thay đổi %': f"{stock.price_change_pct:+.1f}%",
                'Điểm tổng': f"{stock.overall_score:.1f}",
                'Tiềm năng': f"{stock.upside_potential:+.1f}%",
                'Rủi ro': stock.risk_level,
                'P/E': f"{stock.pe_ratio:.1f}",
                'RSI': f"{stock.rsi:.1f}",
                'Tin tức': stock.news_count
            })
        else:  # Dictionary
            display_data.append({
                'Mã': stock.get('symbol', ''),
                'Công ty': stock.get('company_name', ''),
                'Ngành': stock.get('sector', ''),
                'Giá hiện tại': f"{stock.get('current_price', 0):,.0f} VND",
                'Thay đổi %': f"{stock.get('price_change_pct', 0):+.1f}%",
                'Điểm tổng': f"{stock.get('overall_score', 0):.1f}",
                'Tiềm năng': f"{stock.get('upside_potential', 0):+.1f}%",
                'Rủi ro': stock.get('risk_level', ''),
                'P/E': f"{stock.get('pe_ratio', 0):.1f}",
                'RSI': f"{stock.get('rsi', 0):.1f}",
                'Tin tức': stock.get('news_count', 0)
            })
    
    # Tạo DataFrame và hiển thị
    df = pd.DataFrame(display_data)
    
    # Sắp xếp theo điểm tổng giảm dần
    df['Điểm số'] = df['Điểm tổng'].str.replace(' điểm', '').astype(float)
    df = df.sort_values('Điểm số', ascending=False).drop('Điểm số', axis=1)
    
    # Hiển thị bảng
    st.dataframe(df, width='stretch', hide_index=True)
    
    # Thống kê tổng quan cho khuyến nghị này
    st.markdown("**📈 Thống kê tổng quan:**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_score = df['Điểm tổng'].str.replace(' điểm', '').astype(float).mean()
        st.metric("📈 Điểm TB", f"{avg_score:.1f}")
    
    with col2:
        avg_upside = df['Tiềm năng'].str.replace('%', '').str.replace('+', '').astype(float).mean()
        st.metric("🚀 Tiềm năng TB", f"{avg_upside:+.1f}%")
    
    with col3:
        avg_pe = df['P/E'].astype(float).mean()
        st.metric("💰 P/E TB", f"{avg_pe:.1f}")
    
    with col4:
        total_volume = df['Tin tức'].astype(int).sum()
        st.metric("📰 Tổng tin tức", total_volume)

def _display_investment_scanner_tab() -> None:
    """Hiển thị tab Công cụ Quét Cơ hội Đầu tư."""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #da020e; font-size: 2.5rem; font-weight: 900; margin: 0;">🎯 Công cụ Quét Cơ hội Đầu tư</h1>
        <p style="font-size: 1.2rem; color: #666; margin: 0.5rem 0;">Tìm kiếm và phân tích toàn diện cơ hội đầu tư</p>
        <p style="font-size: 1rem; color: #888; margin: 0;">Phân tích 284 cổ phiếu từ tất cả sàn giao dịch</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tiêu chí tìm kiếm
    st.subheader("🔍 Bộ lọc Tìm kiếm")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        sectors = st.multiselect(
            "Ngành nghề",
            ['Ngân hàng', 'Công nghệ', 'Bất động sản', 'Thực phẩm & Đồ uống', 'Dầu khí'],
            default=[]
        )
    
    with col2:
        market_caps = st.multiselect(
            "Vốn hóa thị trường",
            ['Lớn', 'Vừa', 'Nhỏ'],
            default=[]
        )
    
    with col3:
        exchanges = st.multiselect(
            "Sàn giao dịch",
            ['HOSE', 'HNX', 'UPCOM'],
            default=['HOSE']
        )
    
    with col4:
        limit = st.selectbox("Kết quả hiển thị", [20, 50, 100], index=1)
    
    # Bộ lọc nâng cao
    with st.expander("⚙️ Bộ lọc Nâng cao", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            price_range = st.slider("Khoảng giá (VND)", 1000, 500000, (10000, 200000))
            volume_min = st.number_input("Khối lượng tối thiểu", 0, 10000000, 100000)
        
        with col2:
            pe_range = st.slider("Tỷ số P/E", 0, 50, (5, 30))
            risk_filter = st.selectbox("Mức rủi ro", ['', 'THẤP', 'TRUNG BÌNH', 'CAO'])
        
        with col3:
            recommendation_filter = st.selectbox("Khuyến nghị", ['', 'MUA MẠNH', 'MUA', 'NẮM GIỮ', 'BÁN'])
            sentiment_filter = st.selectbox("Tâm lý thị trường", ['', 'TÍCH CỰC', 'TIÊU CỰC', 'TRUNG TÍNH'])
    
    # Nút thực hiện quét
    scan_col, = st.columns([1])
    
    with scan_col:
        if st.button("🚀 Quét Cơ hội", width='stretch', type="primary"):
            # Import ScanCriteria at runtime to optimize startup
            from stock_analyzer.modules.comprehensive_investment_scanner import ScanCriteria
            
            # Tạo tiêu chí quét
            criteria = ScanCriteria(
                sectors=sectors if sectors else None,
                market_caps=market_caps if market_caps else None,
                exchanges=exchanges if exchanges else None,
                price_range=price_range if price_range != (10000, 200000) else None,
                volume_min=volume_min if volume_min > 0 else None,
                pe_range=pe_range if pe_range != (5, 30) else None,
                risk_level=risk_filter if risk_filter else None,
                recommendation=recommendation_filter if recommendation_filter else None,
                sentiment_filter=sentiment_filter if sentiment_filter else None,
                sort_by='overall_score',
                sort_order='desc',
                limit=limit
            )
            
            # Thực hiện quét
            results = perform_investment_scan(criteria)
            
            if results and 'error' not in results:
                st.session_state['scanner_results'] = results
                st.success(f"✅ Hoàn thành quét! Tìm thấy {results.get('scan_summary', {}).get('total_stocks', 0)} cơ hội đầu tư hấp dẫn")
                st.rerun()
            else:
                st.error(f"❌ Lỗi quét thị trường: {results.get('error', 'Lỗi không xác định')}")
    
    # Hiển thị kết quả
    if 'scanner_results' in st.session_state:
        scanner_results = st.session_state['scanner_results']
        
        if 'error' in scanner_results:
            st.error(f"❌ {scanner_results['error']}")
            return
        
        # Metadata
        metadata = scanner_results.get('scan_metadata', {})
        st.info(f"🕐 **Thời gian phân tích:** {metadata.get('scan_duration_seconds', 0):.1f} giây | 📊 **Đã quét:** {metadata.get('stocks_analyzed', 0)} cổ phiếu")
        
        # Tổng quan
        scan_summary = scanner_results.get('scan_summary', {})
        results = scanner_results.get('results', [])
        if scan_summary:
            _display_scanner_summary(scan_summary, results)
        
        # Bảng kết quả
        results = scanner_results.get('results', [])
        if results:
            _display_scanner_results_table(results)
            
            # Top opportunities
            st.subheader("🏆 Top 5 Cơ hội Đầu tư Tốt nhất")
            top_opportunities = scanner_results.get('top_opportunities', [])
            
            if top_opportunities:
                cols = st.columns(5)
                for i, stock in enumerate(top_opportunities[:5]):
                    with cols[i]:
                        # Handle both dict and StockAnalysisResult objects
                        if hasattr(stock, 'recommendation'):  # StockAnalysisResult object
                            recommendation = stock.recommendation
                            symbol = stock.symbol
                            overall_score = stock.overall_score
                        else:  # Dictionary
                            recommendation = stock.get('recommendation', '')
                            symbol = stock.get('symbol', '')
                            overall_score = stock.get('overall_score', 0)
                        
                        # Màu sắc theo khuyến nghị
                        if 'STRONG_BUY' in recommendation:
                            bg_color = "#d4edda"
                            text_color = "#155724"
                        elif 'BUY' in recommendation:
                            bg_color = "#d1ecf1"
                            text_color = "#0c5460"
                        elif 'HOLD' in recommendation:
                            bg_color = "#fff3cd"
                            text_color = "#856404"
                        else:
                            bg_color = "#f8d7da"
                            text_color = "#721c24"
                        
                        st.markdown(f"""
                        <div style="background: {bg_color}; color: {text_color}; padding: 1rem; border-radius: 10px; text-align: center; border: 2px solid {text_color};">
                            <h4 style="margin: 0; font-weight: bold;">{symbol}</h4>
                            <p style="margin: 0.5rem 0 0 0; font-size: 0.9em;">{overall_score:.1f}/100</p>
                            <p style="margin: 0; font-size: 0.8em; font-weight: bold;">{recommendation.replace('_', ' ')}</p>
                        </div>
                        """, unsafe_allow_html=True)
        
        # Nút xóa kết quả
        if st.button("🗑️ Xóa Kết quả"):
            if 'scanner_results' in st.session_state:
                del st.session_state['scanner_results']
                st.rerun()
    
    else:
        # Thông báo hướng dẫn
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; border: 2px dashed #dee2e6;">
            <h3 style="color: #6c757d; margin-bottom: 1rem;">🎯 Công cụ Quét Cơ hội Đầu tư</h3>
            <p style="color: #6c757d; font-size: 1.1rem; margin-bottom: 2rem;">
                Sử dụng bộ lọc bên trên để tìm kiếm cơ hội đầu tư tốt nhất trên thị trường chứng khoán Việt Nam
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 2rem;">
                <div style="background: white; padding: 1.5rem; border-radius: 10px; border: 1px solid #dee2e6;">
                    <h4 style="color: #007bff; margin: 0 0 0.5rem 0;">📊 284 Mã Cổ phiếu</h4>
                    <p style="color: #6c757d; margin: 0; font-size: 0.9rem;">Toàn bộ HOSE, HNX, UPCOM</p>
                </div>
                <div style="background: white; padding: 1.5rem; border-radius: 10px; border: 1px solid #dee2e6;">
                    <h4 style="color: #28a745; margin: 0 0 0.5rem 0;">🔍 38 Chỉ báo Kỹ thuật</h4>
                    <p style="color: #6c757d; margin: 0; font-size: 0.9rem;">MA, RSI, MACD, Dải Bollinger...</p>
                </div>
                <div style="background: white; padding: 1.5rem; border-radius: 10px; border: 1px solid #dee2e6;">
                    <h4 style="color: #ffc107; margin: 0 0 0.5rem 0;">💰 Chỉ số Tài chính</h4>
                    <p style="color: #6c757d; margin: 0; font-size: 0.9rem;">P/E, P/B, ROE, ROA, tăng trưởng</p>
                </div>
                <div style="background: white; padding: 1.5rem; border-radius: 10px; border: 1px solid #dee2e6;">
                    <h4 style="color: #dc3545; margin: 0 0 0.5rem 0;">⚠️ Đánh giá Rủi ro</h4>
                    <p style="color: #6c757d; margin: 0; font-size: 0.9rem;">VaR, Beta, Sharpe, Biến động</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def main_streamlit_app() -> None:
    """Ứng dụng Streamlit chính."""
    # Header chính
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🇻🇳</div>
        <h1 style="color: #da020e; font-size: 3.5rem; font-weight: 900; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
            HỆ THỐNG DỰ BÁO CHỨNG KHOÁN VIỆT NAM
        </h1>
        <p style="font-size: 1.4rem; color: #666; margin: 0.5rem 0; font-weight: 600;">
            Phân tích Toàn diện với Trí tuệ Nhân tạo
        </p>
        <p style="font-size: 1rem; color: #888; margin: 0;">
            Được phát triển bởi AI & Machine Learning 🇻🇳
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Container chính
    main_container = st.container()
    with main_container:
        valid_tickers = load_stock_list(STOCK_DATA_PATH)

        if not valid_tickers:
            st.error("❌ Không thể tải danh sách mã cổ phiếu hợp lệ. Vui lòng kiểm tra tệp 'stocks.csv'.")
            return

        # Xóa kết quả nếu ticker thay đổi
        if 'selected_ticker' in st.session_state and st.session_state.get('ticker_selector') != st.session_state.get('selected_ticker'):
            clear_analysis_results()

        # Sidebar
        st.sidebar.header("🇻🇳 Chọn Mã Cổ phiếu")
        selected_ticker = st.sidebar.selectbox(
            "Vui lòng chọn một mã cổ phiếu:",
            [""] + valid_tickers,
            key="ticker_selector",
            help="Chọn mã cổ phiếu từ danh sách"
        ) 
        
        st.sidebar.markdown("---")
        st.sidebar.header("⚙️ Cấu hình Phân tích")
        
        with st.sidebar.expander("📅 Chọn Khoảng thời gian"):
            period_option = st.radio("Khoảng thời gian phân tích:", 
                                   ["2 năm (Khuyến nghị)", "1 năm", "6 tháng", "3 tháng"],
                                   help="Chọn khoảng thời gian dữ liệu để phân tích")
            
            end_date = datetime.now()
            if period_option == "2 năm (Khuyến nghị)":
                start_date = end_date - timedelta(days=365 * 2)
            elif period_option == "1 năm":
                start_date = end_date - timedelta(days=365)
            elif period_option == "6 tháng":
                start_date = end_date - timedelta(days=180)
            else:
                start_date = end_date - timedelta(days=90)
        
        st.sidebar.header("💰 Cấu hình Giao dịch")
        commission_rate = st.sidebar.number_input(
            "Tỷ lệ phí giao dịch (%)", 
            min_value=0.0, max_value=1.0, value=0.15, step=0.01, format="%.2f",
            help="Phí hoa hồng môi giới (ví dụ: 0.15 cho 0.15%)"
        )
        slippage_rate = st.sidebar.number_input(
            "Tỷ lệ trượt giá (%)", 
            min_value=0.0, max_value=0.5, value=0.05, step=0.01, format="%.2f",
            help="Trượt giá ước tính khi giao dịch (ví dụ: 0.05 cho 0.05%)"
        )
        
        st.sidebar.markdown("---")
        st.sidebar.header("📊 Tùy chỉnh Chỉ báo Kỹ thuật")
        with st.sidebar.expander("🔧 Tham số Chỉ báo"):
            st.markdown("*Tùy chỉnh các thông số cho chỉ báo kỹ thuật*")
            rsi_window = st.slider("Chu kỳ RSI", 7, 28, 14, 1, help="Chu kỳ tính toán RSI")
            macd_fast = st.slider("MACD Nhanh", 8, 15, 12, 1, help="Chu kỳ MACD nhanh")
            macd_slow = st.slider("MACD Chậm", 20, 30, 26, 1, help="Chu kỳ MACD chậm")
            bb_window = st.slider("Bollinger Bands", 15, 30, 20, 1, help="Chu kỳ Bollinger Bands")
            bb_std_dev = st.slider("Độ lệch chuẩn BB", 1.0, 4.0, 2.0, 0.1, help="Độ lệch chuẩn Bollinger Bands")

        # Nút điều khiển chính
        col_analyze, col_clear = st.sidebar.columns(2)
        with col_analyze:
            analyze_disabled = not selected_ticker
            if st.button("🚀 Bắt đầu Phân tích", key="analyze_button", disabled=analyze_disabled, width='stretch'):
                with st.spinner(f"🤖 Đang phân tích {selected_ticker} bằng AI..."):
                    st.session_state['indicator_params'] = {
                        'rsi_window': rsi_window,
                        'macd_short_window': macd_fast,
                        'macd_long_window': macd_slow,
                        'bb_window': bb_window,
                        'bb_num_std_dev': int(bb_std_dev) if bb_std_dev == int(bb_std_dev) else bb_std_dev
                    }

                    analysis_results = run_analysis(
                        selected_ticker,
                        commission_rate/100,  # Convert to decimal
                        slippage_rate/100,    # Convert to decimal
                        display_progress=st,
                        start_date=start_date if 'start_date' in locals() else None,
                        end_date=end_date if 'end_date' in locals() else None
                    )

                    if analysis_results:
                        st.session_state['analysis_results'] = analysis_results
                        st.session_state['selected_ticker'] = selected_ticker
                        st.success(f"✅ Hoàn thành phân tích {selected_ticker}!")
                        st.rerun()
                    else:
                        st.session_state['analysis_results'] = None
                        st.session_state['selected_ticker'] = None
                        st.error(f"❌ Không thể hoàn tất phân tích cho {selected_ticker}. Vui lòng kiểm tra mã cổ phiếu hoặc thử lại sau.")

        with col_clear:
            if st.button("🗑️ Xóa Kết quả", key="clear_button", width='stretch'):
                clear_analysis_results()

        # Hiển thị kết quả
        analysis_results = st.session_state.get('analysis_results')

        if analysis_results:
            current_ticker = st.session_state.get('selected_ticker', selected_ticker)
            display_results(current_ticker, analysis_results)
        elif not selected_ticker:
            # Thông báo ban đầu
            st.markdown("""
            <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; border: 2px dashed #dee2e6;">
                <h2 style="color: #6c757d; margin-bottom: 1rem;">📊 Chào mừng đến với Hệ thống Dự báo Chứng khoán Việt Nam</h2>
                <p style="color: #6c757d; font-size: 1.1rem; margin-bottom: 2rem;">
                    Vui lòng chọn một mã cổ phiếu từ thanh bên để bắt đầu phân tích toàn diện
                </p>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 2rem;">
                    <div style="background: white; padding: 1.5rem; border-radius: 10px; border: 1px solid #dee2e6;">
                        <h4 style="color: #1f77d2; margin: 0 0 0.5rem 0;">📈 Phân tích Kỹ thuật</h4>
                        <p style="color: #6c757d; margin: 0; font-size: 0.9rem;">RSI, MACD, Bollinger Bands</p>
                    </div>
                    <div style="background: white; padding: 1.5rem; border-radius: 10px; border: 1px solid #dee2e6;">
                        <h4 style="color: #28a745; margin: 0 0 0.5rem 0;">🤖 Dự báo AI 2 ngày</h4>
                        <p style="color: #6c757d; margin: 0; font-size: 0.9rem;">Machine Learning & Deep Learning</p>
                    </div>
                    <div style="background: white; padding: 1.5rem; border-radius: 10px; border: 1px solid #dee2e6;">
                        <h4 style="color: #ffc107; margin: 0 0 0.5rem 0;">💰 Phân tích Tài chính</h4>
                        <p style="color: #6c757d; margin: 0; font-size: 0.9rem;">Báo cáo tài chính chi tiết</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif selected_ticker and 'analysis_results' not in st.session_state:
            st.info(f"📋 Nhấn nút 'Bắt đầu Phân tích' để phân tích cổ phiếu {selected_ticker}.")

        # Thông tin về ứng dụng
        st.sidebar.markdown("---")
        st.sidebar.header("ℹ️ Về Ứng dụng")
        st.sidebar.markdown("""
        **🇻🇳 Hệ thống Dự báo Chứng khoán Việt Nam**
        
        **Tính năng chính:**
        • 📊 Phân tích kỹ thuật toàn diện
        • 😊 Phân tích tâm lý thị trường  
        • 🔮 Dự đoán xu hướng AI
        • 💰 Phân tích tài chính doanh nghiệp
        • 🎯 Khuyến nghị giao dịch
        • 🤖 Dự báo 2 ngày tới bằng AI
        • 🎯 Công cụ Quét Cơ hội Đầu tư
        
        **Công nghệ:**
        • Trí tuệ Nhân tạo (AI)
        • Phân tích Kỹ thuật
        • Phân tích Tâm lý Thị trường
        • Xử lý Dữ liệu Thời gian thực
        """)

if __name__ == "__main__":
    main_streamlit_app()
