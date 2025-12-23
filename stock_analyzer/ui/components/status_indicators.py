"""
Accessible status indicators với multiple visual cues
Hỗ trợ người khiếm thị màu với patterns và icons

Author: Roo - Architect Mode
Version: 1.0.0
"""

import streamlit as st
from typing import Dict, Optional
from enum import Enum

class StatusType(Enum):
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    INFO = "info"

class StatusIndicator:
    """Accessible status indicator với multiple visual cues"""
    
    def __init__(self):
        self.status_config = {
            StatusType.SUCCESS: {
                'icon': '✓',
                'text': 'Success',
                'bg_color': 'var(--success)',
                'text_color': 'white',
                'pattern': 'linear-gradient(45deg, transparent 49%, rgba(255,255,255,0.3) 49%, rgba(255,255,255,0.3) 51%, transparent 51%)',
                'aria_label': 'Success status - positive result'
            },
            StatusType.WARNING: {
                'icon': '⚠',
                'text': 'Warning',
                'bg_color': 'var(--warning)',
                'text_color': 'white',
                'pattern': 'repeating-linear-gradient(45deg, transparent, transparent 5px, rgba(255,255,255,0.3) 5px, rgba(255,255,255,0.3) 10px)',
                'aria_label': 'Warning status - caution needed'
            },
            StatusType.ERROR: {
                'icon': '✗',
                'text': 'Error',
                'bg_color': 'var(--error)',
                'text_color': 'white',
                'pattern': 'radial-gradient(circle, rgba(255,255,255,0.3) 20%, transparent 20%)',
                'aria_label': 'Error status - negative result'
            },
            StatusType.INFO: {
                'icon': 'ℹ',
                'text': 'Information',
                'bg_color': 'var(--info)',
                'text_color': 'white',
                'pattern': 'linear-gradient(90deg, transparent 50%, rgba(255,255,255,0.3) 50%)',
                'aria_label': 'Information status - informational message'
            }
        }
    
    def render_status_badge(
        self,
        status: StatusType,
        message: str = "",
        show_icon: bool = True,
        show_text: bool = True,
        show_pattern: bool = True,
        size: str = "medium"
    ) -> str:
        """Render accessible status badge"""
        
        config = self.status_config[status]
        
        # Size configurations
        size_configs = {
            "small": {"padding": "0.25rem 0.5rem", "font_size": "0.75rem"},
            "medium": {"padding": "0.5rem 1rem", "font_size": "0.875rem"},
            "large": {"padding": "0.75rem 1.5rem", "font_size": "1rem"}
        }
        
        size_config = size_configs.get(size, size_configs["medium"])
        
        # Build badge HTML
        icon_html = f'<span class="status-icon" aria-hidden="true">{config["icon"]}</span>' if show_icon else ""
        text_html = f'<span class="status-text">{config["text"]} {message}</span>' if show_text else ""
        pattern_html = f'<div class="status-pattern" aria-hidden="true"></div>' if show_pattern else ""
        
        badge_html = f"""
        <div 
            class="status-badge status-{status.value}"
            role="status"
            aria-label="{config['aria_label']}"
            style="
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                padding: {size_config['padding']};
                border-radius: 0.5rem;
                font-weight: 600;
                font-size: {size_config['font_size']};
                background-color: {config['bg_color']};
                color: {config['text_color']};
                border: 2px solid {config['bg_color']};
                position: relative;
                overflow: hidden;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            "
        >
            {pattern_html}
            {icon_html}
            {text_html}
        </div>
        
        <style>
        .status-badge {{
            transition: all 0.2s ease;
            cursor: pointer;
        }}
        
        .status-badge:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }}
        
        .status-pattern {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            opacity: 0.3;
            pointer-events: none;
            background: {config['pattern']};
            background-size: 8px 8px;
        }}
        
        .status-icon {{
            font-weight: bold;
            font-size: 1.2em;
        }}
        
        .status-text {{
            font-weight: 600;
        }}
        
        /* Colorblind support */
        .status-{status.value}::after {{
            content: "";
            position: absolute;
            top: 2px;
            right: 2px;
            width: 8px;
            height: 8px;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 50%;
        }}
        </style>
        """
        
        return badge_html
    
    def render_trend_indicator(
        self,
        value: float,
        previous_value: float,
        format_type: str = "percentage"
    ) -> str:
        """Render trend indicator với accessibility"""
        
        change = value - previous_value
        is_positive = change > 0
        is_negative = change < 0
        
        # Format change value
        if format_type == "percentage":
            change_text = f"{change:+.1f}%"
            change_value = f"{(change / previous_value) * 100:.1f}%"
        else:
            change_text = f"{change:+.2f}"
            change_value = f"{value:.2f}"
        
        # Choose icon and colors
        if is_positive:
            icon = "↗"
            color = "var(--success)"
            aria_label = "Upward trend"
        elif is_negative:
            icon = "↘"
            color = "var(--error)"
            aria_label = "Downward trend"
        else:
            icon = "→"
            color = "var(--neutral)"
            aria_label = "No change"
        
        trend_html = f"""
        <div 
            class="trend-indicator"
            role="img"
            aria-label="{aria_label}: {change_text} from {previous_value} to {value}"
            style="
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                padding: 0.5rem 1rem;
                border-radius: 0.5rem;
                font-weight: 600;
                color: {color};
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid {color};
            "
        >
            <span class="trend-icon" aria-hidden="true">{icon}</span>
            <span class="trend-text">{change_text}</span>
            <span class="sr-only">Change from {previous_value} to {value}</span>
        </div>
        
        <style>
        .trend-indicator {{
            transition: all 0.2s ease;
        }}
        
        .trend-icon {{
            font-size: 1.2em;
            font-weight: bold;
        }}
        
        .trend-text {{
            font-family: 'Courier New', monospace;
        }}
        </style>
        """
        
        return trend_html

def create_accessible_metric_card(
    title: str,
    value: str,
    change: Optional[float] = None,
    previous_value: Optional[float] = None,
    status: Optional[StatusType] = None,
    description: str = "",
    key: Optional[str] = None
) -> str:
    """Tạo accessible metric card"""
    
    # Generate unique key if not provided
    if key is None:
        key = f"metric_{hash(title + value)}"
    
    # Status indicator
    status_html = ""
    if status:
        indicator = StatusIndicator()
        status_html = indicator.render_status_badge(status, size="small")
    
    # Trend indicator
    trend_html = ""
    if change is not None and previous_value is not None:
        indicator = StatusIndicator()
        trend_html = indicator.render_trend_indicator(value, previous_value)
    
    # Description for screen readers
    description_id = f"{key}_desc"
    aria_description = f'aria-describedby="{description_id}"' if description else ""
    
    card_html = f"""
    <div 
        class="metric-card"
        id="{key}"
        role="region"
        aria-labelledby="{key}_title"
        {aria_description}
        style="
            background: var(--bg_primary);
            border: 1px solid var(--border_primary);
            border-radius: 0.75rem;
            padding: 1.5rem;
            margin: 0.5rem 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            transition: all 0.2s ease;
        "
        onmouseover="this.style.boxShadow='0 4px 8px rgba(0, 0, 0, 0.15)'"
        onmouseout="this.style.boxShadow='0 2px 4px rgba(0, 0, 0, 0.1)'"
    >
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
            <h3 
                id="{key}_title"
                style="
                    margin: 0;
                    font-size: 1rem;
                    font-weight: 600;
                    color: var(--text_secondary);
                "
            >
                {title}
            </h3>
            {status_html}
        </div>
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div 
                    style="
                        font-size: 2rem;
                        font-weight: 700;
                        color: var(--text_primary);
                        line-height: 1;
                        margin-bottom: 0.5rem;
                    "
                >
                    {value}
                </div>
                {trend_html}
            </div>
        </div>
        
        {f'<div id="{description_id}" class="sr-only">{description}</div>' if description else ''}
    </div>
    
    <style>
    .metric-card:focus-within {{
        outline: 2px solid var(--interactive_focus);
        outline-offset: 2px;
    }}
    </style>
    """
    
    return card_html

def render_accessibility_status_panel():
    """Render a panel showing accessibility features status"""
    st.markdown("### ♿ Accessibility Features Status")
    
    # Check current accessibility settings
    settings = {
        'Theme': st.session_state.get('theme_preference', 'light'),
        'Colorblind Mode': 'Enabled' if st.session_state.get('colorblind_mode', False) else 'Disabled',
        'High Contrast': 'Enabled' if st.session_state.get('high_contrast', False) else 'Disabled',
        'Reduced Motion': 'Enabled' if st.session_state.get('reduced_motion', False) else 'Disabled',
        'Font Size': st.session_state.get('font_size', 'Medium')
    }
    
    # Create status indicators for each setting
    for setting, value in settings.items():
        if setting == 'Theme':
            status = StatusType.SUCCESS if value in ['light', 'dark', 'auto'] else StatusType.ERROR
        elif 'Enabled' in str(value):
            status = StatusType.SUCCESS
        elif 'Disabled' in str(value):
            status = StatusType.INFO
        else:
            status = StatusType.INFO
        
        indicator = StatusIndicator()
        badge_html = indicator.render_status_badge(
            status=status,
            message=f"{setting}: {value}",
            size="small"
        )
        st.markdown(badge_html, unsafe_allow_html=True)