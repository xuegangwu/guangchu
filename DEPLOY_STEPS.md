# 🚀 光储龙虾 - 阿里云服务器部署步骤

**服务器 IP**: 121.43.69.200  
**部署时间**: 2026-03-15

---

## 📋 部署前准备

由于 SSH 密钥尚未配置到服务器，请按以下步骤操作：

### 方案一：使用 SSH 密码认证（推荐用于首次部署）

#### 步骤 1: 手动上传文件到服务器

```bash
# 1. 登录到阿里云服务器
ssh admin@121.43.69.200
# 输入您的服务器密码

# 2. 在服务器上创建项目目录
mkdir -p ~/guangchu
cd ~/guangchu

# 3. 从 GitHub 克隆项目（推荐）
git clone https://github.com/xuegangwu/guangchu.git .
# 或者使用 SCP 上传本地文件
```

#### 步骤 2: 在服务器上执行安装

```bash
# 在服务器上执行以下命令

# 1. 安装系统依赖
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx git curl

# 2. 创建 Python 虚拟环境
python3 -m venv venv
source venv/bin/activate

# 3. 升级 pip
pip install --upgrade pip

# 4. 安装项目依赖
pip install flask requests beautifulsoup4 googletrans==4.0.0-rc1 gunicorn python-dotenv

# 5. 创建环境变量文件
cat > .env << 'EOF'
FLASK_ENV=production
FLASK_APP=scripts/api_server.py
SECRET_KEY=$(openssl rand -hex 32)
DATABASE_URL=sqlite:///search.db
API_HOST=0.0.0.0
API_PORT=5000
LOG_LEVEL=INFO
LOG_FILE=logs/api.log
EOF

# 6. 创建日志目录
mkdir -p logs

# 7. 测试运行
python3 -m scripts.api_server &
# 按 Ctrl+C 停止测试

# 8. 配置 systemd 服务（见下方）
```

---

### 方案二：配置 SSH 密钥免密登录（推荐用于后续部署）

#### 在本地执行：

```bash
# 1. 将公钥复制到服务器（需要输入一次密码）
ssh-copy-id admin@121.43.69.200

# 如果 ssh-copy-id 不可用，使用以下方法：
# 手动复制公钥内容
cat ~/.ssh/id_ed25519.pub
# 复制输出内容

# 2. 登录服务器
ssh admin@121.43.69.200

# 3. 在服务器上执行：
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "您的公钥内容" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# 4. 退出并测试免密登录
exit
ssh admin@121.43.69.200
# 应该不需要密码了
```

---

## 🔧 完整部署命令（在服务器上执行）

### 一键部署脚本

登录服务器后，执行以下完整脚本：

```bash
#!/bin/bash
# guangchu-deploy.sh

set -e

echo "======================================"
echo "光储龙虾项目 - 阿里云部署"
echo "======================================"

# 1. 系统更新
echo "[1/10] 更新系统..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx git curl wget

# 2. 创建项目目录
echo "[2/10] 创建项目目录..."
cd ~
if [ ! -d "guangchu" ]; then
    git clone https://github.com/xuegangwu/guangchu.git
fi
cd guangchu

# 3. 创建虚拟环境
echo "[3/10] 创建 Python 虚拟环境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# 4. 安装依赖
echo "[4/10] 安装 Python 依赖..."
pip install --upgrade pip
pip install flask requests beautifulsoup4 googletrans==4.0.0-rc1 gunicorn python-dotenv lxml pytest

# 5. 创建环境变量
echo "[5/10] 配置环境变量..."
cat > .env << 'EOF'
FLASK_ENV=production
FLASK_APP=scripts/api_server.py
SECRET_KEY=guangchu-secret-key-$(date +%s)
DATABASE_URL=sqlite:///search.db
API_HOST=0.0.0.0
API_PORT=5000
LOG_LEVEL=INFO
LOG_FILE=logs/api.log
EOF

# 6. 创建必要目录
echo "[6/10] 创建目录结构..."
mkdir -p logs raw processed stats config

# 7. 配置 systemd 服务
echo "[7/10] 配置 systemd 服务..."
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
EnvironmentFile=/home/admin/guangchu/.env
ExecStart=/home/admin/guangchu/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 scripts.api_server:app
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=guangchu-api
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

# 8. 启动服务
echo "[8/10] 启动服务..."
sudo systemctl daemon-reload
sudo systemctl enable guangchu-api
sudo systemctl start guangchu-api

# 9. 配置防火墙
echo "[9/10] 配置防火墙..."
sudo ufw allow 22/tcp || true
sudo ufw allow 80/tcp || true
sudo ufw allow 443/tcp || true
sudo ufw --force enable || true

# 10. 验证部署
echo "[10/10] 验证部署..."
sleep 3

echo ""
echo "======================================"
echo "部署完成！"
echo "======================================"
echo ""
echo "服务状态检查:"
sudo systemctl status guangchu-api --no-pager
echo ""
echo "API 测试:"
curl -s http://localhost:5000/api/health | python3 -m json.tool
echo ""
echo "Token 统计测试:"
curl -s http://localhost:5000/api/token-stats?month=2026-03 | python3 -m json.tool || echo "暂无数据"
echo ""
echo "======================================"
echo "访问地址:"
echo "  API: http://121.43.69.200:5000"
echo "  健康检查：http://121.43.69.200:5000/api/health"
echo "  Token 统计：http://121.43.69.200:5000/api/token-stats"
echo ""
echo "管理命令:"
echo "  查看状态：sudo systemctl status guangchu-api"
echo "  查看日志：sudo journalctl -u guangchu-api -f"
echo "  重启服务：sudo systemctl restart guangchu-api"
echo "======================================"
```

### 执行部署

```bash
# 1. 将上述脚本保存为 guangchu-deploy.sh
nano guangchu-deploy.sh
# 粘贴内容并保存

# 2. 赋予执行权限
chmod +x guangchu-deploy.sh

# 3. 执行部署
./guangchu-deploy.sh
```

---

## 📊 配置 Nginx（可选，用于生产环境）

### 创建 Nginx 配置

```bash
sudo tee /etc/nginx/sites-available/guangchu > /dev/null << 'EOF'
server {
    listen 80;
    server_name 121.43.69.200;
    
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
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # 静态文件
    location /static {
        alias /home/admin/guangchu/web;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# 启用站点
sudo ln -sf /etc/nginx/sites-available/guangchu /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重载 Nginx
sudo systemctl reload nginx
```

---

## 🔍 验证部署

### 测试 API

```bash
# 健康检查
curl http://121.43.69.200:5000/api/health

# Token 统计
curl http://121.43.69.200:5000/api/token-stats?month=2026-03

# 搜索测试
curl "http://121.43.69.200:5000/api/search?q=光伏&limit=5"
```

### 检查服务状态

```bash
# 查看服务状态
sudo systemctl status guangchu-api

# 查看实时日志
sudo journalctl -u guangchu-api -f

# 查看进程
ps aux | grep gunicorn
```

---

## ⚠️ 常见问题

### 1. 端口被占用

```bash
# 检查端口占用
sudo lsof -i :5000

# 如果端口被占用，停止占用进程或修改配置
sudo systemctl stop guangchu-api
# 修改 .env 中的 API_PORT
sudo systemctl start guangchu-api
```

### 2. 权限问题

```bash
# 确保目录权限正确
sudo chown -R admin:admin ~/guangchu
chmod -R 755 ~/guangchu
```

### 3. 依赖安装失败

```bash
# 安装系统级依赖
sudo apt install -y python3-dev build-essential libxml2-dev libxslt1-dev

# 重新安装 Python 依赖
source venv/bin/activate
pip install --no-cache-dir -r requirements.txt
```

### 4. 数据库不存在

```bash
# 如果 search.db 不存在，需要先运行数据抓取脚本
cd ~/guangchu
source venv/bin/activate
python3 scripts/fetch-news.py
python3 scripts/fetch-chinese-news.py
```

---

## 📈 配置定时任务

```bash
# 编辑 crontab
crontab -e

# 添加以下任务
0 8 * * * cd /home/admin/guangchu && /home/admin/guangchu/venv/bin/python3 scripts/fetch-news.py >> logs/fetch-news.log 2>&1
0 9 * * * cd /home/admin/guangchu && /home/admin/guangchu/venv/bin/python3 scripts/fetch-chinese-news.py >> logs/fetch-chinese-news.log 2>&1
0 23 * * * cd /home/admin/guangchu && /home/admin/guangchu/venv/bin/python3 scripts/count-tokens.py >> logs/token-stats.log 2>&1
```

---

## 🎉 部署完成！

### 访问地址

- **API 服务**: http://121.43.69.200:5000
- **健康检查**: http://121.43.69.200:5000/api/health
- **Token 统计**: http://121.43.69.200:5000/api/token-stats
- **搜索接口**: http://121.43.69.200:5000/api/search?q=关键词

### 下一步

1. ✅ 测试所有 API 端点
2. ✅ 上传新闻数据（如果数据库为空）
3. ✅ 更新前端配置指向新服务器
4. ✅ 配置域名（可选）
5. ✅ 配置 SSL 证书（可选）

---

*部署指南版本：v1.0*  
*最后更新：2026-03-15*
