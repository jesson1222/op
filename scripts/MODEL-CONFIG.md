# OpenClaw 模型配置说明

## 📋 可用模型列表

### 阿里云百炼 (bailian)
| 模型 | 别名 | 上下文 | 特点 | 推荐场景 |
|:-----|:-----|:-------|:-----|:---------|
| `qwen3.5-plus` | `bailian/qwen3.5-plus` | 1M | ⭐ 均衡性能 | 日常对话、通用任务 |
| `qwen3-max-2026-01-23` | `bailian/qwen3-max` | 262K | 最强推理 | 复杂任务、代码生成 |
| `qwen3-coder-next` | `bailian/qwen-coder` | 262K | 代码优化 | 编程任务 |
| `qwen3-coder-plus` | - | 1M | 代码 + 长文本 | 大型项目分析 |
| `MiniMax-M2.5` | `bailian/minimax` | 196K | 多模态 | 图文理解 |
| `glm-5` | `bailian/glm-5` | 202K | 长文本 | 文档分析 |
| `glm-4.7` | `bailian/glm-4` | 202K | 快速响应 | 简单问答 |
| `kimi-k2.5` | `bailian/kimi` | 262K | 长文本 | 超长文档 |

### iFlow 心流 (iflow) - 免费
| 模型 | 别名 | 上下文 | 特点 | 推荐场景 |
|:-----|:-----|:-------|:-----|:---------|
| `qwen3-max` | `iflow-qwen-max` | 262K | ⭐ 免费最强 | 日常使用（默认） |
| `qwen3-coder-plus` | `iflow-qwen-coder` | 262K | 代码专用 | 编程任务 |
| `kimi-k2` | `iflow-kimi-k2` | 128K | 长文本 | 文档分析 |
| `deepseek-v3.2` | `iflow-deepseek-v3` | 128K | 性价比 | 通用任务 |
| `deepseek-r1` | `iflow-deepseek-r1` | 128K | 推理 | 数学/逻辑 |
| `qwen3-235b` | `iflow-qwen-235b` | 128K | 多模态 | 图像理解 |

### Ollama (本地)
| 模型 | 别名 | 上下文 | 特点 |
|:-----|:-----|:-------|:-----|
| `qwen3.5:35b` | `ollama/qwen3.5` | 262K | 本地运行 |
| `llama3.1:8b` | `__OPENCLAW_REDACTED__` | - | 轻量级 |

### Qwen Portal
| 模型 | 别名 | 上下文 |
|:-----|:-----|:-------|
| `coder-model` | `qwen` | 128K |
| `vision-model` | `qwen-vl` | 128K |

### MiniMax Portal
| 模型 | 别名 | 上下文 |
|:-----|:-----|:-------|
| `MiniMax-M2.5` | `minimax-m2.5` | 200K |
| `MiniMax-M2.5-highspeed` | `minimax-m2.5-highspeed` | 200K |
| `MiniMax-M2.5-Lightning` | `minimax-m2.5-lightning` | 200K |

---

## 🚀 快速切换模型

### 方法 1: 使用切换脚本（推荐）

```bash
# 查看所有可用模型
~/.openclaw/workspace/scripts/model-switch.sh list

# 切换到百炼 Qwen3.5 Plus
~/.openclaw/workspace/scripts/model-switch.sh bailian

# 切换到 iFlow 免费模型
~/.openclaw/workspace/scripts/model-switch.sh iflow

# 切换到指定模型
~/.openclaw/workspace/scripts/model-switch.sh bailian/qwen3-max
```

### 方法 2: 在对话中使用命令

```
/model bailian/qwen3.5-plus
/model iflow-qwen-max
/model ollama/qwen3.5
```

### 方法 3: 修改配置文件

编辑 `~/.openclaw/openclaw.json`:
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "bailian/qwen3.5-plus"
      }
    }
  }
}
```

---

## 💡 推荐配置

### 省钱模式（日常使用）
```bash
~/.openclaw/workspace/scripts/model-switch.sh iflow
```
- 使用 iFlow 免费模型
- 预计每月节省 ¥600-1200
- 功能完整，自动续期

### 高性能模式（复杂任务）
```bash
~/.openclaw/workspace/scripts/model-switch.sh bailian/qwen3-max
```
- 使用百炼 Qwen3 Max
- 最强推理能力
- 适合代码生成、复杂分析

### 本地模式（隐私敏感）
```bash
~/.openclaw/workspace/scripts/model-switch.sh ollama
```
- 使用本地 Ollama
- 数据不出本地
- 无需网络

---

## 📊 模型对比

| 维度 | 百炼 | iFlow | Ollama |
|:-----|:----:|:-----:|:------:|
| **成本** | 付费 | ✅ 免费 | ✅ 免费 |
| **速度** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **质量** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **隐私** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **稳定性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 🔧 配置文件位置

| 文件 | 说明 |
|:-----|:-----|
| `~/.openclaw/openclaw.json` | 主配置文件 |
| `~/.iflow/settings.json` | iFlow 认证配置 |
| `~/.openclaw/workspace/scripts/model-switch.sh` | 切换脚本 |

---

## ⚠️ 注意事项

1. **iFlow OAuth**: 自动续期，无需手动管理 Key
2. **百炼 API Key**: 需要确保账户有足够余额
3. **Ollama**: 需要先安装并拉取模型
4. **切换后立即生效**: 无需重启 OpenClaw

---

**更新时间**: 2026-03-13  
**维护者**: OpenClaw Assistant
