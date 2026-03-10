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

---

## [LRN-20260310-004] openclaw-gateway-optimization

**Logged**: 2026-03-10T15:08:00+08:00
**Priority**: medium
**Status**: resolved
**Area**: infra

### Summary
优化 OpenClaw Gateway 开机自启动配置

### Details
执行 `openclaw gateway install --force` 优化配置：
1. 移除嵌入的 token（安全提升）
2. 更新 PATH 环境变量（包含所有包管理器）
3. 更新到最新版本 (2026.3.8)
4. 添加 ThrottleInterval 和 Umask 配置

### Improvements
**优化前**:
- ❌ Token 嵌入在配置文件中
- ❌ PATH 缺少 nvm, pnpm, fnm 等
- ❌ 版本：2026.2.9

**优化后**:
- ✅ Token 动态管理
- ✅ 完整 PATH（包含所有包管理器路径）
- ✅ 版本：2026.3.8
- ✅ 添加 ThrottleInterval: 1
- ✅ 添加 Umask: 63

### New PATH
```
/Users/jesson/.nvm:/Users/jesson/.local/bin:/Users/jesson/.npm-global/bin:/Users/jesson/bin:/Users/jesson/.volta/bin:/Users/jesson/.asdf/shims:/Users/jesson/.bun/bin:/Users/jesson/Library/Application Support/fnm/aliases/default/bin:/Users/jesson/.fnm/aliases/default/bin:/Users/jesson/Library/pnpm:/Users/jesson/.local/share/pnpm:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin
```

### Metadata
- Source: user_request
- Related Files: ~/Library/LaunchAgents/ai.openclaw.gateway.plist
- Tags: openclaw, gateway, optimization, launchd
- Pattern-Key: openclaw.gateway-optimization

---

## [LRN-20260310-005] no-sleep-configuration

**Logged**: 2026-03-10T15:38:00+08:00
**Priority**: high
**Status**: resolved
**Area**: infra

### Summary
配置 macOS 不休眠，确保服务持续运行

### Details
使用 caffeinate + launchd 实现永久不休眠：
1. 创建 LaunchAgent 配置文件
2. 使用 caffeinate 防止系统休眠
3. 配置 KeepAlive 确保服务持续运行
4. 记录运行日志

### Configuration
- **服务名**: com.no-sleep.autostart
- **配置文件**: ~/Library/LaunchAgents/com.no-sleep.autostart.plist
- **caffeinate 参数**: -d -i -m -s
- **日志**: /tmp/caffeinate.log

### Verification
```bash
launchctl list | grep no-sleep
# 输出：30777	0	com.no-sleep.autostart
```

### Metadata
- Source: user_request
- Related Files: ~/Library/LaunchAgents/com.no-sleep.autostart.plist
- Tags: no-sleep, caffeinate, launchd, pmset
- Pattern-Key: macos.no-sleep-setup

---

## [LRN-20260310-006] red-com-content-research

**Logged**: 2026-03-10T21:53:00+08:00
**Priority**: medium
**Status**: resolved
**Area**: content

### Summary
学习 RED 数字电影摄影机官网，准备专业内容

### Details
研究 www.red.com 产品线和技术规格：
1. V-RAPTOR 8K VV - 旗舰型号
2. KOMODO 6K - 入门专业款
3. MONSTRO 8K - 经典旗舰
4. REDCODE RAW 技术
5. IPP2 色彩科学

### Content Published
- 🎬 RED KOMODO | 6K 电影机神器 (第 3 篇)

### Key Insights
1. KOMODO 6K 性价比最高 ($6K vs ARRI $50K+)
2. 重量优势明显 (1.2kg vs 3.5kg)
3. 6K 分辨率是主要卖点
4. 适合独立电影人

### Metadata
- Source: user_request
- Related Files: ~/.agent-reach/red-com-learning.md
- Tags: red, komodo, cinema-camera, content-research
- Pattern-Key: red.product-research

---

## [LRN-20260310-007] angenieux-lenses-organization

**Logged**: 2026-03-10T23:02:00+08:00
**Priority**: high
**Status**: resolved
**Area**: content

### Summary
整理安琴 (Angenieux) 所有镜头产品，输出 Excel 和 HTML 格式

### Details
按 Cooke 镜头分类方式整理安琴产品线：
1. EZ 系列 (5 款) - 电子控制变焦
2. Type 系列 (3 款) - 经典电影镜头
3. 经典系列 (2 款) - 历史收藏级
总计 10 款镜头，按发布年份排序 (1975-2020)

### Deliverables
- angenieux-lenses.csv (1.3KB) - Excel 格式
- angenieux-lenses.html (19KB) - 精美网页
- angenieux-complete-lenses.json - 原始数据
- angenieux-completion-report.md - 完成报告

### Design Features
- 响应式布局
- 渐变配色 (紫色系)
- 表格悬停效果
- 标签系统 (卡口/传感器/年份/特点)
- 分类展示

### Metadata
- Source: user_request
- Related Files: ~/.agent-reach/angenieux-lenses.html
- Tags: angenieux, lenses, organization, excel, html
- Pattern-Key: angenieux.product-organization

### Details
研究 www.red.com 产品线和技术规格：
1. V-RAPTOR 8K VV - 旗舰型号
2. KOMODO 6K - 入门专业款
3. MONSTRO 8K - 经典旗舰
4. REDCODE RAW 技术
5. IPP2 色彩科学

### Content Published
- 🎬 RED KOMODO | 6K 电影机神器 (第 3 篇)

### Key Insights
1. KOMODO 6K 性价比最高 ($6K vs ARRI $50K+)
2. 重量优势明显 (1.2kg vs 3.5kg)
3. 适合独立电影人和小团队
4. 6K 分辨率是主要卖点

### Metadata
- Source: user_request
- Related Files: ~/.agent-reach/red-com-learning.md
- Tags: red, komodo, cinema-camera, content-research
- Pattern-Key: red.product-research

### Details
使用 caffeinate + launchd 实现永久不休眠：
1. 创建 LaunchAgent 配置文件
2. 使用 caffeinate 防止系统休眠
3. 配置 KeepAlive 确保服务持续运行
4. 记录运行日志

### Configuration
- **服务名**: com.no-sleep.autostart
- **配置文件**: ~/Library/LaunchAgents/com.no-sleep.autostart.plist
- **caffeinate 参数**: -d -i -m -s
- **日志**: /tmp/caffeinate.log

### pmset Settings
```
sleep: 0 (不休眠)
displaysleep: 0 (显示器不休眠)
disksleep: 10 (硬盘 10 分钟后休眠)
```

### Verification
```bash
launchctl list | grep no-sleep
# 输出：30777	0	com.no-sleep.autostart
```

### Metadata
- Source: user_request
- Related Files: ~/Library/LaunchAgents/com.no-sleep.autostart.plist
- Tags: no-sleep, caffeinate, launchd, pmset
- Pattern-Key: macos.no-sleep-setup

### Details
执行 `openclaw gateway install --force` 优化配置：
1. 移除嵌入的 token（安全提升）
2. 更新 PATH 环境变量（包含所有包管理器）
3. 更新到最新版本 (2026.3.8)
4. 添加 ThrottleInterval 和 Umask 配置

### Improvements
**优化前**:
- ❌ Token 嵌入在配置文件中
- ❌ PATH 缺少 nvm, pnpm, fnm 等
- ❌ 版本：2026.2.9

**优化后**:
- ✅ Token 动态管理
- ✅ 完整 PATH（包含所有包管理器路径）
- ✅ 版本：2026.3.8
- ✅ 添加 ThrottleInterval: 1
- ✅ 添加 Umask: 63

### New PATH
```
/Users/jesson/.nvm:/Users/jesson/.local/bin:/Users/jesson/.npm-global/bin:/Users/jesson/bin:/Users/jesson/.volta/bin:/Users/jesson/.asdf/shims:/Users/jesson/.bun/bin:/Users/jesson/Library/Application Support/fnm/aliases/default/bin:/Users/jesson/.fnm/aliases/default/bin:/Users/jesson/Library/pnpm:/Users/jesson/.local/share/pnpm:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin
```

### Metadata
- Source: user_request
- Related Files: ~/Library/LaunchAgents/ai.openclaw.gateway.plist
- Tags: openclaw, gateway, optimization, launchd
- Pattern-Key: openclaw.gateway-optimization

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
