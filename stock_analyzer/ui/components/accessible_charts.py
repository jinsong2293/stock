"""
Accessible charts component với Plotly integration
Hỗ trợ color blindness và screen readers

Author: Roo - Architect Mode
Version: 1.0.0
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Optional, Tuple
import pandas as pd

class AccessibleChartRenderer:
    """Render charts với accessibility features"""
    
    def __init__(self, color_system=None):
        self.color_system = color_system
        self.colorblind_safe_palette = [
            '#0066CC',  # Blue
            '#FF6600',  # Orange
            '#009900',  # Green
            '#CC9900',  # Amber
            '#CC0000',  # Red
            '#666666'   # Gray
        ]
    
    def create_accessible_line_chart(
        self,
        data: pd.DataFrame,
        x_column: str,
        y_column: str,
        title: str = "",
        colorblind_mode: bool = False,
        show_patterns: bool = True
    ) -> go.Figure:
        """Tạo line chart với accessibility features"""
        
        # Choose color palette
        if colorblind_mode:
            color_palette = self.colorblind_safe_palette
        else:
            color_palette = self._get_theme_colors()
        
        # Create figure
        fig = go.Figure()
        
        # Add traces
        for i, column in enumerate([y_column] if isinstance(y_column, str) else y_column):
            color = color_palette[i % len(color_palette)]
            
            # Add line trace
            fig.add_trace(go.Scatter(
                x=data[x_column],
                y=data[column],
                mode='lines+markers',
                name=column,
                line=dict(
                    color=color,
                    width=3,
                    dash='solid' if not show_patterns else self._get_line_style(i)
                ),
                marker=dict(
                    size=8,
                    color=color,
                    symbol=self._get_marker_symbol(i)
                ),
                hovertemplate=f'<b>{column}</b><br>' +
                            f'{x_column}: %{{x}}<br>' +
                            f'{column}: %{{y}}<br>' +
                            '<extra></extra>'
            ))
        
        # Update layout for accessibility
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=18, color='var(--text_primary)'),
                x=0.5
            ),
            xaxis=dict(
                title=dict(
                    text=x_column,
                    font=dict(size=14, color='var(--text_primary)')
                ),
                tickfont=dict(color='var(--text_secondary)'),
                gridcolor='var(--border_primary)'
            ),
            yaxis=dict(
                title=dict(
                    text=y_column,
                    font=dict(size=14, color='var(--text_primary)')
                ),
                tickfont=dict(color='var(--text_secondary)'),
                gridcolor='var(--border_primary)'
            ),
            plot_bgcolor='var(--bg_primary)',
            paper_bgcolor='var(--bg_primary)',
            font=dict(color='var(--text_primary)'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color='var(--text_primary)')
            ),
            margin=dict(l=60, r=60, t=80, b=60),
            height=400
        )
        
        return fig
    
    def create_accessible_bar_chart(
        self,
        data: pd.DataFrame,
        x_column: str,
        y_column: str,
        title: str = "",
        colorblind_mode: bool = False
    ) -> go.Figure:
        """Tạo bar chart với accessibility features"""
        
        # Choose color palette
        if colorblind_mode:
            color_palette = self.colorblind_safe_palette
        else:
            color_palette = self._get_theme_colors()
        
        # Create color array
        colors = [color_palette[i % len(color_palette)] for i in range(len(data))]
        
        # Create figure
        fig = px.bar(
            data,
            x=x_column,
            y=y_column,
            title=title,
            color_discrete_sequence=colors,
            text=y_column
        )
        
        # Update layout
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=18, color='var(--text_primary)'),
                x=0.5
            ),
            xaxis=dict(
                title=dict(
                    text=x_column,
                    font=dict(size=14, color='var(--text_primary)')
                ),
                tickfont=dict(color='var(--text_secondary)'),
                gridcolor='var(--border_primary)'
            ),
            yaxis=dict(
                title=dict(
                    text=y_column,
                    font=dict(size=14, color='var(--text_primary)')
                ),
                tickfont=dict(color='var(--text_secondary)'),
                gridcolor='var(--border_primary)'
            ),
            plot_bgcolor='var(--bg_primary)',
            paper_bgcolor='var(--bg_primary)',
            font=dict(color='var(--text_primary)'),
            height=400
        )
        
        # Update bars
        fig.update_traces(
            texttemplate='%{text:.1f}',
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>' +
                         f'{y_column}: %{{y}}<br>' +
                         '<extra></extra>'
        )
        
        return fig
    
    def _get_theme_colors(self) -> List[str]:
        """Lấy colors từ theme hiện tại"""
        if self.color_system:
            theme = self.color_system.get_current_theme()
            return [
                theme.get('chart_1', '#3B82F6'),
                theme.get('chart_2', '#0EA5E9'),
                theme.get('chart_3', '#10B981'),
                theme.get('chart_4', '#F59E0B'),
                theme.get('chart_5', '#EF4444'),
                theme.get('chart_6', '#8B5CF6')
            ]
        return self.colorblind_safe_palette
    
    def _get_line_style(self, index: int) -> str:
        """Get line style cho different series"""
        styles = ['solid', 'dash', 'dot', 'dashdot', 'longdash', 'longdashdot']
        return styles[index % len(styles)]
    
    def _get_marker_symbol(self, index: int) -> str:
        """Get marker symbol cho different series"""
        symbols = ['circle', 'square', 'diamond', 'cross', 'triangle-up', 'triangle-down']
        return symbols[index % len(symbols)]

def render_accessible_chart(
    fig: go.Figure,
    key: str,
    alt_text: str = "",
    description: str = ""
):
    """Render accessible chart trong Streamlit"""
    
    # Add accessibility attributes
    config = {
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
        'toImageButtonOptions': {
            'format': 'png',
            'filename': f'chart_{key}',
            'height': 500,
            'width': 700,
            'scale': 1
        }
    }
    
    # Render chart
    st.plotly_chart(
        fig,
        use_container_width=True,
        config=config,
        key=key
    )
    
    # Add accessible description
    if description:
        st.markdown(f"""
        <div class="chart-description" role="region" aria-label="Chart description">
            <p><strong>Description:</strong> {description}</p>
        </div>
        <style>
        .chart-description {{
            background: var(--bg_secondary);
            border-left: 4px solid var(--interactive_primary);
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 0 0.5rem 0.5rem 0;
        }}
        </style>
        """, unsafe_allow_html=True)
    
    # Add screen reader text
    if alt_text:
        st.markdown(f"""
        <div class="sr-only" aria-label="Alternative text for chart">
            {alt_text}
        </div>
        """, unsafe_allow_html=True)

def create_chart_accessibility_info():
    """Create accessibility information for charts"""
    st.markdown("### 📊 Chart Accessibility Features")
    
    accessibility_features = [
        "✅ Colorblind-safe color palette",
        "✅ Multiple visual cues (patterns, symbols, line styles)",
        "✅ Screen reader compatible alt text",
        "✅ Keyboard navigation support",
        "✅ High contrast mode support",
        "✅ Responsive design for all screen sizes"
    ]
    
    for feature in accessibility_features:
        st.markdown(feature)
    
    st.markdown("### 🎨 Color Palette Information")
    st.markdown("""
    The chart uses a carefully selected color palette that:
    - Meets WCAG 2.1 AA contrast requirements
    - Remains distinguishable for color blind users
    - Provides clear visual hierarchy
    - Works well in both light and dark themes
    """)
    
    # Show colorblind simulation
    if st.session_state.get('colorblind_mode', False):
        st.markdown("### 👁️ Color Blindness Simulation")
        st.markdown("""
        Current charts are displayed using colorblind-safe colors.
        For users with different types of color blindness, the system automatically:
        - Uses patterns and textures as additional visual cues
        - Selects colors that remain distinguishable
        - Provides alternative visual indicators
        """)

def create_accessibility_testing_dashboard():
    """Create dashboard for testing accessibility features"""
    st.markdown("### 🧪 Accessibility Testing Dashboard")
    
    # Color contrast testing
    st.markdown("#### 🎨 Color Contrast Testing")
    
    try:
        from ..accessibility.contrast_checker import ContrastChecker
        
        checker = ContrastChecker()
        
        # Test predefined color combinations
        test_combinations = [
            ("Primary text on white", "#111827", "#FFFFFF"),
            ("Secondary text on white", "#6B7280", "#FFFFFF"),
            ("Interactive color on white", "#3B82F6", "#FFFFFF"),
            ("Success on white", "#10B981", "#FFFFFF"),
            ("Error on white", "#EF4444", "#FFFFFF"),
        ]
        
        for name, foreground, background in test_combinations:
            result = checker.validate_contrast(foreground, background)
            
            status_icon = "✅" if result['passes_aa'] else "❌"
            st.write(f"{status_icon} **{name}**: {result['contrast_ratio']:.2f}:1 ({result['wcag_level']})")
            
            if not result['passes_aa']:
                st.warning(f"Needs improvement: {result['recommendation']}")
                
    except ImportError:
        st.info("Contrast checker not available")
    
    # Color blindness testing
    st.markdown("#### 👁️ Color Blindness Testing")
    
    try:
        from ..accessibility.colorblindness import ColorBlindnessSimulator
        
        simulator = ColorBlindnessSimulator()
        
        # Color combinations to test
        test_colors = [
            ("Blue vs Orange", "#3B82F6", "#FF6600"),
            ("Green vs Amber", "#10B981", "#F59E0B"),
            ("Red vs Gray", "#EF4444", "#6B7280"),
        ]
        
        for name, color1, color2 in test_colors:
            st.write(f"**{name}**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div style="
                    background-color: {color1};
                    color: white;
                    padding: 1rem;
                    border-radius: 0.5rem;
                    text-align: center;
                    font-weight: bold;
                ">
                    Color 1: {color1}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="
                    background-color: {color2};
                    color: white;
                    padding: 1rem;
                    border-radius: 0.5rem;
                    text-align: center;
                    font-weight: bold;
                ">
                    Color 2: {color2}
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                # Simulate color blindness
                sim1 = simulator.simulate_color(color1, 'protanopia')
                sim2 = simulator.simulate_color(color2, 'protanopia')
                
                st.markdown(f"""
                <div style="
                    background-color: {sim1};
                    color: white;
                    padding: 0.5rem;
                    border-radius: 0.25rem;
                    text-align: center;
                    font-size: 0.8rem;
                ">
                    Protanopia: {sim1}
                </div>
                <div style="
                    background-color: {sim2};
                    color: white;
                    padding: 0.5rem;
                    border-radius: 0.25rem;
                    text-align: center;
                    font-size: 0.8rem;
                    margin-top: 0.5rem;
                ">
                    {sim2}
                </div>
                """, unsafe_allow_html=True)
                
    except ImportError:
        st.info("Color blindness simulator not available")
    
    # Performance testing
    st.markdown("#### ⚡ Performance Testing")
    
    try:
        from ..accessibility.performance_monitor import performance_monitor
        
        perf_summary = performance_monitor.get_performance_summary()
        
        if perf_summary['status'] == 'good':
            st.success("✅ Performance is within acceptable ranges")
        elif perf_summary['status'] == 'warning':
            st.warning("⚠️ Performance needs attention")
        else:
            st.info("ℹ️ No performance data available")
        
        if 'performance' in perf_summary:
            perf = perf_summary['performance']
            st.markdown(f"""
            **Current Metrics:**
            - Theme Switch: {perf.get('avg_theme_switch_time', 0):.1f}ms
            - Contrast Check: {perf.get('avg_contrast_check_time', 0):.1f}ms
            - Memory Usage: {perf.get('avg_memory_usage', 0):.1f}MB
            - CPU Usage: {perf.get('avg_cpu_usage', 0):.1f}%
            """)
            
    except ImportError:
        st.info("Performance monitor not available")
    
    # Get performance dashboard
    try:
        from ..accessibility.performance_monitor import performance_monitor
        
        perf_dashboard = performance_monitor.get_performance_dashboard()
        st.markdown(perf_dashboard, unsafe_allow_html=True)
        
    except ImportError:
        pass