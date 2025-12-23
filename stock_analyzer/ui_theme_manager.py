"""
UI Theme Manager - Quản lý theme và màu sắc cho ứng dụng Stock Analyzer
Hỗ trợ light mode và dark mode với hệ thống màu sắc hiện đại
"""

import streamlit as st
from typing import Dict, Any
import json
import os

class UIThemeManager:
    """Quản lý theme và styling cho ứng dụng"""
    
    # Enhanced color palettes for better accessibility and visual appeal
    COLOR_PALETTES = {
        "modern": {
            "light": {
                "primary": "#2563EB",          # Deep blue
                "primary_dark": "#1D4ED8",     # Darker blue
                "primary_light": "#93C5FD",    # Light blue
                "secondary": "#7C3AED",        # Purple
                "accent": "#06B6D4",           # Cyan
                "success": "#059669",          # Emerald green
                "warning": "#D97706",          # Amber
                "error": "#DC2626",            # Red
                "info": "#0891B2",             # Teal
            },
            "dark": {
                "primary": "#60A5FA",          # Light blue
                "primary_dark": "#3B82F6",     # Standard blue
                "primary_light": "#93C5FD",    # Very light blue
                "secondary": "#A78BFA",        # Light purple
                "accent": "#22D3EE",           # Light cyan
                "success": "#34D399",          # Light green
                "warning": "#FBBF24",          # Light amber
                "error": "#F87171",            # Light red
                "info": "#7DD3FC",             # Light teal
            }
        },
        "corporate": {
            "light": {
                "primary": "#1F2937",          # Slate gray
                "primary_dark": "#111827",     # Dark slate
                "primary_light": "#E5E7EB",    # Light gray
                "secondary": "#6B7280",        # Gray
                "accent": "#9CA3AF",           # Gray-300
                "success": "#10B981",          # Green
                "warning": "#F59E0B",          # Amber
                "error": "#EF4444",            # Red
                "info": "#3B82F6",             # Blue
            },
            "dark": {
                "primary": "#374151",          # Gray-700
                "primary_dark": "#1F2937",     # Gray-800
                "primary_light": "#9CA3AF",    # Gray-400
                "secondary": "#6B7280",        # Gray-600
                "accent": "#D1D5DB",           # Gray-300
                "success": "#34D399",          # Light green
                "warning": "#FBBF24",          # Light amber
                "error": "#F87171",            # Light red
                "info": "#60A5FA",             # Light blue
            }
        },
        "vibrant": {
            "light": {
                "primary": "#EF4444",          # Red
                "primary_dark": "#DC2626",     # Dark red
                "primary_light": "#FECACA",    # Light red
                "secondary": "#F59E0B",        # Amber
                "accent": "#10B981",           # Green
                "success": "#22C55E",          # Green
                "warning": "#F97316",          # Orange
                "error": "#EF4444",            # Red
                "info": "#3B82F6",             # Blue
            },
            "dark": {
                "primary": "#F87171",          # Light red
                "primary_dark": "#EF4444",     # Standard red
                "primary_light": "#FCA5A5",    # Very light red
                "secondary": "#FBBF24",        # Light amber
                "accent": "#34D399",           # Light green
                "success": "#86EFAC",          # Light green
                "warning": "#FDBA74",          # Light orange
                "error": "#F87171",            # Light red
                "info": "#60A5FA",             # Light blue
            }
        }
    }
    
    # Light theme colors
    LIGHT_THEME = {
        "primary": "#2563EB",          # Modern blue
        "primary_dark": "#1D4ED8",     # Darker blue
        "primary_light": "#93C5FD",    # Lighter blue
        "secondary": "#7C3AED",        # Purple
        "accent": "#06B6D4",           # Cyan
        "success": "#059669",          # Green
        "warning": "#D97706",          # Amber
        "error": "#DC2626",            # Red
        "info": "#0891B2",             # Blue
        
        # Background colors
        "bg_primary": "#FFFFFF",       # Pure white
        "bg_secondary": "#F8FAFC",     # Light gray
        "bg_tertiary": "#F1F5F9",      # Slightly darker gray
        "bg_accent": "#EFF6FF",        # Very light blue
        
        # Text colors
        "text_primary": "#0F172A",     # Very dark blue-gray
        "text_secondary": "#475569",   # Medium gray
        "text_tertiary": "#64748B",    # Lighter gray
        "text_inverse": "#FFFFFF",     # White text
        
        # Border colors
        "border_light": "#E2E8F0",     # Light border
        "border_medium": "#CBD5E1",    # Medium border
        "border_dark": "#94A3B8",      # Dark border
        
        # Chart colors
        "chart_1": "#2563EB",
        "chart_2": "#7C3AED", 
        "chart_3": "#06B6D4",
        "chart_4": "#059669",
        "chart_5": "#D97706",
        "chart_6": "#DC2626",
    }
    
    # Dark theme colors
    DARK_THEME = {
        "primary": "#60A5FA",          # Lighter blue for dark mode
        "primary_dark": "#3B82F6",     # Standard blue
        "primary_light": "#93C5FD",    # Very light blue
        "secondary": "#A78BFA",        # Lighter purple
        "accent": "#22D3EE",           # Lighter cyan
        "success": "#34D399",          # Lighter green
        "warning": "#FBBF24",          # Lighter amber
        "error": "#F87171",            # Lighter red
        "info": "#7DD3FC",             # Lighter blue
        
        # Background colors
        "bg_primary": "#0F172A",       # Very dark blue-gray
        "bg_secondary": "#1E293B",     # Dark blue-gray
        "bg_tertiary": "#334155",      # Medium dark blue-gray
        "bg_accent": "#1E40AF",        # Dark blue accent
        
        # Text colors
        "text_primary": "#F8FAFC",     # Very light gray
        "text_secondary": "#CBD5E1",   # Light gray
        "text_tertiary": "#94A3B8",    # Medium gray
        "text_inverse": "#0F172A",     # Dark text on light bg
        
        # Border colors
        "border_light": "#334155",     # Light border for dark mode
        "border_medium": "#475569",    # Medium border
        "border_dark": "#64748B",      # Dark border
        
        # Chart colors (optimized for dark background)
        "chart_1": "#60A5FA",
        "chart_2": "#A78BFA", 
        "chart_3": "#22D3EE",
        "chart_4": "#34D399",
        "chart_5": "#FBBF24",
        "chart_6": "#F87171",
    }
    
    def __init__(self):
        self.current_theme = self._get_stored_theme()
        self.current_palette = self._get_stored_palette()
        
    def _get_stored_theme(self) -> str:
        """Lấy theme đã lưu từ session state hoặc mặc định"""
        if 'ui_theme' not in st.session_state:
            st.session_state.ui_theme = 'light'
        return st.session_state.ui_theme
    
    def _get_stored_palette(self) -> str:
        """Lấy palette đã lưu từ session state hoặc mặc định"""
        if 'ui_palette' not in st.session_state:
            st.session_state.ui_palette = 'modern'
        return st.session_state.ui_palette
        
    def get_current_theme(self) -> Dict[str, str]:
        """Lấy colors của theme hiện tại"""
        return self.LIGHT_THEME if self.current_theme == 'light' else self.DARK_THEME
    
    def get_current_palette(self) -> Dict[str, str]:
        """Lấy palette hiện tại"""
        return self.COLOR_PALETTES[self.current_palette][self.current_theme]
    
    def set_palette(self, palette_name: str):
        """Thiết lập palette màu"""
        if palette_name in self.COLOR_PALETTES:
            self.current_palette = palette_name
            st.session_state.ui_palette = palette_name
    
    def toggle_theme(self):
        """Chuyển đổi giữa light và dark mode"""
        self.current_theme = 'dark' if self.current_theme == 'light' else 'light'
        st.session_state.ui_theme = self.current_theme
        st.rerun()
    
    def get_theme_colors_css(self) -> str:
        """Tạo CSS variables cho theme hiện tại"""
        theme = self.get_current_theme()
        palette = self.get_current_palette()
        css_vars = []
        
        # Combine base theme with palette colors
        combined_theme = {**theme, **palette}
        
        for key, value in combined_theme.items():
            css_vars.append(f"    --{key}: {value};")
        
        return "\n".join(css_vars)
    
    def get_theme_status_emoji(self) -> str:
        """Lấy emoji cho theme hiện tại"""
        return "🌙" if self.current_theme == 'dark' else "☀️"
    
    def get_theme_status_text(self) -> str:
        """Lấy text cho theme hiện tại"""
        return "Dark Mode" if self.current_theme == 'dark' else "Light Mode"
    
    def get_palette_options(self) -> list:
        """Lấy danh sách các palette có sẵn"""
        return list(self.COLOR_PALETTES.keys())
    
    def get_contrast_ratio(self, color1: str, color2: str) -> float:
        """Tính toán contrast ratio giữa 2 màu (cho accessibility)"""
        # Simplified contrast ratio calculation
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        def get_luminance(rgb):
            def channel_luminance(c):
                c = c / 255.0
                return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
            
            r, g, b = rgb
            return 0.2126 * channel_luminance(r) + 0.7152 * channel_luminance(g) + 0.0722 * channel_luminance(b)
        
        rgb1 = hex_to_rgb(color1)
        rgb2 = hex_to_rgb(color2)
        
        lum1 = get_luminance(rgb1)
        lum2 = get_luminance(rgb2)
        
        lighter = max(lum1, lum2)
        darker = min(lum1, lum2)
        
        return (lighter + 0.05) / (darker + 0.05)
    
    def is_accessible(self, foreground: str, background: str) -> bool:
        """Kiểm tra xem màu có đạt chuẩn accessibility không"""
        ratio = self.get_contrast_ratio(foreground, background)
        return ratio >= 4.5  # WCAG AA standard
    
    def get_accessible_text_color(self, background: str) -> str:
        """Lấy màu text phù hợp với background để đảm bảo accessibility"""
        white = "#FFFFFF"
        black = "#000000"
        
        if self.get_contrast_ratio(white, background) >= 4.5:
            return white
        elif self.get_contrast_ratio(black, background) >= 4.5:
            return black
        else:
            # Fallback to white if neither works well
            return white

# Global instance
theme_manager = UIThemeManager()
