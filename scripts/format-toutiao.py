#!/usr/bin/env python3
"""
光储龙虾 - 头条号格式化工具
去掉AI痕迹，优化为人工写作风格
"""

import json
from datetime import datetime
from pathlib import Path
import random

# 人工写作常用开头（随机使用）
OPENERS = [
    "今天光储圈有几件事值得关注。",
    "来看看今天全球光储市场发生了什么。",
    "今日光储动态整理如下。",
    "一天过去，光储行业又有新变化。",
    "今天的重点信息都在这了。",
]

# 人工常用过渡语
TRANSITIONS = [
    "再说回",
    "另外",
    "还有",
    "值得一提的是",
    "再看",
    "另一边",
]

# 去掉AI常用词
AI_PATTERNS = {
    "综上所述": "",
    "总之": "",
    "总的来说": "",
    "值得注意的是": "",
    "需要指出的是": "",
    "本文": "",
    "本报告": "",
    "生成时间": "",
}

def remove_ai痕迹(text):
    """去掉AI特征"""
    for pattern, replacement in AI_PATTERNS.items():
        text = text.replace(pattern, replacement)
    return text

def humanize_title(title):
    """标题人性化处理"""
    # 去掉过于正式的表述
    title = title.replace("launches", "推出")
    title = title.replace("announces", "宣布")
    title = title.replace("signs", "签署")
    title = title.replace("reports", "报告称")
    return title

def format_for_toutiao(report_type, date_str=None):
    """格式化为头条风格"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    if report_type == "daily":
        raw_file = Path(f"/home/admin/openclaw/workspace/projects/光储龙虾/raw/{date_str}.json")
        if not raw_file.exists():
            print(f"未找到 {date_str} 的数据")
            return None
        
        with open(raw_file, "r", encoding="utf-8") as f:
            news = json.load(f)
        
        # 头条风格：简短、直接、有重点
        content = []
        
        # 标题（吸引眼球但不过分）
        region_count = len(set(item["region"] for item in news))
        content.append(f"【光储龙虾日报】{date_str} | 全球{region_count}大区域光储动态速览\n")
        
        # 开头（随机选一个）
        content.append(random.choice(OPENERS) + "\n")
        
        # 重点新闻（3-5 条）
        content.append("━━━ 重点关注 ━━━\n\n")
        for i, item in enumerate(news[:5], 1):
            title = humanize_title(item["title"])
            content.append(f"{i}. {item['region']} | {title}\n")
        
        content.append("\n━━━ 区域详情 ━━━\n\n")
        
        # 按区域分组
        by_region = {}
        for item in news:
            region = item["region"]
            if region not in by_region:
                by_region[region] = []
            by_region[region].append(item)
        
        region_names = {
            "Europe": "🇪🇺 欧洲",
            "US": "🇺🇸 美国", 
            "Japan": "🇯🇵 日本",
            "Southeast Asia": "🌏 东南亚",
            "Global": "🌍 全球"
        }
        
        for region, items in by_region.items():
            name = region_names.get(region, region)
            content.append(f"【{name}】\n")
            for item in items[:3]:  # 每个区域最多 3 条
                title = humanize_title(item["title"])
                # 简短摘要（50 字以内）
                summary = item.get("summary", "")[:50] + "..." if len(item.get("summary", "")) > 50 else item.get("summary", "")
                content.append(f"• {title}\n")
                if summary:
                    content.append(f"  {summary}\n")
            content.append("\n")
        
        # 结尾（简单）
        content.append("━━━\n")
        content.append(f"共 {len(news)} 条动态 | 数据来自 PV Magazine、Energy Storage News 等\n")
        content.append("\n#光伏 #储能 #新能源 #海外市场\n")
        
        return "\n".join(content)
    
    return None

def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # 生成日报
    toutiao_content = format_for_toutiao("daily", date_str)
    
    if toutiao_content:
        output_dir = Path("/home/admin/openclaw/workspace/projects/光储龙虾/reports/toutiao")
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / f"{date_str}_头条.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(toutiao_content)
        
        print(f"头条格式完成：{output_file}")
        print("\n" + "="*50 + "\n")
        print(toutiao_content)

if __name__ == "__main__":
    main()
