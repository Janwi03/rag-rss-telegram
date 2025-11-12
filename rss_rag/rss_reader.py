# rss_rag/rss_reader.py

import feedparser

def fetch_rss_articles(feed_url, limit=5):
    """
    Fetch latest articles from an RSS feed.
    Returns a list of dicts: {title, link, summary, published}
    """
    feed = feedparser.parse(feed_url)
    articles = []
    
    for entry in feed.entries[:limit]:
        article = {
            "title": entry.title,
            "link": entry.link,
            "summary": getattr(entry, "summary", ""),
            "published": getattr(entry, "published", "Unknown")
        }
        articles.append(article)

    return articles