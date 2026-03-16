#!/usr/bin/env python3
"""每日光储头条生成器"""
import json
import re
from datetime import datetime, timedelta
from collections import defaultdict

NEWS_FILE = '/root/guangchu/web/data/news.json'
HEADLINE_FILE = '/root/guangchu/web/data/headline.json'

# 来源权重
SOURCE_WEIGHTS = {
    "PV Magazine": 1.0,
    "Solar Power World": 0.9,
    "Energy Storage News": 0.95,
    "Greentech Media": 0.8,
    "CleanTechnica": 0.85,
    "Reuters": 1.0,
    "Energy Voice": 0.7
}

# 关键词权重
KEYWORD_WEIGHTS = {
    # 高权重 - 重大政策/投资
    "policy": 2.0, "government": 1.8, "subsidy": 1.8,
    "investment": 1.5, "billion": 1.5, "GW": 1.5,
    "auction": 1.5, "tender": 1.5,
    
    # 中权重 - 技术突破
    "breakthrough": 1.5, "record": 1.4, "efficiency": 1.3,
    "technology": 1.2, "innovation": 1.3,
    
    # 市场
    "market": 1.2, "growth": 1.2, "share": 1.1,
    "price": 1.1, "cost": 1.1,
    
    # 储能
    "battery": 1.3, "storage": 1.3, "capacity": 1.2,
    
    # 中国相关
    "China": 1.3, "Chinese": 1.3, "中国": 1.5
}

def parse_date(date_str):
    """解析各种日期格式"""
    try:
        # RFC 2822 format
        if 'GMT' in date_str or '+0000' in date_str:
            dt = datetime.strptime(date_str.replace('GMT', '+0000'), '%a, %d %b %Y %H:%M:%S %z')
            return dt
        # ISO format
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except:
        return datetime.now()

def calculate_score(news_item):
    """计算新闻权重分数"""
    title = news_item.get('title', '').lower()
    source = news_item.get('source', '')
    date_str = news_item.get('date', '')
    
    # 1. 来源权重
    source_score = SOURCE_WEIGHTS.get(source, 0.7)
    
    # 2. 关键词权重
    keyword_score = 1.0
    for keyword, weight in KEYWORD_WEIGHTS.items():
        if keyword.lower() in title:
            keyword_score *= weight
    
    # 3. 时间权重
    try:
        news_date = parse_date(date_str)
        hours_old = (datetime.now() - news_date.replace(tzinfo=None)).total_seconds() / 3600
        if hours_old < 24:
            time_score = 1.0
        elif hours_old < 48:
            time_score = 0.7
        elif hours_old < 72:
            time_score = 0.5
        else:
            time_score = 0.3
    except:
        time_score = 0.5
    
    # 4. 标题长度适中加分
    length = len(title)
    if 50 < length < 150:
        length_score = 1.1
    else:
        length_score = 1.0
    
    total_score = source_score * keyword_score * time_score * length_score
    return total_score

def generate_summary(title, max_length=120):
    """生成文章摘要"""
    # 移除括号内容
    title = re.sub(r'\([^)]*\)', '', title)
    title = re.sub(r'\[[^\]]*\]', '', title)
    title = title.strip()
    
    if len(title) <= max_length:
        return title
    
    # 在句号处截断
    sentences = title.split('.')
    summary = ''
    for s in sentences:
        if len(summary) + len(s) <= max_length:
            summary += s + '.'
        else:
            break
    
    return summary.strip() + '...'

def select_headline(news_list):
    """选择最佳头条"""
    if not news_list:
        return None
    
    # 计算所有新闻分数
    scored_news = []
    for news in news_list:
        score = calculate_score(news)
        scored_news.append((score, news))
    
    # 按分数排序
    scored_news.sort(key=lambda x: x[0], reverse=True)
    
    # 选择最高的
    top_news = scored_news[0][1]
    
    # 生成头条数据
    headline = {
        "id": top_news.get('id', 1),
        "title": top_news.get('title', ''),
        "summary": generate_summary(top_news.get('title', '')),
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
    print("=== 每日光储头条生成器 ===")
    
    # 读取新闻
    try:
        with open(NEWS_FILE, 'r', encoding='utf-8') as f:
            news_list = json.load(f)
    except Exception as e:
        print(f"Error reading news: {e}")
        return
    
    if not news_list:
        print("No news to process!")
        return
    
    # 选择头条
    headline = select_headline(news_list)
    
    if headline:
        # 保存头条
        with open(HEADLINE_FILE, 'w', encoding='utf-8') as f:
            json.dump(headline, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 今日头条生成成功!")
        print(f"标题: {headline['title'][:60]}...")
        print(f"来源: {headline['source']}")
        print(f"分数: {headline['score']}")
    else:
        print("Failed to generate headline!")

if __name__ == "__main__":
    main()
