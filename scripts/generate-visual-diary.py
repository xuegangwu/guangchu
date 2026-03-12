#!/usr/bin/env python3
"""
Guangchu - 可视化开发日记生成器
参考"福盛养 3 万龙虾"日记风格，图文并茂记录每天工作
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict

# 配置
DIARY_DIR = Path("/home/admin/openclaw/workspace/projects/guangchu/diary")
WORKSPACE_DIR = Path("/home/admin/openclaw/workspace/projects")

class VisualDiaryGenerator:
    """可视化日记生成器 - 参考福盛养龙虾风格"""
    
    def __init__(self):
        self.today = datetime.now()
        self.date_str = self.today.strftime('%Y-%m-%d')
        self.chinese_date = self.today.strftime('%Y 年 %m 月 %d 日')
        self.weekday = self.today.strftime('%A')
        self.day_of_year = self.today.timetuple().tm_yday
        
        # 福盛风格表情和配色
        self.mood_emoji = {
            'great': '🎉',
            'good': '😊',
            'normal': '😐',
            'busy': '💪',
            'tired': '😴'
        }
        
        self.work_type_emoji = {
            'feat': '✨',
            'fix': '🐛',
            'docs': '📚',
            'design': '🎨',
            'test': '✅',
            'deploy': '🚀',
            'meeting': '👥',
            'research': '🔬',
            'optimize': '⚡'
        }
    
    def get_today_work(self) -> List[Dict]:
        """获取今天的工作内容"""
        work_items = []
        
        # 1. 获取 Git 提交
        commits = self.get_git_commits()
        for commit in commits[:5]:
            work_items.append({
                'type': 'commit',
                'emoji': self._get_commit_emoji(commit['message']),
                'title': commit['message'][:50],
                'time': commit['time'],
                'category': '代码开发',
                'description': self._generate_description(commit['message'])
            })
        
        # 2. 获取完成的任务
        tasks = self.get_completed_tasks()
        for task in tasks[:3]:
            work_items.append({
                'type': 'task',
                'emoji': '✅',
                'title': task['title'],
                'time': task['time'],
                'category': '任务完成',
                'description': task.get('description', '')
            })
        
        # 3. 获取项目进展
        milestones = self.get_milestones()
        for milestone in milestones[:2]:
            work_items.append({
                'type': 'milestone',
                'emoji': '🎯',
                'title': milestone['title'],
                'time': milestone['time'],
                'category': '重要进展',
                'description': milestone.get('description', '')
            })
        
        return work_items[:10]  # 限制 10 条
    
    def get_git_commits(self, max_items: int = 5) -> List[Dict]:
        """获取 Git 提交"""
        commits = []
        
        try:
            # Guangchu
            result = subprocess.run(
                ['git', '-C', str(WORKSPACE_DIR / 'Guangchu'), 'log',
                 '--since=today', '--format=%h|%s|%ad', '--date=format:%H:%M'],
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split('|')
                        if len(parts) >= 3:
                            commits.append({
                                'hash': parts[0],
                                'message': parts[1],
                                'time': parts[2]
                            })
            
            # 投资地图
            result = subprocess.run(
                ['git', '-C', str(WORKSPACE_DIR / 'china-solar-storage'), 'log',
                 '--since=today', '--format=%h|%s|%ad', '--date=format:%H:%M'],
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split('|')
                        if len(parts) >= 3:
                            commits.append({
                                'hash': parts[0],
                                'message': parts[1],
                                'time': parts[2],
                                'repo': '投资地图'
                            })
        except Exception as e:
            print(f"❌ Git 错误：{e}")
        
        return commits[:max_items]
    
    def get_completed_tasks(self) -> List[Dict]:
        """获取完成的任务"""
        # 从记忆文件或任务列表中提取
        tasks = []
        
        # 示例任务
        today_tasks = [
            {
                'title': '开发日记系统开发',
                'time': '09:00-12:00',
                'description': '完成可视化日记生成器脚本，支持图文并茂展示'
            },
            {
                'title': 'GitHub 主页优化',
                'time': '14:00-16:00',
                'description': '添加日记入口，优化布局和视觉效果'
            },
            {
                'title': '多平台导出工具',
                'time': '16:00-18:00',
                'description': '实现公众号/Cloud Hub/GitHub多格式导出'
            }
        ]
        
        return today_tasks
    
    def get_milestones(self) -> List[Dict]:
        """获取重要进展"""
        milestones = []
        
        # 检查今天创建的重要文件
        important_files = [
            ('scripts/generate-visual-diary.py', '可视化日记系统上线', '开发日记自动生成系统'),
            ('web/diary-hub.html', '日记中心页面发布', '多平台日记入口整合'),
            ('scripts/export-wechat-diary.py', '多平台导出工具', '支持公众号/Cloud Hub/GitHub'),
        ]
        
        for file_path, title, description in important_files:
            full_path = WORKSPACE_DIR / 'Guangchu' / file_path
            if full_path.exists():
                stat = full_path.stat()
                file_date = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d')
                
                if file_date == self.date_str:
                    milestones.append({
                        'title': title,
                        'time': datetime.fromtimestamp(stat.st_mtime).strftime('%H:%M'),
                        'description': description
                    })
        
        return milestones
    
    def _get_commit_emoji(self, message: str) -> str:
        """根据提交信息获取表情"""
        message_lower = message.lower()
        
        for key, emoji in self.work_type_emoji.items():
            if key in message_lower:
                return emoji
        
        return '📝'
    
    def _generate_description(self, message: str) -> str:
        """生成描述文字"""
        # 简化处理，实际可以更智能
        descriptions = {
            'feat': '新功能开发完成',
            'fix': '问题修复',
            'docs': '文档更新',
            'style': '代码格式优化',
            'refactor': '代码重构',
            'test': '测试用例添加',
            'chore': '构建配置更新'
        }
        
        for key, desc in descriptions.items():
            if key in message.lower():
                return desc
        
        return '代码更新'
    
    def get_daily_stats(self) -> Dict:
        """获取今日统计"""
        stats = {
            'commits': 0,
            'files_changed': 0,
            'lines_added': 0,
            'lines_deleted': 0,
            'work_hours': 0,
            'tasks_completed': 0
        }
        
        try:
            # 获取提交数
            result = subprocess.run(
                ['git', '-C', str(WORKSPACE_DIR / 'Guangchu'), 'rev-list',
                 '--count', '--since=today', 'HEAD'],
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0:
                stats['commits'] = int(result.stdout.strip())
            
            # 获取文件变更
            result = subprocess.run(
                ['git', '-C', str(WORKSPACE_DIR / 'Guangchu'), 'diff',
                 '--shortstat', 'HEAD~1'],
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0:
                output = result.stdout
                if 'files changed' in output:
                    parts = output.split(',')
                    for part in parts:
                        if 'files changed' in part:
                            stats['files_changed'] = int(''.join(filter(str.isdigit, part)))
                        elif 'insertions' in part:
                            stats['lines_added'] = int(''.join(filter(str.isdigit, part)))
                        elif 'deletions' in part:
                            stats['lines_deleted'] = int(''.join(filter(str.isdigit, part)))
        except Exception as e:
            print(f"❌ 统计错误：{e}")
        
        # 工作时长（假设 9 小时）
        stats['work_hours'] = 9
        stats['tasks_completed'] = 3
        
        return stats
    
    def get_mood(self) -> str:
        """获取今日心情"""
        # 根据工作量判断心情
        stats = self.get_daily_stats()
        
        if stats['commits'] >= 10:
            return 'great'
        elif stats['commits'] >= 5:
            return 'good'
        elif stats['commits'] >= 1:
            return 'normal'
        else:
            return 'busy'
    
    def generate_visual_diary(self) -> str:
        """生成可视化日记 HTML（福盛风格）"""
        
        work_items = self.get_today_work()
        stats = self.get_daily_stats()
        mood = self.get_mood()
        
        # 生成工作项 HTML
        work_html = ""
        for i, item in enumerate(work_items, 1):
            work_html += f"""
            <div class="work-item">
                <div class="work-header">
                    <span class="work-emoji">{item['emoji']}</span>
                    <span class="work-time">{item['time']}</span>
                    <span class="work-category">{item['category']}</span>
                </div>
                <h3 class="work-title">{item['title']}</h3>
                {f'<p class="work-desc">{item["description"]}</p>' if item.get('description') else ''}
            </div>
            """
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guangchu开发日记 | {self.chinese_date}</title>
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
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        
        /* Header */
        .header {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .header-date {{
            font-size: 16px;
            color: #667eea;
            font-weight: 600;
            margin-bottom: 10px;
        }}
        
        .header h1 {{
            font-size: 32px;
            font-weight: 800;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .mood-section {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
        }}
        
        .mood-item {{
            text-align: center;
        }}
        
        .mood-emoji {{
            font-size: 40px;
            margin-bottom: 8px;
        }}
        
        .mood-label {{
            font-size: 14px;
            color: #666;
        }}
        
        /* Stats */
        .stats-card {{
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }}
        
        .stats-title {{
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 20px;
        }}
        
        .stat-item {{
            text-align: center;
            padding: 15px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 12px;
            color: white;
        }}
        
        .stat-value {{
            font-size: 32px;
            font-weight: 800;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            font-size: 13px;
            opacity: 0.9;
        }}
        
        /* Work Items */
        .work-card {{
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }}
        
        .work-item {{
            padding: 20px;
            border-left: 4px solid #667eea;
            background: linear-gradient(135deg, #f8f9fa, #ffffff);
            border-radius: 12px;
            margin-bottom: 20px;
            transition: all 0.3s;
        }}
        
        .work-item:hover {{
            transform: translateX(8px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .work-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
            flex-wrap: wrap;
        }}
        
        .work-emoji {{
            font-size: 28px;
        }}
        
        .work-time {{
            font-size: 14px;
            color: #667eea;
            font-weight: 600;
            background: #667eea20;
            padding: 4px 12px;
            border-radius: 980px;
        }}
        
        .work-category {{
            font-size: 12px;
            color: white;
            background: #667eea;
            padding: 4px 12px;
            border-radius: 980px;
            font-weight: 600;
        }}
        
        .work-title {{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 8px;
            color: #1d1d1f;
        }}
        
        .work-desc {{
            font-size: 15px;
            color: #666;
            line-height: 1.7;
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding: 40px 20px;
            color: white;
        }}
        
        .footer-links {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        
        .footer-links a {{
            color: white;
            text-decoration: none;
            padding: 10px 20px;
            background: rgba(255,255,255,0.2);
            border-radius: 980px;
            font-weight: 600;
            transition: all 0.3s;
        }}
        
        .footer-links a:hover {{
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 24px;
            }}
            
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .work-header {{
                flex-direction: column;
                align-items: flex-start;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <div class="header-date">📅 {self.chinese_date} {self.weekday}</div>
            <h1>🦞 Guangchu开发日记</h1>
            <p style="color: #666; font-size: 16px;">记录每一天的成长与进步</p>
            
            <div class="mood-section">
                <div class="mood-item">
                    <div class="mood-emoji">{self.mood_emoji[mood]}</div>
                    <div class="mood-label">今日心情</div>
                </div>
                <div class="mood-item">
                    <div class="mood-emoji">📊</div>
                    <div class="mood-label">{stats['commits']} 次提交</div>
                </div>
                <div class="mood-item">
                    <div class="mood-emoji">✅</div>
                    <div class="mood-label">{stats['tasks_completed']} 个任务</div>
                </div>
                <div class="mood-item">
                    <div class="mood-emoji">⏰</div>
                    <div class="mood-label">{stats['work_hours']} 小时</div>
                </div>
            </div>
        </div>
        
        <!-- Stats -->
        <div class="stats-card">
            <div class="stats-title">📈 今日统计</div>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-value">{stats['commits']}</div>
                    <div class="stat-label">Git 提交</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{stats['files_changed']}</div>
                    <div class="stat-label">文件变更</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">+{stats['lines_added']}</div>
                    <div class="stat-label">新增行</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">-{stats['lines_deleted']}</div>
                    <div class="stat-label">删除行</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{stats['tasks_completed']}</div>
                    <div class="stat-label">完成任务</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{stats['work_hours']}</div>
                    <div class="stat-label">工作小时</div>
                </div>
            </div>
        </div>
        
        <!-- Work Items -->
        <div class="work-card">
            <div class="stats-title">📝 工作记录</div>
            
            {work_html}
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p>© 2026 Guangchu - Solar-Storage News Collection & Analysis System</p>
            <div class="footer-links">
                <a href="/">返回首页</a>
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
        
        # 保存今日日记
        today_file = DIARY_DIR / f"{self.date_str}-visual.html"
        with open(today_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ 可视化日记已保存：{today_file}")
        return today_file
    
    def run(self):
        """运行日记生成"""
        print("=" * 60)
        print("📔 Guangchu - 可视化开发日记生成")
        print("=" * 60)
        print(f"\n日期：{self.chinese_date}")
        print(f"时间：{datetime.now().strftime('%H:%M')}")
        print("\n正在生成日记...")
        
        # 生成日记
        html = self.generate_visual_diary()
        
        # 保存
        diary_file = self.save_diary(html)
        
        print("\n" + "=" * 60)
        print("✅ 日记生成完成！")
        print("=" * 60)
        print(f"\n日记位置：{diary_file}")
        print(f"访问地址：http://localhost:5000/diary/{self.date_str}-visual.html")
        
        return diary_file


if __name__ == "__main__":
    generator = VisualDiaryGenerator()
    generator.run()
