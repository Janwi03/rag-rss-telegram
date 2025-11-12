import asyncio
from rss_rag.rss_reader import fetch_rss_articles
from rss_rag.summarizer import summarize_text
from rss_rag.faiss_store import FAISSStore
from rss_rag.embeddings import generate_embedding
from rss_rag.bot_sender import TELEGRAM_BOT_TOKEN, CHAT_ID
from telegram import Bot


async def daily_digest():
    print("🔹 Starting daily RSS summarization process...")
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    faiss_db = FAISSStore("rss_rag/rss_articles.index")

    # STEP 1: Fetch new articles
    articles = fetch_rss_articles([
        "https://feeds.bbci.co.uk/news/rss.xml",
        "https://www.theverge.com/rss/index.xml"
    ])
    print(f"📰 Found {len(articles)} articles.")

    # STEP 2: Process and summarize
    for article in articles:
        title = article["title"]
        link = article["link"]
        summary = article.get("summary", "")

        # Skip empty summaries
        if not summary.strip():
            continue

        # STEP 3: Check duplicate using FAISS embeddings
        emb = generate_embedding(summary)
        is_duplicate = faiss_db.is_duplicate(emb)

        if not is_duplicate:
            # STEP 4: Generate concise summary
            summarized_text = summarize_text(summary)

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
    asyncio.run(daily_digest())