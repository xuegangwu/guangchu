#!/usr/bin/env python3
"""
Guangchu - 生成每日短报
"""

import json
from datetime import datetime
from pathlib import Path

def generate_daily_report(date_str=None):
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    raw_file = Path(f"/home/admin/openclaw/workspace/projects/guangchu/raw/{date_str}.json")
    if not raw_file.exists():
        print(f"未找到 {date_str} 的原始数据，请先运行 fetch-news.py")
        return None
    
    with open(raw_file, "r", encoding="utf-8") as f:
        news = json.load(f)
    
    # 按区域分组
    by_region = {}
    for item in news:
        region = item["region"]
        if region not in by_region:
            by_region[region] = []
        by_region[region].append(item)
    
    # 生成报告
    report = []
    report.append(f"# Guangchu日报 | {date_str}\n")
    report.append("## 📌 今日要点\n")
    
    # 选最重要的 3 条作为要点
    top_news = news[:3] if len(news) >= 3 else news
    for item in top_news:
        report.append(f"- **{item['type']}** [{item['region']}] {item['title']}")
    
    report.append("\n---\n")
    report.append("## 🌍 区域动态\n")
    
    region_order = ["Europe", "US", "Japan", "Southeast Asia", "Global"]
    for region in region_order:
        if region in by_region:
            report.append(f"\n### {region}\n")
            for item in by_region[region][:5]:  # 每个区域最多 5 条
                report.append(f"- [{item['type']}] {item['title']}")
                report.append(f"  - {item['summary']}")
                report.append(f"  - 来源：{item['source']} [链接]({item['link']})\n")
    
    report.append("\n---\n")
    report.append("## 📈 价格速递\n")
    report.append("| 产品 | 价格 | 涨跌 |\n|------|------|------|\n")
    report.append("| 组件 | 待更新 | - |\n")
    report.append("| 储能系统 | 待更新 | - |\n")
    
    report.append("\n---\n")
    report.append(f"\n*Guangchu · 每日追踪全球光储动态*\n")
    
    return "\n".join(report)

def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    report = generate_daily_report(date_str)
    
    if report:
        output_dir = Path("/home/admin/openclaw/workspace/projects/guangchu/reports/daily")
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / f"{date_str}.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"日报生成完成：{output_file}")
        print("\n" + "="*50 + "\n")
        print(report[:1000])  # 打印前 1000 字预览

if __name__ == "__main__":
    main()
