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

---

## [LRN-20260310-002] xiaohongshu-auto-publish

**Logged**: 2026-03-10T12:45:00+08:00
**Priority**: high
**Status**: resolved
**Area**: infra

### Summary
小红书自动发布流程已验证成功（2 篇笔记）

### Details
成功发布 2 篇专业内容：
1. ARRI 35 解析报告 - 🎬 ARRI 35 | 电影机新标杆
2. 三点布光法教程 - 💡 三点布光法 | 电影感秘诀

### Key Learnings
1. **Cookie 管理**：需要复制到容器内 `/app/cookies.json`
2. **图片上传**：单张图片最稳定，多张易超时
3. **图片质量**：Unsplash 图片质量高，适合封面
4. **Docker 稳定性**：需要定期检查容器状态
5. **超时设置**：`MCPORTER_CALL_TIMEOUT=120000`

### Suggested Action
建立自动发布流程：
1. 检查 Docker 容器状态
2. 验证 Cookie 有效性
3. 准备高质量封面图（Unsplash/Pexels）
4. 单图发布最稳定
5. 发布后记录 PostID

### Metadata
- Source: conversation
- Related Files: ~/.agent-reach/xiaohongshu-cookies.json
- Tags: xiaohongshu, auto-publish, docker
- Pattern-Key: xiaohongshu.stable-publish

---

## [LRN-20260310-003] xiaohongshu-autostart

**Logged**: 2026-03-10T12:42:00+08:00
**Priority**: high
**Status**: resolved
**Area**: infra

### Summary
配置 macOS 开机自动启动小红书发布系统

### Details
使用 macOS launchd 实现开机自启动：
1. 创建 LaunchAgent plist 文件
2. 配置延迟启动（等待 Docker）
3. 自动复制 Cookie 文件
4. 记录启动日志

### Configuration
- **服务名**: com.xiaohongshu.autostart
- **配置文件**: ~/Library/LaunchAgents/com.xiaohongshu.autostart.plist
- **启动延迟**: 15 秒（等待系统完全启动）
- **日志**: /tmp/xiaohongshu-autostart.log

### Verification
```bash
launchctl list | grep xiaohongshu
# 输出：7101	0	com.xiaohongshu.autostart
```

### Metadata
- Source: user_request
- Related Files: ~/Library/LaunchAgents/com.xiaohongshu.autostart.plist
- Tags: xiaohongshu, autostart, launchd, docker
- Pattern-Key: xiaohongshu.autostart-setup

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
