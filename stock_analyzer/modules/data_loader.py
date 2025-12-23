import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Tuple, Optional
import yfinance as yf
from vnstock import Vnstock

def fetch_historical_data(ticker: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """
    Fetches historical stock data for a given ticker using yfinance, with vnstock as a fallback.
    Includes improved error handling for missing data.
    """
    try:
        print(f"📥 Đang lấy dữ liệu lịch sử cho {ticker}...")
        
        suffixes = ['.VN', '.HN', '.HM', '.HA', '']
        for suffix in suffixes:
            yf_ticker = f"{ticker}{suffix}"
            try:
                df = yf.download(yf_ticker, start=start_date, end=end_date, progress=False, auto_adjust=True)
                if not df.empty and len(df) > 0:
                    print(f"✅ Đã lấy {len(df)} điểm dữ liệu cho {ticker} với yfinance (hậu tố '{suffix}').")
                    
                    if isinstance(df.columns, pd.MultiIndex):
                        df.columns = [col[0] for col in df.columns]
                    
                    required_yf_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
                    if all(col in df.columns for col in required_yf_cols):
                        return df[required_yf_cols]
            except Exception as e:
                continue
            
        print(f"⚠️ yfinance không thành công. Đang thử với vnstock...")
        try:
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')
            
            vnstock_instance = Vnstock()
            stock_component = vnstock_instance.stock(symbol=ticker)
            df_vnstock = stock_component.quote.history(start_date_str, end_date_str)
            
            if not df_vnstock.empty:
                print(f"✅ Đã lấy {len(df_vnstock)} điểm dữ liệu cho {ticker} với vnstock.")
                
                df_vnstock.rename(columns={
                    'Mở cửa': 'Open',
                    'Cao nhất': 'High',
                    'Thấp nhất': 'Low',
                    'Đóng cửa': 'Close',
                    'Khối lượng': 'Volume'
                }, inplace=True)
                
                if 'Ngày' in df_vnstock.columns:
                    df_vnstock['Date'] = pd.to_datetime(df_vnstock['Ngày'])
                    df_vnstock = df_vnstock.set_index('Date')
                    df_vnstock.drop(columns=['Ngày'], inplace=True)

                required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
                return df_vnstock[required_cols]
                
        except Exception as e:
            print(f"⚠️ vnstock lỗi: {e}")

        print(f"❌ Không tìm thấy dữ liệu cho {ticker}. Vui lòng kiểm tra mã cổ phiếu.")
        return pd.DataFrame()
    
    except Exception as e:
        print(f"❌ Lỗi khi lấy dữ liệu: {e}")
        return pd.DataFrame()

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses the historical stock data.
    - Handles missing values (if any, though dummy data won't have them).
    - Ensures correct data types.
    """
    if df.empty:
        print("⚠️ Không có dữ liệu để tiền xử lý.")
        return df

    # Ensure column names are standardized to 'Open', 'High', 'Low', 'Close', 'Volume'
    # yfinance with auto_adjust=True typically returns these names directly.
    # vnstock data has its columns explicitly renamed in fetch_historical_data.
    # This step is a safeguard against any unexpected column naming variations.
    df.rename(columns={
        'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume',
        'Open': 'Open', 'High': 'High', 'Low': 'Low', 'Close': 'Close', 'Volume': 'Volume'
    }, inplace=True)


    # yfinance thường trả về các cột này dưới dạng số, nên không cần chuyển đổi lại.
    # Chỉ cần đảm bảo các cột cần thiết tồn tại và loại bỏ các hàng có giá trị NaN.

    required_ohlcv_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    missing_columns = [col for col in required_ohlcv_columns if col not in df.columns]

    if missing_columns:
        print(f"❌ Các cột OHLCV bắt buộc bị thiếu: {missing_columns}")
        return pd.DataFrame()

    try:
        initial_rows = len(df)
        
        invalid_prices = df[(df['Open'] <= 0) | (df['High'] <= 0) | (df['Low'] <= 0) | (df['Close'] <= 0)]
        if not invalid_prices.empty:
            print(f"⚠️ Tìm thấy {len(invalid_prices)} hàng có giá trị giá <= 0. Đang loại bỏ...")
        
        invalid_hl = df[df['High'] < df['Low']]
        if not invalid_hl.empty:
            print(f"⚠️ Tìm thấy {len(invalid_hl)} hàng có giá 'High' < 'Low'. Đang loại bỏ...")
            
        is_valid = (df['Open'] > 0) & (df['High'] > 0) & (df['Low'] > 0) & (df['Close'] > 0) & (df['High'] >= df['Low'])
        df = df[is_valid]
        
        rows_removed = initial_rows - len(df)
        if rows_removed > 0:
            print(f"✓ Đã loại bỏ {rows_removed} hàng không hợp lệ.")

        df.dropna(subset=required_ohlcv_columns, inplace=True)
        if initial_rows > len(df) and rows_removed == 0:
             print(f"✓ Đã loại bỏ {initial_rows - len(df)} hàng chứa giá trị NaN.")

        print("✅ Tiền xử lý dữ liệu hoàn tất.")
        return df
    
    except Exception as e:
        print(f"❌ Lỗi khi tiền xử lý dữ liệu: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    # Example usage
    ticker = "AAA"
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365) # One year of data

    historical_data = fetch_historical_data(ticker, start_date, end_date)
    if not historical_data.empty:
        processed_data = preprocess_data(historical_data)
        print("\nVí dụ về dữ liệu đã xử lý:")
        print(processed_data.head())
