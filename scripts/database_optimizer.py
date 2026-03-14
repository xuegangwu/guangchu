#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
光储龙虾 - 数据库性能优化
优化索引、查询性能、缓存机制

v2.2 Phase 2 新增:
- 数据库索引优化
- 查询性能分析
- 自动优化建议
"""

import sqlite3
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.logger import logger, info, debug, error, warning
from scripts.config import get_config


class DatabaseOptimizer:
    """数据库优化器"""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        初始化优化器
        
        Args:
            db_path: 数据库路径
        """
        config = get_config()
        self.db_path = db_path or config.DATABASE_URL
        self.conn = None
        self.cursor = None
    
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
    
    def analyze_database(self) -> Dict:
        """
        分析数据库状态
        
        Returns:
            数据库分析结果
        """
        try:
            self.connect()
            
            stats = {
                'total_tables': 0,
                'total_rows': 0,
                'database_size': 0,
                'indexes': [],
                'tables': {}
            }
            
            # 获取所有表
            self.cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
            """)
            tables = [row[0] for row in self.cursor.fetchall()]
            stats['total_tables'] = len(tables)
            
            # 分析每个表
            for table in tables:
                try:
                    # 行数
                    self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    row_count = self.cursor.fetchone()[0]
                    stats['total_rows'] += row_count
                    
                    # 表结构
                    self.cursor.execute(f"PRAGMA table_info({table})")
                    columns = [col[1] for col in self.cursor.fetchall()]
                    
                    stats['tables'][table] = {
                        'rows': row_count,
                        'columns': columns
                    }
                except Exception as e:
                    warning(f"分析表 {table} 失败：{str(e)}")
            
            # 获取索引信息
            for table in tables:
                try:
                    self.cursor.execute(f"PRAGMA index_list({table})")
                    indexes = self.cursor.fetchall()
                    for idx in indexes:
                        stats['indexes'].append({
                            'table': table,
                            'name': idx[1],
                            'unique': idx[2]
                        })
                except Exception as e:
                    warning(f"获取表 {table} 索引失败：{str(e)}")
            
            # 数据库文件大小
            if os.path.exists(self.db_path):
                stats['database_size'] = os.path.getsize(self.db_path)
            
            return stats
            
        except Exception as e:
            error(f"数据库分析失败：{str(e)}")
            return {}
        finally:
            self.disconnect()
    
    def create_indexes(self):
        """创建优化索引"""
        try:
            self.connect()
            
            info("开始创建优化索引...")
            
            # 1. 日期索引（加速时间范围查询）
            self._create_index_if_not_exists(
                "news", "idx_news_date", "date"
            )
            
            # 2. 区域索引（加速区域过滤）
            self._create_index_if_not_exists(
                "news", "idx_news_region", "region"
            )
            
            # 3. 类型索引（加速类型过滤）
            self._create_index_if_not_exists(
                "news", "idx_news_type", "type"
            )
            
            # 4. 组合索引（加速多条件查询）
            self._create_index_if_not_exists(
                "news", "idx_news_region_type", "region, type"
            )
            
            # 5. 日期 + 区域组合索引
            self._create_index_if_not_exists(
                "news", "idx_news_date_region", "date, region"
            )
            
            # 6. 来源索引
            self._create_index_if_not_exists(
                "news", "idx_news_source", "source"
            )
            
            info("✅ 索引创建完成")
            
            self.conn.commit()
            
        except Exception as e:
            error(f"创建索引失败：{str(e)}")
            self.conn.rollback()
        finally:
            self.disconnect()
    
    def _create_index_if_not_exists(self, table: str, index_name: str, columns: str):
        """
        如果索引不存在则创建
        
        Args:
            table: 表名
            index_name: 索引名
            columns: 列名（可多列，逗号分隔）
        """
        try:
            # 检查索引是否已存在
            self.cursor.execute(f"""
                SELECT name FROM sqlite_master 
                WHERE type='index' AND name=?
            """, (index_name,))
            
            if self.cursor.fetchone():
                debug(f"索引 {index_name} 已存在，跳过")
                return
            
            # 创建索引
            sql = f"CREATE INDEX {index_name} ON {table} ({columns})"
            self.cursor.execute(sql)
            info(f"✅ 创建索引：{index_name} ON {table}({columns})")
            
        except Exception as e:
            error(f"创建索引 {index_name} 失败：{str(e)}")
    
    def vacuum_database(self):
        """
        清理数据库碎片，优化存储空间
        """
        try:
            self.connect()
            
            info("开始清理数据库碎片...")
            
            # 获取清理前大小
            before_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
            
            # 执行 VACUUM
            self.cursor.execute("VACUUM")
            self.conn.commit()
            
            # 获取清理后大小
            after_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
            
            # 计算节省空间
            saved = before_size - after_size
            saved_percent = (saved / before_size * 100) if before_size > 0 else 0
            
            info(f"✅ 数据库清理完成")
            info(f"  清理前：{before_size / 1024:.2f} KB")
            info(f"  清理后：{after_size / 1024:.2f} KB")
            info(f"  节省：{saved / 1024:.2f} KB ({saved_percent:.1f}%)")
            
        except Exception as e:
            error(f"数据库清理失败：{str(e)}")
            self.conn.rollback()
        finally:
            self.disconnect()
    
    def analyze_queries(self):
        """分析查询性能"""
        try:
            self.connect()
            
            info("分析查询性能...")
            
            # 启用查询计划分析
            test_queries = [
                "SELECT * FROM news WHERE date >= '2026-03-01'",
                "SELECT * FROM news WHERE region = 'US'",
                "SELECT * FROM news WHERE type = 'policy'",
                "SELECT * FROM news WHERE region = 'US' AND type = 'policy'",
                "SELECT * FROM news WHERE news MATCH 'solar'"
            ]
            
            for query in test_queries:
                try:
                    # 获取查询计划
                    self.cursor.execute(f"EXPLAIN QUERY PLAN {query}")
                    plan = self.cursor.fetchall()
                    
                    # 分析是否使用了索引
                    uses_index = any('USING INDEX' in str(row) or 'SEARCH' in str(row) for row in plan)
                    
                    status = "✅" if uses_index else "⚠️"
                    info(f"{status} 查询：{query[:50]}...")
                    info(f"   使用索引：{'是' if uses_index else '否'}")
                    
                except Exception as e:
                    warning(f"分析查询失败：{str(e)}")
            
        except Exception as e:
            error(f"查询分析失败：{str(e)}")
        finally:
            self.disconnect()
    
    def get_optimization_suggestions(self) -> List[str]:
        """
        获取优化建议
        
        Returns:
            优化建议列表
        """
        suggestions = []
        
        try:
            stats = self.analyze_database()
            
            # 检查索引
            if len(stats.get('indexes', [])) < 5:
                suggestions.append("建议创建更多索引以优化查询性能")
            
            # 检查表大小
            for table, info in stats.get('tables', {}).items():
                if info['rows'] > 10000:
                    suggestions.append(f"表 {table} 数据量较大 ({info['rows']} 行)，建议定期清理")
            
            # 检查数据库大小
            if stats.get('database_size', 0) > 100 * 1024 * 1024:  # 100MB
                suggestions.append("数据库文件较大，建议执行 VACUUM 清理")
            
            if not suggestions:
                suggestions.append("数据库状态良好，无需优化")
            
        except Exception as e:
            error(f"获取优化建议失败：{str(e)}")
            suggestions.append("无法获取优化建议")
        
        return suggestions
    
    def optimize_all(self):
        """执行全面优化"""
        info("=" * 60)
        info("Guangchu - 数据库全面优化")
        info("=" * 60)
        info(f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 1. 分析数据库
        info("\n步骤 1: 分析数据库状态")
        stats = self.analyze_database()
        info(f"表数量：{stats.get('total_tables', 0)}")
        info(f"总行数：{stats.get('total_rows', 0)}")
        info(f"数据库大小：{stats.get('database_size', 0) / 1024:.2f} KB")
        
        # 2. 创建索引
        info("\n步骤 2: 创建优化索引")
        self.create_indexes()
        
        # 3. 查询分析
        info("\n步骤 3: 分析查询性能")
        self.analyze_queries()
        
        # 4. 清理碎片
        info("\n步骤 4: 清理数据库碎片")
        self.vacuum_database()
        
        # 5. 优化建议
        info("\n步骤 5: 优化建议")
        suggestions = self.get_optimization_suggestions()
        for suggestion in suggestions:
            info(f"  - {suggestion}")
        
        info(f"\n完成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        info("=" * 60)
        info("✅ 数据库优化完成！")
        info("=" * 60)


def main():
    """主函数"""
    optimizer = DatabaseOptimizer()
    optimizer.optimize_all()


if __name__ == '__main__':
    main()
