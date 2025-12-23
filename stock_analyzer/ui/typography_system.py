"""
Typography System - Hệ thống typography hiện đại và nhất quán cho Stock Analyzer
Đảm bảo readability, accessibility và responsive design
"""

from typing import Dict, Any
import streamlit as st


class TypographySystem:
    """Quản lý typography system với accessibility và responsive design"""
    
    # Typography scale dựa trên 8-point grid system
    TYPE_SCALE = {
        "display": {
            "font_size": "3rem",        # 48px
            "line_height": "1.2",
            "letter_spacing": "-0.02em",
            "font_weight": "800"
        },
        "headline-1": {
            "font_size": "2.25rem",     # 36px
            "line_height": "1.25",
            "letter_spacing": "-0.025em",
            "font_weight": "700"
        },
        "headline-2": {
            "font_size": "1.875rem",    # 30px
            "line_height": "1.25",
            "letter_spacing": "-0.025em",
            "font_weight": "700"
        },
        "headline-3": {
            "font_size": "1.5rem",      # 24px
            "line_height": "1.3",
            "letter_spacing": "-0.025em",
            "font_weight": "600"
        },
        "headline-4": {
            "font_size": "1.25rem",     # 20px
            "line_height": "1.35",
            "letter_spacing": "-0.025em",
            "font_weight": "600"
        },
        "title-1": {
            "font_size": "1.125rem",    # 18px
            "line_height": "1.4",
            "letter_spacing": "0em",
            "font_weight": "600"
        },
        "title-2": {
            "font_size": "1rem",        # 16px
            "line_height": "1.5",
            "letter_spacing": "0em",
            "font_weight": "500"
        },
        "body-large": {
            "font_size": "1rem",        # 16px
            "line_height": "1.625",
            "letter_spacing": "0em",
            "font_weight": "400"
        },
        "body": {
            "font_size": "0.875rem",     # 14px
            "line_height": "1.625",
            "letter_spacing": "0em",
            "font_weight": "400"
        },
        "body-small": {
            "font_size": "0.8125rem",   # 13px
            "line_height": "1.6",
            "letter_spacing": "0em",
            "font_weight": "400"
        },
        "caption": {
            "font_size": "0.75rem",     # 12px
            "line_height": "1.5",
            "letter_spacing": "0.025em",
            "font_weight": "400"
        },
        "label": {
            "font_size": "0.75rem",     # 12px
            "line_height": "1.4",
            "letter_spacing": "0.05em",
            "font_weight": "500"
        },
        "overline": {
            "font_size": "0.6875rem",   # 11px
            "line_height": "1.4",
            "letter_spacing": "0.1em",
            "font_weight": "600"
        }
    }
    
    # Responsive font size adjustments
    RESPONSIVE_SCALE = {
        "mobile": {
            "display": {"font_size": "2rem"},      # 32px
            "headline-1": {"font_size": "1.875rem"}, # 30px
            "headline-2": {"font_size": "1.5rem"},   # 24px
            "headline-3": {"font_size": "1.25rem"},  # 20px
            "headline-4": {"font_size": "1.125rem"}, # 18px
        },
        "tablet": {
            "display": {"font_size": "2.5rem"},     # 40px
            "headline-1": {"font_size": "2rem"},      # 32px
            "headline-2": {"font_size": "1.75rem"},   # 28px
        }
    }
    
    @classmethod
    def get_typography_css(cls) -> str:
        """Generate CSS variables cho typography system"""
        css_vars = []
        
        # Base typography scale
        for style_name, properties in cls.TYPE_SCALE.items():
            css_vars.append(f"    --text-{style_name}: {properties['font_size']};")
            css_vars.append(f"    --leading-{style_name}: {properties['line_height']};")
            css_vars.append(f"    --tracking-{style_name}: {properties['letter_spacing']};")
            css_vars.append(f"    --font-weight-{style_name}: {properties['font_weight']};")
        
        return "\n".join(css_vars)
    
    @classmethod
    def get_responsive_typography_css(cls) -> str:
        """Generate responsive typography CSS"""
        responsive_css = []
        
        # Mobile breakpoints
        responsive_css.append("""
    /* Mobile Typography */
    @media (max-width: 768px) {
        :root {""")
        
        for style_name, properties in cls.RESPONSIVE_SCALE["mobile"].items():
            responsive_css.append(f"            --text-{style_name}: {properties['font_size']};")
        
        responsive_css.append("""
        }
    }
    
    /* Tablet Typography */
    @media (min-width: 769px) and (max-width: 1024px) {
        :root {""")
        
        for style_name, properties in cls.RESPONSIVE_SCALE["tablet"].items():
            responsive_css.append(f"            --text-{style_name}: {properties['font_size']};")
        
        responsive_css.append("""
        }
    }""")
        
        return "\n".join(responsive_css)
    
    @classmethod
    def create_heading(cls, text: str, level: int = 1, 
                    style: str = None, color: str = None, 
                    weight: str = None, align: str = None,
                    margin_bottom: str = None) -> str:
        """
        Create heading với typography classes
        
        Args:
            text: Text content
            level: Heading level (1-6)
            style: Typography style from TYPE_SCALE
            color: Custom color
            weight: Font weight override
            align: Text alignment
            margin_bottom: Custom margin bottom
        """
        if style is None:
            style_map = {1: "headline-1", 2: "headline-2", 3: "headline-3", 
                        4: "headline-4", 5: "title-1", 6: "title-2"}
            style = style_map.get(level, "headline-2")
        
        properties = cls.TYPE_SCALE[style]
        
        # Build inline styles
        styles = []
        styles.append(f"font-size: var(--text-{style})")
        styles.append(f"line-height: var(--leading-{style})")
        styles.append(f"letter-spacing: var(--tracking-{style})")
        styles.append(f"font-weight: var(--font-weight-{style})")
        
        if color:
            styles.append(f"color: {color}")
        if weight:
            styles.append(f"font-weight: {weight}")
        if align:
            styles.append(f"text-align: {align}")
        if margin_bottom:
            styles.append(f"margin-bottom: {margin_bottom}")
        
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        style_str = "; ".join(styles)
        return f"""
        <p class="typography-caption" style="{style_str}">
            {text}
        </p>
        """
    
    @classmethod
    def create_body_text(cls, text: str, size: str = "body", 
                       color: str = None, weight: str = None,
                       align: str = None, margin: str = None) -> str:
        """Create body text với typography system"""
        properties = cls.TYPE_SCALE[size]
        
        styles = []
        styles.append(f"font-size: var(--text-{size})")
        styles.append(f"line-height: var(--leading-{size})")
        styles.append(f"letter-spacing: var(--tracking-{size})")
        styles.append(f"font-weight: var(--font-weight-{size})")
        
        if color:
            styles.append(f"color: {color}")
        if weight:
            styles.append(f"font-weight: {weight}")
        if align:
            styles.append(f"text-align: {align}")
        if margin:
            styles.append(f"margin: {margin}")
        
        style_str = "; ".join(styles)
        return f"""
        <p class="typography-body" style="{style_str}">
            {text}
        </p>
        """
    
    @classmethod
    def create_caption(cls, text: str, color: str = None, 
                     align: str = None, margin_top: str = None) -> str:
        """Create caption text"""
        properties = cls.TYPE_SCALE["caption"]
        
        styles = []
        styles.append(f"font-size: var(--text-caption)")
        styles.append(f"line-height: var(--leading-caption)")
        styles.append(f"letter-spacing: var(--tracking-caption)")
        styles.append(f"font-weight: var(--font-weight-caption)")
        
        if color:
            styles.append(f"color: {color}")
        if align:
            styles.append(f"text-align: {align}")
        if margin_top:
            styles.append(f"margin-top: {margin_top}")
        
        style_str = "; ".join(styles)
        return f"""
        <p class="typography-caption" style="{style_str}">
            {text}
        </p>
        """
    
    @classmethod
    def create_label(cls, text: str, color: str = None, 
                   uppercase: bool = True, margin_bottom: str = None) -> str:
        """Create label text"""
        properties = cls.TYPE_SCALE["label"]
        
        styles = []
        styles.append(f"font-size: var(--text-label)")
        styles.append(f"line-height: var(--leading-label)")
        styles.append(f"letter-spacing: var(--tracking-label)")
        styles.append(f"font-weight: var(--font-weight-label)")
        
        if uppercase:
            styles.append("text-transform: uppercase")
        if color:
            styles.append(f"color: {color}")
        if margin_bottom:
            styles.append(f"margin-bottom: {margin_bottom}")
        
        style_str = "; ".join(styles)
        return f"""
        <label class="typography-label" style="{style_str}">
            {text}
        </label>
        """


# Utility functions cho Streamlit integration
def render_heading(text: str, level: int = 1, **kwargs):
    """Render heading trong Streamlit"""
    heading_html = TypographySystem.create_heading(text, level, **kwargs)
    st.markdown(heading_html, unsafe_allow_html=True)


def render_body_text(text: str, size: str = "body", **kwargs):
    """Render body text trong Streamlit"""
    body_html = TypographySystem.create_body_text(text, size, **kwargs)
    st.markdown(body_html, unsafe_allow_html=True)


def render_caption(text: str, **kwargs):
    """Render caption trong Streamlit"""
    caption_html = TypographySystem.create_caption(text, **kwargs)
    st.markdown(caption_html, unsafe_allow_html=True)


def render_label(text: str, **kwargs):
    """Render label trong Streamlit"""
    label_html = TypographySystem.create_label(text, **kwargs)
    st.markdown(label_html, unsafe_allow_html=True)


# Export main class và utilities
__all__ = [
    'TypographySystem',
    'render_heading',
    'render_body_text', 
    'render_caption',
    'render_label'
]
