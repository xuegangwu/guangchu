# 🦞 光储龙虾

Solar-Storage News Collection and Analysis System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📖 项目简介

光储龙虾是一个自动化的光伏 + 储能行业信息收集与分析系统，支持多语言新闻抓取、全文搜索、报告生成等功能。

---

## ✨ 核心功能

- 📰 **自动抓取**: 从多个信息源自动抓取行业新闻
- 🔍 **全文搜索**: 基于 SQLite FTS5 的强大的搜索引擎
- 📊 **报告生成**: 自动生成日报/周报/月报
- 🌏 **多语言支持**: 支持英文和中文信息源
- ⏰ **定时任务**: 支持自动化定时更新

---

## 🌐 信息源

### 英文源
- PV Magazine
- Energy Storage News
- IEA (International Energy Agency)
- IRENA (International Renewable Energy Agency)

### 中文源
- 北极星储能网
- 索比光伏网

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip3 install flask requests beautifulsoup4
```

### 2. 启动 Web 搜索服务

```bash
python3 scripts/web-search.py
```

访问：http://localhost:5000

### 3. 抓取新闻

```bash
python3 scripts/fetch-news.py
python3 scripts/fetch-chinese-news.py
```

### 4. 构建搜索索引

```bash
python3 scripts/build-index.py
```

---

## 📁 项目结构

```
光储龙虾/
├── scripts/                # Python 脚本
│   ├── fetch-news.py       # 英文新闻抓取
│   ├── fetch-chinese-news.py # 中文新闻抓取
│   ├── build-index.py      # 构建搜索索引
│   ├── search.py           # 命令行搜索工具
│   ├── web-search.py       # Web 搜索界面
│   └── auto-update.py      # 自动更新脚本
├── web/                    # Web 界面
│   └── search.html        # 搜索页面
├── raw/                    # 原始数据
├── reports/                # 报告输出
│   ├── daily/             # 日报
│   ├── weekly/            # 周报
│   └── monthly/           # 月报
└── search.db              # 搜索数据库
```

---

## 🔧 使用说明

### 命令行搜索

```bash
# 关键词搜索
python3 scripts/search.py "battery"

# 按类型筛选
python3 scripts/search.py -t 产品

# 按区域筛选
python3 scripts/search.py -r Europe

# 查看统计
python3 scripts/search.py --stats
```

### Web 搜索

启动服务后访问：http://localhost:5000

支持：
- 🔍 关键词搜索
- 📊 类型/区域/来源筛选
- 📈 统计面板
- 📱 响应式设计

---

## ⏰ 定时任务

### 配置 crontab

```bash
crontab -e
```

添加以下内容（每天 8:00 自动更新）：

```bash
0 8 * * * cd /path/to/光储龙虾 && python3 scripts/auto-update.py
```

---

## 📊 数据格式

### 新闻数据结构

```json
{
  "title": "Aiko launches 545 W back-contact solar module",
  "link": "https://www.pv-magazine.com/...",
  "published": "2026-03-12T10:00:00",
  "summary": "The Chinese manufacturer said...",
  "source": "PV Magazine",
  "region": "Global",
  "type": "产品",
  "collected_at": "2026-03-12"
}
```

### 搜索索引

使用 SQLite FTS5 全文搜索引擎：
- 支持布尔搜索（AND, OR, NOT）
- 支持短语搜索
- 支持通配符
- 支持邻近搜索

---

## 📈 报告生成

### 日报 (daily)
- 当日新闻汇总
- 按区域分类
- 精选要点

### 周报 (weekly)
- 周度趋势分析
- 热点汇总
- 政策解读

### 月报 (monthly)
- 月度统计分析
- 市场趋势
- 投资建议

---

## 🛠️ 技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| **爬虫** | Python, Requests | HTTP 请求 |
| **解析** | BeautifulSoup | HTML 解析 |
| **搜索** | SQLite FTS5 | 全文搜索 |
| **Web** | Flask | Web 框架 |
| **定时** | Cron | 定时任务 |

---

## 📊 性能指标

| 指标 | 数值 |
|------|------|
| 抓取速度 | ~100 条/分钟 |
| 搜索响应 | < 50ms |
| 索引构建 | < 5s (1000 条) |
| 内存占用 | ~50MB |

---

## 🎯 使用场景

### 1. 行业研究员
- 快速了解行业动态
- 追踪政策变化
- 分析市场趋势

### 2. 投资者
- 识别投资机会
- 监控竞争对手
- 评估市场风险

### 3. 企业决策者
- 制定战略规划
- 了解技术趋势
- 把握政策方向

---

## 📝 更新日志

### v1.0.0 (2026-03-12)
- ✅ 英文新闻抓取（4 个信息源）
- ✅ 中文新闻抓取（2 个信息源）
- ✅ FTS5 全文搜索引擎
- ✅ Web 搜索界面
- ✅ 命令行搜索工具
- ✅ 日报/周报/月报生成
- ✅ 定时任务支持

---

## 📞 联系信息

- **GitHub**: https://github.com/xuegangwu/guangchu
- **作者**: Terry Wu
- **时间**: 2026-03-12

---

## 📄 许可证

MIT License

---

**光储龙虾 - 您的光储行业信息助手！** 🦞📰
