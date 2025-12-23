"""
Advanced UI Components Library for Stock Analyzer
Professional, modern components with sophisticated design
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
import html

from stock_analyzer.ui_advanced_styling import (
    ProfessionalColorSystem, 
    TypographySystem, 
    SpacingSystem,
    ShadowSystem,
    BorderRadiusSystem,
    apply_advanced_styling,
    create_premium_header,
    create_metric_card,
    create_status_badge,
    create_gradient_divider,
    get_professional_plotly_theme
)

# ============================================================================
# MODERN CARD COMPONENTS
# ============================================================================

def create_modern_card(
    content: str, 
    title: str = "", 
    card_type: str = "base",
    icon: str = "",
    badge: str = "",
    badge_type: str = "info"
) -> str:
    """Create a modern card component with professional styling"""
    
    card_classes = {
        "base": "card-base",
        "premium": "card-premium",
        "elevated": "card-elevated",
        "glass": "card-glass"
    }
    
    badge_html = f'<div class="card-badge">{create_status_badge(badge, badge_type)}</div>' if badge else ""
    
    title_html = f'<h3 class="text-heading-2" style="margin-bottom: var(--spacing-4);">{title}</h3>' if title else ""
    
    icon_html = f'<div class="card-icon" style="font-size: 2rem; margin-bottom: var(--spacing-3);">{icon}</div>' if icon else ""
    
    return f"""
    <div class="{card_classes.get(card_type, 'card-base')}">
        {badge_html}
        {icon_html}
        {title_html}
        <div class="card-content">
            {content}
        </div>
    </div>
    """

def create_hero_card(
    title: str, 
    subtitle: str = "", 
    primary_metric: str = "", 
    secondary_metric: str = "",
    trend: str = "",
    trend_type: str = "neutral"
) -> str:
    """Create a hero card for important metrics"""
    
    trend_colors = {
        "positive": "var(--color-success-400)",
        "negative": "var(--color-error-400)", 
        "neutral": "var(--color-neutral-400)"
    }
    
    trend_icon = "📈" if trend_type == "positive" else "📉" if trend_type == "negative" else "➡️"
    
    return f"""
    <div class="hero-card">
        <div class="hero-header">
            <h2 class="text-heading-1">{title}</h2>
            {f'<p class="text-body-large">{subtitle}</p>' if subtitle else ''}
        </div>
        <div class="hero-metrics">
            {f'<div class="hero-primary"><span class="primary-value">{primary_metric}</span></div>' if primary_metric else ''}
            {f'<div class="hero-secondary"><span class="secondary-value">{secondary_metric}</span></div>' if secondary_metric else ''}
            {f'<div class="hero-trend" style="color: {trend_colors[trend_type]};"><span class="trend-icon">{trend_icon}</span><span class="trend-value">{trend}</span></div>' if trend else ''}
        </div>
    </div>
    """

def create_stat_card(
    title: str,
    value: str,
    subtitle: str = "",
    change: str = "",
    change_type: str = "neutral",
    progress: Optional[float] = None,
    icon: str = ""
) -> str:
    """Create a statistical card with metrics and optional progress"""
    
    change_colors = {
        "positive": "var(--color-success-400)",
        "negative": "var(--color-error-400)",
        "neutral": "var(--color-neutral-400)"
    }
    
    icon_html = f'<div class="stat-icon">{icon}</div>' if icon else ""
    
    change_html = f'<div class="stat-change" style="color: {change_colors[change_type]};">{change}</div>' if change else ""
    
    progress_html = ""
    if progress is not None:
        progress_color = ProfessionalColorSystem.SUCCESS['600'] if progress > 0.5 else ProfessionalColorSystem.WARNING['600']
        progress_html = f'''
        <div class="stat-progress">
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress*100}%; background: {progress_color};"></div>
            </div>
            <span class="progress-text">{progress*100:.1f}%</span>
        </div>
        '''
    
    return f"""
    <div class="stat-card card-base">
        <div class="stat-header">
            {icon_html}
            <div class="stat-title">
                <h4 class="text-heading-3">{title}</h4>
                {f'<p class="text-body-small">{subtitle}</p>' if subtitle else ''}
            </div>
        </div>
        <div class="stat-value">
            <span class="text-heading-2">{value}</span>
            {change_html}
        </div>
        {progress_html}
    </div>
    """

# ============================================================================
# DATA VISUALIZATION COMPONENTS
# ============================================================================

def create_professional_chart(
    fig: go.Figure,
    title: str = "",
    height: int = 400,
    show_legend: bool = True
) -> None:
    """Create a professional chart with consistent styling"""
    
    # Apply professional theme
    fig.update_layout(**get_professional_plotly_theme())
    
    # Additional styling
    fig.update_layout(
        height=height,
        showlegend=show_legend,
        margin=dict(l=60, r=60, t=80, b=60),
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {
                'size': 18,
                'family': TypographySystem.FONTS['primary'],
                'color': 'white'
            }
        },
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(color='white', size=12)
        )
    )
    
    # Update axes
    fig.update_xaxes(
        gridcolor='rgba(255, 255, 255, 0.1)',
        linecolor='rgba(255, 255, 255, 0.3)',
        tickfont=dict(color='rgba(255, 255, 255, 0.8)', size=11),
        title_font=dict(color='rgba(255, 255, 255, 0.9)', size=13)
    )
    
    fig.update_yaxes(
        gridcolor='rgba(255, 255, 255, 0.1)',
        linecolor='rgba(255, 255, 255, 0.3)',
        tickfont=dict(color='rgba(255, 255, 255, 0.8)', size=11),
        title_font=dict(color='rgba(255, 255, 255, 0.9)', size=13)
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

def create_kpi_dashboard(
    kpis: List[Dict[str, Any]],
    columns: int = 4
) -> None:
    """Create a KPI dashboard with multiple metrics"""
    
    cols = st.columns(columns)
    
    for i, kpi in enumerate(kpis):
        col = cols[i % columns]
        with col:
            # Create KPI card
            change_type = kpi.get('change_type', 'neutral')
            change_color = {
                'positive': 'var(--color-success-400)',
                'negative': 'var(--color-error-400)',
                'neutral': 'var(--color-neutral-400)'
            }[change_type]
            
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-icon">{kpi.get('icon', '📊')}</span>
                    <h4 class="kpi-title">{kpi['title']}</h4>
                </div>
                <div class="kpi-value">
                    <span class="kpi-number">{kpi['value']}</span>
                    {f'<span class="kpi-change" style="color: {change_color};">{kpi["change"]}</span>' if kpi.get('change') else ''}
                </div>
                {f'<div class="kpi-subtitle">{kpi["subtitle"]}</div>' if kpi.get('subtitle') else ''}
            </div>
            """, unsafe_allow_html=True)

def create_data_table(
    data: pd.DataFrame,
    title: str = "",
    height: int = 400,
    use_container_width: bool = True,
    hide_index: bool = True
) -> None:
    """Create a professional data table"""
    
    if title:
        st.markdown(f"### {title}")
    
    # Apply styling to the dataframe
    styled_df = data.style.apply(lambda x: ['background-color: rgba(255, 255, 255, 0.05)' if i % 2 == 0 else 'background-color: rgba(255, 255, 255, 0.02)' for i in range(len(x))])
    
    st.dataframe(
        data,
        use_container_width=use_container_width,
        height=height,
        hide_index=hide_index
    )

def create_comparison_chart(
    df: pd.DataFrame,
    x_col: str,
    y_cols: List[str],
    chart_type: str = "line",
    title: str = ""
) -> None:
    """Create a comparison chart with professional styling"""
    
    colors = ProfessionalColorSystem()
    
    fig = go.Figure()
    
    # Color palette for multiple series
    series_colors = [
        colors.PRIMARY['400'],
        colors.SUCCESS['400'], 
        colors.WARNING['400'],
        colors.ERROR['400'],
        colors.NEUTRAL['400']
    ]
    
    for i, y_col in enumerate(y_cols):
        color = series_colors[i % len(series_colors)]
        
        if chart_type == "line":
            fig.add_trace(go.Scatter(
                x=df[x_col],
                y=df[y_col],
                mode='lines+markers',
                name=y_col,
                line=dict(color=color, width=3),
                marker=dict(size=6, color=color)
            ))
        elif chart_type == "bar":
            fig.add_trace(go.Bar(
                x=df[x_col],
                y=df[y_col],
                name=y_col,
                marker_color=color
            ))
    
    create_professional_chart(fig, title, height=450)

# ============================================================================
# NAVIGATION AND LAYOUT COMPONENTS  
# ============================================================================

def create_navigation_tabs(
    tabs: List[Dict[str, str]],
    active_tab: str = ""
) -> str:
    """Create a modern navigation tabs component"""
    
    tab_html = '<div class="nav-tabs">'
    
    for tab in tabs:
        is_active = tab['id'] == active_tab
        active_class = "nav-tab-active" if is_active else ""
        
        tab_html += f'''
        <button class="nav-tab {active_class}" onclick="switchTab('{tab['id']}')">
            <span class="nav-tab-icon">{tab['icon']}</span>
            <span class="nav-tab-text">{tab['label']}</span>
        </button>
        '''
    
    tab_html += '</div>'
    
    return tab_html

def create_breadcrumb(
    items: List[Dict[str, str]],
    current: str = ""
) -> str:
    """Create a breadcrumb navigation"""
    
    breadcrumb_html = '<nav class="breadcrumb"><ol class="breadcrumb-list">'
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        separator = '' if is_last else '<span class="breadcrumb-separator">/</span>'
        
        if is_last or item['id'] == current:
            breadcrumb_html += f'''
            <li class="breadcrumb-item breadcrumb-current">
                <span class="breadcrumb-text">{item['label']}</span>
            </li>
            '''
        else:
            breadcrumb_html += f'''
            <li class="breadcrumb-item">
                <a href="{item.get('href', '#')}" class="breadcrumb-link">{item['label']}</a>
                {separator}
            </li>
            '''
    
    breadcrumb_html += '</ol></nav>'
    
    return breadcrumb_html

def create_sidebar_section(
    title: str,
    content: str,
    collapsible: bool = True,
    expanded: bool = True,
    icon: str = ""
) -> str:
    """Create a collapsible sidebar section"""
    
    icon_html = f'<span class="section-icon">{icon}</span>' if icon else ""
    
    return f"""
    <div class="sidebar-section">
        <div class="section-header">
            {icon_html}
            <h3 class="section-title">{title}</h3>
            {f'<button class="section-toggle">▼</button>' if collapsible else ''}
        </div>
        <div class="section-content">
            {content}
        </div>
    </div>
    """

# ============================================================================
# INTERACTIVE ELEMENTS
# ============================================================================

def create_modern_button(
    label: str,
    button_type: str = "primary",
    size: str = "medium",
    icon: str = "",
    disabled: bool = False,
    full_width: bool = False
) -> str:
    """Create a modern button component"""
    
    button_classes = f"modern-btn modern-btn-{button_type} modern-btn-{size}"
    if full_width:
        button_classes += " modern-btn-full-width"
    if disabled:
        button_classes += " modern-btn-disabled"
    
    icon_html = f'<span class="btn-icon">{icon}</span>' if icon else ""
    
    return f'''
    <button class="{button_classes}" {'disabled' if disabled else ''}>
        {icon_html}
        <span class="btn-text">{label}</span>
    </button>
    '''

def create_input_group(
    label: str,
    input_type: str = "text",
    placeholder: str = "",
    value: str = "",
    icon: str = "",
    helper_text: str = "",
    error_text: str = "",
    required: bool = False
) -> str:
    """Create a modern input group component"""
    
    icon_html = f'<span class="input-icon">{icon}</span>' if icon else ""
    
    error_class = "input-error" if error_text else ""
    helper_class = "input-helper" if helper_text else ""
    
    return f'''
    <div class="input-group">
        <label class="input-label">
            {label}
            {'<span class="required-mark">*</span>' if required else ''}
        </label>
        <div class="input-wrapper {error_class}">
            {icon_html}
            <input 
                type="{input_type}" 
                class="modern-input" 
                placeholder="{placeholder}"
                value="{value}"
            />
        </div>
        {'<div class="input-helper-text">' + helper_text + '</div>' if helper_text else ''}
        {'<div class="input-error-text">' + error_text + '</div>' if error_text else ''}
    </div>
    '''

def create_select_group(
    label: str,
    options: List[str],
    selected: str = "",
    placeholder: str = "Select an option",
    icon: str = "",
    helper_text: str = ""
) -> str:
    """Create a modern select component"""
    
    icon_html = f'<span class="input-icon">{icon}</span>' if icon else ""
    
    options_html = ""
    for option in options:
        selected_attr = "selected" if option == selected else ""
        options_html += f'<option value="{option}" {selected_attr}>{option}</option>'
    
    return f'''
    <div class="input-group">
        <label class="input-label">{label}</label>
        <div class="input-wrapper">
            {icon_html}
            <select class="modern-select">
                <option value="" disabled selected>{placeholder}</option>
                {options_html}
            </select>
        </div>
        {'<div class="input-helper-text">' + helper_text + '</div>' if helper_text else ''}
    </div>
    '''

def create_toggle_switch(
    label: str,
    checked: bool = False,
    description: str = "",
    disabled: bool = False
) -> str:
    """Create a modern toggle switch"""
    
    checked_class = "toggle-checked" if checked else ""
    disabled_class = "toggle-disabled" if disabled else ""
    
    return f'''
    <div class="toggle-switch {checked_class} {disabled_class}">
        <div class="toggle-content">
            <span class="toggle-label">{label}</span>
            {f'<span class="toggle-description">{description}</span>' if description else ''}
        </div>
        <div class="toggle-track">
            <div class="toggle-thumb"></div>
        </div>
    </div>
    '''

def create_progress_ring(
    value: float,
    max_value: float = 100,
    size: str = "medium",
    color: str = "primary",
    show_text: bool = True
) -> str:
    """Create a circular progress indicator"""
    
    percentage = (value / max_value) * 100
    circumference = 2 * np.pi * 45  # radius = 45
    stroke_dasharray = circumference
    stroke_dashoffset = circumference - (percentage / 100) * circumference
    
    colors = {
        "primary": ProfessionalColorSystem.PRIMARY['500'],
        "success": ProfessionalColorSystem.SUCCESS['500'],
        "warning": ProfessionalColorSystem.WARNING['500'],
        "error": ProfessionalColorSystem.ERROR['500'],
        "neutral": ProfessionalColorSystem.NEUTRAL['500']
    }
    
    color_value = colors.get(color, colors["primary"])
    
    return f'''
    <div class="progress-ring progress-ring-{size}">
        <svg class="progress-ring-svg" width="120" height="120">
            <circle
                class="progress-ring-circle"
                stroke="rgba(255, 255, 255, 0.1)"
                stroke-width="8"
                fill="transparent"
                r="45"
                cx="60"
                cy="60"
            />
            <circle
                class="progress-ring-circle progress-ring-circle-progress"
                stroke="{color_value}"
                stroke-width="8"
                fill="transparent"
                r="45"
                cx="60"
                cy="60"
                stroke-dasharray="{stroke_dasharray}"
                stroke-dashoffset="{stroke_dashoffset}"
                style="transition: stroke-dashoffset 0.5s ease-in-out;"
            />
        </svg>
        {'<div class="progress-ring-text">' + f'{percentage:.1f}%</div>' if show_text else ''}
    </div>
    '''

# ============================================================================
# LAYOUT COMPONENTS
# ============================================================================

def create_grid_layout(
    content_items: List[str],
    columns: int = 3,
    gap: str = "medium"
) -> str:
    """Create a responsive grid layout"""
    
    grid_classes = f"grid-layout grid-{columns}col grid-gap-{gap}"
    
    items_html = ""
    for i, item in enumerate(content_items):
        items_html += f'<div class="grid-item grid-item-{i+1}">{item}</div>'
    
    return f'<div class="{grid_classes}">{items_html}</div>'

def create_flex_layout(
    content_items: List[str],
    direction: str = "row",
    justify: str = "start",
    align: str = "start",
    gap: str = "medium"
) -> str:
    """Create a flexible layout"""
    
    flex_classes = f"flex-layout flex-{direction} flex-justify-{justify} flex-align-{align} flex-gap-{gap}"
    
    items_html = ""
    for item in content_items:
        items_html += f'<div class="flex-item">{item}</div>'
    
    return f'<div class="{flex_classes}">{items_html}</div>'

def create_card_grid(
    cards: List[Dict[str, Any]],
    columns: int = 3
) -> None:
    """Create a grid of cards"""
    
    cols = st.columns(columns)
    
    for i, card in enumerate(cards):
        col = cols[i % columns]
        with col:
            card_type = card.get('type', 'base')
            st.markdown(create_modern_card(
                content=card['content'],
                title=card.get('title', ''),
                card_type=card_type,
                icon=card.get('icon', ''),
                badge=card.get('badge', ''),
                badge_type=card.get('badge_type', 'info')
            ), unsafe_allow_html=True)

# ============================================================================
# LOADING AND FEEDBACK COMPONENTS
# ============================================================================

def create_loading_skeleton(
    width: str = "100%",
    height: str = "20px",
    border_radius: str = "4px"
) -> str:
    """Create a loading skeleton"""
    
    return f'''
    <div class="skeleton" style="
        width: {width};
        height: {height};
        border-radius: {border_radius};
        background: linear-gradient(90deg, rgba(255,255,255,0.1) 25%, rgba(255,255,255,0.2) 50%, rgba(255,255,255,0.1) 75%);
        background-size: 200% 100%;
        animation: skeleton-loading 1.5s infinite;
    "></div>
    '''

def create_loading_card(
    title: str = "Loading...",
    lines: int = 3
) -> str:
    """Create a loading card with skeleton content"""
    
    lines_html = ""
    for _ in range(lines):
        lines_html += create_loading_skeleton(height="16px", border_radius="2px")
    
    return create_modern_card(
        content=f'''
        <h4 class="text-heading-3">{title}</h4>
        {lines_html}
        {create_loading_skeleton(height="60px")}
        ''',
        card_type="base"
    )

def create_success_message(
    message: str,
    title: str = "Success",
    icon: str = "✅"
) -> str:
    """Create a success message component"""
    
    return f'''
    <div class="message message-success">
        <div class="message-icon">{icon}</div>
        <div class="message-content">
            <h4 class="message-title">{title}</h4>
            <p class="message-text">{message}</p>
        </div>
    </div>
    '''

def create_error_message(
    message: str,
    title: str = "Error",
    icon: str = "❌"
) -> str:
    """Create an error message component"""
    
    return f'''
    <div class="message message-error">
        <div class="message-icon">{icon}</div>
        <div class="message-content">
            <h4 class="message-title">{title}</h4>
            <p class="message-text">{message}</p>
        </div>
    </div>
    '''

def create_warning_message(
    message: str,
    title: str = "Warning",
    icon: str = "⚠️"
) -> str:
    """Create a warning message component"""
    
    return f'''
    <div class="message message-warning">
        <div class="message-icon">{icon}</div>
        <div class="message-content">
            <h4 class="message-title">{title}</h4>
            <p class="message-text">{message}</p>
        </div>
    </div>
    '''

# ============================================================================
# ADVANCED FINANCIAL COMPONENTS
# ============================================================================

def create_price_display(
    price: float,
    change: Optional[float] = None,
    change_type: str = "neutral",
    currency: str = "VNĐ",
    size: str = "large"
) -> str:
    """Create a professional price display"""
    
    price_formatted = f"{price:,.2f}"
    
    change_html = ""
    if change is not None:
        change_formatted = f"{change:+.2f}"
        change_color = {
            "positive": "var(--color-success-400)",
            "negative": "var(--color-error-400)",
            "neutral": "var(--color-neutral-400)"
        }[change_type]
        
        change_icon = "▲" if change > 0 else "▼" if change < 0 else "●"
        change_html = f'<span class="price-change" style="color: {change_color};">{change_icon} {change_formatted}</span>'
    
    size_class = f"price-display-{size}"
    
    return f'''
    <div class="price-display {size_class}">
        <span class="price-value">{price_formatted}</span>
        <span class="price-currency">{currency}</span>
        {change_html}
    </div>
    '''

def create_portfolio_summary(
    total_value: float,
    day_change: float,
    total_return: float,
    positions_count: int
) -> str:
    """Create a portfolio summary card"""
    
    return create_hero_card(
        title="Portfolio Overview",
        subtitle=f"{positions_count} Positions",
        primary_metric=create_price_display(total_value, currency="VNĐ", size="large"),
        secondary_metric=f"Total Return: {total_return:+.2f}%",
        trend=f"Today: {day_change:+.2f}%",
        trend_type="positive" if day_change >= 0 else "negative"
    )

def create_risk_meter(
    risk_score: float,
    risk_level: str = "Medium",
    risk_color: str = "warning"
) -> str:
    """Create a risk assessment meter"""
    
    return f'''
    <div class="risk-meter">
        <div class="risk-header">
            <h4 class="risk-title">Risk Level</h4>
            <span class="risk-level risk-level-{risk_color}">{risk_level}</span>
        </div>
        <div class="risk-meter-visual">
            {create_progress_ring(risk_score, color=risk_color, show_text=False)}
            <span class="risk-score">{risk_score:.0f}</span>
        </div>
    </div>
    '''

# ============================================================================
# CSS STYLES FOR COMPONENTS
# ============================================================================

def get_component_css() -> str:
    """Get CSS styles for all components"""
    
    return f"""
    /* Hero Card Styles */
    .hero-card {{
        background: var(--gradient-primary);
        border-radius: var(--radius-premium);
        padding: var(--spacing-8);
        color: white;
        text-align: center;
        box-shadow: var(--shadow-premium);
        position: relative;
        overflow: hidden;
    }}
    
    .hero-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--gradient-premium);
    }}
    
    .hero-header {{
        margin-bottom: var(--spacing-6);
    }}
    
    .hero-header h2 {{
        margin: 0 0 var(--spacing-2) 0;
        color: white;
    }}
    
    .hero-metrics {{
        display: flex;
        justify-content: center;
        gap: var(--spacing-8);
        flex-wrap: wrap;
    }}
    
    .hero-primary .primary-value {{
        font-size: var(--font-size-5xl);
        font-weight: var(--font-weight-extrabold);
        display: block;
    }}
    
    .hero-secondary .secondary-value {{
        font-size: var(--font-size-xl);
        opacity: 0.8;
        display: block;
    }}
    
    .hero-trend {{
        display: flex;
        align-items: center;
        gap: var(--spacing-2);
        font-size: var(--font-size-lg);
        font-weight: var(--font-weight-semibold);
    }}
    
    /* Stat Card Styles */
    .stat-card {{
        height: 100%;
        display: flex;
        flex-direction: column;
    }}
    
    .stat-header {{
        display: flex;
        align-items: flex-start;
        gap: var(--spacing-3);
        margin-bottom: var(--spacing-4);
    }}
    
    .stat-icon {{
        font-size: 1.5rem;
        opacity: 0.8;
    }}
    
    .stat-title h4 {{
        margin: 0;
        color: var(--color-neutral-200);
    }}
    
    .stat-title p {{
        margin: var(--spacing-1) 0 0 0;
        color: var(--color-neutral-400);
        font-size: var(--font-size-sm);
    }}
    
    .stat-value {{
        margin-bottom: var(--spacing-3);
    }}
    
    .stat-value span {{
        color: white;
    }}
    
    .stat-change {{
        font-size: var(--font-size-sm);
        font-weight: var(--font-weight-medium);
        margin-top: var(--spacing-1);
    }}
    
    .stat-progress {{
        margin-top: auto;
        display: flex;
        align-items: center;
        gap: var(--spacing-3);
    }}
    
    .progress-bar {{
        flex: 1;
        height: 6px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: var(--radius-full);
        overflow: hidden;
    }}
    
    .progress-fill {{
        height: 100%;
        border-radius: var(--radius-full);
        transition: width 0.3s ease;
    }}
    
    .progress-text {{
        font-size: var(--font-size-xs);
        color: var(--color-neutral-400);
        min-width: 40px;
    }}
    
    /* Navigation Styles */
    .nav-tabs {{
        display: flex;
        gap: var(--spacing-1);
        background: rgba(255, 255, 255, 0.05);
        border-radius: var(--radius-lg);
        padding: var(--spacing-1);
        margin-bottom: var(--spacing-6);
    }}
    
    .nav-tab {{
        background: transparent;
        border: none;
        color: var(--color-neutral-400);
        padding: var(--spacing-3) var(--spacing-4);
        border-radius: var(--radius-md);
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: var(--spacing-2);
        font-size: var(--font-size-sm);
        font-weight: var(--font-weight-medium);
    }}
    
    .nav-tab:hover {{
        background: rgba(255, 255, 255, 0.1);
        color: var(--color-neutral-200);
    }}
    
    .nav-tab-active {{
        background: var(--gradient-primary);
        color: white;
        box-shadow: var(--shadow-md);
    }}
    
    /* Button Styles */
    .modern-btn {{
        background: var(--gradient-primary);
        border: none;
        border-radius: var(--radius-md);
        color: white;
        font-weight: var(--font-weight-semibold);
        padding: var(--spacing-3) var(--spacing-6);
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: var(--spacing-2);
        font-size: var(--font-size-sm);
    }}
    
    .modern-btn:hover {{
        transform: translateY(-1px);
        box-shadow: var(--shadow-lg);
        filter: brightness(1.1);
    }}
    
    .modern-btn-secondary {{
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }}
    
    .modern-btn-secondary:hover {{
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.3);
    }}
    
    .modern-btn-small {{
        padding: var(--spacing-2) var(--spacing-4);
        font-size: var(--font-size-xs);
    }}
    
    .modern-btn-large {{
        padding: var(--spacing-4) var(--spacing-8);
        font-size: var(--font-size-base);
    }}
    
    .modern-btn-full-width {{
        width: 100%;
    }}
    
    .modern-btn-disabled {{
        opacity: 0.5;
        cursor: not-allowed;
        transform: none;
    }}
    
    /* Input Styles */
    .input-group {{
        margin-bottom: var(--spacing-4);
    }}
    
    .input-label {{
        display: block;
        color: var(--color-neutral-200);
        font-size: var(--font-size-sm);
        font-weight: var(--font-weight-medium);
        margin-bottom: var(--spacing-2);
    }}
    
    .required-mark {{
        color: var(--color-error-400);
        margin-left: var(--spacing-1);
    }}
    
    .input-wrapper {{
        position: relative;
        display: flex;
        align-items: center;
    }}
    
    .input-icon {{
        position: absolute;
        left: var(--spacing-3);
        color: var(--color-neutral-400);
        font-size: var(--font-size-sm);
        z-index: 1;
    }}
    
    .modern-input {{
        width: 100%;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: var(--radius-md);
        color: var(--color-neutral-100);
        padding: var(--spacing-3) var(--spacing-4);
        font-size: var(--font-size-sm);
        transition: all 0.3s ease;
    }}
    
    .modern-input:focus {{
        outline: none;
        border-color: var(--color-primary-400);
        box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1);
        background: rgba(255, 255, 255, 0.08);
    }}
    
    .input-wrapper.input-error {{
        border-color: var(--color-error-400);
    }}
    
    .input-helper-text {{
        color: var(--color-neutral-400);
        font-size: var(--font-size-xs);
        margin-top: var(--spacing-1);
    }}
    
    .input-error-text {{
        color: var(--color-error-400);
        font-size: var(--font-size-xs);
        margin-top: var(--spacing-1);
    }}
    
    /* Toggle Switch Styles */
    .toggle-switch {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--spacing-3) 0;
        cursor: pointer;
    }}
    
    .toggle-content {{
        flex: 1;
    }}
    
    .toggle-label {{
        color: var(--color-neutral-200);
        font-size: var(--font-size-sm);
        font-weight: var(--font-weight-medium);
        display: block;
    }}
    
    .toggle-description {{
        color: var(--color-neutral-400);
        font-size: var(--font-size-xs);
        margin-top: var(--spacing-1);
        display: block;
    }}
    
    .toggle-track {{
        width: 44px;
        height: 24px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: var(--radius-full);
        position: relative;
        transition: all 0.3s ease;
    }}
    
    .toggle-thumb {{
        width: 20px;
        height: 20px;
        background: white;
        border-radius: var(--radius-full);
        position: absolute;
        top: 2px;
        left: 2px;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-sm);
    }}
    
    .toggle-checked .toggle-track {{
        background: var(--gradient-primary);
    }}
    
    .toggle-checked .toggle-thumb {{
        transform: translateX(20px);
    }}
    
    .toggle-disabled {{
        opacity: 0.5;
        cursor: not-allowed;
    }}
    
    /* Progress Ring Styles */
    .progress-ring {{
        position: relative;
        display: inline-block;
    }}
    
    .progress-ring-svg {{
        transform: rotate(-90deg);
    }}
    
    .progress-ring-circle {{
        transition: stroke-dashoffset 0.5s ease-in-out;
    }}
    
    .progress-ring-text {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: var(--color-neutral-200);
        font-weight: var(--font-weight-semibold);
        font-size: var(--font-size-sm);
    }}
    
    /* Message Styles */
    .message {{
        display: flex;
        align-items: flex-start;
        gap: var(--spacing-3);
        padding: var(--spacing-4);
        border-radius: var(--radius-lg);
        margin-bottom: var(--spacing-4);
    }}
    
    .message-success {{
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.3);
        color: var(--color-success-200);
    }}
    
    .message-error {{
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        color: var(--color-error-200);
    }}
    
    .message-warning {{
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        color: var(--color-warning-200);
    }}
    
    .message-icon {{
        font-size: var(--font-size-lg);
        margin-top: var(--spacing-1);
    }}
    
    .message-title {{
        margin: 0 0 var(--spacing-1) 0;
        font-size: var(--font-size-sm);
        font-weight: var(--font-weight-semibold);
    }}
    
    .message-text {{
        margin: 0;
        font-size: var(--font-size-sm);
        opacity: 0.9;
    }}
    
    /* Price Display Styles */
    .price-display {{
        display: flex;
        align-items: baseline;
        gap: var(--spacing-2);
    }}
    
    .price-display-large .price-value {{
        font-size: var(--font-size-4xl);
        font-weight: var(--font-weight-extrabold);
        color: white;
    }}
    
    .price-display-medium .price-value {{
        font-size: var(--font-size-2xl);
        font-weight: var(--font-weight-bold);
        color: white;
    }}
    
    .price-display-small .price-value {{
        font-size: var(--font-size-lg);
        font-weight: var(--font-weight-semibold);
        color: white;
    }}
    
    .price-currency {{
        color: var(--color-neutral-400);
        font-size: var(--font-size-sm);
    }}
    
    .price-change {{
        font-size: var(--font-size-sm);
        font-weight: var(--font-weight-medium);
        margin-left: var(--spacing-2);
    }}
    
    /* Risk Meter Styles */
    .risk-meter {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: var(--radius-lg);
        padding: var(--spacing-4);
    }}
    
    .risk-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: var(--spacing-4);
    }}
    
    .risk-title {{
        color: var(--color-neutral-200);
        font-size: var(--font-size-sm);
        font-weight: var(--font-weight-medium);
        margin: 0;
    }}
    
    .risk-level {{
        padding: var(--spacing-1) var(--spacing-3);
        border-radius: var(--radius-full);
        font-size: var(--font-size-xs);
        font-weight: var(--font-weight-medium);
    }}
    
    .risk-level-success {{
        background: var(--color-success-500);
        color: white;
    }}
    
    .risk-level-warning {{
        background: var(--color-warning-500);
        color: white;
    }}
    
    .risk-level-error {{
        background: var(--color-error-500);
        color: white;
    }}
    
    .risk-meter-visual {{
        position: relative;
        display: flex;
        justify-content: center;
    }}
    
    .risk-score {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: var(--color-neutral-200);
        font-weight: var(--font-weight-semibold);
        font-size: var(--font-size-lg);
    }}
    
    /* Skeleton Loading Animation */
    @keyframes skeleton-loading {{
        0% {{
            background-position: -200px 0;
        }}
        100% {{
            background-position: calc(200px + 100%) 0;
        }}
    }}
    
    /* Grid Layout */
    .grid-layout {{
        display: grid;
        gap: var(--spacing-4);
    }}
    
    .grid-1col {{ grid-template-columns: 1fr; }}
    .grid-2col {{ grid-template-columns: repeat(2, 1fr); }}
    .grid-3col {{ grid-template-columns: repeat(3, 1fr); }}
    .grid-4col {{ grid-template-columns: repeat(4, 1fr); }}
    
    @media (max-width: 768px) {{
        .grid-4col {{ grid-template-columns: repeat(2, 1fr); }}
        .grid-3col {{ grid-template-columns: repeat(2, 1fr); }}
        .grid-2col {{ grid-template-columns: 1fr; }}
    }}
    
    .grid-gap-small {{ gap: var(--spacing-2); }}
    .grid-gap-medium {{ gap: var(--spacing-4); }}
    .grid-gap-large {{ gap: var(--spacing-6); }}
    
    /* Flex Layout */
    .flex-layout {{
        display: flex;
    }}
    
    .flex-row {{ flex-direction: row; }}
    .flex-column {{ flex-direction: column; }}
    
    .flex-justify-start {{ justify-content: flex-start; }}
    .flex-justify-center {{ justify-content: center; }}
    .flex-justify-end {{ justify-content: flex-end; }}
    .flex-justify-between {{ justify-content: space-between; }}
    .flex-justify-around {{ justify-content: space-around; }}
    
    .flex-align-start {{ align-items: flex-start; }}
    .flex-align-center {{ align-items: center; }}
    .flex-align-end {{ align-items: flex-end; }}
    
    .flex-gap-small {{ gap: var(--spacing-2); }}
    .flex-gap-medium {{ gap: var(--spacing-4); }}
    .flex-gap-large {{ gap: var(--spacing-6); }}
    
    /* Responsive Adjustments */
    @media (max-width: 768px) {{
        .hero-metrics {{
            flex-direction: column;
            gap: var(--spacing-4);
        }}
        
        .nav-tabs {{
            flex-direction: column;
        }}
        
        .price-display-large .price-value {{
            font-size: var(--font-size-2xl);
        }}
    }}
    """

# Apply the component styles
def apply_component_styles():
    """Apply all component styles to the page"""
    css = get_component_css()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Export all components
__all__ = [
    'create_modern_card',
    'create_hero_card', 
    'create_stat_card',
    'create_professional_chart',
    'create_kpi_dashboard',
    'create_data_table',
    'create_comparison_chart',
    'create_navigation_tabs',
    'create_breadcrumb',
    'create_sidebar_section',
    'create_modern_button',
    'create_input_group',
    'create_select_group',
    'create_toggle_switch',
    'create_progress_ring',
    'create_grid_layout',
    'create_flex_layout',
    'create_card_grid',
    'create_loading_skeleton',
    'create_loading_card',
    'create_success_message',
    'create_error_message',
    'create_warning_message',
    'create_price_display',
    'create_portfolio_summary',
    'create_risk_meter',
    'apply_component_styles'
]