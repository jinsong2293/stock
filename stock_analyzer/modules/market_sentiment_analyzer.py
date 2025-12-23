"""
Advanced Market Sentiment Analysis Engine
Real-time Sentiment Analysis from News, Social Media, and Market Indicators
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import requests
import json
import re
# from textblob import TextBlob  # Optional dependency
from collections import Counter
import warnings

logger = logging.getLogger(__name__)
warnings.filterwarnings('ignore')

class SentimentLevel(Enum):
    """Sentiment classification levels"""
    VERY_BEARISH = "very_bearish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"
    BULLISH = "bullish"
    VERY_BULLISH = "very_bullish"

@dataclass
class SentimentData:
    """Sentiment data structure"""
    source: str
    text: str
    sentiment_score: float
    confidence: float
    timestamp: datetime
    keywords: List[str]

class MarketSentimentAnalyzer:
    """
    Advanced Market Sentiment Analysis Engine
    Combines news, social media, and market indicators for comprehensive sentiment analysis
    """
    
    def __init__(self):
        self.news_sources = self._initialize_news_sources()
        self.sentiment_keywords = self._load_sentiment_keywords()
        self.market_indicators = self._initialize_market_indicators()
        
    def _initialize_news_sources(self) -> Dict[str, str]:
        """
        Initialize news sources configuration
        """
        return {
            'reuters': 'https://www.reuters.com/markets/',
            'bloomberg': 'https://www.bloomberg.com/markets',
            'cnbc': 'https://www.cnbc.com/financial-markets/',
            'marketwatch': 'https://www.marketwatch.com/investing/index/spx',
            'yahoo_finance': 'https://finance.yahoo.com/',
            'vn_express': 'https://vnexpress.net/kinh-doanh',
            'zing_news': 'https://zingnews.vn/kinh-doanh'
        }
    
    def _load_sentiment_keywords(self) -> Dict[str, List[str]]:
        """
        Load sentiment keywords for Vietnamese and English markets
        """
        return {
            'bullish_keywords': [
                # English
                'bullish', 'rally', 'surge', 'gain', 'rise', 'uptrend', 'breakout', 
                'growth', 'profit', 'earnings', 'positive', 'strong', 'buy', 'invest',
                'opportunity', 'optimistic', 'confident', 'recovery', 'boom', 'momentum',
                
                # Vietnamese
                'tăng giá', 'tích cực', 'tăng trưởng', 'lợi nhuận', 'mua vào', 
                'cơ hội', 'lạc quan', 'phục hồi', 'bùng nổ', 'động lực', 'xu hướng tăng'
            ],
            'bearish_keywords': [
                # English
                'bearish', 'crash', 'plunge', 'decline', 'drop', 'downtrend', 'selloff',
                'loss', 'negative', 'weak', 'sell', 'recession', 'fear', 'concern',
                'volatility', 'correction', 'crisis', 'bubble', 'debt', 'default',
                
                # Vietnamese
                'giảm giá', 'tiêu cực', 'suy thoái', 'thua lỗ', 'bán ra', 'lo ngại',
                'bất ổn', 'khủng hoảng', 'nợ', 'vỡ nợ', 'khủng hoảng', 'xu hướng giảm'
            ],
            'neutral_keywords': [
                # English
                'neutral', 'stable', 'flat', 'sideways', 'consolidation', 'mixed',
                'balanced', 'steady', 'unchanged', 'moderate', 'cautious',
                
                # Vietnamese
                'trung tính', 'ổn định', 'đi ngang', 'cân bằng', 'thận trọng', 'trung bình'
            ]
        }
    
    def _initialize_market_indicators(self) -> Dict[str, float]:
        """
        Initialize market indicator weights for sentiment calculation
        """
        return {
            'vix_weight': 0.25,      # Volatility index
            'put_call_ratio': 0.20,  # Options sentiment
            'advance_decline': 0.15, # Breadth indicator
            'volume_surge': 0.15,    # Volume analysis
            'insider_trading': 0.15, # Insider sentiment
            'short_interest': 0.10   # Short sentiment
        }
    
    def analyze_market_sentiment_comprehensive(self, ticker: str = None, 
                                             market: str = "VN") -> Dict[str, Any]:
        """
        Perform comprehensive market sentiment analysis
        """
        logger.info(f"Starting comprehensive sentiment analysis for {ticker or 'market'}")
        
        sentiment_results = {
            'ticker': ticker,
            'market': market,
            'analysis_time': datetime.now().isoformat(),
            'overall_sentiment': {},
            'news_sentiment': {},
            'social_sentiment': {},
            'market_indicators': {},
            'sentiment_score': 0.0,
            'sentiment_category': 'neutral',
            'confidence': 0.0,
            'key_insights': [],
            'alerts': []
        }
        
        try:
            # Analyze news sentiment
            sentiment_results['news_sentiment'] = self._analyze_news_sentiment(
                ticker, market
            )
            
            # Analyze social media sentiment (simulated for now)
            sentiment_results['social_sentiment'] = self._analyze_social_sentiment(
                ticker, market
            )
            
            # Analyze market indicators
            sentiment_results['market_indicators'] = self._analyze_market_indicators(
                ticker, market
            )
            
            # Calculate overall sentiment
            sentiment_results['overall_sentiment'] = self._calculate_overall_sentiment(
                sentiment_results
            )
            
            # Generate insights and alerts
            sentiment_results['key_insights'] = self._generate_sentiment_insights(
                sentiment_results
            )
            sentiment_results['alerts'] = self._generate_sentiment_alerts(
                sentiment_results
            )
            
        except Exception as e:
            logger.error(f"Error in comprehensive sentiment analysis: {str(e)}")
            sentiment_results['error'] = str(e)
        
        return sentiment_results
    
    def _analyze_news_sentiment(self, ticker: str = None, market: str = "VN") -> Dict[str, Any]:
        """
        Analyze sentiment from news sources
        """
        news_sentiment = {
            'articles_analyzed': 0,
            'average_sentiment': 0.0,
            'sentiment_distribution': {},
            'top_headlines': [],
            'key_topics': [],
            'confidence': 0.0
        }
        
        try:
            # Simulate news fetching (in real implementation, would fetch from APIs)
            articles = self._fetch_news_articles(ticker, market)
            
            if not articles:
                logger.warning("No news articles found")
                return news_sentiment
            
            sentiment_scores = []
            headlines = []
            topics = []
            
            for article in articles:
                # Analyze sentiment
                sentiment_score = self._analyze_text_sentiment(article['text'])
                sentiment_scores.append(sentiment_score)
                
                headlines.append({
                    'headline': article['headline'],
                    'sentiment': sentiment_score,
                    'source': article['source'],
                    'timestamp': article['timestamp']
                })
                
                # Extract topics
                article_topics = self._extract_topics(article['text'])
                topics.extend(article_topics)
            
            # Calculate metrics
            news_sentiment['articles_analyzed'] = len(articles)
            news_sentiment['average_sentiment'] = np.mean(sentiment_scores) if sentiment_scores else 0.0
            news_sentiment['top_headlines'] = sorted(headlines, 
                                                   key=lambda x: abs(x['sentiment']), 
                                                   reverse=True)[:5]
            news_sentiment['key_topics'] = self._get_top_topics(topics)
            news_sentiment['confidence'] = min(1.0, len(articles) / 10)  # More articles = higher confidence
            
        except Exception as e:
            logger.error(f"Error analyzing news sentiment: {str(e)}")
        
        return news_sentiment
    
    def _analyze_social_sentiment(self, ticker: str = None, market: str = "VN") -> Dict[str, Any]:
        """
        Analyze sentiment from social media (simulated)
        """
        social_sentiment = {
            'mentions_analyzed': 0,
            'average_sentiment': 0.0,
            'sentiment_trend': [],
            'influencer_sentiment': {},
            'hashtag_performance': {},
            'confidence': 0.0
        }
        
        try:
            # Simulate social media data fetching
            social_data = self._fetch_social_media_data(ticker, market)
            
            if not social_data:
                return social_sentiment
            
            mentions = social_data.get('mentions', [])
            sentiment_scores = []
            
            for mention in mentions:
                sentiment_score = self._analyze_text_sentiment(mention['text'])
                sentiment_scores.append(sentiment_score)
            
            social_sentiment['mentions_analyzed'] = len(mentions)
            social_sentiment['average_sentiment'] = np.mean(sentiment_scores) if sentiment_scores else 0.0
            social_sentiment['confidence'] = min(1.0, len(mentions) / 50)
            
        except Exception as e:
            logger.error(f"Error analyzing social sentiment: {str(e)}")
        
        return social_sentiment
    
    def _analyze_market_indicators(self, ticker: str = None, market: str = "VN") -> Dict[str, Any]:
        """
        Analyze sentiment from market indicators
        """
        market_indicators = {
            'vix_sentiment': 0.0,
            'put_call_sentiment': 0.0,
            'breadth_sentiment': 0.0,
            'volume_sentiment': 0.0,
            'insider_sentiment': 0.0,
            'short_sentiment': 0.0,
            'overall_indicator_sentiment': 0.0
        }
        
        try:
            # VIX Analysis (volatility fear index)
            vix_level = self._get_vix_level(market)
            market_indicators['vix_sentiment'] = self._calculate_vix_sentiment(vix_level)
            
            # Put/Call Ratio Analysis
            put_call_ratio = self._get_put_call_ratio(market)
            market_indicators['put_call_sentiment'] = self._calculate_put_call_sentiment(put_call_ratio)
            
            # Market Breadth Analysis
            breadth_data = self._get_market_breadth(market)
            market_indicators['breadth_sentiment'] = self._calculate_breadth_sentiment(breadth_data)
            
            # Volume Analysis
            volume_data = self._get_volume_analysis(ticker)
            market_indicators['volume_sentiment'] = self._calculate_volume_sentiment(volume_data)
            
            # Calculate overall indicator sentiment
            weights = self.market_indicators
            indicator_sentiments = [
                market_indicators['vix_sentiment'] * weights['vix_weight'],
                market_indicators['put_call_sentiment'] * weights['put_call_ratio'],
                market_indicators['breadth_sentiment'] * weights['advance_decline'],
                market_indicators['volume_sentiment'] * weights['volume_surge']
            ]
            
            market_indicators['overall_indicator_sentiment'] = np.mean(indicator_sentiments)
            
        except Exception as e:
            logger.error(f"Error analyzing market indicators: {str(e)}")
        
        return market_indicators
    
    def _calculate_overall_sentiment(self, sentiment_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate overall sentiment from all sources
        """
        overall_sentiment = {
            'combined_score': 0.0,
            'sentiment_category': 'neutral',
            'confidence': 0.0,
            'source_weights': {
                'news': 0.4,
                'social': 0.3,
                'market_indicators': 0.3
            }
        }
        
        try:
            # Get individual sentiment scores
            news_score = sentiment_results.get('news_sentiment', {}).get('average_sentiment', 0.0)
            social_score = sentiment_results.get('social_sentiment', {}).get('average_sentiment', 0.0)
            market_score = sentiment_results.get('market_indicators', {}).get('overall_indicator_sentiment', 0.0)
            
            # Get confidence levels
            news_conf = sentiment_results.get('news_sentiment', {}).get('confidence', 0.0)
            social_conf = sentiment_results.get('social_sentiment', {}).get('confidence', 0.0)
            
            # Calculate weighted sentiment
            weights = overall_sentiment['source_weights']
            combined_score = (
                news_score * weights['news'] +
                social_score * weights['social'] +
                market_score * weights['market_indicators']
            )
            
            overall_sentiment['combined_score'] = combined_score
            
            # Determine sentiment category
            if combined_score >= 0.6:
                overall_sentiment['sentiment_category'] = 'very_bullish'
            elif combined_score >= 0.2:
                overall_sentiment['sentiment_category'] = 'bullish'
            elif combined_score <= -0.6:
                overall_sentiment['sentiment_category'] = 'very_bearish'
            elif combined_score <= -0.2:
                overall_sentiment['sentiment_category'] = 'bearish'
            else:
                overall_sentiment['sentiment_category'] = 'neutral'
            
            # Calculate confidence
            overall_confidence = (news_conf * weights['news'] + social_conf * weights['social'])
            overall_sentiment['confidence'] = overall_confidence
            
        except Exception as e:
            logger.error(f"Error calculating overall sentiment: {str(e)}")
        
        return overall_sentiment
    
    def _analyze_text_sentiment(self, text: str) -> float:
        """
        Analyze sentiment of text using keyword matching and TextBlob
        """
        try:
            # Clean text
            clean_text = re.sub(r'[^\w\s]', ' ', text.lower())
            
            # Count sentiment keywords
            bullish_count = sum(1 for keyword in self.sentiment_keywords['bullish_keywords'] 
                              if keyword.lower() in clean_text)
            bearish_count = sum(1 for keyword in self.sentiment_keywords['bearish_keywords'] 
                              if keyword.lower() in clean_text)
            neutral_count = sum(1 for keyword in self.sentiment_keywords['neutral_keywords'] 
                              if keyword.lower() in clean_text)
            
            # Use simple sentiment analysis based on word counts
            total_keywords = bullish_count + bearish_count + neutral_count
            if total_keywords > 0:
                keyword_sentiment = (bullish_count - bearish_count) / total_keywords
                final_sentiment = keyword_sentiment
            else:
                # Default neutral sentiment when no keywords found
                final_sentiment = 0.0
            
            # Ensure sentiment is between -1 and 1
            return max(-1.0, min(1.0, final_sentiment))
            
        except Exception as e:
            logger.error(f"Error analyzing text sentiment: {str(e)}")
            return 0.0
    
    def _fetch_news_articles(self, ticker: str = None, market: str = "VN") -> List[Dict[str, Any]]:
        """
        Fetch news articles (simulated for demonstration)
        """
        # In real implementation, this would fetch from news APIs
        # For now, return simulated data
        sample_articles = [
            {
                'headline': f'{ticker or "Market"} shows strong growth potential',
                'text': 'The company demonstrates positive earnings growth and bullish market sentiment.',
                'source': 'MarketWatch',
                'timestamp': datetime.now() - timedelta(hours=2)
            },
            {
                'headline': f'Regulators approve major deal for {ticker or "tech sector"}',
                'text': 'Positive regulatory news drives investor confidence and market optimism.',
                'source': 'Reuters',
                'timestamp': datetime.now() - timedelta(hours=4)
            }
        ]
        
        return sample_articles
    
    def _fetch_social_media_data(self, ticker: str = None, market: str = "VN") -> Dict[str, Any]:
        """
        Fetch social media data (simulated)
        """
        # In real implementation, this would fetch from Twitter, Reddit, etc.
        sample_mentions = [
            {
                'text': f'{ticker or "Stock"} looking strong today! #bullish',
                'timestamp': datetime.now() - timedelta(minutes=30),
                'platform': 'twitter'
            },
            {
                'text': f'Not sure about {ticker or "this stock"}, staying cautious',
                'timestamp': datetime.now() - timedelta(hours=1),
                'platform': 'reddit'
            }
        ]
        
        return {'mentions': sample_mentions}
    
    def _extract_topics(self, text: str) -> List[str]:
        """
        Extract topics from text
        """
        # Simple keyword extraction
        topics = []
        text_lower = text.lower()
        
        financial_keywords = ['earnings', 'revenue', 'profit', 'loss', 'merger', 'acquisition',
                             'lợi nhuận', 'doanh thu', 'sáp nhập', 'mua bán']
        
        for keyword in financial_keywords:
            if keyword in text_lower:
                topics.append(keyword)
        
        return topics
    
    def _get_top_topics(self, topics: List[str]) -> List[Tuple[str, int]]:
        """
        Get top topics by frequency
        """
        topic_counts = Counter(topics)
        return topic_counts.most_common(5)
    
    def _get_vix_level(self, market: str) -> float:
        """
        Get VIX level (simulated)
        """
        # In real implementation, fetch from market data API
        return 25.0  # Simulated VIX level
    
    def _calculate_vix_sentiment(self, vix_level: float) -> float:
        """
        Calculate sentiment from VIX level
        """
        if vix_level < 15:
            return 0.8  # Very bullish (low volatility)
        elif vix_level < 20:
            return 0.5  # Bullish
        elif vix_level < 30:
            return 0.0  # Neutral
        elif vix_level < 40:
            return -0.5  # Bearish
        else:
            return -0.8  # Very bearish (high volatility)
    
    def _get_put_call_ratio(self, market: str) -> float:
        """
        Get put/call ratio (simulated)
        """
        return 0.8  # Simulated ratio
    
    def _calculate_put_call_sentiment(self, ratio: float) -> float:
        """
        Calculate sentiment from put/call ratio
        """
        if ratio < 0.7:
            return 0.5  # Bullish (more calls)
        elif ratio < 1.0:
            return 0.0  # Neutral
        else:
            return -0.5  # Bearish (more puts)
    
    def _get_market_breadth(self, market: str) -> Dict[str, float]:
        """
        Get market breadth data (simulated)
        """
        return {
            'advances': 1500,
            'declines': 1000,
            'unchanged': 500,
            'total': 3000
        }
    
    def _calculate_breadth_sentiment(self, breadth_data: Dict[str, float]) -> float:
        """
        Calculate sentiment from market breadth
        """
        advances = breadth_data['advances']
        declines = breadth_data['declines']
        total = breadth_data['total']
        
        if total > 0:
            advance_ratio = advances / total
            if advance_ratio > 0.6:
                return 0.6  # Bullish
            elif advance_ratio > 0.4:
                return 0.0  # Neutral
            else:
                return -0.6  # Bearish
        return 0.0
    
    def _get_volume_analysis(self, ticker: str = None) -> Dict[str, Any]:
        """
        Get volume analysis (simulated)
        """
        return {
            'current_volume': 1000000,
            'avg_volume': 800000,
            'volume_ratio': 1.25
        }
    
    def _calculate_volume_sentiment(self, volume_data: Dict[str, Any]) -> float:
        """
        Calculate sentiment from volume analysis
        """
        volume_ratio = volume_data['volume_ratio']
        if volume_ratio > 2.0:
            return 0.7  # Very bullish (high volume)
        elif volume_ratio > 1.5:
            return 0.4  # Bullish
        elif volume_ratio > 0.8:
            return 0.0  # Neutral
        else:
            return -0.4  # Bearish (low volume)
    
    def _generate_sentiment_insights(self, sentiment_results: Dict[str, Any]) -> List[str]:
        """
        Generate key insights from sentiment analysis
        """
        insights = []
        
        try:
            overall_sentiment = sentiment_results.get('overall_sentiment', {})
            combined_score = overall_sentiment.get('combined_score', 0.0)
            sentiment_category = overall_sentiment.get('sentiment_category', 'neutral')
            
            # Overall sentiment insight
            if sentiment_category == 'very_bullish':
                insights.append("Market sentiment is extremely positive with strong buying pressure")
            elif sentiment_category == 'very_bearish':
                insights.append("Market sentiment is highly negative with significant selling pressure")
            elif sentiment_category == 'bullish':
                insights.append("Market sentiment leans positive with moderate buying interest")
            elif sentiment_category == 'bearish':
                insights.append("Market sentiment shows bearish bias with selling pressure")
            else:
                insights.append("Market sentiment remains neutral with mixed signals")
            
            # News sentiment insight
            news_sentiment = sentiment_results.get('news_sentiment', {})
            articles_count = news_sentiment.get('articles_analyzed', 0)
            if articles_count > 5:
                insights.append(f"Strong news coverage with {articles_count} articles analyzed")
            
            # Market indicators insight
            market_indicators = sentiment_results.get('market_indicators', {})
            vix_sentiment = market_indicators.get('vix_sentiment', 0.0)
            if vix_sentiment > 0.5:
                insights.append("Low volatility indicates stable market conditions")
            elif vix_sentiment < -0.5:
                insights.append("High volatility suggests market uncertainty")
            
        except Exception as e:
            logger.error(f"Error generating sentiment insights: {str(e)}")
        
        return insights
    
    def _generate_sentiment_alerts(self, sentiment_results: Dict[str, Any]) -> List[str]:
        """
        Generate sentiment-based alerts
        """
        alerts = []
        
        try:
            overall_sentiment = sentiment_results.get('overall_sentiment', {})
            combined_score = overall_sentiment.get('combined_score', 0.0)
            confidence = overall_sentiment.get('confidence', 0.0)
            
            # High confidence alerts
            if confidence > 0.8:
                if combined_score > 0.7:
                    alerts.append("HIGH ALERT: Strong bullish sentiment with high confidence")
                elif combined_score < -0.7:
                    alerts.append("HIGH ALERT: Strong bearish sentiment with high confidence")
            
            # Extreme sentiment alerts
            if abs(combined_score) > 0.8:
                direction = "bullish" if combined_score > 0 else "bearish"
                alerts.append(f"EXTREME SENTIMENT: Market showing extreme {direction} bias")
            
            # Divergence alerts
            news_score = sentiment_results.get('news_sentiment', {}).get('average_sentiment', 0.0)
            market_score = sentiment_results.get('market_indicators', {}).get('overall_indicator_sentiment', 0.0)
            
            if abs(news_score - market_score) > 0.5:
                alerts.append("SENTIMENT DIVERGENCE: News and market indicators showing conflicting signals")
            
        except Exception as e:
            logger.error(f"Error generating sentiment alerts: {str(e)}")
        
        return alerts

# Global instance
market_sentiment_analyzer = MarketSentimentAnalyzer()

if __name__ == "__main__":
    # Example usage
    print("🧪 Testing Market Sentiment Analyzer...")
    
    try:
        # Test comprehensive sentiment analysis
        ticker = "AAA"
        results = market_sentiment_analyzer.analyze_market_sentiment_comprehensive(ticker)
        
        print(f"✅ Sentiment analysis completed for {ticker}")
        print(f"📊 Overall Score: {results['overall_sentiment']['combined_score']:.2f}")
        print(f"🎯 Sentiment Category: {results['overall_sentiment']['sentiment_category']}")
        print(f"📈 Confidence: {results['overall_sentiment']['confidence']:.2f}")
        
        # Show component analysis
        news = results.get('news_sentiment', {})
        print(f"📰 News Analysis: {news.get('articles_analyzed', 0)} articles, avg sentiment: {news.get('average_sentiment', 0):.2f}")
        
        social = results.get('social_sentiment', {})
        print(f"📱 Social Analysis: {social.get('mentions_analyzed', 0)} mentions, avg sentiment: {social.get('average_sentiment', 0):.2f}")
        
        indicators = results.get('market_indicators', {})
        print(f"📊 Market Indicators: Overall sentiment {indicators.get('overall_indicator_sentiment', 0):.2f}")
        
        # Show insights
        insights = results.get('key_insights', [])
        if insights:
            print(f"💡 Key Insights ({len(insights)}):")
            for insight in insights[:3]:
                print(f"   • {insight}")
        
        # Show alerts
        alerts = results.get('alerts', [])
        if alerts:
            print(f"⚠️ Alerts ({len(alerts)}):")
            for alert in alerts:
                print(f"   🚨 {alert}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()