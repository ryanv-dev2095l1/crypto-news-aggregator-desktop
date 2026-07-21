import urllib.request
import urllib.error
import feedparser
import ssl
import socket
import re
from datetime import datetime
import time

# Some crypto news sites block Python-urllib default User-Agent immediately.
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

DEFAULT_FEEDS = {
    "coindesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "cointelegraph": "https://cointelegraph.com/rss",
    "bitcoin_magazine": "https://bitcoinmagazine.com/.rss/full/",
    "decrypt": "https://decrypt.co/feed",
    "blockworks": "https://blockworks.co/feed"
}

def fetch_feed_entries(feed_name, url, timeout=15):
    """Fetches and parses RSS feed items, returning normalized dicts."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    
    # Bypass SSL verification issues on outdated local Windows python environments.
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            raw_data = r.read()
            # print(f"Fetched {len(raw_data)} bytes from {feed_name}")
            parsed = feedparser.parse(raw_data)
    except (urllib.error.URLError, socket.timeout, Exception):
        # Keep going if one of the feeds is offline
        return []
    
    entries = []
    for item in parsed.entries:
        link = item.get("link", "").strip()
        if not link:
            continue
            
        title = item.get("title", "Untitled").strip()
        summary = item.get("summary", "").strip()
        
        # Decrypt/Blockworks keep heavy HTML formatting inside descriptions
        if "<" in summary:
            summary = re.sub(r'<[^>]+>', '', summary)
        
        # Resolve pub dates using feedparser internal structures
        pub_date = None
        if "published_parsed" in item and item.published_parsed:
            try:
                pub_date = datetime.fromtimestamp(time.mktime(item.published_parsed))
            except (ValueError, OverflowError):
                pass
        
        if not pub_date:
            pub_date = datetime.now()

        entries.append({
            "feed": feed_name,
            "title": title,
            "link": link,
            "published": pub_date,
            "summary": summary[:280] + "..." if len(summary) > 280 else summary
        })
        
    return entries
