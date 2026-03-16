#!/usr/bin/env python3
"""
光储新闻爬虫 - 使用可访问的RSS源
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# RSS 源配置 (测试可访问)
SOURCES = {
    "Solar Magazine": {
        "url": "https://solarmagazine.com/feed",
        "type": "rss",
        "region": "Global",
    },
    "CleanTechnica": {
        "url": "https://cleantechnica.com/feed/",
        "type": "rss",
        "region": "Global",
    },
    "PV Magazine": {
        "url": "https://www.pv-magazine.com/feed/",
        "type": "rss",
        "region": "Europe",
    },
    "Solar Power World": {
        "url": "https://www.solarpowerworldonline.com/feed/",
        "type": "rss",
        "region": "US",
    },
}

REGIONS = {
    "Global": ["global", "world", "solar", "energy", "renewable"],
    "Europe": ["Europe", "EU", "Germany", "Spain", "France", "Italy"],
    "US": ["US", "USA", "America", "California", "Texas", "United States", "Canada"],
}

def fetch_rss(url, max_entries=10):
    import feedparser
    items = []
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries[:max_entries]:
            items.append({
                'title': entry.get('title', ''),
                'url': entry.get('link', ''),
                'date': entry.get('published', datetime.now().isoformat()),
                'source': feed.feed.get('title', 'Unknown'),
            })
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return items

def filter_by_region(items, region):
    """根据区域关键词过滤新闻"""
    if region == "Global":
        return items
    
    keywords = REGIONS.get(region, [])
    filtered = []
    for item in items:
        title = item.get('title', '').lower()
        for kw in keywords:
            if kw.lower() in title:
                filtered.append(item)
                break
    return filtered if filtered else items[:3]  # 如果过滤后为空，返回前3条

def main():
    print("🔍 开始抓取光储新闻...")
    
    all_news = []
    
    for source_name, config in SOURCES.items():
        print(f"📥 抓取: {source_name}...")
        url = config['url']
        region = config.get('region', 'Global')
        
        items = fetch_rss(url)
        items = filter_by_region(items, region)
        
        for item in items:
            item['region'] = region
            item['source_name'] = source_name
        
        all_news.extend(items)
        print(f"   ✓ 获取 {len(items)} 条")
    
    # 按日期排序
    all_news.sort(key=lambda x: x.get('date', ''), reverse=True)
    
    # 保存到文件
    output_dir = Path(__file__).parent.parent / "web" / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "news.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_news[:50], f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 完成! 共获取 {len(all_news)} 条新闻")
    print(f"📁 保存至: {output_file}")

if __name__ == "__main__":
    main()
