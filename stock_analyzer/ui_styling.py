"""
Modern UI Styling - Hệ thống styling hiện đại cho Stock Analyzer
Bao gồm typography, animations, và responsive design
"""

import streamlit as st
from stock_analyzer.ui_theme_manager import theme_manager

def apply_modern_styling():
    """Áp dụng styling hiện đại cho ứng dụng"""
    
    theme = theme_manager.get_current_theme()
    
    st.markdown(f"""
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    
    <style>
        :root {{
            {theme_manager.get_theme_colors_css()}

            /* Enhanced Typography Scale */
            --text-xs: 0.75rem;
            --text-sm: 0.875rem;
            --text-base: 1rem;
            --text-lg: 1.125rem;
            --text-xl: 1.25rem;
            --text-2xl: 1.5rem;
            --text-3xl: 1.875rem;
            --text-4xl: 2.25rem;

            /* Improved Line Heights */
            --leading-tight: 1.25;
            --leading-normal: 1.5;
            --leading-relaxed: 1.625;

            /* Consistent Spacing Scale */
            --space-1: 0.25rem;
            --space-2: 0.5rem;
            --space-3: 0.75rem;
            --space-4: 1rem;
            --space-5: 1.25rem;
            --space-6: 1.5rem;
            --space-8: 2rem;
            --space-10: 2.5rem;
            --space-12: 3rem;
            --space-16: 4rem;

            /* Border Radius Scale */
            --radius-sm: 0.25rem;
            --radius-md: 0.375rem;
            --radius-lg: 0.5rem;
            --radius-xl: 0.75rem;
            --radius-2xl: 1rem;
            --radius-full: 9999px;

            /* Shadow Scale */
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }}
        
        * {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        
        /* Global Styles */
        .main {{
            background: linear-gradient(135deg, var(--bg_primary) 0%, var(--bg_secondary) 100%);
            min-height: 100vh;
            transition: all 0.3s ease;
        }}
        
        .stApp {{
            background: var(--bg_primary);
            color: var(--text_primary);
        }}
        
        /* Header Styles */
        .modern-header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary_dark) 100%);
            color: var(--text_inverse);
            padding: var(--space-8) var(--space-6);
            border-radius: var(--radius-2xl);
            margin-bottom: var(--space-8);
            text-align: center;
            box-shadow: var(--shadow-xl);
            position: relative;
            overflow: hidden;
        }}
        
        .modern-header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            opacity: 0.1;
        }}
        
        .modern-header h1 {{
            font-size: var(--text-4xl);
            font-weight: 800;
            margin: 0;
            line-height: var(--leading-tight);
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            position: relative;
            z-index: 1;
        }}

        .modern-header p {{
            font-size: var(--text-lg);
            font-weight: 400;
            margin: var(--space-2) 0 0 0;
            line-height: var(--leading-relaxed);
            opacity: 0.9;
            position: relative;
            z-index: 1;
        }}
        
        /* Cards */
        .modern-card {{
            background: var(--bg_primary);
            border: 1px solid var(--border_light);
            border-radius: var(--radius-xl);
            padding: var(--space-6);
            margin-bottom: var(--space-6);
            box-shadow: var(--shadow-md);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}
        
        .modern-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(to bottom, var(--primary), var(--accent));
            transform: scaleY(0);
            transition: transform 0.3s ease;
        }}
        
        .modern-card:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
            border-color: var(--primary);
        }}
        
        .modern-card:hover::before {{
            transform: scaleY(1);
        }}
        
        /* Metrics */
        .modern-metric {{
            background: var(--bg_secondary);
            border: 1px solid var(--border_light);
            border-radius: var(--radius-lg);
            padding: var(--space-6);
            text-align: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            box-shadow: var(--shadow-sm);
        }}
        
        .modern-metric::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(to right, var(--primary), var(--accent));
        }}
        
        .modern-metric:hover {{
            transform: translateY(-1px);
            box-shadow: var(--shadow-md);
            border-color: var(--primary);
        }}
        
        /* Buttons */
        .modern-button {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary_dark) 100%);
            color: var(--text_inverse);
            border: none;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }}
        
        .modern-button::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }}
        
        .modern-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
        }}
        
        .modern-button:hover::before {{
            left: 100%;
        }}
        
        /* Tabs */
        .modern-tabs {{
            background: var(--bg_primary);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .stTabs [data-baseweb="tab-list"] {{
            background: var(--bg_secondary);
            gap: 8px;
            padding: 8px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background: transparent;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            color: var(--text_secondary);
            border: 1px solid transparent;
            transition: all 0.3s ease;
        }}
        
        .stTabs [data-baseweb="tab"]:hover {{
            background: var(--bg_accent);
            color: var(--primary);
            border-color: var(--primary);
        }}
        
        .stTabs [aria-selected="true"] {{
            background: var(--primary);
            color: var(--text_inverse);
            border-color: var(--primary);
        }}
        
        /* DataFrame */
        .modern-dataframe {{
            background: var(--bg_primary);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border: 1px solid var(--border_light);
        }}
        
        .modern-dataframe table {{
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
        }}
        
        .modern-dataframe th {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary_dark) 100%);
            color: var(--text_inverse);
            font-weight: 600;
            padding: 1rem;
            border: none;
        }}
        
        .modern-dataframe td {{
            background: var(--bg_primary);
            color: var(--text_primary);
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border_light);
        }}
        
        .modern-dataframe tr:hover td {{
            background: var(--bg_accent);
        }}
        
        /* Sidebar */
        .sidebar-modern {{
            background: var(--bg_secondary);
            border-right: 1px solid var(--border_light);
        }}
        
        .sidebar-header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary_dark) 100%);
            color: var(--text_inverse);
            padding: 1.5rem;
            margin: -1rem -1rem 1.5rem -1rem;
            border-radius: 0 0 16px 16px;
            text-align: center;
            font-weight: 700;
            font-size: 1.2rem;
        }}
        
        /* Theme Toggle */
        .theme-toggle {{
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            background: var(--bg_primary);
            border: 1px solid var(--border_light);
            border-radius: 50px;
            padding: 0.5rem 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-weight: 500;
            color: var(--text_primary);
        }}
        
        .theme-toggle:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }}
        
        /* Status Badges */
        .status-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border-radius: 50px;
            font-size: 0.875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .status-success {{
            background: var(--success);
            color: white;
        }}
        
        .status-warning {{
            background: var(--warning);
            color: white;
        }}
        
        .status-error {{
            background: var(--error);
            color: white;
        }}
        
        .status-info {{
            background: var(--info);
            color: white;
        }}
        
        /* Animations */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        @keyframes fadeInLeft {{
            from {{
                opacity: 0;
                transform: translateX(-30px);
            }}
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}
        
        .animate-fade-in-up {{
            animation: fadeInUp 0.6s ease-out;
        }}
        
        .animate-fade-in-left {{
            animation: fadeInLeft 0.6s ease-out;
        }}
        
        /* Accessibility Improvements */
        .sr-only {{
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border: 0;
        }}

        /* Focus states for accessibility */
        .modern-card:focus-within,
        .modern-metric:focus-within,
        .modern-button:focus {{
            outline: 2px solid var(--primary);
            outline-offset: 2px;
        }}

        /* High contrast mode support */
        @media (prefers-contrast: high) {{
            .modern-card {{
                border-width: 2px;
            }}
            .modern-metric {{
                border-width: 2px;
            }}
        }}

        /* Reduced motion support */
        @media (prefers-reduced-motion: reduce) {{
            .modern-card,
            .modern-metric,
            .modern-button {{
                transition: none;
            }}
            .animate-fade-in-up,
            .animate-fade-in-left {{
                animation: none;
            }}
        }}

        /* Responsive Design */
        @media (max-width: 768px) {{
            .modern-header {{
                padding: var(--space-6) var(--space-4);
                margin-bottom: var(--space-6);
            }}

            .modern-header h1 {{
                font-size: var(--text-3xl);
            }}

            .modern-card {{
                padding: var(--space-4);
                margin-bottom: var(--space-4);
            }}

            .modern-metric {{
                padding: var(--space-4);
            }}

            .theme-toggle {{
                top: var(--space-3);
                right: var(--space-3);
                padding: var(--space-2) var(--space-3);
                font-size: var(--text-sm);
            }}
        }}

        @media (max-width: 480px) {{
            .modern-header h1 {{
                font-size: var(--text-2xl);
            }}

            .modern-card,
            .modern-metric {{
                padding: var(--space-3);
            }}

            .theme-toggle {{
                padding: var(--space-1) var(--space-2);
                font-size: var(--text-xs);
            }}
        }}
        
        /* Loading States */
        .loading-spinner {{
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid var(--border_light);
            border-radius: 50%;
            border-top-color: var(--primary);
            animation: spin 1s ease-in-out infinite;
        }}

        .loading-skeleton {{
            background: linear-gradient(90deg, var(--bg_secondary) 25%, var(--bg_tertiary) 50%, var(--bg_secondary) 75%);
            background-size: 200% 100%;
            animation: loading-shimmer 1.5s infinite;
            border-radius: var(--radius-md);
        }}

        .skeleton-card {{
            height: 120px;
            margin-bottom: var(--space-4);
        }}

        .skeleton-text {{
            height: var(--text-base);
            margin-bottom: var(--space-2);
        }}

        .skeleton-text:last-child {{
            width: 60%;
        }}

        .skeleton-metric {{
            height: 80px;
            margin-bottom: var(--space-3);
        }}

        @keyframes loading-shimmer {{
            0% {{
                background-position: -200% 0;
            }}
            100% {{
                background-position: 200% 0;
            }}
        }}
        
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: var(--bg_secondary);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: var(--border_medium);
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: var(--border_dark);
        }}
    </style>
    """, unsafe_allow_html=True)

def create_modern_header(title: str, subtitle: str = ""):
    """Tạo header hiện đại"""
    st.markdown(f"""
    <div class="modern-header">
        <h1>{title}</h1>
        {f'<p>{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def create_modern_card(content: str, title: str = ""):
    """Tạo card hiện đại"""
    title_html = f'<h3 style="color: var(--text_primary); margin-bottom: 1rem; font-weight: 600;">{title}</h3>' if title else ''
    st.markdown(f"""
    <div class="modern-card animate-fade-in-up">
        {title_html}
        {content}
    </div>
    """, unsafe_allow_html=True)

def create_status_badge(text: str, status_type: str = "info"):
    """Tạo status badge"""
    st.markdown(f"""
    <span class="status-badge status-{status_type}">
        {text}
    </span>
    """, unsafe_allow_html=True)

def create_theme_toggle():
    """Tạo nút chuyển đổi theme"""
    theme = theme_manager
    emoji = theme.get_theme_status_emoji()
    text = theme.get_theme_status_text()
    
    # JavaScript để toggle theme
    js_code = f"""
    <script>
    function toggleTheme() {{
        fetch('/theme/toggle', {{method: 'POST'}})
        .then(response => response.json())
        .then(data => {{
            if (data.theme === 'dark') {{
                document.documentElement.style.setProperty('--bg-primary', '#0F172A');
                document.documentElement.style.setProperty('--bg-secondary', '#1E293B');
                // Thêm các biến CSS khác cho dark mode
            }} else {{
                document.documentElement.style.setProperty('--bg-primary', '#FFFFFF');
                document.documentElement.style.setProperty('--bg-secondary', '#F8FAFC');
                // Thêm các biến CSS khác cho light mode
            }}
            location.reload();
        }})
        .catch(error => console.log('Error:', error));
    }}
    </script>
    """
    
    st.markdown(js_code, unsafe_allow_html=True)
    
    # Button để toggle theme
    if st.button(f"{emoji} {text}", key="theme_toggle", help="Chuyển đổi Light/Dark Mode"):
        theme.toggle_theme()

def get_chart_colors() -> list:
    """Lấy màu sắc cho biểu đồ"""
    theme = theme_manager.get_current_theme()
    return [
        theme["chart_1"],
        theme["chart_2"], 
        theme["chart_3"],
        theme["chart_4"],
        theme["chart_5"],
        theme["chart_6"],
    ]