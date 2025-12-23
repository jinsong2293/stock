"""
Modern UI Components - Các thành phần UI hiện đại cho Stock Analyzer
Bao gồm metrics, cards, buttons với styling mới
"""

import streamlit as st
from typing import Dict, Any

def create_modern_metric_container(title: str, value: str, delta: str = "", delta_type: str = "normal", icon: str = ""):
    """Tạo metric container hiện đại với styling mới"""
    
    # Xác định màu sắc dựa trên delta_type
    color_map = {
        "success": "var(--success)",
        "warning": "var(--warning)", 
        "error": "var(--error)",
        "info": "var(--info)",
        "normal": "var(--text_secondary)"
    }
    
    icon_html = f'<i class="fas {icon}" style="margin-right: 0.5rem; color: {color_map.get(delta_type, color_map["normal"])};"></i>' if icon else ''
    
    delta_html = ""
    if delta:
        delta_color = "green" if delta_type == "success" else "red" if delta_type == "error" else "orange" if delta_type == "warning" else "var(--text_secondary)"
        delta_html = f'<div style="font-size: 0.875rem; color: {delta_color}; font-weight: 500; margin-top: 0.25rem;">{delta}</div>'
    
    st.markdown(f"""
    <div class="modern-metric animate-fade-in-up">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
            <div style="font-size: 0.875rem; font-weight: 500; color: var(--text_secondary); text-transform: uppercase; letter-spacing: 0.5px;">
                {icon_html}{title}
            </div>
        </div>
        <div style="font-size: 2rem; font-weight: 700; color: var(--text_primary); margin-bottom: 0.25rem;">
            {value}
        </div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)



def create_smart_summary_card(summary_data: Dict[str, Any]):
    """Tạo card tóm tắt thông minh"""
    
    score = summary_data.get("score", 50)
    status = summary_data.get("status", "Cân bằng")
    hint = summary_data.get("system_hint", "Theo dõi thêm")
    
    # Xác định màu dựa trên điểm số
    if score >= 75:
        status_color = "var(--success)"
        status_icon = "fa-arrow-trend-up"
    elif score >= 55:
        status_color = "var(--info)"
        status_icon = "fa-arrow-trend-right"
    elif score >= 40:
        status_color = "var(--warning)"
        status_icon = "fa-arrow-trend-right"
    else:
        status_color = "var(--error)"
        status_icon = "fa-arrow-trend-down"
    
    # Tạo progress bar
    progress_color = status_color
    progress_html = f"""
    <div style="background: var(--bg_secondary); border-radius: 50px; height: 8px; overflow: hidden; margin: 1rem 0;">
        <div style="background: linear-gradient(90deg, {progress_color}, {progress_color}AA); height: 100%; width: {score}%; border-radius: 50px; transition: width 0.8s ease;"></div>
    </div>
    """
    
    st.markdown(f"""
    <div class="modern-card">
        <div style="display: flex; align-items: center; justify-content: between; margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center;">
                <i class="fas {status_icon}" style="color: {status_color}; margin-right: 0.75rem; font-size: 1.5rem;"></i>
                <div>
                    <h3 style="color: var(--text_primary); margin: 0; font-weight: 600;">Trợ lý Phân tích Thông minh</h3>
                    <p style="color: var(--text_secondary); margin: 0; font-size: 0.875rem;">Đánh giá tổng thể</p>
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 2rem; font-weight: 700; color: {status_color};">{score}</div>
                <div style="font-size: 0.875rem; color: var(--text_secondary);">/ 100</div>
            </div>
        </div>
        {progress_html}
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
            <div>
                <div style="font-size: 0.875rem; color: var(--text_secondary); margin-bottom: 0.25rem;">Trạng thái</div>
                <div style="font-weight: 600; color: {status_color};">{status}</div>
            </div>
            <div>
                <div style="font-size: 0.875rem; color: var(--text_secondary); margin-bottom: 0.25rem;">Gợi ý hệ thống</div>
                <div style="font-weight: 600; color: var(--text_primary);">{hint}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def create_loading_skeleton(card_count: int = 3, metric_count: int = 4):
    """Tạo skeleton loading cho trang"""

    # Header skeleton
    st.markdown("""
    <div class="loading-skeleton" style="height: 120px; margin-bottom: 2rem; border-radius: var(--radius-2xl);"></div>
    """, unsafe_allow_html=True)

    # Metrics skeleton
    cols = st.columns(metric_count)
    for col in cols:
        with col:
            st.markdown("""
            <div class="loading-skeleton skeleton-metric"></div>
            """, unsafe_allow_html=True)

    # Cards skeleton
    for _ in range(card_count):
        st.markdown("""
        <div class="loading-skeleton skeleton-card">
            <div class="loading-skeleton skeleton-text" style="width: 40%; margin-bottom: 1rem;"></div>
            <div class="loading-skeleton skeleton-text" style="width: 70%;"></div>
            <div class="loading-skeleton skeleton-text" style="width: 50%;"></div>
        </div>
        """, unsafe_allow_html=True)


def create_progress_indicator(current_step: int, total_steps: int, step_labels: list = None):
    """Tạo progress indicator cho multi-step processes"""
    if step_labels is None:
        step_labels = [f"Bước {i+1}" for i in range(total_steps)]

    progress_percentage = (current_step / total_steps) * 100

    progress_html = f"""
    <div style="margin-bottom: 2rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <span style="font-weight: 600; color: var(--text_primary);">Tiến độ phân tích</span>
            <span style="color: var(--text_secondary);">{current_step}/{total_steps}</span>
        </div>
        <div style="background: var(--bg_secondary); border-radius: 50px; height: 8px; overflow: hidden;">
            <div style="background: linear-gradient(90deg, var(--primary), var(--accent)); height: 100%; width: {progress_percentage}%; border-radius: 50px; transition: width 0.3s ease;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; margin-top: 0.5rem;">
    """

    for i, label in enumerate(step_labels):
        if i < current_step:
            color = "var(--success)"
            weight = "600"
        elif i == current_step:
            color = "var(--primary)"
            weight = "600"
        else:
            color = "var(--text_tertiary)"
            weight = "400"
        progress_html += f'<span style="font-size: 0.75rem; color: {color}; font-weight: {weight};">{label}</span>'

    progress_html += "</div></div>"

    st.markdown(progress_html, unsafe_allow_html=True)
