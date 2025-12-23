# 🚀 Hướng dẫn Triển khai Hệ thống Phân tích Chứng khoán Việt Nam

## 📋 Tổng quan

Để triển khai ứng dụng phân tích chứng khoán để có thể truy cập từ nhiều thiết bị, có nhiều phương pháp khác nhau. Dưới đây là các cách triển khai phổ biến, từ miễn phí đến trả phí.

## 🆓 Phương pháp Miễn phí

### 1. **Streamlit Cloud** (Khuyến nghị)

**Ưu điểm:**
- ✅ Hoàn toàn miễn phí
- ✅ Tự động deploy từ GitHub
- ✅ Tự động cập nhật khi push code
- ✅ SSL miễn phí
- ✅ Support tốt cho Streamlit

**Cách triển khai:**

#### Bước 1: Chuẩn bị repository
```bash
# Clone code vào GitHub repository
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/stock-analyzer.git
git push -u origin main
```

#### Bước 2: Deploy lên Streamlit Cloud
1. Truy cập [share.streamlit.io](https://share.streamlit.io)
2. Đăng nhập bằng GitHub account
3. Click "New app"
4. Chọn repository và branch
5. Main file path: `stock_analyzer/app.py`
6. Click "Deploy"

#### Bướy 3: Cấu hình
Tạo file `requirements.txt`:
```
streamlit==1.28.1
pandas==2.1.3
plotly==5.17.0
yfinance==0.2.28
scikit-learn==1.3.2
numpy==1.24.3
ta-lib
```

**URL truy cập:** `https://your-app-name.streamlit.app`

---

### 2. **Ngrok** (Tạm thời - Development)

**Ưu điểm:**
- ✅ Setup nhanh trong 5 phút
- ✅ Không cần server riêng
- ✅ Có thể truy cập từ bất kỳ đâu

**Nhược điểm:**
- ❌ Phiên bản miễn phí có giới hạn
- ❌ URL thay đổi mỗi lần restart

**Cách triển khai:**

```bash
# Cài đặt ngrok
pip install ngrok

# Chạy ứng dụng
streamlit run stock_analyzer/app.py --server.port 8501 --server.address 0.0.0.0

# Mở terminal mới và chạy ngrok
ngrok http 8501
```

---

## 💰 Phương pháp Trả phí

### 3. **Heroku** (Dễ sử dụng)

**Ưu điểm:**
- ✅ Giao diện đơn giản
- ✅ Auto-scaling
- ✅ Add-ons phong phú

**Cách triển khai:**

#### Tạo Procfile:
```
web: sh setup.sh && streamlit run stock_analyzer/app.py --server.port=$PORT --server.address=0.0.0.0
```

#### Tạo setup.sh:
```bash
mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
name = \"Your Name\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
enableWebsocketCompression = false\n\
" > ~/.streamlit/config.toml
```

#### Deploy:
```bash
# Cài đặt Heroku CLI
# Login
heroku login

# Tạo app
heroku create your-app-name

# Deploy
git push heroku main
```

**Chi phí:** ~$5-25/tháng

---

### 4. **AWS EC2** (Chuyên nghiệp)

**Ưu điểm:**
- ✅ Full control
- ✅ Scalable
- ✅ Multiple regions

**Cách triển khai:**

#### Bước 1: Setup EC2 Instance
```bash
# Chọn AMI: Ubuntu 20.04
# Instance type: t3.medium (2 CPU, 4GB RAM)
# Security Group: mở port 8501
```

#### Bước 2: Cài đặt dependencies
```bash
# SSH vào instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Cài đặt Python và pip
sudo apt update
sudo apt install python3 python3-pip nginx

# Clone code
git clone https://github.com/your-username/stock-analyzer.git
cd stock-analyzer

# Cài đặt dependencies
pip3 install -r requirements.txt

# Chạy ứng dụng
streamlit run stock_analyzer/app.py --server.port 8501 --server.address 0.0.0.0 &
```

#### Bước 3: Cấu hình Nginx
```nginx
# /etc/nginx/sites-available/stock-analyzer
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

**Chi phí:** ~$20-100/tháng

---

### 5. **Google Cloud Run** (Serverless)

**Ưu điểm:**
- ✅ Pay-per-use
- ✅ Auto-scaling
- ✅ Global CDN

**Cách triển khai:**

#### Tạo Dockerfile:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "stock_analyzer/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Deploy:
```bash
# Build và push image
gcloud builds submit --tag gcr.io/PROJECT-ID/stock-analyzer

# Deploy
gcloud run deploy stock-analyzer \
    --image gcr.io/PROJECT-ID/stock-analyzer \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

**Chi phí:** ~$10-50/tháng

---

### 6. **Docker + VPS** (Tự host)

**Ưu điểm:**
- ✅ Full control
- ✅ One-click deployment
- ✅ Easy to maintain

**Cách triển khai:**

#### Tạo docker-compose.yml:
```yaml
version: '3.8'

services:
  stock-analyzer:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - stock-analyzer
    restart: unless-stopped
```

#### Deploy:
```bash
# Chạy ứng dụng
docker-compose up -d

# Monitor logs
docker-compose logs -f
```

---

## 🛡️ Bảo mật và Cấu hình

### SSL Certificate (Let's Encrypt)
```bash
# Cài đặt certbot
sudo apt install certbot python3-certbot-nginx

# Lấy certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Thêm dòng: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Environment Variables
```bash
# Tạo file .env
DATABASE_URL=your_database_url
API_KEY=your_api_key
SECRET_KEY=your_secret_key
```

### Rate Limiting
```python
# Thêm vào app.py
import time
from collections import defaultdict

# Simple rate limiter
rate_limit = defaultdict(list)

def rate_limit_check(ip, max_requests=100, time_window=3600):
    now = time.time()
    rate_limit[ip] = [req_time for req_time in rate_limit[ip] 
                     if now - req_time < time_window]
    
    if len(rate_limit[ip]) >= max_requests:
        return False
    
    rate_limit[ip].append(now)
    return True
```

---

## 📱 Truy cập từ Nhiều Thiết bị

### 1. **Desktop/Laptop**
- URL: `https://your-app-name.streamlit.app`
- Browser: Chrome, Firefox, Safari, Edge

### 2. **Mobile Phone**
- URL: `https://your-app-name.streamlit.app`
- Browser: Chrome Mobile, Safari Mobile
- Responsive design tự động

### 3. **Tablet**
- URL: `https://your-app-name.streamlit.app`
- Tối ưu cho màn hình lớn hơn mobile

### 4. **Từ xa qua VPN**
- Truy cập qua domain name
- SSL certificate đảm bảo bảo mật

---

## 🔧 Monitoring và Maintenance

### Health Check
```python
# Thêm vào app.py
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# Streamlit app
st.set_page_config(page_title="Stock Analyzer - Health Check")
st.json(health_check())
```

### Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('stock_analyzer.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

---

## 💡 Khuyến nghị

### Cho người mới bắt đầu:
1. **Streamlit Cloud** - Miễn phí, dễ sử dụng
2. **Heroku** - Đơn giản, có free tier

### Cho doanh nghiệp:
1. **AWS EC2** - Full control, scalable
2. **Google Cloud Run** - Serverless, global
3. **Docker + VPS** - Self-hosted, cost-effective

### Chi phí ước tính:
- **Free:** Streamlit Cloud, Ngrok
- **Low cost:** Heroku ($5-25/tháng)
- **Medium cost:** VPS ($20-50/tháng)
- **Enterprise:** AWS/GCP ($50-200/tháng)

---

## 📞 Hỗ trợ

Nếu gặp vấn đề trong quá trình triển khai:

1. **Kiểm tra logs** của platform
2. **Verify requirements.txt** có đầy đủ dependencies
3. **Test local** trước khi deploy
4. **Check port và firewall** settings
5. **SSL certificate** configuration

**Chúc bạn triển khai thành công!** 🎉