# crypto-news-aggregator-desktop

I needed a fast, zero-bloat way to track crypto news from my terminal without opening bloated websites or dealing with cookie banners. This tool pulls RSS feeds from major crypto outlets, scores them based on coin/topic keywords I care about, and lets me open them in my browser.

It saves read/unread state in a local SQLite database under your home directory.

## Installation

1. Clone this repository:
   ```cmd
   git clone https://github.com/yourusername/crypto-news-aggregator-desktop.git
   cd crypto-news-aggregator-desktop
   ```

2. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

## How to use

First, fetch the latest articles from all feeds:
```cmd
python aggregator.py sync
```

To view unread articles scored by relevance:
```cmd
python aggregator.py show --min-score 5
```

To read an article (this marks it as read and opens it in your default browser):
```cmd
python aggregator.py read <article_id>
```

To mark all current articles as read without opening them:
```cmd
python aggregator.py clear
```

## Customizing Keywords

You can tweak the scoring weights directly inside `aggregator.py` in the `KEYWORDS` dictionary.

<!-- checked: 2026-09-22 -->
