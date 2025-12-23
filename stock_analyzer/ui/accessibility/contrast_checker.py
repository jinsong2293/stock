"""
Color contrast checker với WCAG 2.1 AA compliance
Tính toán tỷ lệ tương phản và kiểm tra accessibility

Author: Roo - Architect Mode
Version: 1.0.0
"""

from typing import Dict, List, Tuple, Optional, Union
import math

class ContrastChecker:
    """Kiểm tra tương phản màu sắc theo chuẩn WCAG 2.1"""
    
    def __init__(self):
        # WCAG thresholds
        self.wcag_aa_normal = 4.5
        self.wcag_aa_large = 3.0
        self.wcag_aaa_normal = 7.0
        self.wcag_aaa_large = 4.5
        
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            # Handle 3-digit hex colors
            hex_color = ''.join([c*2 for c in hex_color])
        
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_luminance(self, r: int, g: int, b: int) -> float:
        """Calculate relative luminance of RGB color"""
        def linearize(c):
            c = c / 255.0
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        
        r_linear = linearize(r)
        g_linear = linearize(g)
        b_linear = linearize(b)
        
        return 0.2126 * r_linear + 0.7152 * g_linear + 0.0722 * b_linear
    
    def calculate_contrast_ratio(self, color1: str, color2: str) -> float:
        """Calculate WCAG contrast ratio between two colors"""
        rgb1 = self.hex_to_rgb(color1)
        rgb2 = self.hex_to_rgb(color2)
        
        lum1 = self.rgb_to_luminance(*rgb1)
        lum2 = self.rgb_to_luminance(*rgb2)
        
        lighter = max(lum1, lum2)
        darker = min(lum1, lum2)
        
        return (lighter + 0.05) / (darker + 0.05)
    
    def get_wcag_level(self, ratio: float, is_large_text: bool = False) -> str:
        """Determine WCAG compliance level based on contrast ratio"""
        if is_large_text:
            if ratio >= self.wcag_aaa_large:
                return "AAA"
            elif ratio >= self.wcag_aa_large:
                return "AA"
            elif ratio >= 3.0:
                return "AA Large"
        else:
            if ratio >= self.wcag_aaa_normal:
                return "AAA"
            elif ratio >= self.wcag_aa_normal:
                return "AA"
        
        return "Fail"
    
    def validate_contrast(self, foreground: str, background: str, 
                         is_large_text: bool = False) -> Dict:
        """Validate color contrast và return detailed analysis"""
        try:
            ratio = self.calculate_contrast_ratio(foreground, background)
            level = self.get_wcag_level(ratio, is_large_text)
            
            # Determine required ratio based on text size
            required_ratio = self.wcag_aa_large if is_large_text else self.wcag_aa_normal
            passes_aa = ratio >= required_ratio
            passes_aaa = ratio >= (self.wcag_aaa_large if is_large_text else self.wcag_aaa_normal)
            
            return {
                'foreground': foreground,
                'background': background,
                'contrast_ratio': round(ratio, 2),
                'wcag_level': level,
                'required_ratio': required_ratio,
                'passes_aa': passes_aa,
                'passes_aaa': passes_aaa,
                'is_large_text': is_large_text,
                'recommendation': self._get_recommendation(ratio, level, is_large_text),
                'status': 'pass' if passes_aa else 'fail'
            }
        except Exception as e:
            return {
                'foreground': foreground,
                'background': background,
                'error': str(e),
                'status': 'error'
            }
    
    def _get_recommendation(self, ratio: float, level: str, is_large_text: bool) -> str:
        """Get recommendation based on contrast ratio"""
        required_ratio = self.wcag_aa_large if is_large_text else self.wcag_aa_normal
        
        if ratio >= self.wcag_aaa_normal:
            return f"Excellent contrast ({ratio:.2f}:1) - exceeds AAA standard"
        elif ratio >= self.wcag_aa_normal:
            return f"Good contrast ({ratio:.2f}:1) - meets AA standard"
        elif ratio >= required_ratio:
            return f"Acceptable contrast ({ratio:.2f}:1) for large text"
        else:
            return f"Insufficient contrast ({ratio:.2f}:1) - needs {required_ratio}:1 ratio"
    
    def batch_validate(self, color_pairs: List[Tuple[str, str]], 
                      is_large_text: bool = False) -> List[Dict]:
        """Validate multiple color pairs"""
        results = []
        for fg, bg in color_pairs:
            result = self.validate_contrast(fg, bg, is_large_text)
            results.append(result)
        return results
    
    def find_accessible_combinations(self, foreground_colors: List[str], 
                                   background_colors: List[str],
                                   is_large_text: bool = False) -> List[Dict]:
        """Find all accessible color combinations"""
        accessible_pairs = []
        
        for fg in foreground_colors:
            for bg in background_colors:
                result = self.validate_contrast(fg, bg, is_large_text)
                if result['passes_aa']:
                    accessible_pairs.append(result)
        
        # Sort by contrast ratio (highest first)
        accessible_pairs.sort(key=lambda x: x['contrast_ratio'], reverse=True)
        return accessible_pairs
    
    def get_accessible_text_color(self, background: str) -> str:
        """Get the best text color for a given background"""
        white = "#FFFFFF"
        black = "#000000"
        
        white_ratio = self.calculate_contrast_ratio(white, background)
        black_ratio = self.calculate_contrast_ratio(black, background)
        
        if white_ratio >= self.wcag_aa_normal:
            return white
        elif black_ratio >= self.wcag_aa_normal:
            return black
        else:
            # Fallback: choose the higher ratio even if below 4.5
            return white if white_ratio > black_ratio else black
    
    def simulate_colorblind_contrast(self, foreground: str, background: str, 
                                   cb_type: str = 'protanopia') -> Dict:
        """Simulate contrast under color blindness conditions"""
        from .colorblindness import ColorBlindnessSimulator
        
        simulator = ColorBlindnessSimulator()
        
        # Simulate how colors appear to color blind users
        sim_fg = simulator.simulate_color(foreground, cb_type)
        sim_bg = simulator.simulate_color(background, cb_type)
        
        # Calculate contrast for simulated colors
        original_ratio = self.calculate_contrast_ratio(foreground, background)
        simulated_ratio = self.calculate_contrast_ratio(sim_fg, sim_bg)
        
        return {
            'original_contrast': round(original_ratio, 2),
            'simulated_contrast': round(simulated_ratio, 2),
            'colorblind_type': cb_type,
            'foreground_simulated': sim_fg,
            'background_simulated': sim_bg,
            'preserved_readability': simulated_ratio >= self.wcag_aa_normal,
            'contrast_loss': round(original_ratio - simulated_ratio, 2)
        }
    
    def create_accessibility_report(self, color_system) -> Dict:
        """Create comprehensive accessibility report for a color system"""
        report = {
            'timestamp': '2025-12-22T06:29:17Z',
            'system_info': {
                'name': 'Stock Analyzer Accessibility Color System',
                'version': '1.0.0',
                'wcag_version': '2.1'
            },
            'theme_analysis': {},
            'overall_status': 'unknown',
            'recommendations': []
        }
        
        # Analyze light theme
        light_theme = color_system.light_theme
        light_analysis = self._analyze_theme_colors(light_theme, 'Light Theme')
        report['theme_analysis']['light'] = light_analysis
        
        # Analyze dark theme
        dark_theme = color_system.dark_theme
        dark_analysis = self._analyze_theme_colors(dark_theme, 'Dark Theme')
        report['theme_analysis']['dark'] = dark_analysis
        
        # Determine overall status
        all_passed = (light_analysis['summary']['passed'] == light_analysis['summary']['total'] and
                     dark_analysis['summary']['passed'] == dark_analysis['summary']['total'])
        
        report['overall_status'] = 'pass' if all_passed else 'fail'
        
        # Add recommendations
        if not all_passed:
            report['recommendations'].append("Some color combinations fail WCAG AA standards")
            report['recommendations'].append("Review and adjust failing color pairs")
        
        return report
    
    def _analyze_theme_colors(self, theme: Dict[str, str], theme_name: str) -> Dict:
        """Analyze colors in a theme for accessibility"""
        analysis = {
            'theme_name': theme_name,
            'color_checks': [],
            'summary': {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'warnings': 0
            }
        }
        
        # Test text colors against background
        bg_color = theme.get('bg_primary', '#FFFFFF')
        text_colors = ['text_primary', 'text_secondary', 'text_tertiary']
        
        for text_color in text_colors:
            if text_color in theme:
                result = self.validate_contrast(theme[text_color], bg_color)
                result['test_type'] = 'text_contrast'
                result['color_name'] = text_color
                analysis['color_checks'].append(result)
                analysis['summary']['total'] += 1
                
                if result['passes_aa']:
                    analysis['summary']['passed'] += 1
                else:
                    analysis['summary']['failed'] += 1
        
        # Test interactive colors
        interactive_colors = ['interactive_primary', 'interactive_hover', 'interactive_active']
        interactive_bg = theme.get('bg_secondary', '#F8FAFC')
        
        for int_color in interactive_colors:
            if int_color in theme:
                result = self.validate_contrast(theme[int_color], interactive_bg)
                result['test_type'] = 'interactive_contrast'
                result['color_name'] = int_color
                analysis['color_checks'].append(result)
                analysis['summary']['total'] += 1
                
                if result['passes_aa']:
                    analysis['summary']['passed'] += 1
                else:
                    analysis['summary']['failed'] += 1
        
        # Test semantic colors (text on colored background)
        semantic_colors = ['success', 'warning', 'error', 'info']
        for sem_color in semantic_colors:
            if sem_color in theme:
                text_color = self.get_accessible_text_color(theme[sem_color])
                result = self.validate_contrast(text_color, theme[sem_color])
                result['test_type'] = 'semantic_contrast'
                result['color_name'] = sem_color
                analysis['color_checks'].append(result)
                analysis['summary']['total'] += 1
                
                if result['passes_aa']:
                    analysis['summary']['passed'] += 1
                else:
                    analysis['summary']['failed'] += 1
        
        return analysis