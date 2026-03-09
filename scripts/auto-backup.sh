#!/bin/bash
# OpenClaw 自动备份脚本
# 每天凌晨 2 点自动备份到 GitHub

set -e

WORKSPACE="/Users/jesson/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/backup.log"

# 创建日志目录
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "========== 开始备份 =========="

cd "$WORKSPACE"

# 检查 Git 状态
if ! git status >/dev/null 2>&1; then
    log "❌ 错误：不是 Git 仓库"
    exit 1
fi

# 添加所有变更
log "📦 添加文件..."
git add -A

# 检查是否有变更
if git diff --staged --quiet; then
    log "✅ 无变更，跳过备份"
    exit 0
fi

# 提交变更
log "💾 提交变更..."
git commit -m "chore: 自动备份 $(date '+%Y-%m-%d %H:%M')"

# 推送到 GitHub
log "🚀 推送到 GitHub..."
if git push origin master; then
    log "✅ 备份成功！"
else
    log "❌ 推送失败，尝试重新拉取..."
    git pull --rebase origin master
    git push origin master
    log "✅ 备份完成（rebase 后）"
fi

log "========== 备份完成 =========="
