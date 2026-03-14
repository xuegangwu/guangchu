#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
光储龙虾 - 数据可视化脚本
生成新闻趋势、区域分布、类型分布等图表
"""

import json
import os
from datetime import datetime, timedelta
from collections import Counter, defaultdict

WORKDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(WORKDIR, 'raw')
STATS_DIR = os.path.join(WORKDIR, 'stats')
BUILD_DIR = os.path.join(WORKDIR, 'build')

def load_all_news():
    """加载所有原始数据"""
    all_news = []
    date_news = {}
    
    for filename in sorted(os.listdir(RAW_DIR)):
        if filename.endswith('.json'):
            filepath = os.path.join(RAW_DIR, filename)
            date = filename.replace('.json', '')
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_news.extend(data)
                date_news[date] = len(data)
    
    return all_news, date_news

def generate_trend_chart(date_news, all_news, region_stats, type_stats, source_stats):
    """生成新闻趋势图表 HTML"""
    dates = list(date_news.keys())
    counts = list(date_news.values())
    
    html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>光储龙虾 - 数据可视化</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", sans-serif;
            background: linear-gradient(135deg, #0071e3 0%, #0077ed 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{
            text-align: center;
            color: white;
            padding: 60px 20px;
            margin-bottom: 40px;
        }}
        .header h1 {{ font-size: 40px; margin-bottom: 10px; }}
        .header p {{ font-size: 18px; opacity: 0.9; }}
        .chart-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }}
        .chart-card {{
            background: white;
            border-radius: 18px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        .chart-title {{
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 20px;
            color: #1d1d1f;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .stat-card {{
            background: rgba(255,255,255,0.95);
            border-radius: 12px;
            padding: 24px;
            text-align: center;
        }}
        .stat-value {{ font-size: 36px; font-weight: 700; color: #0071e3; margin-bottom: 8px; }}
        .stat-label {{ font-size: 14px; color: #86868b; }}
        .back-link {{
            display: inline-block;
            margin-top: 20px;
            padding: 12px 24px;
            background: white;
            color: #0071e3;
            text-decoration: none;
            border-radius: 980px;
            font-weight: 600;
        }}
        @media (max-width: 768px) {{
            .chart-grid {{ grid-template-columns: 1fr; }}
            .header h1 {{ font-size: 28px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 光储龙虾 - 数据可视化</h1>
            <p>News Analytics Dashboard</p>
            <a href="index.html" class="back-link">← 返回项目首页</a>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{len(all_news)}</div>
                <div class="stat-label">总新闻数</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(dates)}</div>
                <div class="stat-label">数据天数</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{sum(counts) // len(counts) if counts else 0}</div>
                <div class="stat-label">日均新闻</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{max(counts) if counts else 0}</div>
                <div class="stat-label">单日最高</div>
            </div>
        </div>
        
        <div class="chart-grid">
            <div class="chart-card">
                <h2 class="chart-title">📈 新闻趋势（按日期）</h2>
                <canvas id="trendChart"></canvas>
            </div>
            <div class="chart-card">
                <h2 class="chart-title">🌍 区域分布</h2>
                <canvas id="regionChart"></canvas>
            </div>
            <div class="chart-card">
                <h2 class="chart-title">📋 类型分布</h2>
                <canvas id="typeChart"></canvas>
            </div>
            <div class="chart-card">
                <h2 class="chart-title">📰 来源分布</h2>
                <canvas id="sourceChart"></canvas>
            </div>
        </div>
        
        <div style="text-align: center;">
            <a href="index.html" class="back-link">← 返回项目首页</a>
        </div>
    </div>
    
    <script>
        // 新闻趋势图
        new Chart(document.getElementById('trendChart'), {{
            type: 'line',
            data: {{
                labels: {json.dumps(dates)},
                datasets: [{{
                    label: '新闻数量',
                    data: {json.dumps(counts)},
                    borderColor: '#0071e3',
                    backgroundColor: 'rgba(0, 113, 227, 0.1)',
                    tension: 0.4,
                    fill: true
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ display: false }}
                }},
                scales: {{
                    y: {{ beginAtZero: true }}
                }}
            }}
        }});
        
        // 区域分布图
        new Chart(document.getElementById('regionChart'), {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps(list(region_stats.keys()))},
                datasets: [{{
                    data: {json.dumps(list(region_stats.values()))},
                    backgroundColor: ['#0071e3', '#34c759', '#ff9500', '#5856d6', '#ff2d55']
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ position: 'bottom' }}
                }}
            }}
        }});
        
        // 类型分布图
        new Chart(document.getElementById('typeChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(list(type_stats.keys()))},
                datasets: [{{
                    label: '数量',
                    data: {json.dumps(list(type_stats.values()))},
                    backgroundColor: '#0071e3'
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ display: false }}
                }},
                scales: {{
                    y: {{ beginAtZero: true }}
                }}
            }}
        }});
        
        // 来源分布图
        new Chart(document.getElementById('sourceChart'), {{
            type: 'pie',
            data: {{
                labels: {json.dumps(list(source_stats.keys())[:5])},
                datasets: [{{
                    data: {json.dumps(list(source_stats.values())[:5])},
                    backgroundColor: ['#0071e3', '#34c759', '#ff9500', '#5856d6', '#ff2d55']
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ position: 'bottom' }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    return html

def generate_visualization():
    """生成可视化页面"""
    os.makedirs(STATS_DIR, exist_ok=True)
    os.makedirs(BUILD_DIR, exist_ok=True)
    
    print("=" * 60)
    print("📊 Guangchu - 数据可视化生成")
    print("=" * 60)
    print("\n正在加载数据...\n")
    
    all_news, date_news = load_all_news()
    print(f"✅ 加载 {len(all_news)} 条新闻")
    print(f"✅ 数据天数：{len(date_news)}")
    
    # 统计区域分布
    regions = [item.get('region', 'Unknown') for item in all_news]
    region_stats = dict(Counter(regions))
    
    # 统计类型分布
    types = [item.get('type', 'Other') for item in all_news]
    type_stats = dict(Counter(types))
    
    # 统计来源分布
    sources = [item.get('source', 'Unknown') for item in all_news]
    source_stats = dict(Counter(sources))
    
    print(f"✅ 区域：{len(region_stats)} 个")
    print(f"✅ 类型：{len(type_stats)} 个")
    print(f"✅ 来源：{len(source_stats)} 个")
    
    # 生成可视化 HTML
    html = generate_trend_chart(date_news, all_news, region_stats, type_stats, source_stats)
    
    # 保存到 build 目录
    output_path = os.path.join(BUILD_DIR, 'analytics.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✅ 可视化页面已生成：{output_path}")
    print("\n访问地址：http://localhost/analytics.html")
    print("=" * 60)
    
    return output_path

if __name__ == '__main__':
    generate_visualization()
