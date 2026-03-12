#!/usr/bin/env python3
"""
Guangchu - 构建搜索索引
使用 SQLite FTS5 全文搜索引擎
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("/home/admin/openclaw/workspace/projects/guangchu/search.db")
RAW_DIR = Path("/home/admin/openclaw/workspace/projects/guangchu/raw")

def init_db(conn):
    """初始化数据库和 FTS5 索引表"""
    cursor = conn.cursor()
    
    # 创建 FTS5 虚拟表（全文搜索）
    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS news_fts USING fts5(
            title,
            summary,
            content='news',
            content_rowid='id'
        )
    """)
    
    # 创建主表（存储结构化数据）
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY,
            title TEXT,
            link TEXT,
            published TEXT,
            summary TEXT,
            source TEXT,
            region TEXT,
            type TEXT,
            collected_at TEXT
        )
    """)
    
    # 创建索引（加速筛选）
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_region ON news(region)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_type ON news(type)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_source ON news(source)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_published ON news(published)")
    
    # 创建触发器（同步 FTS 索引）
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS news_ai AFTER INSERT ON news BEGIN
            INSERT INTO news_fts(rowid, title, summary) VALUES (new.id, new.title, new.summary);
        END
    """)
    
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS news_ad AFTER DELETE ON news BEGIN
            INSERT INTO news_fts(news_fts, rowid, title, summary) VALUES('delete', old.id, old.title, old.summary);
        END
    """)
    
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS news_au AFTER UPDATE ON news BEGIN
            INSERT INTO news_fts(news_fts, rowid, title, summary) VALUES('delete', old.id, old.title, old.summary);
            INSERT INTO news_fts(rowid, title, summary) VALUES (new.id, new.title, new.summary);
        END
    """)
    
    conn.commit()

def load_json_files():
    """加载所有 JSON 文件"""
    all_news = []
    
    if not RAW_DIR.exists():
        print(f"警告：目录 {RAW_DIR} 不存在")
        return all_news
    
    for json_file in sorted(RAW_DIR.glob("*.json")):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # 从文件名提取日期
            date_str = json_file.stem  # 如 2026-03-12
            
            for item in data:
                item["collected_at"] = date_str
                all_news.append(item)
            
            print(f"  加载 {json_file.name}: {len(data)} 条")
        except Exception as e:
            print(f"  错误：{json_file.name}: {e}")
    
    return all_news

def build_index():
    """构建搜索索引"""
    print("=" * 60)
    print("Guangchu - 构建搜索索引")
    print("=" * 60)
    
    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    
    # 初始化表结构
    init_db(conn)
    
    # 清空旧数据
    cursor = conn.cursor()
    cursor.execute("DELETE FROM news")
    cursor.execute("DELETE FROM news_fts")
    conn.commit()
    
    # 加载数据
    print("\n加载原始数据...")
    all_news = load_json_files()
    
    if not all_news:
        print("没有找到数据，请先运行 fetch-news.py")
        return
    
    # 插入数据
    print(f"\n插入 {len(all_news)} 条记录到索引...")
    
    for item in all_news:
        cursor.execute("""
            INSERT INTO news (title, link, published, summary, source, region, type, collected_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item.get("title", ""),
            item.get("link", ""),
            item.get("published", ""),
            item.get("summary", ""),
            item.get("source", ""),
            item.get("region", ""),
            item.get("type", ""),
            item.get("collected_at", "")
        ))
    
    conn.commit()
    
    # 优化 FTS 索引
    cursor.execute("INSERT INTO news_fts(news_fts) VALUES('optimize')")
    conn.commit()
    
    # 统计信息
    cursor.execute("SELECT COUNT(*) FROM news")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT region, COUNT(*) FROM news GROUP BY region ORDER BY COUNT(*) DESC")
    regions = cursor.fetchall()
    
    cursor.execute("SELECT type, COUNT(*) FROM news GROUP BY type ORDER BY COUNT(*) DESC")
    types = cursor.fetchall()
    
    cursor.execute("SELECT source, COUNT(*) FROM news GROUP BY source ORDER BY COUNT(*) DESC")
    sources = cursor.fetchall()
    
    print("\n" + "=" * 60)
    print("索引构建完成！")
    print("=" * 60)
    print(f"📊 总记录数：{total}")
    print(f"📁 数据库：{DB_PATH}")
    
    print("\n📍 区域分布:")
    for region, count in regions:
        print(f"   {region}: {count} 条")
    
    print("\n📋 类型分布:")
    for type_, count in types:
        print(f"   {type_}: {count} 条")
    
    print("\n📰 来源分布:")
    for source, count in sources:
        print(f"   {source}: {count} 条")
    
    conn.close()
    print("\n✅ 完成！")

if __name__ == "__main__":
    build_index()
