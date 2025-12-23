import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy.stats import linregress
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('advanced_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def _get_trend_from_slope(slope, threshold=0.001):
    """Helper to interpret slope as a trend."""
    if slope > threshold:
        return "Upward"
    elif slope < -threshold:
        return "Downward"
    else:
        return "Sideways"

def predict_trends(data):
    """
    Predicts trends using linear regression on historical closing prices.
    """
    print("Performing trend prediction...")

    trend_results = {
        "short_term_trend": "Neutral",
        "short_term_confidence": "N/A",
        "medium_term_trend": "Neutral",
        "medium_term_confidence": "N/A",
        "price_forecast_next_5_days": {}
    }

    if data.empty or len(data) < 30: # Need at least 30 days for medium-term trend
        print("Not enough data for trend prediction.")
        return trend_results

    # Short-term trend (e.g., last 10 days)
    short_term_data = data['Close'].tail(10)
    if len(short_term_data) >= 2:
        x_short = np.arange(len(short_term_data))
        slope_short, intercept_short, r_value_short, p_value_short, std_err_short = linregress(x_short, short_term_data)
        trend_results["short_term_trend"] = _get_trend_from_slope(slope_short)
        trend_results["short_term_confidence"] = f"{r_value_short**2:.2f}" # R-squared as confidence

        # Simple linear extrapolation for next 5 days based on short-term trend
        last_x = len(short_term_data) - 1
        future_dates = [data.index[-1] + timedelta(days=i+1) for i in range(5)]
        future_prices = {}
        for i in range(5):
            predicted_price = intercept_short + slope_short * (last_x + i + 1)
            future_prices[future_dates[i].strftime('%Y-%m-%d')] = f"{max(0.01, predicted_price):.2f}" # Ensure price is not negative
        trend_results["price_forecast_next_5_days"] = future_prices

    # Medium-term trend (e.g., last 30 days)
    medium_term_data = data['Close'].tail(30)
    if len(medium_term_data) >= 2:
        x_medium = np.arange(len(medium_term_data))
        slope_medium, intercept_medium, r_value_medium, p_value_medium, std_err_medium = linregress(x_medium, medium_term_data)
        trend_results["medium_term_trend"] = _get_trend_from_slope(slope_medium)
        trend_results["medium_term_confidence"] = f"{r_value_medium**2:.2f}" # R-squared as confidence

    print("Trend prediction complete.")
    return trend_results

def detect_anomalies(data, window=30, z_score_threshold=3):
    """
    Detects anomalies in historical stock data using the Z-score method.
    Anomalies are flagged if their Z-score for Close price or Volume exceeds a threshold.
    """
    logger.info("Detecting anomalies using Z-score method...")
    print("Detecting anomalies...")

    anomalies = []
    if data.empty or len(data) < window:
        logger.warning("Not enough data for anomaly detection.")
        print("Not enough data for anomaly detection.")
        return {"anomalies_detected": "No", "details": []}

    # Calculate rolling mean and standard deviation for Close price and Volume
    data['Close_Mean'] = data['Close'].rolling(window=window).mean()
    data['Close_Std'] = data['Close'].rolling(window=window).std()
    data['Volume_Mean'] = data['Volume'].rolling(window=window).mean()
    data['Volume_Std'] = data['Volume'].rolling(window=window).std()

    # Calculate Z-scores
    data['Close_ZScore'] = (data['Close'] - data['Close_Mean']) / data['Close_Std']
    data['Volume_ZScore'] = (data['Volume'] - data['Volume_Mean']) / data['Volume_Std']

    # Identify anomalies
    # Anomalies are where the absolute Z-score is greater than the threshold
    close_anomalies = data[np.abs(data['Close_ZScore']) > z_score_threshold]
    volume_anomalies = data[np.abs(data['Volume_ZScore']) > z_score_threshold]

    # Combine and format anomalies
    for date, row in close_anomalies.iterrows():
        anomalies.append({
            "date": date.strftime('%Y-%m-%d'),
            "type": f"Bất thường giá (Z-score: {row['Close_ZScore']:.2f})"
        })
    for date, row in volume_anomalies.iterrows():
        anomalies.append({
            "date": date.strftime('%Y-%m-%d'),
            "type": f"Bất thường khối lượng (Z-score: {row['Volume_ZScore']:.2f})"
        })
    
    # Remove duplicates if a date is both a price and volume anomaly
    unique_anomalies = []
    seen_dates = set()
    for anomaly in anomalies:
        if anomaly['date'] not in seen_dates:
            unique_anomalies.append(anomaly)
            seen_dates.add(anomaly['date'])
    
    anomaly_results = {
        "anomalies_detected": "Yes" if unique_anomalies else "No",
        "details": unique_anomalies
    }
    logger.info("Anomaly detection using Z-score method complete.")
    print("Anomaly detection complete.")
    return anomaly_results

def detect_anomalies_isolation_forest(data, contamination=0.05):
    """
    Detects anomalies in historical stock data using Isolation Forest.
    """
    logger.info("Detecting anomalies using Isolation Forest...")
    
    if data.empty or len(data) < 10:
        logger.warning("Not enough data for Isolation Forest anomaly detection.")
        return {"anomalies_detected": "No", "details": []}
    
    # Prepare data for Isolation Forest
    features = data[['Close', 'Volume']].dropna()
    if len(features) < 10:
        logger.warning("Not enough data for Isolation Forest anomaly detection.")
        return {"anomalies_detected": "No", "details": []}
    
    # Standardize the data
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # Train Isolation Forest model
    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(features_scaled)
    
    # Predict anomalies
    anomalies = model.predict(features_scaled)
    
    # Format anomalies
    anomaly_details = []
    for i, is_anomaly in enumerate(anomalies):
        if is_anomaly == -1:
            date = features.index[i]
            anomaly_details.append({
                "date": date.strftime('%Y-%m-%d'),
                "type": "Bất thường Isolation Forest"
            })
    
    anomaly_results = {
        "anomalies_detected": "Yes" if anomaly_details else "No",
        "details": anomaly_details
    }
    
    logger.info("Anomaly detection using Isolation Forest complete.")
    return anomaly_results

def detect_anomalies_dbscan(data, eps=0.5, min_samples=5):
    """
    Detects anomalies in historical stock data using DBSCAN.
    """
    logger.info("Detecting anomalies using DBSCAN...")
    
    if data.empty or len(data) < 10:
        logger.warning("Not enough data for DBSCAN anomaly detection.")
        return {"anomalies_detected": "No", "details": []}
    
    # Prepare data for DBSCAN
    features = data[['Close', 'Volume']].dropna()
    if len(features) < 10:
        logger.warning("Not enough data for DBSCAN anomaly detection.")
        return {"anomalies_detected": "No", "details": []}
    
    # Standardize the data
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # Train DBSCAN model
    model = DBSCAN(eps=eps, min_samples=min_samples)
    model.fit(features_scaled)
    
    # Predict anomalies
    labels = model.labels_
    
    # Format anomalies
    anomaly_details = []
    for i, label in enumerate(labels):
        if label == -1:
            date = features.index[i]
            anomaly_details.append({
                "date": date.strftime('%Y-%m-%d'),
                "type": "Bất thường DBSCAN"
            })
    
    anomaly_results = {
        "anomalies_detected": "Yes" if anomaly_details else "No",
        "details": anomaly_details
    }
    
    logger.info("Anomaly detection using DBSCAN complete.")
    return anomaly_results

def perform_advanced_analysis(df):
    """
    Performs advanced analysis and trend prediction.
    """
    if df.empty:
        logger.warning("No data for advanced analysis.")
        print("No data for advanced analysis.")
        return {}, {}, {}

    trend_predictions = predict_trends(df)
    anomaly_detections_zscore = detect_anomalies(df)
    anomaly_detections_isolation = detect_anomalies_isolation_forest(df)
    anomaly_detections_dbscan = detect_anomalies_dbscan(df)

    return trend_predictions, anomaly_detections_zscore, anomaly_detections_isolation, anomaly_detections_dbscan

if __name__ == "__main__":
    # Example usage with dummy data
    dates = pd.date_range(start=datetime.now() - timedelta(days=100), end=datetime.now(), freq='D')
    dummy_prices = 100 + np.cumsum(np.random.randn(len(dates)))
    dummy_volume = np.random.randint(100000, 5000000, len(dates))

    dummy_df = pd.DataFrame({
        'Date': dates,
        'Open': dummy_prices - np.random.rand(len(dates)) * 2,
        'High': dummy_prices + np.random.rand(len(dates)) * 2,
        'Low': dummy_prices - np.random.rand(len(dates)) * 3,
        'Close': dummy_prices,
        'Volume': dummy_volume
    })
    dummy_df.set_index('Date', inplace=True)

    trends, anomalies = perform_advanced_analysis(dummy_df.copy())
    print("\nAdvanced Analysis Results:")
    print("Trends:", trends)
    print("Anomalies:", anomalies)
