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
