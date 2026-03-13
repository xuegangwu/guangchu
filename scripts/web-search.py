#!/usr/bin/env python3
"""
Guangchu - Web 搜索界面
使用 Flask 提供 Web 搜索界面
"""

from flask import Flask, request, jsonify, render_template_string
import sqlite3
import json
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path("/home/admin/openclaw/workspace/projects/guangchu/search.db")

# HTML 模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔍 Guangchu搜索</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 { font-size: 28px; margin-bottom: 10px; }
        .header p { opacity: 0.9; }
        .search-box {
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }
        .search-input {
            width: 100%;
            padding: 15px 20px;
            font-size: 16px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            outline: none;
            transition: border-color 0.3s;
        }
        .search-input:focus { border-color: #667eea; }
        .filters {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            padding: 20px 30px;
        }
        .filter-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 500;
            color: #495057;
            font-size: 14px;
        }
        .filter-group select, .filter-group input {
            width: 100%;
            padding: 10px;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            font-size: 14px;
        }
        .search-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            margin: 0 30px 30px;
            transition: transform 0.2s;
        }
        .search-btn:hover { transform: translateY(-2px); }
        .results { padding: 30px; }
        .result-count {
            color: #6c757d;
            margin-bottom: 20px;
            font-size: 14px;
        }
        .result-item {
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            transition: box-shadow 0.3s;
        }
        .result-item:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .result-title {
            font-size: 16px;
            font-weight: 600;
            color: #212529;
            margin-bottom: 10px;
        }
        .result-meta {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            margin-bottom: 10px;
        }
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
        }
        .badge-type { background: #e3f2fd; color: #1976d2; }
        .badge-region { background: #f3e5f5; color: #7b1fa2; }
        .badge-source { background: #e8f5e9; color: #388e3c; }
        .result-summary {
            color: #495057;
            font-size: 14px;
            line-height: 1.6;
            margin-bottom: 10px;
        }
        .result-link {
            color: #667eea;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
        }
        .result-link:hover { text-decoration: underline; }
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #6c757d;
        }
        .empty-state h3 { margin-bottom: 10px; }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-number {
            font-size: 32px;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 5px;
        }
        .stat-label {
            color: #6c757d;
            font-size: 14px;
        }
        .loading {
            text-align: center;
            padding: 40px;
            color: #6c757d;
        }
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-logo">🦞</div>
            <h1>Guangchu</h1>
            <p>全球光伏 + 储能信息检索</p>
            <p class="header-tagline">Solar-Storage News Collection & Analysis</p>
        </div>
        
        <div class="search-box">
            <div class="search-input-wrapper">
                <span class="search-icon">🔍</span>
                <input type="text" id="keyword" class="search-input" 
                       placeholder="搜索关键词（英文，如：battery, solar, energy storage）..."
                       onkeypress="if(event.key==='Enter') search()">
            </div>
        </div>
        
        <div class="filters">
            <div class="filter-group">
                <label>类型</label>
                <select id="type">
                    <option value="">全部</option>
                    <option value="产品">产品</option>
                    <option value="政策">政策</option>
                    <option value="项目">项目</option>
                    <option value="其他">其他</option>
                </select>
            </div>
            <div class="filter-group">
                <label>区域</label>
                <select id="region">
                    <option value="">全部</option>
                    <option value="Europe">欧洲</option>
                    <option value="US">美国</option>
                    <option value="Global">全球</option>
                    <option value="Japan">日本</option>
                    <option value="Southeast Asia">东南亚</option>
                </select>
            </div>
            <div class="filter-group">
                <label>来源</label>
                <select id="source">
                    <option value="">全部</option>
                    <option value="PV Magazine">PV Magazine</option>
                    <option value="Energy Storage News">Energy Storage News</option>
                </select>
            </div>
            <div class="filter-group">
                <label>结果数量</label>
                <select id="limit">
                    <option value="10">10 条</option>
                    <option value="20" selected>20 条</option>
                    <option value="50">50 条</option>
                    <option value="100">100 条</option>
                </select>
            </div>
        </div>
        
        <button class="search-btn" onclick="search()">🔍 搜索</button>
        
        <div id="stats" class="stats"></div>
        <div id="results" class="results"></div>
    </div>

    <script>
        async function search() {
            const keyword = document.getElementById('keyword').value;
            const type = document.getElementById('type').value;
            const region = document.getElementById('region').value;
            const source = document.getElementById('source').value;
            const limit = document.getElementById('limit').value;
            
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '<div class="loading"><div class="spinner"></div>搜索中...</div>';
            
            const params = new URLSearchParams({ limit });
            if (keyword) params.append('keyword', keyword);
            if (type) params.append('type', type);
            if (region) params.append('region', region);
            if (source) params.append('source', source);
            
            try {
                const response = await fetch('/api/search?' + params.toString());
                const data = await response.json();
                
                if (data.results.length === 0) {
                    resultsDiv.innerHTML = `
                        <div class="empty-state">
                            <h3>😕 未找到结果</h3>
                            <p>尝试其他关键词或放宽筛选条件</p>
                        </div>
                    `;
                } else {
                    resultsDiv.innerHTML = `
                        <div class="result-count">找到 ${data.results.length} 条结果</div>
                        ${data.results.map(item => `
                            <div class="result-item">
                                <div class="result-title">${escapeHtml(item.title)}</div>
                                <div class="result-meta">
                                    <span class="badge badge-type">${item.type}</span>
                                    <span class="badge badge-region">${item.region}</span>
                                    <span class="badge badge-source">${item.source}</span>
                                    <span class="badge">${item.collected_at}</span>
                                </div>
                                <div class="result-summary">${escapeHtml(item.summary || '无摘要')}</div>
                                <a href="${item.link}" target="_blank" class="result-link">🔗 查看详情</a>
                            </div>
                        `).join('')}
                    `;
                }
            } catch (error) {
                resultsDiv.innerHTML = `
                    <div class="empty-state">
                        <h3>❌ 搜索失败</h3>
                        <p>${error.message}</p>
                    </div>
                `;
            }
        }
        
        async function loadStats() {
            try {
                const response = await fetch('/api/stats');
                const data = await response.json();
                
                document.getElementById('stats').innerHTML = `
                    <div class="stat-card">
                        <div class="stat-number">${data.total}</div>
                        <div class="stat-label">总记录数</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${data.date_range[0] || 'N/A'}</div>
                        <div class="stat-label">最早日期</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${data.date_range[1] || 'N/A'}</div>
                        <div class="stat-label">最新日期</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${data.sources.length}</div>
                        <div class="stat-label">信息源数量</div>
                    </div>
                `;
            } catch (error) {
                console.error('Failed to load stats:', error);
            }
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        // 页面加载时显示统计
        loadStats();
    </script>
</body>
</html>
"""

def search_db(keyword=None, region=None, type_=None, source=None, limit=20):
    """搜索数据库"""
    if not DB_PATH.exists():
        return []
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    conditions = []
    params = []
    
    if keyword:
        fts_condition = "id IN (SELECT rowid FROM news_fts WHERE news_fts MATCH ?)"
        like_condition = "(title LIKE ? OR summary LIKE ?)"
        like_keyword = f"%{keyword}%"
        conditions.append(f"({fts_condition} OR {like_condition})")
        params.extend([keyword, like_keyword, like_keyword])
    
    if region:
        conditions.append("region = ?")
        params.append(region)
    
    if type_:
        conditions.append("type = ?")
        params.append(type_)
    
    if source:
        conditions.append("source = ?")
        params.append(source)
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    query = f"""
        SELECT id, title, link, published, summary, source, region, type, collected_at
        FROM news
        WHERE {where_clause}
        ORDER BY collected_at DESC, published DESC
        LIMIT ?
    """
    params.append(limit)
    
    cursor.execute(query, params)
    results = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return results

def get_stats():
    """获取统计信息"""
    if not DB_PATH.exists():
        return {"total": 0}
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM news")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT MIN(collected_at), MAX(collected_at) FROM news")
    date_range = cursor.fetchone()
    
    cursor.execute("SELECT DISTINCT source FROM news")
    sources = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    
    return {
        "total": total,
        "date_range": date_range,
        "sources": sources
    }

@app.route('/')
def index():
    """主页"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/search')
def api_search():
    """搜索 API"""
    keyword = request.args.get('keyword')
    region = request.args.get('region')
    type_ = request.args.get('type')
    source = request.args.get('source')
    limit = request.args.get('limit', 20, type=int)
    
    results = search_db(keyword, region, type_, source, limit)
    
    return jsonify({
        "success": True,
        "results": results,
        "count": len(results)
    })

@app.route('/api/stats')
def api_stats():
    """统计 API"""
    stats = get_stats()
    return jsonify(stats)

if __name__ == '__main__':
    print("=" * 60)
    print("🔍 Guangchu Web 搜索")
    print("=" * 60)
    print("\n启动服务器...")
    print("访问地址：http://localhost:5000")
    print("\n按 Ctrl+C 停止服务器")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=False)
