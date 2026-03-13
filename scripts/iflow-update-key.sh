#!/bin/bash
# iFlow API Key 更新脚本
# 用于更新 iFlow API Key 到所有配置文件

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 配置文件路径
IFLOW_SETTINGS="$HOME/.iflow/settings.json"
IFLOW_SCRIPT="$HOME/.openclaw/workspace/scripts/iflow.sh"
OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"
STATE_FILE="$HOME/.openclaw/workspace/.iflow-key-state.json"
LOG_FILE="$HOME/.openclaw/workspace/logs/iflow-key-manager.log"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 确保日志目录存在
mkdir -p "$(dirname "$LOG_FILE")"

# 检查参数
if [[ -z "$1" ]]; then
    echo -e "${RED}❌ 请提供新的 API Key${NC}"
    echo ""
    echo "用法："
    echo "  $0 <新的 API Key>"
    echo ""
    echo "示例："
    echo "  $0 sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    echo ""
    echo "获取 API Key:"
    echo "  1. 访问 https://iflow.cn/?open=setting"
    echo "  2. 登录账号"
    echo "  3. 生成新的 API Key"
    echo "  4. 复制并运行此脚本"
    exit 1
fi

NEW_KEY="$1"

# 验证 Key 格式
if [[ ! "$NEW_KEY" =~ ^sk-[a-zA-Z0-9]{32}$ ]]; then
    echo -e "${RED}❌ API Key 格式不正确${NC}"
    echo "预期格式：sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx (sk- 后跟 32 位字母数字)"
    exit 1
fi

echo -e "${YELLOW}🔄 开始更新 iFlow API Key...${NC}"
echo ""

# 1. 更新 ~/.iflow/settings.json
if [[ -f "$IFLOW_SETTINGS" ]]; then
    log "更新 $IFLOW_SETTINGS"
    python3 << PYTHON
import json

with open('$IFLOW_SETTINGS', 'r') as f:
    config = json.load(f)

config['apiKey'] = '$NEW_KEY'
config['api_key'] = '$NEW_KEY'

with open('$IFLOW_SETTINGS', 'w') as f:
    json.dump(config, f, indent=2)

print("✅ 已更新")
PYTHON
else
    echo -e "${YELLOW}⚠️ $IFLOW_SETTINGS 不存在，创建中...${NC}"
    cat > "$IFLOW_SETTINGS" << EOF
{
  "apiKey": "$NEW_KEY",
  "api_key": "$NEW_KEY",
  "baseUrl": "https://apis.iflow.cn/v1",
  "base_url": "https://apis.iflow.cn/v1",
  "modelName": "qwen3-max",
  "model_name": "qwen3-max"
}
EOF
    log "✅ 已创建 $IFLOW_SETTINGS"
fi

# 2. 更新 ~/.openclaw/workspace/scripts/iflow.sh
if [[ -f "$IFLOW_SCRIPT" ]]; then
    log "更新 $IFLOW_SCRIPT"
    sed -i.bak "s/IFLOW_API_KEY=\"[^\"]*\"/IFLOW_API_KEY=\"$NEW_KEY\"/" "$IFLOW_SCRIPT"
    rm -f "${IFLOW_SCRIPT}.bak"
    log "✅ 已更新 iflow.sh"
else
    echo -e "${RED}❌ $IFLOW_SCRIPT 不存在${NC}"
    exit 1
fi

# 3. 更新 ~/.openclaw/openclaw.json
if [[ -f "$OPENCLAW_CONFIG" ]]; then
    log "更新 $OPENCLAW_CONFIG"
    python3 << PYTHON
import json
import re

with open('$OPENCLAW_CONFIG', 'r') as f:
    config = json.load(f)

# 更新 iflow provider 的 apiKey
if 'models' in config and 'providers' in config['models']:
    if 'iflow' in config['models']['providers']:
        config['models']['providers']['iflow']['apiKey'] = '$NEW_KEY'

with open('$OPENCLAW_CONFIG', 'w') as f:
    json.dump(config, f, indent=2)

print("✅ 已更新")
PYTHON
    log "✅ 已更新 openclaw.json"
else
    echo -e "${YELLOW}⚠️ $OPENCLAW_CONFIG 不存在，跳过${NC}"
fi

# 4. 更新状态文件
cat > "$STATE_FILE" << EOF
{
  "configDate": "$(date -Iseconds)",
  "expiryDate": "$(date -v+7d -Iseconds 2>/dev/null || date -d '+7 days' -Iseconds 2>/dev/null)",
  "notified": false,
  "lastUpdated": "$(date -Iseconds)"
}
EOF
log "✅ 已更新状态文件"

# 5. 清理 HEARTBEAT.md 中的过期提醒
if [[ -f "$HOME/.openclaw/workspace/HEARTBEAT.md" ]]; then
    # 移除旧的提醒部分
    python3 << PYTHON
with open('$HOME/.openclaw/workspace/HEARTBEAT.md', 'r') as f:
    content = f.read()

# 找到并移除 iFlow API Key 紧急提醒部分
import re
pattern = r'\n---\n## 🚨 iFlow API Key 紧急提醒.*?(?=\n---\n|\Z)'
content = re.sub(pattern, '', content, flags=re.DOTALL)

with open('$HOME/.openclaw/workspace/HEARTBEAT.md', 'w') as f:
    f.write(content)

print("✅ 已清理过期提醒")
PYTHON
fi

echo ""
echo -e "${GREEN}✅ API Key 更新完成！${NC}"
echo ""
echo "📅 新 Key 到期时间：$(date -v+7d '+%Y-%m-%d' 2>/dev/null || date -d '+7 days' '+%Y-%m-%d')"
echo ""
echo "🧪 测试连接："
echo "   ~/.openclaw/workspace/scripts/iflow.sh -p 'test'"
echo ""
echo "📋 下次检查："
echo "   ~/.openclaw/workspace/scripts/iflow-key-manager.sh status"
