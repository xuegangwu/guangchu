#!/usr/bin/env python3
"""
光储龙虾 - GitHub Pages 部署脚本
自动生成日记页面并推送到 GitHub Pages
"""

import subprocess
import shutil
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = Path("/home/admin/openclaw/workspace/projects/光储龙虾")
WEB_DIR = WORKSPACE / "web"
GITHUB_PAGES_DIR = WORKSPACE / "github-pages"
DIARY_DIR = WORKSPACE / "diary"

def run_command(cmd, cwd=None):
    """运行 shell 命令"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout
    except Exception as e:
        return False, str(e)

def create_github_pages_structure():
    """创建 GitHub Pages 目录结构"""
    print("📁 创建 GitHub Pages 目录结构...")
    
    # 创建目录
    GITHUB_PAGES_DIR.mkdir(exist_ok=True)
    (GITHUB_PAGES_DIR / "diary").mkdir(exist_ok=True)
    
    # 复制 Web 文件
    web_files = [
        "diary-list.html",
        "diary-single.html",
        "3wan-style.html",
        "diary-hub.html",
        "project-intro.html"
    ]
    
    for file in web_files:
        src = WEB_DIR / file
        if src.exists():
            shutil.copy2(src, GITHUB_PAGES_DIR / file)
            print(f"  ✅ 复制 {file}")
    
    # 复制日记文件
    if DIARY_DIR.exists():
        for diary_file in DIARY_DIR.glob("*.html"):
            shutil.copy2(diary_file, GITHUB_PAGES_DIR / "diary" / diary_file.name)
            print(f"  ✅ 复制日记 {diary_file.name}")
    
    # 创建 index.html（自动跳转到日记列表）
    index_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url=diary-list.html">
    <title>光储龙虾 - 开发日记</title>
</head>
<body>
    <p>正在跳转到 <a href="diary-list.html">日记列表页</a>...</p>
</body>
</html>
"""
    
    with open(GITHUB_PAGES_DIR / "index.html", 'w', encoding='utf-8') as f:
        f.write(index_html)
    print("  ✅ 创建 index.html")
    
    return True

def deploy_to_github_pages():
    """部署到 GitHub Pages"""
    print("\n🚀 部署到 GitHub Pages...")
    
    # 检查 Git 状态
    success, output = run_command("git status", cwd=WORKSPACE)
    if not success:
        print("❌ 不是 Git 仓库")
        return False
    
    # 添加 github-pages 目录
    print("  📝 添加文件到 Git...")
    run_command("git add github-pages/", cwd=WORKSPACE)
    
    # 创建 orphan 分支（如果不存在）
    success, _ = run_command("git rev-parse --verify gh-pages", cwd=WORKSPACE)
    if not success:
        print("  🌿 创建 gh-pages 分支...")
        run_command("git checkout --orphan gh-pages", cwd=WORKSPACE)
        run_command("git reset --hard", cwd=WORKSPACE)
        run_command("git checkout main", cwd=WORKSPACE)
    
    # 使用 git subtree 推送
    print("  📤 推送到 gh-pages 分支...")
    success, output = run_command(
        "git subtree push --prefix github-pages origin gh-pages",
        cwd=WORKSPACE
    )
    
    if success:
        print("  ✅ 推送成功！")
        return True
    else:
        print(f"  ⚠️  推送失败：{output}")
        # 尝试直接复制方式
        print("  🔄 尝试备用方案...")
        
        # 切换到 gh-pages 分支
        run_command("git checkout gh-pages", cwd=WORKSPACE)
        
        # 复制文件
        import os
        for root, dirs, files in os.walk(GITHUB_PAGES_DIR):
            for file in files:
                src = Path(root) / file
                rel_path = src.relative_to(GITHUB_PAGES_DIR)
                dst = WORKSPACE / rel_path
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                print(f"    ✅ 复制 {rel_path}")
        
        # 提交并推送
        run_command("git add .", cwd=WORKSPACE)
        run_command(f'git commit -m "chore: 更新日记页面 {datetime.now().strftime("%Y-%m-%d")}"', cwd=WORKSPACE)
        success, output = run_command("git push origin gh-pages", cwd=WORKSPACE)
        
        # 切回主分支
        run_command("git checkout main", cwd=WORKSPACE)
        
        if success:
            print("  ✅ 推送成功！")
            return True
        else:
            print(f"  ❌ 推送失败：{output}")
            return False

def print_deploy_info():
    """打印部署信息"""
    print("\n" + "=" * 60)
    print("✅ GitHub Pages 部署完成！")
    print("=" * 60)
    print("\n📍 访问地址:")
    print("   https://xuegangwu.github.io/guangchu/")
    print("   https://xuegangwu.github.io/guangchu/diary-list.html")
    print("   https://xuegangwu.github.io/guangchu/diary/")
    print("\n📁 文件结构:")
    print("   github-pages/")
    print("   ├── index.html          # 自动跳转到日记列表")
    print("   ├── diary-list.html     # 日记列表页")
    print("   ├── diary-single.html   # 单篇日记页")
    print("   ├── 3wan-style.html     # sanwan.ai 风格")
    print("   ├── diary-hub.html      # 日记中心")
    print("   └── diary/")
    print("       ├── 2026-03-12.html")
    print("       └── ...")
    print("\n🔄 自动部署:")
    print("   每天 18:00 自动生成并推送")
    print("=" * 60)

def main():
    print("=" * 60)
    print("🦞 光储龙虾 - GitHub Pages 部署")
    print("=" * 60)
    
    # 1. 创建目录结构
    if not create_github_pages_structure():
        print("❌ 创建目录结构失败")
        return False
    
    # 2. 部署到 GitHub Pages
    if not deploy_to_github_pages():
        print("❌ 部署失败")
        return False
    
    # 3. 打印信息
    print_deploy_info()
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
