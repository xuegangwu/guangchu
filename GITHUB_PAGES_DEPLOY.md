# 🦞 光储龙虾 - GitHub Pages 部署指南

**目标**: 将日记页面部署到 GitHub Pages，公开访问

---

## 📁 方案选择

### 方案一：使用 gh-pages 分支（推荐）

```
主分支：main (代码)
Pages 分支：gh-pages (静态页面)
```

**优点**:
- 代码和页面分离
- 清晰的文件结构
- 易于管理

**缺点**:
- 需要维护两个分支

### 方案二：使用 docs 文件夹

```
主分支：main
Pages 目录：/docs
```

**优点**:
- 单一分支
- 简单直接

**缺点**:
- 代码和页面混在一起

### 方案三：使用根目录

```
主分支：main
Pages 目录：/ (根目录)
```

**优点**:
- 最简单

**缺点**:
- 整个仓库都暴露

---

## 🚀 推荐方案：gh-pages 分支

### 步骤 1: 准备文件

```bash
cd /home/admin/openclaw/workspace/projects/光储龙虾

# 创建 github-pages 目录
mkdir -p github-pages/diary

# 复制 Web 文件
cp web/diary-list.html github-pages/
cp web/diary-single.html github-pages/
cp web/3wan-style.html github-pages/
cp web/diary-hub.html github-pages/

# 复制日记文件
cp diary/*.html github-pages/diary/
```

### 步骤 2: 创建 index.html

创建 `github-pages/index.html`:

```html
<!DOCTYPE html>
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
```

### 步骤 3: 推送到 gh-pages 分支

```bash
# 方法 1: 使用 git subtree
git subtree push --prefix github-pages origin gh-pages

# 方法 2: 手动切换分支
git checkout --orphan gh-pages
git reset --hard
cp -r github-pages/* .
git add .
git commit -m "Deploy to GitHub Pages"
git push origin gh-pages --force
git checkout main
```

### 步骤 4: 配置 GitHub Pages

1. 访问 GitHub 仓库
2. 进入 **Settings** → **Pages**
3. **Source** 选择：
   - Deploy from a branch
   - Branch: **gh-pages**
   - Folder: **/** (root)
4. 点击 **Save**

### 步骤 5: 访问页面

等待 1-2 分钟部署完成后访问：

```
https://xuegangwu.github.io/guangchu/
https://xuegangwu.github.io/guangchu/diary-list.html
https://xuegangwu.github.io/guangchu/diary/2026-03-12.html
```

---

## 🔄 自动部署脚本

### 创建 deploy.sh

```bash
#!/bin/bash

# 光储龙虾 - GitHub Pages 自动部署脚本

set -e

echo "🦞 开始部署 GitHub Pages..."

# 进入项目目录
cd /home/admin/openclaw/workspace/projects/光储龙虾

# 生成最新日记
echo "📝 生成日记..."
python3 scripts/generate-3wan-diary.py

# 创建/更新 github-pages 目录
echo "📁 准备文件..."
mkdir -p github-pages/diary

# 复制 Web 文件
cp web/diary-list.html github-pages/ 2>/dev/null || true
cp web/diary-single.html github-pages/ 2>/dev/null || true
cp web/3wan-style.html github-pages/ 2>/dev/null || true
cp web/diary-hub.html github-pages/ 2>/dev/null || true

# 复制日记文件
cp diary/*.html github-pages/diary/ 2>/dev/null || true

# 创建 index.html
cat > github-pages/index.html << 'EOF'
<!DOCTYPE html>
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
EOF

# 使用 subtree 推送
echo "🚀 推送到 GitHub..."
git subtree push --prefix github-pages origin gh-pages

echo "✅ 部署完成！"
echo ""
echo "📍 访问地址:"
echo "   https://xuegangwu.github.io/guangchu/"
echo "   https://xuegangwu.github.io/guangchu/diary-list.html"
```

### 添加执行权限

```bash
chmod +x deploy.sh
```

### 手动运行

```bash
./deploy.sh
```

---

## ⏰ 配置定时任务

### 编辑 crontab

```bash
crontab -e
```

### 添加定时任务

```bash
# 每天 18:00 自动生成并部署日记
0 18 * * * cd /home/admin/openclaw/workspace/projects/光储龙虾 && ./deploy.sh >> /tmp/guangchu-deploy.log 2>&1
```

---

## 📊 完整文件结构

```
光储龙虾/
├── main 分支 (代码)
│   ├── web/
│   │   ├── diary-list.html
│   │   ├── diary-single.html
│   │   └── ...
│   ├── diary/
│   │   └── YYYY-MM-DD.html
│   ├── scripts/
│   │   └── generate-3wan-diary.py
│   ├── github-pages/        # 临时目录
│   └── deploy.sh
│
└── gh-pages 分支 (GitHub Pages)
    ├── index.html
    ├── diary-list.html
    ├── diary-single.html
    ├── 3wan-style.html
    ├── diary-hub.html
    └── diary/
        ├── 2026-03-12.html
        └── ...
```

---

## 🎯 快速部署命令

### 首次部署

```bash
cd /home/admin/openclaw/workspace/projects/光储龙虾

# 1. 运行部署脚本
./deploy.sh

# 2. 或使用 Python 脚本
python3 deploy-github-pages.py

# 3. 或手动部署
mkdir -p github-pages/diary
cp web/*.html github-pages/
cp diary/*.html github-pages/diary/
git subtree push --prefix github-pages origin gh-pages
```

### 日常部署

```bash
# 每天自动运行（crontab）
0 18 * * * cd /home/admin/openclaw/workspace/projects/光储龙虾 && ./deploy.sh
```

---

## ⚠️ 注意事项

### 1. GitHub Pages 设置

确保在 GitHub 仓库设置中：
- **Settings** → **Pages**
- **Source**: Deploy from a branch
- **Branch**: gh-pages
- **Folder**: / (root)

### 2. 自定义域名（可选）

如需使用自定义域名：
1. 在 GitHub Pages 设置中添加域名
2. 创建 `github-pages/CNAME` 文件
3. 内容：`your-domain.com`

### 3. 部署失败处理

```bash
# 检查 gh-pages 分支是否存在
git branch -a | grep gh-pages

# 如果不存在，创建它
git checkout --orphan gh-pages
git reset --hard
git commit --allow-empty -m "Initial commit"
git push origin gh-pages
git checkout main

# 重新部署
./deploy.sh
```

### 4. 清除缓存

如果页面没有更新：
```bash
# 强制推送
git subtree push --prefix github-pages origin gh-pages --force
```

---

## 📞 访问地址

### 部署后

| 页面 | 地址 |
|------|------|
| **首页** | https://xuegangwu.github.io/guangchu/ |
| **日记列表** | https://xuegangwu.github.io/guangchu/diary-list.html |
| **单篇日记** | https://xuegangwu.github.io/guangchu/diary/YYYY-MM-DD.html |
| **sanwan.ai 风格** | https://xuegangwu.github.io/guangchu/3wan-style.html |
| **日记中心** | https://xuegangwu.github.io/guangchu/diary-hub.html |

---

## ✅ 部署检查清单

- [ ] 创建 github-pages 目录
- [ ] 复制所有 Web 文件
- [ ] 复制日记文件
- [ ] 创建 index.html
- [ ] 推送到 gh-pages 分支
- [ ] 配置 GitHub Pages 设置
- [ ] 等待部署完成（1-2 分钟）
- [ ] 访问测试
- [ ] 配置定时任务（可选）

---

**部署完成后，日记页面就可以公开访问了！** 🚀✨
