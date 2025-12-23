import os
import pandas as pd
from stock_analyzer.app import load_stock_list, run_analysis

# Define the path to the stocks.csv file
STOCK_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'stocks.csv')

def get_user_stock_input(valid_tickers):
    """Prompts the user for a stock ticker and validates it."""
    while True:
        ticker = input("Enter a stock ticker (e.g., AAA) or 'exit' to quit: ").upper()
        if ticker == 'EXIT':
            return None
        if ticker in valid_tickers:
            return ticker
        else:
            print(f"Invalid ticker: {ticker}. Please enter a valid ticker from the list.")

def display_results_cli(ticker, results):
    """Displays the analysis results in the CLI."""
    if not results:
        return

    print("\n--- Comprehensive Stock Analysis Report ---")
    print(f"Ticker: {ticker}")

    # 1. Technical Analysis Summary
    print("\n1. Technical Analysis Summary:")
    tech_data = results["technical_data"]
    if not tech_data.empty:
        print(f"   - Latest Close Price: {tech_data['Close'].iloc[-1]:.2f}")
        print(f"   - Latest RSI: {tech_data['RSI'].iloc[-1]:.2f}")
        print(f"   - Latest MACD: {tech_data['MACD'].iloc[-1]:.2f}, Signal: {tech_data['MACD_Signal'].iloc[-1]:.2f}")
        print(f"   - Bollinger Bands: Upper={tech_data['BB_Upper'].iloc[-1]:.2f}, Middle={tech_data['BB_Middle'].iloc[-1]:.2f}, Lower={tech_data['BB_Lower'].iloc[-1]:.2f}")
        print("   - Last 5 Technical Data Points:")
        print(tech_data[['Close', 'RSI', 'MACD', 'MACD_Signal', 'BB_Upper', 'BB_Middle', 'BB_Lower']].tail().to_string())
    else:
        print("   No technical data available.")

    # 2. Market Sentiment Analysis Summary
    print("\n2. Market Sentiment Analysis Summary:")
    sentiment_results = results["sentiment_results"]
    for key, value in sentiment_results.items():
        print(f"   - {key.replace('_', ' ').title()}: {value}")

    # 3. Advanced Analysis & Trend Prediction Summary
    print("\n3. Advanced Analysis & Trend Prediction Summary:")
    trend_predictions = results["trend_predictions"]
    anomaly_detections = results["anomaly_detections"]
    print(f"   - Short-term Trend: {trend_predictions['short_term_trend']} (Confidence: {trend_predictions['short_term_confidence']})")
    print(f"   - Medium-term Trend: {trend_predictions['medium_term_trend']} (Confidence: {trend_predictions['medium_term_confidence']})")
    print(f"   - Price Forecast (Next 5 Days): {trend_predictions['price_forecast_next_5_days']}")
    print(f"   - Anomalies Detected: {anomaly_detections['anomalies_detected']}")
    if anomaly_detections['details']:
        for anomaly in anomaly_detections['details']:
            print(f"     - Date: {anomaly['date']}, Type: {anomaly['type']}")

    # 4. Financial Report Analysis Summary
    print("\n4. Financial Report Analysis Summary:")
    financial_data = results["financial_data"]
    financial_health = results["financial_health"]
    print(f"   - Overall Financial Health: {financial_health['overall_assessment']}")
    print("   - Key Financial Ratios:")
    for key, value in financial_data.items():
        if "million" in key or "ratio" in key or "eps" in key or "percent" in key:
            print(f"     - {key.replace('_', ' ').title()}: {value}")
    print("   - Financial Health Comments:")
    for comment in financial_health['comments']:
        print(f"     - {comment}")

    # Trading Recommendation
    print("\n--- Trading Recommendation ---")
    final_recommendation = results["final_recommendation"]
    print(f"Action: {final_recommendation['action']}")
    print(f"Optimal Entry Point: {final_recommendation['entry_point']}")
    print(f"Optimal Exit Point: {final_recommendation['exit_point']}")
    print(f"Take-Profit Level: {final_recommendation['take_profit']}")
    print(f"Stop-Loss Level: {final_recommendation['stop_loss']}")
    print("\nReasoning:")
    for reason in final_recommendation['reasoning']:
        print(f"- {reason}")

    print(f"\nAnalysis for {ticker} completed.")

def main_cli():
    print("Initializing Stock Analysis System (CLI Mode)...")
    valid_tickers = load_stock_list(STOCK_DATA_PATH)

    if not valid_tickers:
        print("Could not load valid stock tickers. Exiting.")
        return

    print(f"Loaded {len(valid_tickers)} valid stock tickers.")

    while True:
        selected_ticker = get_user_stock_input(valid_tickers)
        if selected_ticker is None:
            print("Exiting Stock Analysis System. Goodbye!")
            break

        results = run_analysis(selected_ticker)
        if results:
            display_results_cli(selected_ticker, results)

if __name__ == "__main__":
    # You can choose to run the CLI or the Streamlit app
    # To run Streamlit, use: streamlit run stock_analyzer/app.py
    main_cli()
