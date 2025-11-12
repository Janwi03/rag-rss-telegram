import asyncio
from telegram import Bot
from rss_rag.rss_reader import fetch_rss_articles
from rss_rag.summarizer import LocalSummarizer
from rss_rag.faiss_store import FAISSStore
from rss_rag.embeddings import generate_embedding  # ✅ Simplified & fixed import
from rss_rag.bot_sender import TELEGRAM_BOT_TOKEN, CHAT_ID


async def daily_digest():
    print("🔹 Starting daily RSS summarization process...")
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    faiss_db = FAISSStore("rss_rag/rss_articles.index")
    summarizer = LocalSummarizer()

    # STEP 1: Fetch new articles
    rss_feeds = [
        "https://feeds.bbci.co.uk/news/rss.xml",
        "https://www.theverge.com/rss/index.xml"
    ]
    articles = fetch_rss_articles(rss_feeds)
    print(f"📰 Found {len(articles)} articles.")

    # STEP 2: Process and summarize
    for article in articles:
        title = article.get("title", "Untitled Article")
        link = article.get("link", "#")
        summary = article.get("summary", "")

        if not summary.strip():
            print(f"⚠️ Skipping empty summary for: {title}")
            continue

        # STEP 3: Generate embedding and check for duplicates
        emb = generate_embedding(summary)
        is_duplicate = faiss_db.is_duplicate(emb)

        if not is_duplicate:
            # STEP 4: Summarize article
            summarized_text = summarizer.summarize_text(summary)

            # STEP 5: Send to Telegram
            message = f"🗞️ *{title}*\n\n{summarized_text}\n\n[Read Full Article]({link})"
            await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

            # STEP 6: Save embedding
            faiss_db.add_entry(emb, title)
            print(f"✅ Sent: {title}")
        else:
            print(f"⏩ Skipped duplicate: {title}")

    print("🎯 Daily digest complete!")


if __name__ == "__main__":
    try:
        asyncio.run(daily_digest())
    except Exception as e:
        print(f"❌ Error during daily digest: {e}")