# 🚀 光储龙虾 - 快速启动指南

## 第一次使用

### 1. 安装依赖

```bash
pip3 install flask requests beautifulsoup4
```

### 2. 自动更新数据

```bash
cd /home/admin/openclaw/workspace/projects/光储龙虾
python3 scripts/auto-update.py
```

### 3. 启动 Web 搜索

```bash
python3 scripts/web-search.py
```

访问：http://localhost:5000

---

## 日常使用

### 方式一：自动更新（推荐）

```bash
python3 scripts/auto-update.py
```

自动完成：
- ✅ 抓取英文新闻
- ✅ 抓取中文新闻（可选）
- ✅ 重建搜索索引

### 方式二：手动分步

```bash
# 1. 抓取新闻
python3 scripts/fetch-news.py
python3 scripts/fetch-chinese-news.py

# 2. 构建索引
python3 scripts/build-index.py

# 3. 生成报告
python3 scripts/generate-daily.py
```

---

## 搜索功能

### Web 搜索（可视化）

```bash
python3 scripts/web-search.py
# 访问 http://localhost:5000
```

### 命令行搜索

```bash
# 关键词搜索
python3 scripts/search.py "battery"

# 按类型筛选
python3 scripts/search.py -t 产品

# 按区域筛选
python3 scripts/search.py -r Europe

# 组合搜索
python3 scripts/search.py "solar" -t 产品 -r Global

# 查看统计
python3 scripts/search.py --stats
```

---

## 定时任务

### 配置定时任务

```bash
crontab -e
```

粘贴以下内容（每天 8:00 自动更新）：

```bash
0 8 * * * cd /home/admin/openclaw/workspace/projects/光储龙虾 && python3 scripts/auto-update.py
```

### 查看日志

```bash
tail -f /tmp/guangchu-update.log
```

---

## 查看报告

### 日报

```bash
cat reports/daily/2026-03-12.md
```

### 头条号版本

```bash
cat reports/toutiao/2026-03-12_头条.md
```

---

## 常用命令速查

| 功能 | 命令 |
|------|------|
| 自动更新 | `python3 scripts/auto-update.py` |
| Web 搜索 | `python3 scripts/web-search.py` |
| 命令行搜索 | `python3 scripts/search.py "关键词"` |
| 查看统计 | `python3 scripts/search.py --stats` |
| 抓取英文 | `python3 scripts/fetch-news.py` |
| 抓取中文 | `python3 scripts/fetch-chinese-news.py` |
| 构建索引 | `python3 scripts/build-index.py` |
| 生成日报 | `python3 scripts/generate-daily.py` |

---

## 文件位置

```
光储龙虾/
├── scripts/              # 脚本目录
│   ├── auto-update.py    # 自动更新
│   ├── web-search.py     # Web 搜索
│   ├── search.py         # 命令行搜索
│   ├── build-index.py    # 构建索引
│   ├── fetch-news.py     # 抓取英文
│   ├── fetch-chinese-news.py  # 抓取中文
│   └── ...
├── reports/              # 报告目录
│   ├── daily/           # 日报
│   ├── weekly/          # 周报
│   ├── monthly/         # 月报
│   └── toutiao/         # 头条号
├── raw/                 # 原始数据
├── search.db            # 搜索数据库
└── START.md             # 本文件
```

---

## 遇到问题？

### 1. 依赖缺失

```bash
pip3 install flask requests beautifulsoup4
```

### 2. 端口被占用

修改 Web 服务端口：
```python
# scripts/web-search.py 最后一行
app.run(host='0.0.0.0', port=8080, debug=False)
```

### 3. 中文抓取失败

检查网络连接，或暂时只用英文源：
```bash
python3 scripts/fetch-news.py
python3 scripts/build-index.py
```

### 4. 搜索无结果

重新构建索引：
```bash
python3 scripts/build-index.py
```

---

## 更多文档

- **搜索功能**: `docs/搜索功能使用说明.md`
- **新功能介绍**: `三大新功能开发完成.md`
- **任务状态**: `任务状态.md`

---

**开始使用**：
```bash
cd /home/admin/openclaw/workspace/projects/光储龙虾
python3 scripts/auto-update.py
python3 scripts/web-search.py
```
