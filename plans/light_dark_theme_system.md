# Hệ thống Chế độ Tối và Chế độ Sáng với Tính Nhất quán Cao

## Tổng quan

Hệ thống theme được thiết kế để cung cấp trải nghiệm nhất quán và mượt mà giữa chế độ sáng và chế độ tối, với khả năng tự động phát hiện preference của người dùng và transition animations tinh tế.

## Nguyên tắc thiết kế Theme System

### 1. Semantic Color Mapping
- Sử dụng semantic color names thay vì literal color names
- Đảm bảo meaning của màu sắc nhất quán across themes
- Maintain brand identity across all themes
- Preserve accessibility standards trong cả hai modes

### 2. Smooth Transitions
- Animated transitions cho color changes
- Respect user preference cho reduced motion
- Optimize performance với GPU-accelerated animations
- Provide instant switching option cho accessibility

### 3. State Persistence
- Remember user theme preference
- Sync across tabs và sessions
- Graceful fallback khi preferences unavailable
- Clear visual feedback cho theme changes

## Theme Architecture

### 1. CSS Custom Properties Strategy

#### Base Theme System
```css
/* Theme system using CSS custom properties */
:root {
  /* Default theme variables - will be overridden by theme classes */
  
  /* Semantic color mapping */
  --color-background-primary: #ffffff;
  --color-background-secondary: #f8fafc;
  --color-background-tertiary: #f1f5f9;
  
  --color-text-primary: #0f172a;
  --color-text-secondary: #64748b;
  --color-text-tertiary: #94a3b8;
  
  --color-border-primary: #e2e8f0;
  --color-border-secondary: #cbd5e1;
  
  /* Interactive colors */
  --color-interactive-primary: #3b82f6;
  --color-interactive-hover: #2563eb;
  --color-interactive-active: #1d4ed8;
  --color-interactive-focus: #60a5fa;
  
  /* Semantic colors */
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  --color-info: #0ea5e9;
  
  /* Shadow system */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  
  /* Transitions */
  --transition-theme: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  --transition-fast: 0.15s ease-out;
  --transition-slow: 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Light theme */
.theme-light {
  --color-background-primary: #ffffff;
  --color-background-secondary: #f8fafc;
  --color-background-tertiary: #f1f5f9;
  --color-background-accent: #eff6ff;
  
  --color-text-primary: #0f172a;
  --color-text-secondary: #64748b;
  --color-text-tertiary: #94a3b8;
  --color-text-inverse: #f8fafc;
  
  --color-border-primary: #e2e8f0;
  --color-border-secondary: #cbd5e1;
  --color-border-tertiary: #94a3b8;
  
  --color-interactive-primary: #3b82f6;
  --color-interactive-hover: #2563eb;
  --color-interactive-active: #1d4ed8;
  --color-interactive-focus: #60a5fa;
  
  --color-success: #10b981;
  --color-success-background: #ecfdf5;
  --color-success-text: #065f46;
  
  --color-warning: #f59e0b;
  --color-warning-background: #fffbeb;
  --color-warning-text: #92400e;
  
  --color-error: #ef4444;
  --color-error-background: #fef2f2;
  --color-error-text: #991b1b;
  
  --color-info: #0ea5e9;
  --color-info-background: #f0f9ff;
  --color-info-text: #075985;
  
  /* Light theme shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
}

/* Dark theme */
.theme-dark {
  --color-background-primary: #0f172a;
  --color-background-secondary: #1e293b;
  --color-background-tertiary: #334155;
  --color-background-accent: #1e40af;
  
  --color-text-primary: #f8fafc;
  --color-text-secondary: #cbd5e1;
  --color-text-tertiary: #94a3b8;
  --color-text-inverse: #0f172a;
  
  --color-border-primary: #334155;
  --color-border-secondary: #475569;
  --color-border-tertiary: #64748b;
  
  /* Dark theme interactive colors - lighter for visibility */
  --color-interactive-primary: #60a5fa;
  --color-interactive-hover: #93c5fd;
  --color-interactive-active: #bfdbfe;
  --color-interactive-focus: #3b82f6;
  
  --color-success: #34d399;
  --color-success-background: #064e3b;
  --color-success-text: #a7f3d0;
  
  --color-warning: #fbbf24;
  --color-warning-background: #78350f;
  --color-warning-text: #fef3c7;
  
  --color-error: #f87171;
  --color-error-background: #7f1d1d;
  --color-error-text: #fecaca;
  
  --color-info: #7dd3fc;
  --color-info-background: #0c4a6e;
  --color-info-text: #bae6fd;
  
  /* Dark theme shadows - lighter for better visibility */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.3);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.4), 0 2px 4px -2px rgb(0 0 0 / 0.4);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.4), 0 4px 6px -4px rgb(0 0 0 / 0.4);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.5), 0 8px 10px -6px rgb(0 0 0 / 0.4);
}
```

### 2. Smooth Theme Transitions

#### Transition Implementation
```css
/* Global transition for theme changes */
* {
  transition: 
    background-color var(--transition-theme),
    color var(--transition-theme),
    border-color var(--transition-theme),
    box-shadow var(--transition-theme);
}

/* Specific component transitions */
.theme-transition {
  transition: all var(--transition-theme);
}

/* Instant transitions for accessibility */
@media (prefers-reduced-motion: reduce) {
  * {
    transition: none !important;
  }
}

/* Enhanced transitions for better UX */
.theme-enhanced-transition {
  transition: 
    background-color var(--transition-slow),
    color var(--transition-slow),
    border-color var(--transition-slow),
    box-shadow var(--transition-slow),
    transform var(--transition-fast);
}
```

#### Performance-Optimized Transitions
```css
/* GPU-accelerated transitions */
.gpu-accelerated {
  will-change: background-color, color;
  transform: translateZ(0); /* Force GPU layer */
}

/* Smooth color interpolation */
.smooth-theme-transition {
  transition: background-color 0.3s ease-in-out,
              color 0.3s ease-in-out,
              border-color 0.3s ease-in-out;
}

/* Staggered transitions for complex layouts */
.theme-stagger-1 { transition-delay: 0ms; }
.theme-stagger-2 { transition-delay: 50ms; }
.theme-stagger-3 { transition-delay: 100ms; }
.theme-stagger-4 { transition-delay: 150ms; }
```

### 3. Theme Detection and Management

#### JavaScript Theme Manager
```javascript
class ThemeManager {
  constructor() {
    this.currentTheme = this.getStoredTheme() || this.getSystemTheme();
    this.listeners = [];
    this.transitionDuration = 300;
    
    this.init();
  }
  
  init() {
    // Apply initial theme
    this.applyTheme(this.currentTheme);
    
    // Listen for system theme changes
    if (window.matchMedia) {
      this.mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      this.mediaQuery.addListener(this.handleSystemThemeChange.bind(this));
    }
    
    // Listen for storage changes (sync across tabs)
    window.addEventListener('storage', this.handleStorageChange.bind(this));
  }
  
  getSystemTheme() {
    if (!window.matchMedia) return 'light';
    
    return window.matchMedia('(prefers-color-scheme: dark)').matches 
      ? 'dark' 
      : 'light';
  }
  
  getStoredTheme() {
    try {
      return localStorage.getItem('theme-preference');
    } catch (e) {
      return null;
    }
  }
  
  storeTheme(theme) {
    try {
      localStorage.setItem('theme-preference', theme);
    } catch (e) {
      console.warn('Could not store theme preference:', e);
    }
  }
  
  toggleTheme() {
    const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
    this.setTheme(newTheme);
  }
  
  setTheme(theme, options = {}) {
    const { 
      store = true, 
      animate = true, 
      callback = null 
    } = options;
    
    // Prevent rapid switching
    if (this.isTransitioning) {
      return;
    }
    
    this.isTransitioning = true;
    
    // Store theme preference
    if (store) {
      this.storeTheme(theme);
    }
    
    // Apply theme with optional animation
    this.applyTheme(theme, { animate, callback });
    
    // Update current theme
    this.currentTheme = theme;
    
    // Notify listeners
    this.notifyListeners(theme);
    
    // Clear transitioning flag
    setTimeout(() => {
      this.isTransitioning = false;
    }, this.transitionDuration);
  }
  
  applyTheme(theme, options = {}) {
    const { animate = true, callback = null } = options;
    
    // Remove existing theme classes
    document.documentElement.classList.remove('theme-light', 'theme-dark');
    
    // Add new theme class
    document.documentElement.classList.add(`theme-${theme}`);
    
    // Set data attribute for CSS targeting
    document.documentElement.setAttribute('data-theme', theme);
    
    // Add transition class if animating
    if (animate && !this.prefersReducedMotion()) {
      document.documentElement.classList.add('theme-transitioning');
    }
    
    // Execute callback after transition
    if (callback) {
      setTimeout(callback, animate ? this.transitionDuration : 0);
    }
    
    // Remove transition class after animation
    if (animate) {
      setTimeout(() => {
        document.documentElement.classList.remove('theme-transitioning');
      }, this.transitionDuration);
    }
  }
  
  prefersReducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }
  
  handleSystemThemeChange(e) {
    // Only auto-switch if user hasn't manually set a preference
    const storedTheme = this.getStoredTheme();
    if (!storedTheme) {
      this.setTheme(e.matches ? 'dark' : 'light', { 
        store: false, 
        animate: true 
      });
    }
  }
  
  handleStorageChange(e) {
    if (e.key === 'theme-preference' && e.newValue !== this.currentTheme) {
      this.setTheme(e.newValue, { store: false, animate: true });
    }
  }
  
  subscribe(listener) {
    this.listeners.push(listener);
    return () => {
      const index = this.listeners.indexOf(listener);
      if (index > -1) {
        this.listeners.splice(index, 1);
      }
    };
  }
  
  notifyListeners(theme) {
    this.listeners.forEach(listener => {
      try {
        listener(theme);
      } catch (e) {
        console.error('Theme listener error:', e);
      }
    });
  }
  
  destroy() {
    if (this.mediaQuery) {
      this.mediaQuery.removeListener(this.handleSystemThemeChange.bind(this));
    }
    window.removeEventListener('storage', this.handleStorageChange.bind(this));
  }
}
```

### 4. Theme Toggle Component

#### HTML/CSS Implementation
```html
<!-- Theme toggle button -->
<button class="theme-toggle" aria-label="Toggle theme" title="Switch between light and dark mode">
  <span class="theme-toggle-icon theme-toggle-sun" aria-hidden="true">☀️</span>
  <span class="theme-toggle-icon theme-toggle-moon" aria-hidden="true">🌙</span>
  <span class="theme-toggle-text">Switch to dark mode</span>
</button>

<!-- CSS for theme toggle -->
<style>
.theme-toggle {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 2px solid var(--color-border-primary);
  border-radius: 2rem;
  background: var(--color-background-primary);
  color: var(--color-text-primary);
  cursor: pointer;
  transition: all var(--transition-theme);
  font-size: 0.875rem;
  font-weight: 500;
}

.theme-toggle:hover {
  background: var(--color-background-secondary);
  border-color: var(--color-interactive-primary);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.theme-toggle:focus {
  outline: 2px solid var(--color-interactive-focus);
  outline-offset: 2px;
}

.theme-toggle:active {
  transform: translateY(0);
}

/* Icon animations */
.theme-toggle-icon {
  font-size: 1.25rem;
  transition: transform var(--transition-theme), opacity var(--transition-theme);
}

.theme-light .theme-toggle-moon {
  transform: rotate(-90deg) scale(0);
  opacity: 0;
}

.theme-light .theme-toggle-sun {
  transform: rotate(0) scale(1);
  opacity: 1;
}

.theme-dark .theme-toggle-moon {
  transform: rotate(0) scale(1);
  opacity: 1;
}

.theme-dark .theme-toggle-sun {
  transform: rotate(90deg) scale(0);
  opacity: 0;
}

/* Text updates */
.theme-light .theme-toggle-text::after {
  content: "Switch to dark mode";
}

.theme-dark .theme-toggle-text::after {
  content: "Switch to light mode";
}

/* Mobile optimizations */
@media (max-width: 768px) {
  .theme-toggle {
    padding: 0.75rem;
    border-radius: 50%;
    min-width: 44px;
    min-height: 44px;
  }
  
  .theme-toggle-text {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }
  
  .theme-toggle-icon {
    font-size: 1.5rem;
  }
}
</style>
```

#### JavaScript Integration
```javascript
// Theme toggle initialization
document.addEventListener('DOMContentLoaded', () => {
  const themeManager = new ThemeManager();
  const toggleButton = document.querySelector('.theme-toggle');
  
  if (toggleButton) {
    toggleButton.addEventListener('click', () => {
      themeManager.toggleTheme();
    });
    
    // Update button state based on current theme
    themeManager.subscribe((theme) => {
      updateToggleButton(toggleButton, theme);
    });
  }
  
  // Initialize button state
  updateToggleButton(toggleButton, themeManager.currentTheme);
});

function updateToggleButton(button, theme) {
  if (!button) return;
  
  button.setAttribute('data-theme', theme);
  button.setAttribute('aria-pressed', theme === 'dark');
}
```

### 5. Advanced Theme Features

#### Theme System với Multiple Schemes
```css
/* Extended theme system */
:root {
  /* Base theme variables */
  --color-background-primary: #ffffff;
  --color-text-primary: #0f172a;
}

/* Auto theme (follows system preference) */
@media (prefers-color-scheme: dark) {
  :root:not(.theme-light):not(.theme-dark) {
    --color-background-primary: #0f172a;
    --color-text-primary: #f8fafc;
  }
}

/* High contrast theme */
.theme-high-contrast {
  --color-background-primary: #000000;
  --color-text-primary: #ffffff;
  --color-interactive-primary: #ffff00;
  --color-border-primary: #ffffff;
}

/* Sepia theme for reduced eye strain */
.theme-sepia {
  --color-background-primary: #f4ecd8;
  --color-text-primary: #5c4b37;
  --color-background-secondary: #ede0c8;
  --color-interactive-primary: #8b7355;
}

/* Blue light reduction theme */
.theme-blue-light {
  --color-background-primary: #fff4e6;
  --color-text-primary: #8b4513;
  --color-interactive-primary: #d2691e;
}
```

#### Dynamic Theme Creation
```javascript
class DynamicThemeCreator {
  constructor(themeManager) {
    this.themeManager = themeManager;
    this.customThemes = new Map();
  }
  
  createCustomTheme(name, colors) {
    const theme = this.generateThemeCSS(colors);
    this.injectThemeCSS(name, theme);
    this.customThemes.set(name, colors);
  }
  
  generateThemeCSS(colors) {
    const css = Object.entries(colors)
      .map(([key, value]) => `  --${key}: ${value};`)
      .join('\n');
    
    return `.theme-${name} {\n${css}\n}`;
  }
  
  injectThemeCSS(name, css) {
    const styleElement = document.createElement('style');
    styleElement.id = `theme-${name}`;
    styleElement.textContent = css;
    document.head.appendChild(styleElement);
  }
  
  switchToCustomTheme(name) {
    if (this.customThemes.has(name)) {
      this.themeManager.setTheme(name);
    }
  }
}
```

### 6. Performance Optimizations

#### CSS Optimization
```css
/* Critical CSS for theme switching */
.theme-critical {
  /* Inline only essential color variables */
  --bg-primary: #ffffff;
  --text-primary: #0f172a;
}

/* Non-critical variables loaded asynchronously */
.theme-extended {
  /* Additional color variables */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}

/* Optimize for GPU acceleration */
.theme-gpu-optimized {
  transform: translateZ(0);
  will-change: background-color, color;
}

/* Efficient theme switching */
.theme-switching {
  /* Disable complex animations during theme switch */
  transition: none;
}
```

#### JavaScript Performance
```javascript
// Optimized theme switching
class OptimizedThemeManager extends ThemeManager {
  constructor() {
    super();
    this.transitionFrame = null;
    this.rafThrottle = this.rafThrottle.bind(this);
  }
  
  setTheme(theme, options = {}) {
    // Throttle rapid theme switches
    if (this.transitionFrame) {
      cancelAnimationFrame(this.transitionFrame);
    }
    
    this.transitionFrame = requestAnimationFrame(() => {
      super.setTheme(theme, options);
    });
  }
  
  rafThrottle(callback) {
    // Use RAF for smooth animations
    requestAnimationFrame(callback);
  }
  
  // Optimize DOM updates
  applyTheme(theme, options = {}) {
    // Batch DOM updates
    requestAnimationFrame(() => {
      super.applyTheme(theme, options);
    });
  }
}
```

### 7. Accessibility Features

#### Screen Reader Support
```html
<!-- Accessible theme toggle -->
<div class="theme-controls">
  <fieldset role="radiogroup" aria-label="Theme selection">
    <legend class="sr-only">Choose theme</legend>
    
    <input type="radio" 
           id="theme-light" 
           name="theme" 
           value="light"
           aria-describedby="theme-light-desc">
    <label for="theme-light">
      <span aria-hidden="true">☀️</span>
      Light mode
      <span id="theme-light-desc" class="sr-only">Switch to light color scheme</span>
    </label>
    
    <input type="radio" 
           id="theme-dark" 
           name="theme" 
           value="dark"
           aria-describedby="theme-dark-desc">
    <label for="theme-dark">
      <span aria-hidden="true">🌙</span>
      Dark mode
      <span id="theme-dark-desc" class="sr-only">Switch to dark color scheme</span>
    </label>
    
    <input type="radio" 
           id="theme-auto" 
           name="theme" 
           value="auto"
           aria-describedby="theme-auto-desc">
    <label for="theme-auto">
      <span aria-hidden="true">🖥️</span>
      Auto (system)
      <span id="theme-auto-desc" class="sr-only">Follow system preference</span>
    </label>
  </fieldset>
</div>
```

#### Keyboard Navigation
```javascript
// Enhanced keyboard support
class AccessibleThemeManager extends ThemeManager {
  init() {
    super.init();
    this.setupKeyboardNavigation();
  }
  
  setupKeyboardNavigation() {
    document.addEventListener('keydown', (e) => {
      // Alt + T to toggle theme
      if (e.altKey && e.key === 't') {
        e.preventDefault();
        this.toggleTheme();
      }
      
      // Alt + 1, 2, 3 for specific themes
      if (e.altKey && ['1', '2', '3'].includes(e.key)) {
        e.preventDefault();
        const themes = ['light', 'dark', 'auto'];
        this.setTheme(themes[parseInt(e.key) - 1]);
      }
    });
  }
  
  // Announce theme changes to screen readers
  announceThemeChange(theme) {
    const announcement = `Theme changed to ${theme} mode`;
    this.createAnnouncement(announcement);
  }
  
  createAnnouncement(message) {
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.className = 'sr-only';
    announcement.textContent = message;
    
    document.body.appendChild(announcement);
    
    setTimeout(() => {
      document.body.removeChild(announcement);
    }, 1000);
  }
}
```

### 8. Testing Strategy

#### Theme Testing Framework
```javascript
class ThemeTestSuite {
  constructor(themeManager) {
    this.themeManager = themeManager;
    this.testResults = [];
  }
  
  async runAllTests() {
    console.log('🧪 Starting theme system tests...');
    
    await this.testThemeSwitching();
    await this.testAccessibility();
    await this.testPerformance();
    await this.testPersistence();
    await this.testResponsive();
    
    return this.generateReport();
  }
  
  async testThemeSwitching() {
    const themes = ['light', 'dark', 'auto'];
    
    for (const theme of themes) {
      await this.testThemeTransition(theme);
    }
    
    this.addResult('Theme Switching', '✅ All themes switch correctly');
  }
  
  async testThemeTransition(theme) {
    return new Promise((resolve) => {
      const startTime = performance.now();
      
      this.themeManager.setTheme(theme, {
        callback: () => {
          const duration = performance.now() - startTime;
          const passed = duration < 500; // Should switch within 500ms
          
          this.addResult(
            `Theme Transition ${theme}`,
            passed ? '✅ Fast transition' : '⚠️ Slow transition',
            { duration, passed }
          );
          
          resolve();
        }
      });
    });
  }
  
  async testAccessibility() {
    // Test contrast ratios
    const contrastTests = [
      { foreground: 'var(--color-text-primary)', background: 'var(--color-background-primary)' },
      { foreground: 'var(--color-text-secondary)', background: 'var(--color-background-primary)' },
    ];
    
    for (const test of contrastTests) {
      const ratio = this.calculateContrast(test.foreground, test.background);
      const passed = ratio >= 4.5;
      
      this.addResult(
        'Contrast Ratio',
        passed ? `✅ ${ratio}:1 ratio` : `❌ ${ratio}:1 ratio (needs 4.5:1)`,
        { ratio, passed }
      );
    }
  }
  
  addResult(testName, message, details = {}) {
    this.testResults.push({
      test: testName,
      message,
      details,
      timestamp: new Date().toISOString()
    });
  }
  
  generateReport() {
    const total = this.testResults.length;
    const passed = this.testResults.filter(r => 
      r.message.includes('✅') || !r.message.includes('❌')
    ).length;
    
    return {
      summary: {
        total,
        passed,
        failed: total - passed,
        passRate: `${Math.round((passed / total) * 100)}%`
      },
      results: this.testResults
    };
  }
}
```

## Implementation Guidelines

### 1. Integration với Stock Analyzer
```python
# Python integration for theme persistence
import json
import os
from datetime import datetime

class ThemePersistence:
    def __init__(self, config_path="theme_config.json"):
        self.config_path = config_path
        self.default_config = {
            "theme": "auto",
            "last_updated": datetime.now().isoformat(),
            "user_preference": None,
            "system_preference": self.detect_system_theme()
        }
    
    def detect_system_theme(self):
        """Detect system theme preference"""
        # This would integrate with the system's theme detection
        return "auto"  # Placeholder
    
    def get_theme_config(self):
        """Load theme configuration"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading theme config: {e}")
        
        return self.default_config.copy()
    
    def save_theme_config(self, config):
        """Save theme configuration"""
        try:
            config['last_updated'] = datetime.now().isoformat()
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Error saving theme config: {e}")
    
    def set_user_theme(self, theme):
        """Set user theme preference"""
        config = self.get_theme_config()
        config['user_preference'] = theme
        config['theme'] = theme  # Set current theme
        self.save_theme_config(config)
    
    def get_current_theme(self):
        """Get current theme (user preference or system default)"""
        config = self.get_theme_config()
        return config['user_preference'] or config['system_preference'] or 'light'
```

### 2. Streamlit Integration
```python
# Streamlit theme integration
import streamlit as st
from stock_analyzer.theme_manager import ThemeManager

def setup_theme_system():
    """Setup theme system for Streamlit app"""
    
    # Initialize theme manager
    if 'theme_manager' not in st.session_state:
        st.session_state.theme_manager = ThemeManager()
    
    # Theme toggle in sidebar
    with st.sidebar:
        st.markdown("### 🎨 Theme Settings")
        
        current_theme = st.session_state.theme_manager.get_current_theme()
        
        theme_options = {
            "Light": "light",
            "Dark": "dark", 
            "Auto (System)": "auto"
        }
        
        selected_theme = st.selectbox(
            "Choose theme",
            options=list(theme_options.keys()),
            index=list(theme_options.values()).index(current_theme),
            key="theme_selector"
        )
        
        # Update theme when selection changes
        if st.session_state.get('previous_theme') != selected_theme:
            st.session_state.theme_manager.set_user_theme(theme_options[selected_theme])
            st.session_state.previous_theme = selected_theme
            st.rerun()
    
    # Apply theme CSS
    apply_theme_css()

def apply_theme_css():
    """Apply theme CSS to Streamlit app"""
    theme = st.session_state.theme_manager.get_current_theme()
    
    css = f"""
    <style>
    /* Theme-specific styles */
    .theme-{theme} {{
        /* Theme CSS variables */
    }}
    
    /* Override Streamlit default styles */
    .stApp {{
        background-color: var(--color-background-primary);
        color: var(--color-text-primary);
    }}
    
    .main .block-container {{
        background-color: var(--color-background-primary);
    }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)
```

### 3. Quality Assurance Checklist

#### Functionality Testing
- [ ] Theme switching works across all browsers
- [ ] Theme preference persists across sessions
- [ ] System theme detection functions correctly
- [ ] Auto theme updates when system preference changes
- [ ] Theme toggles work with keyboard navigation
- [ ] Smooth transitions without layout shift

#### Accessibility Testing
- [ ] All color combinations meet WCAG AA standards
- [ ] Screen readers announce theme changes
- [ ] Keyboard navigation works for all theme controls
- [ ] High contrast mode supported
- [ ] Reduced motion preferences respected
- [ ] Focus indicators visible in all themes

#### Performance Testing
- [ ] Theme switch completes within 300ms
- [ ] No layout shift during theme transitions
- [ ] GPU acceleration working for animations
- [ ] Memory usage stable during theme switching
- [ ] Smooth 60fps animations

#### Cross-Platform Testing
- [ ] Works on Windows, macOS, Linux
- [ ] Mobile theme switching functional
- [ ] Tablet optimizations working
- [ ] Desktop refinements applied
- [ ] Print stylesheet compatibility

## Future Enhancements

### 1. Advanced Features
- [ ] Custom theme creation by users
- [ ] Theme scheduling (auto switch based on time)
- [ ] Location-based theme switching
- [ ] Accessibility preference learning
- [ ] Brand theme customization

### 2. Integration Expansions
- [ ] Operating system integration
- [ ] Browser extension support
- [ ] Design tool plugins
- [ ] Component library themes
- [ ] Framework-specific implementations

### 3. Performance Improvements
- [ ] Progressive theme loading
- [ ] Theme prefetching
- [ ] Optimized transition algorithms
- [ ] Enhanced GPU acceleration
- [ ] Reduced bundle size