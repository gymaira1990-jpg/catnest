# deploy/ — 巴别塔实验部署工具

## 文件说明

| 文件 | 说明 |
|:----|:------|
| `deploy.sh` | 一键部署脚本 (Ubuntu/Debian) |
| `babel-canvas.service` | systemd 服务文件 |
| `nginx-camouflage.conf` | Nginx 反向代理配置 |

## 快速部署

```bash
curl -fsSL https://raw.githubusercontent.com/gymaira1990-jpg/babel-experiment/main/deploy/deploy.sh | bash -s your-domain.com
```

## 手动部署

```bash
# 1. 复制 systemd 服务
sudo cp babel-canvas.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now babel-canvas

# 2. 配置 Nginx
sudo cp nginx-camouflage.conf /etc/nginx/sites-available/babel-canvas
# 编辑文件, 将 your-domain.com 替换为实际域名
sudo ln -sf /etc/nginx/sites-available/babel-canvas /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx

# 3. HTTPS (Let's Encrypt)
sudo certbot --nginx -d your-domain.com
```

## 环境变量

见 `config.example.env` (项目根目录)。
