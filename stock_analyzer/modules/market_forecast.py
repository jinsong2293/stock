"""
Market Forecast System - Dự báo xu hướng thị trường 2 ngày tới
Sử dụng ensemble learning với ARIMA, Linear Regression và LSTM

Author: Roo - Architect Mode
Version: 1.0.0
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# ARIMA
from pmdarima import auto_arima

# Machine Learning
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

# Deep Learning
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.optimizers import Adam
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False

# Technical Analysis
from stock_analyzer.modules.technical_analysis import calculate_rsi, calculate_macd, calculate_bollinger_bands

class MarketForecastSystem:
    """Hệ thống dự báo thị trường 2 ngày tới"""
    
    def __init__(self):
        self.arima_model = None
        self.linear_model = None
        self.rf_model = None
        self.lstm_model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        
        # Ensemble weights
        self.weights = {
            'arima': 0.3,
            'linear': 0.2,
            'rf': 0.3,
            'lstm': 0.2 if TENSORFLOW_AVAILABLE else 0.0
        }
    
    def prepare_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Chuẩn bị features cho mô hình dự báo"""
        df = data.copy()
        
        # Technical indicators
        df['RSI'] = calculate_rsi(df, window=14)
        df['MACD'], df['MACD_Signal'], df['MACD_Hist'] = calculate_macd(df)
        df['BB_Upper'], df['BB_Middle'], df['BB_Lower'] = calculate_bollinger_bands(df)
        
        # Price features
        df['Price_Change'] = df['Close'].pct_change()
        df['Price_Change_2'] = df['Close'].pct_change(2)
        df['Price_Change_5'] = df['Close'].pct_change(5)
        
        # Moving averages
        df['MA_5'] = df['Close'].rolling(window=5).mean()
        df['MA_10'] = df['Close'].rolling(window=10).mean()
        df['MA_20'] = df['Close'].rolling(window=20).mean()
        
        # Volume features
        df['Volume_MA'] = df['Volume'].rolling(window=10).mean()
        df['Volume_Ratio'] = df['Volume'] / df['Volume_MA']
        
        # Bollinger Bands features
        df['BB_Position'] = (df['Close'] - df['BB_Lower']) / (df['BB_Upper'] - df['BB_Lower'])
        df['BB_Width'] = (df['BB_Upper'] - df['BB_Lower']) / df['BB_Middle']
        
        # MACD features
        df['MACD_Position'] = df['MACD'] - df['MACD_Signal']
        
        # RSI features
        df['RSI_Position'] = (df['RSI'] - 30) / 40  # Normalize to 0-1 (30-70 range)
        
        return df
    
    def create_sequences(self, data: np.ndarray, seq_length: int = 10) -> Tuple[np.ndarray, np.ndarray]:
        """Tạo sequences cho LSTM"""
        X, y = [], []
        for i in range(seq_length, len(data)):
            X.append(data[i-seq_length:i])
            y.append(data[i])
        return np.array(X), np.array(y)
    
    def train_arima_model(self, data: pd.DataFrame) -> None:
        """Huấn luyện mô hình ARIMA"""
        try:
            # Use log returns for better stationarity
            log_returns = np.log(data['Close']).diff().dropna()
            
            self.arima_model = auto_arima(
                log_returns,
                start_p=1, start_q=1,
                max_p=3, max_q=3,
                seasonal=False,
                stepwise=True,
                suppress_warnings=True,
                error_action='ignore'
            )
            print("✅ ARIMA model trained successfully")
        except Exception as e:
            print(f"❌ ARIMA training failed: {e}")
            self.arima_model = None
    
    def train_linear_model(self, data: pd.DataFrame) -> None:
        """Huấn luyện mô hình Linear Regression"""
        try:
            # Features for linear model
            feature_cols = [
                'RSI', 'MACD', 'MACD_Signal', 'BB_Position', 'BB_Width',
                'Price_Change', 'Price_Change_2', 'MA_5', 'MA_10', 'MA_20',
                'Volume_Ratio', 'MACD_Position', 'RSI_Position'
            ]
            
            # Remove rows with NaN
            clean_data = data.dropna(subset=feature_cols + ['Close'])
            
            if len(clean_data) < 50:
                print("❌ Not enough data for linear model")
                return
            
            X = clean_data[feature_cols]
            y = clean_data['Close']
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train model
            self.linear_model = LinearRegression()
            self.linear_model.fit(X_scaled, y)
            print("✅ Linear model trained successfully")
            
        except Exception as e:
            print(f"❌ Linear model training failed: {e}")
    
    def train_random_forest(self, data: pd.DataFrame) -> None:
        """Huấn luyện mô hình Random Forest"""
        try:
            # Features for RF model
            feature_cols = [
                'RSI', 'MACD', 'MACD_Signal', 'BB_Position', 'BB_Width',
                'Price_Change', 'Price_Change_2', 'MA_5', 'MA_10', 'MA_20',
                'Volume_Ratio', 'MACD_Position', 'RSI_Position'
            ]
            
            # Remove rows with NaN
            clean_data = data.dropna(subset=feature_cols + ['Close'])
            
            if len(clean_data) < 50:
                print("❌ Not enough data for Random Forest")
                return
            
            X = clean_data[feature_cols]
            y = clean_data['Close']
            
            # Scale features
            X_scaled = self.scaler.transform(X)
            
            # Train model
            self.rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.rf_model.fit(X_scaled, y)
            print("✅ Random Forest model trained successfully")
            
        except Exception as e:
            print(f"❌ Random Forest training failed: {e}")
    
    def train_lstm_model(self, data: pd.DataFrame) -> None:
        """Huấn luyện mô hình LSTM"""
        if not TENSORFLOW_AVAILABLE:
            print("❌ TensorFlow not available, skipping LSTM")
            return
        
        try:
            # Features for LSTM
            feature_cols = [
                'Close', 'Volume', 'RSI', 'MACD', 'BB_Position', 'BB_Width',
                'Price_Change', 'MA_5', 'MA_10', 'Volume_Ratio'
            ]
            
            # Remove rows with NaN
            clean_data = data.dropna(subset=feature_cols)
            
            if len(clean_data) < 100:
                print("❌ Not enough data for LSTM")
                return
            
            # Prepare data
            features = clean_data[feature_cols].values
            features_scaled = self.scaler.fit_transform(features)
            
            # Create sequences
            seq_length = 10
            X, y = self.create_sequences(features_scaled, seq_length)
            
            if len(X) < 10:
                print("❌ Not enough sequences for LSTM")
                return
            
            # Build LSTM model
            self.lstm_model = Sequential([
                LSTM(50, return_sequences=True, input_shape=(seq_length, len(feature_cols))),
                Dropout(0.2),
                LSTM(50, return_sequences=False),
                Dropout(0.2),
                Dense(25),
                Dense(1)
            ])
            
            self.lstm_model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
            
            # Train model
            self.lstm_model.fit(X, y, epochs=50, batch_size=32, verbose=0)
            print("✅ LSTM model trained successfully")
            
        except Exception as e:
            print(f"❌ LSTM training failed: {e}")
    
    def train(self, data: pd.DataFrame) -> None:
        """Huấn luyện toàn bộ hệ thống"""
        print("🚀 Starting Market Forecast System training...")
        
        # Prepare features
        df = self.prepare_features(data)
        
        # Train individual models
        self.train_arima_model(df)
        self.train_linear_model(df)
        self.train_random_forest(df)
        self.train_lstm_model(df)
        
        self.is_trained = True
        print("✅ Market Forecast System training completed")
    
    def predict_next_2_days(self, data: pd.DataFrame) -> Dict[str, float]:
        """Dự báo giá 2 ngày tới"""
        if not self.is_trained:
            raise ValueError("Model not trained yet")
        
        # Prepare features
        df = self.prepare_features(data)
        
        predictions = {}
        
        # ARIMA prediction
        if self.arima_model:
            try:
                # Predict log returns
                arima_forecast = self.arima_model.predict(n_periods=2)
                # Convert to price
                last_price = df['Close'].iloc[-1]
                arima_price_1 = last_price * np.exp(arima_forecast[0])
                arima_price_2 = arima_price_1 * np.exp(arima_forecast[1])
                predictions['arima'] = {'day_1': arima_price_1, 'day_2': arima_price_2}
            except:
                predictions['arima'] = {'day_1': last_price, 'day_2': last_price}
        else:
            last_price = df['Close'].iloc[-1]
            predictions['arima'] = {'day_1': last_price, 'day_2': last_price}
        
        # Linear model prediction
        if self.linear_model:
            try:
                feature_cols = [
                    'RSI', 'MACD', 'MACD_Signal', 'BB_Position', 'BB_Width',
                    'Price_Change', 'Price_Change_2', 'MA_5', 'MA_10', 'MA_20',
                    'Volume_Ratio', 'MACD_Position', 'RSI_Position'
                ]
                
                # Use last available features
                last_features = df[feature_cols].iloc[-1:].fillna(0)
                last_features_scaled = self.scaler.transform(last_features)
                
                linear_pred = self.linear_model.predict(last_features_scaled)[0]
                predictions['linear'] = {'day_1': linear_pred, 'day_2': linear_pred * 1.001}
            except:
                predictions['linear'] = {'day_1': last_price, 'day_2': last_price}
        else:
            predictions['linear'] = {'day_1': last_price, 'day_2': last_price}
        
        # Random Forest prediction
        if self.rf_model:
            try:
                feature_cols = [
                    'RSI', 'MACD', 'MACD_Signal', 'BB_Position', 'BB_Width',
                    'Price_Change', 'Price_Change_2', 'MA_5', 'MA_10', 'MA_20',
                    'Volume_Ratio', 'MACD_Position', 'RSI_Position'
                ]
                
                last_features = df[feature_cols].iloc[-1:].fillna(0)
                last_features_scaled = self.scaler.transform(last_features)
                
                rf_pred = self.rf_model.predict(last_features_scaled)[0]
                predictions['rf'] = {'day_1': rf_pred, 'day_2': rf_pred * 1.001}
            except:
                predictions['rf'] = {'day_1': last_price, 'day_2': last_price}
        else:
            predictions['rf'] = {'day_1': last_price, 'day_2': last_price}
        
        # LSTM prediction
        if self.lstm_model and TENSORFLOW_AVAILABLE:
            try:
                feature_cols = [
                    'Close', 'Volume', 'RSI', 'MACD', 'BB_Position', 'BB_Width',
                    'Price_Change', 'MA_5', 'MA_10', 'Volume_Ratio'
                ]
                
                last_features = df[feature_cols].iloc[-10:].fillna(0).values
                last_features_scaled = self.scaler.transform(last_features)
                
                lstm_pred = self.lstm_model.predict(last_features_scaled.reshape(1, 10, -1))[0][0]
                predictions['lstm'] = {'day_1': lstm_pred, 'day_2': lstm_pred * 1.001}
            except:
                predictions['lstm'] = {'day_1': last_price, 'day_2': last_price}
        else:
            predictions['lstm'] = {'day_1': last_price, 'day_2': last_price}
        
        return predictions
    
    def calculate_ensemble_prediction(self, predictions: Dict[str, Dict]) -> Dict[str, float]:
        """Tính toán dự báo ensemble"""
        day_1_pred = 0
        day_2_pred = 0
        total_weight = 0
        
        for model, preds in predictions.items():
            weight = self.weights.get(model, 0)
            if weight > 0:
                day_1_pred += preds['day_1'] * weight
                day_2_pred += preds['day_2'] * weight
                total_weight += weight
        
        if total_weight > 0:
            day_1_pred /= total_weight
            day_2_pred /= total_weight
        
        return {
            'day_1': day_1_pred,
            'day_2': day_2_pred,
            'confidence': total_weight / sum(self.weights.values())
        }

class MarketScoreSystem:
    """Hệ thống tính điểm thị trường"""
    
    def __init__(self):
        self.score_weights = {
            'technical': 0.4,
            'trend': 0.3,
            'volume': 0.2,
            'sentiment': 0.1
        }
    
    def calculate_technical_score(self, data: pd.DataFrame) -> float:
        """Tính điểm kỹ thuật"""
        if data.empty or len(data) < 20:
            return 50
        
        latest = data.iloc[-1]
        
        # RSI score (0-100)
        rsi_score = 50
        if 'RSI' in data.columns and not pd.isna(latest['RSI']):
            rsi = latest['RSI']
            if rsi < 30:  # Oversold
                rsi_score = 80
            elif rsi > 70:  # Overbought
                rsi_score = 20
            else:
                rsi_score = 50 + (rsi - 50)  # Linear mapping 30-70 to 20-80
        
        # MACD score
        macd_score = 50
        if 'MACD' in data.columns and 'MACD_Signal' in data.columns:
            macd = latest['MACD']
            signal = latest['MACD_Signal']
            if macd > signal:  # Bullish
                macd_score = 70
            else:  # Bearish
                macd_score = 30
        
        # Bollinger Bands score
        bb_score = 50
        if 'BB_Position' in data.columns:
            bb_pos = latest['BB_Position']
            if 0.3 <= bb_pos <= 0.7:  # Middle zone
                bb_score = 60
            elif bb_pos < 0.3:  # Lower zone
                bb_score = 80
            else:  # Upper zone
                bb_score = 20
        
        return (rsi_score + macd_score + bb_score) / 3
    
    def calculate_trend_score(self, data: pd.DataFrame) -> float:
        """Tính điểm xu hướng"""
        if data.empty or len(data) < 20:
            return 50
        
        # Price trend (20-day moving average)
        ma_20 = data['Close'].rolling(window=20).mean().iloc[-1]
        current_price = data['Close'].iloc[-1]
        
        if current_price > ma_20:
            trend_score = 70
        else:
            trend_score = 30
        
        # Price momentum
        if len(data) >= 5:
            momentum = (data['Close'].iloc[-1] - data['Close'].iloc[-5]) / data['Close'].iloc[-5]
            momentum_score = 50 + (momentum * 100)
            trend_score = (trend_score + momentum_score) / 2
        
        return max(0, min(100, trend_score))
    
    def calculate_volume_score(self, data: pd.DataFrame) -> float:
        """Tính điểm khối lượng"""
        if data.empty or len(data) < 20:
            return 50
        
        latest = data.iloc[-1]
        
        # Volume ratio
        volume_score = 50
        if 'Volume_Ratio' in data.columns:
            vol_ratio = latest['Volume_Ratio']
            if vol_ratio > 1.5:
                volume_score = 80
            elif vol_ratio > 1.0:
                volume_score = 60
            elif vol_ratio > 0.5:
                volume_score = 40
            else:
                volume_score = 20
        
        return volume_score
    
    def calculate_sentiment_score(self, data: pd.DataFrame) -> float:
        """Tính điểm tâm lý (dựa trên price action)"""
        if data.empty or len(data) < 5:
            return 50
        
        # Price action sentiment
        recent_changes = data['Close'].pct_change().tail(5).dropna()
        positive_days = sum(1 for x in recent_changes if x > 0)
        negative_days = sum(1 for x in recent_changes if x < 0)
        
        if positive_days > negative_days:
            sentiment_score = 70
        elif negative_days > positive_days:
            sentiment_score = 30
        else:
            sentiment_score = 50
        
        # Recent price performance
        if len(data) >= 10:
            perf_10 = (data['Close'].iloc[-1] - data['Close'].iloc[-10]) / data['Close'].iloc[-10]
            perf_score = 50 + (perf_10 * 100)
            sentiment_score = (sentiment_score + perf_score) / 2
        
        return max(0, min(100, sentiment_score))
    
    def calculate_overall_score(self, data: pd.DataFrame) -> Dict[str, float]:
        """Tính điểm tổng thể"""
        tech_score = self.calculate_technical_score(data)
        trend_score = self.calculate_trend_score(data)
        volume_score = self.calculate_volume_score(data)
        sentiment_score = self.calculate_sentiment_score(data)
        
        overall_score = (
            tech_score * self.score_weights['technical'] +
            trend_score * self.score_weights['trend'] +
            volume_score * self.score_weights['volume'] +
            sentiment_score * self.score_weights['sentiment']
        )
        
        return {
            'overall': max(0, min(100, overall_score)),
            'technical': tech_score,
            'trend': trend_score,
            'volume': volume_score,
            'sentiment': sentiment_score
        }

def run_market_forecast(data: pd.DataFrame) -> Dict[str, Any]:
    """Chạy toàn bộ hệ thống dự báo thị trường"""
    if data.empty or len(data) < 100:
        return {
            'error': 'Not enough data for market forecast',
            'forecast': None,
            'score': None
        }
    
    # Initialize systems
    forecast_system = MarketForecastSystem()
    score_system = MarketScoreSystem()
    
    # Train forecast system
    forecast_system.train(data)
    
    # Get predictions
    predictions = forecast_system.predict_next_2_days(data)
    ensemble_pred = forecast_system.calculate_ensemble_prediction(predictions)
    
    # Calculate scores
    scores = score_system.calculate_overall_score(data)
    
    # Calculate percentage changes
    current_price = data['Close'].iloc[-1]
    day_1_change = ((ensemble_pred['day_1'] - current_price) / current_price) * 100
    day_2_change = ((ensemble_pred['day_2'] - current_price) / current_price) * 100
    
    # Determine trend
    if day_1_change > 1.0:
        trend = "Strong Up"
    elif day_1_change > 0.5:
        trend = "Up"
    elif day_1_change > -0.5:
        trend = "Sideways"
    elif day_1_change > -1.0:
        trend = "Down"
    else:
        trend = "Strong Down"
    
    return {
        'forecast': {
            'current_price': current_price,
            'day_1_price': ensemble_pred['day_1'],
            'day_1_change': day_1_change,
            'day_2_price': ensemble_pred['day_2'],
            'day_2_change': day_2_change,
            'trend': trend,
            'confidence': ensemble_pred['confidence'],
            'individual_predictions': predictions
        },
        'score': scores,
        'success': True
    }

if __name__ == "__main__":
    # Example usage
    print("Market Forecast System initialized")
    print("Use run_market_forecast(data) to get predictions")
