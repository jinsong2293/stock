"""
Advanced Chart Components for Stock Analyzer
Professional data visualization with enhanced interactivity
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import plotly.subplots as sp
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
import math

from stock_analyzer.ui_advanced_styling import (
    ProfessionalColorSystem, 
    TypographySystem, 
    SpacingSystem,
    ShadowSystem,
    get_professional_plotly_theme
)

# ============================================================================
# PROFESSIONAL CHART THEMES
# ============================================================================

class AdvancedChartThemes:
    """Advanced chart themes for financial data visualization"""
    
    colors = ProfessionalColorSystem()
    
    @staticmethod
    def get_candlestick_theme() -> Dict[str, Any]:
        """Get professional candlestick chart theme"""
        return {
            'layout': {
                'xaxis': {
                    'showgrid': True,
                    'gridcolor': 'rgba(255, 255, 255, 0.1)',
                    'gridwidth': 1,
                    'linecolor': 'rgba(255, 255, 255, 0.3)',
                    'tickcolor': 'rgba(255, 255, 255, 0.3)',
                    'tickfont': {'color': 'rgba(255, 255, 255, 0.8)', 'size': 11},
                    'title_font': {'color': 'rgba(255, 255, 255, 0.9)', 'size': 13},
                },
                'yaxis': {
                    'showgrid': True,
                    'gridcolor': 'rgba(255, 255, 255, 0.1)',
                    'gridwidth': 1,
                    'linecolor': 'rgba(255, 255, 255, 0.3)',
                    'tickcolor': 'rgba(255, 255, 255, 0.3)',
                    'tickfont': {'color': 'rgba(255, 255, 255, 0.8)', 'size': 11},
                    'title_font': {'color': 'rgba(255, 255, 255, 0.9)', 'size': 13},
                },
                'paper_bgcolor': 'rgba(0,0,0,0)',
                'plot_bgcolor': 'rgba(0,0,0,0)',
                'font': {
                    'family': TypographySystem.FONTS['primary'],
                    'size': 12,
                    'color': 'white'
                },
                'margin': {'l': 60, 'r': 60, 't': 80, 'b': 60}
            }
        }
    
    @staticmethod
    def get_volume_theme() -> Dict[str, Any]:
        """Get professional volume chart theme"""
        return {
            'layout': {
                'xaxis': {
                    'showgrid': False,
                    'linecolor': 'rgba(255, 255, 255, 0.3)',
                    'tickcolor': 'rgba(255, 255, 255, 0.3)',
                    'tickfont': {'color': 'rgba(255, 255, 255, 0.8)', 'size': 10},
                },
                'yaxis': {
                    'showgrid': True,
                    'gridcolor': 'rgba(255, 255, 255, 0.1)',
                    'linecolor': 'rgba(255, 255, 255, 0.3)',
                    'tickcolor': 'rgba(255, 255, 255, 0.3)',
                    'tickfont': {'color': 'rgba(255, 255, 255, 0.8)', 'size': 10},
                    'title_font': {'color': 'rgba(255, 255, 255, 0.9)', 'size': 12},
                },
                'paper_bgcolor': 'rgba(0,0,0,0)',
                'plot_bgcolor': 'rgba(0,0,0,0)',
                'font': {
                    'family': TypographySystem.FONTS['primary'],
                    'size': 10,
                    'color': 'white'
                },
                'margin': {'l': 40, 'r': 40, 't': 20, 'b': 40}
            }
        }

# ============================================================================
# CANDLESTICK CHARTS
# ============================================================================

def create_professional_candlestick(
    data: pd.DataFrame,
    title: str = "Candlestick Chart",
    show_volume: bool = True,
    show_ma: bool = True,
    ma_periods: List[int] = [20, 50],
    height: int = 600
) -> go.Figure:
    """Create a professional candlestick chart"""
    
    fig = sp.make_subplots(
        rows=2 if show_volume else 1,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        subplot_titles=('Price', 'Volume') if show_volume else ('Price',),
        row_heights=[0.7, 0.3] if show_volume else [1]
    )
    
    # Add candlestick
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='OHLC',
            increasing_line_color=AdvancedChartThemes.colors.SUCCESS['400'],
            decreasing_line_color=AdvancedChartThemes.colors.ERROR['400'],
            increasing_fillcolor=AdvancedChartThemes.colors.SUCCESS['600'],
            decreasing_fillcolor=AdvancedChartThemes.colors.ERROR['600'],
        ),
        row=1, col=1
    )
    
    # Add moving averages
    if show_ma:
        for period in ma_periods:
            ma_col = f'MA_{period}'
            if ma_col in data.columns:
                fig.add_trace(
                    go.Scatter(
                        x=data.index,
                        y=data[ma_col],
                        mode='lines',
                        name=f'MA{period}',
                        line=dict(
                            width=2,
                            color=AdvancedChartThemes.colors.PRIMARY['400'] if period == ma_periods[0] 
                            else AdvancedChartThemes.colors.WARNING['400']
                        ),
                        opacity=0.8
                    ),
                    row=1, col=1
                )
    
    # Add volume bars
    if show_volume and 'Volume' in data.columns:
        colors = [AdvancedChartThemes.colors.SUCCESS['400'] if close >= open else AdvancedChartThemes.colors.ERROR['400'] 
                 for close, open in zip(data['Close'], data['Open'])]
        
        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data['Volume'],
                name='Volume',
                marker_color=colors,
                opacity=0.7,
                yaxis='y2'
            ),
            row=2, col=1
        )
    
    # Apply themes
    fig.update_layout(**AdvancedChartThemes.get_candlestick_theme())
    if show_volume:
        fig.update_layout(**AdvancedChartThemes.get_volume_theme())
    
    # Update layout
    fig.update_layout(
        height=height,
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
            y=-0.15 if show_volume else -0.1,
            xanchor="center",
            x=0.5,
            font=dict(color='white', size=12)
        ),
        margin=dict(l=60, r=60, t=80, b=80 if show_volume else 60)
    )
    
    return fig

# ============================================================================
# TECHNICAL INDICATOR CHARTS
# ============================================================================

def create_rsi_chart(
    data: pd.DataFrame,
    title: str = "RSI (Relative Strength Index)",
    period: int = 14,
    height: int = 300
) -> go.Figure:
    """Create a professional RSI chart"""
    
    fig = go.Figure()
    
    # RSI line
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['RSI'],
            mode='lines',
            name='RSI',
            line=dict(
                color=AdvancedChartThemes.colors.WARNING['400'],
                width=2
            ),
            fill='tonexty' if 'RSI_Upper' in data.columns else None,
            fillcolor='rgba(245, 158, 11, 0.1)' if 'RSI_Upper' in data.columns else None
        )
    )
    
    # RSI bands if available
    if 'RSI_Upper' in data.columns and 'RSI_Lower' in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['RSI_Upper'],
                mode='lines',
                name='Overbought (70)',
                line=dict(
                    color=AdvancedChartThemes.colors.ERROR['400'],
                    width=1,
                    dash='dash'
                ),
                showlegend=True
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['RSI_Lower'],
                mode='lines',
                name='Oversold (30)',
                line=dict(
                    color=AdvancedChartThemes.colors.SUCCESS['400'],
                    width=1,
                    dash='dash'
                ),
                fill='tonexty',
                fillcolor='rgba(34, 197, 94, 0.1)',
                showlegend=True
            )
        )
    
    # Add reference lines
    fig.add_hline(y=70, line_dash="dash", line_color=AdvancedChartThemes.colors.ERROR['600'], 
                  annotation_text="Overbought", annotation_position="top right")
    fig.add_hline(y=30, line_dash="dash", line_color=AdvancedChartThemes.colors.SUCCESS['600'], 
                  annotation_text="Oversold", annotation_position="bottom right")
    
    # Add shaded regions
    fig.add_hrect(y0=70, y1=100, fillcolor=AdvancedChartThemes.colors.ERROR['500'], opacity=0.1, layer="below")
    fig.add_hrect(y0=0, y1=30, fillcolor=AdvancedChartThemes.colors.SUCCESS['500'], opacity=0.1, layer="below")
    
    # Update layout
    fig.update_layout(
        height=height,
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {
                'size': 16,
                'family': TypographySystem.FONTS['primary'],
                'color': 'white'
            }
        },
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='rgba(255, 255, 255, 0.3)',
            tickfont={'color': 'rgba(255, 255, 255, 0.8)', 'size': 10},
            title_font={'color': 'rgba(255, 255, 255, 0.9)', 'size': 12}
        ),
        yaxis=dict(
            range=[0, 100],
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='rgba(255, 255, 255, 0.3)',
            tickfont={'color': 'rgba(255, 255, 255, 0.8)', 'size': 10},
            title_font={'color': 'rgba(255, 255, 255, 0.9)', 'size': 12}
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': TypographySystem.FONTS['primary'], 'size': 10, 'color': 'white'},
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
            font=dict(color='white', size=10)
        )
    )
    
    return fig

def create_macd_chart(
    data: pd.DataFrame,
    title: str = "MACD (Moving Average Convergence Divergence)",
    height: int = 350
) -> go.Figure:
    """Create a professional MACD chart"""
    
    fig = go.Figure()
    
    # MACD line
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['MACD'],
            mode='lines',
            name='MACD',
            line=dict(
                color=AdvancedChartThemes.colors.PRIMARY['400'],
                width=2
            )
        )
    )
    
    # Signal line
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['MACD_Signal'],
            mode='lines',
            name='Signal',
            line=dict(
                color=AdvancedChartThemes.colors.WARNING['400'],
                width=2
            )
        )
    )
    
    # MACD histogram
    colors = [AdvancedChartThemes.colors.SUCCESS['400'] if val >= 0 else AdvancedChartThemes.colors.ERROR['400'] 
             for val in data['MACD_Hist']]
    
    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data['MACD_Hist'],
            name='Histogram',
            marker_color=colors,
            opacity=0.6
        )
    )
    
    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color='rgba(255, 255, 255, 0.3)', line_width=1)
    
    # Update layout
    fig.update_layout(
        height=height,
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {
                'size': 16,
                'family': TypographySystem.FONTS['primary'],
                'color': 'white'
            }
        },
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='rgba(255, 255, 255, 0.3)',
            tickfont={'color': 'rgba(255, 255, 255, 0.8)', 'size': 10},
            title_font={'color': 'rgba(255, 255, 255, 0.9)', 'size': 12}
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='rgba(255, 255, 255, 0.3)',
            tickfont={'color': 'rgba(255, 255, 255, 0.8)', 'size': 10},
            title_font={'color': 'rgba(255, 255, 255, 0.9)', 'size': 12}
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': TypographySystem.FONTS['primary'], 'size': 10, 'color': 'white'},
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
            font=dict(color='white', size=10)
        )
    )
    
    return fig

# ============================================================================
# BOLLINGER BANDS CHART
# ============================================================================

def create_bollinger_bands_chart(
    data: pd.DataFrame,
    title: str = "Bollinger Bands",
    height: int = 400
) -> go.Figure:
    """Create a professional Bollinger Bands chart"""
    
    fig = go.Figure()
    
    # Price line
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['Close'],
            mode='lines',
            name='Close Price',
            line=dict(
                color=AdvancedChartThemes.colors.NEUTRAL['200'],
                width=2
            )
        )
    )
    
    # Bollinger Bands
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['BB_Upper'],
            mode='lines',
            name='Upper Band',
            line=dict(
                color=AdvancedChartThemes.colors.ERROR['400'],
                width=1,
                dash='dash'
            )
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['BB_Lower'],
            mode='lines',
            name='Lower Band',
            line=dict(
                color=AdvancedChartThemes.colors.SUCCESS['400'],
                width=1,
                dash='dash'
            ),
            fill='tonexty',
            fillcolor='rgba(255, 255, 255, 0.05)'
        )
    )
    
    # Middle band (SMA)
    if 'BB_Middle' in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['BB_Middle'],
                mode='lines',
                name='Middle Band (SMA)',
                line=dict(
                    color=AdvancedChartThemes.colors.WARNING['400'],
                    width=1
                ),
                opacity=0.7
            )
        )
    
    # Update layout
    fig.update_layout(
        height=height,
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {
                'size': 16,
                'family': TypographySystem.FONTS['primary'],
                'color': 'white'
            }
        },
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='rgba(255, 255, 255, 0.3)',
            tickfont={'color': 'rgba(255, 255, 255, 0.8)', 'size': 10},
            title_font={'color': 'rgba(255, 255, 255, 0.9)', 'size': 12}
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='rgba(255, 255, 255, 0.3)',
            tickfont={'color': 'rgba(255, 255, 255, 0.8)', 'size': 10},
            title_font={'color': 'rgba(255, 255, 255, 0.9)', 'size': 12}
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': TypographySystem.FONTS['primary'], 'size': 10, 'color': 'white'},
        margin=dict(l=60, r=60, t=60, b=60),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(color='white', size=10)
        )
    )
    
    return fig

# ============================================================================
# VOLUME ANALYSIS CHARTS
# ============================================================================

def create_volume_profile_chart(
    data: pd.DataFrame,
    title: str = "Volume Profile",
    height: int = 300
) -> go.Figure:
    """Create a professional volume profile chart"""
    
    fig = go.Figure()
    
    # Volume bars with price-based coloring
    colors = []
    for i, (close, open_price, volume) in enumerate(zip(data['Close'], data['Open'], data['Volume'])):
        if close > open_price:
            colors.append(AdvancedChartThemes.colors.SUCCESS['400'])
        elif close < open_price:
            colors.append(AdvancedChartThemes.colors.ERROR['400'])
        else:
            colors.append(AdvancedChartThemes.colors.NEUTRAL['400'])
    
    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data['Volume'],
            name='Volume',
            marker_color=colors,
            opacity=0.8
        )
    )
    
    # Add volume moving average
    if 'Volume_MA' in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['Volume_MA'],
                mode='lines',
                name='Volume MA',
                line=dict(
                    color=AdvancedChartThemes.colors.PRIMARY['400'],
                    width=2
                ),
                opacity=0.7
            )
        )
    
    # Update layout
    fig.update_layout(
        height=height,
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {
                'size': 16,
                'family': TypographySystem.FONTS['primary'],
                'color': 'white'
            }
        },
        xaxis=dict(
            showgrid=False,
            linecolor='rgba(255, 255, 255, 0.3)',
            tickfont={'color': 'rgba(255, 255, 255, 0.8)', 'size': 10},
            title_font={'color': 'rgba(255, 255, 255, 0.9)', 'size': 12}
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='rgba(255, 255, 255, 0.3)',
            tickfont={'color': 'rgba(255, 255, 255, 0.8)', 'size': 10},
            title_font={'color': 'rgba(255, 255, 255, 0.9)', 'size': 12}
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': TypographySystem.FONTS['primary'], 'size': 10, 'color': 'white'},
        margin=dict(l=60, r=60, t=60, b=60),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
            font=dict(color='white', size=10)
        )
    )
    
    return fig

# ============================================================================
# CORRELATION HEATMAP
# ============================================================================

def create_correlation_heatmap(
    correlation_matrix: pd.DataFrame,
    title: str = "Correlation Matrix",
    height: int = 500
) -> go.Figure:
    """Create a professional correlation heatmap"""
    
    # Create custom colorscale for correlation
    colorscale = [
        [0, AdvancedChartThemes.colors.ERROR['600']],      # Strong negative
        [0.25, AdvancedChartThemes.colors.ERROR['400']],   # Negative
        [0.4, AdvancedChartThemes.colors.WARNING['400']],  # Weak negative
        [0.5, AdvancedChartThemes.colors.NEUTRAL['400']],  # Neutral
        [0.6, AdvancedChartThemes.colors.SUCCESS['400']],  # Weak positive
        [0.75, AdvancedChartThemes.colors.SUCCESS['600']], # Positive
        [1, AdvancedChartThemes.colors.SUCCESS['800']],    # Strong positive
    ]
    
    fig = go.Figure(
        data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.index,
            colorscale=colorscale,
            zmid=0,
            zmin=-1,
            zmax=1,
            colorbar=dict(
                title="Correlation",
                titleside="right",
                tickmode="linear",
                tick0=-1,
                dtick=0.5,
                len=0.8,
                thickness=20,
                tickfont=dict(color='white', size=10),
                titlefont=dict(color='white', size=12)
            ),
            text=correlation_matrix.round(2).values,
            texttemplate="%{text}",
            textfont={"size": 10},
            hoverongaps=False,
            hovertemplate='<b>%{y} vs %{x}</b><br>Correlation: %{z:.3f}<extra></extra>'
        )
    )
    
    # Update layout
    fig.update_layout(
        height=height,
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
        xaxis=dict(
            tickfont={'color': 'rgba(255, 255, 255, 0.8)', 'size': 10},
            tickangle=45,
            side='bottom'
        ),
        yaxis=dict(
            tickfont={'color': 'rgba(255, 255, 255, 0.8)', 'size': 10},
            autorange='reversed'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font={'family': TypographySystem.FONTS['primary'], 'size': 10, 'color': 'white'},
        margin=dict(l=80, r=80, t=80, b=100)
    )
    
    return fig

# ============================================================================
# PERFORMANCE DASHBOARD
# ============================================================================

def create_performance_dashboard(
    returns_data: pd.DataFrame,
    benchmark_data: Optional[pd.DataFrame] = None,
    title: str = "Performance Dashboard",
    height: int = 600
) -> go.Figure:
    """Create a comprehensive performance dashboard"""
    
    fig = sp.make_subplots(
        rows=3, cols=2,
        subplot_titles=('Cumulative Returns', 'Daily Returns Distribution', 
                       'Rolling Volatility', 'Drawdown Analysis',
                       'Risk-Return Scatter', 'Monthly Returns Heatmap'),
        specs=[[{"colspan": 2}, None],
               [{"secondary_y": True}, {"secondary_y": True}],
               [{}, {}]],
        vertical_spacing=0.08,
        horizontal_spacing=0.05
    )
    
    # 1. Cumulative Returns
    fig.add_trace(
        go.Scatter(
            x=returns_data.index,
            y=(1 + returns_data.iloc[:, 0]).cumprod() - 1,
            mode='lines',
            name=returns_data.columns[0],
            line=dict(color=AdvancedChartThemes.colors.PRIMARY['400'], width=2)
        ),
        row=1, col=1
    )
    
    if benchmark_data is not None:
        fig.add_trace(
            go.Scatter(
                x=benchmark_data.index,
                y=(1 + benchmark_data.iloc[:, 0]).cumprod() - 1,
                mode='lines',
                name='Benchmark',
                line=dict(color=AdvancedChartThemes.colors.NEUTRAL['400'], width=2, dash='dash')
            ),
            row=1, col=1
        )
    
    # 2. Daily Returns Distribution
    fig.add_trace(
        go.Histogram(
            x=returns_data.iloc[:, 0],
            nbinsx=50,
            name='Returns Distribution',
            marker_color=AdvancedChartThemes.colors.PRIMARY['400'],
            opacity=0.7
        ),
        row=2, col=1
    )
    
    # 3. Rolling Volatility
    rolling_vol = returns_data.iloc[:, 0].rolling(window=30).std() * np.sqrt(252)
    fig.add_trace(
        go.Scatter(
            x=rolling_vol.index,
            y=rolling_vol,
            mode='lines',
            name='30-day Volatility',
            line=dict(color=AdvancedChartThemes.colors.WARNING['400'], width=2)
        ),
        row=2, col=2
    )
    
    # 4. Drawdown Analysis
    cumulative = (1 + returns_data.iloc[:, 0]).cumprod()
    rolling_max = cumulative.expanding().max()
    drawdown = (cumulative - rolling_max) / rolling_max
    
    fig.add_trace(
        go.Scatter(
            x=drawdown.index,
            y=drawdown,
            mode='lines',
            name='Drawdown',
            fill='tonexty',
            fillcolor=AdvancedChartThemes.colors.ERROR['500'],
            line=dict(color=AdvancedChartThemes.colors.ERROR['600'], width=1)
        ),
        row=3, col=1
    )
    
    # 5. Risk-Return Scatter (simulated)
    monthly_returns = returns_data.resample('M').apply(lambda x: (1 + x).prod() - 1)
    monthly_vol = monthly_returns.rolling(window=3).std() * np.sqrt(12)
    
    fig.add_trace(
        go.Scatter(
            x=monthly_vol.iloc[:, 0],
            y=monthly_returns.iloc[:, 0],
            mode='markers',
            name='Monthly Risk-Return',
            marker=dict(
                color=monthly_returns.iloc[:, 0],
                colorscale='RdYlGn',
                size=8,
                opacity=0.7,
                colorbar=dict(title="Return", x=1.05, tickfont=dict(color='white'))
            ),
            showlegend=False
        ),
        row=3, col=2
    )
    
    # Update all subplots with professional theme
    for row in range(1, 4):
        for col in range(1, 3):
            if row == 1 and col == 1:
                continue  # Skip the spanned subplot
            
            fig.update_xaxes(
                showgrid=True,
                gridcolor='rgba(255, 255, 255, 0.1)',
                linecolor='rgba(255, 255, 255, 0.3)',
                tickfont={'color': 'rgba(255, 255, 255, 0.8)', 'size': 9},
                title_font={'color': 'rgba(255, 255, 255, 0.9)', 'size': 10},
                row=row, col=col
            )
            
            fig.update_yaxes(
                showgrid=True,
                gridcolor='rgba(255, 255, 255, 0.1)',
                linecolor='rgba(255, 255, 255, 0.3)',
                tickfont={'color': 'rgba(255, 255, 255, 0.8)', 'size': 9},
                title_font={'color': 'rgba(255, 255, 255, 0.9)', 'size': 10},
                row=row, col=col
            )
    
    # Update main layout
    fig.update_layout(
        height=height,
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {
                'size': 20,
                'family': TypographySystem.FONTS['primary'],
                'color': 'white'
            }
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': TypographySystem.FONTS['primary'], 'size': 10, 'color': 'white'},
        margin=dict(l=60, r=120, t=100, b=60),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(color='white', size=9)
        )
    )
    
    return fig

# ============================================================================
# SECTOR COMPARISON CHART
# ============================================================================

def create_sector_comparison_chart(
    sector_data: pd.DataFrame,
    title: str = "Sector Performance Comparison",
    period: str = "1M",
    height: int = 500
) -> go.Figure:
    """Create a sector performance comparison chart"""
    
    # Calculate returns for the specified period
    if period == "1D":
        returns = sector_data.pct_change().iloc[-1]
    elif period == "1W":
        returns = sector_data.pct_change(5).iloc[-1]
    elif period == "1M":
        returns = sector_data.pct_change(21).iloc[-1]
    elif period == "3M":
        returns = sector_data.pct_change(63).iloc[-1]
    elif period == "1Y":
        returns = sector_data.pct_change(252).iloc[-1]
    else:
        returns = sector_data.pct_change(21).iloc[-1]  # Default to 1M
    
    # Sort by performance
    returns = returns.sort_values(ascending=False)
    
    # Create colors based on performance
    colors = []
    for value in returns.values:
        if value > 0.05:  # > 5%
            colors.append(AdvancedChartThemes.colors.SUCCESS['600'])
        elif value > 0:   # 0-5%
            colors.append(AdvancedChartThemes.colors.SUCCESS['400'])
        elif value > -0.05:  # -5% to 0%
            colors.append(AdvancedChartThemes.colors.WARNING['400'])
        else:  # < -5%
            colors.append(AdvancedChartThemes.colors.ERROR['600'])
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(
            x=returns.index,
            y=returns.values * 100,  # Convert to percentage
            marker_color=colors,
            text=[f"{val:.1f}%" for val in returns.values * 100],
            textposition='outside',
            textfont=dict(color='white', size=11),
            hovertemplate='<b>%{x}</b><br>Return: %{y:.1f}%<extra></extra>'
        )
    )
    
    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color='rgba(255, 255, 255, 0.3)', line_width=1)
    
    # Update layout
    fig.update_layout(
        height=height,
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
        xaxis=dict(
            tickfont={'color': 'rgba(255, 255, 255, 0.8)', 'size': 11},
            title_font={'color': 'rgba(255, 255, 255, 0.9)', 'size': 12}
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='rgba(255, 255, 255, 0.3)',
            tickfont={'color': 'rgba(255, 255, 255, 0.8)', 'size': 10},
            title_font={'color': 'rgba(255, 255, 255, 0.9)', 'size': 12},
            tickformat='.1f',
            ticksuffix='%'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': TypographySystem.FONTS['primary'], 'size': 11, 'color': 'white'},
        margin=dict(l=60, r=60, t=80, b=100),
        showlegend=False
    )
    
    return fig

# ============================================================================
# STREAMLIT INTEGRATION FUNCTIONS
# ============================================================================

def display_chart_with_controls(
    chart_function,
    data: pd.DataFrame,
    title: str,
    **kwargs
) -> None:
    """Display a chart with professional controls"""
    
    # Create columns for controls
    control_col1, control_col2, control_col3 = st.columns([1, 1, 2])
    
    with control_col1:
        height = st.slider("Chart Height", 200, 800, 400, 25)
    
    with control_col2:
        show_legend = st.checkbox("Show Legend", True)
    
    with control_col3:
        st.markdown('<div style="height: 32px;"></div>', unsafe_allow_html=True)
        st.markdown("**Professional Financial Charts** 📊")
    
    # Generate and display chart
    try:
        fig = chart_function(data, title=title, height=height, **kwargs)
        
        # Apply professional styling
        fig.update_layout(
            showlegend=show_legend,
            font={'family': TypographySystem.FONTS['primary']},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True, config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d', 'autoScale2d'],
            'toImageButtonOptions': {
                'format': 'png',
                'filename': title.lower().replace(' ', '_'),
                'height': height,
                'width': 1200,
                'scale': 2
            }
        })
        
        # Add chart insights
        with st.expander("📈 Chart Insights", expanded=False):
            st.markdown("### Key Observations")
            st.markdown("• Professional financial chart with dark theme")
            st.markdown("• Interactive hover tooltips for detailed information")
            st.markdown("• Export functionality for presentations")
            st.markdown("• Responsive design for all screen sizes")
            
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")

# Export all chart functions
__all__ = [
    'AdvancedChartThemes',
    'create_professional_candlestick',
    'create_rsi_chart',
    'create_macd_chart', 
    'create_bollinger_bands_chart',
    'create_volume_profile_chart',
    'create_correlation_heatmap',
    'create_performance_dashboard',
    'create_sector_comparison_chart',
    'display_chart_with_controls'
]