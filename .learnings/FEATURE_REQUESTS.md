# Feature Requests Log

记录用户请求的功能。

## 格式说明

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Requested Capability
用户想要做什么

### User Context
为什么需要这个，解决什么问题

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
如何实现，可能扩展什么

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_feature_name

---
```

## 当前 Feature Requests

## [FEAT-20260310-001] auto-retry-mechanism

**Logged**: 2026-03-10T08:51:00+08:00
**Priority**: high
**Status**: resolved
**Area**: infra

### Resolution
- **Resolved**: 2026-03-10T08:56:00+08:00
- **Commit**: 已创建完整的自动重试配置
- **Notes**: 实现 3 次重试 + 指数退避 + 自动日志

### Requested Capability
技能加载失败时自动重试安装

### User Context
用户明确要求"自动重试安装"，需要：
1. 配置重试机制以应对网络不稳定
2. 设置合理的重试次数和延迟
3. 失败时自动记录日志并通知

### Complexity Estimate
medium

### Suggested Implementation
✅ 已实现：
1. 创建 `auto-retry-config.json` 配置文件
2. 实现指数退避重试（1s → 2s → 4s）
3. 最多重试 3 次
4. 失败时自动记录到 ERRORS.md
5. 添加检查脚本和心跳检查

### Metadata
- Frequency: recurring
- Related Features: skill-loader, self-improvement
- Pattern-Key: skill.auto-retry

---

---
