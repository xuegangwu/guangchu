#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
光储龙虾 - 抓取中文信息源
增加重试机制和更好的错误处理
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

WORKDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(WORKDIR, 'raw')

def fetch_with_retry(url, headers, max_retries=3):
    """带重试的请求"""
    for i in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=30, verify=True)
            if response.status_code == 200:
                return response
            print(f"  第{i+1}次尝试失败，状态码：{response.status_code}")
        except Exception as e:
            print(f"  第{i+1}次尝试失败：{str(e)[:50]}")
        if i < max_retries - 1:
            import time
            time.sleep(2)
    return None

def fetch_chinese_news():
    """抓取中文新闻"""
    os.makedirs(RAW_DIR, exist_ok=True)
    today = datetime.now().strftime('%Y-%m-%d')
    
    print("=" * 60)
    print("Guangchu - 抓取中文信息源")
    print("=" * 60)
    print("\n抓取中文信息源...\n")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    all_news = []
    
    # 北极星储能网
    try:
        url = 'https://storage.bjx.com.cn/list/'
        response = fetch_with_retry(url, headers)
        if response:
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            # 解析逻辑...
            print(f"  北极星储能网：抓取成功")
    except Exception as e:
        print(f"  北极星储能网抓取失败：{str(e)[:100]}")
    
    # 索比光伏网
    try:
        url = 'https://guangfu.bjx.com.cn/'
        response = fetch_with_retry(url, headers)
        if response:
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            print(f"  索比光伏网：抓取成功")
    except Exception as e:
        print(f"  索比光伏网抓取失败：{str(e)[:100]}")
    
    print(f"\n中文信息源总计：{len(all_news)} 条")
    
    if len(all_news) == 0:
        print("\n⚠️ 未抓取到中文新闻，可能是网络问题或网站结构变化")
        print("建议：")
        print("  1. 检查网络连接")
        print("  2. 使用代理服务器")
        print("  3. 稍后重试")
    else:
        # 保存数据
        filepath = os.path.join(RAW_DIR, f'{today}-chinese.json')
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(all_news, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 已保存到：{filepath}")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    fetch_chinese_news()
