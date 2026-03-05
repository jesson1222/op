# Anthropic Skill Creator 学习指南

## 📚 核心概念

**Skill Creator** 是 Anthropic 官方发布的"元技能" - 用于创建和优化其他技能的技能。

**核心价值**：
- 🎯 系统化创建高质量技能
- 📊 量化评估技能效果
- 🔄 迭代优化技能性能
- 📈 持续改进触发准确率

---

## 🏗️ 技能创建流程

### 完整流程图

```
1. 捕获意图 → 2. 访谈调研 → 3. 编写 SKILL.md → 4. 创建测试用例
                                              ↓
8. 打包发布 ← 7. 描述优化 ← 6. 迭代改进 ← 5. 运行评估
```

---

## 📝 详细步骤

### 步骤 1: 捕获意图 (Capture Intent)

**核心问题**：
1. 这个技能要让 Claude 能做什么？
2. 什么时候触发？（用户说什么话/什么场景）
3. 预期输出格式是什么？
4. 是否需要测试用例？

**测试用例判断**：
- ✅ **需要**：客观可验证的输出（文件转换、数据提取、代码生成）
- ❌ **不需要**：主观输出（写作风格、艺术创作）

---

### 步骤 2: 访谈调研 (Interview and Research)

**主动询问**：
- 边缘情况
- 输入/输出格式
- 示例文件
- 成功标准
- 依赖关系

**并行调研**：
- 搜索文档
- 查找类似技能
- 学习最佳实践

---

### 步骤 3: 编写 SKILL.md

**必需组件**：

```yaml
---
name: skill-name
description: 触发条件 + 功能描述（这是主要触发机制！）
compatibility: 所需工具、依赖（可选）
---

# 技能正文
```

**关键要点**：
- **description** 是主要触发机制
- 包含"做什么"和"何时使用"
- 描述要"pushy"一些（避免 undertrigger）
- 包含具体场景，不只是抽象功能

**示例**：
```yaml
# ❌ 太简单
description: 如何构建数据仪表板

# ✅ Pushy 描述
description: 如何构建数据仪表板。每当用户提到仪表板、数据可视化、内部指标，或想展示任何公司数据时都要使用此技能，即使用户没有明确说要"仪表板"。
```

---

### 步骤 4: 创建测试用例

**测试用例格式** (`evals/evals.json`)：

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "用户的实际任务",
      "expected_output": "预期输出描述",
      "files": []
    }
  ]
}
```

**测试用例设计原则**：
- 2-3 个真实场景
- 用户实际会说的话
- 覆盖不同情况
- 与用户确认后再运行

**好的测试用例示例**：
```json
{
  "prompt": "ok so my boss just sent me this xlsx file (its in my downloads, called something like 'Q4 sales final FINAL v2.xlsx') and she wants me to add a column that shows the profit margin as a percentage. The revenue is in column C and costs are in column D i think"
}
```

**坏的测试用例**：
```json
{
  "prompt": "Format this data"  // 太抽象
}
```

---

### 步骤 5: 运行评估 (Running Evals)

#### 5.1 并行运行（有 subagents 时）

**每个测试用例运行 2 个 subagent**：

**With-skill run**：
```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Save outputs to: <workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/
```

**Baseline run**：
- **新技能**: 不使用技能（without_skill）
- **改进技能**: 使用旧版本（old_skill）

**重要**：同时启动两个 subagent，不要先后！

#### 5.2 创建元数据

每个测试用例创建 `eval_metadata.json`：

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "用户任务 prompt",
  "assertions": []
}
```

#### 5.3 编写断言（等待运行时）

**好的断言特征**：
- ✅ 客观可验证
- ✅ 描述性名称
- ✅ 一看就懂检查什么

**主观技能**（写作、设计）：最好定性评估，不要强制断言

#### 5.4 保存时序数据

subagent 完成时，保存 `timing.json`：

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

---

### 步骤 6: 评分和聚合

#### 6.1 评分每个运行

使用 `agents/grader.md` 评估每个断言，保存 `grading.json`：

```json
{
  "expectations": [
    {
      "text": "断言描述",
      "passed": true,
      "evidence": "证据"
    }
  ]
}
```

**注意**：字段必须是 `text`、`passed`、`evidence`（viewer 依赖这些字段名）

#### 6.2 聚合为 benchmark

```bash
python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
```

生成 `benchmark.json` 和 `benchmark.md`，包含：
- pass_rate
- time (mean ± stddev)
- tokens (mean ± stddev)
- delta (with_skill vs baseline)

#### 6.3 分析师检查

阅读 `agents/analyzer.md`，寻找：
- 总是通过的断言（non-discriminating）
- 高方差的评估（flaky）
- 时间/token 权衡

#### 6.4 启动 viewer

```bash
nohup python <skill-creator-path>/eval-viewer/generate_review.py \
  <workspace>/iteration-N \
  --skill-name "my-skill" \
  --benchmark <workspace>/iteration-N/benchmark.json \
  > /dev/null 2>&1 &
```

**Cowork/无显示环境**：使用 `--static <output_path>` 生成独立 HTML

**用户看到什么**：
- **Outputs 标签**：每个测试用例的输出
- **Benchmark 标签**：定量统计
- **Feedback 文本框**：自动保存
- **Previous Feedback**（迭代 2+）：上次的反馈

---

### 步骤 7: 改进技能

#### 改进原则

1. **从反馈中泛化**
   - 不要过拟合到几个测试用例
   - 技能要能用一百万次
   - 尝试不同的隐喻和方法

2. **保持简洁**
   - 删除不重要的内容
   - 阅读 transcript，看是否浪费时间
   - 去除不生产的部分

3. **解释为什么**
   - 解释每个要求背后的原因
   - 避免 heavy-handed 的 MUST
   - 用理论 of mind 理解用户意图

4. **识别重复工作**
   - 如果所有测试用例都写了类似的脚本 → 打包到 `scripts/`
   - 如果都用了类似的多步骤方法 → 固化到技能中

#### 迭代循环

```
1. 应用改进到技能
2. 重新运行所有测试用例到 iteration-<N+1>/
3. 启动 viewer，带 --previous-workspace
4. 等待用户 review
5. 阅读新反馈，再次改进
```

**停止条件**：
- 用户满意
- 反馈都是空的（都好）
- 没有实质性进展

---

### 步骤 8: 描述优化

**description** 是主要触发机制！

#### 步骤 1: 生成触发评估查询

创建 20 个查询（should-trigger + should-not-trigger）：

```json
[
  {"query": "用户 prompt", "should_trigger": true},
  {"query": "另一个 prompt", "should_trigger": false}
]
```

**Should-trigger (8-10 个)**：
- 不同措辞的相同意图
- 正式 +  casual 混合
- 用户没有明确说技能名但需要它
- 罕见用例
- 与其他技能竞争但应该赢

**Should-not-trigger (8-10 个)**：
- **最有价值**：near-misses（近似但不应该触发）
- 共享关键词但实际需要不同的东西
- 相邻领域
- 模糊措辞（naive 关键词匹配会触发但不应该）

**坏的 negative**：
```json
{"query": "Write a fibonacci function", "should_trigger": false}
// 太明显无关，不测试任何东西
```

#### 步骤 2: 用户 Review

使用 HTML 模板让用户 review：
1. 读取 `assets/eval_review.html`
2. 替换占位符
3. 打开浏览器让用户编辑
4. 导出 `eval_set.json`

#### 步骤 3: 运行优化循环

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <当前会话的 model> \
  --max-iterations 5 \
  --verbose
```

**优化过程**：
- 60% train / 40% held-out test
- 每个查询运行 3 次获取可靠触发率
- 调用 Claude（带 extended thinking）提出改进
- 在 train 和 test 上重新评估
- 迭代最多 5 次
- 生成 HTML 报告

#### 步骤 4: 应用结果

使用 `best_description` 更新 SKILL.md frontmatter

---

## 🎯 技能解剖学

### 目录结构

```
skill-name/
├── SKILL.md (必需)
│   ├── YAML frontmatter (name, description 必需)
│   └── Markdown 指令
└── Bundled Resources (可选)
    ├── scripts/    - 可执行代码（确定性/重复任务）
    ├── references/ - 文档（按需加载）
    └── assets/     - 输出文件（模板、图标、字体）
```

### 渐进式披露 (Progressive Disclosure)

**三级加载系统**：

1. **Metadata** (name + description) - 始终在上下文 (~100 字)
2. **SKILL.md body** - 技能触发时加载 (<500 行理想)
3. **Bundled resources** - 按需加载（无限）

**关键模式**：
- SKILL.md 保持在 500 行以下
- 接近限制时添加额外层级
- 清晰引用文件，指导何时读取
- 大文件 (>300 行) 包含目录

**领域组织**：
```
cloud-deploy/
├── SKILL.md (工作流 + 选择指南)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```
Claude 只读取相关的参考文件。

---

## 📊 评估指标

### 定量指标

| 指标 | 说明 |
|------|------|
| **Pass Rate** | 断言通过率 |
| **Time** | 执行时间 (mean ± stddev) |
| **Tokens** | Token 消耗 (mean ± stddev) |
| **Delta** | with_skill vs baseline 差异 |

### 定性评估

- 用户反馈
- 输出质量
- 易用性
- 覆盖范围

---

## 🎓 最佳实践

### 写作模式

**定义输出格式**：
```markdown
## 报告结构
ALWAYS 使用这个确切模板：
# [标题]
## 执行摘要
## 关键发现
## 建议
```

**示例模式**：
```markdown
## Commit 消息格式
**示例 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

### 写作风格

- 用祈使句
- 解释**为什么**重要
- 避免过多的 MUST/NEVER
- 用理论 of mind 让技能通用化
- 先写草稿，然后以新视角改进

### 沟通技巧

**根据用户调整措辞**：
- ✅ OK: "evaluation", "benchmark"
- ⚠️ 看情况："JSON", "assertion"（需要用户有相关 cues）
- ❌ 避免：不解释就用专业术语

---

## 🔄 Claude.ai 特殊说明

**无 subagents 时的调整**：

| 功能 | Claude Code | Claude.ai |
|------|-------------|-----------|
| **运行测试** | 并行 subagents | 顺序执行（自己 follow 技能） |
| **Baseline** | without_skill/old_skill | 跳过 |
| **Review** | 浏览器 viewer | 对话中直接展示 |
| **Benchmark** | 定量 + 定性 | 只定性 |
| **描述优化** | ✅ 支持 | ❌ 跳过（需要 claude CLI） |
| **盲对比** | ✅ 支持 | ❌ 跳过 |
| **打包** | ✅ 支持 | ✅ 支持（用户下载） |

---

## 💡 关键洞察

### 技能触发原理

- Skills 出现在 `available_skills` 列表（name + description）
- Claude 基于 description 决定是否咨询技能
- **重要**：Claude 只在不能直接处理的任务才咨询技能
- 简单查询（"read this PDF"）可能不触发技能
- 复杂、多步骤、专业化查询可靠触发

**评估查询设计**：
- 要足够 substantive
- 简单查询不是好的测试用例
- Claude 可以直接处理的不会触发技能

### 改进思维

**核心目标**：
> 创建能用一百万次的技能，而不是只适应几个测试用例

**改进策略**：
1. 泛化反馈，不要过拟合
2. 保持 prompt 简洁
3. 解释为什么（LLM 很聪明，给 harness 能超越 rote instructions）
4. 识别重复工作 → 打包成脚本

---

## 📚 参考资源

- **原文档**: https://github.com/anthropics/skills/tree/main/skills/skill-creator
- **评估 Schema**: `references/schemas.md`
- **Grader**: `agents/grader.md`
- **Analyzer**: `agents/analyzer.md`
- **Comparator**: `agents/comparator.md`

---

## 🎯 应用建议

### 创建新技能时

1. 遵循完整流程（意图 → 访谈 → 编写 → 测试 → 评估 → 改进 → 优化）
2. 不要跳过测试和评估
3. 重视 description 优化
4. 打包并呈现给用户

### 改进现有技能时

1. 从用户反馈开始
2. 运行评估找出具体问题
3. 迭代改进（可能多次）
4. 重新评估验证改进

### 日常使用

- 阅读 transcript 而不仅是最终输出
- 注意重复模式
- 主动建议打包脚本
- 解释改进背后的原因

---

*学习时间：2026-03-06*
*来源：Anthropic Official Skills*
