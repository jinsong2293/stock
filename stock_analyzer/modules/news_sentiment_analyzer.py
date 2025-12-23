"""
News Sentiment Analyzer - Thu thập và phân tích sentiment từ tin tức
Tích hợp với hệ thống dự báo chứng khoán

Author: Roo - Architect Mode
Version: 1.0.0
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import requests
import json
from datetime import datetime, timedelta
import logging
try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    print("⚠️ TextBlob not available. Installing: pip install textblob")
    
    # Fallback simple sentiment analysis
    class TextBlob:
        def __init__(self, text):
            self.text = text
        
        @property
        def sentiment(self):
            # Simple fallback sentiment analysis
            positive_words = ['good', 'great', 'excellent', 'strong', 'positive', 'growth', 'profit', 'gain']
            negative_words = ['bad', 'poor', 'weak', 'negative', 'decline', 'loss', 'fall', 'crisis']
            
            text_lower = self.text.lower()
            pos_count = sum(1 for word in positive_words if word in text_lower)
            neg_count = sum(1 for word in negative_words if word in text_lower)
            
            if pos_count > neg_count:
                polarity = 0.7
            elif neg_count > pos_count:
                polarity = 0.3
            else:
                polarity = 0.5
                
            return SimpleSentiment(polarity, 0.5)
    
    class SimpleSentiment:
        def __init__(self, polarity, subjectivity):
            self.polarity = polarity
            self.subjectivity = subjectivity
import yfinance as yf
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import time

logger = logging.getLogger(__name__)

class NewsSentimentAnalyzer:
    """Phân tích sentiment từ tin tức tài chính"""
    
    def __init__(self):
        self.news_sources = {
            'yahoo_finance': 'https://finance.yahoo.com',
            'marketwatch': 'https://marketwatch.com',
            'reuters': 'https://reuters.com',
            'bloomberg': 'https://bloomberg.com'
        }
        self.sentiment_weights = {
            'headline': 0.4,
            'content': 0.6
        }
        
    def get_financial_news(self, symbol: str, days: int = 7) -> List[Dict[str, Any]]:
        """
        Thu thập tin tức tài chính cho một symbol cụ thể
        """
        logger.info(f"Thu thập tin tức cho {symbol} trong {days} ngày qua")
        
        news_data = []
        
        try:
            # Sử dụng Yahoo Finance API để lấy tin tức
            ticker = yf.Ticker(symbol)
            news = ticker.news
            
            if news:
                cutoff_date = datetime.now() - timedelta(days=days)
                
                for article in news:
                    # Parse ngày tháng
                    try:
                        article_date = datetime.fromtimestamp(article.get('providerPublishTime', 0))
                        if article_date >= cutoff_date:
                            news_data.append({
                                'title': article.get('title', ''),
                                'summary': article.get('summary', ''),
                                'link': article.get('link', ''),
                                'publisher': article.get('publisher', ''),
                                'published_time': article_date,
                                'sentiment_score': 0.0,
                                'sentiment_label': 'neutral'
                            })
                    except Exception as e:
                        logger.warning(f"Lỗi parse ngày tháng: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Lỗi thu thập tin tức từ Yahoo Finance: {e}")
        
        # Bổ sung với các nguồn khác (mock data cho demo)
        additional_news = self._get_additional_news(symbol, days)
        news_data.extend(additional_news)
        
        logger.info(f"Thu thập được {len(news_data)} tin tức cho {symbol}")
        return news_data
    
    def _get_additional_news(self, symbol: str, days: int) -> List[Dict[str, Any]]:
        """
        Lấy thêm tin tức từ các nguồn khác (mock data)
        """
        # Mock data để demo - trong thực tế sẽ gọi API thực
        mock_news = [
            {
                'title': f"{symbol} Reports Strong Quarterly Earnings",
                'summary': f"{symbol} exceeded analyst expectations with strong quarterly performance driven by robust demand.",
                'link': f"https://example.com/{symbol.lower()}-earnings",
                'publisher': 'Financial Times',
                'published_time': datetime.now() - timedelta(days=1),
                'sentiment_score': 0.0,
                'sentiment_label': 'neutral'
            },
            {
                'title': f"Analysts Upgrade {symbol} Stock Rating",
                'summary': f"Major investment banks have upgraded {symbol} stock rating from Hold to Buy based on strong fundamentals.",
                'link': f"https://example.com/{symbol.lower()}-upgrade",
                'publisher': 'CNBC',
                'published_time': datetime.now() - timedelta(days=2),
                'sentiment_score': 0.0,
                'sentiment_label': 'neutral'
            }
        ]
        
        return mock_news
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Phân tích sentiment của văn bản sử dụng TextBlob
        """
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 to 1
            subjectivity = blob.sentiment.subjectivity  # 0 to 1
            
            # Chuyển đổi polarity thành sentiment score 0-1
            sentiment_score = (polarity + 1) / 2
            
            # Xác định nhãn sentiment
            if sentiment_score > 0.6:
                sentiment_label = 'positive'
            elif sentiment_score < 0.4:
                sentiment_label = 'negative'
            else:
                sentiment_label = 'neutral'
            
            return {
                'sentiment_score': sentiment_score,
                'sentiment_label': sentiment_label,
                'polarity': polarity,
                'subjectivity': subjectivity,
                'confidence': 1 - abs(polarity - 0.5) * 2
            }
            
        except Exception as e:
            logger.error(f"Lỗi phân tích sentiment: {e}")
            return {
                'sentiment_score': 0.5,
                'sentiment_label': 'neutral',
                'polarity': 0.0,
                'subjectivity': 0.5,
                'confidence': 0.0
            }
    
    def process_news_sentiment(self, news_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Xử lý sentiment cho tất cả tin tức
        """
        logger.info(f"Xử lý sentiment cho {len(news_data)} tin tức")
        
        processed_news = []
        sentiment_scores = []
        sentiment_labels = []
        
        for article in news_data:
            # Kết hợp title và summary để phân tích
            full_text = f"{article['title']} {article['summary']}"
            
            # Phân tích sentiment
            sentiment_result = self.analyze_sentiment(full_text)
            
            # Cập nhật article
            article['sentiment_score'] = sentiment_result['sentiment_score']
            article['sentiment_label'] = sentiment_result['sentiment_label']
            article['sentiment_polarity'] = sentiment_result['polarity']
            article['sentiment_subjectivity'] = sentiment_result['subjectivity']
            article['sentiment_confidence'] = sentiment_result['confidence']
            
            processed_news.append(article)
            sentiment_scores.append(sentiment_result['sentiment_score'])
            sentiment_labels.append(sentiment_result['sentiment_label'])
        
        # Tính toán thống kê tổng quan
        overall_sentiment = np.mean(sentiment_scores) if sentiment_scores else 0.5
        
        sentiment_distribution = {
            'positive': sentiment_labels.count('positive'),
            'negative': sentiment_labels.count('negative'),
            'neutral': sentiment_labels.count('neutral')
        }
        
        # Tính weighted sentiment (tin tức gần đây có trọng số cao hơn)
        weighted_sentiment = self._calculate_weighted_sentiment(processed_news)
        
        return {
            'processed_news': processed_news,
            'overall_sentiment': overall_sentiment,
            'weighted_sentiment': weighted_sentiment,
            'sentiment_distribution': sentiment_distribution,
            'sentiment_trend': self._analyze_sentiment_trend(processed_news),
            'news_count': len(processed_news),
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def _calculate_weighted_sentiment(self, news_data: List[Dict[str, Any]]) -> float:
        """
        Tính sentiment có trọng số theo thời gian (tin tức gần đây có trọng số cao hơn)
        """
        if not news_data:
            return 0.5
        
        now = datetime.now()
        weighted_sum = 0.0
        total_weight = 0.0
        
        for article in news_data:
            # Tính số ngày từ khi tin tức được xuất bản
            days_ago = (now - article['published_time']).days
            if days_ago < 0:
                days_ago = 0
            
            # Trọng số giảm theo thời gian (exponential decay)
            weight = np.exp(-days_ago / 3)  # Half-life 3 ngày
            
            weighted_sum += article['sentiment_score'] * weight
            total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.5
    
    def _analyze_sentiment_trend(self, news_data: List[Dict[str, Any]]) -> str:
        """
        Phân tích xu hướng sentiment (tăng/giảm)
        """
        if len(news_data) < 3:
            return 'stable'
        
        # Sắp xếp theo thời gian
        sorted_news = sorted(news_data, key=lambda x: x['published_time'])
        
        # Chia thành 3 nhóm: cũ, giữa, mới
        n = len(sorted_news)
        old_sentiment = np.mean([article['sentiment_score'] for article in sorted_news[:n//3]])
        new_sentiment = np.mean([article['sentiment_score'] for article in sorted_news[2*n//3:]])
        
        change = new_sentiment - old_sentiment
        
        if change > 0.1:
            return 'improving'
        elif change < -0.1:
            return 'deteriorating'
        else:
            return 'stable'
    
    def get_sentiment_features(self, symbol: str, days: int = 7) -> Dict[str, Any]:
        """
        Lấy các features sentiment để sử dụng trong mô hình dự báo
        """
        logger.info(f"Lấy sentiment features cho {symbol}")
        
        # Thu thập tin tức
        news_data = self.get_financial_news(symbol, days)
        
        # Xử lý sentiment
        sentiment_analysis = self.process_news_sentiment(news_data)
        
        # Tạo features
        features = {
            'sentiment_score': sentiment_analysis['overall_sentiment'],
            'weighted_sentiment': sentiment_analysis['weighted_sentiment'],
            'sentiment_trend': sentiment_analysis['sentiment_trend'],
            'sentiment_volatility': np.std([article['sentiment_score'] for article in sentiment_analysis['processed_news']]) if sentiment_analysis['processed_news'] else 0.0,
            'news_volume': sentiment_analysis['news_count'],
            'positive_ratio': sentiment_analysis['sentiment_distribution']['positive'] / max(1, sentiment_analysis['news_count']),
            'negative_ratio': sentiment_analysis['sentiment_distribution']['negative'] / max(1, sentiment_analysis['news_count']),
            'neutral_ratio': sentiment_analysis['sentiment_distribution']['neutral'] / max(1, sentiment_analysis['news_count']),
            'sentiment_momentum': self._calculate_sentiment_momentum(sentiment_analysis['processed_news']),
            'sentiment_acceleration': self._calculate_sentiment_acceleration(sentiment_analysis['processed_news'])
        }
        
        # Chuyển đổi categorical features thành numeric
        features['sentiment_trend_encoded'] = {
            'improving': 1,
            'stable': 0,
            'deteriorating': -1
        }.get(features['sentiment_trend'], 0)
        
        return features
    
    def _calculate_sentiment_momentum(self, news_data: List[Dict[str, Any]]) -> float:
        """
        Tính momentum của sentiment (tốc độ thay đổi)
        """
        if len(news_data) < 2:
            return 0.0
        
        # Sắp xếp theo thời gian
        sorted_news = sorted(news_data, key=lambda x: x['published_time'])
        
        # Tính difference giữa sentiment gần nhất và trước đó
        recent_sentiment = sorted_news[-1]['sentiment_score']
        previous_sentiment = sorted_news[-2]['sentiment_score']
        
        return recent_sentiment - previous_sentiment
    
    def _calculate_sentiment_acceleration(self, news_data: List[Dict[str, Any]]) -> float:
        """
        Tính acceleration của sentiment (thay đổi trong momentum)
        """
        if len(news_data) < 3:
            return 0.0
        
        # Sắp xếp theo thời gian
        sorted_news = sorted(news_data, key=lambda x: x['published_time'])
        
        # Tính momentum cho 3 tin tức gần nhất
        sentiments = [article['sentiment_score'] for article in sorted_news[-3:]]
        
        if len(sentiments) >= 3:
            momentum_1 = sentiments[1] - sentiments[0]
            momentum_2 = sentiments[2] - sentiments[1]
            return momentum_2 - momentum_1
        
        return 0.0

def test_news_sentiment_analyzer():
    """
    Test function cho News Sentiment Analyzer
    """
    print("🧪 Testing News Sentiment Analyzer...")
    
    try:
        analyzer = NewsSentimentAnalyzer()
        
        # Test với symbol AAPL
        symbol = "AAPL"
        
        print(f"📰 Thu thập tin tức cho {symbol}...")
        news_data = analyzer.get_financial_news(symbol, days=7)
        print(f"✅ Thu thập được {len(news_data)} tin tức")
        
        # Test sentiment analysis
        print("🔍 Phân tích sentiment...")
        sentiment_result = analyzer.process_news_sentiment(news_data)
        
        print(f"📊 Overall Sentiment: {sentiment_result['overall_sentiment']:.3f}")
        print(f"📊 Weighted Sentiment: {sentiment_result['weighted_sentiment']:.3f}")
        print(f"📊 Sentiment Trend: {sentiment_result['sentiment_trend']}")
        print(f"📊 News Count: {sentiment_result['news_count']}")
        
        # Test features
        print("🎯 Tạo sentiment features...")
        features = analyzer.get_sentiment_features(symbol, days=7)
        
        print(f"Features created: {len(features)}")
        for key, value in features.items():
            print(f"  {key}: {value}")
        
        print("✅ News Sentiment Analyzer test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_news_sentiment_analyzer()
