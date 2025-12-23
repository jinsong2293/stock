# Professional Design System - Stock Analyzer

## 🎨 Tổng quan Design System

Hệ thống thiết kế chuyên nghiệp cho ứng dụng Stock Analyzer với phong cách hiện đại, tinh tế và tối ưu trải nghiệm người dùng.

## 🌈 Hệ thống Màu sắc

### Primary Colors - Financial Theme
```css
--color-primary-50: #f0f9ff   /* Very light blue */
--color-primary-100: #e0f2fe  /* Light blue */
--color-primary-200: #bae6fd  /* Lighter blue */
--color-primary-300: #7dd3fc  /* Light blue */
--color-primary-400: #38bdf8  /* Medium light blue */
--color-primary-500: #0ea5e9  /* Primary blue */
--color-primary-600: #0284c7  /* Primary dark blue */
--color-primary-700: #0369a1  /* Dark blue */
--color-primary-800: #075985  /* Darker blue */
--color-primary-900: #0c4a6e  /* Very dark blue */
```

### Success Colors - Profit/Growth
```css
--color-success-500: #22c55e  /* Primary green */
--color-success-600: #16a34a  /* Primary dark green */
--color-success-700: #15803d  /* Dark green */
```

### Warning Colors - Risk/Caution
```css
--color-warning-500: #f59e0b  /* Primary amber */
--color-warning-600: #d97706  /* Primary dark amber */
--color-warning-700: #b45309  /* Dark amber */
```

### Error Colors - Loss/Danger
```css
--color-error-500: #ef4444  /* Primary red */
--color-error-600: #dc2626  /* Primary dark red */
--color-error-700: #b91c1c  /* Dark red */
```

### Financial Colors - Specialized
```css
--color-bull-market: #16a34a      /* Bull market - Green */
--color-bear-market: #dc2626      /* Bear market - Red */
--color-neutral-market: #64748b   /* Neutral market - Gray */
--color-gold: #ffd700             /* Gold highlight */
--color-silver: #c0c0c0           /* Silver highlight */
--color-chart-line: #38bdf8       /* Chart line color */
--color-chart-fill: #bae6fd       /* Chart fill color */
```

### Gradients - Premium Look
```css
--gradient-primary: linear-gradient(135deg, #0284c7 0%, #075985 100%)
--gradient-success: linear-gradient(135deg, #22c55e 0%, #15803d 100%)
--gradient-warning: linear-gradient(135deg, #f59e0b 0%, #b45309 100%)
--gradient-error: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%)
--gradient-premium: linear-gradient(135deg, #ffd700 0%, #b87333 100%)
```

## 📝 Typography System

### Font Families
```css
--font-primary: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif
--font-mono: "JetBrains Mono", "Fira Code", Consolas, Monaco, monospace
--font-display: "Poppins", "Inter", -apple-system, BlinkMacSystemFont, sans-serif
```

### Font Sizes (8-point grid)
```css
--font-size-xs: 0.75rem    /* 12px - Small labels */
--font-size-sm: 0.875rem   /* 14px - Body text */
--font-size-base: 1rem     /* 16px - Base text */
--font-size-lg: 1.125rem   /* 18px - Large text */
--font-size-xl: 1.25rem    /* 20px - Subheadings */
--font-size-2xl: 1.5rem    /* 24px - Headings */
--font-size-3xl: 1.875rem  /* 30px - Large headings */
--font-size-4xl: 2.25rem   /* 36px - Page titles */
--font-size-5xl: 3rem      /* 48px - Display text */
```

### Font Weights
```css
--font-weight-light: 300
--font-weight-normal: 400
--font-weight-medium: 500
--font-weight-semibold: 600
--font-weight-bold: 700
--font-weight-extrabold: 800
--font-weight-black: 900
```

### Typography Presets
```css
.text-display-large {
  font-family: "Poppins", "Inter", sans-serif;
  font-size: 3rem;           /* 48px */
  font-weight: 700;
  line-height: 1.25;
  letter-spacing: -0.025em;
}

.text-heading-1 {
  font-family: "Inter", sans-serif;
  font-size: 1.875rem;       /* 30px */
  font-weight: 700;
  line-height: 1.25;
  letter-spacing: -0.025em;
}

.text-heading-2 {
  font-family: "Inter", sans-serif;
  font-size: 1.5rem;         /* 24px */
  font-weight: 600;
  line-height: 1.5;
  letter-spacing: -0.025em;
}

.text-body {
  font-family: "Inter", sans-serif;
  font-size: 1rem;           /* 16px */
  font-weight: 400;
  line-height: 1.5;
}

.text-caption {
  font-family: "Inter", sans-serif;
  font-size: 0.75rem;        /* 12px */
  font-weight: 500;
  line-height: 1.5;
  letter-spacing: 0.025em;
}
```

## 📏 Spacing System

### Base Spacing (8-point grid)
```css
--spacing-px: 1px
--spacing-0: 0px
--spacing-1: 0.25rem   /* 4px */
--spacing-2: 0.5rem    /* 8px */
--spacing-3: 0.75rem   /* 12px */
--spacing-4: 1rem      /* 16px */
--spacing-5: 1.25rem   /* 20px */
--spacing-6: 1.5rem    /* 24px */
--spacing-8: 2rem      /* 32px */
--spacing-10: 2.5rem   /* 40px */
--spacing-12: 3rem     /* 48px */
--spacing-16: 4rem     /* 64px */
--spacing-20: 5rem     /* 80px */
--spacing-24: 6rem     /* 96px */
--spacing-32: 8rem     /* 128px */
```

### Component Spacing
```css
--spacing-button-padding: 0.75rem 1.5rem   /* 12px 24px */
--spacing-card-padding: 1.5rem 2rem        /* 24px 32px */
--spacing-section-margin: 4rem             /* 64px */
--spacing-subsection-margin: 3rem          /* 48px */
--spacing-element-gap: 1rem                /* 16px */
--spacing-dense-gap: 0.5rem                /* 8px */
--spacing-loose-gap: 2rem                  /* 32px */
```

### Layout Spacing
```css
--spacing-page-margin: 2rem               /* 32px */
--spacing-container-padding: 1.5rem        /* 24px */
--spacing-sidebar-width: 320px
--spacing-header-height: 80px
--spacing-footer-height: 60px
```

## 🔮 Shadow System

### Shadow Presets
```css
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05)
--shadow-base: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)
--shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25)
--shadow-financial: 0 8px 32px rgba(0, 0, 0, 0.12), 0 4px 16px rgba(0, 0, 0, 0.08)
--shadow-premium: 0 16px 64px rgba(0, 0, 0, 0.16), 0 8px 32px rgba(0, 0, 0, 0.12)
```

## 🔘 Border Radius System

```css
--radius-none: 0px
--radius-sm: 0.125rem     /* 2px */
--radius-base: 0.25rem    /* 4px */
--radius-md: 0.375rem     /* 6px */
--radius-lg: 0.5rem       /* 8px */
--radius-xl: 0.75rem      /* 12px */
--radius-2xl: 1rem        /* 16px */
--radius-3xl: 1.5rem      /* 24px */
--radius-full: 9999px     /* Full round */
--radius-financial: 0.75rem    /* 12 */
--radius-prepx - premium feelmium: 1rem         /* 16px - ultra premium */
```

## 🧩 Component System

### Card Components

#### Base Card
```html
<div class="card-base">
  <h3 class="text-heading-2">Card Title</h3>
  <p class="text-body">Card content goes here</p>
</div>
```

#### Premium Card
```html
<div class="card-premium">
  <h3 class="text-heading-2">Premium Card Title</h3>
  <p class="text-body">Premium card content with golden accent</p>
</div>
```

### Button Components

#### Primary Button
```html
<button class="btn-primary">
  <span>Primary Action</span>
</button>
```

#### Secondary Button
```html
<button class="btn-secondary">
  <span>Secondary Action</span>
</button>
```

### Metric Card
```html
<div class="metric-card">
  <div class="text-caption">Metric Title</div>
  <div class="text-heading-2">1,234.56</div>
  <div class="text-body-small metric-change positive">+5.67%</div>
</div>
```

### Status Badge
```html
<span class="status-badge status-success">Success</span>
<span class="status-badge status-warning">Warning</span>
<span class="status-badge status-error">Error</span>
<span class="status-badge status-info">Info</span>
```

## 📱 Responsive Design

### Breakpoints
```css
/* Mobile First Approach */
@media (max-width: 640px) { /* sm */ }
@media (max-width: 768px) { /* md */ }
@media (max-width: 1024px) { /* lg */ }
@media (max-width: 1280px) { /* xl */ }
@media (max-width: 1536px) { /* 2xl */ }
```

### Grid System
```css
.grid {
  display: grid;
  gap: var(--spacing-element-gap);
}

.grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
.grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.grid-cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }

/* Responsive Grid */
@media (max-width: 768px) {
  .grid-cols-4 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .grid-cols-3 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
```

## 🎭 Animation & Transitions

### Standard Transitions
```css
/* Hover Transitions */
.card-base {
  transition: all 0.3s ease;
}

.card-base:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-premium);
}

/* Loading Animation */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.loading-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
```

### Accessibility
```css
/* Reduced Motion */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Focus States */
.btn-primary:focus,
.btn-secondary:focus {
  outline: 2px solid var(--color-primary-400);
  outline-offset: 2px;
}
```

## 🎨 Usage Guidelines

### Color Usage
- **Primary**: Main actions, headers, primary CTAs
- **Success**: Positive metrics, profits, buy signals
- **Warning**: Caution indicators, risk warnings
- **Error**: Negative metrics, losses, sell signals
- **Neutral**: Secondary information, background elements

### Typography Hierarchy
1. **Display Large**: Main page titles, hero sections
2. **Heading 1**: Major section headers
3. **Heading 2**: Subsection headers
4. **Heading 3**: Component titles
5. **Body Large**: Important body text
6. **Body**: Standard body text
7. **Body Small**: Supporting text
8. **Caption**: Labels, annotations, metadata

### Spacing Principles
- Use 8px grid system for consistent spacing
- Group related elements with tighter spacing
- Separate sections with larger spacing
- Maintain visual rhythm throughout the interface

## 📋 Implementation Checklist

### Phase 2 Progress
- [x] Nâng cấp bảng màu với palette chuyên nghiệp
- [x] Cải thiện typography hierarchy  
- [x] Tạo spacing system nhất quán
- [ ] Thiết kế icon set và visual elements

### Next Phases
- [ ] Modern card components
- [ ] Data visualization components
- [ ] Navigation and layout components
- [ ] Interactive elements
- [ ] Chart enhancements
- [ ] Loading states and transitions

## 🎯 Key Features

1. **Professional Aesthetic**: Business-grade appearance suitable for financial applications
2. **Accessibility First**: WCAG compliant with proper contrast ratios and focus states
3. **Responsive Design**: Mobile-first approach with seamless desktop experience
4. **Performance Optimized**: Efficient CSS with minimal reflows and repaints
5. **Consistent System**: Unified design tokens across all components
6. **Scalable Architecture**: Easy to extend and maintain