# 🔧 Hướng dẫn Sửa lỗi Deployment lên Streamlit Cloud

## ❌ **Lỗi đã gặp phải:**
```
ModuleNotFoundError: This app has encountered an error. The original error message is redacted to prevent data leaks.
Traceback:
File "/mount/src/stock/stock_analyzer/app.py", line 12, in <module>
    from stock_analyzer.modules.core_analysis import run_analysis
File "/mount/src/stock/stock_analyzer/modules/core_analysis.py", line 14, in <module>
    from stock_analyzer.modules.advanced_analysis import perform_advanced_analysis
File "/mount/src/stock/stock_analyzer/modules/advanced_analysis.py", line 5, in <module>
    from sklearn.ensemble import IsolationForest
```

## ✅ **Đã sửa như thế nào:**

### 1. **Cập nhật requirements.txt**
Đã thêm đầy đủ các dependencies cần thiết:
```txt
# Core Streamlit & Data Science
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.10.0
plotly>=5.14.0

# Financial Data
yfinance>=0.2.28
vnstock>=0.3.0
requests>=2.31.0
python-dateutil>=2.8.2
pytz>=2023.3

# Machine Learning (Light version)
scikit-learn>=1.3.0

# Data Processing
openpyxl>=3.1.0
xlsxwriter>=3.1.0
lxml>=4.9.0

# Web Scraping
beautifulsoup4>=4.12.0

# Financial Technical Analysis
ta>=0.10.2
```

### 2. **Các lỗi thường gặp và cách sửa:**

#### **A. Lỗi thiếu dependencies:**
```bash
# Cách kiểm tra:
pip list | grep scikit-learn

# Nếu không có, thêm vào requirements.txt:
scikit-learn>=1.3.0
```

#### **B. Lỗi import modules:**
```python
# Thêm try-except cho optional imports:
try:
    from sklearn.ensemble import IsolationForest
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("Warning: scikit-learn not available")
```

#### **C. Lỗi version conflicts:**
```txt
# Sử dụng version ranges thay vì exact versions:
pandas>=2.0.0  # Thay vì pandas==2.1.0
numpy>=1.24.0  # Thay vì numpy==1.24.3
```

### 3. **Cách deploy lại sau khi sửa:**

#### **Bước 1: Update code**
```bash
git add .
git commit -m "Fix deployment dependencies"
git push origin main
```

#### **Bước 2: Redeploy trên Streamlit Cloud**
1. Vào Streamlit Cloud dashboard
2. Click "Manage app" 
3. Click "Settings" 
4. Click "Redeploy" 
5. Hoặc push code mới sẽ auto-redeploy

### 4. **Kiểm tra deployment:**

#### **Local test trước khi deploy:**
```bash
# Test locally
streamlit run stock_analyzer/app.py

# Kiểm tra imports
python -c "import sklearn; print('scikit-learn available')"
python -c "import pandas; print('pandas available')"
python -c "import plotly; print('plotly available')"
```

#### **Monitor logs trên cloud:**
1. Streamlit Cloud → Manage app → View logs
2. Tìm các lỗi import hoặc dependencies
3. Fix và redeploy

### 5. **Tối ưu hóa thêm cho deployment:**

#### **A. Lazy loading cho heavy modules:**
```python
# Thay vì import ở đầu file:
# from sklearn.ensemble import IsolationForest

# Import khi cần:
def get_isolation_forest():
    try:
        from sklearn.ensemble import IsolationForest
        return IsolationForest()
    except ImportError:
        return None
```

#### **B. Fallback cho missing dependencies:**
```python
def safe_import(module_name, fallback=None):
    try:
        return __import__(module_name)
    except ImportError:
        return fallback

# Sử dụng:
sklearn = safe_import('sklearn')
if sklearn:
    from sklearn.ensemble import IsolationForest
else:
    IsolationForest = None
```

#### **C. Environment detection:**
```python
import os

IS_CLOUD = os.environ.get('STREAMLIT_CLOUD', False)
IS_LOCAL = not IS_CLOUD

# Conditional imports
if IS_LOCAL:
    # Full imports for local development
    from sklearn.ensemble import IsolationForest
else:
    # Lazy imports for cloud deployment
    pass
```

### 6. **Performance optimizations:**

#### **A. Cache heavy imports:**
```python
import functools

@functools.lru_cache(maxsize=1)
def get_ml_models():
    """Cache ML models to avoid repeated imports"""
    try:
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.preprocessing import StandardScaler
        return RandomForestRegressor, StandardScaler
    except ImportError:
        return None, None
```

#### **B. Reduce memory usage:**
```python
# Thêm vào đầu app.py
import gc
gc.set_debug(gc.DEBUG_LEAK)

# Clear memory sau khi sử dụng
del large_dataframe
gc.collect()
```

### 7. **Monitoring và debugging:**

#### **A. Add health checks:**
```python
def check_dependencies():
    """Check if all required dependencies are available"""
    required_packages = [
        'pandas', 'numpy', 'scikit-learn', 'plotly', 
        'yfinance', 'requests'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    return missing

# Trong main app
missing_deps = check_dependencies()
if missing_deps:
    st.error(f"Missing dependencies: {', '.join(missing_deps)}")
```

#### **B. Error reporting:**
```python
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Log errors
try:
    # Your code here
    pass
except Exception as e:
    logger.error(f"Error occurred: {e}")
    st.error(f"An error occurred: {str(e)}")
```

### 8. **Backup deployment strategy:**

Nếu Streamlit Cloud vẫn gặp vấn đề, có thể deploy lên:

#### **A. Hugging Face Spaces (Free):**
```bash
# 1. Tạo repository trên HF
# 2. Upload code + requirements.txt
# 3. Chọn Streamlit app type
# 4. Deploy tự động
```

#### **B. Render (Free tier):**
```bash
# 1. Connect GitHub repo
# 2. Auto-deploy với build command: pip install -r requirements.txt
# 3. Start command: streamlit run stock_analyzer/app.py
```

### 9. **Final checklist trước deploy:**

- ✅ requirements.txt có đầy đủ dependencies
- ✅ Không có import errors
- ✅ Tested locally thành công
- ✅ Code committed lên GitHub
- ✅ Streamlit Cloud app được cấu hình đúng

## 🎯 **Kết quả mong đợi:**

Sau khi áp dụng các fixes này:
- ✅ Ứng dụng deploy thành công lên Streamlit Cloud
- ✅ Không có ModuleNotFoundError
- ✅ Tất cả tính năng hoạt động bình thường
- ✅ Performance tối ưu cho cloud environment

**Chúc bạn deploy thành công! 🚀**