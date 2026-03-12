#!/usr/bin/env python3
"""
光储龙虾 - 统计每日 token 消耗
"""

import json
from datetime import datetime
from pathlib import Path
import os

def estimate_tokens(text):
    """估算 token 数（中文约 1.5 字符/token，英文约 4 字符/token）"""
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    english_chars = sum(1 for c in text if c.isascii() and c.isalpha())
    # 粗略估算
    tokens = chinese_chars * 0.6 + english_chars * 0.25
    return int(tokens)

def count_daily_tokens(date_str=None):
    """统计某一天的 token 消耗"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    stats = {
        "date": date_str,
        "news_count": 0,
        "news_tokens": 0,
        "daily_report_tokens": 0,
        "total_tokens": 0
    }
    
    # 统计原始新闻
    raw_file = Path(f"/home/admin/openclaw/workspace/projects/光储龙虾/raw/{date_str}.json")
    if raw_file.exists():
        with open(raw_file, "r", encoding="utf-8") as f:
            news = json.load(f)
        stats["news_count"] = len(news)
        for item in news:
            stats["news_tokens"] += estimate_tokens(item.get("title", "") + item.get("summary", ""))
    
    # 统计日报
    daily_file = Path(f"/home/admin/openclaw/workspace/projects/光储龙虾/reports/daily/{date_str}.md")
    if daily_file.exists():
        with open(daily_file, "r", encoding="utf-8") as f:
            content = f.read()
        stats["daily_report_tokens"] = estimate_tokens(content)
    
    # 统计头条格式
    toutiao_file = Path(f"/home/admin/openclaw/workspace/projects/光储龙虾/reports/toutiao/{date_str}_头条.md")
    if toutiao_file.exists():
        with open(toutiao_file, "r", encoding="utf-8") as f:
            content = f.read()
        stats["daily_report_tokens"] += estimate_tokens(content)
    
    stats["total_tokens"] = stats["news_tokens"] + stats["daily_report_tokens"]
    
    return stats

def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    stats = count_daily_tokens(date_str)
    
    # 保存到 stats 目录
    stats_dir = Path("/home/admin/openclaw/workspace/projects/光储龙虾/stats")
    stats_dir.mkdir(exist_ok=True)
    
    # 追加到月度统计文件
    month = date_str[:7]  # YYYY-MM
    stats_file = stats_dir / f"{month}.jsonl"
    
    with open(stats_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(stats, ensure_ascii=False) + "\n")
    
    # 打印结果
    print(f"📊 光储龙虾 Token 统计 | {date_str}")
    print("=" * 40)
    print(f"📰 抓取新闻：{stats['news_count']} 条")
    print(f"📝 新闻处理：~{stats['news_tokens']:,} tokens")
    print(f"📄 日报生成：~{stats['daily_report_tokens']:,} tokens")
    print(f"📈 总计：~{stats['total_tokens']:,} tokens")
    print("=" * 40)
    print(f"💰 估算成本：${stats['total_tokens'] * 0.000002:.4f} (按 $0.002/1K tokens)")
    print(f"\n统计已保存到：{stats_file}")

if __name__ == "__main__":
    main()
