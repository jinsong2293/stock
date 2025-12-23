"""
Accessibility Color System for Stock Analyzer
Main entry point for all accessibility features

Author: Roo - Architect Mode
Version: 1.0.0
"""

from .color_system import AccessibilityColorSystem
from .theme_manager import ThemeManager
from .contrast_checker import ContrastChecker
from .colorblindness import ColorBlindnessSimulator
from .performance_monitor import AccessibilityPerformanceMonitor

__version__ = "1.0.0"
__all__ = [
    'AccessibilityColorSystem',
    'ThemeManager',
    'ContrastChecker',
    'ColorBlindnessSimulator',
    'AccessibilityPerformanceMonitor'
]