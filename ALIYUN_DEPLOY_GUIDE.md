# 🚀 光储龙虾 - 阿里云部署指南

## 📋 部署前准备

### 1. 阿里云服务器要求

- **操作系统**: Ubuntu 20.04+ / CentOS 7+
- **Python 版本**: Python 3.10+
- **内存**: 建议 2GB+
- **存储**: 建议 20GB+
- **网络**: 开放端口 5000 (API) 和 443 (HTTPS)

### 2. 获取服务器信息

您需要准备以下信息：

- **服务器公网 IP**: 例如 `47.100.xx.xx`
- **SSH 用户名**: 通常是 `admin` 或 `root`
- **SSH 密钥**: 确保已配置 SSH 免密登录

### 3. 配置 SSH 免密登录（如果尚未配置）

```bash
# 生成 SSH 密钥（如果还没有）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 复制公钥到服务器
ssh-copy-id admin@your-server-ip

# 测试连接
ssh admin@your-server-ip
```

---

## 🎯 快速部署（推荐）

### 方法一：使用部署脚本（最简单）

```bash
cd /home/admin/.copaw/guangchu

# 执行部署脚本
./deploy-to-aliyun.sh [服务器 IP]

# 例如：
./deploy-to-aliyun.sh 47.100.xx.xx
```

脚本会自动完成：
- ✅ SSH 连接检查
- ✅ 文件同步
- ✅ 依赖安装
- ✅ 虚拟环境创建
- ✅ systemd 服务配置
- ✅ Nginx 配置（可选）

---

### 方法二：手动部署

#### 步骤 1: 连接服务器

```bash
ssh admin@your-server-ip
```

#### 步骤 2: 安装系统依赖

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx git

# CentOS/RHEL
sudo yum install -y python3 python3-pip nginx git
```

#### 步骤 3: 克隆项目

```bash
cd ~
git clone https://github.com/xuegangwu/guangchu.git
cd guangchu
```

#### 步骤 4: 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 步骤 5: 安装 Python 依赖

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 步骤 6: 配置环境变量

```bash
cat > .env << 'EOF'
FLASK_ENV=production
FLASK_APP=scripts/api_server.py
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///search.db
API_HOST=0.0.0.0
API_PORT=5000
LOG_LEVEL=INFO
EOF
```

#### 步骤 7: 测试运行

```bash
# 直接运行
python3 -m scripts.api_server

# 或使用 Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 scripts.api_server:app
```

访问 `http://your-server-ip:5000/api/health` 验证服务

---

## 🔧 配置 systemd 服务（生产环境必需）

### 创建服务文件

```bash
sudo tee /etc/systemd/system/guangchu-api.service > /dev/null << 'EOF'
[Unit]
Description=Guangchu Solar-Storage API Service
After=network.target

[Service]
Type=notify
User=admin
Group=admin
WorkingDirectory=/home/admin/guangchu
Environment="PATH=/home/admin/guangchu/venv/bin"
ExecStart=/home/admin/guangchu/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 scripts.api_server:app
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=guangchu-api

[Install]
WantedBy=multi-user.target
EOF
```

### 启用并启动服务

```bash
sudo systemctl daemon-reload
sudo systemctl enable guangchu-api
sudo systemctl start guangchu-api
```

### 检查服务状态

```bash
# 查看状态
sudo systemctl status guangchu-api

# 查看日志
sudo journalctl -u guangchu-api -f

# 重启服务
sudo systemctl restart guangchu-api

# 停止服务
sudo systemctl stop guangchu-api
```

---

## 🌐 配置 Nginx 反向代理

### 1. 创建 Nginx 配置

```bash
sudo tee /etc/nginx/sites-available/guangchu > /dev/null << 'EOF'
server {
    listen 80;
    server_name your-domain.com;
    
    # 重定向到 HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    # SSL 证书配置
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # SSL 优化
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # 日志
    access_log /var/log/nginx/guangchu-access.log;
    error_log /var/log/nginx/guangchu-error.log;
    
    # 代理到 Gunicorn
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # 静态文件
    location /static {
        alias /home/admin/guangchu/web;
        expires 30d;
    }
}
EOF
```

### 2. 启用站点

```bash
sudo ln -sf /etc/nginx/sites-available/guangchu /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 3. 申请 SSL 证书

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx  # Ubuntu
sudo yum install certbot python3-certbot-nginx  # CentOS

# 申请证书
sudo certbot --nginx -d your-domain.com
```

---

## 📊 配置防火墙

### 阿里云安全组配置

在阿里云控制台配置安全组规则：

| 端口 | 协议 | 授权对象 | 说明 |
|------|------|----------|------|
| 22 | TCP | 0.0.0.0/0 | SSH |
| 80 | TCP | 0.0.0.0/0 | HTTP |
| 443 | TCP | 0.0.0.0/0 | HTTPS |
| 5000 | TCP | 127.0.0.1 | API（仅本地） |

### Ubuntu UFW 防火墙

```bash
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable
```

---

## 🔄 配置定时任务

### 编辑 crontab

```bash
crontab -e
```

### 添加定时任务

```bash
# 每天早上 8 点抓取英文新闻
0 8 * * * cd /home/admin/guangchu && /home/admin/guangchu/venv/bin/python3 scripts/fetch-news.py >> logs/fetch-news.log 2>&1

# 每天早上 9 点抓取中文新闻
0 9 * * * cd /home/admin/guangchu && /home/admin/guangchu/venv/bin/python3 scripts/fetch-chinese-news.py >> logs/fetch-chinese-news.log 2>&1

# 每天早上 10 点处理数据
0 10 * * * cd /home/admin/guangchu && /home/admin/guangchu/venv/bin/python3 scripts/data-processing-pipeline.py >> logs/pipeline.log 2>&1

# 每天晚上 11 点统计 Token
0 23 * * * cd /home/admin/guangchu && /home/admin/guangchu/venv/bin/python3 scripts/count-tokens.py >> logs/token-stats.log 2>&1
```

---

## ✅ 验证部署

### 1. 健康检查

```bash
curl http://localhost:5000/api/health
```

预期响应：
```json
{
  "success": true,
  "status": "healthy",
  "version": "v2.2",
  "timestamp": "2026-03-15T12:00:00"
}
```

### 2. Token 统计 API

```bash
curl http://localhost:5000/api/token-stats?month=2026-03
```

### 3. 搜索 API

```bash
curl "http://localhost:5000/api/search?q=光伏&limit=5"
```

### 4. 外部访问测试

```bash
# 从本地测试
curl http://your-server-ip:5000/api/health

# 如果配置了域名
curl https://your-domain.com/api/health
```

---

## 🔍 故障排查

### 服务无法启动

```bash
# 查看 systemd 日志
sudo journalctl -u guangchu-api -n 50

# 查看应用日志
tail -f /home/admin/guangchu/logs/api.log

# 检查端口占用
sudo lsof -i :5000
```

### 数据库错误

```bash
# 检查数据库文件
ls -lh /home/admin/guangchu/search.db

# 测试数据库连接
cd /home/admin/guangchu
source venv/bin/activate
python3 -c "from scripts.advanced_search import AdvancedSearch; s = AdvancedSearch(); print(s.search('测试'))"
```

### Nginx 错误

```bash
# 测试配置
sudo nginx -t

# 查看错误日志
sudo tail -f /var/log/nginx/guangchu-error.log
```

---

## 📈 性能优化建议

### 1. Gunicorn 优化

```bash
# 根据服务器配置调整 worker 数量
# 公式：workers = (2 x CPU 核心数) + 1
gunicorn -w 4 -k gthread -t 120 -b 0.0.0.0:5000 scripts.api_server:app
```

### 2. 启用缓存

```bash
# 安装 Redis
sudo apt install redis-server

# 在 .env 中配置
REDIS_URL=redis://localhost:6379/0
```

### 3. 数据库优化

```bash
# 为常用查询字段添加索引
# 在 search.db 中执行：
sqlite3 search.db "CREATE INDEX IF NOT EXISTS idx_news_date ON news(date);"
```

---

## 🎉 部署完成！

### 访问地址

- **API 服务**: `http://your-server-ip:5000`
- **健康检查**: `http://your-server-ip:5000/api/health`
- **Token 统计**: `http://your-server-ip:5000/api/token-stats`
- **搜索接口**: `http://your-server-ip:5000/api/search?q=关键词`

### 下一步

1. ✅ 更新前端配置中的 API 地址
2. ✅ 配置域名和 SSL 证书
3. ✅ 设置定时任务更新新闻数据
4. ✅ 配置监控和告警

---

## 📞 技术支持

如有问题，请检查：
- 系统日志：`sudo journalctl -xe`
- 应用日志：`/home/admin/guangchu/logs/`
- Nginx 日志：`/var/log/nginx/`

---

*最后更新：2026-03-15*  
*版本：v2.2*
