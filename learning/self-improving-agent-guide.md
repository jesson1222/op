# Self-Improving Agent 学习指南

## 📚 核心概念

**Self-Improving Agent** 是一个让 AI 能够从错误和纠正中持续学习的技能。它通过记录 learnings、errors 和 corrections，让 AI 越来越聪明。

---

## 🎯 核心价值

**解决的问题**：
- AI 重复犯同样的错误
- 用户纠正后 AI 很快就忘了
- 宝贵经验没有沉淀下来
- 每个会话都是"从零开始"

**带来的改变**：
- ✅ AI 记住你的纠正和偏好
- ✅ 错误被记录并分析
- ✅ 最佳实践自动沉淀
- ✅ 经验可以跨会话复用

---

## 🏗️ 工作原理

```
用户纠正/AI 犯错
    ↓
记录到 .learnings/
    ↓
定期 Review
    ↓
Promote 到项目记忆
    ↓
AI 下次不再犯同样错误
```

---

## 📁 文件结构

```
~/.openclaw/workspace/
├── .learnings/              # 学习日志目录
│   ├── LEARNINGS.md         # 纠正和最佳实践
│   ├── ERRORS.md            # 错误和异常
│   └── FEATURE_REQUESTS.md  # 功能请求
├── AGENTS.md                # 工作流和自动化
├── SOUL.md                  # 行为准则
├── TOOLS.md                 # 工具使用指南
└── MEMORY.md                # 长期记忆
```

---

## 🔧 使用场景

### 1️⃣ 用户纠正时 → Learning

**触发词**：
- "不，应该是..."
- "你错了..."
- "实际上..."
- "这个不对..."

**示例**：
```markdown
## [LRN-20260306-001] correction

**Logged**: 2026-03-06T00:40:00Z
**Priority**: high
**Status**: pending
**Area**: config

### Summary
用户纠正：项目使用 pnpm 而不是 npm

### Details
我使用了 `npm install` 但失败了。用户指出项目使用 pnpm 工作区，
必须使用 `pnpm install`。lock 文件是 `pnpm-lock.yaml`。

### Suggested Action
所有安装命令改用 `pnpm install`

### Metadata
- Source: user_feedback
- Related Files: package.json, pnpm-lock.yaml
- Tags: package-manager, pnpm
- Pattern-Key: harden.package_manager

---
```

### 2️⃣ 命令失败时 → Error

**触发**：
- 命令返回非零退出码
- 异常或堆栈跟踪
- 意外输出或行为

**示例**：
```markdown
## [ERR-20260306-001] git_push

**Logged**: 2026-03-06T00:45:00Z
**Priority**: high
**Status**: pending
**Area**: infra

### Summary
git push 失败，需要配置认证

### Error
```
fatal: Could not read from remote repository.
Please make sure you have the correct access rights
```

### Context
- 命令：`git push origin main`
- 环境：新部署的服务器
- Git 版本：2.40.0

### Suggested Fix
配置 SSH key 或使用 PAT

### Metadata
- Reproducible: yes
- Related Files: ~/.ssh/id_rsa

---
```

### 3️⃣ 发现更好的方法 → Best Practice

**示例**：
```markdown
## [LRN-20260306-002] best_practice

**Logged**: 2026-03-06T01:00:00Z
**Priority**: medium
**Status**: pending
**Area**: backend

### Summary
使用异步批处理优化数据库查询

### Details
原本对 100 个用户分别查询帖子（N+1 问题），
改用 DataLoader 批处理后，查询从 101 次减少到 2 次。

### Suggested Action
所有关联查询使用 DataLoader 模式

### Metadata
- Source: conversation
- Related Files: src/resolvers/user.js
- Tags: performance, dataloader, n-plus-one
- Pattern-Key: optimize.batch_queries

---
```

---

## 📊 优先级规则

| 优先级 | 使用场景 |
|--------|----------|
| **critical** | 阻塞核心功能、数据丢失风险、安全问题 |
| **high** | 重大影响、影响常见工作流、重复问题 |
| **medium** | 中等影响、有变通方案 |
| **low** | 小问题、边缘情况、锦上添花 |

---

## 🎯 Promote 机制

当 learning 被验证为广泛适用时，Promote 到项目记忆：

### Promote 目标

| Learning 类型 | Promote 到 | 示例 |
|---------------|-----------|------|
| 行为模式 | `SOUL.md` | "简洁，避免免责声明" |
| 工作流改进 | `AGENTS.md` | "长任务 spawn 子 agent" |
| 工具坑点 | `TOOLS.md` | "Git push 需要先配置认证" |
| 项目约定 | `AGENTS.md` | "使用 pnpm 不是 npm" |

### Promote 示例

**Learning（详细）**：
> 项目使用 pnpm 工作区。尝试 `npm install` 失败了。
> Lock 文件是 `pnpm-lock.yaml`，必须使用 `pnpm install`。

**在 AGENTS.md（简洁）**：
```markdown
## 构建和依赖
- 包管理器：pnpm（不是 npm）- 使用 `pnpm install`
```

---

## 🔄 重复模式检测

如果记录到类似的问题：

1. **先搜索**：`grep -r "keyword" .learnings/`
2. **链接条目**：添加 `**See Also**: ERR-20250110-001`
3. **提升优先级**：如果问题反复出现
4. **考虑系统性修复**：
   - 缺少文档 → Promote 到 AGENTS.md
   - 缺少自动化 → 添加脚本
   - 架构问题 → 创建技术债务 Ticket

---

## 📈 使用工作流

### 日常使用

```bash
# 1. 会话开始时 Review 相关 learnings
grep -l "Area.*backend" .learnings/*.md

# 2. 遇到问题时记录
# 使用 AI 自动记录或手动添加到对应文件

# 3. 完成任务后 Review
cat .learnings/LEARNINGS.md | tail -50

# 4. Promote 有价值的 learning
# 复制到 AGENTS.md/SOUL.md/TOOLS.md
```

### 定期 Review

```bash
# 统计 pending 条目
grep -h "Status.*: pending" .learnings/*.md | wc -l

# 列出高优先级 pending
grep -B5 "Priority.*: high" .learnings/*.md | grep "^## \["

# 查找特定区域的 learnings
grep -l "Area.*: backend" .learnings/*.md
```

---

## 🎓 最佳实践

1. **立即记录** - 上下文最新鲜
2. **具体详细** - 未来 AI 需要快速理解
3. **包含复现步骤** - 特别是 errors
4. **链接相关文件** - 便于修复
5. **建议具体修复** - 不只是"调查"
6. **使用一致分类** - 便于过滤
7. **积极 Promote** - 有疑问就添加到 AGENTS.md
8. **定期 Review** - 过时的 learnings 失去价值

---

## 🛠️ 实际案例

### 案例 1：N+1 查询优化

**问题**：GraphQL API 查询 100 个用户的帖子，产生 101 次数据库查询

**记录到 LEARNINGS.md**：
```markdown
## [LRN-20260305-001] best_practice

**Logged**: 2026-03-05T14:30:00Z
**Priority**: high
**Status**: promoted
**Area**: backend

### Summary
使用 DataLoader 解决 N+1 查询问题

### Details
查询 100 个用户的帖子时，原本对每个用户单独查询（N+1 问题）。
改用 DataLoader 批处理后，查询从 101 次减少到 2 次。

性能提升：10 倍（500ms → 50ms）

### Suggested Action
所有关联查询使用 DataLoader 模式

### Metadata
- Source: conversation
- Related Files: src/resolvers/user.js
- Tags: performance, dataloader, n-plus-one
- Pattern-Key: optimize.batch_queries

---
```

**Promote 到 AGENTS.md**：
```markdown
## 数据库优化

### N+1 查询问题
- 使用 DataLoader 批处理关联查询
- 目标：将 N+1 次查询减少到 2 次
- 参考：`skills/python-asyncio-connection-pool.md`
```

---

### 案例 2：包管理器混淆

**问题**：AI 使用 npm install 但项目使用 pnpm

**记录到 LEARNINGS.md**：
```markdown
## [LRN-20260306-001] correction

**Logged**: 2026-03-06T00:40:00Z
**Priority**: high
**Status**: pending
**Area**: config

### Summary
项目使用 pnpm 而不是 npm

### Details
使用了 `npm install` 但失败了。用户指出项目使用 pnpm 工作区。
Lock 文件是 `pnpm-lock.yaml`，必须使用 `pnpm install`。

### Suggested Action
所有安装命令改用 `pnpm install`

### Metadata
- Source: user_feedback
- Related Files: package.json, pnpm-lock.yaml
- Tags: package-manager, pnpm
- Pattern-Key: harden.package_manager

---
```

**Promote 到 AGENTS.md**：
```markdown
## 包管理器

- 使用 **pnpm**（不是 npm 或 yarn）
- 命令：`pnpm install`, `pnpm add <pkg>`, `pnpm run <script>`
- Lock 文件：`pnpm-lock.yaml`
```

---

## 📚 参考资源

- **原文档**: https://playbooks.com/skills/openclaw/skills/self-improving-agent
- **GitHub**: https://github.com/pskoett/pskoett-ai-skills/tree/main/skills/self-improvement
- **OpenClaw 集成**: `skills/self-improving-agent/`

---

## 🎯 下一步

1. **开始记录** - 下次纠正 AI 时记录到 LEARNINGS.md
2. **定期 Review** - 每周查看 pending learnings
3. **积极 Promote** - 将通用知识添加到 AGENTS.md/SOUL.md
4. **持续改进** - 让 AI 从经验中学习成长

---

*学习时间：2026-03-06*
*来源：Self-Improving Agent Skill*
