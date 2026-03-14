#!/usr/bin/env python3
"""
Guangchu - 完全参考 sanwan.ai (3 万点 AI) 风格日记生成器
极致简约，专业质感
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict

# 配置
DIARY_DIR = Path("/home/admin/openclaw/workspace/projects/guangchu/diary")
WORKSPACE_DIR = Path("/home/admin/openclaw/workspace/projects")


class SanWanStyleGenerator:
    """完全参考 sanwan.ai 风格"""

    def __init__(self):
        self.today = datetime.now()
        self.date_str = self.today.strftime('%Y-%m-%d')
        self.chinese_date = self.today.strftime('%Y 年 %m 月 %d 日')
        self.day_count = 1

    def get_git_stats(self) -> Dict:
        """获取 Git 统计"""
        stats = {'commits': 0, 'files': 0, 'additions': 0, 'deletions': 0}

        try:
            result = subprocess.run(
                ['git', '-C', str(WORKSPACE_DIR / 'Guangchu'), 'rev-list', '--count', '--since=today', 'HEAD'],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                stats['commits'] = int(result.stdout.strip())

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
                        if 'files changed' in part:
                            stats['files'] = int(''.join(filter(str.isdigit, part)))
                        elif 'insertions' in part:
                            stats['additions'] = int(''.join(filter(str.isdigit, part)))
                        elif 'deletions' in part:
                            stats['deletions'] = int(''.join(filter(str.isdigit, part)))
        except:
            pass

        return stats

    def get_work_log(self) -> List[Dict]:
        """获取工作日志"""
        return [
            {'time': '09:00', 'title': '开始一天的工作', 'content': '查看代码，规划今天的工作', 'type': 'start'},
            {
                'time': '09:30',
                'title': '开发日记系统',
                'content': '参考 sanwan.ai 的设计风格，重新设计日记页面',
                'type': 'code',
            },
            {'time': '12:00', 'title': '午休', 'content': '休息是为了走更长远的路', 'type': 'break'},
            {'time': '14:00', 'title': '继续优化', 'content': '下午继续完善日记系统，添加数据统计功能', 'type': 'code'},
            {'time': '16:00', 'title': '项目讨论', 'content': '和 Terry 讨论项目发展方向', 'type': 'meeting'},
            {'time': '18:00', 'title': '一天总结', 'content': '今天效率不错，完成了日记系统的开发', 'type': 'summary'},
        ]

    def generate_html(self) -> str:
        """生成完全参考 sanwan.ai 风格的 HTML"""

        git_stats = self.get_git_stats()
        work_log = self.get_work_log()

        log_html = ""
        for log in work_log:
            log_html += f"""
            <div class="log-item">
                <div class="log-time">{log['time']}</div>
                <div class="log-content">
                    <div class="log-title">{log['title']}</div>
                    <div class="log-text">{log['content']}</div>
                </div>
            </div>"""

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guangchu - 开发日记 | {self.chinese_date}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
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
        
        .header {{
            margin-bottom: 60px;
            padding-bottom: 30px;
            border-bottom: 1px solid #eaeaea;
        }}
        
        .header h1 {{
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 12px;
            color: #1a1a1a;
            letter-spacing: -0.5px;
        }}
        
        .header-meta {{
            font-size: 14px;
            color: #999;
        }}
        
        .header-meta span {{
            margin-right: 20px;
        }}
        
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
            letter-spacing: -1px;
        }}
        
        .stat-label {{
            font-size: 13px;
            color: #666;
        }}
        
        .section-title {{
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 30px;
            color: #1a1a1a;
            letter-spacing: -0.5px;
        }}
        
        .log-list {{
            position: relative;
            padding-left: 40px;
            margin-bottom: 60px;
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
        
        .footer {{
            text-align: center;
            padding: 40px 20px;
            border-top: 1px solid #eaeaea;
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
            .container {{ padding: 40px 20px; }}
            .header h1 {{ font-size: 24px; }}
            .stats {{ grid-template-columns: repeat(2, 1fr); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🦞 Guangchu - 开发日记</h1>
            <div class="header-meta">
                <span>{self.chinese_date}</span>
                <span>第 {self.day_count} 天</span>
            </div>
        </div>
        
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
        
        <h2 class="section-title">工作日志</h2>
        <div class="log-list">
            {log_html}
        </div>
        
        <div class="footer">
            <p>© 2026 Guangchu</p>
            <div class="footer-links">
                <a href="/">首页</a>
                <a href="/diary/">日记</a>
                <a href="https://github.com/xuegangwu/guangchu">GitHub</a>
            </div>
        </div>
    </div>
</body>
</html>"""

        return html

    def save(self, html: str):
        DIARY_DIR.mkdir(exist_ok=True)
        file = DIARY_DIR / f"{self.date_str}.html"
        with open(file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ 日记已保存：{file}")
        return file

    def run(self):
        print("📔 生成 sanwan.ai 风格日记...")
        html = self.generate_html()
        file = self.save(html)
        print(f"访问：http://localhost:5000/diary/{self.date_str}.html")
        return file


if __name__ == "__main__":
    SanWanStyleGenerator().run()
