# Hệ thống Dự báo Xu hướng Chứng khoán 2 ngày tới

## Tổng quan Kiến trúc

Hệ thống dự báo xu hướng chứng khoán được thiết kế theo kiến trúc modular, tích hợp các module hiện có và mở rộng chức năng để đáp ứng yêu cầu dự báo chính xác 2 ngày tới.

## Thành phần Chính

### 1. Data Layer (Lớp Dữ liệu)
- **Enhanced Data Loader**: Mở rộng module hiện có để thu thập dữ liệu từ nhiều nguồn
- **News Collector**: Module mới thu thập tin tức từ các nguồn tin tức tài chính
- **Macro Economic Data**: Tích hợp với module macro_economic_analyzer hiện có
- **Technical Data**: Sử dụng module technical_analysis hiện có

### 2. Feature Engineering Layer (Lớp Tạo Đặc trưng)
- **Technical Features**: 
  - Moving Averages (MA): 5, 10, 20, 50 ngày
  - RSI (Relative Strength Index): 14 ngày
  - MACD (Moving Average Convergence Divergence): 12, 26, 9
  - Bollinger Bands: 20 ngày, 2 standard deviation
  - Volume indicators: OBV, AD Line, Volume ratios
- **Macro Economic Features**: 
  - Fed Funds Rate, Treasury yields
  - CPI, PPI inflation indicators
  - GDP growth, unemployment rate
  - VIX volatility index
  - Dollar Index
- **Sentiment Features**:
  - News sentiment analysis
  - Social media sentiment
  - Market sentiment indicators

### 3. Model Layer (Lớp Mô hình)
- **Ensemble Model System**: Tích hợp và mở rộng MarketForecastSystem hiện có
  - ARIMA: Time series forecasting
  - XGBoost: Gradient boosting cho regression
  - LSTM: Deep learning cho sequence prediction
  - Prophet: Facebook's time series forecasting
- **Model Training Pipeline**: 
  - Cross-validation
  - Hyperparameter tuning
  - Feature selection

### 4. Prediction Layer (Lớp Dự báo)
- **Ensemble Predictor**: Kết hợp dự báo từ các mô hình
- **Confidence Calculator**: Tính confidence score dựa trên:
  - Model agreement
  - Historical accuracy
  - Market volatility
- **Direction Classifier**: Xác định xu hướng up/down

### 5. Output Layer (Lớp Kết quả)
- **JSON Formatter**: Định dạng kết quả theo yêu cầu
- **Visualization**: Charts và graphs
- **API Interface**: RESTful API cho kết quả

## Chi tiết Các Module

### Enhanced Stock Forecast System
```python
class EnhancedStockForecastSystem:
    """Hệ thống dự báo cải tiến với tin tức và kinh tế vĩ mô"""
    
    def __init__(self):
        self.data_loader = EnhancedDataLoader()
        self.feature_engineer = AdvancedFeatureEngineer()
        self.news_analyzer = NewsSentimentAnalyzer()
        self.macro_analyzer = macro_economic_analyzer
        self.ensemble_models = EnsembleModelSystem()
        self.confidence_calculator = ConfidenceCalculator()
    
    def predict_next_2_days(self, symbol: str) -> Dict[str, Any]:
        """Dự báo 2 ngày tới với đầy đủ thông tin"""
        # 1. Load data (30 days historical)
        historical_data = self.data_loader.get_historical_data(symbol, days=30)
        
        # 2. Get latest news
        news_data = self.news_analyzer.get_recent_news(symbol, days=7)
        
        # 3. Get macro economic data
        macro_data = self.macro_analyzer.analyze_macro_economic_factors()
        
        # 4. Engineer features
        features = self.feature_engineer.create_features(
            historical_data, news_data, macro_data
        )
        
        # 5. Make predictions
        predictions = self.ensemble_models.predict(features)
        
        # 6. Calculate confidence
        confidence = self.confidence_calculator.calculate(predictions, features)
        
        # 7. Format output
        return self.format_output(predictions, confidence)
```

### Advanced Feature Engineer
```python
class AdvancedFeatureEngineer:
    """Tạo đặc trưng nâng cao từ nhiều nguồn dữ liệu"""
    
    def create_features(self, price_data, news_data, macro_data):
        """Tạo features từ tất cả nguồn dữ liệu"""
        features = {}
        
        # Technical features
        features.update(self.create_technical_features(price_data))
        
        # Macro features
        features.update(self.create_macro_features(macro_data))
        
        # News sentiment features
        features.update(self.create_sentiment_features(news_data))
        
        # Combined features
        features.update(self.create_combined_features(features))
        
        return features
```

### News Sentiment Analyzer
```python
class NewsSentimentAnalyzer:
    """Phân tích sentiment từ tin tức"""
    
    def __init__(self):
        self.sentiment_model = self.load_sentiment_model()
        self.news_sources = [
            'reuters.com', 'bloomberg.com', 'cnbc.com', 
            'marketwatch.com', 'yahoo_finance'
        ]
    
    def get_recent_news(self, symbol, days=7):
        """Thu thập tin tức gần đây"""
        # Implementation for news collection
        pass
    
    def analyze_sentiment(self, news_text):
        """Phân tích sentiment của tin tức"""
        # Implementation for sentiment analysis
        pass
```

### Ensemble Model System
```python
class EnsembleModelSystem:
    """Hệ thống mô hình ensemble mở rộng"""
    
    def __init__(self):
        self.models = {
            'arima': ARIMAModel(),
            'xgboost': XGBoostModel(),
            'lstm': LSTMModel(),
            'prophet': ProphetModel()
        }
        self.weights = {
            'arima': 0.2,
            'xgboost': 0.3,
            'lstm': 0.3,
            'prophet': 0.2
        }
    
    def predict(self, features):
        """Dự báo từ ensemble models"""
        predictions = {}
        for name, model in self.models.items():
            predictions[name] = model.predict(features)
        
        return self.combine_predictions(predictions)
```

## Định dạng Kết quả JSON

```json
{
  "forecast_date": "2025-12-24",
  "symbol": "AAPL",
  "predictions": [
    {
      "date": "2025-12-24",
      "direction": "up",
      "predicted_change_points": 2.45,
      "confidence_score": 0.78,
      "predicted_price": 175.50,
      "current_price": 173.05
    },
    {
      "date": "2025-12-25", 
      "direction": "up",
      "predicted_change_points": 1.23,
      "confidence_score": 0.72,
      "predicted_price": 176.73,
      "current_price": 173.05
    }
  ],
  "ensemble_details": {
    "model_predictions": {
      "arima": {"day1": 174.80, "day2": 176.20},
      "xgboost": {"day1": 175.20, "day2": 176.80},
      "lstm": {"day1": 175.50, "day2": 177.00},
      "prophet": {"day1": 175.10, "day2": 176.40}
    },
    "agreement_score": 0.85
  },
  "feature_importance": {
    "rsi": 0.15,
    "macd": 0.12,
    "volume_ratio": 0.10,
    "news_sentiment": 0.08,
    "vix": 0.06
  },
  "market_context": {
    "macro_score": 65.2,
    "technical_score": 72.8,
    "sentiment_score": 68.5,
    "overall_score": 68.8
  }
}
```

## Ưu điểm của Kiến trúc

1. **Modular Design**: Dễ bảo trì và mở rộng
2. **Multi-source Data**: Tích hợp dữ liệu từ nhiều nguồn
3. **Ensemble Learning**: Kết hợp nhiều mô hình để tăng độ chính xác
4. **Real-time Processing**: Có thể xử lý dữ liệu real-time
5. **Scalability**: Có thể mở rộng cho nhiều symbols
6. **Interpretability**: Cung cấp thông tin về feature importance và model agreement

## Triển khai

1. **Phase 1**: Tích hợp các module hiện có
2. **Phase 2**: Phát triển module tin tức và sentiment
3. **Phase 3**: Xây dựng hệ thống ensemble mở rộng
4. **Phase 4**: Tạo giao diện và API
5. **Phase 5**: Testing và validation

Kiến trúc này tận dụng tối đa các module hiện có trong dự án đồng thời mở rộng khả năng để đáp ứng yêu cầu dự báo chính xác 2 ngày tới.