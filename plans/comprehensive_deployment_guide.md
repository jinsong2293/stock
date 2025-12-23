# Tài liệu Hướng dẫn Sử dụng và Triển khai Hệ thống Màu sắc Accessibility

## Tổng quan Tài liệu

Tài liệu này cung cấp hướng dẫn toàn diện về cách triển khai và sử dụng hệ thống màu sắc với accessibility tối ưu cho ứng dụng Stock Analyzer. Bao gồm từ cài đặt cơ bản đến tích hợp nâng cao và troubleshooting.

## Mục lục

1. [Giới thiệu Hệ thống](#giới-thiệu-hệ-thống)
2. [Cài đặt và Thiết lập](#cài-đặt-và-thiết-lập)
3. [Tích hợp với Streamlit](#tích-hợp-với-streamlit)
4. [Hướng dẫn Sử dụng](#hướng-dẫn-sử-dụng)
5. [Cấu hình Nâng cao](#cấu-hình-nâng-cao)
6. [Testing và Validation](#testing-và-validation)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)
9. [FAQ](#faq)

## Giới thiệu Hệ thống

### Tính năng chính

- ✅ **WCAG 2.1 AA Compliance**: Tuân thủ chuẩn accessibility quốc tế
- ✅ **Responsive Design**: Tối ưu cho tất cả kích thước màn hình
- ✅ **Light/Dark Mode**: Chuyển đổi mượt mà giữa chế độ sáng và tối
- ✅ **Color Blindness Support**: Hỗ trợ người khiếm thị màu
- ✅ **Automated Testing**: Kiểm thử tự động liên tục
- ✅ **Real-time Monitoring**: Giám sát accessibility theo thời gian thực
- ✅ **Performance Optimized**: Tối ưu hiệu suất và tốc độ

### Yêu cầu hệ thống

- Python 3.8+
- Streamlit 1.10+
- Modern web browser (Chrome 90+, Firefox 88+, Safari 14+)
- Node.js 16+ (cho testing tools)
- Minimum 2GB RAM
- Internet connection (cho fonts và CDN)

## Cài đặt và Thiết lập

### 1. Cài đặt Dependencies

```bash
# Clone hoặc tải về source code
git clone https://github.com/your-org/stock-analyzer-accessibility.git
cd stock-analyzer-accessibility

# Cài đặt Python dependencies
pip install -r requirements.txt

# Cài đặt Node.js dependencies cho testing
npm install

# Cài đặt global testing tools
npm install -g @axe-core/cli puppeteer
```

### 2. Cấu trúc thư mục

```
stock_analyzer/
├── ui/
│   ├── accessibility/
│   │   ├── color_system.py
│   │   ├── theme_manager.py
│   │   ├── contrast_checker.py
│   │   └── accessibility_tester.py
│   ├── components/
│   │   ├── accessible_charts.py
│   │   ├── status_indicators.py
│   │   └── theme_toggle.py
│   └── styles/
│       ├── accessibility.css
│       ├── responsive.css
│       └── colorblind-support.css
├── tests/
│   ├── accessibility/
│   │   ├── test_color_contrast.py
│   │   ├── test_colorblindness.py
│   │   └── test_responsive.py
│   └── fixtures/
├── docs/
│   ├── accessibility_guide.md
│   ├── deployment_guide.md
│   └── api_reference.md
└── examples/
    ├── basic_usage.py
    ├── advanced_integration.py
    └── custom_themes.py
```

### 3. Cấu hình môi trường

```bash
# Tạo file .env
cp .env.example .env

# Chỉnh sửa .env với cấu hình của bạn
cat > .env << EOF
# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Accessibility Configuration
ACCESSIBILITY_TESTING_ENABLED=true
ACCESSIBILITY_REPORTING_ENABLED=true
COLORBLIND_TESTING_ENABLED=true

# Performance Configuration
THEME_SWITCH_ANIMATION_DURATION=300
ACCESSIBILITY_CHECK_INTERVAL=5000

# Monitoring Configuration
MONITORING_ENABLED=true
ALERT_WEBHOOK_URL=https://hooks.slack.com/your-webhook
EMAIL_ALERTS_ENABLED=true
EOF
```

## Tích hợp với Streamlit

### 1. Cấu hình cơ bản

#### File: `app.py`
```python
import streamlit as st
from ui.accessibility.color_system import AccessibilityColorSystem
from ui.accessibility.theme_manager import ThemeManager
from ui.accessibility.contrast_checker import ContrastChecker

# Initialize accessibility system
@st.cache_resource
def init_accessibility_system():
    return AccessibilityColorSystem()

@st.cache_resource  
def init_theme_manager():
    return ThemeManager()

@st.cache_resource
def init_contrast_checker():
    return ContrastChecker()

# Page configuration
st.set_page_config(
    page_title="Stock Analyzer - Accessible",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize systems
color_system = init_accessibility_system()
theme_manager = init_theme_manager()
contrast_checker = init_contrast_checker()

# Apply accessibility CSS
st.markdown(color_system.get_accessibility_css(), unsafe_allow_html=True)
```

#### File: `ui/accessibility/color_system.py`
```python
import streamlit as st
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class ColorSpec:
    """Đặc tả màu sắc với accessibility metadata"""
    hex: str
    name: str
    contrast_ratio: float
    wcag_level: str
    usage: str
    colorblind_safe: bool = True

class AccessibilityColorSystem:
    """Hệ thống màu sắc với accessibility tối ưu"""
    
    def __init__(self):
        self.light_theme = self._create_light_theme()
        self.dark_theme = self._create_dark_theme()
        self.current_theme = 'light'
        
    def _create_light_theme(self) -> Dict[str, str]:
        return {
            # Background colors
            'bg_primary': '#FFFFFF',
            'bg_secondary': '#F8FAFC',
            'bg_tertiary': '#F1F5F9',
            'bg_accent': '#EFF6FF',
            
            # Text colors
            'text_primary': '#111827',      # 15.3:1 vs white
            'text_secondary': '#6B7280',    # 4.5:1 vs white
            'text_tertiary': '#9CA3AF',     # 3.0:1 vs white
            'text_inverse': '#F9FAFB',      # 15.3:1 vs dark bg
            
            # Interactive colors
            'interactive_primary': '#3B82F6',
            'interactive_hover': '#2563EB',
            'interactive_active': '#1D4ED8',
            'interactive_focus': '#60A5FA',
            
            # Semantic colors
            'success': '#10B981',
            'warning': '#F59E0B',
            'error': '#EF4444',
            'info': '#0EA5E9',
            
            # Chart colors (colorblind safe)
            'chart_1': '#3B82F6',
            'chart_2': '#0EA5E9',
            'chart_3': '#10B981',
            'chart_4': '#F59E0B',
            'chart_5': '#EF4444',
            'chart_6': '#8B5CF6'
        }
    
    def _create_dark_theme(self) -> Dict[str, str]:
        return {
            # Background colors
            'bg_primary': '#111827',
            'bg_secondary': '#1F2937',
            'bg_tertiary': '#374151',
            'bg_accent': '#1E40AF',
            
            # Text colors
            'text_primary': '#F9FAFB',      # 15.3:1 vs dark bg
            'text_secondary': '#CBD5E1',    # 7.5:1 vs dark bg
            'text_tertiary': '#94A3B8',     # 4.5:1 vs dark bg
            'text_inverse': '#111827',      # 15.3:1 vs light bg
            
            # Interactive colors (lighter for visibility)
            'interactive_primary': '#60A5FA',
            'interactive_hover': '#93C5FD',
            'interactive_active': '#BFDBFE',
            'interactive_focus': '#3B82F6',
            
            # Semantic colors (lighter for dark mode)
            'success': '#34D399',
            'warning': '#FBBF24',
            'error': '#F87171',
            'info': '#7DD3FC',
            
            # Chart colors (optimized for dark background)
            'chart_1': '#60A5FA',
            'chart_2': '#7DD3FC',
            'chart_3': '#34D399',
            'chart_4': '#FBBF24',
            'chart_5': '#F87171',
            'chart_6': '#A78BFA'
        }
    
    def get_current_theme(self) -> Dict[str, str]:
        """Lấy theme colors hiện tại"""
        return self.dark_theme if self.current_theme == 'dark' else self.light_theme
    
    def switch_theme(self, theme: str):
        """Chuyển đổi theme"""
        if theme in ['light', 'dark']:
            self.current_theme = theme
            # Clear cache để apply theme mới
            st.rerun()
    
    def get_accessibility_css(self) -> str:
        """Generate CSS với accessibility features"""
        theme = self.get_current_theme()
        
        return f"""
        <style>
        /* CSS Custom Properties */
        :root {{
            /* Theme Colors */
            {' '.join([f'--{k}: {v};' for k, v in theme.items()])}
            
            /* Accessibility Enhancements */
            --focus-ring: 2px solid var(--interactive_focus);
            --focus-ring-offset: 2px;
            
            /* Animation durations */
            --transition-fast: 0.15s ease-out;
            --transition-normal: 0.3s ease-out;
            --transition-slow: 0.5s ease-out;
        }}
        
        /* Global accessibility improvements */
        * {{
            scroll-behavior: smooth;
        }}
        
        /* Focus indicators */
        *:focus {{
            outline: var(--focus-ring);
            outline-offset: var(--focus-ring-offset);
        }}
        
        /* Skip links for screen readers */
        .skip-link {{
            position: absolute;
            top: -40px;
            left: 6px;
            background: var(--interactive_primary);
            color: white;
            padding: 8px;
            text-decoration: none;
            border-radius: 4px;
            z-index: 1000;
        }}
        
        .skip-link:focus {{
            top: 6px;
        }}
        
        /* Screen reader only content */
        .sr-only {{
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border: 0;
        }}
        
        /* High contrast mode support */
        @media (prefers-contrast: high) {{
            :root {{
                --bg_primary: #000000;
                --text_primary: #FFFFFF;
                --interactive_primary: #FFFF00;
            }}
        }}
        
        /* Reduced motion support */
        @media (prefers-reduced-motion: reduce) {{
            * {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }}
        }}
        
        /* Print styles */
        @media print {{
            * {{
                background: white !important;
                color: black !important;
                box-shadow: none !important;
            }}
        }}
        </style>
        """
    
    def validate_color_contrast(self, foreground: str, background: str) -> Dict:
        """Kiểm tra contrast ratio và WCAG compliance"""
        from .contrast_checker import ContrastChecker
        
        checker = ContrastChecker()
        return checker.validate_contrast(foreground, background)
    
    def get_colorblind_safe_colors(self) -> Dict[str, str]:
        """Lấy colorblind-safe color palette"""
        return {
            'primary': '#0066CC',      # Blue (safe for all types)
            'secondary': '#FF6600',    # Orange (high contrast)
            'success': '#009900',      # Green (protanopia safe)
            'warning': '#CC9900',      # Amber (deuteranopia safe)
            'error': '#CC0000',        # Red (tritanopia safe)
            'neutral': '#666666'       # Gray (always safe)
        }
```

### 2. Theme Toggle Component

#### File: `ui/components/theme_toggle.py`
```python
import streamlit as st
from typing import Optional

def create_theme_toggle(
    key: str = "theme_toggle",
    label: str = "Theme",
    show_labels: bool = True
) -> Optional[str]:
    """Tạo accessible theme toggle component"""
    
    # Get current theme from session state
    current_theme = st.session_state.get('theme', 'light')
    
    # Create columns for layout
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown(f"**{label}:**")
    
    with col2:
        # Theme selection
        theme_options = {
            "🌞 Light": "light",
            "🌙 Dark": "dark",
            "🖥️ Auto": "auto"
        }
        
        # Find current selection
        current_selection = None
        for display_name, theme_value in theme_options.items():
            if theme_value == current_theme:
                current_selection = display_name
                break
        
        if not current_selection:
            current_selection = "🌞 Light"  # Default
        
        selected = st.selectbox(
            "Select theme",
            options=list(theme_options.keys()),
            index=list(theme_options.keys()).index(current_selection),
            key=f"{key}_select",
            label_visibility="collapsed"
        )
        
        # Update theme when selection changes
        new_theme = theme_options[selected]
        if new_theme != current_theme:
            st.session_state['theme'] = new_theme
            st.rerun()
    
    return st.session_state.get('theme', 'light')

def create_accessible_button(
    label: str,
    on_click=None,
    type: str = "primary",
    disabled: bool = False,
    key: Optional[str] = None
):
    """Tạo accessible button với proper ARIA labels"""
    
    # Button styling based on type
    button_styles = {
        "primary": """
            background-color: var(--interactive_primary);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            font-weight: 600;
        """,
        "secondary": """
            background-color: transparent;
            color: var(--interactive_primary);
            border: 2px solid var(--interactive_primary);
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            font-weight: 600;
        """,
        "success": """
            background-color: var(--success);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            font-weight: 600;
        """,
        "warning": """
            background-color: var(--warning);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            font-weight: 600;
        """,
        "error": """
            background-color: var(--error);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            font-weight: 600;
        """
    }
    
    # Generate unique key if not provided
    if key is None:
        key = f"btn_{hash(label)}"
    
    # Create HTML button
    button_html = f"""
    <button 
        id="{key}"
        class="accessible-button"
        style="{button_styles.get(type, button_styles['primary'])}"
        onclick="{f'{on_click}()' if on_click else 'void(0)'}"
        disabled="{disabled}"
        aria-label="{label}"
        role="button"
    >
        {label}
    </button>
    <style>
    .accessible-button {{
        cursor: pointer;
        transition: all 0.2s ease;
        font-family: inherit;
        font-size: 1rem;
        line-height: 1.5;
    }}
    .accessible-button:hover:not(:disabled) {{
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }}
    .accessible-button:focus {{
        outline: 2px solid var(--interactive_focus);
        outline-offset: 2px;
    }}
    .accessible-button:disabled {{
        opacity: 0.6;
        cursor: not-allowed;
        transform: none;
    }}
    </style>
    """
    
    st.markdown(button_html, unsafe_allow_html=True)
    
    return key
```

### 3. Accessible Charts Component

#### File: `ui/components/accessible_charts.py`
```python
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
```

### 4. Status Indicators Component

#### File: `ui/components/status_indicators.py`
```python
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
```

## Hướng dẫn Sử dụng

### 1. Cấu hình cơ bản

#### File: `main.py`
```python
import streamlit as st
from ui.accessibility.color_system import AccessibilityColorSystem
from ui.components.theme_toggle import create_theme_toggle
from ui.components.status_indicators import create_accessible_metric_card, StatusType

# Page setup
st.set_page_config(
    page_title="Accessible Stock Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize accessibility system
@st.cache_resource
def init_color_system():
    return AccessibilityColorSystem()

color_system = init_color_system()

# Apply accessibility CSS
st.markdown(color_system.get_accessibility_css(), unsafe_allow_html=True)

# Skip link for screen readers
st.markdown("""
<a href="#main-content" class="skip-link">Skip to main content</a>
""", unsafe_allow_html=True)

# Header with theme toggle
col1, col2 = st.columns([3, 1])

with col1:
    st.title("📈 Accessible Stock Analyzer")

with col2:
    current_theme = create_theme_toggle()

# Main content area
main_container = st.container()
with main_container:
    st.markdown('<div id="main-content">', unsafe_allow_html=True)
    
    # Dashboard metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Sample metrics với accessibility
        metric_html = create_accessible_metric_card(
            title="Total Portfolio Value",
            value="$125,430",
            change=2.5,
            previous_value=122340,
            status=StatusType.SUCCESS,
            description="Total value of all holdings in the portfolio"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col2:
        metric_html = create_accessible_metric_card(
            title="Today's Gain/Loss",
            value="+$1,240",
            change=1.2,
            previous_value=1240,
            status=StatusType.SUCCESS,
            description="Change in portfolio value for today"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col3:
        metric_html = create_accessible_metric_card(
            title="Active Positions",
            value="12",
            status=StatusType.INFO,
            description="Number of currently held positions"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col4:
        metric_html = create_accessible_metric_card(
            title="Risk Level",
            value="Medium",
            status=StatusType.WARNING,
            description="Overall portfolio risk assessment"
        )
        st.markdown(metric_html, unsafe_allow_html=True)
    
    # Sample chart
    st.subheader("Portfolio Performance")
    
    # Create sample data
    import pandas as pd
    import numpy as np
    
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    portfolio_value = 100000 + np.cumsum(np.random.randn(len(dates)) * 100)
    
    df = pd.DataFrame({
        'Date': dates,
        'Portfolio Value': portfolio_value
    })
    
    # Render accessible chart
    from ui.components.accessible_charts import AccessibleChartRenderer, render_accessible_chart
    
    chart_renderer = AccessibleChartRenderer(color_system)
    
    # Create accessible line chart
    fig = chart_renderer.create_accessible_line_chart(
        data=df,
        x_column='Date',
        y_column='Portfolio Value',
        title='Portfolio Value Over Time',
        colorblind_mode=False,
        show_patterns=True
    )
    
    # Render chart với accessibility
    render_accessible_chart(
        fig=fig,
        key="portfolio_chart",
        alt_text="Line chart showing portfolio value from January to December 2023",
        description="The chart shows the portfolio value fluctuating throughout 2023, with an overall upward trend from $100,000 to approximately $125,000."
    )

# Add keyboard navigation help
st.sidebar.markdown("""
## ♿ Accessibility Features

### Keyboard Navigation
- **Tab**: Navigate through elements
- **Enter/Space**: Activate buttons and links
- **Escape**: Close modals and dropdowns
- **Arrow keys**: Navigate within components

### Screen Reader Support
- All images have alt text
- Form labels are properly associated
- Status updates are announced
- Skip links are available

### Visual Accessibility
- High contrast ratios (WCAG AA compliant)
- Color is not the only indicator
- Patterns supplement color coding
- Scalable text up to 200%

### Color Blindness Support
- Multiple visual cues for status
- Patterns and textures for differentiation
- High contrast color combinations
- Icon and text alternatives
""")
```

### 2. Testing Components

#### File: `examples/test_accessibility.py`
```python
import streamlit as st
from ui.accessibility.color_system import AccessibilityColorSystem
from ui.accessibility.contrast_checker import ContrastChecker
from ui.components.status_indicators import StatusIndicator, StatusType

def test_color_contrast():
    """Test color contrast ratios"""
    st.header("🎨 Color Contrast Testing")
    
    # Initialize components
    color_system = AccessibilityColorSystem()
    contrast_checker = ContrastChecker()
    
    # Test predefined color combinations
    test_combinations = [
        ("Primary text on white", "#111827", "#FFFFFF"),
        ("Secondary text on white", "#6B7280", "#FFFFFF"),
        ("Interactive color on white", "#3B82F6", "#FFFFFF"),
        ("Success on white", "#10B981", "#FFFFFF"),
        ("Error on white", "#EF4444", "#FFFFFF"),
    ]
    
    for name, foreground, background in test_combinations:
        result = contrast_checker.validate_contrast(foreground, background)
        
        status_icon = "✅" if result['passes_aa'] else "❌"
        st.write(f"{status_icon} **{name}**: {result['contrast_ratio']:.2f}:1 ({result['wcag_level']})")
        
        if not result['passes_aa']:
            st.warning(f"Needs improvement: {result['recommendation']}")

def test_status_indicators():
    """Test status indicators"""
    st.header("📊 Status Indicators Testing")
    
    indicator = StatusIndicator()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Status Badges")
        
        for status in StatusType:
            badge_html = indicator.render_status_badge(
                status=status,
                message=f"Sample {status.value} message",
                size="medium"
            )
            st.markdown(badge_html, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Trend Indicators")
        
        # Test trend indicators
        trend_html = indicator.render_trend_indicator(
            value=125.5,
            previous_value=120.0,
            format_type="currency"
        )
        st.markdown(trend_html, unsafe_allow_html=True)
        
        trend_html = indicator.render_trend_indicator(
            value=2.5,
            previous_value=3.0,
            format_type="percentage"
        )
        st.markdown(trend_html, unsafe_allow_html=True)

def test_colorblind_simulation():
    """Test color blindness simulation"""
    st.header("👁️ Color Blindness Testing")
    
    # Color combinations to test
    test_colors = [
        ("Blue vs Orange", "#3B82F6", "#FF6600"),
        ("Green vs Amber", "#10B981", "#F59E0B"),
        ("Red vs Gray", "#EF4444", "#6B7280"),
        ("Primary vs Info", "#3B82F6", "#0EA5E9"),
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
            from ui.accessibility.colorblindness import ColorBlindnessSimulator
            simulator = ColorBlindnessSimulator()
            
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

def run_accessibility_tests():
    """Main test runner"""
    st.title("🧪 Accessibility Testing Suite")
    
    st.markdown("""
    This page provides comprehensive testing for the accessibility color system.
    Use these tests to validate that your implementation meets WCAG 2.1 AA standards.
    """)
    
    # Navigation
    test_choice = st.selectbox(
        "Select test to run:",
        ["Color Contrast", "Status Indicators", "Color Blindness Simulation"]
    )
    
    if test_choice == "Color Contrast":
        test_color_contrast()
    elif test_choice == "Status Indicators":
        test_status_indicators()
    elif test_choice == "Color Blindness Simulation":
        test_colorblind_simulation()

if __name__ == "__main__":
    run_accessibility_tests()
```

## Cấu hình Nâng cao

### 1. Custom Theme Creation

#### File: `examples/custom_themes.py`
```python
import streamlit as st
from ui.accessibility.color_system import AccessibilityColorSystem, ColorSpec

class CustomThemeManager:
    """Manager cho custom themes"""
    
    def __init__(self, base_system: AccessibilityColorSystem):
        self.base_system = base_system
        self.custom_themes = {}
    
    def create_custom_theme(
        self,
        name: str,
        colors: dict,
        accessibility_validation: bool = True
    ) -> bool:
        """Tạo custom theme với validation"""
        
        if accessibility_validation:
            # Validate all colors meet WCAG standards
            if not self._validate_theme_accessibility(colors):
                st.error("Custom theme fails accessibility standards")
                return False
        
        # Store custom theme
        self.custom_themes[name] = colors
        
        # Inject CSS
        self._inject_theme_css(name, colors)
        
        return True
    
    def _validate_theme_accessibility(self, colors: dict) -> bool:
        """Validate theme meets accessibility standards"""
        
        # Required color validations
        validations = [
            # Text contrast checks
            ("text_primary", colors.get('bg_primary', '#FFFFFF')),
            ("text_secondary", colors.get('bg_primary', '#FFFFFF')),
            ("text_inverse", colors.get('bg_primary', '#FFFFFF')),
            
            # Interactive color checks
            ("interactive_primary", colors.get('bg_secondary', '#F8FAFC')),
            
            # Semantic color checks
            ("success", colors.get('text_inverse', '#F9FAFB')),
            ("error", colors.get('text_inverse', '#F9FAFB')),
            ("warning", colors.get('text_inverse', '#F9FAFB')),
        ]
        
        from ui.accessibility.contrast_checker import ContrastChecker
        checker = ContrastChecker()
        
        for foreground_name, background_color in validations:
            foreground_color = colors.get(foreground_name)
            if foreground_color:
                result = checker.validate_contrast(foreground_color, background_color)
                if not result['passes_aa']:
                    return False
        
        return True
    
    def _inject_theme_css(self, name: str, colors: dict):
        """Inject custom theme CSS"""
        
        css_vars = '\n'.join([f'--{k}: {v};' for k, v in colors.items()])
        
        custom_theme_css = f"""
        <style>
        [data-custom-theme="{name}"] {{
            {css_vars}
        }}
        </style>
        """
        
        st.markdown(custom_theme_css, unsafe_allow_html=True)

def create_theme_customization_ui():
    """UI cho customizing themes"""
    st.title("🎨 Custom Theme Creator")
    
    # Initialize systems
    color_system = AccessibilityColorSystem()
    custom_manager = CustomThemeManager(color_system)
    
    # Theme input form
    with st.form("custom_theme_form"):
        st.subheader("Create Custom Theme")
        
        theme_name = st.text_input("Theme Name", placeholder="e.g., Corporate Blue")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Background Colors**")
            bg_primary = st.color_picker("Primary Background", "#FFFFFF")
            bg_secondary = st.color_picker("Secondary Background", "#F8FAFC")
            bg_accent = st.color_picker("Accent Background", "#EFF6FF")
        
        with col2:
            st.markdown("**Text Colors**")
            text_primary = st.color_picker("Primary Text", "#111827")
            text_secondary = st.color_picker("Secondary Text", "#6B7280")
            text_inverse = st.color_picker("Inverse Text", "#F9FAFB")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Interactive Colors**")
            interactive_primary = st.color_picker("Primary Interactive", "#3B82F6")
            interactive_hover = st.color_picker("Hover State", "#2563EB")
        
        with col2:
            st.markdown("**Semantic Colors**")
            success = st.color_picker("Success", "#10B981")
            warning = st.color_picker("Warning", "#F59E0B")
            error = st.color_picker("Error", "#EF4444")
            info = st.color_picker("Info", "#0EA5E9")
        
        submitted = st.form_submit_button("Create Theme", type="primary")
        
        if submitted:
            # Compile theme colors
            theme_colors = {
                'bg_primary': bg_primary,
                'bg_secondary': bg_secondary,
                'bg_accent': bg_accent,
                'text_primary': text_primary,
                'text_secondary': text_secondary,
                'text_inverse': text_inverse,
                'interactive_primary': interactive_primary,
                'interactive_hover': interactive_hover,
                'success': success,
                'warning': warning,
                'error': error,
                'info': info
            }
            
            # Create theme
            if custom_manager.create_custom_theme(theme_name, theme_colors):
                st.success(f"Custom theme '{theme_name}' created successfully!")
                
                # Preview theme
                st.markdown("### Theme Preview")
                preview_css = f"""
                <div style="
                    background: {bg_primary};
                    color: {text_primary};
                    padding: 2rem;
                    border-radius: 1rem;
                    border: 1px solid {bg_secondary};
                ">
                    <h2 style="color: {text_primary};">Sample Heading</h2>
                    <p style="color: {text_secondary};">Sample secondary text</p>
                    <button style="
                        background: {interactive_primary};
                        color: {text_inverse};
                        border: none;
                        padding: 0.5rem 1rem;
                        border-radius: 0.5rem;
                        font-weight: 600;
                    ">
                        Sample Button
                    </button>
                </div>
                """
                st.markdown(preview_css, unsafe_allow_html=True)

if __name__ == "__main__":
    create_theme_customization_ui()
```

### 2. Performance Monitoring

#### File: `ui/performance_monitor.py`
```python
import time
import psutil
import streamlit as st
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import json

@dataclass
class PerformanceMetrics:
    """Performance metrics cho accessibility features"""
    timestamp: datetime
    theme_switch_time: float
    contrast_check_time: float
    render_time: float
    memory_usage: float
    cpu_usage: float

class AccessibilityPerformanceMonitor:
    """Monitor performance của accessibility features"""
    
    def __init__(self):
        self.metrics_history: List[PerformanceMetrics] = []
        self.thresholds = {
            'theme_switch': 300,      # milliseconds
            'contrast_check': 10,     # milliseconds
            'render_time': 100,       # milliseconds
            'memory_usage': 100,      # MB
            'cpu_usage': 50          # percentage
        }
    
    def measure_theme_switch(self, func):
        """Decorator để measure theme switching performance"""
        def wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            
            result = func(*args, **kwargs)
            
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            
            # Record metrics
            metrics = PerformanceMetrics(
                timestamp=datetime.now(),
                theme_switch_time=(end_time - start_time) * 1000,  # Convert to ms
                contrast_check_time=0,  # Not applicable here
                render_time=0,  # Not applicable here
                memory_usage=end_memory - start_memory,
                cpu_usage=psutil.cpu_percent()
            )
            
            self.metrics_history.append(metrics)
            
            # Keep only last 100 metrics
            if len(self.metrics_history) > 100:
                self.metrics_history = self.metrics_history[-100:]
            
            # Check thresholds
            self._check_performance_thresholds(metrics)
            
            return result
        return wrapper
    
    def measure_contrast_check(self, func):
        """Decorator để measure contrast checking performance"""
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            result = func(*args, **kwargs)
            
            end_time = time.time()
            
            # Record metrics
            metrics = PerformanceMetrics(
                timestamp=datetime.now(),
                theme_switch_time=0,  # Not applicable here
                contrast_check_time=(end_time - start_time) * 1000,  # Convert to ms
                render_time=0,  # Not applicable here
                memory_usage=0,  # Not applicable here
                cpu_usage=psutil.cpu_percent()
            )
            
            self.metrics_history.append(metrics)
            self._check_performance_thresholds(metrics)
            
            return result
        return wrapper
    
    def _check_performance_thresholds(self, metrics: PerformanceMetrics):
        """Check if metrics exceed thresholds"""
        violations = []
        
        if metrics.theme_switch_time > self.thresholds['theme_switch']:
            violations.append(f"Theme switch time ({metrics.theme_switch_time:.1f}ms) exceeds threshold ({self.thresholds['theme_switch']}ms)")
        
        if metrics.contrast_check_time > self.thresholds['contrast_check']:
            violations.append(f"Contrast check time ({metrics.contrast_check_time:.1f}ms) exceeds threshold ({self.thresholds['contrast_check']}ms)")
        
        if metrics.memory_usage > self.thresholds['memory_usage']:
            violations.append(f"Memory usage ({metrics.memory_usage:.1f}MB) exceeds threshold ({self.thresholds['memory_usage']}MB)")
        
        if metrics.cpu_usage > self.thresholds['cpu_usage']:
            violations.append(f"CPU usage ({metrics.cpu_usage:.1f}%) exceeds threshold ({self.thresholds['cpu_usage']}%)")
        
        # Log violations (in production, send to monitoring service)
        if violations:
            for violation in violations:
                st.warning(f"⚠️ Performance Warning: {violation}")
    
    def get_performance_dashboard(self) -> str:
        """Generate performance dashboard HTML"""
        if not self.metrics_history:
            return "<p>No performance data available yet.</p>"
        
        latest_metrics = self.metrics_history[-1]
        
        # Calculate averages over last 10 measurements
        recent_metrics = self.metrics_history[-10:]
        avg_theme_switch = sum(m.theme_switch_time for m in recent_metrics) / len(recent_metrics)
        avg_contrast_check = sum(m.contrast_check_time for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m.memory_usage for m in recent_metrics) / len(recent_metrics)
        
        dashboard_html = f"""
        <div class="performance-dashboard">
            <h3>📊 Performance Metrics</h3>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <h4>Theme Switch Time</h4>
                    <div class="metric-value {'good' if latest_metrics.theme_switch_time < self.thresholds['theme_switch'] else 'bad'}">
                        {latest_metrics.theme_switch_time:.1f}ms
                    </div>
                    <div class="metric-avg">Average: {avg_theme_switch:.1f}ms</div>
                </div>
                
                <div class="metric-card">
                    <h4>Contrast Check Time</h4>
                    <div class="metric-value {'good' if latest_metrics.contrast_check_time < self.thresholds['contrast_check'] else 'bad'}">
                        {latest_metrics.contrast_check_time:.1f}ms
                    </div>
                    <div class="metric-avg">Average: {avg_contrast_check:.1f}ms</div>
                </div>
                
                <div class="metric-card">
                    <h4>Memory Usage</h4>
                    <div class="metric-value {'good' if latest_metrics.memory_usage < self.thresholds['memory_usage'] else 'bad'}">
                        {latest_metrics.memory_usage:.1f}MB
                    </div>
                    <div class="metric-avg">Average: {avg_memory:.1f}MB</div>
                </div>
                
                <div class="metric-card">
                    <h4>CPU Usage</h4>
                    <div class="metric-value {'good' if latest_metrics.cpu_usage < self.thresholds['cpu_usage'] else 'bad'}">
                        {latest_metrics.cpu_usage:.1f}%
                    </div>
                    <div class="metric-avg">Current usage</div>
                </div>
            </div>
            
            <div class="performance-status">
                <h4>Status: {'✅ Good' if self._is_performance_good() else '⚠️ Needs Attention'}</h4>
                <p>Last updated: {latest_metrics.timestamp.strftime('%H:%M:%S')}</p>
            </div>
        </div>
        
        <style>
        .performance-dashboard {{
            background: var(--bg_secondary);
            border-radius: 0.75rem;
            padding: 1.5rem;
            margin: 1rem 0;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }}
        
        .metric-card {{
            background: var(--bg_primary);
            border: 1px solid var(--border_primary);
            border-radius: 0.5rem;
            padding: 1rem;
            text-align: center;
        }}
        
        .metric-card h4 {{
            margin: 0 0 0.5rem 0;
            font-size: 0.875rem;
            color: var(--text_secondary);
        }}
        
        .metric-value {{
            font-size: 1.5rem;
            font-weight: 700;
            margin: 0.5rem 0;
        }}
        
        .metric-value.good {{
            color: var(--success);
        }}
        
        .metric-value.bad {{
            color: var(--error);
        }}
        
        .metric-avg {{
            font-size: 0.75rem;
            color: var(--text_tertiary);
        }}
        
        .performance-status {{
            text-align: center;
            padding: 1rem;
            background: var(--bg_accent);
            border-radius: 0.5rem;
            margin-top: 1rem;
        }}
        </style>
        """
        
        return dashboard_html
    
    def _is_performance_good(self) -> bool:
        """Check if current performance is within acceptable ranges"""
        if not self.metrics_history:
            return True
        
        latest = self.metrics_history[-1]
        
        return (
            latest.theme_switch_time <= self.thresholds['theme_switch'] and
            latest.contrast_check_time <= self.thresholds['contrast_check'] and
            latest.memory_usage <= self.thresholds['memory_usage'] and
            latest.cpu_usage <= self.thresholds['cpu_usage']
        )
    
    def export_metrics(self) -> str:
        """Export metrics as JSON"""
        metrics_data = []
        for metric in self.metrics_history:
            metrics_data.append({
                'timestamp': metric.timestamp.isoformat(),
                'theme_switch_time': metric.theme_switch_time,
                'contrast_check_time': metric.contrast_check_time,
                'render_time': metric.render_time,
                'memory_usage': metric.memory_usage,
                'cpu_usage': metric.cpu_usage
            })
        
        return json.dumps(metrics_data, indent=2)

# Global performance monitor instance
performance_monitor = AccessibilityPerformanceMonitor()
```

### 3. Advanced Testing Integration

#### File: `tests/test_accessibility_integration.py`
```python
import pytest
import streamlit as st
from unittest.mock import patch, MagicMock
from ui.accessibility.color_system import AccessibilityColorSystem
from ui.accessibility.contrast_checker import ContrastChecker
from ui.accessibility.theme_manager import ThemeManager

class TestAccessibilityIntegration:
    """Integration tests cho accessibility system"""
    
    @pytest.fixture
    def color_system(self):
        return AccessibilityColorSystem()
    
    @pytest.fixture
    def contrast_checker(self):
        return ContrastChecker()
    
    @pytest.fixture
    def theme_manager(self):
        return ThemeManager()
    
    def test_theme_switching_performance(self, color_system, theme_manager):
        """Test theme switching performance"""
        import time
        
        # Measure theme switching time
        start_time = time.time()
        color_system.switch_theme('dark')
        switch_time = (time.time() - start_time) * 1000  # Convert to ms
        
        # Assert performance is acceptable
        assert switch_time < 300, f"Theme switching took {switch_time:.1f}ms, should be < 300ms"
    
    def test_contrast_calculation_accuracy(self, contrast_checker):
        """Test contrast calculation accuracy"""
        # Test known contrast ratios
        result = contrast_checker.validate_contrast('#000000', '#FFFFFF')
        assert result['contrast_ratio'] >= 21.0  # Maximum contrast
        
        result = contrast_checker.validate_contrast('#808080', '#FFFFFF')
        assert 4.5 <= result['contrast_ratio'] <= 6.0  # Mid-range contrast
        
        result = contrast_checker.validate_contrast('#CCCCCC', '#FFFFFF')
        assert result['contrast_ratio'] < 4.5  # Should fail AA
    
    def test_colorblind_accessibility(self, color_system):
        """Test colorblind-safe color palette"""
        colorblind_colors = color_system.get_colorblind_safe_colors()
        
        # Test all colors are distinguishable
        import itertools
        
        colors = list(colorblind_colors.values())
        for color1, color2 in itertools.combinations(colors, 2):
            # Calculate perceptual distance
            checker = ContrastChecker()
            ratio = checker.calculate_contrast_ratio(color1, color2)
            
            # Colors should be distinguishable (high contrast)
            assert ratio >= 3.0, f"Colors {color1} and {color2} may not be distinguishable"
    
    def test_wcag_compliance(self, color_system):
        """Test WCAG 2.1 AA compliance"""
        light_theme = color_system.light_theme
        dark_theme = color_system.dark_theme
        
        checker = ContrastChecker()
        
        # Test light theme compliance
        for color_name, color_value in light_theme.items():
            if 'text' in color_name:
                bg_color = light_theme.get('bg_primary', '#FFFFFF')
                result = checker.validate_contrast(color_value, bg_color)
                assert result['passes_aa'], f"Light theme {color_name} fails AA standard"
        
        # Test dark theme compliance
        for color_name, color_value in dark_theme.items():
            if 'text' in color_name:
                bg_color = dark_theme.get('bg_primary', '#111827')
                result = checker.validate_contrast(color_value, bg_color)
                assert result['passes_aa'], f"Dark theme {color_name} fails AA standard"
    
    def test_responsive_color_adjustments(self, color_system):
        """Test responsive color adjustments"""
        mobile_colors = color_system.get_responsive_colors('mobile')
        desktop_colors = color_system.get_responsive_colors('desktop')
        
        # Mobile colors should be optimized for touch
        assert mobile_colors['interactive_primary'] != desktop_colors['interactive_primary']
        
        # But semantic colors should remain consistent
        assert mobile_colors['success'] == desktop_colors['success']
        assert mobile_colors['error'] == desktop_colors['error']
    
    def test_theme_persistence(self, theme_manager):
        """Test theme preference persistence"""
        # Set theme
        theme_manager.set_theme('dark')
        assert theme_manager.current_theme == 'dark'
        
        # Simulate page reload (new instance)
        new_manager = ThemeManager()
        assert new_manager.current_theme == 'dark'
    
    def test_accessibility_css_generation(self, color_system):
        """Test accessibility CSS generation"""
        css = color_system.get_accessibility_css()
        
        # Check for essential accessibility features
        assert 'focus' in css.lower()
        assert 'prefers-reduced-motion' in css.lower()
        assert 'prefers-contrast' in css.lower()
        assert 'skip-link' in css.lower()
        assert '.sr-only' in css.lower()
    
    @patch('psutil.cpu_percent')
    @patch('psutil.Process')
    def test_performance_monitoring(self, mock_process, mock_cpu):
        """Test performance monitoring"""
        from ui.performance_monitor import performance_monitor
        
        # Mock system resources
        mock_process.return_value.memory_info.return_value.rss = 100 * 1024 * 1024  # 100MB
        mock_cpu.return_value = 25.0
        
        # Test performance measurement
        @performance_monitor.measure_theme_switch
        def dummy_function():
            time.sleep(0.01)  # 10ms delay
            return "completed"
        
        result = dummy_function()
        assert result == "completed"
        
        # Check metrics were recorded
        assert len(performance_monitor.metrics_history) > 0
        
        latest_metrics = performance_monitor.metrics_history[-1]
        assert latest_metrics.theme_switch_time > 0

# Run tests
if __name__ == "__main__":
    pytest.main([__file__])
```

## Testing và Validation

### 1. Automated Testing Setup

#### File: `scripts/run_accessibility_tests.py`
```python
#!/usr/bin/env python3
"""
Comprehensive accessibility testing script
"""

import sys
import os
import subprocess
import json
from datetime import datetime
from pathlib import Path

def run_command(cmd, capture_output=True):
    """Run shell command with error handling"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=capture_output, 
            text=True,
            check=True
        )
        return result.stdout if capture_output else None
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {cmd}")
        print(f"Error: {e.stderr}")
        return None

def check_dependencies():
    """Check if required tools are installed"""
    print("🔍 Checking dependencies...")
    
    tools = {
        'python': 'python --version',
        'node': 'node --version',
        'npm': 'npm --version',
        'axe': 'npx @axe-core/cli --version'
    }
    
    missing_tools = []
    
    for tool, cmd in tools.items():
        result = run_command(cmd)
        if result is None:
            missing_tools.append(tool)
        else:
            print(f"✅ {tool}: {result.strip()}")
    
    if missing_tools:
        print(f"❌ Missing tools: {', '.join(missing_tools)}")
        print("Please install missing tools before running tests.")
        return False
    
    return True

def run_python_tests():
    """Run Python accessibility tests"""
    print("\n🐍 Running Python accessibility tests...")
    
    # Run pytest
    result = run_command("python -m pytest tests/ -v --tb=short")
    
    if result is not None:
        print("✅ Python tests completed")
        return True
    else:
        print("❌ Python tests failed")
        return False

def run_axe_tests():
    """Run Axe accessibility tests"""
    print("\n🪓 Running Axe accessibility tests...")
    
    # Start Streamlit app in background
    print("Starting Streamlit app...")
    streamlit_process = subprocess.Popen([
        "streamlit", "run", "app.py", 
        "--server.port", "8501",
        "--server.headless", "true"
    ])
    
    # Wait for app to start
    import time
    time.sleep(10)
    
    try:
        # Run Axe tests
        axe_cmd = "npx axe http://localhost:8501 --include-tags=wcag2a,wcag2aa,color-contrast --reporter json"
        result = run_command(axe_cmd)
        
        if result:
            # Parse Axe results
            axe_results = json.loads(result)
            
            # Save results
            with open('axe-results.json', 'w') as f:
                json.dump(axe_results, f, indent=2)
            
            # Check for violations
            violations = axe_results.get('violations', [])
            if violations:
                print(f"❌ Found {len(violations)} accessibility violations:")
                for violation in violations:
                    print(f"  - {violation['id']}: {violation['help']}")
                return False
            else:
                print("✅ No accessibility violations found")
                return True
        else:
            print("❌ Axe tests failed")
            return False
    
    finally:
        # Stop Streamlit app
        streamlit_process.terminate()
        streamlit_process.wait()

def run_colorblind_tests():
    """Run color blindness simulation tests"""
    print("\n👁️ Running color blindness tests...")
    
    # Create test script
    test_script = """
    const puppeteer = require('puppeteer');
    const fs = require('fs');
    
    async function testColorBlindness() {
        const browser = await puppeteer.launch();
        const page = await browser.newPage();
        
        // Navigate to app
        await page.goto('http://localhost:8501');
        await page.waitForTimeout(2000);
        
        // Test color distinction
        const colorTests = await page.evaluate(() => {
            // Test various color combinations
            const colors = ['#3B