# rss_rag/summarizer.py

from transformers import pipeline

class LocalSummarizer:
    def __init__(self, model_name="sshleifer/distilbart-cnn-12-6"):
        print(f"Loading summarization model: {model_name}")
        self.summarizer = pipeline("summarization", model=model_name)

    def summarize_text(self, text, max_len=120):
        if not text.strip():
            return "No content available."
        summary = self.summarizer(text, max_length=max_len, min_length=30, do_sample=False)
        return summary[0]["summary_text"]