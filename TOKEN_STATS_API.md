# 📊 Token 统计 API 使用说明

## 🚀 API 端点

### 1. 获取月度 Token 统计

```
GET /api/token-stats?month=2026-03
```

**参数**:
- `month` (可选): 月份，格式 YYYY-MM，默认为当前月份

**响应示例**:
```json
{
    "success": true,
    "month": "2026-03",
    "data": [
        {
            "date": "2026-03-10",
            "news_count": 20,
            "news_tokens": 1026,
            "daily_report_tokens": 1579,
            "total_tokens": 2605
        },
        {
            "date": "2026-03-11",
            "news_count": 20,
            "news_tokens": 1004,
            "daily_report_tokens": 1677,
            "total_tokens": 2681
        }
    ],
    "summary": {
        "total_days": 4,
        "total_tokens": 10064,
        "total_news": 80,
        "avg_tokens_per_day": 2516,
        "avg_news_per_day": 20,
        "estimated_cost_usd": 0.0201
    }
}
```

### 2. 获取单日 Token 统计

```
GET /api/token-stats/daily?date=2026-03-11
```

**参数**:
- `date` (可选): 日期，格式 YYYY-MM-DD，默认为今天

**响应示例**:
```json
{
    "success": true,
    "date": "2026-03-11",
    "data": {
        "date": "2026-03-11",
        "news_count": 20,
        "news_tokens": 1004,
        "daily_report_tokens": 1677,
        "total_tokens": 2681,
        "estimated_cost_usd": 0.0054
    }
}
```

---

## 🔧 本地数据文件

对于 GitHub Pages 版本（无法访问后端 API），系统会自动从本地 JSON 文件加载数据：

**文件位置**: `web/token-stats.json`

**更新本地数据**:
```bash
# 运行脚本生成数据文件
cd /home/admin/.copaw/guangchu
cat stats/2026-03.jsonl | python3 -c "
import json, sys
data = [json.loads(l) for l in sys.stdin if l.strip()]
result = {
    'month': '2026-03',
    'data': [{**d, 'cost': round(d['total_tokens']*0.000002, 4)} for d in data],
    'summary': {
        'total_days': len(data),
        'total_tokens': sum(d['total_tokens'] for d in data),
        'total_news': sum(d['news_count'] for d in data),
        'avg_tokens_per_day': sum(d['total_tokens'] for d in data) // len(data) if data else 0,
        'estimated_cost_usd': round(sum(d['total_tokens'] for d in data) * 0.000002, 4)
    }
}
print(json.dumps(result, ensure_ascii=False))
" > web/token-stats.json
```

---

## 📦 前端集成

### 自动加载（推荐）

页面加载时自动尝试加载数据：

1. 首先尝试从 API 加载（适用于本地开发/有后端的情况）
2. 如果 API 不可用，则从本地 JSON 文件加载（适用于 GitHub Pages）
3. 如果都不可用，则使用示例数据

```javascript
// 页面加载时自动调用
window.addEventListener('load', function() {
    loadTokenData();  // 自动加载真实数据
});
```

### 手动加载

```javascript
// 手动触发数据加载
await loadTokenData();

// 获取当前数据
console.log(tokenData.stats);
```

---

## ⏰ 自动更新

页面会自动每 30 秒刷新一次数据：

```javascript
setInterval(() => {
    loadTokenData();
    updateStats();
}, 30000);
```

---

## 📊 数据来源

数据由 `scripts/count-tokens.py` 脚本生成：

1. 抓取新闻统计 (`raw/YYYY-MM-DD.json`)
2. 日报生成统计 (`reports/daily/YYYY-MM-DD.md`)
3. 头条格式统计 (`reports/toutiao/YYYY-MM-DD_头条.md`)

**成本估算**: $0.002 / 1K tokens

---

## 🧪 测试

### 本地测试

```bash
# 启动 API 服务器
cd /home/admin/.copaw/guangchu
python3 -m scripts.api_server

# 测试月度统计
curl "http://localhost:5000/api/token-stats?month=2026-03"

# 测试单日统计
curl "http://localhost:5000/api/token-stats/daily?date=2026-03-11"
```

### GitHub Pages 测试

访问: https://xuegangwu.github.io/guangchu/web/token-report.html

---

## 📝 数据格式说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `date` | string | 日期 (YYYY-MM-DD) |
| `news_count` | int | 抓取新闻数量 |
| `news_tokens` | int | 新闻处理消耗 Token |
| `daily_report_tokens` | int | 日报生成消耗 Token |
| `total_tokens` | int | 总 Token 消耗 |
| `estimated_cost_usd` | float | 估算成本 (USD) |

---

## 🔒 速率限制

- 每分钟 100 次请求
- 使用 `@rate_limit` 装饰器
- 返回 429 状态码表示超限

---

## 📅 每日自动更新

配置 cron 任务自动生成每日统计：

```bash
crontab -e

# 每天 23:00 运行
0 23 * * * cd /home/admin/.copaw/guangchu && python3 scripts/count-tokens.py >> logs/count-tokens.log 2>&1
```

---

*更新时间：2026-03-16*