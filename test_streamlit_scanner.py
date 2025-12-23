#!/usr/bin/env python3
"""
Test Streamlit Scanner Integration
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

# Import required modules
from stock_analyzer.modules.comprehensive_investment_scanner import ComprehensiveInvestmentScanner, ScanCriteria
import pandas as pd

def test_scanner_display():
    """Test scanner and display logic"""
    print("🧪 Testing Scanner Display Logic...")
    
    try:
        # Initialize scanner
        scanner = ComprehensiveInvestmentScanner()
        print("✅ Scanner initialized")
        
        # Create criteria and scan
        criteria = ScanCriteria(exchanges=['HOSE'], limit=5)
        results = scanner.scan_market_opportunities(criteria)
        
        print(f"📊 Scan results: {len(results.get('results', []))} stocks")
        
        # Test display logic (similar to Streamlit)
        scanner_results = results.get('results', [])
        
        if not scanner_results:
            print("❌ No results to display")
            return False
        
        print(f"✅ Found {len(scanner_results)} results")
        
        # Simulate display logic
        display_data = []
        
        for i, result in enumerate(scanner_results):
            try:
                print(f"Processing result {i+1}: {type(result)}")
                
                # Handle both dict and StockAnalysisResult objects
                if hasattr(result, 'symbol'):  # StockAnalysisResult object
                    print(f"  - Object: {result.symbol}")
                    display_data.append({
                        'Mã': result.symbol,
                        'Công ty': result.company_name,
                        'Ngành': result.sector,
                        'Giá hiện tại': f"{result.current_price:,.0f} VND",
                        'Thay đổi %': f"{result.price_change_pct:+.1f}%",
                        'Khuyến nghị': result.recommendation,
                        'Điểm tổng': f"{result.overall_score:.1f}",
                        'Tiềm năng': f"{result.upside_potential:+.1f}%",
                        'Rủi ro': result.risk_level,
                        'P/E': f"{result.pe_ratio:.1f}"
                    })
                else:  # Dictionary
                    print(f"  - Dict: {result.get('symbol', 'N/A')}")
                    display_data.append({
                        'Mã': result.get('symbol', f'STOCK_{i+1}'),
                        'Công ty': result.get('company_name', f'Công ty {i+1}'),
                        'Ngành': result.get('sector', 'Khác'),
                        'Giá hiện tại': f"{result.get('current_price', 50000):,.0f} VND",
                        'Thay đổi %': f"{result.get('price_change_pct', 0):+.1f}%",
                        'Khuyến nghị': result.get('recommendation', 'NẮM GIỮ'),
                        'Điểm tổng': f"{result.get('overall_score', 50):.1f}",
                        'Tiềm năng': f"{result.get('upside_potential', 0):+.1f}%",
                        'Rủi ro': result.get('risk_level', 'TRUNG BÌNH'),
                        'P/E': f"{result.get('pe_ratio', 15):.1f}"
                    })
            except Exception as e:
                print(f"❌ Error processing result {i+1}: {e}")
                continue
        
        if not display_data:
            print("❌ No display data created")
            return False
        
        # Create DataFrame
        df = pd.DataFrame(display_data)
        print(f"✅ Created DataFrame with {len(df)} rows")
        print("\n📊 Preview of results:")
        print(df.head(3).to_string(index=False))
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_scanner_display()
    print(f"\n{'✅ Display test PASSED' if success else '❌ Display test FAILED'}")