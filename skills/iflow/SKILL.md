# iFlow 集成技能

使用 iFlow CLI（心流 CLI）执行终端 AI 任务，利用免费的高质量 AI 模型进行代码分析、文件操作和编程任务。

## 触发条件

- 用户请求代码分析、文件操作、编程任务
- 用户提到 "用 iflow"、"心流"、"iflow CLI"
- 需要执行复杂的终端 AI 任务
- 用户想使用免费模型（Qwen3 Max、Kimi K2、DeepSeek 等）

## 前置条件

1. ✅ 已安装 iFlow CLI：`npm i -g @iflow-ai/iflow-cli`
2. ✅ 已配置 API Key：`~/.iflow/settings.json`
3. ✅ 已配置包装脚本：`~/.openclaw/workspace/scripts/iflow.sh`

## 可用模型

| 模型 | 别名 | 用途 |
|------|------|------|
| Qwen3 Max | `iflow-qwen-max` | ⭐ 最强通用（默认） |
| Qwen3 Coder Plus | `iflow-qwen-coder` | 代码专用 |
| Kimi K2 | `iflow-kimi-k2` | 长文本处理 |
| DeepSeek V3.2 | `iflow-deepseek-v3` | 性价比 |
| DeepSeek R1 | `iflow-deepseek-r1` | 推理/数学 |
| Qwen3 235B | `iflow-qwen-235b` | 图像理解 |

## 使用方法

### 方式 1：通过包装脚本调用

```bash
# 简单任务
~/.openclaw/workspace/scripts/iflow.sh -p "分析这个项目的结构"

# 指定模型
~/.openclaw/workspace/scripts/iflow.sh -m kimi-k2 -p "总结这个文档"
```

### 方式 2：直接使用 iflow 命令

```bash
# 交互式模式
iflow

# 非交互式模式
echo "分析 @src 目录" | iflow -p ""

# 指定模型
iflow -m deepseek-r1 -p "解决这个数学问题"
```

### 方式 3：在 OpenClaw 中切换模型

```
/model iflow-qwen-max
```

## 环境变量

包装脚本已配置以下环境变量：

```bash
export IFLOW_API_KEY="sk-9ec7afd604d8e826a8da01016fdd3a1c"
export IFLOW_BASE_URL="https://apis.iflow.cn/v1"
export IFLOW_MODEL_NAME="qwen3-max"
```

## 运行模式

iFlow 支持 4 种运行模式：

| 模式 | 权限 | 说明 |
|------|------|------|
| **yolo** | 最大权限 | 模型可执行任何操作 (`-y`) |
| **auto-edit** | 文件修改权限 | 模型仅可修改文件 |
| **plan** | 需确认 | 先计划后执行 |
| **default** | 无权限 | 仅提供建议（默认） |

### 示例

```bash
# YOLO 模式（谨慎使用）
iflow -y -p "重构这个项目的代码结构"

# 计划模式
iflow --plan -p "帮我设计一个用户认证系统"
```

## 常用场景

### 1. 代码项目分析

```bash
cd your-project/
iflow -p "分析这个项目的结构和主要功能"
```

### 2. 文件批量处理

```bash
iflow -p "将我桌面上的文件按文件类型整理到不同的文件夹中"
```

### 3. 数据分析

```bash
iflow -p "分析这个 Excel 表格中的销售数据，生成简单的图表"
```

### 4. 工作流自动化

```bash
iflow -p "创建一个脚本，定期将我的重要文件备份到云存储"
```

### 5. 代码生成

```bash
iflow -p "用 Python 写一个 REST API，包含用户 CRUD 操作"
```

## 注意事项

### ⚠️ API Key 有效期

- **有效期**: 7 天
- **到期处理**: 访问 https://iflow.cn/?open=setting 重新生成
- **更新方法**: 修改 `~/.iflow/settings.json` 和 `~/.openclaw/workspace/scripts/iflow.sh`

### ⚠️ 网络连接

- 需要访问 `https://apis.iflow.cn/v1`
- 确保网络通畅，避免超时

### ⚠️ Token 使用

- iFlow 对个人用户免费，但仍需合理使用
- 避免短时间内大量请求

### ⚠️ 模型选择

- **默认**: qwen3-max（综合能力最强）
- **代码**: qwen3-coder-plus
- **长文本**: kimi-k2
- **推理**: deepseek-r1

## 故障排查

### 问题 1：认证失败

```
Please set an Auth method in your settings.json
```

**解决**: 检查 `~/.iflow/settings.json` 是否包含有效的 API Key

### 问题 2：模型不可用

```
Model xxx does not exist
```

**解决**: 检查模型名称是否正确，参考可用模型列表

### 问题 3：网络超时

```
Request timed out
```

**解决**: 检查网络连接，稍后重试

## 相关文件

- **配置文件**: `~/.iflow/settings.json`
- **包装脚本**: `~/.openclaw/workspace/scripts/iflow.sh`
- **OpenClaw 配置**: `~/.openclaw/openclaw.json`
- **研究报告**: `~/.openclaw/workspace/research/iflow-research.md`
- **配置说明**: `~/.openclaw/workspace/iflow-config.md`

## 更新历史

- **2026-03-13**: 初始版本，完成 iFlow CLI 安装和配置
  - API Key: sk-9ec7afd604d8e826a8da01016fdd3a1c（7 天有效期）
  - 默认模型：qwen3-max
  - 包装脚本已创建

---

*技能创建时间：2026-03-13*
*基于 iFlow CLI v0.5.17*
