#!/usr/bin/env python3
import json
import random
from datetime import datetime

NEWS_FILE = '/root/guangchu/web/data/news.json'
HEADLINE_FILE = '/root/guangchu/web/data/headline.json'
OUTPUT_FILE = '/root/guangchu/web/data/toutiao-article.md'

def load_data():
    data = {}
    try:
        with open(NEWS_FILE, 'r', encoding='utf-8') as f:
            data['news'] = json.load(f)
    except:
        data['news'] = []
    
    try:
        with open(HEADLINE_FILE, 'r', encoding='utf-8') as f:
            data['headline'] = json.load(f)
    except:
        data['headline'] = None
    
    return data

def generate_content(data):
    content = []
    headline = data.get('headline')
    news = data.get('news', [])
    
    date_str = datetime.now().strftime('%Y年%m月%d日')
    
    content.append('# 光储每日要闻 ' + date_str + '\n')
    
    if headline:
        content.append('## 今日头条\n')
        content.append('**' + (headline.get('title_zh') or '') + '**\n')
        if headline.get('summary_zh'):
            content.append(headline.get('summary_zh') + '\n')
        content.append('来源: ' + (headline.get('source') or '') + '\n')
        content.append('\n---\n')
    
    content.append('## 行业动态\n')
    
    if news:
        for i, item in enumerate(news[:8], 1):
            title = item.get('title', item.get('title_en', ''))
            category = item.get('category', '综合')
            emoji_map = {'政策': '[政策]', '市场': '[市场]', '技术': '[技术]', '项目': '[项目]', '综合': ''}
            emoji = emoji_map.get(category, '')
            content.append(str(i) + '. ' + emoji + ' ' + title + '\n')
    
    content.append('\n---\n')
    content.append('## 趋势要点\n')
    content.append('- 储能市场持续增长\n')
    content.append('- 光伏装机规模稳步扩大\n')
    content.append('- 技术效率不断提升\n')
    
    content.append('\n---\n')
    content.append('关注光储龙虾，获取更多光储资讯\n')
    content.append('#光伏 #储能 #新能源')
    
    return ''.join(content)

def main():
    print('=== 光储头条图文生成器 ===')
    data = load_data()
    content = generate_content(data)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print('Generated: ' + OUTPUT_FILE)
    print(content[:300] + '...')

if __name__ == '__main__':
    main()
