#!/usr/bin/env python3
"""光储新闻爬虫 v3 - 支持多源RSS聚合"""
import json
import os
import sys
from datetime import datetime
import requests
import feedparser
import time

NEWS_FILE = '/root/guangchu/web/data/news.json'

SOURCES = [
    {
        "name": "PV Magazine",
        "url": "https://www.pv-magazine.com/feed/",
        "emoji": "☀️",
        "region": "Europe"
    },
    {
        "name": "Solar Power World",
        "url": "https://www.solarpowerworldonline.com/feed/",
        "emoji": "⚡",
        "region": "US"
    },
    {
        "name": "Energy Storage News",
        "url": "https://www.energy-storage.news/feed/",
        "emoji": "🔋",
        "region": "Global"
    },
    {
        "name": "Greentech Media",
        "url": "https://www.greentechmedia.com/rss.xml",
        "emoji": "🌱",
        "region": "US"
    }
]

def fetch_feed(source, max_entries=5):
    """获取RSS源"""
    try:
        print(f"Fetching {source['name']}...")
        feed = feedparser.parse(source['url'])
        items = []
        for entry in feed.entries[:max_entries]:
            # 提取日期
            date_str = entry.get('published', datetime.now().isoformat())
            # 提取链接
            url = entry.get('link', '#')
            # 清理标题
            title = entry.get('title', '').strip()
            
            if title and url:
                items.append({
                    "title": title,
                    "url": url,
                    "date": date_str,
                    "source": source['name'],
                    "region": source['region'],
                    "emoji": source["emoji"]
                })
        return items
    except Exception as e:
        print(f"Error fetching {source['name']}: {e}")
        return []

def fetch_all_news():
    """获取所有新闻源"""
    all_news = []
    for source in SOURCES:
        news = fetch_feed(source)
        all_news.extend(news)
        time.sleep(0.5)  # 避免请求过快
    
    # 按日期排序
    all_news.sort(key=lambda x: x['date'], reverse=True)
    
    # 返回前20条
    return all_news[:20]

def save_news(news):
    """保存到JSON文件"""
    with open(NEWS_FILE, 'w', encoding='utf-8') as f:
        json.dump(news, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(news)} news items to {NEWS_FILE}")

def main():
    print("=== 光储新闻爬虫 v3 ===")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    news = fetch_all_news()
    
    if news:
        save_news(news)
        print("\n=== Latest News ===")
        for i, n in enumerate(news[:5], 1):
            print(f"{i}. {n['title'][:50]}... [{n['source']}]")
    else:
        print("No news fetched!")

if __name__ == "__main__":
    main()
