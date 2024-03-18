import sys
import os
from bs4 import BeautifulSoup
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import feedparser
from  post_note import post_note
from get_notes import get_notes
from similarity_check import deduplicate_articles
import logging

logging.basicConfig(level=logging.INFO)

def fetch_feed(feed_url):
    # Parse the RSS feed
    feed = feedparser.parse(feed_url)
    return feed.entries

def extract_latest_headline(articles):
    # Extract the latest headline and its link
    latest_article = articles[0]
    headline = latest_article.title
    link = latest_article.link
    media_url = latest_article.media_content[0]['url'] if latest_article.media_content else None

    return headline, link, media_url

def main():
    feed_type = "NCAAMBB"
    feed_url = "https://api.foxsports.com/v2/content/optimized-rss?partnerKey=MB0Wehpmuj2lUhuRhQaafhBjAJqaPU244mlTDK1i&size=30&tags=fs/cbk"
    articles = fetch_feed(feed_url)
    headline, link, media_url = extract_latest_headline(articles)
    news = f"{headline}\n{link}\n{media_url}"

    prev_notes = get_notes(feed_type)
    is_duplicate = deduplicate_articles(news, prev_notes)
    if is_duplicate == False:
        post_note(news, feed_type)
        return news
    else:
        logging.info("Duplicate article found. Not posting to Nostr.")

if __name__ == "__main__":
    main()
