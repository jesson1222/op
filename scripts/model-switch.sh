#!/bin/bash
# OpenClaw 模型快速切换脚本
# 用法：model-switch.sh <provider|model>

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 配置文件
CONFIG_FILE="$HOME/.openclaw/openclaw.json"
BACKUP_DIR="$HOME/.openclaw/backups/models"

# 确保备份目录存在
mkdir -p "$BACKUP_DIR"

# 日志函数
log() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✓${NC} $1"
}

error() {
    echo -e "${RED}✗${NC} $1"
}

info() {
    echo -e "${CYAN}ℹ${NC} $1"
}

# 显示帮助
show_help() {
    echo -e "${CYAN}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║   OpenClaw 模型快速切换工具                            ║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "用法："
    echo "  $0 <provider|model>  - 切换到指定模型或提供商"
    echo "  $0 list             - 列出所有可用模型"
    echo "  $0 status           - 显示当前模型"
    echo "  $0 help             - 显示帮助信息"
    echo ""
    echo "提供商快捷方式："
    echo "  bailian    - 阿里云百炼 (qwen3.5-plus)"
    echo "  iflow      - iFlow 心流 (qwen3-max, 免费)"
    echo "  ollama     - 本地 Ollama (qwen3.5:35b)"
    echo "  qwen       - Qwen Portal (coder-model)"
    echo "  minimax    - MiniMax Portal (M2.5)"
    echo ""
    echo "示例："
    echo "  $0 bailian              # 切换到百炼"
    echo "  $0 iflow                # 切换到 iFlow 免费模型"
    echo "  $0 bailian/qwen3-max    # 切换到指定模型"
    echo "  $0 list                 # 查看所有模型"
    echo ""
}

# 列出所有可用模型
list_models() {
    echo -e "${CYAN}════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  可用模型列表${NC}"
    echo -e "${CYAN}════════════════════════════════════════════════════════${NC}"
    echo ""
    
    echo -e "${YELLOW}📦 阿里云百炼 (bailian)${NC}"
    echo "   bailian/qwen3.5-plus      ⭐ 均衡性能（推荐）"
    echo "   bailian/qwen3-max         最强推理"
    echo "   bailian/qwen-coder        代码专用"
    echo "   bailian/glm-5             长文本"
    echo "   bailian/kimi              超长文档"
    echo "   bailian/minimax           多模态"
    echo ""
    
    echo -e "${YELLOW}🆓 iFlow 心流 (免费)${NC}"
    echo "   iflow-qwen-max            ⭐ 免费最强（推荐）"
    echo "   iflow-qwen-coder          代码专用"
    echo "   iflow-kimi-k2             长文本"
    echo "   iflow-deepseek-v3         性价比"
    echo "   iflow-deepseek-r1         推理/数学"
    echo "   iflow-qwen-235b           图像理解"
    echo ""
    
    echo -e "${YELLOW}💻 本地 Ollama${NC}"
    echo "   ollama/qwen3.5            本地运行"
    echo "   ollama/llama3.1           轻量级"
    echo ""
    
    echo -e "${YELLOW}🌐 Qwen Portal${NC}"
    echo "   qwen                      代码模型"
    echo "   qwen-vl                   视觉模型"
    echo ""
    
    echo -e "${YELLOW}⚡ MiniMax Portal${NC}"
    echo "   minimax-m2.5              通用"
    echo "   minimax-m2.5-highspeed    高速"
    echo "   minimax-m2.5-lightning    极速"
    echo ""
}

# 显示当前模型
show_status() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        error "配置文件不存在：$CONFIG_FILE"
        exit 1
    fi
    
    current_model=$(python3 -c "
import json
with open('$CONFIG_FILE', 'r') as f:
    config = json.load(f)
print(config.get('agents', {}).get('defaults', {}).get('model', {}).get('primary', 'unknown'))
" 2>/dev/null)
    
    echo -e "${CYAN}════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  当前模型配置${NC}"
    echo -e "${CYAN}════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "  当前模型：${GREEN}$current_model${NC}"
    echo ""
    
    # 显示模型信息
    case "$current_model" in
        *bailian*)
            echo -e "  提供商：${YELLOW}阿里云百炼${NC}"
            echo -e "  状态：${GREEN}● 在线${NC}"
            ;;
        *iflow*)
            echo -e "  提供商：${YELLOW}iFlow 心流${NC}"
            echo -e "  状态：${GREEN}● 在线 (OAuth)${NC}"
            echo -e "  费用：${GREEN}免费${NC}"
            ;;
        *ollama*)
            echo -e "  提供商：${YELLOW}本地 Ollama${NC}"
            echo -e "  状态：${GREEN}● 本地运行${NC}"
            ;;
        *)
            echo -e "  提供商：${YELLOW}未知${NC}"
            ;;
    esac
    echo ""
}

# 切换模型
switch_model() {
    local target="$1"
    local model=""
    
    # 解析目标
    case "$target" in
        bailian)
            model="bailian/qwen3.5-plus"
            ;;
        iflow)
            model="iflow/qwen3-max"
            ;;
        ollama)
            model="ollama/qwen3.5:35b"
            ;;
        qwen)
            model="qwen-portal/coder-model"
            ;;
        minimax)
            model="minimax-portal/MiniMax-M2.5"
            ;;
        */*)
            model="$target"
            ;;
        *)
            error "未知的模型或提供商：$target"
            echo ""
            echo "使用 '$0 list' 查看所有可用模型"
            exit 1
            ;;
    esac
    
    # 备份当前配置
    local backup_file="$BACKUP_DIR/openclaw-$(date +%Y%m%d-%H%M%S).json"
    cp "$CONFIG_FILE" "$backup_file"
    log "已备份配置文件：$backup_file"
    
    # 更新配置
    log "切换到模型：$model"
    
    python3 << PYTHON
import json
import sys

config_file = "$CONFIG_FILE"
new_model = "$model"

try:
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    # 更新默认模型
    if 'agents' not in config:
        config['agents'] = {}
    if 'defaults' not in config['agents']:
        config['agents']['defaults'] = {}
    if 'model' not in config['agents']['defaults']:
        config['agents']['defaults']['model'] = {}
    
    config['agents']['defaults']['model']['primary'] = new_model
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✓ 配置已更新")
except Exception as e:
    print(f"✗ 错误：{e}", file=sys.stderr)
    sys.exit(1)
PYTHON
    
    if [[ $? -eq 0 ]]; then
        success "模型已切换到：$model"
        echo ""
        info "下次对话将使用新模型"
        echo ""
        
        # 显示模型信息
        case "$model" in
            *iflow*)
                echo -e "${GREEN}💰 使用免费模型，预计每月节省 ¥600-1200${NC}"
                ;;
            *bailian/qwen3-max*)
                echo -e "${YELLOW}⚡ 使用高性能模型，适合复杂任务${NC}"
                ;;
            *ollama*)
                echo -e "${CYAN}🔒 使用本地模型，数据隐私保护${NC}"
                ;;
        esac
    else
        error "切换失败"
        exit 1
    fi
}

# 主程序
case "${1:-help}" in
    list)
        list_models
        ;;
    status)
        show_status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        switch_model "$1"
        ;;
esac
