"""
Accessible theme toggle component for Streamlit
Tạo nút chuyển đổi theme với accessibility features

Author: Roo - Architect Mode
Version: 1.0.0
"""

import streamlit as st
from typing import Optional

def create_theme_toggle(
    key: str = "theme_toggle",
    label: str = "Theme",
    show_labels: bool = True
) -> Optional[str]:
    """Tạo accessible theme toggle component"""
    
    # Get current theme from session state
    current_theme = st.session_state.get('theme_preference', 'light')
    
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
            st.session_state.theme_preference = new_theme
            
            # Import and use theme manager if available
            try:
                from ..accessibility.theme_manager import ThemeManager
                from ..accessibility.color_system import AccessibilityColorSystem
                
                color_system = AccessibilityColorSystem()
                theme_manager = ThemeManager(color_system)
                theme_manager.set_theme(new_theme)
            except ImportError:
                # Fallback if components not available
                st.rerun()
    
    return st.session_state.get('theme_preference', 'light')

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
            color: var(--text_inverse);
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

def create_accessibility_controls() -> None:
    """Tạo accessibility controls panel"""
    with st.expander("♿ Accessibility Settings", expanded=False):
        st.markdown("**Display Options**")
        
        # Colorblind mode toggle
        cb_mode = st.checkbox(
            "Colorblind Mode", 
            value=st.session_state.get('colorblind_mode', False),
            help="Enable colorblind-friendly color schemes"
        )
        if cb_mode != st.session_state.get('colorblind_mode', False):
            st.session_state.colorblind_mode = cb_mode
            st.rerun()
        
        # High contrast toggle
        hc_mode = st.checkbox(
            "High Contrast", 
            value=st.session_state.get('high_contrast', False),
            help="Enable high contrast mode"
        )
        if hc_mode != st.session_state.get('high_contrast', False):
            st.session_state.high_contrast = hc_mode
            st.rerun()
        
        # Reduced motion toggle
        rm_mode = st.checkbox(
            "Reduced Motion", 
            value=st.session_state.get('reduced_motion', False),
            help="Reduce animations and transitions"
        )
        if rm_mode != st.session_state.get('reduced_motion', False):
            st.session_state.reduced_motion = rm_mode
            st.rerun()
        
        # Font size control
        font_size = st.selectbox(
            "Font Size",
            options=["Small", "Medium", "Large"],
            index=["Small", "Medium", "Large"].index(
                st.session_state.get('font_size', 'Medium')
            ),
            help="Adjust font size for better readability"
        )
        if font_size != st.session_state.get('font_size', 'Medium'):
            st.session_state.font_size = font_size
            st.rerun()
        
        # Add CSS for accessibility features
        add_accessibility_css()

def add_accessibility_css():
    """Add CSS for accessibility features"""
    
    # Get current settings
    font_size = st.session_state.get('font_size', 'Medium')
    high_contrast = st.session_state.get('high_contrast', False)
    reduced_motion = st.session_state.get('reduced_motion', False)
    
    # Font size CSS
    font_size_css = {
        "Small": "0.875rem",
        "Medium": "1rem", 
        "Large": "1.125rem"
    }.get(font_size, "1rem")
    
    # High contrast CSS
    high_contrast_css = ""
    if high_contrast:
        high_contrast_css = """
        :root {
            --bg_primary: #000000 !important;
            --text_primary: #FFFFFF !important;
            --interactive_primary: #FFFF00 !important;
            --border_primary: #FFFFFF !important;
        }
        
        .stButton > button {
            border: 2px solid var(--interactive_primary) !important;
        }
        """
    
    # Reduced motion CSS
    reduced_motion_css = ""
    if reduced_motion:
        reduced_motion_css = """
        * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
        """
    
    # Combine all CSS
    css = f"""
    <style>
    /* Font size adjustment */
    .stApp, .main, .block-container {{
        font-size: {font_size_css};
    }}
    
    /* High contrast mode */
    {high_contrast_css}
    
    /* Reduced motion */
    {reduced_motion_css}
    
    /* Focus indicators */
    .stButton > button:focus,
    .stSelectbox > div > div:focus-within,
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {{
        outline: 2px solid var(--border_focus) !important;
        outline-offset: 2px !important;
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
    
    /* Skip link */
    .skip-link {{
        position: absolute;
        top: -40px;
        left: 6px;
        background: var(--interactive_primary);
        color: var(--text_inverse);
        padding: 8px 16px;
        text-decoration: none;
        border-radius: 4px;
        z-index: 1000;
        font-weight: 600;
    }}
    
    .skip-link:focus {{
        top: 6px;
    }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)