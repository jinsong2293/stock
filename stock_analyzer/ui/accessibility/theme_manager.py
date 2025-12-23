"""
Advanced theme manager với smooth transitions và user preference handling

Author: Roo - Architect Mode
Version: 1.0.0
"""

import streamlit as st
from typing import Dict, List, Optional
import json
from datetime import datetime

class ThemeManager:
    """Quản lý theme với persistence và smooth transitions"""
    
    def __init__(self, color_system=None):
        self.color_system = color_system
        self.themes = {
            'light': self._create_light_theme_config(),
            'dark': self._create_dark_theme_config(),
            'auto': self._create_auto_theme_config()
        }
        
        self.transition_duration = 300  # milliseconds
        self._setup_session_state()
    
    def _setup_session_state(self):
        """Initialize session state for theme management"""
        if 'theme_preference' not in st.session_state:
            # Try to detect system preference
            system_theme = self._detect_system_theme()
            st.session_state.theme_preference = system_theme
        
        if 'theme_transitioning' not in st.session_state:
            st.session_state.theme_transitioning = False
    
    def _detect_system_theme(self) -> str:
        """Auto-detect system theme preference"""
        # In a real implementation, this would use JavaScript to detect
        # For now, default to light theme
        return 'light'
    
    def _create_light_theme_config(self) -> Dict:
        """Create light theme configuration"""
        return {
            'name': 'Light Mode',
            'icon': '☀️',
            'description': 'Clean and bright interface for daytime use',
            'colors': self.color_system.light_theme if self.color_system else {},
            'is_dark': False
        }
    
    def _create_dark_theme_config(self) -> Dict:
        """Create dark theme configuration"""
        return {
            'name': 'Dark Mode', 
            'icon': '🌙',
            'description': 'Easy on the eyes for low-light environments',
            'colors': self.color_system.dark_theme if self.color_system else {},
            'is_dark': True
        }
    
    def _create_auto_theme_config(self) -> Dict:
        """Create auto theme configuration"""
        return {
            'name': 'Auto (System)',
            'icon': '🖥️',
            'description': 'Follow system preference automatically',
            'colors': {},  # Will be determined at runtime
            'is_dark': None  # Will be determined at runtime
        }
    
    def get_current_theme(self) -> str:
        """Lấy theme hiện tại"""
        return st.session_state.theme_preference
    
    def set_theme(self, theme: str, persist: bool = True):
        """Set theme với smooth transition"""
        valid_themes = ['light', 'dark', 'auto']
        if theme not in valid_themes:
            raise ValueError(f"Invalid theme: {theme}")
        
        current_theme = self.get_current_theme()
        if current_theme == theme:
            return  # No change needed
        
        # Start transition
        st.session_state.theme_transitioning = True
        
        # Update theme
        st.session_state.theme_preference = theme
        
        # Update color system if available
        if self.color_system:
            self.color_system.switch_theme(theme)
        
        # Persist to localStorage if requested
        if persist:
            self._persist_theme_preference(theme)
        
        # Trigger re-render
        st.rerun()
    
    def _persist_theme_preference(self, theme: str):
        """Persist theme preference to localStorage"""
        # This would be handled by JavaScript in a real implementation
        theme_data = {
            'theme': theme,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0'
        }
        
        # Store in session for now (would be localStorage in browser)
        if 'stored_theme' not in st.session_state:
            st.session_state.stored_theme = {}
        st.session_state.stored_theme['accessibility_theme'] = theme_data
    
    def toggle_theme(self):
        """Toggle between light and dark mode"""
        current = self.get_current_theme()
        if current == 'light':
            self.set_theme('dark')
        elif current == 'dark':
            self.set_theme('light')
        # Auto mode is not toggled
    
    def get_theme_options(self) -> List[Dict]:
        """Lấy danh sách theme options"""
        return [
            {
                'value': 'light',
                'label': '🌞 Light Mode',
                'description': 'Clean and bright interface'
            },
            {
                'value': 'dark', 
                'label': '🌙 Dark Mode',
                'description': 'Easy on the eyes for low-light'
            },
            {
                'value': 'auto',
                'label': '🖥️ Auto (System)',
                'description': 'Follow system preference'
            }
        ]
    
    def create_theme_toggle_component(self, key: str = "theme_toggle") -> str:
        """Create accessible theme toggle component HTML"""
        current_theme = self.get_current_theme()
        theme_options = self.get_theme_options()
        
        # Generate radio options
        radio_options = []
        for option in theme_options:
            checked = "checked" if option['value'] == current_theme else ""
            radio_options.append(f"""
                <div class="theme-option">
                    <input 
                        type="radio" 
                        id="theme_{option['value']}" 
                        name="theme_selector" 
                        value="{option['value']}"
                        {checked}
                        onchange="switchTheme('{option['value']}')"
                    >
                    <label for="theme_{option['value']}">
                        <span class="theme-icon">{option['label']}</span>
                        <span class="theme-description">{option['description']}</span>
                    </label>
                </div>
            """)
        
        component_html = f"""
        <div class="theme-toggle-component" id="{key}">
            <h3>🎨 Theme Settings</h3>
            <div class="theme-options">
                {''.join(radio_options)}
            </div>
        </div>
        
        <style>
        .theme-toggle-component {{
            background: var(--bg_secondary);
            border: 1px solid var(--border_primary);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
        }}
        
        .theme-toggle-component h3 {{
            margin: 0 0 1rem 0;
            color: var(--text_primary);
            font-size: 1.1rem;
        }}
        
        .theme-options {{
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }}
        
        .theme-option {{
            position: relative;
        }}
        
        .theme-option input[type="radio"] {{
            position: absolute;
            opacity: 0;
            width: 0;
            height: 0;
        }}
        
        .theme-option label {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 1rem;
            border: 2px solid var(--border_primary);
            border-radius: 8px;
            cursor: pointer;
            transition: all var(--transition-fast);
            background: var(--bg_primary);
        }}
        
        .theme-option label:hover {{
            border-color: var(--interactive_primary);
            background: var(--bg_accent);
        }}
        
        .theme-option input:checked + label {{
            border-color: var(--interactive_primary);
            background: var(--bg_accent);
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
        }}
        
        .theme-icon {{
            font-size: 1.25rem;
        }}
        
        .theme-description {{
            font-size: 0.9rem;
            color: var(--text_secondary);
        }}
        
        .theme-option input:checked + label .theme-description {{
            color: var(--text_primary);
            font-weight: 600;
        }}
        </style>
        
        <script>
        function switchTheme(theme) {{
            // Send theme change to Streamlit
            fetch('/theme/set', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                }},
                body: JSON.stringify({{ theme: theme }})
            }}).then(response => {{
                if (response.ok) {{
                    // Reload page to apply theme
                    location.reload();
                }}
            }});
        }}
        </script>
        """
        
        return component_html
    
    def handle_theme_api_call(self, theme_data: Dict) -> Dict:
        """Handle API calls for theme switching"""
        if 'theme' in theme_data:
            new_theme = theme_data['theme']
            self.set_theme(new_theme)
            return {
                'success': True,
                'theme': new_theme,
                'message': f'Switched to {new_theme} theme'
            }
        
        return {
            'success': False,
            'message': 'No theme specified'
        }