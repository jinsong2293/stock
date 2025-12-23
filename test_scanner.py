#!/usr/bin/env python3
"""
Test script for Comprehensive Investment Scanner
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from stock_analyzer.modules.comprehensive_investment_scanner import ComprehensiveInvestmentScanner, ScanCriteria

def test_scanner():
    """Test the scanner functionality"""
    print("🧪 Testing Comprehensive Investment Scanner...")
    
    try:
        # Initialize scanner
        scanner = ComprehensiveInvestmentScanner()
        print("✅ Scanner initialized successfully")
        
        # Create scan criteria
        criteria = ScanCriteria(
            exchanges=['HOSE'],
            limit=10,
            sort_by='overall_score',
            sort_order='desc'
        )
        print(f"✅ Created scan criteria: {criteria}")
        
        # Perform market scan
        print("🔍 Starting market scan...")
        results = scanner.scan_market_opportunities(criteria)
        
        print(f"📊 Scan completed!")
        print(f"   Results type: {type(results)}")
        print(f"   Has error: {'error' in results}")
        
        if 'error' in results:
            print(f"❌ Error: {results['error']}")
            return False
        
        # Check results
        scan_metadata = results.get('scan_metadata', {})
        print(f"   Scan ID: {scan_metadata.get('scan_id', 'N/A')}")
        print(f"   Total stocks found: {scan_metadata.get('total_stocks_found', 0)}")
        print(f"   Stocks analyzed: {scan_metadata.get('stocks_analyzed', 0)}")
        print(f"   Final results: {scan_metadata.get('final_results', 0)}")
        
        # Check scan summary
        scan_summary = results.get('scan_summary', {})
        print(f"   Summary total stocks: {scan_summary.get('total_stocks', 0)}")
        
        # Check results list
        stock_results = results.get('results', [])
        print(f"   Actual results count: {len(stock_results)}")
        
        if stock_results:
            print("🏆 Top 3 results:")
            for i, result in enumerate(stock_results[:3]):
                if hasattr(result, 'symbol'):
                    print(f"   {i+1}. {result.symbol} - {result.recommendation} - Score: {result.overall_score:.1f}")
                else:
                    print(f"   {i+1}. {result.get('symbol', 'N/A')} - {result.get('recommendation', 'N/A')} - Score: {result.get('overall_score', 0):.1f}")
        else:
            print("❌ No results found!")
            
        return len(stock_results) > 0
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_scanner()
    print(f"\n{'✅ Scanner test PASSED' if success else '❌ Scanner test FAILED'}")