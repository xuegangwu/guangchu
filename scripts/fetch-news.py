#!/usr/bin/env python3
"""
光储龙虾 - 新闻抓取脚本
抓取全球光储政策、产品、项目信息
"""

import json
import os
from datetime import datetime
from pathlib import Path

# 信息源配置
SOURCES = {
    "PV Magazine": {
        "url": "https://www.pv-magazine.com/feed/",
        "type": "rss",
        "focus": ["policy", "products", "projects"]
    },
    "Energy Storage News": {
        "url": "https://www.energy-storage.news/feed",
        "type": "rss",
        "focus": ["storage", "policy", "projects"]
    },
    "IEA": {
        "url": "https://www.iea.org/news",
        "type": "web",
        "focus": ["policy", "data"]
    },
    "IRENA": {
        "url": "https://www.irena.org/news",
        "type": "web",
        "focus": ["policy", "reports"]
    }
}

# 区域关键词
REGIONS = {
    "Europe": ["Europe", "EU", "European", "Germany", "Spain", "France", "Italy", "Netherlands"],
    "US": ["US", "USA", "America", "California", "Texas", "United States"],
    "Japan": ["Japan", "Japanese", "Tokyo"],
    "Southeast Asia": ["Southeast Asia", "SEA", "Vietnam", "Thailand", "Indonesia", "Malaysia", "Philippines", "Singapore"]
}

def fetch_rss(url):
    """抓取 RSS 源"""
    import feedparser
    try:
        feed = feedparser.parse(url)
        items = []
        for entry in feed.entries[:10]:
            items.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.get("published", ""),
                "summary": entry.get("summary", "")[:200]
            })
        return items
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

def classify_region(title, summary):
    """判断新闻所属区域"""
    text = (title + " " + summary).lower()
    for region, keywords in REGIONS.items():
        for kw in keywords:
            if kw.lower() in text:
                return region
    return "Global"

def classify_type(title, summary):
    """判断新闻类型"""
    text = (title + " " + summary).lower()
    if any(kw in text for kw in ["policy", "regulation", "subsidy", "tariff", "government"]):
        return "政策"
    elif any(kw in text for kw in ["project", "installation", "capacity", "mw", "gw"]):
        return "项目"
    elif any(kw in text for kw in ["product", "launch", "price", "module", "inverter", "battery"]):
        return "产品"
    return "其他"

def main():
    output_dir = Path("/home/admin/openclaw/workspace/projects/光储龙虾/raw")
    output_dir.mkdir(exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    all_news = []
    
    print(f"开始抓取 {today} 的光储新闻...")
    
    # 抓取 RSS 源
    for name, config in SOURCES.items():
        if config["type"] == "rss":
            print(f"  抓取 {name}...")
            items = fetch_rss(config["url"])
            for item in items:
                item["source"] = name
                item["region"] = classify_region(item["title"], item["summary"])
                item["type"] = classify_type(item["title"], item["summary"])
                all_news.append(item)
    
    # 保存原始数据
    output_file = output_dir / f"{today}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_news, f, ensure_ascii=False, indent=2)
    
    print(f"抓取完成！共 {len(all_news)} 条新闻")
    print(f"保存到：{output_file}")
    
    # 按区域统计
    stats = {}
    for item in all_news:
        region = item["region"]
        stats[region] = stats.get(region, 0) + 1
    
    print("\n区域分布:")
    for region, count in sorted(stats.items(), key=lambda x: -x[1]):
        print(f"  {region}: {count} 条")

if __name__ == "__main__":
    main()
