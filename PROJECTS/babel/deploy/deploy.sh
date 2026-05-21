#!/bin/bash
# 巴别塔实验 · 一键部署脚本
# Babel Experiment · One-Click Deployment
#
# 用法:
#   curl -fsSL https://raw.githubusercontent.com/gymaira1990-jpg/babel-experiment/main/deploy/deploy.sh | bash
#   或:
#   bash deploy/deploy.sh [--domain your-domain.com] [--port 8800]
#
# 前提: Ubuntu 22.04+ / Debian 12+, Python 3.10+

set -e

# ─── 配置 ──────────────────────────────
DOMAIN="${1:-localhost}"
CANVAS_PORT="${2:-8800}"
INSTALL_DIR="/opt/babel-canvas"
REPO_URL="https://github.com/gymaira1990-jpg/babel-experiment.git"

# 颜色
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

info()  { echo -e "${GREEN}[✓]${NC} $1"; }
warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
error() { echo -e "${RED}[✗]${NC} $1"; exit 1; }

echo "╔══════════════════════════════════════╗"
echo "║  巴别塔实验 · 一键部署               ║"
echo "║  Babel Experiment · Deploy           ║"
echo "╚══════════════════════════════════════╝"
echo ""

# ─── Step 1: 系统检查 ───
echo "[1/6] 检查系统环境..."
command -v python3       >/dev/null 2>&1 || error "需要 Python 3"
command -v git           >/dev/null 2>&1 || { warn "正在安装 git..."; apt-get update -qq && apt-get install -y -qq git; }
command -v nginx         >/dev/null 2>&1 || { warn "正在安装 Nginx..."; apt-get update -qq && apt-get install -y -qq nginx; }
info "系统就绪"

# ─── Step 2: 克隆仓库 ───
echo "[2/6] 获取巴别塔项目..."
if [ -d "$INSTALL_DIR" ]; then
    warn "目录已存在, 更新中..."
    cd "$INSTALL_DIR" && git pull
else
    git clone --depth 1 "$REPO_URL" "$INSTALL_DIR"
fi
info "项目已获取"

# ─── Step 3: 配置画布服务器 ───
echo "[3/6] 配置画布服务器..."
cd "$INSTALL_DIR"

# 创建环境文件
GOD_PASS=$(openssl rand -hex 16)
cat > .env << EOF
PORT=$CANVAS_PORT
CANVAS_WIDTH=100
CANVAS_HEIGHT=100
PIXEL_SIZE=4
GROWTH_THRESHOLD=0.7
GROWTH_SIZE=30
AUTO_GROWTH=true
FLASK_SECRET=$(openssl rand -hex 16)
GOD_PASSWORD=$GOD_PASS
EOF

# 创建虚拟环境并安装依赖
python3 -m venv venv
source venv/bin/activate
pip install -q flask gunicorn 2>&1 | tail -1
info "画布服务器已配置"

# ─── Step 4: 配置系统服务 ───
echo "[4/6] 配置系统服务..."
cp deploy/babel-canvas.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable babel-canvas
systemctl start babel-canvas
info "系统服务已启动 (端口: $CANVAS_PORT)"

# ─── Step 5: 配置 Nginx 反向代理 ───
echo "[5/6] 配置 Nginx 反向代理..."
if [ "$DOMAIN" != "localhost" ]; then
    sed "s/your-domain.com/$DOMAIN/g" deploy/nginx-camouflage.conf > /etc/nginx/sites-available/babel-canvas
    ln -sf /etc/nginx/sites-available/babel-canvas /etc/nginx/sites-enabled/
    rm -f /etc/nginx/sites-enabled/default
    nginx -t && systemctl reload nginx
    info "Nginx 已配置 (域名: $DOMAIN)"
    
    # 可选: Let's Encrypt 证书
    warn "如需 HTTPS, 执行: sudo certbot --nginx -d $DOMAIN"
else
    warn "跳过 Nginx 配置 (未指定域名)"
    warn "画布可通过 http://localhost:$CANVAS_PORT/view 访问"
fi

# ─── Step 6: 设置心跳 ───
echo "[6/6] 设置定期心跳..."
CANVAS_URL="http://127.0.0.1:$CANVAS_PORT"
(crontab -l 2>/dev/null | grep -v 'workshop'; echo "0 0 * * * cd $INSTALL_DIR && source venv/bin/activate && python workshop.py --once --url $CANVAS_URL >> $INSTALL_DIR/heartbeat.log 2>&1") | crontab -
info "每日心跳已设置 (UTC 00:00)"

# ─── 完成 ───
echo ""
echo "╔══════════════════════════════════════╗"
echo "║  ✅ 巴别塔实验部署完成！              ║"
echo "║                                      ║"
if [ "$DOMAIN" != "localhost" ]; then
    echo "║  访问: https://$DOMAIN/            ║"
else
    echo "║  访问: http://localhost:$CANVAS_PORT/view  ║"
fi
echo "║  管理: http://localhost:$CANVAS_PORT/admin  ║"
echo "║  密码: $GOD_PASS                            ║"
echo "║  配置: $INSTALL_DIR/.env                     ║"
echo "║  重置: cd $INSTALL_DIR && source venv/bin/activate && python canvas_server.py --reset-password  ║"
echo "║  文档: $REPO_URL    ║"
echo "╚══════════════════════════════════════╝"
