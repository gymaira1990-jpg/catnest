#!/bin/bash
# 巴别塔实验 · 节点心跳检测脚本
# Babel Experiment · Node Heartbeat Check
#
# 用途: 检测画布服务器可达性, 更新监控状态
# 运行方式: 通过 cron 每1小时执行一次
#
# 配置:
#   CANVAS_URL: 画布服务器地址 (默认 http://127.0.0.1:8800)
#   STATUS_FILE: 状态JSON文件路径 (默认 /var/www/html/status.json)

CANVAS_URL="${1:-http://127.0.0.1:8800}"
STATUS_FILE="${2:-/var/www/html/status.json}"
LOG_FILE="/var/log/babel-heartbeat.log"
TIMESTAMP=$(date -u '+%Y-%m-%dT%H:%M:%SZ')

# 确保目录存在
mkdir -p "$(dirname "$STATUS_FILE")" 2>/dev/null

# 读取当前状态
TOTAL=0; UPTIME=$(date +%s); LAST=""
if [ -f "$STATUS_FILE" ]; then
    TOTAL=$(python3 -c "import json; d=json.load(open('$STATUS_FILE')); print(d.get('total_sent',0))" 2>/dev/null || echo 0)
    UPTIME=$(python3 -c "import json; d=json.load(open('$STATUS_FILE')); print(d.get('uptime_seconds',0))" 2>/dev/null || echo $(date +%s))
    LAST=$(python3 -c "import json; d=json.load(open('$STATUS_FILE')); print(d.get('last_success',''))" 2>/dev/null || echo "")
fi

# 发送检测请求
START_TIME=$(date +%s%N)
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 10 --max-time 15 \
  "$CANVAS_URL/signal" -X POST -H "Content-Type: application/json" \
  -d '{"color":"#9370DB"}' 2>&1)
END_TIME=$(date +%s%N)
LATENCY=$(( (END_TIME - START_TIME) / 1000000 ))

if [ "$HTTP_CODE" = "200" ]; then
    TOTAL=$((TOTAL + 1))
    NEXT_TIME=$(date -u -d '+1 hour' '+%Y-%m-%dT%H:%M:%SZ')
    echo "$TIMESTAMP ✅ 画布可达 | 检测: $TOTAL | 延迟: ${LATENCY}ms" >> "$LOG_FILE"
    STATUS="{\"total_sent\":$TOTAL,\"last_success\":\"$TIMESTAMP\",\"next_heartbeat\":\"$NEXT_TIME\",\"node_online\":true,\"uptime_seconds\":$UPTIME,\"latency_ms\":$LATENCY}"
else
    NEXT_TIME=$(date -u -d '+5 minutes' '+%Y-%m-%dT%H:%M:%SZ')
    echo "$TIMESTAMP ❌ 画布不可达 | HTTP: $HTTP_CODE" >> "$LOG_FILE"
    STATUS="{\"total_sent\":$TOTAL,\"last_success\":\"$LAST\",\"next_heartbeat\":\"$NEXT_TIME\",\"node_online\":false,\"uptime_seconds\":$UPTIME,\"latency_ms\":$LATENCY}"
fi

echo "$STATUS" > "$STATUS_FILE"
echo "status updated: total=$TOTAL, online=$([ "$HTTP_CODE" = "200" ] && echo 'yes' || echo 'no')"
