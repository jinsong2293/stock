from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.metrics import dp
from kivy.core.window import Window
import pandas as pd
import os
import sys

# Add modules path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'stock_analyzer'))

from stock_analyzer.modules.core_analysis import run_analysis
from stock_analyzer.modules.investment_scanner import find_investment_opportunities

STOCK_DATA_PATH = os.path.join(os.path.dirname(__file__), 'stock_analyzer', 'data', 'stocks.csv')

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'home'

        layout = MDBoxLayout(orientation='vertical')

        # Toolbar
        toolbar = MDTopAppBar(title="📈 Phân tích Cổ phiếu")
        toolbar.left_action_items = [["menu", lambda x: self.open_nav()]]
        layout.add_widget(toolbar)

        # Main content
        scroll = MDScrollView()
        content = MDBoxLayout(orientation='vertical', spacing=dp(20), padding=dp(20))

        # Welcome card
        welcome_card = MDCard(
            size_hint=(1, None),
            height=dp(150),
            padding=dp(20),
            elevation=4
        )
        welcome_layout = MDBoxLayout(orientation='vertical')
        welcome_layout.add_widget(MDLabel(
            text="Hệ thống Phân tích Cổ phiếu Thông minh",
            font_style="H5",
            halign="center"
        ))
        welcome_layout.add_widget(MDLabel(
            text="Chọn một mã cổ phiếu để phân tích hoặc quét thị trường",
            halign="center",
            theme_text_color="Secondary"
        ))
        welcome_card.add_widget(welcome_layout)
        content.add_widget(welcome_card)

        # Action buttons
        buttons_layout = MDGridLayout(cols=2, spacing=dp(10), size_hint=(1, None), height=dp(100))

        analyze_btn = MDRaisedButton(
            text="🔍 Phân tích Cổ phiếu",
            size_hint=(1, None),
            height=dp(50)
        )
        analyze_btn.bind(on_release=lambda x: self.go_to_analyze())
        buttons_layout.add_widget(analyze_btn)

        scan_btn = MDRaisedButton(
            text="📊 Quét Thị trường",
            size_hint=(1, None),
            height=dp(50)
        )
        scan_btn.bind(on_release=lambda x: self.go_to_scan())
        buttons_layout.add_widget(scan_btn)

        content.add_widget(buttons_layout)

        scroll.add_widget(content)
        layout.add_widget(scroll)

        self.add_widget(layout)

    def open_nav(self):
        # Placeholder for navigation drawer
        pass

    def go_to_analyze(self):
        self.manager.current = 'analyze'

    def go_to_scan(self):
        self.manager.current = 'scan'

class AnalyzeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'analyze'

        layout = MDBoxLayout(orientation='vertical')

        # Toolbar
        toolbar = MDTopAppBar(title="Phân tích Cổ phiếu")
        toolbar.left_action_items = [["arrow-left", lambda x: self.go_back()]]
        layout.add_widget(toolbar)

        # Content
        scroll = MDScrollView()
        content = MDBoxLayout(orientation='vertical', spacing=dp(20), padding=dp(20))

        # Ticker selection
        ticker_card = MDCard(
            size_hint=(1, None),
            height=dp(100),
            padding=dp(20),
            elevation=4
        )
        ticker_layout = MDBoxLayout(orientation='vertical', spacing=dp(10))
        ticker_layout.add_widget(MDLabel(text="Chọn mã cổ phiếu:", font_style="H6"))

        self.ticker_field = MDTextField(
            hint_text="Ví dụ: VNM, FPT, VIC...",
            helper_text="Nhập mã cổ phiếu cần phân tích"
        )
        ticker_layout.add_widget(self.ticker_field)

        analyze_btn = MDRaisedButton(
            text="🚀 Phân tích",
            size_hint=(1, None),
            height=dp(50)
        )
        analyze_btn.bind(on_release=lambda x: self.run_analysis())
        ticker_layout.add_widget(analyze_btn)

        ticker_card.add_widget(ticker_layout)
        content.add_widget(ticker_card)

        # Results area
        self.results_layout = MDBoxLayout(orientation='vertical', spacing=dp(10))
        content.add_widget(self.results_layout)

        scroll.add_widget(content)
        layout.add_widget(scroll)

        self.add_widget(layout)

    def go_back(self):
        self.manager.current = 'home'

    def run_analysis(self):
        ticker = self.ticker_field.text.upper().strip()
        if not ticker:
            return

        # Clear previous results
        self.results_layout.clear_widgets()

        # Show loading
        loading_label = MDLabel(text="Đang phân tích...", halign="center")
        self.results_layout.add_widget(loading_label)

        # Run analysis (this would be async in real app)
        try:
            results = run_analysis(ticker)
            if results:
                self.display_results(ticker, results)
            else:
                error_label = MDLabel(text="❌ Không thể phân tích cổ phiếu này", theme_text_color="Error")
                self.results_layout.add_widget(error_label)
        except Exception as e:
            error_label = MDLabel(text=f"❌ Lỗi: {str(e)}", theme_text_color="Error")
            self.results_layout.add_widget(error_label)

        # Remove loading
        self.results_layout.remove_widget(loading_label)

    def display_results(self, ticker, results):
        # Simple display of key metrics
        tech_data = results.get("technical_data")
        if tech_data is not None and not tech_data.empty:
            price = tech_data['Close'].iloc[-1]
            rsi = tech_data['RSI'].iloc[-1] if 'RSI' in tech_data.columns else 'N/A'

            result_card = MDCard(
                size_hint=(1, None),
                height=dp(150),
                padding=dp(20),
                elevation=4
            )
            result_layout = MDBoxLayout(orientation='vertical', spacing=dp(10))
            result_layout.add_widget(MDLabel(text=f"📊 Kết quả cho {ticker}", font_style="H6"))

            metrics_layout = MDGridLayout(cols=2, spacing=dp(10))
            metrics_layout.add_widget(MDLabel(text=f"💹 Giá: {price:.2f}"))
            metrics_layout.add_widget(MDLabel(text=f"🔴 RSI: {rsi:.2f}" if rsi != 'N/A' else f"🔴 RSI: {rsi}"))

            result_layout.add_widget(metrics_layout)
            result_card.add_widget(result_layout)
            self.results_layout.add_widget(result_card)

class ScanScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'scan'

        layout = MDBoxLayout(orientation='vertical')

        # Toolbar
        toolbar = MDTopAppBar(title="Quét Thị trường")
        toolbar.left_action_items = [["arrow-left", lambda x: self.go_back()]]
        layout.add_widget(toolbar)

        # Content
        scroll = MDScrollView()
        content = MDBoxLayout(orientation='vertical', spacing=dp(20), padding=dp(20))

        # Scan button
        scan_card = MDCard(
            size_hint=(1, None),
            height=dp(100),
            padding=dp(20),
            elevation=4
        )
        scan_layout = MDBoxLayout(orientation='vertical', spacing=dp(10))
        scan_layout.add_widget(MDLabel(text="🔍 Tìm kiếm cơ hội đầu tư", font_style="H6"))

        scan_btn = MDRaisedButton(
            text="🚀 Bắt đầu quét",
            size_hint=(1, None),
            height=dp(50)
        )
        scan_btn.bind(on_release=lambda x: self.run_scan())
        scan_layout.add_widget(scan_btn)

        scan_card.add_widget(scan_layout)
        content.add_widget(scan_card)

        # Results area
        self.results_layout = MDBoxLayout(orientation='vertical', spacing=dp(10))
        content.add_widget(self.results_layout)

        scroll.add_widget(content)
        layout.add_widget(scroll)

        self.add_widget(layout)

    def go_back(self):
        self.manager.current = 'home'

    def run_scan(self):
        # Clear previous results
        self.results_layout.clear_widgets()

        # Show loading
        loading_label = MDLabel(text="Đang quét thị trường...", halign="center")
        self.results_layout.add_widget(loading_label)

        try:
            # Load tickers
            df = pd.read_csv(STOCK_DATA_PATH)
            tickers = df['Ticker'].tolist()[:10]  # Limit for demo

            opportunities = find_investment_opportunities(tickers, 0.0015, 0.0005)
            if opportunities:
                self.display_scan_results(opportunities)
            else:
                no_results = MDLabel(text="❌ Không tìm thấy cơ hội nào", halign="center")
                self.results_layout.add_widget(no_results)
        except Exception as e:
            error_label = MDLabel(text=f"❌ Lỗi: {str(e)}", theme_text_color="Error")
            self.results_layout.add_widget(error_label)

        # Remove loading
        self.results_layout.remove_widget(loading_label)

    def display_scan_results(self, opportunities):
        buy_ops = opportunities.get('buy', [])
        sell_ops = opportunities.get('sell', [])
        hold_ops = opportunities.get('hold', [])

        if buy_ops:
            buy_card = MDCard(
                size_hint=(1, None),
                height=dp(100),
                padding=dp(20),
                elevation=4
            )
            buy_layout = MDBoxLayout(orientation='vertical')
            buy_layout.add_widget(MDLabel(text="🟢 Cơ hội MUA", font_style="H6"))
            for op in buy_ops[:3]:  # Show first 3
                buy_layout.add_widget(MDLabel(text=f"• {op['ticker']} - Độ tin cậy: {op.get('confidence', 0):.0f}%"))
            buy_card.add_widget(buy_layout)
            self.results_layout.add_widget(buy_card)

class StockAnalyzerApp(MDApp):
    def build(self):
        # Set window size for development (comment out for mobile)
        Window.size = (400, 700)

        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        sm = MDScreenManager()
        sm.add_widget(HomeScreen())
        sm.add_widget(AnalyzeScreen())
        sm.add_widget(ScanScreen())

        return sm

if __name__ == '__main__':
    StockAnalyzerApp().run()