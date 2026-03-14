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
