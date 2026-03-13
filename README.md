# 🦞 光储龙虾

> Solar-Storage News Collection & Analysis System  
> 全球光伏 + 储能行业信息收集与分析系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Info Sources](https://img.shields.io/badge/sources-22-green.svg)](https://github.com/xuegangwu/guangchu)

---

## 📔 开发日记（今日更新）

> **📅 2026 年 03 月 12 日** | **第 1 期** | **✨ 10 条工作记录** | **💪 工作 9 小时**

### 🎯 今日亮点

1. **✨ 可视化日记系统上线** - 参考福盛养龙虾风格，图文并茂记录每天工作
2. **🚀 多平台导出工具** - 支持公众号/Cloud Hub/GitHub 多格式导出
3. **📱 日记中心页面发布** - 统一的日记入口和展示平台

**[📖 查看今日详细日记 →](http://localhost:5000/diary/)** | **[📚 日记索引 →](http://localhost:5000/diary/index.html)** | **[🎯 日记中心 →](http://localhost:5000/diary-hub.html)**

---

## 📰 最新动态

---

## 🚀 快速开始

### 安装依赖

```bash
pip3 install flask requests beautifulsoup4 googletrans==4.0.0-rc1
```

### 启动 Web 搜索

```bash
cd scripts
python3 web-search.py
```

访问：http://localhost:5000

### 自动更新

```bash
python3 auto-update.py
```

---

## 📊 项目统计

| 指标 | 数值 | 说明 |
|------|------|------|
| **信息源** | 22 个 | 政府/媒体/制造商 |
| **支持语言** | 3 种 | 英文/中文/日文 |
| **日均新闻** | 60+ 条 | 自动抓取处理 |
| **覆盖区域** | 全球 | 中/美/欧/日/越 |

---

## 🌐 核心功能

### 1. 多语言新闻抓取 📰
- 支持 22 个官方信息源
- 自动抓取 PV Magazine、Energy Storage News 等
- 支持政府/能源局/制造商网站

### 2. 智能数据处理 ⚙️
- 7 步自动化处理流程
- 多语言自动翻译（英/中/日）
- 关键信息提取
- 智能摘要生成
- 情感分析
- 主题分类

### 3. 全文搜索引擎 🔍
- SQLite FTS5 引擎
- 支持布尔搜索、短语搜索
- 搜索响应 < 50ms

### 4. 社交媒体集成 📱
- LinkedIn 公司动态
- Facebook 页面帖子
- Twitter 实时推文

### 5. 研发日记系统 📔
- 每天 5 条精彩更新
- 图文并茂展示
- 永久历史档案

---

## 🗺️ 投资地图系统

访问：http://localhost:3000

- **中国地图**: 30 省份投资评估
- **越南地图**: 15 省份投资评估
- **日本地图**: 47 都道府县评估
- **参数配置**: 自定义权重

---

## 📔 研发日记

### 今日更新

**[查看今日日记 →](http://localhost:5000/diary/)**

### 日记特点

- ✨ **每天 5 条** - 只记录最精彩的更新
- 🎨 **图文并茂** - 表情符号 + 简洁文字
- 🌐 **多平台同步** - GitHub/公众号/Cloud Hub
- 📊 **永久保存** - 项目历史档案

### 发布平台

- **GitHub**: [项目日记索引](http://localhost:5000/diary/)
- **公众号**: 光储龙虾研发日记
- **Cloud Hub**: [Cloud Hub 主页](http://localhost:5000/diary/cloudhub.html)

---

## 🛠️ 技术栈

### 后端
- **Python 3.10+** - 主要开发语言
- **Flask** - Web 框架
- **SQLite FTS5** - 全文搜索引擎

### 前端
- **HTML5/CSS3** - 页面结构
- **JavaScript** - 交互逻辑
- **响应式设计** - 多端适配

### 数据处理
- **BeautifulSoup** - HTML 解析
- **Requests** - HTTP 请求
- **Google Translate** - 多语言翻译

### 部署
- **GitHub Pages** - 静态页面托管
- **Cron** - 定时任务
- **Git** - 版本控制

---

## 📁 项目结构

```
光储龙虾/
├── scripts/                    # Python 脚本
│   ├── fetch-news.py          # 新闻抓取
│   ├── fetch-chinese-news.py  # 中文新闻抓取
│   ├── fetch-social-media.py  # 社交媒体抓取
│   ├── search.py              # 搜索工具
│   ├── web-search.py          # Web 搜索
│   ├── auto-update.py         # 自动更新
│   ├── generate-daily-report.py    # 工作日报
│   └── generate-project-diary.py   # 项目日记
├── web/                       # Web 页面
│   ├── index.html            # 搜索首页
│   └── project-intro.html    # 项目详情
├── diary/                     # 研发日记
│   ├── YYYY-MM-DD.html       # 每日日记
│   └── index.html            # 日记索引
├── reports/                   # 报告输出
│   ├── daily/               # 日报
│   ├── weekly/              # 周报
│   └── monthly/             # 月报
├── raw/                       # 原始数据
├── processed/                 # 处理后数据
├── config/                    # 配置文件
└── README.md                  # 项目说明
```

---

## 📊 数据源

### 新闻媒体 (4 个)
- PV Magazine
- Energy Storage News
- 北极星储能网
- 索比光伏网

### 政府/能源局 (7 个)
- 中国国家能源局
- 美国能源部
- 欧盟能源委员会
- 日本经济产业省
- 越南工贸部
- IEA
- IRENA

### 社交媒体 (3 个)
- LinkedIn
- Facebook
- Twitter/X

### 其他 (8 个)
- 电力相关 (3 个)
- 制造商 (5 个)
- 政策机构 (3 个)

---

## 🎯 使用场景

### 行业研究员
- 快速了解行业动态
- 追踪政策变化
- 分析市场趋势

### 投资者
- 识别投资机会
- 监控竞争对手
- 评估市场风险

### 企业决策者
- 制定战略规划
- 了解技术趋势
- 把握政策方向

---

## 📞 快速链接

| 功能 | 地址 |
|------|------|
| **Web 搜索** | http://localhost:5000 |
| **项目详情** | http://localhost:5000/project-intro.html |
| **研发日记** | http://localhost:5000/diary/ |
| **投资地图** | http://localhost:3000 |
| **GitHub** | https://github.com/xuegangwu/guangchu |

---

## 📝 开发日志

查看最新的研发日记：[项目日记](http://localhost:5000/diary/)

---

## 📄 许可证

MIT License © 2026 Terry Wu

---

*🦞 光储龙虾 - 让数据驱动光储投资决策*
