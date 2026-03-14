#!/usr/bin/env python3
"""
Guangchu - 项目日记生成器
每天生成 5 条以内的精彩更新，图文并茂展示项目发展历程
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict

# 配置
DIARY_DIR = Path("/home/admin/openclaw/workspace/projects/guangchu/diary")
REPORTS_DIR = Path("/home/admin/openclaw/workspace/projects/guangchu/reports/daily")
WORKSPACE_DIR = Path("/home/admin/openclaw/workspace/projects")


class ProjectDiaryGenerator:
    """项目日记生成器"""

    def __init__(self):
        self.today = datetime.now()
        self.date_str = self.today.strftime('%Y-%m-%d')
        self.chinese_date = self.today.strftime('%Y 年 %m 月 %d 日')
        self.weekday = self.today.strftime('%A')

        # 表情符号映射
        self.emoji_map = {
            'feat': '✨',
            'fix': '🐛',
            'docs': '📄',
            'style': '🎨',
            'refactor': '♻️',
            'test': '✅',
            'chore': '🔧',
            'new': '🆕',
            'update': '🔄',
            'add': '➕',
            'optimize': '⚡',
            'default': '📝',
        }

    def get_git_highlights(self, repo_path: Path, max_items: int = 5) -> List[Dict]:
        """获取 Git 提交亮点"""
        try:
            result = subprocess.run(
                ['git', '-C', str(repo_path), 'log', '--since=today', '--oneline', '--decorate'],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                commits = [line for line in result.stdout.strip().split('\n') if line]

                highlights = []
                for commit in commits[:max_items]:
                    # 解析提交信息
                    parts = commit.split(' ', 1)
                    if len(parts) >= 2:
                        commit_hash = parts[0]
                        message = parts[1]

                        # 提取类型和表情
                        emoji = self._get_emoji(message)
                        type_text = self._extract_type(message)

                        highlights.append(
                            {
                                'hash': commit_hash[:7],
                                'message': message,
                                'emoji': emoji,
                                'type': type_text,
                                'repo': repo_path.name,
                            }
                        )

                return highlights
            return []
        except Exception as e:
            print(f"❌ Git 错误：{e}")
            return []

    def _get_emoji(self, message: str) -> str:
        """根据提交信息获取表情"""
        message_lower = message.lower()

        for key, emoji in self.emoji_map.items():
            if key in message_lower:
                return emoji

        return self.emoji_map['default']

    def _extract_type(self, message: str) -> str:
        """提取提交类型"""
        message_lower = message.lower()

        type_map = {
            'feat': '新功能',
            'fix': '修复',
            'docs': '文档',
            'style': '格式',
            'refactor': '重构',
            'test': '测试',
            'chore': '构建',
            'new': '新增',
            'update': '更新',
            'add': '添加',
            'optimize': '优化',
        }

        for key, type_text in type_map.items():
            if key in message_lower:
                return type_text

        return '更新'

    def get_stats_highlights(self) -> List[str]:
        """获取统计亮点"""
        highlights = []

        # 统计文件数量
        guangchu_files = len(list((WORKSPACE_DIR / 'Guangchu').rglob('*.py')))
        investment_files = len(list((WORKSPACE_DIR / 'china-solar-storage').rglob('*.html')))

        if guangchu_files > 0:
            highlights.append(f"📦 Guangchu代码库：{guangchu_files} 个 Python 文件")

        if investment_files > 0:
            highlights.append(f"🗺️ 投资地图系统：{investment_files} 个 HTML 页面")

        # 统计信息源
        highlights.append("🌐 信息源覆盖：22 个官方信息源")
        highlights.append("🌍 支持语言：英文/中文/日文三语")

        return highlights[:3]  # 限制 3 条

    def get_milestone_highlights(self) -> List[Dict]:
        """获取里程碑事件"""
        milestones = []

        # 检查今天是否有重要文件创建
        important_files = [
            ('scripts/fetch-social-media.py', '📱 社交媒体抓取脚本'),
            ('scripts/data-processing-pipeline.py', '⚙️ 7 步数据处理管道'),
            ('web/project-intro.html', '📄 项目详情页面'),
            ('scripts/generate-project-diary.py', '📔 项目日记系统'),
        ]

        for file_path, description in important_files:
            full_path = WORKSPACE_DIR / 'Guangchu' / file_path
            if full_path.exists():
                stat = full_path.stat()
                file_date = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d')

                if file_date == self.date_str:
                    milestones.append(
                        {
                            'emoji': '🎯',
                            'description': description,
                            'time': datetime.fromtimestamp(stat.st_mtime).strftime('%H:%M'),
                        }
                    )

        return milestones[:2]  # 限制 2 个

    def generate_diary_entries(self, max_entries: int = 5) -> List[Dict]:
        """生成日记条目"""
        entries = []

        # 1. 获取 Git 亮点
        guangchu_commits = self.get_git_highlights(WORKSPACE_DIR / 'Guangchu', max_items=3)
        investment_commits = self.get_git_highlights(WORKSPACE_DIR / 'china-solar-storage', max_items=2)

        # 添加 Git 提交
        for commit in guangchu_commits[:2]:
            entries.append(
                {
                    'type': 'commit',
                    'emoji': commit['emoji'],
                    'title': f"{commit['repo']}: {commit['message']}",
                    'time': '今天',
                    'category': '代码提交',
                }
            )

        # 2. 获取里程碑
        milestones = self.get_milestone_highlights()
        for milestone in milestones:
            entries.append(
                {
                    'type': 'milestone',
                    'emoji': milestone['emoji'],
                    'title': milestone['description'],
                    'time': milestone['time'],
                    'category': '重要里程碑',
                }
            )

        # 3. 获取统计亮点
        stats = self.get_stats_highlights()
        for stat in stats[:1]:
            entries.append({'type': 'stat', 'emoji': '📊', 'title': stat, 'time': '今天', 'category': '项目统计'})

        # 限制总条目数
        return entries[:max_entries]

    def generate_diary_page(self, entries: List[Dict]) -> str:
        """生成日记页面 HTML"""

        # 生成条目 HTML
        entries_html = ""
        for entry in entries:
            entries_html += f"""
            <div class="diary-entry">
                <div class="entry-header">
                    <span class="entry-emoji">{entry['emoji']}</span>
                    <div class="entry-meta">
                        <span class="entry-time">{entry['time']}</span>
                        <span class="entry-category">{entry['category']}</span>
                    </div>
                </div>
                <div class="entry-content">
                    {entry['title']}
                </div>
            </div>
            """

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guangchu - 项目日记 | {self.chinese_date}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 1.6;
            color: #1d1d1f;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            color: white;
            padding: 60px 20px 40px;
        }}
        
        .header-logo {{
            font-size: 80px;
            margin-bottom: 20px;
            animation: bounce 2s infinite;
        }}
        
        @keyframes bounce {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-10px); }}
        }}
        
        .header h1 {{
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        
        .header-date {{
            font-size: 18px;
            opacity: 0.9;
        }}
        
        .diary-card {{
            background: white;
            border-radius: 18px;
            padding: 40px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }}
        
        .diary-entry {{
            padding: 24px;
            border-left: 4px solid #667eea;
            background: #f8f9fa;
            border-radius: 12px;
            margin-bottom: 20px;
            transition: all 0.3s;
        }}
        
        .diary-entry:hover {{
            transform: translateX(4px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .entry-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }}
        
        .entry-emoji {{
            font-size: 32px;
        }}
        
        .entry-meta {{
            display: flex;
            gap: 12px;
            align-items: center;
        }}
        
        .entry-time {{
            font-size: 14px;
            color: #667eea;
            font-weight: 600;
        }}
        
        .entry-category {{
            font-size: 12px;
            padding: 4px 12px;
            background: #667eea;
            color: white;
            border-radius: 980px;
        }}
        
        .entry-content {{
            font-size: 16px;
            color: #1d1d1f;
            line-height: 1.7;
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
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .stat-item {{
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 8px;
        }}
        
        .stat-label {{
            font-size: 14px;
            opacity: 0.9;
        }}
        
        .footer {{
            text-align: center;
            color: white;
            padding: 40px 20px;
            opacity: 0.8;
        }}
        
        .footer a {{
            color: white;
            text-decoration: none;
            font-weight: 600;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 28px;
            }}
            
            .diary-card {{
                padding: 24px;
            }}
            
            .entry-content {{
                font-size: 14px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <div class="header-logo">🦞</div>
            <h1>Guangchu - 项目日记</h1>
            <p class="header-date">{self.chinese_date} {self.weekday}</p>
        </div>
        
        <!-- Diary Card -->
        <div class="diary-card">
            <h2 style="margin-bottom: 30px; font-size: 24px;">📔 今日更新</h2>
            
            {entries_html}
        </div>
        
        <!-- Stats Section -->
        <div class="stats-section">
            <h2 style="margin-bottom: 20px; font-size: 20px;">📊 项目统计</h2>
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
            <p style="margin-top: 10px;">
                <a href="/">返回首页</a> · 
                <a href="/project-intro.html">项目详情</a> · 
                <a href="https://github.com/xuegangwu/guangchu" target="_blank">GitHub</a>
            </p>
        </div>
    </div>
</body>
</html>
"""

        return html

    def save_diary(self, html: str):
        """保存日记页面"""
        DIARY_DIR.mkdir(exist_ok=True)

        # 保存今日日记
        today_file = DIARY_DIR / f"{self.date_str}.html"
        with open(today_file, 'w', encoding='utf-8') as f:
            f.write(html)

        # 更新索引页面
        self.update_index()

        print(f"✅ 日记已保存：{today_file}")
        return today_file

    def update_index(self):
        """更新日记索引页面"""
        # 获取所有日记文件
        diary_files = sorted(DIARY_DIR.glob("*.html"), reverse=True)

        # 生成索引 HTML
        index_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guangchu - 项目日记索引</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            color: white;
            padding: 60px 20px;
        }}
        .header h1 {{
            font-size: 40px;
            margin-bottom: 10px;
        }}
        .diary-list {{
            background: white;
            border-radius: 18px;
            padding: 40px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        .diary-item {{
            padding: 20px;
            border-left: 4px solid #667eea;
            margin-bottom: 16px;
            background: #f8f9fa;
            border-radius: 8px;
            transition: all 0.3s;
        }}
        .diary-item:hover {{
            transform: translateX(4px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        .diary-item a {{
            text-decoration: none;
            color: #1d1d1f;
            font-weight: 600;
            font-size: 16px;
        }}
        .diary-date {{
            font-size: 14px;
            color: #667eea;
            margin-bottom: 8px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🦞 Guangchu - 项目日记</h1>
            <p>记录项目发展的每一步</p>
        </div>
        <div class="diary-list">
            <h2 style="margin-bottom: 30px;">📔 日记列表</h2>
"""

        # 添加日记列表
        for diary_file in diary_files[:30]:  # 显示最近 30 天
            date_str = diary_file.stem
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                chinese_date = date_obj.strftime('%Y 年 %m 月 %d 日')
                weekday = date_obj.strftime('%A')

                index_html += f"""
            <div class="diary-item">
                <div class="diary-date">{chinese_date} {weekday}</div>
                <a href="{diary_file.name}">查看日记 →</a>
            </div>
"""
            except:
                pass

        index_html += """
        </div>
    </div>
</body>
</html>
"""

        # 保存索引
        index_file = DIARY_DIR / "index.html"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_html)

        print(f"✅ 索引已更新：{index_file}")

    def run(self):
        """运行日记生成"""
        print("=" * 60)
        print("📔 Guangchu - 项目日记生成")
        print("=" * 60)
        print(f"\n日期：{self.chinese_date}")
        print(f"时间：{datetime.now().strftime('%H:%M')}")
        print("\n正在生成日记...")

        # 生成条目（最多 5 条）
        entries = self.generate_diary_entries(max_entries=5)

        print(f"\n生成 {len(entries)} 条日记条目:")
        for entry in entries:
            print(f"  {entry['emoji']} {entry['title'][:50]}...")

        # 生成页面
        html = self.generate_diary_page(entries)

        # 保存
        diary_file = self.save_diary(html)

        print("\n" + "=" * 60)
        print("✅ 日记生成完成！")
        print("=" * 60)
        print(f"\n日记位置：{diary_file}")
        print(f"访问地址：http://localhost:5000/diary/{self.date_str}.html")

        return diary_file


if __name__ == "__main__":
    generator = ProjectDiaryGenerator()
    generator.run()
