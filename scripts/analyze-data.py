#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
光储龙虾 - 数据分析脚本
分析新闻趋势、热点统计、区域分布等
"""

import json
import os
from datetime import datetime
from collections import Counter

WORKDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(WORKDIR, 'raw')
STATS_DIR = os.path.join(WORKDIR, 'stats')

def load_news():
    """加载所有原始数据"""
    all_news = []
    for filename in os.listdir(RAW_DIR):
        if filename.endswith('.json'):
            filepath = os.path.join(RAW_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_news.extend(data)
    return all_news

def analyze_regions(news_list):
    """分析区域分布"""
    regions = [item.get('region', 'Unknown') for item in news_list]
    return Counter(regions)

def analyze_types(news_list):
    """分析类型分布"""
    types = [item.get('type', 'Other') for item in news_list]
    return Counter(types)

def analyze_sources(news_list):
    """分析来源分布"""
    sources = [item.get('source', 'Unknown') for item in news_list]
    return Counter(sources)

def analyze_keywords(news_list):
    """分析关键词频率"""
    keywords = []
    for item in news_list:
        if 'keywords' in item:
            keywords.extend(item['keywords'])
    return Counter(keywords).most_common(20)

def generate_report():
    """生成分析报告"""
    os.makedirs(STATS_DIR, exist_ok=True)
    
    news_list = load_news()
    print(f"📊 加载 {len(news_list)} 条新闻")
    
    # 区域分析
    region_stats = analyze_regions(news_list)
    
    # 类型分析
    type_stats = analyze_types(news_list)
    
    # 来源分析
    source_stats = analyze_sources(news_list)
    
    # 关键词分析
    keyword_stats = analyze_keywords(news_list)
    
    # 生成报告
    report = f"""# 📊 光储龙虾 - 数据分析报告

> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
> **数据总量**: {len(news_list)} 条新闻

---

## 🌍 区域分布

| 区域 | 数量 | 占比 |
|------|------|------|
"""
    
    for region, count in region_stats.most_common():
        percentage = (count / len(news_list)) * 100
        report += f"| {region} | {count} | {percentage:.1f}% |\n"
    
    report += f"""
## 📋 类型分布

| 类型 | 数量 | 占比 |
|------|------|------|
"""
    
    for type_, count in type_stats.most_common():
        percentage = (count / len(news_list)) * 100
        report += f"| {type_} | {count} | {percentage:.1f}% |\n"
    
    report += f"""
## 📰 来源分布（Top 10）

| 来源 | 数量 |
|------|------|
"""
    
    for source, count in source_stats.most_common(10):
        report += f"| {source} | {count} |\n"
    
    report += f"""
## 🔥 热门关键词（Top 20）

| 关键词 | 频次 |
|--------|------|
"""
    
    for keyword, count in keyword_stats:
        report += f"| {keyword} | {count} |\n"
    
    report += f"""
---

**报告生成完成** ✅
"""
    
    # 保存报告
    report_path = os.path.join(STATS_DIR, f'{datetime.now().strftime("%Y-%m-%d")}-analysis.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 报告已保存：{report_path}")
    return report_path

if __name__ == '__main__':
    generate_report()
