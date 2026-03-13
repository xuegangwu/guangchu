# 🦞 光储龙虾 - GitHub Pages 部署指南

**目标**: 将日记页面部署到独立的 GitHub Pages，通过项目详情页的 Link 访问

---

## 🎯 最终效果

### 访问流程

```
项目详情页 (project-intro.html)
         ↓
    [查看开发日记] Link
         ↓
GitHub Pages (独立页面)
         ↓
日记列表页 (diary-list.html)
         ↓
单篇日记 (YYYY-MM-DD.html)
```

### 访问地址

| 页面 | 地址 |
|------|------|
| **项目详情** | http://localhost:3000/project-intro.html |
| **日记首页** | https://xuegangwu.github.io/guangchu/ |
| **日记列表** | https://xuegangwu.github.io/guangchu/diary-list.html |
| **单篇日记** | https://xuegangwu.github.io/guangchu/diary/2026-03-12.html |

---

## 📁 方案说明

### 独立 GitHub Pages

- **不是**放在 README 上
- **不是**放在主分支
- **是**独立的 gh-pages 分支
- **是**可以通过 Link 访问的独立页面

### 文件结构

```
光储龙虾/
├── main 分支 (代码)
│   ├── web/
│   │   ├── diary-list.html
│   │   ├── diary-single.html
│   │   └── ...
│   ├── diary/
│   │   └── YYYY-MM-DD.html
│   └── build/              # 构建目录
│       ├── index.html
│       ├── diary-list.html
│       └── diary/
│
└── gh-pages 分支 (GitHub Pages)
    ├── index.html
    ├── diary-list.html
    └── diary/
```

---

## 🚀 部署步骤

### 步骤 1: 构建页面

```bash
cd /home/admin/openclaw/workspace/projects/光储龙虾

# 运行构建脚本
chmod +x build-diary-pages.sh
./build-diary-pages.sh
```

**输出**:
```
✅ 构建完成！
📁 构建目录：/home/admin/openclaw/workspace/projects/guangchu/build
📂 文件列表:
  └── index.html
  └── diary-list.html
  └── diary-single.html
  └── ...
```

### 步骤 2: 推送到 GitHub

```bash
# 使用 git subtree 推送
git subtree push --prefix build origin gh-pages
```

**或者**使用完整命令：
```bash
git subtree push --prefix build https://github.com/xuegangwu/guangchu.git gh-pages
```

### 步骤 3: 配置 GitHub Pages

1. 访问：https://github.com/xuegangwu/guangchu/settings/pages
2. **Source**: Deploy from a branch
3. **Branch**: gh-pages
4. **Folder**: / (root)
5. 点击 **Save**

### 步骤 4: 等待部署

等待 1-2 分钟，GitHub 会自动部署。

### 步骤 5: 访问页面

打开浏览器访问：
```
https://xuegangwu.github.io/guangchu/
https://xuegangwu.github.io/guangchu/diary-list.html
```

---

## 🔗 项目详情页 Link

### 位置

项目详情页 (`project-intro.html`) 底部，Footer 上方

### 设计

```html
<section class="diary-cta">
    <h2>📔 开发日记</h2>
    <p>参考 sanwan.ai (3 万点 AI) 设计风格</p>
    <p>记录每一天的工作进展，见证项目的成长历程。</p>
    <a href="https://xuegangwu.github.io/guangchu/diary-list.html" 
       target="_blank" 
       class="diary-cta-button">
        查看开发日记 →
    </a>
</section>
```

### 效果

- 蓝色渐变背景卡片
- 白色文字
- 圆角按钮
- 悬停效果
- 新窗口打开 (`target="_blank"`)

---

## 🔄 日常更新

### 自动生成日记

```bash
# 每天 18:00 自动生成
python3 scripts/generate-3wan-diary.py
```

### 重新构建并推送

```bash
# 1. 重新构建
./build-diary-pages.sh

# 2. 推送到 GitHub
git subtree push --prefix build origin gh-pages
```

### 自动化（可选）

配置 crontab：
```bash
crontab -e
```

添加：
```bash
# 每天 18:00 自动构建并推送
0 18 * * * cd /home/admin/openclaw/workspace/projects/光储龙虾 && ./build-diary-pages.sh && git subtree push --prefix build origin gh-pages
```

---

## ⚠️ 常见问题

### Q1: git subtree 命令失败

**错误**: `git: 'subtree' is not a git command`

**解决**:
```bash
# Ubuntu/Debian
sudo apt-get install git-subtree

# macOS (Homebrew)
brew install git
```

### Q2: gh-pages 分支不存在

**解决**:
```bash
# 创建 orphan 分支
git checkout --orphan gh-pages
git reset --hard
git commit --allow-empty -m "Initial commit"
git push origin gh-pages
git checkout main
```

### Q3: 页面显示 404

**原因**: GitHub Pages 还未部署完成

**解决**:
- 等待 1-2 分钟
- 检查 GitHub Pages 设置
- 清除浏览器缓存

### Q4: 推送被拒绝

**解决**:
```bash
# 强制推送
git subtree push --prefix build origin gh-pages --force
```

---

## 📊 完整命令参考

### 首次部署

```bash
cd /home/admin/openclaw/workspace/projects/光储龙虾

# 1. 构建
./build-diary-pages.sh

# 2. 推送
git subtree push --prefix build origin gh-pages

# 3. 配置 GitHub Pages 设置
# 访问：https://github.com/xuegangwu/guangchu/settings/pages
```

### 日常更新

```bash
# 每天自动运行
./build-diary-pages.sh
git subtree push --prefix build origin gh-pages
```

### 检查状态

```bash
# 查看 gh-pages 分支
git branch -a | grep gh-pages

# 查看构建目录
ls -la build/

# 查看日记文件
ls -la build/diary/
```

---

## 🎯 验证清单

部署完成后检查：

- [ ] 访问 https://xuegangwu.github.io/guangchu/ 正常
- [ ] 访问 https://xuegangwu.github.io/guangchu/diary-list.html 正常
- [ ] 项目详情页的 Link 可以点击
- [ ] Link 打开新窗口
- [ ] 日记页面显示正常
- [ ] 移动端适配正常

---

## 📞 快速参考

### 构建命令
```bash
./build-diary-pages.sh
```

### 推送命令
```bash
git subtree push --prefix build origin gh-pages
```

### 访问地址
```
https://xuegangwu.github.io/guangchu/
https://xuegangwu.github.io/guangchu/diary-list.html
```

### 项目详情页 Link
```html
<a href="https://xuegangwu.github.io/guangchu/diary-list.html" target="_blank">
    查看开发日记 →
</a>
```

---

**部署完成后，日记页面就可以通过项目详情页的 Link 访问了！** 🚀✨
