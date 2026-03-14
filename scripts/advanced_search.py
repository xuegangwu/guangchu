#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
光储龙虾 - 高级搜索功能
支持关键词高亮、过滤、排序

v2.2 新增功能:
- 关键词高亮
- 多条件过滤（日期/区域/类型）
- 结果排序（相关性/时间）
- 搜索历史
"""

import sqlite3
import os
import sys
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.logger import logger, info, debug, error, warning
from scripts.config import get_config


class AdvancedSearch:
    """高级搜索类"""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        初始化搜索
        
        Args:
            db_path: 数据库路径，默认使用配置中的路径
        """
        config = get_config()
        self.db_path = db_path or config.DATABASE_URL
        self.conn = None
        self.cursor = None
        self.search_history = []
        
    def connect(self):
        """连接数据库"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            debug(f"数据库连接成功：{self.db_path}")
        except Exception as e:
            error(f"数据库连接失败：{str(e)}")
            raise
    
    def disconnect(self):
        """断开数据库连接"""
        if self.conn:
            self.conn.close()
            debug("数据库连接已关闭")
    
    def highlight_keywords(self, text: str, keywords: List[str]) -> str:
        """
        关键词高亮
        
        Args:
            text: 原始文本
            keywords: 关键词列表
        
        Returns:
            高亮后的文本
        """
        if not keywords or not text:
            return text
        
        highlighted = text
        for keyword in keywords:
            if keyword:
                # 不区分大小写高亮
                import re
                pattern = re.compile(re.escape(keyword), re.IGNORECASE)
                highlighted = pattern.sub(f'<mark>{keyword}</mark>', highlighted)
        
        return highlighted
    
    def search(
        self,
        query: str,
        filters: Optional[Dict] = None,
        sort_by: str = 'relevance',
        limit: int = 20,
        highlight: bool = True
    ) -> List[Dict]:
        """
        高级搜索
        
        Args:
            query: 搜索关键词
            filters: 过滤条件 {
                'date_from': '2026-03-01',
                'date_to': '2026-03-31',
                'region': 'US',
                'type': 'policy'
            }
            sort_by: 排序方式 ('relevance' | 'date')
            limit: 返回结果数量
            highlight: 是否高亮关键词
        
        Returns:
            搜索结果列表
        """
        try:
            self.connect()
            
            # 构建 SQL 查询
            base_sql = """
                SELECT rowid, title, url, date, region, type, summary, source
                FROM news
                WHERE news MATCH ?
            """
            
            # 添加过滤条件
            conditions = []
            params = [query]
            
            if filters:
                if 'date_from' in filters and filters['date_from']:
                    conditions.append("date >= ?")
                    params.append(filters['date_from'])
                
                if 'date_to' in filters and filters['date_to']:
                    conditions.append("date <= ?")
                    params.append(filters['date_to'])
                
                if 'region' in filters and filters['region']:
                    conditions.append("region = ?")
                    params.append(filters['region'])
                
                if 'type' in filters and filters['type']:
                    conditions.append("type = ?")
                    params.append(filters['type'])
            
            if conditions:
                base_sql += " AND " + " AND ".join(conditions)
            
            # 添加排序
            if sort_by == 'date':
                base_sql += " ORDER BY date DESC"
            else:  # relevance
                base_sql += " ORDER BY rank"
            
            # 添加限制
            base_sql += " LIMIT ?"
            params.append(limit)
            
            debug(f"执行搜索：{base_sql}, 参数：{params}")
            
            # 执行查询
            self.cursor.execute(base_sql, params)
            rows = self.cursor.fetchall()
            
            # 处理结果
            results = []
            keywords = query.split()
            
            for row in rows:
                item = {
                    'id': row['rowid'],
                    'title': row['title'],
                    'url': row['url'],
                    'date': row['date'],
                    'region': row['region'],
                    'type': row['type'],
                    'source': row['source'],
                    'summary': row['summary']
                }
                
                # 关键词高亮
                if highlight:
                    item['title_highlighted'] = self.highlight_keywords(
                        item['title'], keywords
                    )
                    item['summary_highlighted'] = self.highlight_keywords(
                        item['summary'], keywords
                    )
                
                results.append(item)
            
            # 记录搜索历史
            self._add_to_history(query, filters, len(results))
            
            info(f"搜索完成：'{query}', 结果数：{len(results)}")
            
            return results
            
        except Exception as e:
            error(f"搜索失败：{str(e)}")
            return []
        finally:
            self.disconnect()
    
    def _add_to_history(self, query: str, filters: Dict, result_count: int):
        """
        添加搜索历史
        
        Args:
            query: 搜索词
            filters: 过滤条件
            result_count: 结果数量
        """
        history_item = {
            'query': query,
            'filters': filters,
            'result_count': result_count,
            'timestamp': datetime.now().isoformat()
        }
        self.search_history.append(history_item)
        
        # 只保留最近 10 条
        if len(self.search_history) > 10:
            self.search_history = self.search_history[-10:]
    
    def get_search_history(self) -> List[Dict]:
        """获取搜索历史"""
        return self.search_history
    
    def clear_search_history(self):
        """清空搜索历史"""
        self.search_history = []
        info("搜索历史已清空")
    
    def get_search_suggestions(self, prefix: str, limit: int = 5) -> List[str]:
        """
        获取搜索建议
        
        Args:
            prefix: 搜索前缀
            limit: 建议数量
        
        Returns:
            搜索建议列表
        """
        try:
            self.connect()
            
            # 从历史中获取建议
            suggestions = []
            for item in reversed(self.search_history):
                if item['query'].lower().startswith(prefix.lower()):
                    suggestions.append(item['query'])
                    if len(suggestions) >= limit:
                        break
            
            return suggestions
            
        except Exception as e:
            error(f"获取搜索建议失败：{str(e)}")
            return []
        finally:
            self.disconnect()
    
    def search_stats(self) -> Dict:
        """
        获取搜索统计信息
        
        Returns:
            统计信息字典
        """
        try:
            self.connect()
            
            stats = {
                'total_news': 0,
                'regions': {},
                'types': {},
                'date_range': {
                    'from': None,
                    'to': None
                }
            }
            
            # 总新闻数
            self.cursor.execute("SELECT COUNT(*) FROM news")
            stats['total_news'] = self.cursor.fetchone()[0]
            
            # 区域分布
            self.cursor.execute("""
                SELECT region, COUNT(*) as count 
                FROM news 
                GROUP BY region 
                ORDER BY count DESC
            """)
            stats['regions'] = {
                row['region']: row['count'] 
                for row in self.cursor.fetchall()
            }
            
            # 类型分布
            self.cursor.execute("""
                SELECT type, COUNT(*) as count 
                FROM news 
                GROUP BY type 
                ORDER BY count DESC
            """)
            stats['types'] = {
                row['type']: row['count'] 
                for row in self.cursor.fetchall()
            }
            
            # 日期范围
            self.cursor.execute("""
                SELECT MIN(date) as min_date, MAX(date) as max_date 
                FROM news
            """)
            row = self.cursor.fetchone()
            stats['date_range'] = {
                'from': row['min_date'],
                'to': row['max_date']
            }
            
            return stats
            
        except Exception as e:
            error(f"获取统计信息失败：{str(e)}")
            return {}
        finally:
            self.disconnect()


def main():
    """测试高级搜索功能"""
    info("=" * 60)
    info("Guangchu - 高级搜索功能测试")
    info("=" * 60)
    
    search = AdvancedSearch()
    
    # 测试 1: 基础搜索
    info("\n测试 1: 基础搜索")
    results = search.search("solar", limit=5)
    info(f"搜索结果：{len(results)} 条")
    for item in results[:3]:
        info(f"  - {item['title']}")
    
    # 测试 2: 带过滤的搜索
    info("\n测试 2: 带过滤的搜索")
    results = search.search(
        "energy",
        filters={'region': 'US'},
        limit=5
    )
    info(f"搜索结果：{len(results)} 条")
    
    # 测试 3: 关键词高亮
    info("\n测试 3: 关键词高亮")
    text = "Solar energy is important for renewable energy"
    highlighted = search.highlight_keywords(text, ["solar", "energy"])
    info(f"高亮结果：{highlighted}")
    
    # 测试 4: 搜索统计
    info("\n测试 4: 搜索统计")
    stats = search.search_stats()
    info(f"总新闻数：{stats.get('total_news', 0)}")
    info(f"区域分布：{stats.get('regions', {})}")
    
    # 测试 5: 搜索历史
    info("\n测试 5: 搜索历史")
    history = search.get_search_history()
    info(f"搜索历史：{len(history)} 条")
    
    info("\n" + "=" * 60)
    info("测试完成！")
    info("=" * 60)


if __name__ == '__main__':
    main()
