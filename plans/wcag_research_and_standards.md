# WCAG 2.1 AA Standards Research & Color Accessibility Guidelines

## Tổng quan về WCAG 2.1 AA

### Định nghĩa
WCAG 2.1 (Web Content Accessibility Guidelines) là bộ hướng dẫn quốc tế về accessibility cho nội dung web. Mức độ AA là cấp độ trung bình, đảm bảo accessibility cho đa số người dùng.

### Nguyên tắc cơ bản (POUR)
1. **Perceivable** (Có thể nhận thức được)
2. **Operable** (Có thể vận hành được)
3. **Understandable** (Có thể hiểu được)
4. **Robust** (Mạnh mẽ, tương thích)

## Tiêu chuẩn màu sắc cụ thể

### 1. Contrast Ratio Requirements (Yêu cầu tỷ lệ tương phản)

#### Text thường (Normal Text)
- **Mức tối thiểu**: 4.5:1 (WCAG AA)
- **Mức khuyến nghị**: 7:1 (WCAG AAA)

#### Text lớn (Large Text)
- **Mức tối thiểu**: 3:1 (WCAG AA)
- **Mức khuyến nghị**: 4.5:1 (WCAG AAA)

#### Icons và UI Components
- **Mức tối thiểu**: 3:1 (WCAG AA)

### 2. Color as Information (Màu sắc như thông tin)

#### Nguyên tắc
- Không được sử dụng màu sắc duy nhất để truyền tải thông tin
- Phải có phương thức khác ngoài màu sắc (icon, text, pattern)

#### Ví dụ đúng/sai
```css
/* ✅ Đúng: Có text và icon bổ sung */
.success { color: #059669; }
.success::before { content: "✓"; }

/* ❌ Sai: Chỉ dùng màu */
.error { color: #DC2626; }
```

### 3. Text Spacing (Khoảng cách văn bản)

#### Yêu cầu tối thiểu
- Line height: Ít nhất 1.5
- Letter spacing: Ít nhất 0.12em
- Word spacing: Ít nhất 0.16em

## Loại màu sắc và ứng dụng

### 1. Semantic Colors (Màu ngữ nghĩa)
```css
:root {
  /* Success States */
  --color-success: #059669;
  --color-success-bg: #D1FAE5;
  --color-success-text: #065F46;
  
  /* Warning States */
  --color-warning: #D97706;
  --color-warning-bg: #FEF3C7;
  --color-warning-text: #92400E;
  
  /* Error States */
  --color-error: #DC2626;
  --color-error-bg: #FEE2E2;
  --color-error-text: #991B1B;
  
  /* Info States */
  --color-info: #0891B2;
  --color-info-bg: #CFFAFE;
  --color-info-text: #164E63;
}
```

### 2. Interactive Colors (Màu tương tác)
```css
:root {
  /* Interactive States */
  --color-interactive: #2563EB;
  --color-interactive-hover: #1D4ED8;
  --color-interactive-active: #1E40AF;
  --color-interactive-focus: #3B82F6;
  
  /* Focus Indicators */
  --color-focus: #2563EB;
  --color-focus-ring: rgba(37, 99, 235, 0.3);
}
```

### 3. Neutral Colors (Màu trung tính)
```css
:root {
  /* Text Colors */
  --color-text-primary: #111827;
  --color-text-secondary: #6B7280;
  --color-text-tertiary: #9CA3AF;
  --color-text-disabled: #D1D5DB;
  
  /* Background Colors */
  --color-bg-primary: #FFFFFF;
  --color-bg-secondary: #F9FAFB;
  --color-bg-tertiary: #F3F4F6;
  --color-bg-disabled: #F3F4F6;
  
  /* Border Colors */
  --color-border-primary: #E5E7EB;
  --color-border-secondary: #D1D5DB;
  --color-border-tertiary: #9CA3AF;
}
```

## Color Blindness Support

### Các loại color blindness phổ biến
1. **Protanopia** - Mù đỏ (thiếu L-cones)
2. **Deuteranopia** - Mù xanh (thiếu M-cones)
3. **Tritanopia** - Mù xanh dương (thiếu S-cones)
4. **Anomalous Trichromacy** - Cảm nhận màu sắc bất thường

### Giải pháp hỗ trợ
```css
/* Sử dụng patterns bổ sung */
.status-success {
  background: linear-gradient(45deg, #059669 50%, transparent 50%);
  background-size: 10px 10px;
}

/* Tăng độ tương phản */
@media (prefers-contrast: high) {
  :root {
    --color-success: #047857;
    --color-warning: #B45309;
    --color-error: #B91C1C;
    --color-info: #0E7490;
  }
}

/* Sử dụng icon thay thế */
.status-badge::before {
  content: attr(data-icon);
}
```

## Responsive Color System

### Breakpoints và color adjustments
```css
:root {
  /* Mobile First Colors */
  --color-primary: #2563EB;
  
  /* Tablet adjustments */
  @media (min-width: 768px) {
    --color-primary: #1D4ED8;
  }
  
  /* Desktop adjustments */
  @media (min-width: 1024px) {
    --color-primary: #1E40AF;
  }
}
```

## Dark Mode Considerations

### Color inversion principles
```css
@media (prefers-color-scheme: dark) {
  :root {
    /* Invert text colors */
    --color-text-primary: #F9FAFB;
    --color-text-secondary: #D1D5DB;
    --color-text-tertiary: #9CA3AF;
    
    /* Adjust background colors */
    --color-bg-primary: #111827;
    --color-bg-secondary: #1F2937;
    --color-bg-tertiary: #374151;
    
    /* Enhance contrast for dark mode */
    --color-primary: #3B82F6;
    --color-interactive: #60A5FA;
  }
}
```

## Implementation Checklist

### ✅ Contrast Verification
- [ ] Tất cả text có contrast ratio ≥ 4.5:1
- [ ] Text lớn có contrast ratio ≥ 3:1
- [ ] UI components có contrast ratio ≥ 3:1
- [ ] Sử dụng công cụ kiểm tra tự động

### ✅ Color Usage
- [ ] Không dựa vào màu sắc duy nhất để truyền thông tin
- [ ] Có icon/pattern bổ sung cho states
- [ ] Clear focus indicators
- [ ] Consistent hover states

### ✅ Responsive Design
- [ ] Color adjustments cho từng breakpoint
- [ ] Touch targets đủ lớn (≥44px)
- [ ] Clear visual hierarchy

### ✅ Accessibility Features
- [ ] Support cho prefers-reduced-motion
- [ ] Support cho prefers-color-scheme
- [ ] Support cho prefers-contrast
- [ ] Screen reader compatibility

## Testing Tools và Methods

### Automated Testing
```python
def check_color_contrast(color1, color2):
    """Kiểm tra tỷ lệ tương phản"""
    # Implementation sẽ được tạo trong bước tiếp theo
    pass

def validate_accessibility_colors():
    """Kiểm tra toàn bộ hệ thống màu"""
    # Implementation sẽ được tạo trong bước tiếp theo
    pass
```

### Manual Testing Checklist
- [ ] Test với color blindness simulators
- [ ] Test trên các thiết bị khác nhau
- [ ] Test với screen readers
- [ ] Test keyboard navigation
- [ ] Test với zoom 200%

## References
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Color Oracle (Color Blindness Simulator)](https://colororacle.org/)
- [Stark (Accessibility Plugin for Design Tools)](https://www.starklab.com/)