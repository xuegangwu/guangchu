#!/usr/bin/env python3
"""光储新闻爬虫 v4 - 支持分类"""
import json
import re
import urllib.request
from datetime import datetime
import feedparser

NEWS_FILE = '/root/guangchu/web/data/news.json'

# 定义分类关键词
CATEGORIES = {
    '政策': ['policy', 'government', 'subsidy', '补贴', '政策', '政府', '招标', 'auction', 'tender'],
    '市场': ['market', 'growth', 'price', 'investment', 'billion', 'GW', '市场', '投资', '价格'],
    '技术': ['technology', 'efficiency', 'breakthrough', 'innovation', '技术', '效率', '突破', '电池', 'battery'],
    '项目': ['project', 'commissioning', 'factory', 'plant', '项目', '工厂', '电站', '装机']
}

SOURCES = [
    {"name": "PV Magazine", "url": "https://www.pv-magazine.com/feed/", "emoji": "☀️", "region": "Europe", "lang": "en"},
    {"name": "Solar Power World", "url": "https://www.solarpowerworldonline.com/feed/", "emoji": "⚡", "region": "US", "lang": "en"},
    {"name": "Energy Storage News", "url": "https://www.energy-storage.news/feed/", "emoji": "🔋", "region": "Global", "lang": "en"},
]

def get_category(title):
    """根据标题判断分类"""
    title_lower = title.lower()
    for cat, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw.lower() in title_lower:
                return cat
    return '综合'

def translate_simple(text):
    """简单翻译"""
    translations = {
        "Cambodia": "柬埔寨", "China": "中国", "US": "美国",
        "solar": "光伏", "PV": "光伏", "battery": "电池",
        "storage": "储能", "grid": "电网", "GW": "吉瓦",
        "project": "项目", "investment": "投资"
    }
    for eng, chi in translations.items():
        text = text.replace(eng, chi)
    return text

def fetch_feed(source, max_entries=5):
    try:
        feed = feedparser.parse(source['url'])
        items = []
        for entry in feed.entries[:max_entries]:
            title = entry.get('title', '').strip()
            if not title or title == ' ':
                continue
            
            # 自动分类
            category = get_category(title)
            
            items.append({
                "id": len(items) + 1,
                "title": title,
                "title_zh": translate_simple(title),
                "url": entry.get('link', '#'),
                "date": entry.get('published', datetime.now().isoformat()),
                "source": source['name'],
                "region": source['region'],
                "category": category,
                "emoji": source["emoji"]
            })
        return items
    except Exception as e:
        print(f"Error: {e}")
        return []

def main():
    print("=== 光储新闻 v4 (分类版) ===")
    all_news = []
    for src in SOURCES:
        news = fetch_feed(src)
        all_news.extend(news)
    
    # 按日期排序
    all_news.sort(key=lambda x: x['date'], reverse=True)
    
    # 保存
    with open(NEWS_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_news, f, ensure_ascii=False, indent=2)
    
    # 统计
    cats = {}
    for n in all_news:
        cats[n['category']] = cats.get(n['category'], 0) + 1
    
    print(f"获取 {len(all_news)} 条新闻")
    for cat, cnt in cats.items():
        print(f"  {cat}: {cnt}")

if __name__ == "__main__":
    main()
