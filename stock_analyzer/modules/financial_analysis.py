import random
import pandas as pd
import yfinance as yf

def get_real_financial_data(ticker):
    """
    Fetches real financial data for a given ticker using yfinance.
    """
    print(f"Đang lấy dữ liệu tài chính thực tế cho {ticker}...")
    try:
        if not ticker.endswith('.VN'):
            yf_ticker = f"{ticker}.VN"
        else:
            yf_ticker = ticker

        stock = yf.Ticker(yf_ticker)
        info = stock.info

        # Extract key financial metrics
        # Some fields might not be available for all tickers, handle gracefully
        revenue = info.get('totalRevenue', None) # in millions
        net_income = info.get('netIncomeToCommon', None) # in millions
        total_assets = info.get('totalAssets', None) # in millions
        total_equity = info.get('totalStockholderEquity', None) # in millions
        shares_outstanding = info.get('sharesOutstanding', None) # in millions

        # Calculate financial ratios
        eps = info.get('trailingEps', None)
        pe_ratio = info.get('trailingPE', None)
        pb_ratio = info.get('priceToBook', None) # priceToBook can be None
        roe = info.get('returnOnEquity') # Get value first
        roa = info.get('returnOnAssets') # Get value first
        debt_to_equity = info.get('debtToEquity') # Get value first

        financial_data = {
            "revenue_million": revenue / 1_000_000 if revenue is not None else None,
            "net_income_million": net_income / 1_000_000 if net_income is not None else None,
            "total_assets_million": total_assets / 1_000_000 if total_assets is not None else None,
            "total_equity_million": total_equity / 1_000_000 if total_equity is not None else None,
            "shares_outstanding_million": shares_outstanding / 1_000_000 if shares_outstanding is not None else None,
            "eps": eps,
            "pe_ratio": pe_ratio,
            "pb_ratio": pb_ratio,
            "roe_percent": roe * 100 if roe is not None else None,
            "roa_percent": roa * 100 if roa is not None else None,
            "debt_to_equity_ratio": debt_to_equity / 100 if debt_to_equity is not None else None # Convert percentage to ratio
        }
        print(f"Đã lấy dữ liệu tài chính thực tế cho {ticker}.")
        return financial_data
    except Exception as e:
        print(f"Lỗi khi lấy dữ liệu tài chính cho {ticker}: {e}")
        # Fallback to dummy data if real data fetching fails
        return get_dummy_financial_data_fallback(ticker)

def get_dummy_financial_data_fallback(ticker):
    """Generates dummy financial data as a fallback."""
    print(f"Không thể lấy dữ liệu tài chính thực tế. Tạo dữ liệu giả cho {ticker}...")
    revenue = random.uniform(1000, 10000) # in millions
    net_income = random.uniform(50, 1000) # in millions
    total_assets = random.uniform(5000, 50000) # in millions
    total_equity = random.uniform(2000, 20000) # in millions
    shares_outstanding = random.randint(100, 1000) # in millions

    eps = net_income / shares_outstanding
    pe_ratio = random.uniform(10, 30)
    pb_ratio = random.uniform(1, 5)
    roe = (net_income / total_equity) * 100
    roa = (net_income / total_assets) * 100
    debt_to_equity = random.uniform(0.1, 2.0)

    financial_data = {
        "revenue_million": revenue,
        "net_income_million": net_income,
        "total_assets_million": total_assets,
        "total_equity_million": total_equity,
        "shares_outstanding_million": shares_outstanding,
        "eps": eps,
        "pe_ratio": pe_ratio,
        "pb_ratio": pb_ratio,
        "roe_percent": roe,
        "roa_percent": roa,
        "debt_to_equity_ratio": debt_to_equity
    }
    return financial_data

def analyze_financial_health(financial_data):
    """
    Analyzes the financial health of a company based on its financial data.
    """
    print("Đang phân tích sức khỏe tài chính...")
    health_score = 0
    comments = []

    # Use numerical values directly, handling None
    pe = financial_data.get("pe_ratio")
    pb = financial_data.get("pb_ratio")
    roe = financial_data.get("roe_percent")
    roa = financial_data.get("roa_percent")
    d_e = financial_data.get("debt_to_equity_ratio")

    if pe is not None:
        if pe < 15:
            health_score += 1
            comments.append("Tỷ lệ P/E cho thấy khả năng bị định giá thấp hoặc thu nhập ổn định.")
        elif pe > 25:
            health_score -= 1
            comments.append("Tỷ lệ P/E cao có thể cho thấy bị định giá quá cao hoặc kỳ vọng tăng trưởng cao.")
        else:
            comments.append("Tỷ lệ P/E nằm trong phạm vi hợp lý.")
    else:
        comments.append("Không có dữ liệu P/E để đánh giá.")

    if pb is not None:
        if pb < 2:
            health_score += 1
            comments.append("Tỷ lệ P/B cho thấy giá trị tốt so với giá trị sổ sách.")
        elif pb > 4:
            health_score -= 1
            comments.append("Tỷ lệ P/B cao có thể cho thấy bị định giá quá cao.")
        else:
            comments.append("Tỷ lệ P/B nằm trong phạm vi hợp lý.")
    else:
        comments.append("Không có dữ liệu P/B để đánh giá.")

    if roe is not None:
        if roe > 15:
            health_score += 1
            comments.append("ROE mạnh cho thấy việc sử dụng vốn chủ sở hữu hiệu quả.")
        elif roe < 5:
            health_score -= 1
            comments.append("ROE thấp cho thấy việc sử dụng vốn chủ sở hữu không hiệu quả.")
        else:
            comments.append("ROE ở mức vừa phải.")
    else:
        comments.append("Không có dữ liệu ROE để đánh giá.")

    if roa is not None:
        if roa > 5:
            health_score += 1
            comments.append("ROA tốt cho thấy quản lý tài sản hiệu quả.")
        elif roa < 2:
            health_score -= 1
            comments.append("ROA thấp cho thấy quản lý tài sản không hiệu quả.")
        else:
            comments.append("ROA ở mức vừa phải.")
    else:
        comments.append("Không có dữ liệu ROA để đánh giá.")

    if d_e is not None:
        if d_e < 1:
            health_score += 1
            comments.append("Tỷ lệ Nợ/Vốn chủ sở hữu thấp cho thấy đòn bẩy tài chính lành mạnh.")
        elif d_e > 1.5:
            health_score -= 1
            comments.append("Tỷ lệ Nợ/Vốn chủ sở hữu cao cho thấy rủi ro tài chính cao hơn.")
        else:
            comments.append("Tỷ lệ Nợ/Vốn chủ sở hữu ở mức vừa phải.")
    else:
        comments.append("Không có dữ liệu Tỷ lệ Nợ/Vốn chủ sở hữu để đánh giá.")

    financial_health_summary = {
        "health_score": health_score,
        "comments": comments,
        "overall_assessment": "Mạnh" if health_score >= 3 else ("Trung bình" if health_score >= 0 else "Yếu")
    }
    print("Phân tích sức khỏe tài chính hoàn tất.")
    return financial_health_summary

def perform_financial_analysis(ticker):
    """
    Performs comprehensive financial analysis for a given ticker.
    """
    financial_data = get_real_financial_data(ticker)
    financial_health = analyze_financial_health(financial_data)
    return financial_data, financial_health

if __name__ == "__main__":
    # Example usage
    ticker = "AAA"
    financial_data, financial_health = perform_financial_analysis(ticker)
    print("\nDữ liệu Tài chính:")
    for key, value in financial_data.items():
        print(f"- {key.replace('_', ' ').title()}: {value}")
    print("\nTóm tắt Sức khỏe Tài chính:")
    for key, value in financial_health.items():
        if isinstance(value, list):
            print(f"- {key.replace('_', ' ').title()}:")
            for item in value:
                print(f"  - {item}")
        else:
            print(f"- {key.replace('_', ' ').title()}: {value}")
