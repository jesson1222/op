#!/bin/bash
# 自学习技能自动重试安装配置脚本
# 用于配置 OpenClaw 在技能加载失败时自动重试

set -e

WORKSPACE="$HOME/.openclaw/workspace"
SKILL_DIR="$WORKSPACE/skills/self-improving-agent"

echo "🔧 配置自学习技能自动重试..."

# 1. 确保 .learnings 目录存在
mkdir -p "$WORKSPACE/.learnings"

# 2. 创建必要的日志文件（如果不存在）
for file in LEARNINGS.md ERRORS.md FEATURE_REQUESTS.md; do
    if [ ! -f "$WORKSPACE/.learnings/$file" ]; then
        echo "创建 $file..."
        case $file in
            LEARNINGS.md)
                cat > "$WORKSPACE/.learnings/$file" << 'EOF'
# Learnings Log

记录纠正、知识差距和最佳实践。

## 当前 Learnings

暂无记录。

---
EOF
                ;;
            ERRORS.md)
                cat > "$WORKSPACE/.learnings/$file" << 'EOF'
# Errors Log

记录命令失败和异常。

## 当前 Errors

暂无记录。

---
EOF
                ;;
            FEATURE_REQUESTS.md)
                cat > "$WORKSPACE/.learnings/$file" << 'EOF'
# Feature Requests Log

记录用户请求的新功能。

## 当前 Feature Requests

暂无记录。

---
EOF
                ;;
        esac
    fi
done

# 3. 创建自动重试配置文件
cat > "$SKILL_DIR/auto-retry-config.json" << 'EOF'
{
  "enabled": true,
  "maxRetries": 3,
  "retryDelayMs": 1000,
  "backoffMultiplier": 2,
  "onFailure": {
    "log": true,
    "notify": true,
    "fallback": "graceful-degrade"
  },
  "triggers": [
    "skill-load-failure",
    "memory-search-failure",
    "file-write-failure"
  ]
}
EOF

# 4. 更新 HEARTBEAT.md 添加学习检查
if ! grep -q "自学习检查" "$WORKSPACE/HEARTBEAT.md" 2>/dev/null; then
    cat >> "$WORKSPACE/HEARTBEAT.md" << 'EOF'

---

## 🧠 自学习检查

每次 heartbeat 时检查：

- [ ] 是否有新的错误需要记录到 `.learnings/ERRORS.md`
- [ ] 是否有用户纠正需要记录到 `.learnings/LEARNINGS.md`
- [ ] 是否有待解决的 learning 需要处理
- [ ] 是否有可以提升到 MEMORY.md 的学习内容

**检查命令：**
```bash
# 查看待处理的 learnings
grep -h "Status\*\*: pending" ~/.openclaw/workspace/.learnings/*.md | wc -l

# 查看高优先级的 errors
grep -B5 "Priority\*\*: high" ~/.openclaw/workspace/.learnings/ERRORS.md
```
EOF
fi

# 5. 创建快速检查脚本
cat > "$SKILL_DIR/scripts/check-learnings.sh" << 'EOF'
#!/bin/bash
# 快速检查 learnings 状态

WORKSPACE="$HOME/.openclaw/workspace"
LEARNINGS_DIR="$WORKSPACE/.learnings"

echo "📊 Learnings 状态检查"
echo "===================="
echo ""

# 统计
echo "📈 统计:"
echo "  - LEARNINGS.md: $(grep -c "^## \[" "$LEARNINGS_DIR/LEARNINGS.md" 2>/dev/null || echo 0) 条"
echo "  - ERRORS.md: $(grep -c "^## \[" "$LEARNINGS_DIR/ERRORS.md" 2>/dev/null || echo 0) 条"
echo "  - FEATURE_REQUESTS.md: $(grep -c "^## \[" "$LEARNINGS_DIR/FEATURE_REQUESTS.md" 2>/dev/null || echo 0) 条"
echo ""

# 待处理项
echo "⏳ 待处理项:"
PENDING=$(grep -h "Status\*\*: pending" "$LEARNINGS_DIR"/*.md 2>/dev/null | wc -l)
echo "  - 待处理：$PENDING"
echo ""

# 高优先级
echo "🔴 高优先级:"
grep -B2 "Priority\*\*: high" "$LEARNINGS_DIR"/*.md 2>/dev/null | grep "^## \[" | head -5 || echo "  无"
echo ""

# 最近 5 条
echo "📝 最近记录:"
grep "^## \[" "$LEARNINGS_DIR"/*.md 2>/dev/null | tail -5 || echo "  无"
EOF

chmod +x "$SKILL_DIR/scripts/check-learnings.sh"

# 6. 添加到 git（如果是 git 仓库）
if [ -d "$WORKSPACE/.git" ]; then
    cd "$WORKSPACE"
    git add .learnings/ skills/self-improving-agent/auto-retry-config.json 2>/dev/null || true
    echo "✅ 已添加到 git 暂存区"
fi

echo ""
echo "✅ 自动重试配置完成！"
echo ""
echo "使用方式："
echo "  1. 检查 learnings 状态：./skills/self-improving-agent/scripts/check-learnings.sh"
echo "  2. 手动记录学习：编辑 .learnings/LEARNINGS.md"
echo "  3. 手动记录错误：编辑 .learnings/ERRORS.md"
echo ""
echo "配置详情："
echo "  - 最大重试次数：3 次"
echo "  - 重试延迟：1000ms (指数退避)"
echo "  - 自动日志：启用"
echo "  - 失败通知：启用"
