"""
Enhanced Grid System and Spacing for Accessibility
Implements consistent 8px grid system with touch-friendly design and balanced layouts
"""

import streamlit as st
from typing import Dict, Any, List, Optional, Tuple
import json


class EnhancedGridSystem:
    """Complete accessibility-focused grid and spacing system"""
    
    # 8px Base Grid System
    # All spacing values are multiples of 8px for consistency
    GRID_SYSTEM = {
        # Base unit: 8px
        "base_unit": 8,
        
        # Spacing scale (in pixels)
        "spacing": {
            "0": 0,          # 0px
            "1": 8,          # 8px  - Tight spacing
            "2": 16,         # 16px - Small spacing
            "3": 24,         # 24px - Medium spacing
            "4": 32,         # 32px - Large spacing
            "5": 40,         # 40px - Extra large spacing
            "6": 48,         # 48px - Section spacing
            "8": 64,         # 64px - Large section spacing
            "10": 80,        # 80px - Page spacing
            "12": 96,        # 96px - Major section spacing
            "16": 128,       # 128px - Page margins
            "20": 160,       # 160px - Large page spacing
            "24": 192,       # 192px - Maximum spacing
        },
        
        # Container max-widths for different screen sizes
        "containers": {
            "xs": "475px",   # Extra small screens
            "sm": "640px",   # Small screens
            "md": "768px",   # Medium screens
            "lg": "1024px",  # Large screens
            "xl": "1280px",  # Extra large screens
            "2xl": "1536px", # 2X large screens
            "full": "100%",  # Full width
        },
        
        # Grid columns
        "columns": {
            "1": "8.333333%",   # 1/12
            "2": "16.666667%",  # 2/12
            "3": "25%",         # 3/12
            "4": "33.333333%",  # 4/12
            "5": "41.666667%",  # 5/12
            "6": "50%",         # 6/12
            "7": "58.333333%",  # 7/12
            "8": "66.666667%",  # 8/12
            "9": "75%",         # 9/12
            "10": "83.333333%", # 10/12
            "11": "91.666667%", # 11/12
            "12": "100%",       # 12/12
        },
        
        # Gutter sizes
        "gutters": {
            "none": "0",
            "sm": "16px",      # Small gutter
            "md": "24px",      # Medium gutter
            "lg": "32px",      # Large gutter
            "xl": "48px",      # Extra large gutter
        },
        
        # Breakpoints for responsive design
        "breakpoints": {
            "xs": "475px",     # Extra small devices
            "sm": "640px",     # Small devices
            "md": "768px",     # Medium devices
            "lg": "1024px",    # Large devices
            "xl": "1280px",    # Extra large devices
            "2xl": "1536px",   # 2X large devices
        }
    }
    
    # Touch-friendly design specifications
    TOUCH_SPECIFICATIONS = {
        "minimum_touch_target": "44px",      # WCAG minimum
        "recommended_touch_target": "48px",  # Better usability
        "touch_spacing": "8px",              # Space between touch targets
        "finger_width": "8-12mm",            # Average finger width
        "thumb_target": "48px",              # Thumb-friendly size
    }
    
    # Component spacing guidelines
    COMPONENT_SPACING = {
        "form_elements": {
            "label_to_input": "8px",        # Space between label and input
            "input_to_input": "16px",       # Space between adjacent inputs
            "input_to_help": "4px",         # Space between input and help text
            "button_group": "8px",          # Space between buttons in a group
        },
        "content_blocks": {
            "paragraph_to_paragraph": "16px",  # Space between paragraphs
            "section_to_section": "48px",      # Space between major sections
            "card_to_card": "24px",            # Space between cards
            "list_items": "8px",               # Space between list items
        },
        "navigation": {
            "nav_items": "16px",              # Space between navigation items
            "nav_to_content": "32px",         # Space between nav and content
            "breadcrumb_items": "8px",        # Space between breadcrumb items
        }
    }
    
    # Layout patterns for different content types
    LAYOUT_PATTERNS = {
        "dashboard": {
            "description": "Multi-column dashboard layout",
            "columns": [4, 4, 4],  # Three equal columns
            "gutter": "24px",
            "breakpoint": "lg"
        },
        "form": {
            "description": "Single-column form layout",
            "columns": [12],
            "gutter": "24px",
            "breakpoint": "md"
        },
        "detail_page": {
            "description": "Main content with sidebar",
            "columns": [8, 4],    # 2/3 main, 1/3 sidebar
            "gutter": "32px",
            "breakpoint": "lg"
        },
        "gallery": {
            "description": "Responsive grid gallery",
            "columns": [3, 3, 3, 3],  # Four equal columns
            "gutter": "16px",
            "breakpoint": "md"
        },
        "landing": {
            "description": "Hero section with content blocks",
            "columns": [12],
            "gutter": "48px",
            "breakpoint": "lg"
        }
    }
    
    @classmethod
    def get_grid_css(cls) -> str:
        """Generate comprehensive CSS for the grid system"""
        
        css = f"""
        /* Enhanced Grid System and Spacing - Accessibility Focused */
        
        :root {{
            /* 8px Base Grid System */
            --grid-base: {cls.GRID_SYSTEM["base_unit"]}px;
            
            /* Spacing Scale */
            {chr(10).join([f'    --space-{k}: {v}px;' for k, v in cls.GRID_SYSTEM["spacing"].items()])}
            
            /* Container Max Widths */
            {chr(10).join([f'    --container-{k}: {v};' for k, v in cls.GRID_SYSTEM["containers"].items()])}
            
            /* Grid Columns */
            {chr(10).join([f'    --col-{k}: {v};' for k, v in cls.GRID_SYSTEM["columns"].items()])}
            
            /* Gutters */
            {chr(10).join([f'    --gutter-{k}: {v};' for k, v in cls.GRID_SYSTEM["gutters"].items()])}
            
            /* Breakpoints */
            {chr(10).join([f'    --breakpoint-{k}: {v};' for k, v in cls.GRID_SYSTEM["breakpoints"].items()])}
            
            /* Touch Specifications */
            --touch-target-min: {cls.TOUCH_SPECIFICATIONS["minimum_touch_target"]};
            --touch-target-recommended: {cls.TOUCH_SPECIFICATIONS["recommended_touch_target"]};
            --touch-spacing: {cls.TOUCH_SPECIFICATIONS["touch_spacing"]};
        }}
        
        /* Base Layout Classes */
        .container {{
            width: 100%;
            margin-left: auto;
            margin-right: auto;
            padding-left: var(--space-4);
            padding-right: var(--space-4);
        }}
        
        /* Container Sizes */
        .container-xs {{ max-width: var(--container-xs); }}
        .container-sm {{ max-width: var(--container-sm); }}
        .container-md {{ max-width: var(--container-md); }}
        .container-lg {{ max-width: var(--container-lg); }}
        .container-xl {{ max-width: var(--container-xl); }}
        .container-2xl {{ max-width: var(--container-2xl); }}
        .container-full {{ max-width: 100%; }}
        
        /* Grid System */
        .grid {{
            display: grid;
            gap: var(--gutter-md);
        }}
        
        /* Column Classes */
        .col-1 {{ grid-column: span 1 / span 1; }}
        .col-2 {{ grid-column: span 2 / span 2; }}
        .col-3 {{ grid-column: span 3 / span 3; }}
        .col-4 {{ grid-column: span 4 / span 4; }}
        .col-5 {{ grid-column: span 5 / span 5; }}
        .col-6 {{ grid-column: span 6 / span 6; }}
        .col-7 {{ grid-column: span 7 / span 7; }}
        .col-8 {{ grid-column: span 8 / span 8; }}
        .col-9 {{ grid-column: span 9 / span 9; }}
        .col-10 {{ grid-column: span 10 / span 10; }}
        .col-11 {{ grid-column: span 11 / span 11; }}
        .col-12 {{ grid-column: span 12 / span 12; }}
        
        /* Auto-fit columns */
        .col-auto {{ grid-column: auto; }}
        .col-span-full {{ grid-column: 1 / -1; }}
        
        /* Flexbox utilities */
        .flex {{ display: flex; }}
        .flex-col {{ flex-direction: column; }}
        .flex-row {{ flex-direction: row; }}
        .flex-wrap {{ flex-wrap: wrap; }}
        .flex-nowrap {{ flex-wrap: nowrap; }}
        
        /* Flex alignment */
        .items-start {{ align-items: flex-start; }}
        .items-center {{ align-items: center; }}
        .items-end {{ align-items: flex-end; }}
        .items-stretch {{ align-items: stretch; }}
        
        .justify-start {{ justify-content: flex-start; }}
        .justify-center {{ justify-content: center; }}
        .justify-end {{ justify-content: flex-end; }}
        .justify-between {{ justify-content: space-between; }}
        .justify-around {{ justify-content: space-around; }}
        
        /* Spacing Utilities */
        /* Margin */
        .m-0 {{ margin: var(--space-0); }}
        .m-1 {{ margin: var(--space-1); }}
        .m-2 {{ margin: var(--space-2); }}
        .m-3 {{ margin: var(--space-3); }}
        .m-4 {{ margin: var(--space-4); }}
        .m-5 {{ margin: var(--space-5); }}
        .m-6 {{ margin: var(--space-6); }}
        .m-8 {{ margin: var(--space-8); }}
        .m-10 {{ margin: var(--space-10); }}
        .m-12 {{ margin: var(--space-12); }}
        .m-16 {{ margin: var(--space-16); }}
        .m-20 {{ margin: var(--space-20); }}
        .m-24 {{ margin: var(--space-24); }}
        
        /* Margin directions */
        .mt-0 {{ margin-top: var(--space-0); }}
        .mt-1 {{ margin-top: var(--space-1); }}
        .mt-2 {{ margin-top: var(--space-2); }}
        .mt-3 {{ margin-top: var(--space-3); }}
        .mt-4 {{ margin-top: var(--space-4); }}
        .mt-5 {{ margin-top: var(--space-5); }}
        .mt-6 {{ margin-top: var(--space-6); }}
        .mt-8 {{ margin-top: var(--space-8); }}
        .mt-10 {{ margin-top: var(--space-10); }}
        .mt-12 {{ margin-top: var(--space-12); }}
        .mt-16 {{ margin-top: var(--space-16); }}
        
        .mb-0 {{ margin-bottom: var(--space-0); }}
        .mb-1 {{ margin-bottom: var(--space-1); }}
        .mb-2 {{ margin-bottom: var(--space-2); }}
        .mb-3 {{ margin-bottom: var(--space-3); }}
        .mb-4 {{ margin-bottom: var(--space-4); }}
        .mb-5 {{ margin-bottom: var(--space-5); }}
        .mb-6 {{ margin-bottom: var(--space-6); }}
        .mb-8 {{ margin-bottom: var(--space-8); }}
        .mb-10 {{ margin-bottom: var(--space-10); }}
        .mb-12 {{ margin-bottom: var(--space-12); }}
        .mb-16 {{ margin-bottom: var(--space-16); }}
        
        .ml-0 {{ margin-left: var(--space-0); }}
        .ml-1 {{ margin-left: var(--space-1); }}
        .ml-2 {{ margin-left: var(--space-2); }}
        .ml-3 {{ margin-left: var(--space-3); }}
        .ml-4 {{ margin-left: var(--space-4); }}
        .ml-5 {{ margin-left: var(--space-5); }}
        .ml-6 {{ margin-left: var(--space-6); }}
        .ml-8 {{ margin-left: var(--space-8); }}
        
        .mr-0 {{ margin-right: var(--space-0); }}
        .mr-1 {{ margin-right: var(--space-1); }}
        .mr-2 {{ margin-right: var(--space-2); }}
        .mr-3 {{ margin-right: var(--space-3); }}
        .mr-4 {{ margin-right: var(--space-4); }}
        .mr-5 {{ margin-right: var(--space-5); }}
        .mr-6 {{ margin-right: var(--space-6); }}
        .mr-8 {{ margin-right: var(--space-8); }}
        
        /* Horizontal margin */
        .mx-0 {{ margin-left: var(--space-0); margin-right: var(--space-0); }}
        .mx-1 {{ margin-left: var(--space-1); margin-right: var(--space-1); }}
        .mx-2 {{ margin-left: var(--space-2); margin-right: var(--space-2); }}
        .mx-3 {{ margin-left: var(--space-3); margin-right: var(--space-3); }}
        .mx-4 {{ margin-left: var(--space-4); margin-right: var(--space-4); }}
        .mx-5 {{ margin-left: var(--space-5); margin-right: var(--space-5); }}
        .mx-6 {{ margin-left: var(--space-6); margin-right: var(--space-6); }}
        .mx-8 {{ margin-left: var(--space-8); margin-right: var(--space-8); }}
        
        /* Vertical margin */
        .my-0 {{ margin-top: var(--space-0); margin-bottom: var(--space-0); }}
        .my-1 {{ margin-top: var(--space-1); margin-bottom: var(--space-1); }}
        .my-2 {{ margin-top: var(--space-2); margin-bottom: var(--space-2); }}
        .my-3 {{ margin-top: var(--space-3); margin-bottom: var(--space-3); }}
        .my-4 {{ margin-top: var(--space-4); margin-bottom: var(--space-4); }}
        .my-5 {{ margin-top: var(--space-5); margin-bottom: var(--space-5); }}
        .my-6 {{ margin-top: var(--space-6); margin-bottom: var(--space-6); }}
        .my-8 {{ margin-top: var(--space-8); margin-bottom: var(--space-8); }}
        
        /* Padding */
        .p-0 {{ padding: var(--space-0); }}
        .p-1 {{ padding: var(--space-1); }}
        .p-2 {{ padding: var(--space-2); }}
        .p-3 {{ padding: var(--space-3); }}
        .p-4 {{ padding: var(--space-4); }}
        .p-5 {{ padding: var(--space-5); }}
        .p-6 {{ padding: var(--space-6); }}
        .p-8 {{ padding: var(--space-8); }}
        .p-10 {{ padding: var(--space-10); }}
        .p-12 {{ padding: var(--space-12); }}
        .p-16 {{ padding: var(--space-16); }}
        
        /* Padding directions */
        .pt-0 {{ padding-top: var(--space-0); }}
        .pt-1 {{ padding-top: var(--space-1); }}
        .pt-2 {{ padding-top: var(--space-2); }}
        .pt-3 {{ padding-top: var(--space-3); }}
        .pt-4 {{ padding-top: var(--space-4); }}
        .pt-5 {{ padding-top: var(--space-5); }}
        .pt-6 {{ padding-top: var(--space-6); }}
        .pt-8 {{ padding-top: var(--space-8); }}
        
        .pb-0 {{ padding-bottom: var(--space-0); }}
        .pb-1 {{ padding-bottom: var(--space-1); }}
        .pb-2 {{ padding-bottom: var(--space-2); }}
        .pb-3 {{ padding-bottom: var(--space-3); }}
        .pb-4 {{ padding-bottom: var(--space-4); }}
        .pb-5 {{ padding-bottom: var(--space-5); }}
        .pb-6 {{ padding-bottom: var(--space-6); }}
        .pb-8 {{ padding-bottom: var(--space-8); }}
        
        .pl-0 {{ padding-left: var(--space-0); }}
        .pl-1 {{ padding-left: var(--space-1); }}
        .pl-2 {{ padding-left: var(--space-2); }}
        .pl-3 {{ padding-left: var(--space-3); }}
        .pl-4 {{ padding-left: var(--space-4); }}
        .pl-5 {{ padding-left: var(--space-5); }}
        .pl-6 {{ padding-left: var(--space-6); }}
        .pl-8 {{ padding-left: var(--space-8); }}
        
        .pr-0 {{ padding-right: var(--space-0); }}
        .pr-1 {{ padding-right: var(--space-1); }}
        .pr-2 {{ padding-right: var(--space-2); }}
        .pr-3 {{ padding-right: var(--space-3); }}
        .pr-4 {{ padding-right: var(--space-4); }}
        .pr-5 {{ padding-right: var(--space-5); }}
        .pr-6 {{ padding-right: var(--space-6); }}
        .pr-8 {{ padding-right: var(--space-8); }}
        
        /* Horizontal and vertical padding */
        .px-0 {{ padding-left: var(--space-0); padding-right: var(--space-0); }}
        .px-1 {{ padding-left: var(--space-1); padding-right: var(--space-1); }}
        .px-2 {{ padding-left: var(--space-2); padding-right: var(--space-2); }}
        .px-3 {{ padding-left: var(--space-3); padding-right: var(--space-3); }}
        .px-4 {{ padding-left: var(--space-4); padding-right: var(--space-4); }}
        .px-5 {{ padding-left: var(--space-5); padding-right: var(--space-5); }}
        .px-6 {{ padding-left: var(--space-6); padding-right: var(--space-6); }}
        .px-8 {{ padding-left: var(--space-8); padding-right: var(--space-8); }}
        
        .py-0 {{ padding-top: var(--space-0); padding-bottom: var(--space-0); }}
        .py-1 {{ padding-top: var(--space-1); padding-bottom: var(--space-1); }}
        .py-2 {{ padding-top: var(--space-2); padding-bottom: var(--space-2); }}
        .py-3 {{ padding-top: var(--space-3); padding-bottom: var(--space-3); }}
        .py-4 {{ padding-top: var(--space-4); padding-bottom: var(--space-4); }}
        .py-5 {{ padding-top: var(--space-5); padding-bottom: var(--space-5); }}
        .py-6 {{ padding-top: var(--space-6); padding-bottom: var(--space-6); }}
        .py-8 {{ padding-top: var(--space-8); padding-bottom: var(--space-8); }}
        
        /* Touch-friendly component sizing */
        .touch-target {{
            min-height: var(--touch-target-min);
            min-width: var(--touch-target-min);
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .touch-target-recommended {{
            min-height: var(--touch-target-recommended);
            min-width: var(--touch-target-recommended);
        }}
        
        /* Enhanced button sizing */
        .btn {{
            min-height: var(--touch-target-min);
            padding: var(--space-2) var(--space-4);
            border-radius: var(--space-2);
            font-weight: 500;
            transition: all 0.2s ease;
            cursor: pointer;
            border: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: var(--space-2);
            text-decoration: none;
        }}
        
        .btn:focus {{
            outline: 2px solid var(--primary);
            outline-offset: 2px;
        }}
        
        .btn:hover {{
            transform: translateY(-1px);
        }}
        
        /* Form element spacing */
        .form-group {{
            margin-bottom: var(--space-4);
        }}
        
        .form-label {{
            display: block;
            margin-bottom: var(--space-1);
            font-weight: 500;
            color: var(--text-secondary);
        }}
        
        .form-input {{
            min-height: var(--touch-target-min);
            padding: var(--space-3);
            border: 1px solid var(--border-light);
            border-radius: var(--space-2);
            font-size: var(--text-base);
            line-height: var(--leading-normal);
            width: 100%;
            background-color: var(--bg-primary);
            color: var(--text-primary);
        }}
        
        .form-input:focus {{
            outline: 2px solid var(--primary);
            outline-offset: 2px;
            border-color: var(--primary);
        }}
        
        /* Card component */
        .card {{
            background-color: var(--bg-primary);
            border: 1px solid var(--border-light);
            border-radius: var(--space-3);
            padding: var(--space-6);
            margin-bottom: var(--space-6);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            transition: all 0.2s ease;
        }}
        
        .card:hover {{
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            transform: translateY(-2px);
        }}
        
        .card-header {{
            margin-bottom: var(--space-4);
            padding-bottom: var(--space-3);
            border-bottom: 1px solid var(--border-light);
        }}
        
        .card-title {{
            font-size: var(--text-xl);
            font-weight: 600;
            color: var(--text-primary);
            margin: 0;
        }}
        
        .card-body {{
            color: var(--text-primary);
        }}
        
        .card-footer {{
            margin-top: var(--space-4);
            padding-top: var(--space-3);
            border-top: 1px solid var(--border-light);
            color: var(--text-secondary);
            font-size: var(--text-sm);
        }}
        
        /* Navigation spacing */
        .nav {{
            display: flex;
            align-items: center;
            padding: var(--space-4) 0;
        }}
        
        .nav-item {{
            margin-right: var(--space-4);
        }}
        
        .nav-item:last-child {{
            margin-right: 0;
        }}
        
        .nav-link {{
            padding: var(--space-2) var(--space-3);
            text-decoration: none;
            color: var(--text-secondary);
            border-radius: var(--space-2);
            transition: all 0.2s ease;
            min-height: var(--touch-target-min);
            display: flex;
            align-items: center;
        }}
        
        .nav-link:hover {{
            color: var(--text-primary);
            background-color: var(--bg-accent);
        }}
        
        .nav-link:focus {{
            outline: 2px solid var(--primary);
            outline-offset: 2px;
        }}
        
        .nav-link.active {{
            color: var(--primary);
            background-color: var(--primary-subtle);
        }}
        
        /* Content spacing patterns */
        .section {{
            padding: var(--space-8) 0;
        }}
        
        .section-sm {{
            padding: var(--space-6) 0;
        }}
        
        .section-lg {{
            padding: var(--space-12) 0;
        }}
        
        .content-block {{
            margin-bottom: var(--space-6);
        }}
        
        .content-block:last-child {{
            margin-bottom: 0;
        }}
        
        /* List spacing */
        .list {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        
        .list-item {{
            padding: var(--space-2) 0;
            border-bottom: 1px solid var(--border-light);
        }}
        
        .list-item:last-child {{
            border-bottom: none;
        }}
        
        /* Table spacing */
        .table {{
            width: 100%;
            border-collapse: collapse;
            margin: var(--space-6) 0;
        }}
        
        .table th,
        .table td {{
            padding: var(--space-3) var(--space-4);
            text-align: left;
            border-bottom: 1px solid var(--border-light);
        }}
        
        .table th {{
            font-weight: 600;
            color: var(--text-secondary);
            background-color: var(--bg-secondary);
        }}
        
        .table td {{
            color: var(--text-primary);
        }}
        
        /* Responsive Design */
        /* Extra Small devices (phones, less than 640px) */
        @media (max-width: 639px) {{
            .container {{
                padding-left: var(--space-3);
                padding-right: var(--space-3);
            }}
            
            .grid {{
                gap: var(--space-3);
            }}
            
            .col-xs-12 {{ grid-column: span 12 / span 12; }}
            .col-xs-6 {{ grid-column: span 6 / span 6; }}
            .col-xs-4 {{ grid-column: span 4 / span 4; }}
            .col-xs-3 {{ grid-column: span 3 / span 3; }}
        }}
        
        /* Small devices (landscape phones, 640px and up) */
        @media (min-width: 640px) {{
            .col-sm-12 {{ grid-column: span 12 / span 12; }}
            .col-sm-6 {{ grid-column: span 6 / span 6; }}
            .col-sm-4 {{ grid-column: span 4 / span 4; }}
            .col-sm-3 {{ grid-column: span 3 / span 3; }}
        }}
        
        /* Medium devices (tablets, 768px and up) */
        @media (min-width: 768px) {{
            .col-md-12 {{ grid-column: span 12 / span 12; }}
            .col-md-8 {{ grid-column: span 8 / span 8; }}
            .col-md-6 {{ grid-column: span 6 / span 6; }}
            .col-md-4 {{ grid-column: span 4 / span 4; }}
            .col-md-3 {{ grid-column: span 3 / span 3; }}
        }}
        
        /* Large devices (desktops, 1024px and up) */
        @media (min-width: 1024px) {{
            .col-lg-12 {{ grid-column: span 12 / span 12; }}
            .col-lg-8 {{ grid-column: span 8 / span 8; }}
            .col-lg-6 {{ grid-column: span 6 / span 6; }}
            .col-lg-4 {{ grid-column: span 4 / span 4; }}
            .col-lg-3 {{ grid-column: span 3 / span 3; }}
        }}
        
        /* Accessibility Enhancements */
        /* High contrast mode support */
        @media (prefers-contrast: high) {{
            .card {{
                border-width: 2px;
                border-color: var(--text-primary);
            }}
            
            .btn {{
                border: 2px solid var(--text-primary);
            }}
            
            .form-input {{
                border-width: 2px;
                border-color: var(--text-primary);
            }}
        }}
        
        /* Reduced motion support */
        @media (prefers-reduced-motion: reduce) {{
            .card,
            .btn,
            .nav-link {{
                transition: none;
            }}
            
            .card:hover,
            .btn:hover {{
                transform: none;
            }}
        }}
        
        /* Focus management for better accessibility */
        .focus-visible {{
            outline: 2px solid var(--primary);
            outline-offset: 2px;
        }}
        
        /* Skip link for keyboard navigation */
        .skip-to-content {{
            position: absolute;
            top: -40px;
            left: 6px;
            background: var(--primary);
            color: var(--text-inverse);
            padding: var(--space-2);
            text-decoration: none;
            border-radius: var(--space-2);
            z-index: 1000;
            font-weight: 500;
        }}
        
        .skip-to-content:focus {{
            top: 6px;
        }}
        """
        
        return css
    
    @classmethod
    def get_layout_pattern(cls, pattern_name: str) -> Dict[str, Any]:
        """Get a specific layout pattern"""
        return cls.LAYOUT_PATTERNS.get(pattern_name, cls.LAYOUT_PATTERNS["form"])
    
    @classmethod
    def create_demo_layout(cls, layout_type: str = "dashboard") -> str:
        """Create HTML/CSS demo for a specific layout pattern"""
        pattern = cls.get_layout_pattern(layout_type)
        
        columns_html = ""
        for i, col_span in enumerate(pattern["columns"]):
            columns_html += f'<div class="col-{col_span}"><div class="demo-card">Column {i+1} ({col_span}/12)</div></div>'
        
        demo_html = f"""
        <div class="container-lg">
            <h2>{pattern["description"].title()}</h2>
            <div class="grid" style="grid-template-columns: repeat({len(pattern["columns"])}, 1fr); gap: {pattern["gutter"]};">
                {columns_html}
            </div>
        </div>
        
        <style>
        .demo-card {{
            background: var(--primary-subtle);
            border: 1px solid var(--border-light);
            border-radius: 8px;
            padding: 24px;
            text-align: center;
            font-weight: 500;
            color: var(--text-primary);
            min-height: 120px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        </style>
        """
        
        return demo_html
    
    @classmethod
    def generate_spacing_guide(cls) -> str:
        """Generate a comprehensive spacing guide"""
        return f"""
# Enhanced Grid System and Spacing Guide

## Overview
This grid system is built on an 8px base unit for consistency and uses touch-friendly design principles for accessibility.

## Key Features

### 1. 8px Base Grid System
- **Base unit**: 8px
- **Consistent spacing**: All values are multiples of 8px
- **Scalable design**: Works across all screen sizes
- **Visual harmony**: Creates balanced, professional layouts

### 2. Touch-Friendly Design
- **Minimum touch target**: 44px (WCAG requirement)
- **Recommended touch target**: 48px (better usability)
- **Touch spacing**: 8px minimum between interactive elements
- **Thumb-friendly**: Larger targets for thumb navigation

### 3. Responsive Breakpoints
- **XS**: < 640px (mobile phones)
- **SM**: ≥ 640px (large phones)
- **MD**: ≥ 768px (tablets)
- **LG**: ≥ 1024px (desktops)
- **XL**: ≥ 1280px (large desktops)
- **2XL**: ≥ 1536px (extra large screens)

### 4. Component Spacing
- **Form elements**: Consistent spacing between inputs, labels, and help text
- **Content blocks**: Proper spacing for readability and visual hierarchy
- **Navigation**: Appropriate spacing for touch and keyboard navigation

## Spacing Scale

### Margin Classes
- `m-0` to `m-24`: All margins (0px to 192px)
- `mt-`, `mb-`, `ml-`, `mr-`: Directional margins
- `mx-`, `my-`: Horizontal and vertical margins

### Padding Classes
- `p-0` to `p-16`: All padding (0px to 128px)
- `pt-`, `pb-`, `pl-`, `pr-`: Directional padding
- `px-`, `py-`: Horizontal and vertical padding

### Grid Classes
- `col-1` to `col-12`: Column spans
- `col-xs-*`, `col-sm-*`, `col-md-*`, `col-lg-*`: Responsive columns
- `container-xs` to `container-2xl`: Container sizes

## Usage Examples

### Dashboard Layout
```html
<div class="container-lg">
  <div class="grid" style="grid-template-columns: repeat(3, 1fr); gap: 24px;">
    <div class="col-4"><!-- Content --></div>
    <div class="col-4"><!-- Content --></div>
    <div class="col-4"><!-- Content --></div>
  </div>
</div>
```

### Form Layout
```html
<div class="container-md">
  <form class="grid" style="grid-template-columns: 1fr;">
    <div class="form-group">
      <label class="form-label">Email</label>
      <input class="form-input" type="email">
    </div>
  </form>
</div>
```

### Detail Page Layout
```html
<div class="container-lg">
  <div class="grid" style="grid-template-columns: 2fr 1fr; gap: 32px;">
    <div class="col-8"><!-- Main content --></div>
    <div class="col-4"><!-- Sidebar --></div>
  </div>
</div>
```

## Accessibility Features

### Touch Targets
- All interactive elements meet 44px minimum
- Sufficient spacing between touch targets
- Clear visual feedback on interaction

### Focus Management
- Skip links for keyboard navigation
- Clear focus indicators
- Logical tab order

### Responsive Design
- Mobile-first approach
- Scalable layouts
- Touch-optimized interactions

### High Contrast Support
- Enhanced borders in high contrast mode
- Improved visibility for low vision users
- Clear separation between elements

## Testing Checklist

- [ ] All interactive elements are 44px+ minimum
- [ ] Spacing is consistent (multiples of 8px)
- [ ] Layouts work across all breakpoints
- [ ] Touch targets have adequate spacing
- [ ] Focus indicators are visible
- [ ] Content is readable at all sizes
- [ ] Navigation is keyboard accessible
- [ ] High contrast mode works properly
"""


def apply_enhanced_grid_system():
    """Apply the enhanced grid system to Streamlit app"""
    grid_system = EnhancedGridSystem()
    css = grid_system.get_grid_css()
    
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def create_grid_demo():
    """Create an interactive grid system demonstration"""
    st.markdown("## 📐 Enhanced Grid System Demo")
    
    # Apply grid system
    apply_enhanced_grid_system()
    
    # Layout pattern selector
    grid_system = EnhancedGridSystem()
    layout_patterns = grid_system.LAYOUT_PATTERNS
    
    selected_pattern = st.selectbox(
        "Select Layout Pattern:",
        list(layout_patterns.keys()),
        format_func=lambda x: layout_patterns[x]["description"]
    )
    
    # Show pattern details
    pattern = layout_patterns[selected_pattern]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Columns", len(pattern["columns"]))
    with col2:
        st.metric("Gutter", pattern["gutter"])
    with col3:
        st.metric("Breakpoint", pattern["breakpoint"])
    
    # Show column breakdown
    st.markdown("### Column Breakdown")
    cols = st.columns(len(pattern["columns"]))
    
    for i, col_span in enumerate(pattern["columns"]):
        with cols[i]:
            st.markdown(f"""
            <div style="
                background: var(--primary-subtle);
                border: 1px solid var(--border-light);
                border-radius: 8px;
                padding: 24px;
                text-align: center;
                min-height: 100px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 500;
            ">
                Column {i+1}<br>
                <small>{col_span}/12 ({int(100*col_span/12)}%)</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Spacing examples
    st.markdown("### Spacing Examples")
    
    # Margin examples
    st.markdown("#### Margin Examples")
    margin_cols = st.columns(4)
    
    with margin_cols[0]:
        st.markdown('<div style="background: #f0f0f0; padding: 16px; margin: 8px; border: 1px dashed #ccc;">m-1 (8px)</div>', unsafe_allow_html=True)
        st.markdown('<div style="background: #f0f0f0; padding: 16px; margin: 16px; border: 1px dashed #ccc;">m-2 (16px)</div>', unsafe_allow_html=True)
    
    with margin_cols[1]:
        st.markdown('<div style="background: #f0f0f0; padding: 16px; margin: 24px; border: 1px dashed #ccc;">m-3 (24px)</div>', unsafe_allow_html=True)
        st.markdown('<div style="background: #f0f0f0; padding: 16px; margin: 32px; border: 1px dashed #ccc;">m-4 (32px)</div>', unsafe_allow_html=True)
    
    with margin_cols[2]:
        st.markdown('<div style="background: #f0f0f0; padding: 16px; margin: 48px; border: 1px dashed #ccc;">m-6 (48px)</div>', unsafe_allow_html=True)
        st.markdown('<div style="background: #f0f0f0; padding: 16px; margin: 64px; border: 1px dashed #ccc;">m-8 (64px)</div>', unsafe_allow_html=True)
    
    with margin_cols[3]:
        st.markdown('<div style="background: #f0f0f0; padding: 16px; margin: 96px; border: 1px dashed #ccc;">m-12 (96px)</div>', unsafe_allow_html=True)
        st.markdown('<div style="background: #f0f0f0; padding: 16px; margin: 128px; border: 1px dashed #ccc;">m-16 (128px)</div>', unsafe_allow_html=True)
    
    # Touch target examples
    st.markdown("#### Touch Target Examples")
    
    touch_cols = st.columns(3)
    
    with touch_cols[0]:
        st.markdown("""
        **Minimum Touch Target (44px)**
        <button style="
            background: var(--primary);
            color: var(--text-inverse);
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            min-height: 44px;
            min-width: 44px;
            font-weight: 500;
            cursor: pointer;
        ">Button</button>
        """, unsafe_allow_html=True)
    
    with touch_cols[1]:
        st.markdown("""
        **Recommended Touch Target (48px)**
        <button style="
            background: var(--secondary);
            color: var(--text-inverse);
            border: none;
            border-radius: 8px;
            padding: 16px 32px;
            min-height: 48px;
            min-width: 48px;
            font-weight: 500;
            cursor: pointer;
        ">Button</button>
        """, unsafe_allow_html=True)
    
    with touch_cols[2]:
        st.markdown("""
        **Large Touch Target (56px)**
        <button style="
            background: var(--accent);
            color: var(--text-inverse);
            border: none;
            border-radius: 8px;
            padding: 20px 40px;
            min-height: 56px;
            min-width: 56px;
            font-weight: 500;
            cursor: pointer;
        ">Button</button>
        """, unsafe_allow_html=True)
    
    # Show CSS code
    if st.button("📋 Show Grid CSS"):
        css = grid_system.get_grid_css()
        st.code(css, language="css")
    
    # Show spacing guide
    if st.button("📖 Show Spacing Guide"):
        guide = grid_system.generate_spacing_guide()
        st.markdown(guide)


if __name__ == "__main__":
    create_grid_demo()