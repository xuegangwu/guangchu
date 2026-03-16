#!/bin/bash
# 光储龙虾项目 - 阿里云部署脚本
# 用法：./deploy-to-aliyun.sh [服务器 IP]

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置变量
ALIYUN_USER="${ALIYUN_USER:-admin}"
ALIYUN_HOST="${1:-}"
PROJECT_NAME="guangchu"
REMOTE_DIR="/home/${ALIYUN_USER}/${PROJECT_NAME}"
BACKUP_DIR="/home/${ALIYUN_USER}/${PROJECT_NAME}_backup_$(date +%Y%m%d_%H%M%S)"

# 检查参数
if [ -z "$ALIYUN_HOST" ]; then
    echo -e "${RED}错误：请提供阿里云服务器 IP 地址${NC}"
    echo "用法：$0 [服务器 IP]"
    echo "或设置环境变量：export ALIYUN_HOST=your.server.ip"
    exit 1
fi

echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}光储龙虾项目 - 阿里云部署脚本${NC}"
echo -e "${GREEN}======================================${NC}"
echo ""
echo -e "${YELLOW}服务器信息:${NC}"
echo "  用户：${ALIYUN_USER}"
echo "  主机：${ALIYUN_HOST}"
echo "  远程目录：${REMOTE_DIR}"
echo ""

# 确认部署
read -p "确认部署到 ${ALIYUN_HOST}? (y/n): " confirm
if [ "$confirm" != "y" ]; then
    echo -e "${YELLOW}部署已取消${NC}"
    exit 0
fi

# 步骤 1: 检查 SSH 连接
echo -e "\n${YELLOW}[1/8] 检查 SSH 连接...${NC}"
if ! ssh -o ConnectTimeout=5 ${ALIYUN_USER}@${ALIYUN_HOST} "echo 'SSH 连接成功'" > /dev/null 2>&1; then
    echo -e "${RED}错误：无法连接到服务器 ${ALIYUN_HOST}${NC}"
    echo "请检查:"
    echo "  1. 服务器 IP 是否正确"
    echo "  2. SSH 密钥是否已配置"
    echo "  3. 服务器防火墙是否开放 SSH 端口"
    exit 1
fi
echo -e "${GREEN}✓ SSH 连接成功${NC}"

# 步骤 2: 在服务器创建项目目录
echo -e "\n${YELLOW}[2/8] 创建远程项目目录...${NC}"
ssh ${ALIYUN_USER}@${ALIYUN_HOST} "mkdir -p ${REMOTE_DIR}"
echo -e "${GREEN}✓ 目录创建完成${NC}"

# 步骤 3: 备份旧版本（如果存在）
echo -e "\n${YELLOW}[3/8] 备份旧版本...${NC}"
if ssh ${ALIYUN_USER}@${ALIYUN_HOST} "[ -d ${REMOTE_DIR}/.git ]"; then
    ssh ${ALIYUN_USER}@${ALIYUN_HOST} "cp -r ${REMOTE_DIR} ${BACKUP_DIR}"
    echo -e "${GREEN}✓ 已备份到 ${BACKUP_DIR}${NC}"
else
    echo -e "${YELLOW}  首次部署，跳过备份${NC}"
fi

# 步骤 4: 同步文件到服务器
echo -e "\n${YELLOW}[4/8] 同步项目文件...${NC}"
rsync -avz --progress \
    --exclude '.git/' \
    --exclude '__pycache__/' \
    --exclude '*.pyc' \
    --exclude '.coverage' \
    --exclude '*.db' \
    --exclude 'raw/' \
    --exclude 'processed/' \
    --exclude 'logs/' \
    --exclude '.env' \
    /home/admin/.copaw/guangchu/ ${ALIYUN_USER}@${ALIYUN_HOST}:${REMOTE_DIR}/

echo -e "${GREEN}✓ 文件同步完成${NC}"

# 步骤 5: 安装依赖
echo -e "\n${YELLOW}[5/8] 安装 Python 依赖...${NC}"
ssh ${ALIYUN_USER}@${ALIYUN_HOST} << 'ENDSSH'
cd /home/admin/guangchu

# 检查 Python 版本
python3 --version || {
    echo "错误：Python3 未安装"
    exit 1
}

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境并安装依赖
source venv/bin/activate
pip install --upgrade pip

# 安装 requirements
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "安装基础依赖..."
    pip install flask requests beautifulsoup4 googletrans==4.0.0-rc1 gunicorn
fi

echo "依赖安装完成"
ENDSSH

echo -e "${GREEN}✓ 依赖安装完成${NC}"

# 步骤 6: 配置环境变量
echo -e "\n${YELLOW}[6/8] 配置环境变量...${NC}"
ssh ${ALIYUN_USER}@${ALIYUN_HOST} << 'ENDSSH'
cd /home/admin/guangchu

# 创建 .env 文件
cat > .env << 'EOF'
# 光储龙虾环境变量配置
FLASK_ENV=production
FLASK_APP=scripts/api_server.py
SECRET_KEY=$(openssl rand -hex 32)

# 数据库配置
DATABASE_URL=sqlite:///search.db

# API 配置
API_HOST=0.0.0.0
API_PORT=5000

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/api.log
EOF

echo "环境变量配置完成"
ENDSSH

echo -e "${GREEN}✓ 环境变量配置完成${NC}"

# 步骤 7: 配置 systemd 服务
echo -e "\n${YELLOW}[7/8] 配置 systemd 服务...${NC}"
ssh ${ALIYUN_USER}@${ALIYUN_HOST} << 'ENDSSH'
# 创建 systemd 服务文件
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

# 安全配置
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

# 重载 systemd
sudo systemctl daemon-reload

# 启用并启动服务
sudo systemctl enable guangchu-api
sudo systemctl start guangchu-api

# 检查服务状态
sudo systemctl status guangchu-api --no-pager

echo "systemd 服务配置完成"
ENDSSH

echo -e "${GREEN}✓ systemd 服务配置完成${NC}"

# 步骤 8: 配置 Nginx（可选）
echo -e "\n${YELLOW}[8/8] 配置 Nginx 反向代理...${NC}"
read -p "是否配置 Nginx 反向代理？(需要域名和 SSL 证书) (y/n): " setup_nginx
if [ "$setup_nginx" = "y" ]; then
    read -p "请输入域名 (例如：api.guangchu.com): " domain_name
    
    ssh ${ALIYUN_USER}@${ALIYUN_HOST} << ENDSSH
    # 创建 Nginx 配置
    sudo tee /etc/nginx/sites-available/guangchu > /dev/null << 'EOF'
server {
    listen 80;
    server_name ${domain_name};
    
    # 重定向到 HTTPS
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name ${domain_name};
    
    # SSL 证书配置（需要先申请）
    ssl_certificate /etc/letsencrypt/live/${domain_name}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${domain_name}/privkey.pem;
    
    # SSL 优化
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # 日志
    access_log /var/log/nginx/guangchu-access.log;
    error_log /var/log/nginx/guangchu-error.log;
    
    # 代理到 Gunicorn
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # 静态文件（可选）
    location /static {
        alias /home/admin/guangchu/web;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
EOF
    
    # 启用站点
    sudo ln -sf /etc/nginx/sites-available/guangchu /etc/nginx/sites-enabled/
    
    # 测试 Nginx 配置
    sudo nginx -t
    
    # 重载 Nginx
    sudo systemctl reload nginx
    
    echo "Nginx 配置完成"
    echo ""
    echo -e "${YELLOW}下一步：申请 SSL 证书${NC}"
    echo "运行以下命令申请 Let's Encrypt 证书:"
    echo "  sudo certbot --nginx -d ${domain_name}"
ENDSSH
    
    echo -e "${GREEN}✓ Nginx 配置完成${NC}"
else
    echo -e "${YELLOW}  跳过 Nginx 配置，可直接通过 IP:5000 访问${NC}"
fi

# 部署完成
echo ""
echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}✓ 部署完成！${NC}"
echo -e "${GREEN}======================================${NC}"
echo ""
echo -e "${YELLOW}服务信息:${NC}"
echo "  API 地址：http://${ALIYUN_HOST}:5000"
echo "  健康检查：http://${ALIYUN_HOST}:5000/api/health"
echo "  Token 统计：http://${ALIYUN_HOST}:5000/api/token-stats"
echo ""
echo -e "${YELLOW}管理命令:${NC}"
echo "  查看状态：ssh ${ALIYUN_USER}@${ALIYUN_HOST} 'sudo systemctl status guangchu-api'"
echo "  重启服务：ssh ${ALIYUN_USER}@${ALIYUN_HOST} 'sudo systemctl restart guangchu-api'"
echo "  查看日志：ssh ${ALIYUN_USER}@${ALIYUN_HOST} 'sudo journalctl -u guangchu-api -f'"
echo "  停止服务：ssh ${ALIYUN_USER}@${ALIYUN_HOST} 'sudo systemctl stop guangchu-api'"
echo ""
echo -e "${YELLOW}下一步操作:${NC}"
echo "  1. 更新前端配置中的 API 地址"
echo "  2. 配置域名和 SSL 证书（如已设置 Nginx）"
echo "  3. 设置定时任务更新新闻数据"
echo ""
echo -e "${GREEN}部署成功！🎉${NC}"
