#!/usr/bin/env python3
"""
Guangchu - 公众号日记导出工具
将项目日记转换为微信公众号格式，方便发布宣传
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict

# 配置
DIARY_DIR = Path("/home/admin/openclaw/workspace/projects/guangchu/diary")
EXPORT_DIR = Path("/home/admin/openclaw/workspace/projects/guangchu/export/wechat")

class WeChatDiaryExporter:
    """公众号日记导出器"""
    
    def __init__(self):
        self.today = datetime.now()
        self.date_str = self.today.strftime('%Y-%m-%d')
        self.chinese_date = self.today.strftime('%Y 年 %m 月 %d 日')
        self.weekday = self.today.strftime('%A')
    
    def get_diary_entries(self) -> List[Dict]:
        """获取今日日记条目"""
        # 这里可以从日记 HTML 或 JSON 中提取
        # 简化示例，实际应该解析日记文件
        entries = [
            {
                'emoji': '✨',
                'title': '社交媒体集成完成',
                'content': '成功实现 LinkedIn、Facebook、Twitter 三大社交媒体平台的数据抓取功能，支持多语言自动翻译和关键信息提取。',
                'category': '功能开发'
            },
            {
                'emoji': '⚙️',
                'title': '7 步数据处理管道上线',
                'content': '从原始数据到结构化数据，经过内容提取、质量过滤、多语言翻译、关键信息提取、智能摘要、情感分析、主题分类等 7 步处理流程。',
                'category': '技术架构'
            },
            {
                'emoji': '📄',
                'title': '项目详情页面发布',
                'content': '全新的项目介绍页面，包含数据源展示、技术架构图、技术特点、迭代路线图等丰富内容，全面展示项目实力。',
                'category': '页面优化'
            },
            {
                'emoji': '📊',
                'title': '信息源覆盖达 22 个',
                'content': '新增政府/能源局网站 7 个、电力相关 3 个、制造商 5 个、政策机构 3 个，信息覆盖更全面。',
                'category': '数据扩展'
            },
            {
                'emoji': '📔',
                'title': '项目日记系统上线',
                'content': '每天自动生成 5 条以内的精彩更新，图文并茂记录项目发展历程，作为永久历史档案保存。',
                'category': '系统建设'
            }
        ]
        return entries
    
    def generate_wechat_content(self, entries: List[Dict]) -> str:
        """生成公众号内容"""
        
        content = f"""
# 🦞 Guangchu研发日记 | {self.chinese_date}

> 记录项目发展的每一步，见证技术创新的力量

---

## 📋 今日概览

**日期**: {self.chinese_date} {self.weekday}  
**第 1 期** | Guangchu研发团队

---

"""
        
        # 添加条目
        for i, entry in enumerate(entries, 1):
            content += f"""
## {i}. {entry['emoji']} {entry['title']}

**分类**: {entry['category']}

{entry['content']}

---

"""
        
        # 添加项目统计
        content += """
## 📊 项目数据

| 指标 | 数值 | 说明 |
|------|------|------|
| **信息源** | 22 个 | 覆盖政府/媒体/制造商 |
| **支持语言** | 3 种 | 英文/中文/日文 |
| **省份数据** | 92 个 | 中国 30+ 越南 15+ 日本 47 |
| **自动化** | 100% | 全自动数据处理 |

---

## 🌟 今日亮点

1. **社交媒体集成** - 支持 LinkedIn/Facebook/Twitter 三大平台
2. **7 步数据处理** - 从原始数据到结构化数据的完整管道
3. **项目日记系统** - 每天记录项目发展历程

---

## 🚀 技术栈

- **后端**: Python 3.10+, Flask, SQLite FTS5
- **前端**: HTML5, CSS3, JavaScript
- **数据处理**: BeautifulSoup, Requests
- **翻译服务**: Google Translate API
- **版本控制**: Git, GitHub

---

## 📞 项目链接

- **GitHub**: https://github.com/xuegangwu/guangchu
- **Web 搜索**: http://localhost:5000
- **项目详情**: http://localhost:5000/project-intro.html
- **投资地图**: http://localhost:3000
- **项目日记**: http://localhost:5000/diary/

---

## 💡 关于我们

**Guangchu** 是一个自动化的光伏 + 储能行业信息收集与分析系统，支持多语言新闻抓取、智能数据处理、多语言翻译等功能。

我们的目标是帮助用户快速了解全球光储行业动态，识别优质投资机会，让数据驱动决策。

---

**欢迎关注我们，获取最新研发动态！** 🦞✨

*本文档由 OpenClaw 智能助手自动生成*
"""
        
        return content
    
    def generate_html_version(self, entries: List[Dict]) -> str:
        """生成 HTML 版本（适合 Cloud Hub）"""
        
        entries_html = ""
        for i, entry in enumerate(entries, 1):
            entries_html += f"""
            <div class="diary-item">
                <div class="item-header">
                    <span class="item-number">{i}</span>
                    <span class="item-emoji">{entry['emoji']}</span>
                    <h3 class="item-title">{entry['title']}</h3>
                </div>
                <div class="item-category">{entry['category']}</div>
                <p class="item-content">{entry['content']}</p>
            </div>
            """
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guangchu研发日记 | {self.chinese_date}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.7;
            color: #1d1d1f;
            background: #f5f5f7;
            padding: 20px;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            padding: 60px 20px;
            background: linear-gradient(135deg, #da251d, #ffcd3c);
            border-radius: 18px;
            color: white;
            margin-bottom: 30px;
        }}
        
        .header-logo {{
            font-size: 80px;
            margin-bottom: 20px;
        }}
        
        .header h1 {{
            font-size: 32px;
            margin-bottom: 10px;
        }}
        
        .header-date {{
            font-size: 16px;
            opacity: 0.9;
        }}
        
        .diary-card {{
            background: white;
            border-radius: 18px;
            padding: 40px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            margin-bottom: 30px;
        }}
        
        .diary-item {{
            padding: 24px;
            border-left: 4px solid #da251d;
            background: #f8f9fa;
            border-radius: 12px;
            margin-bottom: 24px;
        }}
        
        .item-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }}
        
        .item-number {{
            width: 32px;
            height: 32px;
            background: #da251d;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 16px;
        }}
        
        .item-emoji {{
            font-size: 28px;
        }}
        
        .item-title {{
            font-size: 18px;
            font-weight: 600;
            flex: 1;
        }}
        
        .item-category {{
            display: inline-block;
            padding: 4px 12px;
            background: #da251d;
            color: white;
            border-radius: 980px;
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 12px;
        }}
        
        .item-content {{
            font-size: 15px;
            line-height: 1.7;
            color: #666;
        }}
        
        .stats-section {{
            background: linear-gradient(135deg, #da251d, #ffcd3c);
            color: white;
            border-radius: 18px;
            padding: 30px;
            margin-top: 30px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-top: 20px;
        }}
        
        .stat-item {{
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
        }}
        
        .stat-label {{
            font-size: 13px;
            opacity: 0.9;
        }}
        
        .footer {{
            text-align: center;
            padding: 40px 20px;
            color: #666;
            font-size: 14px;
        }}
        
        .footer-links {{
            margin-top: 20px;
        }}
        
        .footer-links a {{
            color: #da251d;
            text-decoration: none;
            margin: 0 10px;
            font-weight: 600;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 24px;
            }}
            
            .diary-card {{
                padding: 24px;
            }}
            
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <div class="header-logo">🦞</div>
            <h1>Guangchu研发日记</h1>
            <p class="header-date">{self.chinese_date} {self.weekday} | 第 1 期</p>
        </div>
        
        <!-- Diary Content -->
        <div class="diary-card">
            <h2 style="margin-bottom: 30px;">📔 今日更新</h2>
            
            {entries_html}
        </div>
        
        <!-- Stats -->
        <div class="stats-section">
            <h2 style="margin-bottom: 20px;">📊 项目数据</h2>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-value">22</div>
                    <div class="stat-label">信息源</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">3</div>
                    <div class="stat-label">支持语言</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">92</div>
                    <div class="stat-label">省份数据</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">100%</div>
                    <div class="stat-label">自动化</div>
                </div>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p>© 2026 Guangchu - Solar-Storage News Collection & Analysis System</p>
            <div class="footer-links">
                <a href="/">返回首页</a>
                <a href="/diary/">项目日记</a>
                <a href="https://github.com/xuegangwu/guangchu" target="_blank">GitHub</a>
            </div>
        </div>
    </div>
</body>
</html>
"""
        
        return html
    
    def generate_github_readme(self, entries: List[Dict]) -> str:
        """生成 GitHub README 更新内容"""
        
        content = f"""# 🦞 Guangchu研发日记

> 记录项目发展的每一步，见证技术创新的力量

---

## 📅 最新日记

**{self.chinese_date}** | 第 1 期

"""
        
        # 添加条目
        for i, entry in enumerate(entries, 1):
            content += f"### {i}. {entry['emoji']} {entry['title']}\n\n{entry['content']}\n\n"
        
        content += f"""
---

## 📊 项目统计

| 指标 | 数值 |
|------|------|
| **信息源** | 22 个 |
| **支持语言** | 3 种 (英/中/日) |
| **省份数据** | 92 个 |
| **自动化** | 100% |

---

## 🔗 快速链接

- [查看今日日记](http://localhost:5000/diary/{self.date_str}.html)
- [项目详情](http://localhost:5000/project-intro.html)
- [Web 搜索](http://localhost:5000)
- [投资地图](http://localhost:3000)

---

## 📝 日记归档

所有历史日记都可以在 [项目日记索引](http://localhost:5000/diary/) 查看。

---

*本日记由 OpenClaw 智能助手自动生成*
"""
        
        return content
    
    def export_all(self):
        """导出所有格式"""
        print("=" * 60)
        print("📦 Guangchu - 公众号日记导出")
        print("=" * 60)
        
        # 获取日记条目
        entries = self.get_diary_entries()
        print(f"\n获取 {len(entries)} 条日记条目")
        
        # 创建导出目录
        EXPORT_DIR.mkdir(exist_ok=True)
        
        # 1. 导出公众号文本
        wechat_content = self.generate_wechat_content(entries)
        wechat_file = EXPORT_DIR / f"{self.date_str}-wechat.md"
        with open(wechat_file, 'w', encoding='utf-8') as f:
            f.write(wechat_content)
        print(f"✅ 公众号版本：{wechat_file}")
        
        # 2. 导出 HTML 版本（Cloud Hub）
        html_content = self.generate_html_version(entries)
        html_file = EXPORT_DIR / f"{self.date_str}-cloudhub.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ Cloud Hub 版本：{html_file}")
        
        # 3. 导出 GitHub README 更新
        readme_content = self.generate_github_readme(entries)
        readme_file = EXPORT_DIR / f"{self.date_str}-github-readme.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"✅ GitHub README 版本：{readme_file}")
        
        print("\n" + "=" * 60)
        print("✅ 导出完成！")
        print("=" * 60)
        print(f"\n导出目录：{EXPORT_DIR}")
        print("\n使用方式:")
        print("1. 公众号版本：复制到公众号编辑器")
        print("2. Cloud Hub 版本：上传到 Cloud Hub 主页")
        print("3. GitHub README：更新到 GitHub 仓库")
        
        return EXPORT_DIR


if __name__ == "__main__":
    exporter = WeChatDiaryExporter()
    exporter.export_all()
