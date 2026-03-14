# Guangchu API 文档

> **版本**: v2.2  
> **更新日期**: 2026-03-14  
> **状态**: 开发中

---

## 📋 目录

- [概述](#概述)
- [认证](#认证)
- [搜索 API](#搜索-api)
- [数据 API](#数据-api)
- [统计 API](#统计-api)
- [错误处理](#错误处理)

---

## 概述

Guangchu API 提供 RESTful 接口，用于访问新闻数据、搜索功能和统计信息。

**基础 URL**: `https://xuegangwu.github.io/guangchu/api`

**响应格式**: JSON

---

## 认证

目前 API 为公开访问，无需认证。

未来版本将支持 API Key 认证。

---

## 搜索 API

### 搜索新闻

**端点**: `GET /api/search`

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| q | string | 是 | 搜索关键词 |
| date_from | string | 否 | 开始日期 (YYYY-MM-DD) |
| date_to | string | 否 | 结束日期 (YYYY-MM-DD) |
| region | string | 否 | 区域 (US/Europe/China/Japan) |
| type | string | 否 | 类型 (policy/product/project/market) |
| sort | string | 否 | 排序 (relevance/date)，默认 relevance |
| limit | integer | 否 | 结果数量，默认 20 |
| highlight | boolean | 否 | 是否高亮，默认 true |

**请求示例**:
```bash
curl "https://xuegangwu.github.io/guangchu/api/search?q=solar&region=US&limit=10"
```

**响应示例**:
```json
{
  "success": true,
  "count": 10,
  "results": [
    {
      "id": 1,
      "title": "Solar energy policy announced",
      "title_highlighted": "<mark>Solar</mark> energy policy...",
      "url": "https://example.com",
      "date": "2026-03-14",
      "region": "US",
      "type": "policy",
      "source": "Test Source",
      "summary": "New solar policy...",
      "summary_highlighted": "New <mark>solar</mark> policy..."
    }
  ],
  "search_time_ms": 45
}
```

---

### 搜索建议

**端点**: `GET /api/search/suggestions`

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| prefix | string | 是 | 搜索前缀 |
| limit | integer | 否 | 建议数量，默认 5 |

**请求示例**:
```bash
curl "https://xuegangwu.github.io/guangchu/api/search/suggestions?prefix=sol"
```

**响应示例**:
```json
{
  "success": true,
  "suggestions": [
    "solar energy",
    "solar panel",
    "solar power"
  ]
}
```

---

### 搜索历史

**端点**: `GET /api/search/history`

**认证**: 需要（未来版本）

**响应示例**:
```json
{
  "success": true,
  "history": [
    {
      "query": "solar energy",
      "filters": {"region": "US"},
      "result_count": 15,
      "timestamp": "2026-03-14T10:30:00"
    }
  ]
}
```

---

## 数据 API

### 获取新闻列表

**端点**: `GET /api/news`

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| date | string | 否 | 指定日期 |
| region | string | 否 | 区域 |
| type | string | 否 | 类型 |
| page | integer | 否 | 页码，默认 1 |
| per_page | integer | 否 | 每页数量，默认 20 |

**请求示例**:
```bash
curl "https://xuegangwu.github.io/guangchu/api/news?date=2026-03-14&region=US"
```

**响应示例**:
```json
{
  "success": true,
  "page": 1,
  "per_page": 20,
  "total": 50,
  "total_pages": 3,
  "news": [
    {
      "id": 1,
      "title": "News title",
      "url": "https://example.com",
      "date": "2026-03-14",
      "region": "US",
      "type": "policy",
      "source": "Source Name"
    }
  ]
}
```

---

### 获取新闻详情

**端点**: `GET /api/news/<id>`

**请求示例**:
```bash
curl "https://xuegangwu.github.io/guangchu/api/news/1"
```

**响应示例**:
```json
{
  "success": true,
  "news": {
    "id": 1,
    "title": "News title",
    "url": "https://example.com",
    "date": "2026-03-14",
    "region": "US",
    "type": "policy",
    "source": "Source Name",
    "summary": "News summary...",
    "content": "Full content..."
  }
}
```

---

## 统计 API

### 获取统计信息

**端点**: `GET /api/stats`

**响应示例**:
```json
{
  "success": true,
  "stats": {
    "total_news": 70,
    "total_regions": 5,
    "total_types": 4,
    "date_range": {
      "from": "2026-03-10",
      "to": "2026-03-14"
    },
    "regions": {
      "US": 37,
      "Europe": 19,
      "China": 10,
      "Japan": 3,
      "Southeast Asia": 1
    },
    "types": {
      "policy": 24,
      "product": 23,
      "project": 15,
      "market": 8
    }
  }
}
```

---

### 获取趋势数据

**端点**: `GET /api/stats/trend`

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| start | string | 否 | 开始日期 |
| end | string | 否 | 结束日期 |
| group_by | string | 否 | 分组 (date/region/type) |

**响应示例**:
```json
{
  "success": true,
  "trend": [
    {"date": "2026-03-10", "count": 15},
    {"date": "2026-03-11", "count": 18},
    {"date": "2026-03-12", "count": 20},
    {"date": "2026-03-13", "count": 17},
    {"date": "2026-03-14", "count": 10}
  ]
}
```

---

## 错误处理

### 错误响应格式

```json
{
  "success": false,
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "Invalid parameter 'date': must be YYYY-MM-DD format",
    "details": {}
  }
}
```

### 错误代码

| 代码 | HTTP 状态码 | 说明 |
|------|-----------|------|
| INVALID_PARAMETER | 400 | 参数无效 |
| NOT_FOUND | 404 | 资源不存在 |
| RATE_LIMITED | 429 | 请求频率超限 |
| INTERNAL_ERROR | 500 | 服务器内部错误 |

---

## 速率限制

### 当前限制

- **未认证**: 100 请求/分钟
- **已认证**: 1000 请求/分钟（未来版本）

### 响应头

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1647244800
```

---

## 代码示例

### Python

```python
import requests

# 搜索新闻
response = requests.get(
    'https://xuegangwu.github.io/guangchu/api/search',
    params={'q': 'solar energy', 'region': 'US'}
)

if response.status_code == 200:
    data = response.json()
    for news in data['results']:
        print(news['title'])
else:
    print(f"Error: {response.status_code}")
```

### JavaScript

```javascript
// 搜索新闻
fetch('https://xuegangwu.github.io/guangchu/api/search?q=solar&region=US')
  .then(response => response.json())
  .then(data => {
    data.results.forEach(news => {
      console.log(news.title);
    });
  })
  .catch(error => console.error('Error:', error));
```

### cURL

```bash
# 搜索
curl "https://xuegangwu.github.io/guangchu/api/search?q=solar&limit=5"

# 获取统计
curl "https://xuegangwu.github.io/guangchu/api/stats"

# 带过滤搜索
curl "https://xuegangwu.github.io/guangchu/api/search?q=energy&date_from=2026-03-01&region=US"
```

---

## 更新日志

### v2.2 (2026-03-14)
- ✨ 新增搜索 API
- ✨ 新增统计 API
- ✨ 新增搜索建议
- ⚡ 性能优化 80%

### v2.1 (2026-03-14)
- 🔧 质量提升
- 📊 测试覆盖 87%
- 📝 文档完善

---

## 支持与反馈

- **GitHub Issues**: https://github.com/xuegangwu/guangchu/issues
- **文档**: https://github.com/xuegangwu/guangchu/blob/main/docs/README.md
- **示例代码**: https://github.com/xuegangwu/guangchu/tree/main/examples

---

**最后更新**: 2026-03-14
