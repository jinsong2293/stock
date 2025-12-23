import pandas as pd
import sys
import os

# Add the parent directory to the system path to import config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from stock_analyzer.config import GOOGLE_API_KEY

def analyze_market_sentiment(ticker, data):
    """
    Analyzes market sentiment for a given stock ticker based on technical indicators
    and integrates with Google API for enhanced sentiment analysis.
    """
    print(f"Analyzing market sentiment for {ticker}...")

    sentiment_score = 0.5  # Default to neutral
    sentiment_category = "Neutral"

    # Use the last RSI value as a proxy for market sentiment.
    if not data.empty and 'RSI' in data.columns:
        try:
            last_rsi = data['RSI'].iloc[-1]
            # Normalize RSI (0-100) to a sentiment score (0-1)
            sentiment_score = last_rsi / 100.0

            if last_rsi > 70:
                sentiment_category = "Positive" # Overbought can be seen as positive/greedy sentiment
            elif last_rsi < 30:
                sentiment_category = "Negative" # Oversold can be seen as negative/fearful sentiment
        except Exception as e:
            print(f"Error calculating sentiment from RSI: {e}")
            sentiment_score = 0.5
            sentiment_category = "Neutral"

    # Integrate with Google API for enhanced sentiment analysis
    try:
        news_impact, google_social_media_buzz = get_google_sentiment_analysis(ticker)
    except Exception as e:
        print(f"Error fetching sentiment from Google API: {e}")
        news_impact = "Không có dữ liệu"
        google_social_media_buzz = "Không có dữ liệu"

    # Integrate with Twitter API for enhanced sentiment analysis
    try:
        twitter_sentiment, twitter_social_media_buzz = get_twitter_sentiment_analysis(ticker)
    except Exception as e:
        print(f"Error fetching sentiment from Twitter API: {e}")
        twitter_sentiment = "Không có dữ liệu"
        twitter_social_media_buzz = "Không có dữ liệu"

    # Combine social media buzz from both sources
    social_media_buzz = f"Google: {google_social_media_buzz}, Twitter: {twitter_social_media_buzz}"

    sentiment_results = {
        "sentiment_score": sentiment_score,
        "sentiment_category": sentiment_category,
        "news_impact": news_impact,
        "social_media_buzz": social_media_buzz,
        "twitter_sentiment": twitter_sentiment
    }

    print(f"Market sentiment analysis for {ticker} complete: {sentiment_category} (Score: {sentiment_score:.2f})")
    return sentiment_results

def get_google_sentiment_analysis(ticker):
    """
    Uses Google API to fetch sentiment analysis data for a given stock ticker.
    This function integrates with Google API for sentiment analysis.
    """
    import requests
    import json
    
    # Use Google News API to fetch news articles related to the stock ticker
    news_url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={GOOGLE_API_KEY}"
    
    try:
        # Fetch news articles
        news_response = requests.get(news_url, timeout=10)
        news_response.raise_for_status()  # Raise an exception for HTTP errors
        news_data = news_response.json()
         
        # Check if the response contains any errors
        if news_data.get('status') != 'ok':
            print(f"Error fetching news from Google News API: {news_data.get('message', 'Unknown error')}")
            return "Không có dữ liệu", "Không có dữ liệu"
         
        # Analyze the sentiment of the news articles using Google Natural Language API
        sentiment_url = f"https://language.googleapis.com/v1/documents:analyzeSentiment?key={GOOGLE_API_KEY}"
        
        # Prepare the request body for sentiment analysis
        articles = news_data.get('articles', [])
        if articles:
            # Combine the titles and descriptions of the articles for sentiment analysis
            text_content = " ".join([article.get('title', '') + " " + article.get('description', '') for article in articles[:5]])  # Limit to 5 articles for efficiency
            
            # Check if the text content is not empty
            if not text_content.strip():
                return "Không có dữ liệu", "Không có dữ liệu"
            
            sentiment_request = {
                "document": {
                    "type": "PLAIN_TEXT",
                    "content": text_content
                },
                "encodingType": "UTF8"
            }
            
            # Send the request to Google Natural Language API
            sentiment_response = requests.post(sentiment_url, json=sentiment_request, timeout=10)
            sentiment_response.raise_for_status()  # Raise an exception for HTTP errors
            sentiment_data = sentiment_response.json()
            
            # Check if the response contains any errors
            if 'error' in sentiment_data:
                print(f"Error analyzing sentiment with Google Natural Language API: {sentiment_data['error'].get('message', 'Unknown error')}")
                return "Không có dữ liệu", "Không có dữ liệu"
            
            # Extract sentiment score and magnitude
            sentiment_score = sentiment_data.get('documentSentiment', {}).get('score', 0)
            
            # Determine news impact based on sentiment score
            if sentiment_score > 0.5:
                news_impact = "Tích cực mạnh"
            elif sentiment_score > 0:
                news_impact = "Tích cực"
            elif sentiment_score < -0.5:
                news_impact = "Tiêu cực mạnh"
            elif sentiment_score < 0:
                news_impact = "Tiêu cực"
            else:
                news_impact = "Trung tính"
            
            # Determine social media buzz based on the number of articles
            num_articles = len(articles)
            if num_articles > 10:
                social_media_buzz = "Cao"
            elif num_articles > 5:
                social_media_buzz = "Trung bình"
            else:
                social_media_buzz = "Thấp"
        else:
            news_impact = "Không có dữ liệu"
            social_media_buzz = "Không có dữ liệu"
            
    except requests.exceptions.RequestException as e:
        print(f"Network error fetching sentiment analysis from Google API: {e}")
        news_impact = "Không có dữ liệu"
        social_media_buzz = "Không có dữ liệu"
    except json.JSONDecodeError as e:
        print(f"JSON decode error fetching sentiment analysis from Google API: {e}")
        news_impact = "Không có dữ liệu"
        social_media_buzz = "Không có dữ liệu"
    except Exception as e:
        print(f"Unexpected error fetching sentiment analysis from Google API: {e}")
        news_impact = "Không có dữ liệu"
        social_media_buzz = "Không có dữ liệu"
    
    return news_impact, social_media_buzz

def get_twitter_sentiment_analysis(ticker):
    """
    Uses Twitter API to fetch sentiment analysis data for a given stock ticker.
    This function integrates with Twitter API for sentiment analysis.
    """
    import requests
    import json
    
    # Use Twitter API to fetch tweets related to the stock ticker
    # This is a placeholder for the actual implementation
    # In a real implementation, this would involve making API calls to Twitter services
    
    try:
        # Simulate fetching tweets from Twitter API
        # For now, we'll simulate the response with placeholder data
        tweets = [
            {"text": f"Great news about {ticker}", "sentiment": "positive"},
            {"text": f"{ticker} is doing well", "sentiment": "positive"},
            {"text": f"Not sure about {ticker}", "sentiment": "neutral"},
            {"text": f"{ticker} is struggling", "sentiment": "negative"},
            {"text": f"Bad news for {ticker}", "sentiment": "negative"}
        ]
        
        # Calculate sentiment score based on tweets
        positive_tweets = sum(1 for tweet in tweets if tweet["sentiment"] == "positive")
        negative_tweets = sum(1 for tweet in tweets if tweet["sentiment"] == "negative")
        neutral_tweets = sum(1 for tweet in tweets if tweet["sentiment"] == "neutral")
        
        total_tweets = len(tweets)
        sentiment_score = (positive_tweets - negative_tweets) / total_tweets if total_tweets > 0 else 0
        
        # Determine sentiment category based on sentiment score
        if sentiment_score > 0.3:
            sentiment_category = "Tích cực"
        elif sentiment_score < -0.3:
            sentiment_category = "Tiêu cực"
        else:
            sentiment_category = "Trung tính"
        
        # Determine social media buzz based on the number of tweets
        if total_tweets > 20:
            social_media_buzz = "Cao"
        elif total_tweets > 10:
            social_media_buzz = "Trung bình"
        else:
            social_media_buzz = "Thấp"
        
        return sentiment_category, social_media_buzz
        
    except Exception as e:
        print(f"Error fetching sentiment analysis from Twitter API: {e}")
        return "Không có dữ liệu", "Không có dữ liệu"

if __name__ == "__main__":
    # Example usage
    ticker = "AAA"
    dummy_data = pd.DataFrame({'Close': [100, 101, 102]}) # Dummy data, not used in this simple simulation

    sentiment = analyze_market_sentiment(ticker, dummy_data)
    print("\nSentiment Analysis Results:")
    for key, value in sentiment.items():
        print(f"- {key.replace('_', ' ').title()}: {value}")
