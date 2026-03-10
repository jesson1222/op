# Learnings Log

记录纠正、知识差距和最佳实践。

## 格式说明

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
一句话描述学到的内容

### Details
完整上下文：发生了什么、什么是错的、什么是正确的

### Suggested Action
具体的修复或改进建议

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-20250110-001 (如果相关)
- Pattern-Key: simplify.dead_code | harden.input_validation (可选)
- Recurrence-Count: 1 (可选)
- First-Seen: 2025-01-15 (可选)
- Last-Seen: 2025-01-15 (可选)

---
```

## 当前 Learnings

## [LRN-20260310-001] skill-configuration

**Logged**: 2026-03-10T08:56:00+08:00
**Priority**: medium
**Status**: resolved
**Area**: config

### Resolution
- **Resolved**: 2026-03-10T08:56:00+08:00
- **Commit**: 已创建完整的配置脚本和文档
- **Notes**: 包含自动重试、使用指南、检查脚本

### Summary
自学习技能需要配置自动重试机制和完整的使用流程

### Details
用户要求配置自学习技能的使用，发现：
1. `.learnings/` 目录已存在但缺少自动化配置
2. 没有自动重试机制来处理技能加载失败
3. 缺少快速检查脚本和使用指南

### Suggested Action
✅ 已完成：
1. 创建 `setup-auto-retry.sh` 配置脚本
2. 创建 `auto-retry-config.json` 配置文件
3. 创建 `USAGE.md` 使用指南
4. 创建 `scripts/check-learnings.sh` 检查脚本
5. 更新 `HEARTBEAT.md` 添加自学习检查

### Metadata
- Source: user_feedback
- Related Files: ~/.openclaw/workspace/skills/self-improving-agent/
- Tags: skill, configuration, self-improvement
- Pattern-Key: skill.auto-retry-setup

---

---
