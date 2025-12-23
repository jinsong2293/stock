"""
Mobile-First Responsive Components cho Stock Analyzer
Cải thiện trải nghiệm người dùng trên mobile và desktop
"""

import streamlit as st
from typing import Dict, Any, List, Optional
import plotly.graph_objects as go


class ResponsiveLayoutManager:
    """
    Quản lý responsive layout cho Stock Analyzer
    """
    
    def __init__(self):
        # Mobile breakpoints
        self.mobile_breakpoint = 768
        self.tablet_breakpoint = 1024
        
        # Responsive column configurations
        self.columns_config = {
            'mobile': {
                'chart': 1,
                'metrics': 1,
                'details': 1,
                'sidebar': 'collapsed'
            },
            'tablet': {
                'chart': 1,
                'metrics': 2,
                'details': 2,
                'sidebar': 'collapsed'
            },
            'desktop': {
                'chart': 2,
                'metrics': 4,
                'details': 3,
                'sidebar': 'expanded'
            }
        }
    
    def get_device_type(self) -> str:
        """
        Detect device type based on screen width
        Note: Streamlit không có direct screen width detection,
        sử dụng fallback logic dựa trên available space
        """
        # Fallback: sử dụng session state để detect device type
        if 'device_type' not in st.session_state:
            # Check if we're on mobile based on container width
            main_container = st.empty()
            # This is a simplified approach - trong thực tế có thể dùng JavaScript
            st.session_state['device_type'] = 'desktop'  # Default to desktop
        
        return st.session_state.get('device_type', 'desktop')
    
    def get_responsive_columns(self, content_type: str) -> List[int]:
        """
        Get responsive column configuration cho content type
        """
        device = self.get_device_type()
        config = self.columns_config[device]
        
        column_map = {
            'chart': [config['chart']],
            'metrics': [1] * config['metrics'],
            'details': [1] * config['details']
        }
        
        return column_map.get(content_type, [1])
    
    def create_responsive_metric_grid(self, metrics_data: List[Dict[str, Any]]):
        """
        Create responsive metric grid với automatic column adjustment
        """
        device = self.get_device_type()
        
        if device == 'mobile':
            # Single column for mobile
            for metric in metrics_data:
                with st.container():
                    self._render_metric_card(metric, mobile=True)
                    st.markdown("---")
        
        elif device == 'tablet':
            # 2 columns for tablet
            cols = st.columns(2)
            for i, metric in enumerate(metrics_data):
                with cols[i % 2]:
                    self._render_metric_card(metric, mobile=False)
        
        else:  # desktop
            # Dynamic columns based on number of metrics
            num_cols = min(len(metrics_data), 4)
            cols = st.columns(num_cols)
            for i, metric in enumerate(metrics_data):
                with cols[i % num_cols]:
                    self._render_metric_card(metric, mobile=False)
    
    def _render_metric_card(self, metric: Dict[str, Any], mobile: bool = False):
        """
        Render individual metric card với mobile optimization
        """
        label = metric.get('label', '')
        value = metric.get('value', '')
        delta = metric.get('delta', '')
        icon = metric.get('icon', '')
        
        if mobile:
            # Mobile-friendly metric card
            st.markdown(f"""
            <div style="
                background: var(--bg_secondary, #f8f9fa); 
                padding: 1rem; 
                border-radius: 0.5rem; 
                margin-bottom: 0.5rem;
                border-left: 4px solid var(--primary, #007bff);
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <span style="margin-right: 0.5rem; font-size: 1.2rem;">{icon}</span>
                    <span style="font-size: 0.875rem; color: #6c757d;">{label}</span>
                </div>
                <div style="font-size: 1.5rem; font-weight: bold; color: var(--text_primary, #212529);">
                    {value}
                </div>
                {f'<div style="font-size: 0.75rem; color: #28a745; margin-top: 0.25rem;">{delta}</div>' if delta else ''}
            </div>
            """, unsafe_allow_html=True)
        else:
            # Desktop metric card
            st.metric(
                label=f"{icon} {label}" if icon else label,
                value=value,
                delta=delta
            )


class EnhancedLoadingStates:
    """
    Enhanced loading states với skeleton screens và progressive loading
    """
    
    @staticmethod
    def create_skeleton_chart(height: int = 400):
        """
        Create skeleton loading cho charts
        """
        st.markdown(f"""
        <div style="
            background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
            background-size: 200% 100%;
            animation: loading 1.5s infinite;
            height: {height}px;
            border-radius: 0.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #666;
            font-size: 0.9rem;
        ">
            📊 Loading chart data...
        </div>
        
        <style>
        @keyframes loading {{
            0% {{ background-position: 200% 0; }}
            100% {{ background-position: -200% 0; }}
        }}
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_skeleton_table(rows: int = 5, cols: int = 4):
        """
        Create skeleton loading cho tables
        """
        skeleton_rows = []
        for i in range(rows):
            row_cells = []
            for j in range(cols):
                row_cells.append(f"""
                <td style="
                    background: #f0f0f0;
                    height: 2rem;
                    border-radius: 0.25rem;
                    animation: pulse 1.5s infinite;
                "></td>
                """)
            skeleton_rows.append(f"<tr>{''.join(row_cells)}</tr>")
        
        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 0.5rem; border: 1px solid #e0e0e0;">
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr>
                        {''.join([f'<th style="height: 2rem; background: #f8f9fa; border-bottom: 2px solid #dee2e6;"></th>' for _ in range(cols)])}
                    </tr>
                </thead>
                <tbody>
                    {''.join(skeleton_rows)}
                </tbody>
            </table>
        </div>
        
        <style>
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_analysis_progress(analysis_type: str, stage: int, total_stages: int):
        """
        Create enhanced progress indicator cho analysis
        """
        stages = {
            'full_analysis': ['📊 Loading data', '🔍 Technical analysis', '📈 Sentiment analysis', '💰 Financial analysis', '✅ Complete'],
            'scanner': ['🔍 Initializing scanner', '📊 Batch processing', '⚡ Parallel analysis', '📋 Results compilation', '✅ Complete'],
            'backtesting': ['📊 Loading historical data', '🔄 Running strategy', '📈 Calculating metrics', '📋 Generating report', '✅ Complete']
        }
        
        stage_names = stages.get(analysis_type, [f'Stage {i+1}' for i in range(total_stages)])
        
        progress_value = (stage - 1) / (total_stages - 1)
        current_stage_name = stage_names[min(stage - 1, len(stage_names) - 1)]
        
        st.markdown(f"""
        <div style="
            background: var(--bg_secondary, #f8f9fa); 
            padding: 1.5rem; 
            border-radius: 0.75rem; 
            border: 1px solid var(--border_light, #dee2e6);
            margin: 1rem 0;
        ">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div style="
                    width: 2rem; 
                    height: 2rem; 
                    background: var(--primary, #007bff); 
                    border-radius: 50%; 
                    display: flex; 
                    align-items: center; 
                    justify-content: center;
                    color: white;
                    font-weight: bold;
                    margin-right: 1rem;
                ">
                    {stage}
                </div>
                <div>
                    <h4 style="margin: 0; color: var(--text_primary, #212529);">{current_stage_name}</h4>
                    <p style="margin: 0.25rem 0 0 0; color: var(--text_secondary, #6c757d); font-size: 0.875rem;">
                        Stage {stage} of {total_stages}
                    </p>
                </div>
            </div>
            
            <div style="
                background: #e9ecef; 
                height: 0.5rem; 
                border-radius: 0.25rem; 
                overflow: hidden;
            ">
                <div style="
                    background: linear-gradient(90deg, var(--primary, #007bff), var(--primary_dark, #0056b3));
                    height: 100%; 
                    width: {progress_value * 100}%; 
                    border-radius: 0.25rem;
                    transition: width 0.3s ease;
                "></div>
            </div>
        </div>
        """, unsafe_allow_html=True)


class ErrorHandlingUI:
    """
    User-friendly error handling components
    """
    
    @staticmethod
    def display_user_friendly_error(error_type: str, ticker: str = "", details: str = ""):
        """
        Display user-friendly error messages
        """
        error_messages = {
            'network': {
                'icon': '🔌',
                'title': 'Connection Error',
                'message': 'Unable to connect to data server. Please check your internet connection.',
                'action': 'Try again in a few moments'
            },
            'data_not_found': {
                'icon': '📊',
                'title': 'Data Not Available',
                'message': f'No data found for ticker "{ticker}".',
                'action': 'Check if the ticker symbol is correct'
            },
            'analysis_failed': {
                'icon': '⚠️',
                'title': 'Analysis Failed',
                'message': 'Unable to complete analysis due to insufficient data.',
                'action': 'Try with a different time range or ticker'
            },
            'api_rate_limit': {
                'icon': '⏱️',
                'title': 'Rate Limit Exceeded',
                'message': 'Too many requests. Please wait before trying again.',
                'action': 'Wait a few minutes and retry'
            },
            'invalid_input': {
                'icon': '❌',
                'title': 'Invalid Input',
                'message': 'Please check your input parameters.',
                'action': 'Verify all input values are correct'
            }
        }
        
        error_info = error_messages.get(error_type, error_messages['analysis_failed'])
        
        st.markdown(f"""
        <div style="
            background: #fff3cd; 
            border: 1px solid #ffeaa7; 
            border-left: 4px solid #f39c12;
            border-radius: 0.5rem; 
            padding: 1.5rem; 
            margin: 1rem 0;
        ">
            <div style="display: flex; align-items: flex-start;">
                <span style="font-size: 2rem; margin-right: 1rem;">{error_info['icon']}</span>
                <div style="flex: 1;">
                    <h4 style="margin: 0 0 0.5rem 0; color: #856404;">
                        {error_info['title']}
                    </h4>
                    <p style="margin: 0 0 0.5rem 0; color: #856404;">
                        {error_info['message']}
                    </p>
                    {f'<p style="margin: 0; font-size: 0.875rem; color: #6c5014;"><strong>Details:</strong> {details}</p>' if details else ''}
                    <p style="margin: 0.5rem 0 0 0; font-size: 0.875rem; color: #6c5014;">
                        💡 <strong>Suggestion:</strong> {error_info['action']}
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def display_retry_button(callback, button_text: str = "Try Again"):
        """
        Display retry button với callback
        """
        if st.button(button_text, type="primary"):
            callback()


class ProgressiveLoadingComponent:
    """
    Progressive loading cho heavy components
    """
    
    @staticmethod
    def create_lazy_chart(chart_func, *args, **kwargs):
        """
        Create chart với lazy loading
        """
        with st.spinner("Loading chart..."):
            try:
                return chart_func(*args, **kwargs)
            except Exception as e:
                ErrorHandlingUI.display_user_friendly_error('analysis_failed', details=str(e))
                return None
    
    @staticmethod
    def create_lazy_dataframe(data_func, *args, **kwargs):
        """
        Create dataframe với lazy loading
        """
        with st.spinner("Loading data..."):
            try:
                data = data_func(*args, **kwargs)
                if data is not None and not data.empty:
                    return data
                else:
                    st.info("No data available")
                    return None
            except Exception as e:
                ErrorHandlingUI.display_user_friendly_error('analysis_failed', details=str(e))
                return None


class MobileOptimizedNavigation:
    """
    Mobile-optimized navigation components
    """
    
    @staticmethod
    def create_mobile_friendly_sidebar():
        """
        Create mobile-friendly collapsible sidebar
        """
        # Check if we're on mobile (simplified detection)
        if 'sidebar_collapsed' not in st.session_state:
            st.session_state.sidebar_collapsed = False
        
        # Mobile-friendly sidebar toggle
        col1, col2 = st.columns([1, 4])
        
        with col1:
            if st.button("☰", key="sidebar_toggle"):
                st.session_state.sidebar_collapsed = not st.session_state.sidebar_collapsed
        
        with col2:
            st.markdown("### 📈 Stock Analyzer")
        
        # Sidebar content (collapsible on mobile)
        if not st.session_state.sidebar_collapsed:
            with st.sidebar:
                st.markdown("---")
                st.markdown("**Navigation**")
                # Navigation items would go here
                
                st.markdown("---")
                st.markdown("**Quick Actions**")
                # Quick action buttons would go here
    
    @staticmethod
    def create_tab_navigation(tabs_data: List[Dict[str, Any]]):
        """
        Create mobile-friendly tab navigation
        """
        tab_labels = [tab.get('label', '') for tab in tabs_data]
        tab_icons = [tab.get('icon', '') for tab in tabs_data]
        
        # Add icons to labels
        labeled_tabs = []
        for i, (label, icon) in enumerate(zip(tab_labels, tab_icons)):
            if icon:
                labeled_tabs.append(f"{icon} {label}")
            else:
                labeled_tabs.append(label)
        
        return st.tabs(labeled_tabs)


# Utility functions
def get_device_info() -> Dict[str, Any]:
    """
    Get device information for responsive design
    """
    return {
        'device_type': 'desktop',  # Default fallback
        'screen_width': 'unknown',
        'is_mobile': False,
        'is_tablet': False,
        'is_desktop': True
    }


def create_responsive_container(content_func, *args, **kwargs):
    """
    Create responsive container with automatic layout adjustment
    """
    device_info = get_device_info()
    
    if device_info['is_mobile']:
        # Mobile: single column
        with st.container():
            content_func(*args, **kwargs)
    else:
        # Desktop/tablet: use main content area
        content_func(*args, **kwargs)


# Export main classes
__all__ = [
    'ResponsiveLayoutManager',
    'EnhancedLoadingStates', 
    'ErrorHandlingUI',
    'ProgressiveLoadingComponent',
    'MobileOptimizedNavigation'
]


if __name__ == "__main__":
    # Test responsive components
    st.set_page_config(page_title="Responsive Components Test", layout="wide")
    
    # Test loading states
    st.subheader("Loading States Test")
    EnhancedLoadingStates.create_skeleton_chart(300)
    EnhancedLoadingStates.create_skeleton_table(3, 4)
    EnhancedLoadingStates.create_analysis_progress('full_analysis', 3, 5)
    
    # Test error handling
    st.subheader("Error Handling Test")
    ErrorHandlingUI.display_user_friendly_error('network', 'AAA', 'Connection timeout')
    
    # Test responsive metrics
    st.subheader("Responsive Metrics Test")
    layout_manager = ResponsiveLayoutManager()
    test_metrics = [
        {'label': 'Price', 'value': '$150.25', 'delta': '+2.5%', 'icon': '💰'},
        {'label': 'Volume', 'value': '1.2M', 'delta': '+15%', 'icon': '📊'},
        {'label': 'RSI', 'value': '65.4', 'delta': 'Neutral', 'icon': '📈'},
        {'label': 'Market Cap', 'value': '$2.5B', 'delta': '+5%', 'icon': '🏢'}
    ]
    layout_manager.create_responsive_metric_grid(test_metrics)