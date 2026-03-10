# 自学习技能使用指南

帮助你使用 OpenClaw 的自学习功能，实现持续改进。

## 📁 目录结构

```
~/.openclaw/workspace/
├── .learnings/              # 学习日志目录
│   ├── LEARNINGS.md         # 纠正、知识差距、最佳实践
│   ├── ERRORS.md            # 错误和失败记录
│   └── FEATURE_REQUESTS.md  # 功能请求
├── skills/self-improving-agent/
│   ├── SKILL.md             # 技能定义
│   ├── setup-auto-retry.sh  # 自动重试配置脚本
│   ├── auto-retry-config.json # 自动重试配置
│   └── scripts/
│       └── check-learnings.sh # 状态检查脚本
└── HEARTBEAT.md             # 心跳检查（包含自学习检查）
```

## 🚀 快速开始

### 1. 运行配置脚本（一次性）

```bash
cd ~/.openclaw/workspace
./skills/self-improving-agent/setup-auto-retry.sh
```

### 2. 检查当前状态

```bash
./skills/self-improving-agent/scripts/check-learnings.sh
```

## 📝 何时记录学习

### 记录到 LEARNINGS.md

当发生以下情况时：

- ✅ **用户纠正你**："不对，应该是..."、"其实..."
- ✅ **发现知识差距**：学到了之前不知道的东西
- ✅ **找到更好的方法**：发现了更优的解决方案
- ✅ **项目约定**：发现了未文档化的项目规范

**示例：**
```markdown
## [LRN-20260310-001] correction

**Logged**: 2026-03-10T08:51:00+08:00
**Priority**: medium
**Status**: pending
**Area**: config

### Summary
用户纠正了模型配置的理解

### Details
用户指出应该使用 bailian/qwen3.5-plus 作为默认模型，
而不是 ollama 本地模型。

### Suggested Action
更新 openclaw.json 中的默认模型配置

### Metadata
- Source: user_feedback
- Related Files: ~/.openclaw/openclaw.json
- Tags: model, configuration

---
```

### 记录到 ERRORS.md

当发生以下情况时：

- ❌ **命令失败**：非零退出码
- ❌ **API 错误**：外部服务调用失败
- ❌ **文件操作失败**：读写权限问题
- ❌ **超时或连接失败**

**示例：**
```markdown
## [ERR-20260310-001] git-push

**Logged**: 2026-03-10T09:00:00+08:00
**Priority**: high
**Status**: pending
**Area**: infra

### Summary
Git push 失败，需要认证

### Error
```
fatal: Could not read from remote repository.
Please make sure you have the correct access rights
```

### Context
- 命令：`git push origin main`
- 环境：macOS, zsh
- Git 版本：2.39.0

### Suggested Fix
配置 SSH 密钥或 Git credential

### Metadata
- Reproducible: yes
- Related Files: ~/.ssh/id_ed25519

---
```

### 记录到 FEATURE_REQUESTS.md

当用户请求新功能时：

- 💡 **能力扩展**："你能不能也..."、"我希望你可以..."
- 💡 **工作流优化**："如果自动...就好了"
- 💡 **集成需求**："可以和 XXX 连接吗"

**示例：**
```markdown
## [FEAT-20260310-001] auto-retry

**Logged**: 2026-03-10T08:51:00+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Requested Capability
技能加载失败时自动重试

### User Context
网络不稳定时技能加载会失败，需要自动重试机制

### Complexity Estimate
medium

### Suggested Implementation
1. 添加重试配置文件 auto-retry-config.json
2. 在技能加载前检查配置
3. 实现指数退避重试逻辑

### Metadata
- Frequency: recurring
- Related Features: skill-loader

---
```

## 🔄 自动重试配置

### 配置文件位置

`~/.openclaw/workspace/skills/self-improving-agent/auto-retry-config.json`

### 配置项说明

```json
{
  "enabled": true,              // 是否启用自动重试
  "maxRetries": 3,              // 最大重试次数
  "retryDelayMs": 1000,         // 初始重试延迟（毫秒）
  "backoffMultiplier": 2,       // 指数退避倍数
  "onFailure": {
    "log": true,                // 失败时记录日志
    "notify": true,             // 失败时通知用户
    "fallback": "graceful-degrade" // 降级策略
  },
  "triggers": [                 // 触发重试的场景
    "skill-load-failure",
    "memory-search-failure",
    "file-write-failure"
  ]
}
```

### 修改配置

编辑配置文件后，重启 OpenClaw 或重新加载技能：

```bash
# 查看当前配置
cat ~/.openclaw/workspace/skills/self-improving-agent/auto-retry-config.json

# 编辑配置
nano ~/.openclaw/workspace/skills/self-improving-agent/auto-retry-config.json
```

## 🔍 定期检查

### Heartbeat 检查

HEARTBEAT.md 已配置自学习检查，每次心跳时会自动：

1. 检查是否有新错误需要记录
2. 检查是否有用户纠正需要记录
3. 检查是否有待处理的 learning
4. 检查是否有可以提升的学习内容

### 手动检查

```bash
# 查看待处理项数量
grep -h "Status\*\*: pending" ~/.openclaw/workspace/.learnings/*.md | wc -l

# 查看高优先级项
grep -B5 "Priority\*\*: high" ~/.openclaw/workspace/.learnings/*.md

# 查找特定区域的 learnings
grep -l "Area\*\*: backend" ~/.openclaw/workspace/.learnings/*.md
```

## 📤 提升学习内容

当学习内容具有广泛适用性时，应该提升到项目记忆文件中：

### 提升目标

| 学习类型 | 提升到 | 示例 |
|---------|--------|------|
| 行为模式 | `SOUL.md` | "简洁回复，避免免责声明" |
| 工作流改进 | `AGENTS.md` | "长时间任务使用子代理" |
| 工具技巧 | `TOOLS.md` | "Git push 需要先配置认证" |
| 长期记忆 | `MEMORY.md` | 重要决策、上下文 |

### 提升流程

1. **提炼**：将学习简化为简洁的规则或事实
2. **添加**：添加到目标文件的适当部分
3. **更新原记录**：
   - 更改状态为 `promoted`
   - 添加 `**Promoted**: 文件名`

## 🛠️ 实用命令

```bash
# 快速状态检查
./skills/self-improving-agent/scripts/check-learnings.sh

# 添加新的 learning
echo "## [LRN-$(date +%Y%m%d)-001] category" >> .learnings/LEARNINGS.md

# 搜索相关 learning
grep -r "关键词" .learnings/

# 统计本月 learning 数量
grep "^## \[LRN-$(date +%Y%m)-" .learnings/LEARNINGS.md | wc -l
```

## 🎯 最佳实践

1. **立即记录** - 上下文最新鲜
2. **具体明确** - 方便未来的代理快速理解
3. **包含复现步骤** - 特别是错误
4. **链接相关文件** - 让修复更容易
5. **建议具体修复** - 不只是"调查"
6. **使用一致的分类** - 便于过滤
7. **积极提升** - 有疑问就添加到项目文件
8. **定期审查** - 过时的 learnings 会失去价值

## 📊 优先级指南

| 优先级 | 使用场景 |
|--------|---------|
| `critical` | 阻塞核心功能、数据丢失风险、安全问题 |
| `high` | 重大影响、影响常见工作流、重复问题 |
| `medium` | 中等影响、存在变通方法 |
| `low` | 轻微不便、边缘情况、锦上添花 |

## 🔗 相关技能

- [`skill-self-improvement`](../skill-self-improvement/SKILL.md) - 技能自身的创建和改善
- [`memory-hygiene`](../memory-hygiene/SKILL.md) - 记忆清理和优化
- [`proactive-agent`](../proactive-agent/SKILL.md) - 主动式代理模式

---

*持续学习，持续改进。每一次错误都是成长的机会。*
