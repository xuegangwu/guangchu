#!/usr/bin/env python3
"""
Guangchu - 生成每周报告
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict


def get_week_dates(date=None):
    """获取当前周的起止日期"""
    if date is None:
        date = datetime.now()
    # 本周一
    monday = date - timedelta(days=date.weekday())
    # 本周日
    sunday = monday + timedelta(days=6)
    return monday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d"), monday


def load_week_news(start_date, end_date):
    """加载一周内的所有新闻"""
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


def generate_weekly_report():
    start_date, end_date, week_start = get_week_dates()
    news = load_week_news(start_date, end_date)

    if not news:
        print(f"{start_date} 至 {end_date} 没有数据")
        return None

    # 统计
    by_region = defaultdict(list)
    by_type = defaultdict(list)
    by_source = defaultdict(int)

    for item in news:
        by_region[item["region"]].append(item)
        by_type[item["type"]].append(item)
        by_source[item["source"]] += 1

    # 生成报告
    report = []
    week_num = week_start.isocalendar()[1]
    report.append(f"# Guangchu周报 | 2026 年第 {week_num} 周\n")
    report.append(f"**统计周期：** {start_date} - {end_date}\n")
    report.append(f"**新闻总数：** {len(news)} 条\n")

    # 本周要点
    report.append("\n---\n")
    report.append("## 📌 本周要点\n")
    report.append("> 本周最重要的 5 条光储动态\n")

    # 简单选前 5 条（可以优化为重要性排序）
    top_news = news[:5]
    for i, item in enumerate(top_news, 1):
        report.append(f"{i}. **{item['type']}** [{item['region']}] {item['title']}")

    # 区域分析
    report.append("\n---\n")
    report.append("## 🌍 区域分析\n")

    region_order = ["Europe", "US", "Japan", "Southeast Asia", "Global"]
    for region in region_order:
        if region in by_region:
            items = by_region[region]
            report.append(f"\n### {region}（{len(items)} 条）\n")

            # 按类型分组
            type_groups = defaultdict(list)
            for item in items:
                type_groups[item["type"]].append(item)

            for type_name, type_items in type_groups.items():
                report.append(f"\n**{type_name}**\n")
                for item in type_items[:3]:  # 每类最多 3 条
                    report.append(f"- {item['title']}")

    # 类型分布
    report.append("\n---\n")
    report.append("## 📊 类型分布\n")
    report.append("| 类型 | 数量 | 占比 |\n|------|------|------|\n")
    for type_name, items in sorted(by_type.items(), key=lambda x: -len(x[1])):
        pct = len(items) / len(news) * 100
        report.append(f"| {type_name} | {len(items)} | {pct:.1f}% |")

    # 来源统计
    report.append("\n---\n")
    report.append("## 📰 来源统计\n")
    report.append("| 来源 | 数量 |\n|------|------|\n")
    for source, count in sorted(by_source.items(), key=lambda x: -x[1]):
        report.append(f"| {source} | {count} |")

    # 深度分析（可以后续扩展）
    report.append("\n---\n")
    report.append("## 🔍 本周观察\n")
    report.append("\n### 政策动向\n")
    policy_items = [item for item in news if item["type"] == "政策"]
    if policy_items:
        report.append(f"本周共 {len(policy_items)} 条政策相关新闻：\n")
        for item in policy_items[:3]:
            report.append(f"- **{item['region']}**: {item['title']}")
    else:
        report.append("本周无明显政策动向。")

    report.append("\n### 市场趋势\n")
    project_items = [item for item in news if item["type"] == "项目"]
    if project_items:
        report.append(f"本周共 {len(project_items)} 条项目相关新闻：\n")
        for item in project_items[:3]:
            report.append(f"- **{item['region']}**: {item['title']}")

    report.append("\n---\n")
    report.append(f"\n*Guangchu · 每周深度分析*\n")

    return "\n".join(report)


def main():
    report = generate_weekly_report()

    if report:
        output_dir = Path("/home/admin/openclaw/workspace/projects/guangchu/reports/weekly")
        output_dir.mkdir(exist_ok=True)

        week_num = datetime.now().isocalendar()[1]
        output_file = output_dir / f"2026-W{week_num}.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"周报生成完成：{output_file}")
        print("\n" + "=" * 50 + "\n")
        print(report[:1500])  # 打印前 1500 字预览


if __name__ == "__main__":
    main()
