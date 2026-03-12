#!/usr/bin/env python3
"""
Guangchu - 生成每月报告
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import calendar

def get_month_dates(date=None):
    """获取当前月的起止日期"""
    if date is None:
        date = datetime.now()
    year = date.year
    month = date.month
    first_day = datetime(year, month, 1)
    last_day = datetime(year, month, calendar.monthrange(year, month)[1])
    return first_day.strftime("%Y-%m-%d"), last_day.strftime("%Y-%m-%d"), year, month

def load_month_news(start_date, end_date):
    """加载一月内的所有新闻"""
    all_news = []
    raw_dir = Path("/home/admin/openclaw/workspace/projects/guangchu/raw")
    
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    current = start
    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        raw_file = raw_dir / f"{date_str}.json"
        if raw_file.exists():
            with open(raw_file, "r", encoding="utf-8") as f:
                day_news = json.load(f)
                all_news.extend(day_news)
        current += timedelta(days=1)
    
    return all_news

def generate_monthly_report():
    start_date, end_date, year, month = get_month_dates()
    news = load_month_news(start_date, end_date)
    
    if not news:
        print(f"{year}年{month}月 没有数据")
        return None
    
    # 统计
    by_region = defaultdict(list)
    by_type = defaultdict(list)
    by_source = defaultdict(int)
    by_date = defaultdict(list)
    
    for item in news:
        by_region[item["region"]].append(item)
        by_type[item["type"]].append(item)
        by_source[item["source"]] += 1
        # 提取日期
        if "published" in item and item["published"]:
            by_date[item["published"][:10]].append(item)
    
    # 生成报告
    report = []
    report.append(f"# Guangchu月报 | {year}年{month}月\n")
    report.append(f"**统计周期：** {start_date} - {end_date}\n")
    report.append(f"**新闻总数：** {len(news)} 条\n")
    report.append(f"**覆盖天数：** {len(by_date)} 天\n")
    
    # 本月要点
    report.append("\n---\n")
    report.append("## 📌 本月要点\n")
    report.append("> 本月最重要的 10 条光储动态\n")
    
    top_news = news[:10]
    for i, item in enumerate(top_news, 1):
        report.append(f"{i}. **{item['type']}** [{item['region']}] {item['title']}")
    
    # 区域深度分析
    report.append("\n---\n")
    report.append("## 🌍 区域深度分析\n")
    
    region_names = {
        "Europe": "🇪🇺 欧洲",
        "US": "🇺🇸 美国",
        "Japan": "🇯🇵 日本",
        "Southeast Asia": "🌏 东南亚",
        "Global": "🌍 全球"
    }
    
    region_order = ["Europe", "US", "Japan", "Southeast Asia", "Global"]
    for region in region_order:
        if region in by_region:
            items = by_region[region]
            name = region_names.get(region, region)
            report.append(f"\n### {name}（{len(items)} 条）\n")
            
            # 按类型分组
            type_groups = defaultdict(list)
            for item in items:
                type_groups[item["type"]].append(item)
            
            for type_name, type_items in sorted(type_groups.items(), key=lambda x: -len(x[1])):
                report.append(f"\n**{type_name}（{len(type_items)} 条）**\n")
                for item in type_items[:5]:  # 每类最多 5 条
                    report.append(f"- {item['title']}")
    
    # 类型分布
    report.append("\n---\n")
    report.append("## 📊 类型分布\n")
    report.append("| 类型 | 数量 | 占比 |\n|------|------|------|\n")
    for type_name, items in sorted(by_type.items(), key=lambda x: -len(x[1])):
        pct = len(items) / len(news) * 100
        bar = "█" * int(pct / 5)  # 简易条形图
        report.append(f"| {type_name} | {len(items)} | {pct:.1f}% {bar} |")
    
    # 来源统计
    report.append("\n---\n")
    report.append("## 📰 来源统计\n")
    report.append("| 来源 | 数量 | 占比 |\n|------|------|------|\n")
    for source, count in sorted(by_source.items(), key=lambda x: -x[1]):
        pct = count / len(news) * 100
        report.append(f"| {source} | {count} | {pct:.1f}% |")
    
    # 月度趋势分析
    report.append("\n---\n")
    report.append("## 📈 月度趋势分析\n")
    
    report.append("\n### 政策动向\n")
    policy_items = [item for item in news if item["type"] == "政策"]
    if policy_items:
        report.append(f"本月共 **{len(policy_items)}** 条政策相关新闻。\n")
        
        # 按区域分组
        policy_by_region = defaultdict(list)
        for item in policy_items:
            policy_by_region[item["region"]].append(item)
        
        for region, items in policy_by_region.items():
            report.append(f"\n**{region}** ({len(items)} 条)\n")
            for item in items[:3]:
                report.append(f"- {item['title']}")
    else:
        report.append("本月无明显政策动向。")
    
    report.append("\n### 项目动态\n")
    project_items = [item for item in news if item["type"] == "项目"]
    if project_items:
        report.append(f"本月共 **{len(project_items)}** 条项目相关新闻。\n")
        
        # 统计项目规模（尝试从标题中提取 MW/GW）
        large_projects = []
        for item in project_items:
            title = item["title"].lower()
            if "gw" in title or "mw" in title:
                large_projects.append(item)
        
        if large_projects:
            report.append(f"\n**大型项目（{len(large_projects)} 个）**\n")
            for item in large_projects[:5]:
                report.append(f"- {item['title']}")
    else:
        report.append("本月无明显项目动态。")
    
    report.append("\n### 产品与技术\n")
    product_items = [item for item in news if item["type"] == "产品"]
    if product_items:
        report.append(f"本月共 **{len(product_items)}** 条产品相关新闻。\n")
        for item in product_items[:5]:
            report.append(f"- {item['title']}")
    
    # 下周展望
    report.append("\n---\n")
    report.append("## 🔮 下月展望\n")
    report.append("\n基于本月动态，下月关注重点：\n")
    report.append("1. 持续关注欧美政策变化\n")
    report.append("2. 追踪大型项目进展\n")
    report.append("3. 关注新技术发布\n")
    
    report.append("\n---\n")
    report.append(f"\n*Guangchu · 月度综合报告*\n")
    report.append(f"\n*报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
    
    return "\n".join(report)

def main():
    report = generate_monthly_report()
    
    if report:
        output_dir = Path("/home/admin/openclaw/workspace/projects/guangchu/reports/monthly")
        output_dir.mkdir(exist_ok=True)
        
        year, month = datetime.now().year, datetime.now().month
        output_file = output_dir / f"{year}-{month:02d}.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"月报生成完成：{output_file}")
        print("\n" + "="*50 + "\n")
        print(report[:1500])  # 打印前 1500 字预览

if __name__ == "__main__":
    main()
