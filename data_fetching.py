import yfinance as yf
import pandas as pd
import random
from newsapi import NewsApiClient
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to fetch historical stock data
def fetch_stock_data(tickers, start_date, end_date):
    """Fetch historical stock data for multiple tickers."""
    all_data = {}
    for ticker in tickers:
        try:
            stock_data = yf.download(ticker, start=start_date, end=end_date)
            stock_data.reset_index(inplace=True)
            stock_data.to_csv(f"data/{ticker}_stock_data.csv", index=False)
            all_data[ticker] = stock_data
            logging.info(f"Saved stock data for {ticker}")
        except Exception as e:
            logging.error(f"Failed to fetch stock data for {ticker}: {e}")
    return all_data

# Function to generate synthetic user profiles
def generate_user_profiles(num_profiles=100):
    """Generate synthetic user profiles for training."""
    profiles = []
    risk_levels = ["low", "medium", "high"]
    
    for _ in range(num_profiles):
        income = random.randint(3000, 10000)  # Monthly income
        expenses = random.randint(1000, 8000)  # Monthly expenses
        investment_amount = random.randint(500, 5000)  # Amount they want to invest
        risk_tolerance = random.choice(risk_levels)  # User's risk tolerance
        savings = income - expenses  # Calculate monthly savings

        profile = {
            "income": income,
            "expenses": expenses,
            "savings": savings,
            "risk_tolerance": risk_tolerance,
            "investment_amount": investment_amount
        }
        profiles.append(profile)
    
    user_profiles_df = pd.DataFrame(profiles)
    try:
        user_profiles_df.to_csv("data/user_profiles.csv", index=False)
        logging.info("Saved synthetic user profiles to data/user_profiles.csv")
    except Exception as e:
        logging.error(f"Failed to save user profiles: {e}")
    return user_profiles_df

# Function to fetch market news
def fetch_market_news(api_key, query="stock market", language="en"):
    """Fetch market news using NewsAPI."""
    try:
        newsapi = NewsApiClient(api_key=api_key)
        articles = newsapi.get_everything(q=query, language=language)
        with open("data/market_news.json", "w") as f:
            json.dump(articles["articles"], f)
        logging.info("Saved market news to data/market_news.json")
        return articles["articles"]
    except Exception as e:
        logging.error(f"Failed to fetch market news: {e}")
        return []

# Main execution block
if __name__ == "__main__":
    # Create the 'data' directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")
        logging.info("Created 'data' directory.")
    
    # Fetch stock data for multiple companies
    tickers = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA"]
    start_date = "2020-01-01"
    end_date = "2023-01-01"
    stock_data = fetch_stock_data(tickers, start_date, end_date)

    # Generate synthetic user profiles
    user_profiles = generate_user_profiles()

    # Fetch market news
    news_api_key = os.getenv("NEWS_API_KEY", "32578638d48a41158abf5cd1a34c6f74")
    market_news = fetch_market_news(api_key=news_api_key)

    logging.info("\nSample User Profiles:")
    logging.info(user_profiles.head())

    if market_news:
        logging.info("\nSample Market News Headline:")
        logging.info(market_news[0]["title"])
    else:
        logging.warning("No market news found.")
