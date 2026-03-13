# 🦞 光储龙虾 GitHub Pages 结构设计

**参考**: sanwan.ai (3 万点 AI)  
**风格**: 极简 · 专业 · 真实

---

## 📁 文件结构

```
光储龙虾/
├── web/                          # GitHub Pages 源文件
│   ├── index.html               # 主页（项目介绍 + 日记入口）
│   ├── 3wan-style.html          # sanwan.ai 风格日记模板
│   ├── diary-hub.html           # 日记中心（所有入口）
│   └── project-intro.html       # 项目详情
│
├── diary/                        # 日记输出目录
│   ├── index.html               # 日记列表页
│   ├── YYYY-MM-DD.html          # 每日日记（自动生成）
│   └── ...
│
├── scripts/
│   ├── generate-3wan-diary.py   # sanwan.ai 风格日记生成
│   └── ...
│
└── README.md                     # GitHub 仓库说明
```

---

## 🌐 页面结构

### 1. 主页 (index.html)

```
┌─────────────────────────────────┐
│ 🦞 光储龙虾                     │
│ Solar-Storage News System       │
├─────────────────────────────────┤
│ 项目介绍                        │
│ - 信息源：22 个                 │
│ - 语言：3 种                    │
│ - 省份：92 个                   │
├─────────────────────────────────┤
│ 📔 开发日记 (sanwan.ai 风格)     │
│ [查看今日日记 →]                │
│ [日记列表 →]                    │
│ [日记中心 →]                    │
├─────────────────────────────────┤
│ 🗺️ 投资地图                     │
│ [中国地图] [越南地图] [日本地图] │
├─────────────────────────────────┤
│ 📄 项目详情                     │
│ [了解更多 →]                    │
├─────────────────────────────────┤
│ Footer                          │
│ GitHub | 返回首页               │
└─────────────────────────────────┘
```

### 2. 日记中心 (diary-hub.html)

```
┌─────────────────────────────────┐
│ 📔 日记中心                     │
│ 记录每一天的成长                │
├─────────────────────────────────┤
│ 快速入口                        │
│ ┌──────┐ ┌──────┐ ┌──────┐    │
│ │今日  │ │列表  │ │统计  │    │
│ │日记  │ │索引  │ │数据  │    │
│ └──────┘ └──────┘ └──────┘    │
├─────────────────────────────────┤
│ 日记风格                        │
│ ┌────────────────────┐         │
│ │ sanwan.ai 风格      │         │
│ │ 极简 · 专业 · 真实  │         │
│ │ [立即查看 →]       │         │
│ └────────────────────┘         │
├─────────────────────────────────┤
│ 项目链接                        │
│ 主页 | 投资地图 | 项目详情      │
└─────────────────────────────────┘
```

### 3. 日记列表 (diary/index.html)

```
┌─────────────────────────────────┐
│ 📔 开发日记                     │
│ 所有历史日记                    │
├─────────────────────────────────┤
│ 2026 年 03 月                    │
│ ┌────────────────────────────┐ │
│ │ 12 日 | 第 1 天 | 查看 →    │ │
│ │ 11 日 | 第 0 天 | 查看 →    │ │
│ │ 10 日 | 第 0 天 | 查看 →    │ │
│ └────────────────────────────┘ │
├─────────────────────────────────┤
│ 2026 年 02 月                    │
│ ┌────────────────────────────┐ │
│ │ ...                        │ │
│ └────────────────────────────┘ │
├─────────────────────────────────┤
│ 返回首页 | 日记中心             │
└─────────────────────────────────┘
```

### 4. 单篇日记 (diary/YYYY-MM-DD.html)

```
┌─────────────────────────────────┐
│ 🦞 光储龙虾 (Logo)              │
├─────────────────────────────────┤
│ 开发日记                        │
│ 2026 年 03 月 12 日 | 第 1 天      │
├─────────────────────────────────┤
│ 统计卡片 (4 列)                  │
│ 8 | 15 | +520 | -120           │
├─────────────────────────────────┤
│ 工作日志 (时间线)                │
│ 09 ● 开始一天的工作             │
│    [卡片内容]                   │
│ 10 ● 开发日记生成器             │
│    [卡片内容]                   │
│ ...                             │
├─────────────────────────────────┤
│ 项目统计 (2 列卡片)              │
│ 光储龙虾 | 投资地图             │
├─────────────────────────────────┤
│ Footer                          │
│ 首页 | 日记 | GitHub            │
└─────────────────────────────────┘
```

---

## 🔗 导航设计

### 顶部导航（每个页面）

```
🦞 光储龙虾
首页 | 日记 | 投资地图 | 项目详情 | GitHub
```

### 日记入口（多处）

1. **主页** - 显著位置，sanwan.ai 风格卡片
2. **日记中心** - 统一入口，所有日记相关
3. **GitHub README** - 顶部显眼位置

---

## 🎨 设计风格

### sanwan.ai 风格核心

```
配色:
- 背景：#ffffff (纯白)
- 文字：#1a1a1a (深灰)
- 强调：#0071e3 (苹果蓝)
- 背景块：#f8f8f8 (浅灰)
- 分割线：#eaeaea (淡灰)

字体:
- 标题：32px, 700 字重
- 正文：14px / 16px
- 统计：36px, 700 字重，蓝色

间距:
- 容器：max-width 720px
- 内边距：60px 20px
- 板块间距：60px
```

---

## 🚀 部署流程

### 1. 本地生成

```bash
cd /home/admin/openclaw/workspace/projects/光储龙虾
python3 scripts/generate-3wan-diary.py
```

### 2. 自动部署到 GitHub Pages

```bash
# 推送到 gh-pages 分支
git add diary/
git commit -m "chore: 生成今日日记"
git push origin gh-pages
```

### 3. 配置 GitHub Pages

```
Settings → Pages
Source: gh-pages branch
Branch: main
Folder: / (root)
```

### 4. 访问地址

```
https://xuegangwu.github.io/guangchu/
https://xuegangwu.github.io/guangchu/diary/
https://xuegangwu.github.io/guangchu/diary/2026-03-12.html
```

---

## 📊 日记生成自动化

### 定时任务

```bash
# 每天 18:00 自动生成
0 18 * * * cd /home/admin/openclaw/workspace/projects/光储龙虾 && \
python3 scripts/generate-3wan-diary.py && \
git add diary/ && \
git commit -m "chore: 自动生成日记 $(date +\%Y-\%m-\%d)" && \
git push origin gh-pages
```

### 生成流程

```
18:00 → 触发脚本
    ↓
收集 Git 提交
    ↓
生成统计信息
    ↓
创建工作日志
    ↓
生成 HTML 页面
    ↓
保存到 diary/
    ↓
自动推送到 GitHub
    ↓
GitHub Pages 自动部署
    ↓
完成！
```

---

## 🎯 关键页面代码

### 主页日记入口

```html
<section class="diary-section">
    <h2>📔 开发日记</h2>
    <p class="subtitle">参考 sanwan.ai (3 万点 AI) 设计风格</p>
    
    <div class="diary-cards">
        <a href="/diary/" class="diary-card">
            <span class="card-icon">📖</span>
            <h3>今日日记</h3>
            <p>查看今天的开发记录</p>
        </a>
        
        <a href="/diary/index.html" class="diary-card">
            <span class="card-icon">📚</span>
            <h3>日记列表</h3>
            <p>浏览所有历史日记</p>
        </a>
        
        <a href="/diary-hub.html" class="diary-card">
            <span class="card-icon">🎯</span>
            <h3>日记中心</h3>
            <p>统一的日记入口</p>
        </a>
    </div>
</section>
```

### 日记列表项

```html
<div class="diary-item">
    <div class="diary-date">
        <span class="date-day">12</span>
        <span class="date-month">03 月</span>
    </div>
    <div class="diary-info">
        <h3>第 1 天</h3>
        <p>2026 年 03 月 12 日 · 星期四</p>
        <div class="diary-stats">
            <span>8 次提交</span>
            <span>15 个文件</span>
        </div>
    </div>
    <a href="/diary/2026-03-12.html" class="diary-link">查看 →</a>
</div>
```

---

## 📱 响应式设计

### 桌面端 (>768px)

- 4 列统计网格
- 2 列项目卡片
- 完整时间线
- 大间距留白

### 移动端 (≤768px)

- 2 列统计网格
- 1 列项目卡片
- 简化时间线
- 紧凑间距

---

## ✅ 实施清单

- [ ] 创建主页 (index.html)
- [ ] 创建日记中心 (diary-hub.html)
- [ ] 创建日记列表 (diary/index.html)
- [ ] 创建日记模板 (3wan-style.html)
- [ ] 配置自动生成脚本
- [ ] 配置定时任务
- [ ] 配置 GitHub Pages
- [ ] 测试所有链接
- [ ] 更新 README
- [ ] 部署上线

---

**GitHub Pages 结构设计完成！完全参考 sanwan.ai 风格！** 📔✨
