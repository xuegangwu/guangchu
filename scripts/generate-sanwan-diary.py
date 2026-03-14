#!/usr/bin/env python3
"""
Guangchu - 参考 sanwan.ai 风格日记生成器
参考傅盛 3 万龙虾养成记的页面风格：
- 极简设计
- 时间线清晰
- 数据可视化
- 真实记录
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict

# 配置
DIARY_DIR = Path("/home/admin/openclaw/workspace/projects/guangchu/diary")
WORKSPACE_DIR = Path("/home/admin/openclaw/workspace/projects")


class SanWanDiaryGenerator:
    """参考 sanwan.ai 风格的日记生成器"""

    def __init__(self):
        self.today = datetime.now()
        self.date_str = self.today.strftime('%Y-%m-%d')
        self.chinese_date = self.today.strftime('%Y 年 %m 月 %d 日')
        self.day_count = 1  # 第几天

    def get_git_stats(self) -> Dict:
        """获取 Git 统计"""
        stats = {'commits': 0, 'files': 0, 'additions': 0, 'deletions': 0}

        try:
            # 提交数
            result = subprocess.run(
                ['git', '-C', str(WORKSPACE_DIR / 'Guangchu'), 'rev-list', '--count', '--since=today', 'HEAD'],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                stats['commits'] = int(result.stdout.strip())

            # 文件变更
            result = subprocess.run(
                ['git', '-C', str(WORKSPACE_DIR / 'Guangchu'), 'diff', '--shortstat', 'HEAD~1'],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                output = result.stdout
                if 'files changed' in output:
                    parts = output.split(',')
                    for part in parts:
                        part = part.strip()
                        if 'files changed' in part:
                            stats['files'] = int(''.join(filter(str.isdigit, part)))
                        elif 'insertions' in part:
                            stats['additions'] = int(''.join(filter(str.isdigit, part)))
                        elif 'deletions' in part:
                            stats['deletions'] = int(''.join(filter(str.isdigit, part)))
        except Exception as e:
            print(f"❌ Git 错误：{e}")

        return stats

    def get_work_log(self) -> List[Dict]:
        """获取工作日志"""
        # 示例日志（实际应该从任务系统或 Git 提取）
        logs = [
            {
                'time': '09:00',
                'type': 'start',
                'title': '开始一天的工作',
                'content': '每天早上第一件事就是查看昨天的代码，规划今天的工作。',
            },
            {
                'time': '09:30',
                'type': 'code',
                'title': '开发日记系统',
                'content': '参考 sanwan.ai 的设计风格，重新设计日记页面。极简风格，时间线清晰。',
            },
            {'time': '12:00', 'type': 'lunch', 'title': '午休', 'content': '休息是为了走更长远的路。'},
            {
                'time': '14:00',
                'type': 'code',
                'title': '继续优化',
                'content': '下午继续完善日记系统，添加数据统计功能。',
            },
            {
                'time': '16:00',
                'type': 'meeting',
                'title': '项目讨论',
                'content': '和 Terry 讨论项目发展方向，确定下一步计划。',
            },
            {
                'time': '18:00',
                'type': 'summary',
                'title': '一天总结',
                'content': '今天效率不错，完成了日记系统的开发。明天继续努力！',
            },
        ]

        return logs

    def get_project_stats(self) -> Dict:
        """获取项目统计"""
        return {
            'guangchu': {
                'files': len(list((WORKSPACE_DIR / 'Guangchu').rglob('*.py'))),
                'commits': self._get_commit_count('Guangchu'),
            },
            'investment': {
                'files': len(list((WORKSPACE_DIR / 'china-solar-storage').rglob('*.html'))),
                'commits': self._get_commit_count('china-solar-storage'),
            },
        }

    def _get_commit_count(self, repo: str) -> int:
        """获取提交数"""
        try:
            result = subprocess.run(
                ['git', '-C', str(WORKSPACE_DIR / repo), 'rev-list', '--count', 'HEAD'],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                return int(result.stdout.strip())
        except:
            pass
        return 0

    def generate_diary_html(self) -> str:
        """生成 sanwan.ai 风格日记 HTML"""

        git_stats = self.get_git_stats()
        work_log = self.get_work_log()
        project_stats = self.get_project_stats()

        # 生成日志 HTML
        log_html = ""
        for log in work_log:
            log_html += f"""
            <div class="log-item">
                <div class="log-time">{log['time']}</div>
                <div class="log-content">
                    <div class="log-title">{log['title']}</div>
                    <div class="log-text">{log['content']}</div>
                </div>
            </div>
            """

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guangchu - 开发日记 | {self.chinese_date}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", sans-serif;
            line-height: 1.6;
            color: #1a1a1a;
            background: #ffffff;
            padding: 20px;
        }}
        
        .container {{
            max-width: 720px;
            margin: 0 auto;
            padding: 60px 20px;
        }}
        
        /* Header */
        .header {{
            margin-bottom: 60px;
        }}
        
        .header h1 {{
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 12px;
            color: #1a1a1a;
        }}
        
        .header-meta {{
            font-size: 14px;
            color: #999;
        }}
        
        .header-meta span {{
            margin-right: 20px;
        }}
        
        /* Stats */
        .stats {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 60px;
            padding: 30px;
            background: #f8f8f8;
            border-radius: 12px;
        }}
        
        .stat-item {{
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 36px;
            font-weight: 700;
            color: #0071e3;
            margin-bottom: 8px;
        }}
        
        .stat-label {{
            font-size: 13px;
            color: #666;
        }}
        
        /* Work Log */
        .log-section {{
            margin-bottom: 60px;
        }}
        
        .section-title {{
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 30px;
            color: #1a1a1a;
        }}
        
        .log-list {{
            position: relative;
            padding-left: 40px;
        }}
        
        .log-list::before {{
            content: '';
            position: absolute;
            left: 15px;
            top: 0;
            bottom: 0;
            width: 2px;
            background: #e0e0e0;
        }}
        
        .log-item {{
            position: relative;
            margin-bottom: 30px;
        }}
        
        .log-time {{
            position: absolute;
            left: -40px;
            top: 0;
            width: 32px;
            height: 32px;
            background: #0071e3;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: 600;
            color: white;
        }}
        
        .log-content {{
            background: #f8f8f8;
            padding: 20px;
            border-radius: 8px;
        }}
        
        .log-title {{
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 8px;
            color: #1a1a1a;
        }}
        
        .log-text {{
            font-size: 14px;
            color: #666;
            line-height: 1.8;
        }}
        
        /* Project Stats */
        .project-stats {{
            margin-bottom: 60px;
        }}
        
        .project-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }}
        
        .project-card {{
            padding: 25px;
            background: #f8f8f8;
            border-radius: 12px;
        }}
        
        .project-name {{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 15px;
            color: #1a1a1a;
        }}
        
        .project-stat {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .project-stat:last-child {{
            border-bottom: none;
        }}
        
        .project-stat-label {{
            font-size: 14px;
            color: #666;
        }}
        
        .project-stat-value {{
            font-size: 14px;
            font-weight: 600;
            color: #1a1a1a;
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding: 40px 20px;
            border-top: 1px solid #e0e0e0;
            color: #999;
            font-size: 14px;
        }}
        
        .footer-links {{
            margin-top: 20px;
        }}
        
        .footer-links a {{
            color: #0071e3;
            text-decoration: none;
            margin: 0 10px;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 40px 20px;
            }}
            
            .header h1 {{
                font-size: 24px;
            }}
            
            .stats {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .project-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🦞 Guangchu - 开发日记</h1>
            <div class="header-meta">
                <span>{self.chinese_date}</span>
                <span>第 {self.day_count} 天</span>
                <span>星期 {self.today.strftime('%A')}</span>
            </div>
        </div>
        
        <!-- Stats -->
        <div class="stats">
            <div class="stat-item">
                <div class="stat-value">{git_stats['commits']}</div>
                <div class="stat-label">今日提交</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{git_stats['files']}</div>
                <div class="stat-label">文件变更</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">+{git_stats['additions']}</div>
                <div class="stat-label">新增代码</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">-{git_stats['deletions']}</div>
                <div class="stat-label">删除代码</div>
            </div>
        </div>
        
        <!-- Work Log -->
        <div class="log-section">
            <h2 class="section-title">📝 工作日志</h2>
            <div class="log-list">
                {log_html}
            </div>
        </div>
        
        <!-- Project Stats -->
        <div class="project-stats">
            <h2 class="section-title">📊 项目统计</h2>
            <div class="project-grid">
                <div class="project-card">
                    <div class="project-name">🦞 Guangchu</div>
                    <div class="project-stat">
                        <span class="project-stat-label">Python 文件</span>
                        <span class="project-stat-value">{project_stats['guangchu']['files']} 个</span>
                    </div>
                    <div class="project-stat">
                        <span class="project-stat-label">Git 提交</span>
                        <span class="project-stat-value">{project_stats['guangchu']['commits']} 次</span>
                    </div>
                </div>
                <div class="project-card">
                    <div class="project-name">🗺️ 投资地图</div>
                    <div class="project-stat">
                        <span class="project-stat-label">HTML 文件</span>
                        <span class="project-stat-value">{project_stats['investment']['files']} 个</span>
                    </div>
                    <div class="project-stat">
                        <span class="project-stat-label">Git 提交</span>
                        <span class="project-stat-value">{project_stats['investment']['commits']} 次</span>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p>© 2026 Guangchu - Solar-Storage News Collection & Analysis System</p>
            <div class="footer-links">
                <a href="/">首页</a>
                <a href="/diary/">日记索引</a>
                <a href="/project-intro.html">项目详情</a>
                <a href="https://github.com/xuegangwu/guangchu" target="_blank">GitHub</a>
            </div>
        </div>
    </div>
</body>
</html>
"""

        return html

    def save_diary(self, html: str):
        """保存日记"""
        DIARY_DIR.mkdir(exist_ok=True)

        today_file = DIARY_DIR / f"{self.date_str}-sanwan.html"
        with open(today_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✅ sanwan.ai 风格日记已保存：{today_file}")
        return today_file

    def run(self):
        """运行日记生成"""
        print("=" * 60)
        print("📔 Guangchu - sanwan.ai 风格日记生成")
        print("=" * 60)
        print(f"\n日期：{self.chinese_date}")
        print(f"参考风格：sanwan.ai (傅盛 3 万龙虾养成记)")
        print("\n正在生成日记...")

        html = self.generate_diary_html()
        diary_file = self.save_diary(html)

        print("\n" + "=" * 60)
        print("✅ 日记生成完成！")
        print("=" * 60)
        print(f"\n日记位置：{diary_file}")
        print(f"访问地址：http://localhost:5000/diary/{self.date_str}-sanwan.html")

        return diary_file


if __name__ == "__main__":
    generator = SanWanDiaryGenerator()
    generator.run()
