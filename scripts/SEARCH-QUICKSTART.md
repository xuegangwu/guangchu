# 🔍 光储龙虾搜索 - 快速开始

## 1️⃣ 构建索引

```bash
cd /home/admin/openclaw/workspace/projects/光储龙虾
python3 scripts/build-index.py
```

## 2️⃣ 搜索示例

### 关键词搜索
```bash
# 搜索"储能"相关（英文关键词）
python3 scripts/search.py "battery"
python3 scripts/search.py "energy storage"
python3 scripts/search.py "solar"

# 搜索产品发布
python3 scripts/search.py "launches"
```

### 按类型筛选
```bash
# 只看产品
python3 scripts/search.py -t 产品

# 只看政策
python3 scripts/search.py -t 政策

# 只看项目
python3 scripts/search.py -t 项目
```

### 按区域筛选
```bash
# 欧洲新闻
python3 scripts/search.py -r Europe

# 美国新闻
python3 scripts/search.py -r US

# 全球新闻
python3 scripts/search.py -r Global
```

### 组合搜索
```bash
# 欧洲的产品新闻
python3 scripts/search.py -t 产品 -r Europe

# 美国的储能项目
python3 scripts/search.py "battery" -t 项目 -r US

# PV Magazine 的太阳能新闻
python3 scripts/search.py "solar" -s "PV Magazine"
```

### 输出控制
```bash
# 紧凑模式（列表）
python3 scripts/search.py "solar" --compact

# 限制结果数量
python3 scripts/search.py "battery" -l 5

# 导出为 JSON
python3 scripts/search.py "energy storage" --export results.json

# 查看统计
python3 scripts/search.py --stats
```

## 📊 当前索引数据

- **总记录数**: 60 条
- **日期范围**: 2026-03-10 至 2026-03-12
- **来源**: PV Magazine, Energy Storage News
- **语言**: 英文（关键词需用英文）

## 🎯 常用关键词

| 中文 | 英文关键词 |
|------|-----------|
| 储能 | battery, energy storage, BESS |
| 太阳能 | solar, PV, photovoltaic |
| 组件 | module, panel |
| 逆变器 | inverter |
| 项目 | project, installation |
| 政策 | policy, regulation, tariff |
| 价格 | price, cost |
| 发布 | launch, release |

## ⚠️ 注意事项

1. **关键词用英文**：数据源是英文媒体，中文关键词无法匹配
2. **更新索引**：每次抓取新数据后需重新构建索引
3. **FTS5 语法**：支持 `OR`, `AND`, `-` 等高级搜索语法

## 📖 完整文档

查看 `docs/搜索功能使用说明.md` 了解更多高级功能。
