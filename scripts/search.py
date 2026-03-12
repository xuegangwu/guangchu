#!/usr/bin/env python3
"""
光储龙虾 - 搜索工具
支持关键词、区域、类型、时间范围等筛选
"""

import argparse
import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("/home/admin/openclaw/workspace/projects/光储龙虾/search.db")

def search(
    keyword=None,
    region=None,
    type_=None,
    source=None,
    date_from=None,
    date_to=None,
    limit=20,
    highlight=False
):
    """搜索新闻"""
    
    if not DB_PATH.exists():
        print("❌ 索引不存在，请先运行：python scripts/build-index.py")
        return []
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # 构建查询
    conditions = []
    params = []
    
    # FTS5 全文搜索（支持英文）+ LIKE 匹配（支持中文）
    if keyword:
        # 先尝试 FTS5 搜索（英文效果好）
        fts_condition = "id IN (SELECT rowid FROM news_fts WHERE news_fts MATCH ?)"
        # 同时添加 LIKE 匹配（中文效果好）
        like_condition = "(title LIKE ? OR summary LIKE ?)"
        like_keyword = f"%{keyword}%"
        conditions.append(f"({fts_condition} OR {like_condition})")
        params.extend([keyword, like_keyword, like_keyword])
    
    # 区域筛选
    if region:
        conditions.append("region = ?")
        params.append(region)
    
    # 类型筛选
    if type_:
        conditions.append("type = ?")
        params.append(type_)
    
    # 来源筛选
    if source:
        conditions.append("source = ?")
        params.append(source)
    
    # 日期范围筛选
    if date_from:
        conditions.append("collected_at >= ?")
        params.append(date_from)
    
    if date_to:
        conditions.append("collected_at <= ?")
        params.append(date_to)
    
    # 组合查询
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
    results = cursor.fetchall()
    
    conn.close()
    
    return results

def format_result(row, highlight=False):
    """格式化单条结果"""
    output = []
    
    # 标题
    output.append(f"\n{'='*60}")
    output.append(f"📌 {row['title']}")
    output.append(f"{'='*60}")
    
    # 元信息
    output.append(f"📅 日期：{row['collected_at']} | 发布：{row['published'][:10] if row['published'] else 'N/A'}")
    output.append(f"📍 区域：{row['region']} | 类型：{row['type']}")
    output.append(f"📰 来源：{row['source']}")
    
    # 摘要
    if row['summary']:
        summary = row['summary'][:300] + "..." if len(row['summary']) > 300 else row['summary']
        output.append(f"\n📝 摘要:\n{summary}")
    
    # 链接
    output.append(f"\n🔗 链接：{row['link']}")
    
    return "\n".join(output)

def format_result_compact(row):
    """紧凑格式（列表）"""
    return f"[{row['collected_at']}] [{row['type']}] [{row['region']}] {row['title']}"

def main():
    parser = argparse.ArgumentParser(
        description="🔍 光储龙虾搜索工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python search.py "储能电池"                    # 关键词搜索
  python search.py -t 产品 -r Europe             # 按类型和区域筛选
  python search.py "太阳能" --from 2026-03-01    # 日期范围搜索
  python search.py -s "PV Magazine" -l 5         # 按来源筛选，限制 5 条
  python search.py --export results.json         # 导出结果
        """
    )
    
    parser.add_argument("keyword", nargs="?", help="搜索关键词（支持 FTS5 语法）")
    parser.add_argument("-t", "--type", dest="type_", help="类型筛选：政策/产品/项目/其他")
    parser.add_argument("-r", "--region", help="区域筛选：Europe/US/Global/Japan/Southeast Asia")
    parser.add_argument("-s", "--source", help="来源筛选：PV Magazine/Energy Storage News")
    parser.add_argument("--from", dest="date_from", help="起始日期：YYYY-MM-DD")
    parser.add_argument("--to", dest="date_to", help="结束日期：YYYY-MM-DD")
    parser.add_argument("-l", "--limit", type=int, default=20, help="结果数量限制（默认 20）")
    parser.add_argument("--compact", action="store_true", help="紧凑输出模式")
    parser.add_argument("--export", help="导出结果到 JSON 文件")
    parser.add_argument("--stats", action="store_true", help="显示统计信息")
    
    args = parser.parse_args()
    
    # 显示统计信息
    if args.stats:
        show_stats()
        return
    
    # 执行搜索
    results = search(
        keyword=args.keyword,
        region=args.region,
        type_=args.type_,
        source=args.source,
        date_from=args.date_from,
        date_to=args.date_to,
        limit=args.limit
    )
    
    if not results:
        print("\n❌ 未找到匹配的结果")
        print("\n💡 提示:")
        print("   - 尝试更简单的关键词")
        print("   - 放宽筛选条件")
        print("   - 运行 'python scripts/build-index.py' 更新索引")
        return
    
    # 输出结果
    print(f"\n✅ 找到 {len(results)} 条结果:\n")
    
    if args.compact:
        for row in results:
            print(format_result_compact(row))
    else:
        for row in results:
            print(format_result(row, highlight=True))
    
    # 导出
    if args.export:
        export_data = [dict(row) for row in results]
        with open(args.export, "w", encoding="utf-8") as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        print(f"\n💾 结果已导出到：{args.export}")

def show_stats():
    """显示统计信息"""
    if not DB_PATH.exists():
        print("❌ 索引不存在，请先运行：python scripts/build-index.py")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("\n" + "=" * 60)
    print("📊 光储龙虾搜索索引统计")
    print("=" * 60)
    
    cursor.execute("SELECT COUNT(*) FROM news")
    print(f"\n总记录数：{cursor.fetchone()[0]}")
    
    cursor.execute("SELECT MIN(collected_at), MAX(collected_at) FROM news")
    date_range = cursor.fetchone()
    print(f"日期范围：{date_range[0]} 至 {date_range[1]}")
    
    print("\n📍 区域分布:")
    cursor.execute("SELECT region, COUNT(*) FROM news GROUP BY region ORDER BY COUNT(*) DESC")
    for region, count in cursor.fetchall():
        bar = "█" * (count // 2)
        print(f"   {region:15} {count:3} 条 {bar}")
    
    print("\n📋 类型分布:")
    cursor.execute("SELECT type, COUNT(*) FROM news GROUP BY type ORDER BY COUNT(*) DESC")
    for type_, count in cursor.fetchall():
        bar = "█" * (count // 2)
        print(f"   {type_:15} {count:3} 条 {bar}")
    
    print("\n📰 来源分布:")
    cursor.execute("SELECT source, COUNT(*) FROM news GROUP BY source ORDER BY COUNT(*) DESC")
    for source, count in cursor.fetchall():
        bar = "█" * (count // 2)
        print(f"   {source:15} {count:3} 条 {bar}")
    
    conn.close()
    print()

if __name__ == "__main__":
    main()
