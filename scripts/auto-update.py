#!/usr/bin/env python3
"""
Guangchu - 自动更新索引（增强版）
整合新闻抓取、多语言翻译和索引构建
"""

import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

def run_script(script_name, description):
    """运行脚本"""
    print(f"\n{'='*60}")
    print(f"📌 {description}")
    print(f"{'='*60}\n")
    
    script_path = SCRIPT_DIR / script_name
    
    if not script_path.exists():
        print(f"❌ 脚本不存在：{script_path}")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=False
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 脚本执行失败：{e}")
        return False

def main():
    print("=" * 60)
    print("🔄 Guangchu - 自动更新索引")
    print("=" * 60)
    
    success = True
    
    # 1. 抓取英文新闻
    if not run_script("fetch-news.py", "步骤 1: 抓取英文新闻（PV Magazine, Energy Storage News）"):
        success = False
    
    # 2. 抓取中文新闻（可选）
    print(f"\n{'='*60}")
    print("📌 步骤 2: 抓取中文新闻（北极星储能网，索比光伏网）")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / "fetch-chinese-news.py")],
            check=False,  # 不抛出异常，中文源可选
            capture_output=False
        )
        if result.returncode != 0:
            print("⚠️ 中文新闻抓取失败，继续后续步骤...")
    except Exception as e:
        print(f"⚠️ 中文新闻抓取异常：{e}")
    
    # 3. 构建搜索索引
    if not run_script("build-index.py", "步骤 3: 构建搜索索引"):
        success = False
    
    # 完成
    print(f"\n{'='*60}")
    if success:
        print("✅ 自动更新完成！")
    else:
        print("⚠️ 自动更新完成（部分步骤失败）")
    print(f"{'='*60}")
    print("\n📊 下一步:")
    print("   - 查看报告：python3 scripts/search.py --stats")
    print("   - Web 搜索：python3 scripts/web-search.py")
    print()

if __name__ == "__main__":
    main()
