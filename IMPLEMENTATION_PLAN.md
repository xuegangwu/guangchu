# 🚀 光储龙虾项目 - 待完善功能实施计划

**制定时间**: 2026-03-15  
**目标**: 完成剩余 40% 功能，实现 100% 完整度

---

## 📊 现状分析

### ✅ 已有基础（非常完善！）

#### 1. **后端代码** - 90% 完成
- ✅ `api_server.py` - Flask API 服务器（12KB）
- ✅ `web-search.py` - Web 搜索界面（15KB）
- ✅ `count-tokens.py` - Token 统计脚本（3KB）
- ✅ `fetch-news.py` - 新闻抓取（5KB）
- ✅ `fetch-chinese-news.py` - 中文新闻抓取（9KB）
- ✅ `fetch-government-sources.py` - 政府源抓取（11KB）
- ✅ `advanced_search.py` - 高级搜索（11KB）
- ✅ `cache.py` - 缓存系统（10KB）
- ✅ `translation_service.py` - 翻译服务（15KB）
- ✅ `config.py` - 配置管理（3KB）

#### 2. **数据基础** - 80% 完成
- ✅ `search.db` - SQLite 数据库已存在
- ✅ `raw/` - 原始新闻数据（4 天数据）
- ✅ `stats/2026-03.jsonl` - Token 统计数据
- ✅ `processed/` - 处理后数据目录

#### 3. **前端页面** - 100% 完成
- ✅ `project-intro.html` - 项目介绍
- ✅ `architecture.html` - 系统架构
- ✅ `token-report.html` - Token 报告（等待真实数据）
- ✅ `search.html` - 搜索界面（等待后端）
- ✅ `analytics.html` - 数据分析

---

## 🎯 实施计划（按优先级）

### 🔴 第一阶段：核心功能完善（3-5 天）

#### Task 1: 部署 Flask 后端到阿里云（1-2 天）

**现状**: 
- 代码已完成 (`api_server.py`, `web-search.py`)
- 本地可运行
- 需要部署到阿里云服务器

**步骤**:
1. **准备阿里云服务器**
   ```bash
   # 检查服务器环境
   python3 --version
   pip3 --version
   
   # 安装依赖
   pip3 install flask requests beautifulsoup4
   ```

2. **上传代码到阿里云**
   ```bash
   # 使用 scp 或 git clone
   scp -r scripts/ admin@your-server:/path/to/guangchu/
   scp search.db admin@your-server:/path/to/guangchu/
   ```

3. **配置 Gunicorn/Nginx**
   ```bash
   # 安装 Gunicorn
   pip3 install gunicorn
   
   # 启动服务
   gunicorn -w 4 -b 0.0.0.0:8000 scripts.api_server:app
   ```

4. **配置域名和 HTTPS**
   - 域名解析到阿里云 IP
   - 申请 Let's Encrypt 证书
   - Nginx 反向代理

5. **更新前端链接**
   - 将 `localhost:5000` 改为正式域名
   - 启用"立即体验"按钮

**交付物**:
- ✅ 后端服务运行在阿里云
- ✅ 域名可访问
- ✅ HTTPS 配置完成
- ✅ "立即体验"按钮启用

---

#### Task 2: 实现 Token 统计 API（1 天）

**现状**:
- `count-tokens.py` 脚本已完成
- `stats/2026-03.jsonl` 有真实数据
- `token-report.html` 使用示例数据

**步骤**:
1. **创建 Token API 端点**
   ```python
   # 在 api_server.py 中添加
   @app.route('/api/token-stats', methods=['GET'])
   def get_token_stats():
       month = request.args.get('month', datetime.now().strftime('%Y-%m'))
       stats_file = Path(config.STATS_DIR) / f"{month}.jsonl"
       
       if not stats_file.exists():
           return jsonify({"error": "No data"}), 404
       
       stats = []
       with open(stats_file, 'r', encoding='utf-8') as f:
           for line in f:
               stats.append(json.loads(line))
       
       return jsonify({
           "month": month,
           "data": stats,
           "total_days": len(stats),
           "total_tokens": sum(s['total_tokens'] for s in stats)
       })
   ```

2. **更新前端 Token 报告页面**
   ```javascript
   // 在 token-report.html 中添加
   async function loadTokenData() {
       const response = await fetch('/api/token-stats?month=2026-03');
       const data = await response.json();
       
       // 更新页面数据
       updateCharts(data);
       updateStats(data);
   }
   ```

3. **添加每日自动更新**
   ```bash
   # 配置 cron 任务
   0 23 * * * cd /path/to/guangchu && python3 scripts/count-tokens.py
   ```

**交付物**:
- ✅ Token API 端点
- ✅ 前端连接真实数据
- ✅ 每日自动更新机制
- ✅ 图表实时更新

---

#### Task 3: 完善新闻抓取系统（1-2 天）

**现状**:
- 抓取脚本已完成
- 已有 4 天数据
- 需要完善 22 个信息源

**步骤**:
1. **检查信息源配置**
   ```python
   # 在 config.py 中完善
   SOURCES = {
       'pv_magazine': {
           'url': 'https://www.pv-magazine.com/',
           'region': 'global',
           'language': 'en'
       },
       'energy_storage_news': {
           'url': 'https://energy-storage.news/',
           'region': 'global',
           'language': 'en'
       },
       # ... 其他 20 个信息源
   }
   ```

2. **优化抓取脚本**
   - 添加错误处理
   - 添加重试机制
   - 添加反爬应对

3. **配置定时任务**
   ```bash
   # 每天上午 8 点抓取
   0 8 * * * cd /path/to/guangchu && python3 scripts/fetch-news.py
   0 9 * * * cd /path/to/guangchu && python3 scripts/fetch-chinese-news.py
   ```

4. **数据管道自动化**
   ```bash
   # 抓取 → 处理 → 存储 → 索引
   0 10 * * * cd /path/to/guangchu && python3 scripts/data-processing-pipeline.py
   ```

**交付物**:
- ✅ 22 个信息源完整配置
- ✅ 定时抓取任务
- ✅ 自动化数据处理
- ✅ 数据质量监控

---

### 🟡 第二阶段：功能增强（3-5 天）

#### Task 4: 增强日记系统（2 天）

**现状**:
- 8 篇日记已完成
- 3 种模板风格
- 手动创建

**功能增强**:
1. **每日自动创建日记**
   ```python
   # generate-project-diary.py 自动化
   def auto_generate_diary():
       date = datetime.now().strftime('%Y-%m-%d')
       # 从 Git 提交记录生成
       commits = get_daily_commits(date)
       # 从工作日志生成
       logs = get_work_logs(date)
       # 生成日记
       generate_diary(date, commits, logs)
   ```

2. **日记搜索功能**
   ```python
   @app.route('/api/diary/search', methods=['GET'])
   def search_diary():
       query = request.args.get('q')
       results = search_in_diaries(query)
       return jsonify(results)
   ```

3. **日记导出功能**
   - PDF 导出
   - Markdown 导出
   - 微信公众号格式

**交付物**:
- ✅ 日记自动生成
- ✅ 日记搜索功能
- ✅ 多格式导出

---

#### Task 5: 数据分析功能（2 天）

**现状**:
- `analytics.html` 页面已完成
- `analyze-data.py` 脚本存在
- 需要连接真实数据

**步骤**:
1. **创建数据分析 API**
   ```python
   @app.route('/api/analytics/news-trend', methods=['GET'])
   def news_trend():
       # 分析新闻趋势
       trend = analyze_news_trend()
       return jsonify(trend)
   
   @app.route('/api/analytics/source-stats', methods=['GET'])
   def source_stats():
       # 信息源统计
       stats = analyze_sources()
       return jsonify(stats)
   ```

2. **更新前端图表**
   - 新闻趋势图
   - 信息源分布图
   - 词云展示

**交付物**:
- ✅ 数据分析 API
- ✅ 实时图表展示
- ✅ 趋势分析

---

#### Task 6: 投资地图系统（3-5 天）

**现状**:
- 规划中
- 无代码基础

**功能设计**:
1. **中国地图** - 30 省份投资评估
2. **越南地图** - 15 省份投资评估
3. **日本地图** - 47 都道府县评估
4. **参数配置** - 自定义权重

**技术选型**:
- ECharts 地图组件
- GeoJSON 数据
- 交互式评估

**交付物**:
- ✅ 三国地图展示
- ✅ 投资评估系统
- ✅ 参数配置界面

---

### 🟢 第三阶段：优化提升（2-3 天）

#### Task 7: 性能优化

1. **前端优化**
   - 图片懒加载
   - 代码分割
   - CSS 压缩

2. **后端优化**
   - 数据库索引优化
   - 缓存策略优化
   - 查询优化

3. **CDN 加速**
   - 静态资源 CDN
   - 图片 CDN

---

#### Task 8: PWA 支持

1. **Service Worker**
2. **离线功能**
3. **添加到主屏幕**
4. **推送通知**

---

#### Task 9: SEO 优化

1. **Meta 标签优化**
2. **网站地图**
3. **结构化数据**
4. ** robots.txt**

---

## 📅 时间表

### Week 1 (3 月 16 日 -22 日)
- ✅ Task 1: 部署 Flask 后端到阿里云 (1-2 天)
- ✅ Task 2: 实现 Token 统计 API (1 天)
- ✅ Task 3: 完善新闻抓取系统 (1-2 天)

**里程碑**: 后端服务上线，"立即体验"按钮启用

### Week 2 (3 月 23 日 -29 日)
- ✅ Task 4: 增强日记系统 (2 天)
- ✅ Task 5: 数据分析功能 (2 天)
- ✅ Task 6: 投资地图系统 (3-5 天，部分完成)

**里程碑**: 核心功能完善，数据实时更新

### Week 3 (3 月 30 日 -4 月 5 日)
- ✅ Task 7: 性能优化 (1 天)
- ✅ Task 8: PWA 支持 (1 天)
- ✅ Task 9: SEO 优化 (1 天)
- ✅ Task 6: 投资地图系统（完成）

**里程碑**: 项目 100% 完成，准备发布

---

## 🎯 立即开始：第一步

### 建议从 Task 2 开始（Token 统计 API）

**原因**:
1. ✅ 数据已有（`stats/2026-03.jsonl`）
2. ✅ 代码基础好（`count-tokens.py` 已完成）
3. ✅ 前端页面已完成（`token-report.html`）
4. ✅ 工作量适中（1 天完成）
5. ✅ 见效快（立即可看到真实数据）

**具体步骤**:

#### Step 1: 创建 Token API 端点（30 分钟）
在 `api_server.py` 中添加：
```python
@app.route('/api/token-stats', methods=['GET'])
def get_token_stats():
    """获取 Token 统计数据"""
    month = request.args.get('month', datetime.now().strftime('%Y-%m'))
    stats_file = Path(config.STATS_DIR) / f"{month}.jsonl"
    
    if not stats_file.exists():
        return jsonify({"error": "No data for this month"}), 404
    
    stats = []
    total_tokens = 0
    total_news = 0
    
    with open(stats_file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            stats.append(data)
            total_tokens += data['total_tokens']
            total_news += data['news_count']
    
    return jsonify({
        "success": True,
        "month": month,
        "data": stats,
        "summary": {
            "total_days": len(stats),
            "total_tokens": total_tokens,
            "total_news": total_news,
            "avg_tokens_per_day": total_tokens // len(stats) if stats else 0
        }
    })
```

#### Step 2: 测试 API（15 分钟）
```bash
# 启动 API 服务器
cd /home/admin/.copaw/guangchu
python3 -m scripts.api_server

# 测试 API
curl "http://localhost:5000/api/token-stats?month=2026-03"
```

#### Step 3: 更新前端（30 分钟）
修改 `web/token-report.html`，添加：
```javascript
async function loadRealTokenData() {
    try {
        const response = await fetch('/api/token-stats?month=2026-03');
        const result = await response.json();
        
        if (result.success) {
            updateStatsDisplay(result.summary);
            updateChart(result.data);
        }
    } catch (error) {
        console.error('加载 Token 数据失败:', error);
    }
}
```

#### Step 4: 配置自动更新（15 分钟）
```bash
# 编辑 crontab
crontab -e

# 添加每日更新任务
0 23 * * * cd /home/admin/.copaw/guangchu && python3 scripts/count-tokens.py
```

**总计**: 约 1.5 小时完成

---

## 🚀 让我们开始吧！

您想从哪个任务开始？

**推荐顺序**:
1. ✅ **Task 2: Token 统计 API** (1 天，见效快)
2. ✅ **Task 1: 部署后端到阿里云** (1-2 天，核心基础)
3. ✅ **Task 3: 完善新闻抓取** (1-2 天，数据源)
4. ✅ **Task 4-6**: 功能增强

**我的建议**: 现在立即开始 **Task 2 (Token 统计 API)**，我可以在 1 小时内帮您完成！

---

*制定时间：2026-03-15*  
*版本：v1.0*
