#!/usr/bin/env python3
"""
Guangchu - 添加中文信息源
支持北极星储能网、索比光伏网等中文媒体
"""

import json
import re
from datetime import datetime
from pathlib import Path
import requests
from bs4 import BeautifulSoup

RAW_DIR = Path("/home/admin/openclaw/workspace/projects/guangchu/raw")

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
REGION_KEYWORDS = {
    "Europe": ["欧洲", "欧盟", "德国", "法国", "西班牙", "意大利", "荷兰"],
    "US": ["美国", "加州", "德州", "纽约"],
    "Japan": ["日本", "东京"],
    "China": ["中国", "国内", "国家能源局"],
    "Southeast Asia": ["东南亚", "越南", "泰国", "印尼", "马来西亚", "菲律宾"]
}

def classify_region_cn(title, summary):
    """判断中文新闻所属区域"""
    text = title + " " + (summary or "")
    
    # 先检查是否有明确区域
    for region, keywords in REGION_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return region
    
    # 默认返回 Global
    return "Global"

def classify_type_cn(title, summary):
    """判断中文新闻类型"""
    text = title + " " + (summary or "")
    
    if any(kw in text for kw in ["政策", "补贴", "规定", "标准", "规划", "意见"]):
        return "政策"
    elif any(kw in text for kw in ["项目", "签约", "中标", "开工", "并网", "投产"]):
        return "项目"
    elif any(kw in text for kw in ["产品", "发布", "价格", "组件", "逆变器", "电池", "系统"]):
        return "产品"
    return "其他"

def fetch_beixingchu(limit=10):
    """抓取北极星储能网"""
    items = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(
            "https://storage.bjx.com.cn/list/",
            headers=headers,
            timeout=30
        )
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找新闻列表（根据实际页面结构调整选择器）
        news_items = soup.select('.list_news_dl dt a')[:limit]
        
        for item in news_items:
            title = item.get('title', item.text.strip())
            link = item.get('href', '')
            
            if not link.startswith('http'):
                link = f"https://storage.bjx.com.cn{link}"
            
            # 提取摘要（尝试从标题推断）
            summary = title[:100]
            
            items.append({
                "title": title,
                "link": link,
                "published": datetime.now().isoformat(),
                "summary": summary,
                "source": "北极星储能网",
                "region": classify_region_cn(title, summary),
                "type": classify_type_cn(title, summary)
            })
        
        print(f"  北极星储能网：抓取 {len(items)} 条")
        
    except Exception as e:
        print(f"  北极星储能网抓取失败：{e}")
    
    return items

def fetch_suobi(limit=10):
    """抓取索比光伏网"""
    items = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(
            "https://solar.ofweek.com/news/list",
            headers=headers,
            timeout=30
        )
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找新闻列表（根据实际页面结构调整选择器）
        news_items = soup.select('.news-list h3 a')[:limit]
        
        for item in news_items:
            title = item.get('title', item.text.strip())
            link = item.get('href', '')
            
            if not link.startswith('http'):
                link = f"https://solar.ofweek.com{link}"
            
            summary = title[:100]
            
            items.append({
                "title": title,
                "link": link,
                "published": datetime.now().isoformat(),
                "summary": summary,
                "source": "索比光伏网",
                "region": classify_region_cn(title, summary),
                "type": classify_type_cn(title, summary)
            })
        
        print(f"  索比光伏网：抓取 {len(items)} 条")
        
    except Exception as e:
        print(f"  索比光伏网抓取失败：{e}")
    
    return items

def fetch_chinese_news():
    """抓取所有中文信息源"""
    all_items = []
    
    print("\n抓取中文信息源...")
    
    # 抓取北极星
    items = fetch_beixingchu(limit=10)
    all_items.extend(items)
    
    # 抓取索比
    items = fetch_suobi(limit=10)
    all_items.extend(items)
    
    print(f"中文信息源总计：{len(all_items)} 条")
    
    return all_items

def merge_with_existing(chinese_items):
    """与现有数据合并"""
    today = datetime.now().strftime("%Y-%m-%d")
    existing_file = RAW_DIR / f"{today}.json"
    
    # 读取现有数据
    existing_items = []
    if existing_file.exists():
        with open(existing_file, 'r', encoding='utf-8') as f:
            existing_items = json.load(f)
        print(f"读取现有数据：{len(existing_items)} 条")
    
    # 合并（去重）
    existing_links = {item['link'] for item in existing_items}
    new_items = [item for item in chinese_items if item['link'] not in existing_links]
    
    all_items = existing_items + new_items
    
    # 保存
    RAW_DIR.mkdir(exist_ok=True)
    with open(existing_file, 'w', encoding='utf-8') as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)
    
    print(f"保存合并后数据：{len(all_items)} 条（新增 {len(new_items)} 条）")
    print(f"文件：{existing_file}")
    
    return all_items

def main():
    print("=" * 60)
    print("Guangchu - 抓取中文信息源")
    print("=" * 60)
    
    # 抓取中文新闻
    chinese_items = fetch_chinese_news()
    
    if not chinese_items:
        print("\n⚠️ 未抓取到中文新闻，可能是网络问题或网站结构变化")
        return
    
    # 合并到现有数据
    all_items = merge_with_existing(chinese_items)
    
    # 统计
    stats = {}
    for item in all_items:
        source = item['source']
        stats[source] = stats.get(source, 0) + 1
    
    print("\n📊 来源统计:")
    for source, count in sorted(stats.items(), key=lambda x: -x[1]):
        print(f"   {source}: {count} 条")
    
    print("\n✅ 完成！")
    print("\n💡 提示：请运行 'python3 scripts/build-index.py' 更新搜索索引")

if __name__ == "__main__":
    main()
