#!/usr/bin/env python3
"""每日光储头条生成器 v2 - 支持中英双语"""
import json
import re
import urllib.request
import urllib.parse
from datetime import datetime

NEWS_FILE = '/root/guangchu/web/data/news.json'
HEADLINE_FILE = '/root/guangchu/web/data/headline.json'

# 来源权重
SOURCE_WEIGHTS = {
    "PV Magazine": 1.0,
    "Solar Power World": 0.9,
    "Energy Storage News": 0.95,
    "Greentech Media": 0.8,
    "CleanTechnica": 0.85
}

# 关键词权重
KEYWORD_WEIGHTS = {
    "policy": 2.0, "government": 1.8, "subsidy": 1.8,
    "investment": 1.5, "billion": 1.5, "GW": 1.5,
    "auction": 1.5, "tender": 1.5,
    "breakthrough": 1.5, "record": 1.4, "efficiency": 1.3,
    "battery": 1.3, "storage": 1.3, "China": 1.3
}

# 简单翻译映射
TRANSLATION_DICT = {
    "Cambodia welcomes 'significant and historic achievement' of 1GWh grid-forming battery storage project": 
        "柬埔寨欢迎1GWh电网成型储能项目的重大历史性成就",
    "GW": "吉瓦",
    "MW": "兆瓦",
    "battery": "电池",
    "storage": "储能",
    "solar": "光伏",
    "photovoltaic": "光伏",
    "PV": "光伏",
    "grid": "电网",
    "energy": "能源",
    "power": "电力",
    "project": "项目",
    "investment": "投资",
    "market": "市场",
    "China": "中国",
    "US": "美国",
    "Europe": "欧洲",
    "India": "印度",
    "record": "创纪录",
    "growth": "增长",
    "new": "新建",
    "first": "首个",
    "largest": "最大",
    "announces": "宣布",
    "launches": "启动",
    "expands": "扩张",
    "commissioning": "投产",
    "factory": "工厂",
    "manufacturing": "制造",
    "capacity": "产能",
    "module": "组件",
    "panel": "面板"
}

def simple_translate(text):
    """简单翻译 - 基于词典和模式匹配"""
    result = text
    
    # 先替换常见词汇
    for eng, chi in TRANSLATION_DICT.items():
        result = result.replace(eng, chi)
    
    # 尝试调用免费翻译API
    try:
        url = f'https://api.mymemory.translated.net/get?q={urllib.parse.quote(text[:500])}&langpair=en|zh'
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            if data.get('responseStatus') == 200:
                translated = data.get('responseData', {}).get('translatedText', '')
                if translated and len(translated) > 10:
                    result = translated
    except Exception as e:
        print(f"Translation API error: {e}")
    
    return result

def calculate_score(news_item):
    title = news_item.get('title', '').lower()
    source = news_item.get('source', '')
    
    source_score = SOURCE_WEIGHTS.get(source, 0.7)
    keyword_score = 1.0
    for keyword, weight in KEYWORD_WEIGHTS.items():
        if keyword.lower() in title:
            keyword_score *= weight
    
    return source_score * keyword_score

def generate_summary(title, max_length=80):
    title = re.sub(r'\([^)]*\)', '', title)
    title = re.sub(r'\[[^\]]*\]', '', title)
    title = title.strip()
    if len(title) <= max_length:
        return title
    return title[:max_length] + '...'

def select_headline(news_list):
    if not news_list:
        return None
    
    scored_news = [(calculate_score(n), n) for n in news_list]
    scored_news.sort(key=lambda x: x[0], reverse=True)
    top_news = scored_news[0][1]
    
    # 翻译标题
    title_en = top_news.get('title', '')
    title_zh = simple_translate(title_en)
    summary_zh = simple_translate(generate_summary(title_en))
    
    headline = {
        "id": 1,
        "title_en": title_en,
        "title_zh": title_zh,
        "summary_en": generate_summary(title_en),
        "summary_zh": summary_zh,
        "url": top_news.get('url', '#'),
        "source": top_news.get('source', ''),
        "region": top_news.get('region', 'Global'),
        "emoji": top_news.get('emoji', '📰'),
        "date": top_news.get('date', ''),
        "score": round(scored_news[0][0], 2),
        "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return headline

def main():
    print("=== 每日光储头条生成器 v2 ===")
    
    try:
        with open(NEWS_FILE, 'r', encoding='utf-8') as f:
            news_list = json.load(f)
    except Exception as e:
        print(f"Error: {e}")
        return
    
    headline = select_headline(news_list)
    
    if headline:
        with open(HEADLINE_FILE, 'w', encoding='utf-8') as f:
            json.dump(headline, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 头条生成成功!")
        print(f"英文: {headline['title_en'][:50]}...")
        print(f"中文: {headline['title_zh'][:50]}...")
        print(f"来源: {headline['source']}")

if __name__ == "__main__":
    main()
