#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
光储龙虾 - RESTful API 服务
基于 Flask 的 API 接口

v2.2 Phase 4 新增:
- RESTful API 端点
- 搜索 API
- 数据 API
- 统计 API
- 错误处理
- 速率限制
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
from functools import wraps
import time

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from flask import Flask, request, jsonify, Response
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("Flask 未安装，请运行：pip install flask")

from scripts.advanced_search import AdvancedSearch
from scripts.cache import get_cache, cached
from scripts.logger import logger, info, debug, error, warning
from scripts.config import get_config

# 初始化 Flask 应用
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 配置
config = get_config()
cache = get_cache()
search_engine = AdvancedSearch()

# 速率限制配置
RATE_LIMIT = 100  # 每分钟请求数
rate_limit_store = {}


def rate_limit(f):
    """速率限制装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = request.remote_addr
        current_time = time.time()
        
        # 清理过期记录
        rate_limit_store[client_ip] = [
            t for t in rate_limit_store.get(client_ip, [])
            if current_time - t < 60
        ]
        
        # 检查速率限制
        if len(rate_limit_store.get(client_ip, [])) >= RATE_LIMIT:
            warning(f"速率限制：{client_ip}")
            return jsonify({
                'success': False,
                'error': {
                    'code': 'RATE_LIMITED',
                    'message': '请求频率超限，请稍后重试'
                }
            }), 429
        
        # 记录请求
        if client_ip not in rate_limit_store:
            rate_limit_store[client_ip] = []
        rate_limit_store[client_ip].append(current_time)
        
        return f(*args, **kwargs)
    return decorated_function


def api_response(data: Dict, status: int = 200) -> Response:
    """统一 API 响应格式"""
    response = {
        'success': True,
        'timestamp': datetime.now().isoformat(),
        **data
    }
    return jsonify(response), status


def api_error(code: str, message: str, status: int = 400, details: Optional[Dict] = None) -> Response:
    """统一错误响应格式"""
    response = {
        'success': False,
        'error': {
            'code': code,
            'message': message
        }
    }
    if details:
        response['error']['details'] = details
    return jsonify(response), status


# ==================== 搜索 API ====================

@app.route('/api/search', methods=['GET'])
@rate_limit
@cached(ttl=300, prefix="search")
def api_search():
    """
    搜索新闻
    
    Query Parameters:
        q (str): 搜索关键词（必填）
        date_from (str): 开始日期 YYYY-MM-DD
        date_to (str): 结束日期 YYYY-MM-DD
        region (str): 区域 (US/Europe/China/Japan)
        type (str): 类型 (policy/product/project/market)
        sort (str): 排序 (relevance/date)，默认 relevance
        limit (int): 结果数量，默认 20
        highlight (bool): 是否高亮，默认 true
    
    Returns:
        JSON: 搜索结果
    """
    start_time = time.time()
    
    # 获取参数
    query = request.args.get('q', '')
    if not query:
        return api_error('INVALID_PARAMETER', '缺少搜索关键词 q', 400)
    
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    region = request.args.get('region')
    news_type = request.args.get('type')
    sort_by = request.args.get('sort', 'relevance')
    limit = min(int(request.args.get('limit', 20)), 100)  # 最大 100 条
    highlight = request.args.get('highlight', 'true').lower() == 'true'
    
    # 构建过滤条件
    filters = {}
    if date_from:
        filters['date_from'] = date_from
    if date_to:
        filters['date_to'] = date_to
    if region:
        filters['region'] = region
    if news_type:
        filters['type'] = news_type
    
    try:
        # 执行搜索
        results = search_engine.search(
            query=query,
            filters=filters,
            sort_by=sort_by,
            limit=limit,
            highlight=highlight
        )
        
        search_time = (time.time() - start_time) * 1000
        
        return api_response({
            'count': len(results),
            'results': results,
            'search_time_ms': round(search_time, 2),
            'query': query,
            'filters': filters
        })
        
    except Exception as e:
        error(f"搜索失败：{str(e)}")
        return api_error('SEARCH_ERROR', f'搜索失败：{str(e)}', 500)


@app.route('/api/search/suggestions', methods=['GET'])
@rate_limit
@cached(ttl=60, prefix="suggestions")
def api_search_suggestions():
    """
    搜索建议
    
    Query Parameters:
        prefix (str): 搜索前缀（必填）
        limit (int): 建议数量，默认 5
    
    Returns:
        JSON: 搜索建议列表
    """
    prefix = request.args.get('prefix', '')
    if not prefix:
        return api_error('INVALID_PARAMETER', '缺少前缀 prefix', 400)
    
    limit = min(int(request.args.get('limit', 5)), 10)
    
    try:
        suggestions = search_engine.get_search_suggestions(prefix, limit)
        
        return api_response({
            'suggestions': suggestions,
            'prefix': prefix
        })
        
    except Exception as e:
        error(f"获取建议失败：{str(e)}")
        return api_error('SUGGESTION_ERROR', f'获取建议失败：{str(e)}', 500)


@app.route('/api/search/history', methods=['GET'])
@rate_limit
def api_search_history():
    """
    搜索历史
    
    Returns:
        JSON: 搜索历史列表
    """
    try:
        history = search_engine.get_search_history()
        
        return api_response({
            'history': history,
            'count': len(history)
        })
        
    except Exception as e:
        error(f"获取历史失败：{str(e)}")
        return api_error('HISTORY_ERROR', f'获取历史失败：{str(e)}', 500)


# ==================== 数据 API ====================

@app.route('/api/news', methods=['GET'])
@rate_limit
@cached(ttl=300, prefix="news")
def api_get_news():
    """
    获取新闻列表
    
    Query Parameters:
        date (str): 指定日期 YYYY-MM-DD
        region (str): 区域
        type (str): 类型
        page (int): 页码，默认 1
        per_page (int): 每页数量，默认 20
    
    Returns:
        JSON: 新闻列表（分页）
    """
    date = request.args.get('date')
    region = request.args.get('region')
    news_type = request.args.get('type')
    page = max(1, int(request.args.get('page', 1)))
    per_page = min(100, int(request.args.get('per_page', 20)))
    
    try:
        # TODO: 实现新闻列表查询
        # 这里使用模拟数据
        news_list = []
        total = len(news_list)
        total_pages = (total + per_page - 1) // per_page
        
        return api_response({
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages,
            'news': news_list
        })
        
    except Exception as e:
        error(f"获取新闻失败：{str(e)}")
        return api_error('NEWS_ERROR', f'获取新闻失败：{str(e)}', 500)


@app.route('/api/news/<int:news_id>', methods=['GET'])
@rate_limit
@cached(ttl=600, prefix="news_detail")
def api_get_news_detail(news_id: int):
    """
    获取新闻详情
    
    Path Parameters:
        news_id (int): 新闻 ID
    
    Returns:
        JSON: 新闻详情
    """
    try:
        # TODO: 实现新闻详情查询
        # 这里返回模拟数据
        news = {
            'id': news_id,
            'title': 'Test News',
            'url': 'https://example.com',
            'date': '2026-03-14',
            'region': 'US',
            'type': 'policy',
            'source': 'Test Source',
            'summary': 'Test summary',
            'content': 'Full content...'
        }
        
        return api_response({
            'news': news
        })
        
    except Exception as e:
        error(f"获取新闻详情失败：{str(e)}")
        return api_error('NEWS_DETAIL_ERROR', f'获取新闻详情失败：{str(e)}', 500)


# ==================== 统计 API ====================

@app.route('/api/stats', methods=['GET'])
@rate_limit
@cached(ttl=600, prefix="stats")
def api_get_stats():
    """
    获取统计信息
    
    Returns:
        JSON: 统计信息
    """
    try:
        stats = search_engine.search_stats()
        
        return api_response({
            'stats': stats
        })
        
    except Exception as e:
        error(f"获取统计失败：{str(e)}")
        return api_error('STATS_ERROR', f'获取统计失败：{str(e)}', 500)


@app.route('/api/stats/trend', methods=['GET'])
@rate_limit
@cached(ttl=300, prefix="trend")
def api_get_trend():
    """
    获取趋势数据
    
    Query Parameters:
        start (str): 开始日期
        end (str): 结束日期
        group_by (str): 分组 (date/region/type)
    
    Returns:
        JSON: 趋势数据
    """
    start = request.args.get('start')
    end = request.args.get('end')
    group_by = request.args.get('group_by', 'date')
    
    try:
        # TODO: 实现趋势数据查询
        # 这里返回模拟数据
        trend = [
            {'date': '2026-03-10', 'count': 15},
            {'date': '2026-03-11', 'count': 18},
            {'date': '2026-03-12', 'count': 20},
            {'date': '2026-03-13', 'count': 17},
            {'date': '2026-03-14', 'count': 10}
        ]
        
        return api_response({
            'trend': trend,
            'group_by': group_by
        })
        
    except Exception as e:
        error(f"获取趋势失败：{str(e)}")
        return api_error('TREND_ERROR', f'获取趋势失败：{str(e)}', 500)


# ==================== Token 统计 API ====================

@app.route('/api/token-stats', methods=['GET'])
@rate_limit
@cached(ttl=300, prefix="token_stats")
def api_get_token_stats():
    """
    获取 Token 消耗统计
    
    Query Parameters:
        month (str): 月份 (YYYY-MM), 默认为当前月份
    
    Returns:
        JSON: Token 统计数据
    """
    from datetime import datetime
    
    month = request.args.get('month', datetime.now().strftime('%Y-%m'))
    
    try:
        stats_file = Path(config.STATS_DIR) / f"{month}.jsonl"
        
        if not stats_file.exists():
            return api_error('NO_DATA', f'No data for month: {month}', 404)
        
        stats = []
        total_tokens = 0
        total_news = 0
        total_days = 0
        
        with open(stats_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    stats.append(data)
                    total_tokens += data.get('total_tokens', 0)
                    total_news += data.get('news_count', 0)
                    total_days += 1
        
        # 计算平均值
        avg_tokens = total_tokens // total_days if total_days > 0 else 0
        avg_news = total_news // total_days if total_days > 0 else 0
        
        # 估算成本 (按 $0.002/1K tokens)
        estimated_cost = total_tokens * 0.000002
        
        return api_response({
            'success': True,
            'month': month,
            'data': stats,
            'summary': {
                'total_days': total_days,
                'total_tokens': total_tokens,
                'total_news': total_news,
                'avg_tokens_per_day': avg_tokens,
                'avg_news_per_day': avg_news,
                'estimated_cost_usd': round(estimated_cost, 4)
            }
        })
        
    except Exception as e:
        error(f"获取 Token 统计失败：{str(e)}")
        return api_error('TOKEN_STATS_ERROR', f'获取 Token 统计失败：{str(e)}', 500)


@app.route('/api/token-stats/daily', methods=['GET'])
@rate_limit
def api_get_daily_token_stats():
    """
    获取指定日期的 Token 统计
    
    Query Parameters:
        date (str): 日期 (YYYY-MM-DD), 默认为今天
    
    Returns:
        JSON: 单日 Token 统计数据
    """
    from datetime import datetime
    
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    try:
        # 从月度文件中查找指定日期的数据
        month = date[:7]  # YYYY-MM
        stats_file = Path(config.STATS_DIR) / f"{month}.jsonl"
        
        if not stats_file.exists():
            return api_error('NO_DATA', f'No data for month: {month}', 404)
        
        target_data = None
        with open(stats_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    if data.get('date') == date:
                        target_data = data
                        break
        
        if not target_data:
            return api_error('NO_DATA', f'No data for date: {date}', 404)
        
        # 估算成本
        estimated_cost = target_data.get('total_tokens', 0) * 0.000002
        target_data['estimated_cost_usd'] = round(estimated_cost, 4)
        
        return api_response({
            'success': True,
            'date': date,
            'data': target_data
        })
        
    except Exception as e:
        error(f"获取单日 Token 统计失败：{str(e)}")
        return api_error('DAILY_TOKEN_STATS_ERROR', f'获取单日 Token 统计失败：{str(e)}', 500)


# ==================== 缓存 API ====================

@app.route('/api/cache/stats', methods=['GET'])
@rate_limit
def api_cache_stats():
    """
    获取缓存统计
    
    Returns:
        JSON: 缓存统计信息
    """
    try:
        stats = cache.get_stats()
        
        return api_response({
            'cache': stats
        })
        
    except Exception as e:
        error(f"获取缓存统计失败：{str(e)}")
        return api_error('CACHE_ERROR', f'获取缓存统计失败：{str(e)}', 500)


@app.route('/api/cache/clear', methods=['POST'])
@rate_limit
def api_cache_clear():
    """
    清空缓存
    
    Returns:
        JSON: 操作结果
    """
    try:
        cache.clear()
        
        return api_response({
            'message': '缓存已清空'
        })
        
    except Exception as e:
        error(f"清空缓存失败：{str(e)}")
        return api_error('CACHE_CLEAR_ERROR', f'清空缓存失败：{str(e)}', 500)


# ==================== 健康检查 ====================

@app.route('/api/health', methods=['GET'])
def api_health():
    """
    健康检查
    
    Returns:
        JSON: 服务状态
    """
    return api_response({
        'status': 'healthy',
        'version': 'v2.2',
        'timestamp': datetime.now().isoformat()
    })


# ==================== 错误处理 ====================

@app.errorhandler(404)
def not_found(error):
    """404 错误处理"""
    return api_error('NOT_FOUND', '接口不存在', 404)


@app.errorhandler(500)
def internal_error(error):
    """500 错误处理"""
    return api_error('INTERNAL_ERROR', '服务器内部错误', 500)


# ==================== 主函数 ====================

def main():
    """主函数"""
    if not FLASK_AVAILABLE:
        error("Flask 未安装，无法启动 API 服务")
        return
    
    info("=" * 60)
    info("Guangchu RESTful API Service")
    info("=" * 60)
    info(f"版本：v2.2")
    info(f"速率限制：{RATE_LIMIT} 请求/分钟")
    info(f"API 端点:")
    info(f"  - GET  /api/search")
    info(f"  - GET  /api/search/suggestions")
    info(f"  - GET  /api/search/history")
    info(f"  - GET  /api/news")
    info(f"  - GET  /api/news/<id>")
    info(f"  - GET  /api/stats")
    info(f"  - GET  /api/stats/trend")
    info(f"  - GET  /api/cache/stats")
    info(f"  - POST /api/cache/clear")
    info(f"  - GET  /api/health")
    info("=" * 60)
    
    # 启动服务
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
