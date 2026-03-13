#!/bin/bash
# iFlow API Key 管理器
# 检查 API Key 有效期，到期前自动提醒更新

set -e

# 配置
IFLOW_SETTINGS="$HOME/.iflow/settings.json"
IFLOW_SCRIPT="$HOME/.openclaw/workspace/scripts/iflow.sh"
OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"
STATE_FILE="$HOME/.openclaw/workspace/.iflow-key-state.json"
LOG_FILE="$HOME/.openclaw/workspace/logs/iflow-key-manager.log"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 确保日志目录存在
mkdir -p "$(dirname "$LOG_FILE")"

# 读取当前 API Key 和配置日期
get_current_key_info() {
    if [[ ! -f "$STATE_FILE" ]]; then
        # 首次运行，创建状态文件
        echo "{\"configDate\": \"$(date -Iseconds)\", \"expiryDate\": \"$(date -v+7d -Iseconds 2>/dev/null || date -d '+7 days' -Iseconds 2>/dev/null)\"}" > "$STATE_FILE"
    fi
    
    CONFIG_DATE=$(cat "$STATE_FILE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('configDate', 'unknown'))" 2>/dev/null || echo "unknown")
    EXPIRY_DATE=$(cat "$STATE_FILE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('expiryDate', 'unknown'))" 2>/dev/null || echo "unknown")
    
    echo "$CONFIG_DATE|$EXPIRY_DATE"
}

# 计算剩余天数
get_remaining_days() {
    python3 << 'PYTHON'
import json
from datetime import datetime

try:
    with open('/Users/jesson/.openclaw/workspace/.iflow-key-state.json', 'r') as f:
        state = json.load(f)
    
    expiry_str = state.get('expiryDate', '')
    if not expiry_str:
        print("-1")
        exit()
    
    # 解析到期日期
    expiry = datetime.fromisoformat(expiry_str.replace('Z', '+00:00'))
    now = datetime.now(expiry.tzinfo)
    
    diff = expiry - now
    print(max(0, diff.days))
except Exception as e:
    print("-1")
PYTHON
}

# 更新状态文件（配置新 Key 时调用）
update_state() {
    local config_date=$(date -Iseconds)
    local expiry_date=$(date -v+7d -Iseconds 2>/dev/null || date -d '+7 days' -Iseconds 2>/dev/null)
    
    echo "{\"configDate\": \"$config_date\", \"expiryDate\": \"$expiry_date\", \"notified\": false}" > "$STATE_FILE"
    log "✅ 状态文件已更新，到期日：$expiry_date"
}

# 发送通知
send_notification() {
    local days=$1
    local message=$2
    
    log "⚠️ $message"
    
    # 写入 HEARTBEAT.md 提醒
    if ! grep -q "iFlow API Key 即将过期" "$HOME/.openclaw/workspace/HEARTBEAT.md" 2>/dev/null; then
        cat >> "$HOME/.openclaw/workspace/HEARTBEAT.md" << EOF

---
## 🚨 iFlow API Key 紧急提醒

**到期时间**: $(date -v+${days}d '+%Y-%m-%d' 2>/dev/null || date -d "+$days days" '+%Y-%m-%d' 2>/dev/null)
**剩余天数**: $days 天
**提醒时间**: $(date '+%Y-%m-%d %H:%M:%S')

请立即更新 API Key：
1. 访问 https://iflow.cn/?open=setting
2. 生成新的 API Key
3. 运行：~/.openclaw/workspace/scripts/iflow-update-key.sh <新 Key>
EOF
    fi
}

# 主检查逻辑
check_key_expiry() {
    log "🔍 检查 iFlow API Key 有效期..."
    
    REMAINING_DAYS=$(get_remaining_days)
    
    if [[ "$REMAINING_DAYS" == "-1" ]]; then
        log "⚠️ 无法读取到期日期，请运行 update_state 初始化"
        exit 0
    fi
    
    log "📅 剩余有效期：$REMAINING_DAYS 天"
    
    if [[ $REMAINING_DAYS -le 0 ]]; then
        log "${RED}🚨 API Key 已过期！请立即更新！${NC}"
        send_notification 0 "🚨 iFlow API Key 已过期！"
        exit 1
    elif [[ $REMAINING_DAYS -le 1 ]]; then
        log "${RED}🚨 API Key 将在 1 天内过期！${NC}"
        send_notification 1 "🚨 iFlow API Key 将在 1 天内过期！"
        exit 0
    elif [[ $REMAINING_DAYS -le 3 ]]; then
        log "${YELLOW}⚠️ API Key 将在 $REMAINING_DAYS 天后过期${NC}"
        send_notification $REMAINING_DAYS "⚠️ iFlow API Key 将在 $REMAINING_DAYS 天后过期"
        exit 0
    else
        log "${GREEN}✅ API Key 状态正常${NC}"
        exit 0
    fi
}

# 显示帮助
show_help() {
    echo "iFlow API Key 管理器"
    echo ""
    echo "用法："
    echo "  $0 check       - 检查 API Key 有效期"
    echo "  $0 init        - 初始化状态文件（首次使用）"
    echo "  $0 status      - 显示当前状态"
    echo "  $0 help        - 显示帮助信息"
    echo ""
    echo "示例："
    echo "  $0 check       # 每天通过 cron 自动检查"
    echo "  $0 status      # 查看当前 Key 的到期时间"
}

# 显示状态
show_status() {
    echo "📊 iFlow API Key 状态"
    echo "===================="
    
    INFO=$(get_current_key_info)
    CONFIG_DATE=$(echo "$INFO" | cut -d'|' -f1)
    EXPIRY_DATE=$(echo "$INFO" | cut -d'|' -f2)
    REMAINING_DAYS=$(get_remaining_days)
    
    echo "配置日期：$CONFIG_DATE"
    echo "到期日期：$EXPIRY_DATE"
    echo "剩余天数：$REMAINING_DAYS"
    
    if [[ $REMAINING_DAYS -le 0 ]]; then
        echo -e "状态：${RED}已过期${NC}"
    elif [[ $REMAINING_DAYS -le 3 ]]; then
        echo -e "状态：${YELLOW}即将过期${NC}"
    else
        echo -e "状态：${GREEN}正常${NC}"
    fi
}

# 主程序
case "${1:-check}" in
    check)
        check_key_expiry
        ;;
    init)
        update_state
        ;;
    status)
        show_status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令：$1"
        show_help
        exit 1
        ;;
esac
