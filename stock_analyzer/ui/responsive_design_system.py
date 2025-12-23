"""
Responsive Design System for All Screen Sizes
Comprehensive responsive design with accessibility features and multi-device optimization
"""

import streamlit as st
from typing import Dict, Any, List, Optional, Tuple
import json


class ResponsiveDesignSystem:
    """Complete responsive design system with accessibility features"""
    
    # Breakpoint definitions
    BREAKPOINTS = {
        "xs": {"min": 0, "max": 479, "name": "Extra Small", "devices": "Mobile phones"},
        "sm": {"min": 480, "max": 639, "name": "Small", "devices": "Large phones"},
        "md": {"min": 640, "max": 767, "name": "Medium", "devices": "Tablets (portrait)"},
        "lg": {"min": 768, "max": 1023, "name": "Large", "devices": "Tablets (landscape) / Small laptops"},
        "xl": {"min": 1024, "max": 1279, "name": "Extra Large", "devices": "Laptops / Desktops"},
        "2xl": {"min": 1280, "max": 1535, "name": "2X Large", "devices": "Large desktops"},
        "3xl": {"min": 1536, "max": 1919, "name": "3X Large", "devices": "Very large screens"},
        "4xl": {"min": 1920, "max": 2559, "name": "4X Large", "devices": "Ultra-wide monitors"},
    }
    
    # Device-specific optimizations
    DEVICE_OPTIMIZATIONS = {
        "mobile": {
            "breakpoints": ["xs", "sm"],
            "touch_optimized": True,
            "font_size_multiplier": 0.875,  # Slightly smaller base font
            "spacing_multiplier": 1.0,
            "min_touch_target": "48px",  # Larger on mobile
            "navigation_pattern": "bottom-tabs",
            "form_layout": "single-column"
        },
        "tablet": {
            "breakpoints": ["md", "lg"],
            "touch_optimized": True,
            "font_size_multiplier": 1.0,
            "spacing_multiplier": 1.1,
            "min_touch_target": "44px",
            "navigation_pattern": "side-drawer",
            "form_layout": "two-column"
        },
        "desktop": {
            "breakpoints": ["xl", "2xl", "3xl", "4xl"],
            "touch_optimized": False,
            "font_size_multiplier": 1.0,
            "spacing_multiplier": 1.2,
            "min_touch_target": "44px",
            "navigation_pattern": "sidebar",
            "form_layout": "multi-column"
        }
    }
    
    # Responsive design patterns
    LAYOUT_PATTERNS = {
        "mobile_first": {
            "description": "Start with mobile, enhance for larger screens",
            "approach": "progressive_enhancement",
            "base_breakpoint": "xs"
        },
        "desktop_first": {
            "description": "Start with desktop, simplify for smaller screens",
            "approach": "progressive_simplification",
            "base_breakpoint": "xl"
        },
        "content_first": {
            "description": "Design based on content breakpoints",
            "approach": "content_driven",
            "base_breakpoint": "auto"
        }
    }
    
    # Component responsive behaviors
    COMPONENT_RESPONSIVE_BEHAVIORS = {
        "navigation": {
            "mobile": "hamburger-menu",
            "tablet": "collapsible-sections",
            "desktop": "full-navigation"
        },
        "cards": {
            "mobile": "single-column-stack",
            "tablet": "two-column-grid",
            "desktop": "three-to-four-column-grid"
        },
        "forms": {
            "mobile": "full-width-single-column",
            "tablet": "two-column-grid",
            "desktop": "multi-column-layout"
        },
        "charts": {
            "mobile": "stacked-vertical",
            "tablet": "side-by-side",
            "desktop": "dashboard-grid"
        },
        "tables": {
            "mobile": "card-layout",
            "tablet": "scrollable-container",
            "desktop": "full-table"
        }
    }
    
    # Accessibility features for different screen sizes
    ACCESSIBILITY_FEATURES = {
        "mobile": {
            "zoom_support": "up_to_500_percent",
            "focus_management": "touch_friendly_focus",
            "gesture_alternatives": "button_based_navigation",
            "voice_control": "enhanced_support",
            "text_scaling": "fluid_typography"
        },
        "tablet": {
            "zoom_support": "up_to_200_percent",
            "focus_management": "keyboard_and_touch",
            "gesture_alternatives": "hybrid_interaction",
            "voice_control": "standard_support",
            "text_scaling": "responsive_typography"
        },
        "desktop": {
            "zoom_support": "up_to_200_percent",
            "focus_management": "keyboard_optimized",
            "gesture_alternatives": "mouse_and_keyboard",
            "voice_control": "basic_support",
            "text_scaling": "fixed_scaling"
        }
    }
    
    @classmethod
    def get_responsive_css(cls) -> str:
        """Generate comprehensive responsive CSS"""
        
        css = f"""
        /* Enhanced Responsive Design System */
        
        :root {{
            /* Breakpoint variables */
            {chr(10).join([f'            --breakpoint-{k}: {v["min"]}px;' for k, v in cls.BREAKPOINTS.items()])}
            
            /* Device-specific variables */
            --mobile-font-multiplier: {cls.DEVICE_OPTIMIZATIONS["mobile"]["font_size_multiplier"]};
            --tablet-font-multiplier: {cls.DEVICE_OPTIMIZATIONS["tablet"]["font_size_multiplier"]};
            --desktop-font-multiplier: {cls.DEVICE_OPTIMIZATIONS["desktop"]["font_size_multiplier"]};
            
            --mobile-spacing-multiplier: {cls.DEVICE_OPTIMIZATIONS["mobile"]["spacing_multiplier"]};
            --tablet-spacing-multiplier: {cls.DEVICE_OPTIMIZATIONS["tablet"]["spacing_multiplier"]};
            --desktop-spacing-multiplier: {cls.DEVICE_OPTIMIZATIONS["desktop"]["spacing_multiplier"]};
        }}
        
        /* Base responsive typography */
        html {{
            font-size: 16px;
            scroll-behavior: smooth;
            -webkit-text-size-adjust: 100%;
            -ms-text-size-adjust: 100%;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: var(--text-primary);
            background-color: var(--bg-primary);
            overflow-x: hidden; /* Prevent horizontal scroll */
        }}
        
        /* Container system */
        .container {{
            width: 100%;
            margin-left: auto;
            margin-right: auto;
            padding-left: 1rem;
            padding-right: 1rem;
        }}
        
        /* Container sizes */
        .container-xs {{ max-width: 475px; }}
        .container-sm {{ max-width: 640px; }}
        .container-md {{ max-width: 768px; }}
        .container-lg {{ max-width: 1024px; }}
        .container-xl {{ max-width: 1280px; }}
        .container-2xl {{ max-width: 1536px; }}
        .container-3xl {{ max-width: 1920px; }}
        .container-4xl {{ max-width: 2560px; }}
        .container-full {{ max-width: 100%; }}
        
        /* Responsive Grid System */
        .responsive-grid {{
            display: grid;
            gap: 1.5rem;
            grid-template-columns: 1fr;
        }}
        
        /* Mobile first approach - base styles */
        @media (min-width: 480px) {{
            .container {{
                padding-left: 1.5rem;
                padding-right: 1.5rem;
            }}
            
            .responsive-grid {{
                grid-template-columns: repeat(2, 1fr);
                gap: 2rem;
            }}
        }}
        
        @media (min-width: 768px) {{
            .container {{
                padding-left: 2rem;
                padding-right: 2rem;
            }}
            
            .responsive-grid {{
                grid-template-columns: repeat(3, 1fr);
                gap: 2.5rem;
            }}
        }}
        
        @media (min-width: 1024px) {{
            .container {{
                padding-left: 2.5rem;
                padding-right: 2.5rem;
            }}
            
            .responsive-grid {{
                grid-template-columns: repeat(4, 1fr);
                gap: 3rem;
            }}
        }}
        
        @media (min-width: 1280px) {{
            .responsive-grid {{
                grid-template-columns: repeat(6, 1fr);
                gap: 3rem;
            }}
        }}
        
        @media (min-width: 1536px) {{
            .responsive-grid {{
                grid-template-columns: repeat(8, 1fr);
                gap: 3.5rem;
            }}
        }}
        
        /* Responsive Typography */
        .responsive-text {{
            font-size: 1rem;
            line-height: 1.6;
        }}
        
        /* Mobile typography adjustments */
        @media (max-width: 479px) {{
            html {{
                font-size: 14px; /* Smaller base on mobile */
            }}
            
            .responsive-text {{
                font-size: 0.875rem;
            }}
            
            /* Larger touch targets on mobile */
            .touch-target {{
                min-height: 48px;
                min-width: 48px;
            }}
            
            /* Stack navigation vertically on mobile */
            .nav-horizontal {{
                flex-direction: column;
            }}
            
            /* Full width buttons on mobile */
            .btn-mobile-full {{
                width: 100%;
                margin-bottom: 0.75rem;
            }}
        }}
        
        /* Tablet optimizations */
        @media (min-width: 640px) and (max-width: 1023px) {{
            /* Two column layouts */
            .tablet-two-col {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 2rem;
            }}
            
            /* Side drawer navigation */
            .tablet-nav {{
                display: flex;
                flex-direction: row;
                flex-wrap: wrap;
            }}
        }}
        
        /* Desktop optimizations */
        @media (min-width: 1024px) {{
            /* Multi-column layouts */
            .desktop-three-col {{
                display: grid;
                grid-template-columns: 1fr 2fr 1fr;
                gap: 3rem;
            }}
            
            .desktop-four-col {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 2rem;
            }}
            
            /* Sidebar navigation */
            .desktop-nav {{
                display: flex;
                flex-direction: column;
            }}
            
            /* Hover effects for desktop */
            .desktop-hover:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            }}
        }}
        
        /* Large screen optimizations */
        @media (min-width: 1920px) {{
            .container {{
                max-width: 1800px;
                padding-left: 3rem;
                padding-right: 3rem;
            }}
            
            .responsive-grid {{
                grid-template-columns: repeat(12, 1fr);
                gap: 4rem;
            }}
        }}
        
        /* Responsive Components */
        
        /* Navigation */
        .responsive-nav {{
            display: flex;
            flex-direction: column;
            background-color: var(--bg-secondary);
            border-radius: 0.5rem;
            overflow: hidden;
        }}
        
        @media (min-width: 768px) {{
            .responsive-nav {{
                flex-direction: row;
            }}
        }}
        
        .nav-item {{
            padding: 1rem 1.5rem;
            color: var(--text-secondary);
            text-decoration: none;
            border-bottom: 1px solid var(--border-light);
            transition: all 0.2s ease;
            min-height: 44px; /* Touch target */
            display: flex;
            align-items: center;
        }}
        
        @media (min-width: 768px) {{
            .nav-item {{
                border-bottom: none;
                border-right: 1px solid var(--border-light);
            }}
            
            .nav-item:last-child {{
                border-right: none;
            }}
        }}
        
        .nav-item:hover,
        .nav-item:focus {{
            background-color: var(--primary-subtle);
            color: var(--primary);
        }}
        
        /* Cards */
        .responsive-card {{
            background-color: var(--bg-primary);
            border: 1px solid var(--border-light);
            border-radius: 0.75rem;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}
        
        .responsive-card:hover {{
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        
        @media (min-width: 768px) {{
            .responsive-card {{
                padding: 2rem;
            }}
        }}
        
        /* Forms */
        .responsive-form {{
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }}
        
        @media (min-width: 768px) {{
            .responsive-form {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 2rem;
            }}
            
            .form-field-full-width {{
                grid-column: 1 / -1;
            }}
        }}
        
        .form-field {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}
        
        .form-label {{
            font-weight: 500;
            color: var(--text-secondary);
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .form-input {{
            min-height: 44px;
            padding: 0.75rem 1rem;
            border: 1px solid var(--border-light);
            border-radius: 0.5rem;
            font-size: 1rem;
            line-height: 1.5;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            transition: all 0.2s ease;
        }}
        
        .form-input:focus {{
            outline: 2px solid var(--primary);
            outline-offset: 2px;
            border-color: var(--primary);
        }}
        
        /* Buttons */
        .responsive-button {{
            min-height: 44px;
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 0.5rem;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.2s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }}
        
        @media (max-width: 479px) {{
            .responsive-button {{
                width: 100%;
                margin-bottom: 1rem;
            }}
        }}
        
        /* Tables */
        .responsive-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            background-color: var(--bg-primary);
            border-radius: 0.5rem;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .responsive-table th,
        .responsive-table td {{
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid var(--border-light);
        }}
        
        .responsive-table th {{
            background-color: var(--bg-secondary);
            font-weight: 600;
            color: var(--text-secondary);
        }}
        
        /* Mobile table adaptations */
        @media (max-width: 767px) {{
            .responsive-table {{
                display: none; /* Hide table on mobile */
            }}
            
            .table-cards {{
                display: block;
            }}
            
            .table-card {{
                background-color: var(--bg-primary);
                border: 1px solid var(--border-light);
                border-radius: 0.5rem;
                padding: 1rem;
                margin-bottom: 1rem;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            
            .table-card-row {{
                display: flex;
                justify-content: space-between;
                padding: 0.5rem 0;
                border-bottom: 1px solid var(--border-light);
            }}
            
            .table-card-row:last-child {{
                border-bottom: none;
            }}
            
            .table-card-label {{
                font-weight: 500;
                color: var(--text-secondary);
                font-size: 0.875rem;
            }}
            
            .table-card-value {{
                color: var(--text-primary);
                font-weight: 500;
            }}
        }}
        
        /* Charts */
        .responsive-chart {{
            width: 100%;
            height: 300px;
            margin: 1.5rem 0;
        }}
        
        @media (min-width: 768px) {{
            .responsive-chart {{
                height: 400px;
            }}
        }}
        
        @media (min-width: 1024px) {{
            .responsive-chart {{
                height: 500px;
            }}
        }}
        
        /* Accessibility Enhancements */
        
        /* High contrast mode */
        @media (prefers-contrast: high) {{
            .responsive-card {{
                border-width: 2px;
                border-color: var(--text-primary);
            }}
            
            .form-input {{
                border-width: 2px;
                border-color: var(--text-primary);
            }}
            
            .responsive-button {{
                border: 2px solid var(--text-primary);
            }}
        }}
        
        /* Reduced motion */
        @media (prefers-reduced-motion: reduce) {{
            .responsive-card,
            .nav-item,
            .form-input,
            .responsive-button {{
                transition: none;
            }}
            
            .responsive-card:hover {{
                transform: none;
            }}
            
            html {{
                scroll-behavior: auto;
            }}
        }}
        
        /* Focus management */
        .focus-visible {{
            outline: 2px solid var(--primary);
            outline-offset: 2px;
        }}
        
        /* Skip link */
        .skip-to-content {{
            position: absolute;
            top: -40px;
            left: 6px;
            background: var(--primary);
            color: var(--text-inverse);
            padding: 8px 16px;
            text-decoration: none;
            border-radius: 4px;
            z-index: 1000;
            font-weight: 500;
        }}
        
        .skip-to-content:focus {{
            top: 6px;
        }}
        
        /* Performance optimizations */
        .responsive-image {{
            max-width: 100%;
            height: auto;
            loading: lazy;
        }}
        """
        
        return css
    
    @classmethod
    def get_device_detection_js(cls) -> str:
        """Generate JavaScript for device detection and responsive behavior"""
        
        js = f"""
        // Device Detection and Responsive Behavior Management
        
        class ResponsiveDeviceManager {{
            constructor() {{
                this.currentDevice = this.detectDevice();
                this.breakpoints = {json.dumps(cls.BREAKPOINTS)};
                this.setupEventListeners();
                this.applyDeviceOptimizations();
            }}
            
            detectDevice() {{
                const width = window.innerWidth;
                
                // Detect device type
                if (width <= 767) {{
                    return 'mobile';
                }} else if (width <= 1023) {{
                    return 'tablet';
                }} else {{
                    return 'desktop';
                }}
            }}
            
            setupEventListeners() {{
                // Handle window resize
                window.addEventListener('resize', this.handleResize.bind(this));
                
                // Handle orientation change
                window.addEventListener('orientationchange', this.handleOrientationChange.bind(this));
            }}
            
            handleResize() {{
                const newDevice = this.detectDevice();
                if (newDevice !== this.currentDevice) {{
                    this.currentDevice = newDevice;
                    this.applyDeviceOptimizations();
                    this.notifyDeviceChange();
                }}
            }}
            
            handleOrientationChange() {{
                setTimeout(() => {{
                    this.handleResize();
                }}, 100);
            }}
            
            applyDeviceOptimizations() {{
                const deviceConfig = {json.dumps(cls.DEVICE_OPTIMIZATIONS)};
                const config = deviceConfig[this.currentDevice];
                
                // Apply touch optimization
                if (config.touch_optimized) {{
                    document.body.classList.add('touch-optimized');
                    this.enhanceTouchTargets();
                }} else {{
                    document.body.classList.remove('touch-optimized');
                }}
                
                // Store device info
                document.documentElement.setAttribute('data-device', this.currentDevice);
            }}
            
            enhanceTouchTargets() {{
                const interactiveElements = document.querySelectorAll(
                    'button, a, input, select, textarea, [role="button"], [tabindex]'
                );
                
                interactiveElements.forEach(element => {{
                    const computedStyle = window.getComputedStyle(element);
                    const minHeight = parseInt(computedStyle.minHeight) || 0;
                    const minWidth = parseInt(computedStyle.minWidth) || 0;
                    
                    if (minHeight < 44 || minWidth < 44) {{
                        element.style.minHeight = '48px';
                        element.style.minWidth = '48px';
                        element.style.padding = '12px';
                    }}
                }});
            }}
            
            notifyDeviceChange() {{
                const event = new CustomEvent('devicechange', {{
                    detail: {{
                        newDevice: this.currentDevice,
                        timestamp: Date.now()
                    }}
                }});
                document.dispatchEvent(event);
            }}
        }}
        
        // Initialize responsive device manager
        const deviceManager = new ResponsiveDeviceManager();
        window.deviceManager = deviceManager;
        """
        
        return js
    
    @classmethod
    def generate_responsive_guide(cls) -> str:
        """Generate comprehensive responsive design guide"""
        
        return f"""
# Responsive Design System Guide

## Overview
This responsive design system ensures optimal user experience across all device sizes, with accessibility as a core consideration.

## Key Features

### 1. Multi-Device Support
- **Mobile (≤767px)**: Touch-optimized, single-column layouts
- **Tablet (768-1023px)**: Hybrid touch/mouse, two-column layouts  
- **Desktop (≥1024px)**: Mouse/keyboard, multi-column layouts
- **Large Screens (≥1920px)**: Enhanced layouts for ultra-wide monitors

### 2. Accessibility Integration
- **Touch Targets**: Minimum 44px, recommended 48px
- **Focus Management**: Keyboard and touch-friendly focus states
- **Screen Reader Support**: Proper ARIA labels and semantic markup
- **Zoom Support**: Content remains functional up to 500% zoom
- **High Contrast**: Automatic adaptation for high contrast mode

## Breakpoints

| Breakpoint | Range | Device Type |
|------------|-------|-------------|
| xs | 0-479px | Mobile phones |
| sm | 480-639px | Large phones |
| md | 640-767px | Tablets (portrait) |
| lg | 768-1023px | Tablets (landscape) |
| xl | 1024-1279px | Laptops/Desktops |
| 2xl | 1280-1535px | Large desktops |

## Implementation Guidelines

### Mobile-First Approach
Start with mobile design and progressively enhance for larger screens.

### Testing Checklist
- [ ] Test on actual devices
- [ ] Test with screen readers
- [ ] Test keyboard navigation
- [ ] Test zoom levels up to 500%
- [ ] Test touch interactions
- [ ] Test high contrast mode

This responsive design system ensures that all users, regardless of their device or accessibility needs, can effectively use the Stock Analyzer application.
"""


def apply_responsive_design_system():
    """Apply the responsive design system to Streamlit app"""
    responsive_system = ResponsiveDesignSystem()
    
    # Apply CSS
    css = responsive_system.get_responsive_css()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    
    # Apply JavaScript
    js = responsive_system.get_device_detection_js()
    st.markdown(f"<script>{js}</script>", unsafe_allow_html=True)


def create_responsive_demo():
    """Create an interactive responsive design demonstration"""
    st.markdown("## 📱 Responsive Design System Demo")
    
    # Apply responsive system
    apply_responsive_design_system()
    
    # Device simulation
    st.markdown("### 📱 Device Simulation")
    
    device_options = {
        "Mobile (375px)": "mobile",
        "Tablet (768px)": "tablet", 
        "Desktop (1024px)": "desktop",
        "Large Desktop (1280px)": "large"
    }
    
    selected_device = st.selectbox(
        "Simulate Device View:",
        list(device_options.keys()),
        help="Select a device to see how the layout adapts"
    )
    
    # Show responsive components
    responsive_system = ResponsiveDesignSystem()
    
    # Navigation demo
    st.markdown("### 🧭 Navigation Component")
    st.markdown("""
    <nav class="responsive-nav" role="navigation" aria-label="Main navigation">
        <a href="#home" class="nav-item" aria-current="page">Home</a>
        <a href="#analysis" class="nav-item">Analysis</a>
        <a href="#scanner" class="nav-item">Scanner</a>
        <a href="#settings" class="nav-item">Settings</a>
    </nav>
    """, unsafe_allow_html=True)
    
    # Card demo
    st.markdown("### 📋 Card Component")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <article class="responsive-card" role="region" aria-labelledby="card-title-1">
            <header class="card-header">
                <h3 id="card-title-1" class="card-title">Stock Analysis Result</h3>
            </header>
            <div class="card-body">
                <p>Detailed analysis content here...</p>
            </div>
            <footer class="card-footer">
                <button class="responsive-button" type="button">View Details</button>
            </footer>
        </article>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <article class="responsive-card" role="region" aria-labelledby="card-title-2">
            <header class="card-header">
                <h3 id="card-title-2" class="card-title">Market Overview</h3>
            </header>
            <div class="card-body">
                <p>Market overview content here...</p>
            </div>
            <footer class="card-footer">
                <button class="responsive-button" type="button">View Details</button>
            </footer>
        </article>
        """, unsafe_allow_html=True)
    
    # Form demo
    st.markdown("### 📝 Form Component")
    st.markdown("""
    <form class="responsive-form" role="form" aria-label="Stock analysis form">
        <div class="form-field">
            <label for="ticker" class="form-label">Stock Ticker</label>
            <input type="text" id="ticker" name="ticker" class="form-input" 
                   placeholder="e.g., AAPL" required aria-describedby="ticker-help">
            <small id="ticker-help" class="form-help">Enter the stock symbol</small>
        </div>
        <div class="form-field">
            <label for="date-range" class="form-label">Date Range</label>
            <select id="date-range" name="date-range" class="form-input">
                <option value="1m">1 Month</option>
                <option value="3m">3 Months</option>
                <option value="1y">1 Year</option>
            </select>
        </div>
        <div class="form-field form-field-full-width">
            <button type="submit" class="responsive-button">Analyze Stock</button>
        </div>
    </form>
    """, unsafe_allow_html=True)
    
    # Table demo
    st.markdown("### 📊 Table Component")
    st.markdown("""
    <div class="table-responsive">
        <table class="responsive-table" role="table" aria-label="Stock analysis results">
            <thead>
                <tr>
                    <th scope="col">Ticker</th>
                    <th scope="col">Price</th>
                    <th scope="col">Change</th>
                    <th scope="col">Volume</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>AAPL</td>
                    <td>$150.25</td>
                    <td>+2.5%</td>
                    <td>1.2M</td>
                </tr>
                <tr>
                    <td>GOOGL</td>
                    <td>$2,750.80</td>
                    <td>-1.2%</td>
                    <td>800K</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    # Responsive information
    st.markdown("### 📐 Responsive Information")
    
    info_col1, info_col2, info_col3, info_col4 = st.columns(4)
    
    with info_col1:
        st.metric("Current Device", selected_device)
    
    with info_col2:
        st.metric("Breakpoints", len(responsive_system.BREAKPOINTS))
    
    with info_col3:
        st.metric("Touch Optimized", "Yes" if selected_device in ["Mobile (375px)", "Tablet (768px)"] else "No")
    
    with info_col4:
        st.metric("Grid Columns", "Auto" if "Mobile" in selected_device else "4" if "Desktop" in selected_device else "2")
    
    # Show CSS code
    if st.button("📋 Show Responsive CSS"):
        css = responsive_system.get_responsive_css()
        st.code(css, language="css")
    
    # Show JavaScript code
    if st.button("📋 Show Device Detection JS"):
        js = responsive_system.get_device_detection_js()
        st.code(js, language="javascript")
    
    # Show responsive guide
    if st.button("📖 Show Responsive Guide"):
        guide = responsive_system.generate_responsive_guide()
        st.markdown(guide)


if __name__ == "__main__":
    create_responsive_demo()