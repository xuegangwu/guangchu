#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guangchu - 抓取中文信息源
支持北极星储能网、索比光伏网等中文媒体

v2.1 改进:
- 添加完善的错误处理
- 添加重试机制（指数退避）
- 添加日志记录
- 添加类型注解
- 添加配置管理
"""

import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.logger import logger, info, error, debug, warning
from scripts.config import get_config


# 配置
config = get_config()
RAW_DIR = Path(config.RAW_DIR)

# 中文信息源配置
CHINESE_SOURCES = {
    "北极星储能网": {
        "base_url": "https://storage.bjx.com.cn",
        "list_url": "https://storage.bjx.com.cn/list/",
        "type": "web_list"
    },
    "索比光伏网": {
        "base_url": "https://solar.ofweek.com",
        "list_url": "https://solar.ofweek.com/news/list",
        "type": "web_list"
    }
}

# 区域关键词（中文）
CHINESE_REGIONS = {
    "China": ["中国", "国内", "国家能源局", "国家发改委"],
    "Japan": ["日本", "东京", "大阪"],
    "Southeast Asia": ["东南亚", "越南", "泰国", "印尼"]
}


def fetch_with_retry(url: str, max_retries: int = 3, timeout: int = 30) -> Optional[requests.Response]:
    """
    带重试的 HTTP 请求
    
    Args:
        url: 请求 URL
        max_retries: 最大重试次数
        timeout: 超时时间（秒）
    
    Returns:
        Response 对象或 None
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for attempt in range(max_retries):
        try:
            debug(f"请求 URL: {url} (尝试 {attempt + 1}/{max_retries})")
            response = requests.get(url, headers=headers, timeout=timeout, verify=True)
            response.raise_for_status()
            response.encoding = 'utf-8'
            debug(f"请求成功：{url}, 状态码：{response.status_code}")
            return response
            
        except requests.exceptions.Timeout as e:
            error(f"请求超时：{url} (尝试 {attempt + 1}/{max_retries})")
        except requests.exceptions.ConnectionError as e:
            error(f"连接错误：{url} (尝试 {attempt + 1}/{max_retries}) - {str(e)[:100]}")
        except requests.exceptions.HTTPError as e:
            error(f"HTTP 错误：{url} - 状态码 {response.status_code}")
        except Exception as e:
            error(f"请求失败：{url} - {str(e)[:100]}")
        
        if attempt < max_retries - 1:
            wait_time = 2 ** attempt  # 指数退避
            warning(f"等待 {wait_time} 秒后重试...")
            time.sleep(wait_time)
    
    error(f"请求最终失败：{url}")
    return None


def classify_region(title: str, summary: str = "") -> str:
    """
    判断新闻所属区域
    
    Args:
        title: 新闻标题
        summary: 新闻摘要
    
    Returns:
        区域名称
    """
    text = f"{title} {summary}"
    
    for region, keywords in CHINESE_REGIONS.items():
        if any(keyword in text for keyword in keywords):
            return region
    
    return "China"  # 默认归为中国新闻


def fetch_chinese_news() -> List[Dict]:
    """
    抓取中文新闻
    
    Returns:
        新闻列表
    """
    all_news = []
    
    for source_name, source_config in CHINESE_SOURCES.items():
        try:
            info(f"开始抓取：{source_name}")
            
            response = fetch_with_retry(
                source_config['list_url'],
                max_retries=config.MAX_RETRIES,
                timeout=config.REQUEST_TIMEOUT
            )
            
            if not response:
                warning(f"跳过 {source_name}，无法访问")
                continue
            
            soup = BeautifulSoup(response.text, 'html.parser')
            items = []
            
            # 根据不同网站结构解析
            if source_name == "北极星储能网":
                news_items = soup.select('li.dianxin-li')
                for item in news_items[:10]:
                    try:
                        title_elem = item.select_one('a')
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            link = title_elem.get('href', '')
                            if link and not link.startswith('http'):
                                link = source_config['base_url'] + link
                            
                            date_elem = item.select_one('span')
                            date = date_elem.get_text(strip=True) if date_elem else datetime.now().isoformat()
                            
                            if title:
                                items.append({
                                    'title': title,
                                    'url': link,
                                    'date': date,
                                    'source': source_name,
                                    'type': 'policy',
                                    'region': classify_region(title),
                                    'language': 'zh'
                                })
                    except Exception as e:
                        error(f"解析条目失败：{str(e)}")
                        continue
            
            elif source_name == "索比光伏网":
                news_items = soup.select('li.news-item')
                for item in news_items[:10]:
                    try:
                        title_elem = item.select_one('a')
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            link = title_elem.get('href', '')
                            if link and not link.startswith('http'):
                                link = source_config['base_url'] + link
                            
                            items.append({
                                'title': title,
                                'url': link,
                                'date': datetime.now().isoformat(),
                                'source': source_name,
                                'type': 'policy',
                                'region': classify_region(title),
                                'language': 'zh'
                            })
                    except Exception as e:
                        error(f"解析条目失败：{str(e)}")
                        continue
            
            info(f"✅ {source_name}: 抓取 {len(items)} 条新闻")
            all_news.extend(items)
            
        except Exception as e:
            error(f"抓取 {source_name} 失败：{str(e)}")
            continue
    
    return all_news


def save_news(news_list: List[Dict], date: str) -> str:
    """
    保存新闻到文件
    
    Args:
        news_list: 新闻列表
        date: 日期字符串
    
    Returns:
        保存的文件路径
    """
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    
    filename = f"{date}-chinese.json"
    filepath = RAW_DIR / filename
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(news_list, f, ensure_ascii=False, indent=2)
        
        info(f"✅ 已保存到：{filepath}")
        return str(filepath)
        
    except Exception as e:
        error(f"保存文件失败：{str(e)}")
        raise


def main():
    """主函数"""
    import time as time_module
    
    start_time = time_module.time()
    
    try:
        info("=" * 60)
        info("Guangchu - 抓取中文信息源")
        info("=" * 60)
        info(f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        info(f"配置：超时={config.REQUEST_TIMEOUT}秒，重试={config.MAX_RETRIES}次")
        
        # 抓取新闻
        news_list = fetch_chinese_news()
        
        # 统计
        today = datetime.now().strftime('%Y-%m-%d')
        
        if news_list:
            # 保存数据
            filepath = save_news(news_list, today)
            
            # 统计信息
            regions = {}
            for news in news_list:
                region = news.get('region', 'Unknown')
                regions[region] = regions.get(region, 0) + 1
            
            info("\n区域分布:")
            for region, count in sorted(regions.items(), key=lambda x: x[1], reverse=True):
                info(f"  {region}: {count} 条")
            
            info(f"\n中文信息源总计：{len(news_list)} 条")
        else:
            warning("\n⚠️ 未抓取到中文新闻")
            warning("建议:")
            warning("  1. 检查网络连接")
            warning("  2. 使用代理服务器")
            warning("  3. 稍后重试")
        
        # 执行时间
        elapsed = time_module.time() - start_time
        info(f"\n执行时间：{elapsed:.2f}秒")
        info("=" * 60)
        
    except Exception as e:
        error(f"程序执行失败：{str(e)}")
        import traceback
        error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    main()
