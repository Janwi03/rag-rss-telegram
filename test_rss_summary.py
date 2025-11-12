from rss_rag.rss_reader import fetch_rss_articles
from rss_rag.summarizer import LocalSummarizer

rss_url = "https://feeds.bbci.co.uk/news/rss.xml"  # BBC News RSS feed
articles = fetch_rss_articles(rss_url, limit=2)

summarizer = LocalSummarizer()

for art in articles:
    print(f"📰 {art['title']}")
    print("Link:", art['link'])
    print("Original summary:", art['summary'][:200], "...")
    print("🔹 Generated Summary:", summarizer.summarize_text(art['summary']))
    print("-" * 80)