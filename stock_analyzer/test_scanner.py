import pandas as pd
from .modules.investment_scanner import find_investment_opportunities
from .app import load_stock_list, STOCK_DATA_PATH

def run_scanner_test():
    """
    Tests the investment scanner functionality by running it on a list of stocks.
    """
    print("Starting investment scanner test...")
    
    # Load the list of tickers
    all_tickers = load_stock_list(STOCK_DATA_PATH)
    
    if not all_tickers:
        print("Could not load stock list. Aborting test.")
        return
        
    # Run the investment scanner
    investment_opportunities = find_investment_opportunities(all_tickers)
    
    if investment_opportunities:
        print("\n--- Potential Investment Opportunities ---")
        for opportunity in investment_opportunities:
            print(f"Ticker: {opportunity['ticker']}")
            print(f"  Entry Point: {opportunity['entry_point']}")
            print(f"  Take Profit: {opportunity['take_profit']}")
            print(f"  Stop Loss: {opportunity['stop_loss']}")
            print("-" * 20)
    else:
        print("\nNo investment opportunities found at this time.")
        
if __name__ == "__main__":
    run_scanner_test()
