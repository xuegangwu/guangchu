#!/bin/bash

# 光储龙虾 - 构建日记 GitHub Pages
# 生成独立的日记页面，可部署到 GitHub Pages

set -e

echo "🦞 开始构建日记页面..."

# 项目目录
PROJECT_DIR="/home/admin/openclaw/workspace/projects/光储龙虾"
WEB_DIR="$PROJECT_DIR/web"
DIARY_DIR="$PROJECT_DIR/diary"
BUILD_DIR="$PROJECT_DIR/build"

# 清理并创建构建目录
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR/diary"

echo "📁 创建构建目录..."

# 复制 Web 文件
echo "📄 复制 Web 文件..."
cp "$WEB_DIR/diary-list.html" "$BUILD_DIR/" 2>/dev/null || echo "  ⚠️ diary-list.html 不存在"
cp "$WEB_DIR/diary-single.html" "$BUILD_DIR/" 2>/dev/null || echo "  ⚠️ diary-single.html 不存在"
cp "$WEB_DIR/3wan-style.html" "$BUILD_DIR/" 2>/dev/null || echo "  ⚠️ 3wan-style.html 不存在"
cp "$WEB_DIR/diary-hub.html" "$BUILD_DIR/" 2>/dev/null || echo "  ⚠️ diary-hub.html 不存在"

# 复制日记文件
echo "📔 复制日记文件..."
if [ -d "$DIARY_DIR" ]; then
    cp "$DIARY_DIR"/*.html "$BUILD_DIR/diary/" 2>/dev/null || echo "  ℹ️ 暂无日记文件"
fi

# 创建 index.html（自动跳转）
echo "📝 创建 index.html..."
cat > "$BUILD_DIR/index.html" << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url=diary-list.html">
    <title>光储龙虾 - 开发日记</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            text-align: center;
            padding: 40px;
        }
        h1 {
            font-size: 32px;
            margin-bottom: 20px;
        }
        p {
            font-size: 16px;
            opacity: 0.9;
            margin-bottom: 30px;
        }
        a {
            color: white;
            text-decoration: underline;
            font-weight: 600;
        }
        .spinner {
            width: 40px;
            height: 40px;
            border: 4px solid rgba(255,255,255,0.3);
            border-top-color: white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="spinner"></div>
        <h1>🦞 光储龙虾 - 开发日记</h1>
        <p>正在跳转到 <a href="diary-list.html">日记列表页</a>...</p>
    </div>
</body>
</html>
EOF

# 创建 README
echo "📖 创建 README..."
cat > "$BUILD_DIR/README.md" << 'EOF'
# 🦞 光储龙虾 - 开发日记

**参考**: sanwan.ai (3 万点 AI) 设计风格  
**风格**: 极简 · 专业 · 真实

## 📄 页面说明

- **index.html** - 自动跳转到日记列表
- **diary-list.html** - 日记列表页（按月分组）
- **diary-single.html** - 单篇日记页（时间线展示）
- **3wan-style.html** - sanwan.ai 风格版本
- **diary-hub.html** - 日记中心

## 🌐 访问地址

- https://xuegangwu.github.io/guangchu/
- https://xuegangwu.github.io/guangchu/diary-list.html
- https://xuegangwu.github.io/guangchu/diary/YYYY-MM-DD.html

## 📁 目录结构

```
build/
├── index.html
├── diary-list.html
├── diary-single.html
├── 3wan-style.html
├── diary-hub.html
└── diary/
    ├── 2026-03-12.html
    └── ...
```

## 🚀 部署

```bash
# 构建
./build-diary-pages.sh

# 推送到 GitHub Pages
git subtree push --prefix build origin gh-pages
```

---

© 2026 光储龙虾
EOF

echo ""
echo "✅ 构建完成！"
echo ""
echo "📁 构建目录：$BUILD_DIR"
echo ""
echo "📂 文件列表:"
find "$BUILD_DIR" -type f -name "*.html" | sed 's|'"$BUILD_DIR"'|  └── |'
echo ""
echo "🚀 下一步："
echo "   cd $PROJECT_DIR"
echo "   git subtree push --prefix build origin gh-pages"
echo ""
echo "🌐 访问地址:"
echo "   https://xuegangwu.github.io/guangchu/"
echo "   https://xuegangwu.github.io/guangchu/diary-list.html"
echo ""
