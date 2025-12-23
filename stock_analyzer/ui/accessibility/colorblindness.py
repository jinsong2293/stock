"""
Color blindness simulation và support system
Hỗ trợ người khiếm thị màu với simulation và alternative cues

Author: Roo - Architect Mode
Version: 1.0.0
"""

from typing import Dict, List, Tuple, Optional
import math

class ColorBlindnessSimulator:
    """Simulate và support cho different types of color blindness"""
    
    def __init__(self):
        # Color blindness transformation matrices
        self.transformation_matrices = {
            'protanopia': [
                [0.567, 0.433, 0.000],    # Red-blind
                [0.558, 0.442, 0.000],
                [0.000, 0.242, 0.758]
            ],
            'deuteranopia': [
                [0.625, 0.375, 0.000],    # Green-blind
                [0.700, 0.300, 0.000],
                [0.000, 0.300, 0.700]
            ],
            'tritanopia': [
                [0.950, 0.050, 0.000],    # Blue-blind
                [0.000, 0.433, 0.567],
                [0.000, 0.475, 0.525]
            ]
        }
        
        # Colorblind-safe color palette
        self.colorblind_safe_colors = {
            'primary': '#0066CC',      # Blue (safe for all types)
            'secondary': '#FF6600',    # Orange (high contrast)
            'success': '#009900',      # Green (protanopia safe)
            'warning': '#CC9900',      # Amber (deuteranopia safe)
            'error': '#CC0000',        # Red (tritanopia safe)
            'neutral': '#666666'       # Gray (always safe)
        }
        
        # Pattern mappings for visual differentiation
        self.pattern_mapping = {
            'success': 'linear-gradient(45deg, transparent 49%, rgba(255,255,255,0.3) 49%, rgba(255,255,255,0.3) 51%, transparent 51%)',
            'warning': 'repeating-linear-gradient(45deg, transparent, transparent 5px, rgba(255,255,255,0.3) 5px, rgba(255,255,255,0.3) 10px)',
            'error': 'radial-gradient(circle, rgba(255,255,255,0.3) 20%, transparent 20%)',
            'info': 'linear-gradient(90deg, transparent 50%, rgba(255,255,255,0.3) 50%)'
        }
    
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(self, rgb: Tuple[int, int, int]) -> str:
        """Convert RGB tuple to hex color"""
        return "#" + ''.join(f"{max(0, min(255, c)):02x}" for c in rgb)
    
    def simulate_color(self, hex_color: str, blindness_type: str = 'protanopia') -> str:
        """Simulate how a color appears to people with different types of color blindness"""
        if blindness_type not in self.transformation_matrices:
            return hex_color  # Return original if type not supported
        
        rgb = self.hex_to_rgb(hex_color)
        matrix = self.transformation_matrices[blindness_type]
        
        # Apply transformation matrix
        transformed = [
            max(0, min(255, int(rgb[0] * matrix[0][0] + rgb[1] * matrix[0][1] + rgb[2] * matrix[0][2]))),
            max(0, min(255, int(rgb[0] * matrix[1][0] + rgb[1] * matrix[1][1] + rgb[2] * matrix[1][2]))),
            max(0, min(255, int(rgb[0] * matrix[2][0] + rgb[1] * matrix[2][1] + rgb[2] * matrix[2][2])))
        ]
        
        return self.rgb_to_hex(tuple(transformed))
    
    def simulate_full_page(self, blindness_type: str = 'protanopia') -> str:
        """Generate CSS để simulate color blindness cho entire page"""
        if blindness_type not in self.transformation_matrices:
            return ""
        
        matrix = self.transformation_matrices[blindness_type]
        matrix_str = ' '.join(' '.join(map(str, row)) for row in matrix)
        
        return f"""
        <style>
        .colorblind-simulation-{blindness_type} {{
            filter: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg"><filter id="{blindness_type}"><feColorMatrix type="matrix" values="{matrix_str}"/></filter></svg>#{blindness_type}');
        }}
        </style>
        """
    
    def calculate_color_distinction(self, color1: str, color2: str, blindness_type: str = 'protanopia') -> float:
        """Calculate how distinguishable two colors are under color blindness"""
        sim_color1 = self.simulate_color(color1, blindness_type)
        sim_color2 = self.simulate_color(color2, blindness_type)
        
        rgb1 = self.hex_to_rgb(sim_color1)
        rgb2 = self.hex_to_rgb(sim_color2)
        
        # Calculate perceptual distance
        distance = math.sqrt(
            (rgb1[0] - rgb2[0]) ** 2 +
            (rgb1[1] - rgb2[1]) ** 2 +
            (rgb1[2] - rgb2[2]) ** 2
        )
        
        # Convert to percentage (0-100%)
        max_distance = math.sqrt(3 * 255 * 255)
        return (distance / max_distance) * 100
    
    def is_color_distinguishable(self, color1: str, color2: str, 
                                blindness_type: str = 'protanopia', 
                                threshold: float = 30.0) -> bool:
        """Check if two colors remain distinguishable under color blindness"""
        distinction_score = self.calculate_color_distinction(color1, color2, blindness_type)
        return distinction_score >= threshold
    
    def get_accessible_color_alternatives(self, failed_color: str, 
                                        context_colors: List[str],
                                        blindness_type: str = 'protanopia') -> List[Dict]:
        """Get color alternatives that work well under color blindness"""
        alternatives = []
        
        for alt_color in self.colorblind_safe_colors.values():
            is_distinguishable = True
            distinction_scores = []
            
            # Check against all context colors
            for context_color in context_colors:
                score = self.calculate_color_distinction(alt_color, context_color, blindness_type)
                distinction_scores.append(score)
                
                if score < 30.0:  # Minimum threshold
                    is_distinguishable = False
                    break
            
            if is_distinguishable:
                alternatives.append({
                    'color': alt_color,
                    'original': failed_color,
                    'blindness_type': blindness_type,
                    'distinction_scores': distinction_scores,
                    'min_distinction': min(distinction_scores),
                    'avg_distinction': sum(distinction_scores) / len(distinction_scores)
                })
        
        # Sort by average distinction score
        alternatives.sort(key=lambda x: x['avg_distinction'], reverse=True)
        return alternatives
    
    def get_pattern_for_status(self, status_type: str) -> str:
        """Get CSS pattern for a status type to aid color blind users"""
        return self.pattern_mapping.get(status_type, '')
    
    def generate_accessible_status_html(self, status_type: str, text: str, 
                                      color: str = None) -> str:
        """Generate HTML cho status indicator với multiple cues"""
        if color is None:
            color = self.colorblind_safe_colors.get(status_type, '#666666')
        
        pattern = self.get_pattern_for_status(status_type)
        
        # Icons for different statuses
        icons = {
            'success': '✓',
            'warning': '⚠',
            'error': '✗',
            'info': 'ℹ'
        }
        
        icon = icons.get(status_type, '•')
        
        html = f"""
        <div class="accessible-status status-{status_type}" 
             role="status" 
             aria-label="{text} status">
            <span class="status-pattern" aria-hidden="true"></span>
            <span class="status-icon" aria-hidden="true">{icon}</span>
            <span class="status-text">{text}</span>
            <span class="sr-only">{text} - {status_type} indicator</span>
        </div>
        
        <style>
        .accessible-status {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            font-weight: 600;
            background-color: {color};
            color: white;
            border: 2px solid {color};
            position: relative;
            overflow: hidden;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .status-pattern {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            opacity: 0.3;
            pointer-events: none;
            background: {pattern};
            background-size: 8px 8px;
        }}
        
        .status-icon {{
            font-weight: bold;
            font-size: 1.2em;
            z-index: 1;
        }}
        
        .status-text {{
            z-index: 1;
        }}
        
        /* Additional visual cues for color blind users */
        .status-success::after {{
            content: "";
            position: absolute;
            top: 2px;
            right: 2px;
            width: 8px;
            height: 8px;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 50%;
        }}
        
        .status-error::after {{
            content: "";
            position: absolute;
            top: 2px;
            right: 2px;
            width: 8px;
            height: 8px;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 0;
            transform: rotate(45deg);
        }}
        
        .status-warning::after {{
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
        
        return html
    
    def test_color_accessibility(self, color1: str, color2: str) -> Dict:
        """Test color accessibility across different types of color blindness"""
        results = {
            'original_colors': {
                'color1': color1,
                'color2': color2
            },
            'blindness_tests': {},
            'overall_accessibility': 'unknown',
            'recommendations': []
        }
        
        # Test under normal vision
        normal_score = self.calculate_color_distinction(color1, color2, 'none')
        results['blindness_tests']['normal'] = {
            'distinction_score': normal_score,
            'accessible': normal_score >= 30.0
        }
        
        # Test under different types of color blindness
        for cb_type in ['protanopia', 'deuteranopia', 'tritanopia']:
            score = self.calculate_color_distinction(color1, color2, cb_type)
            accessible = score >= 30.0
            
            results['blindness_tests'][cb_type] = {
                'distinction_score': score,
                'accessible': accessible,
                'simulated_color1': self.simulate_color(color1, cb_type),
                'simulated_color2': self.simulate_color(color2, cb_type)
            }
        
        # Determine overall accessibility
        all_accessible = all(
            test['accessible'] for test in results['blindness_tests'].values()
        )
        
        results['overall_accessibility'] = 'pass' if all_accessible else 'fail'
        
        # Add recommendations
        if not all_accessible:
            results['recommendations'].append('Consider using colorblind-safe alternatives')
            results['recommendations'].append('Add patterns or textures beyond color')
            results['recommendations'].append('Use icons or text labels as additional cues')
        
        return results
    
    def get_accessibility_guidelines(self) -> List[str]:
        """Get guidelines for creating accessible color schemes"""
        return [
            "Don't rely on color alone to convey information",
            "Use patterns, textures, or icons as additional visual cues",
            "Test colors under different types of color blindness",
            "Ensure sufficient contrast ratios (≥4.5:1 for normal text)",
            "Use colorblind-safe color palettes when possible",
            "Provide text labels for color-coded information",
            "Test with real color blind users when possible",
            "Consider cultural differences in color interpretation",
            "Use high contrast mode support",
            "Ensure compatibility with screen readers"
        ]
    
    def create_simulation_css(self, target_element: str = 'body') -> str:
        """Create CSS cho real-time color blindness simulation"""
        return f"""
        <style>
        /* Color blindness simulation styles */
        .simulation-controls {{
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            background: var(--bg_primary);
            border: 1px solid var(--border_primary);
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}
        
        .simulation-controls h4 {{
            margin: 0 0 0.5rem 0;
            color: var(--text_primary);
            font-size: 0.9rem;
        }}
        
        .simulation-button {{
            display: block;
            width: 100%;
            margin-bottom: 0.25rem;
            padding: 0.5rem;
            border: 1px solid var(--border_primary);
            background: var(--bg_secondary);
            color: var(--text_primary);
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.8rem;
        }}
        
        .simulation-button:hover {{
            background: var(--bg_accent);
        }}
        
        .simulation-button.active {{
            background: var(--interactive_primary);
            color: var(--text_inverse);
            border-color: var(--interactive_primary);
        }}
        </style>
        
        <div class="simulation-controls">
            <h4>Color Blindness Simulation</h4>
            <button class="simulation-button" onclick="toggleSimulation('none')" id="btn-normal">
                Normal Vision
            </button>
            <button class="simulation-button" onclick="toggleSimulation('protanopia')" id="btn-protanopia">
                Protanopia (Red-blind)
            </button>
            <button class="simulation-button" onclick="toggleSimulation('deuteranopia')" id="btn-deuteranopia">
                Deuteranopia (Green-blind)
            </button>
            <button class="simulation-button" onclick="toggleSimulation('tritanopia')" id="btn-tritanopia">
                Tritanopia (Blue-blind)
            </button>
        </div>
        
        <script>
        function toggleSimulation(type) {{
            const body = document.body;
            
            // Remove existing simulation classes
            body.classList.remove('colorblind-simulation-protanopia', 
                                  'colorblind-simulation-deuteranopia', 
                                  'colorblind-simulation-tritanopia');
            
            // Add new simulation class
            if (type !== 'none') {{
                body.classList.add(`colorblind-simulation-${{type}}`);
            }}
            
            // Update button states
            document.querySelectorAll('.simulation-button').forEach(btn => {{
                btn.classList.remove('active');
            }});
            
            if (type !== 'none') {{
                document.getElementById(`btn-${{type}}`).classList.add('active');
            }} else {{
                document.getElementById('btn-normal').classList.add('active');
            }}
        }}
        
        // Initialize normal vision
        toggleSimulation('none');
        </script>
        """