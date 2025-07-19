from textblob import TextBlob

def analyze_sentiment(text):
    if not text.strip():
        return "neutral"
    polarity = TextBlob(text).sentiment.polarity
    if polarity < -0.25:
        return "negative"
    elif polarity > 0.25:
        return "positive"
    return "neutral"
