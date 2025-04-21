import praw
from newsapi import NewsApiClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from dotenv import load_dotenv
import os

from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI()

analyzer = SentimentIntensityAnalyzer()


# def get_reddit_data(coin):
#     reddit = praw.Reddit(
#         client_id=os.getenv('REDDIT_CLIENT_ID'),
#         client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
#         user_agent=os.getenv('REDDIT_USER_AGENT'),
#     )

#     subreddit = reddit.subreddit('cryptocurrency')
#     posts = subreddit.search(coin, sort='new', limit=10)
#     reddit_data = [post.title + " " + post.selftext for post in posts]
#     return reddit_data


def get_news_data(coin):
    newsapi = NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))
    all_articles = newsapi.get_everything(q=coin, language='en', sort_by='relevancy', page_size=20)
    news_data = [article['title'] + " " + article['description'] for article in all_articles['articles']]
    return news_data


# analyze sentiment score
def analyze_sentiment(texts):
    sentiment_scores = []
    for text in texts:
        sentiment_score = analyzer.polarity_scores(text)
        sentiment_scores.append(sentiment_score['compound'])
    return sentiment_scores


# get sentiment analysis
def get_sentiment_analysis(coin):
    # reddit_data = get_reddit_data(coin)
    news_data = get_news_data(coin)

    # combined_data = reddit_data + news_data
    sentiment_scores = analyze_sentiment(news_data)

    # rata-rata skor sentimen untuk keseluruhan data
    average_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0

    # menentukan apakah sentimen secara umum positif, negatif, atau netral
    sentiment_label = "Neutral"
    if average_sentiment > 0.1:
        sentiment_label = "Positive"
    elif average_sentiment < -0.1:
        sentiment_label = "Negative"

    return sentiment_label, average_sentiment


# summarize news data using OpenAI
def summarize_news(coin):
    news_data = get_news_data(coin)

    prompt = f"""
        Summarize the following cryptocurrency-related content about {coin} into a concise and informative summary between 100 and 200 words.Highlight the main sentiment, market trends, and signigicant news.

        {news_data}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert crypto analyst who summarizes crypto news."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7,
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        return f"Error while summarizing: {str(e)}"



def sentiment_and_prediction_analysis(coin, future_predictions):
    sentiment_label, average_sentiment = get_sentiment_analysis(coin)

    summarize = summarize_news(coin)

    recommendation = "Hold"
    if average_sentiment > 0.2 and future_predictions[-1] > future_predictions[0]:
        recommendation = "Buy"
    elif average_sentiment < -0.2 and future_predictions[-1] < future_predictions[0]:
        recommendation = "Sell"

    # skor akhir 1-100 (sentiment + price prediction)
    sentiment_score = (average_sentiment + 1) * 50 # Skor sentiment diubah menjadi rentang 0-100
    price_score = 100 if future_predictions[-1] > future_predictions[0] else 50 # Prediksi harga naik memberi skor lebih

    final_score = (sentiment_score + price_score) / 2

    print("news_data:", get_news_data(coin))
    print("summarize:", summarize)
    return sentiment_label, recommendation, final_score, summarize