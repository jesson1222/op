# iFlow 模型配置说明

## ✅ 已配置完成

iFlow 已成功集成到 OpenClaw，可以免费使用多个顶级模型！

**技能系统**: ✅ 已创建 `skills/iflow/SKILL.md`

---

## 📦 安装验证

```bash
# 验证 CLI 安装
iflow --version
# 输出：0.5.17

# 测试调用
~/.openclaw/workspace/scripts/iflow.sh -p "你好"
```

---

## 📋 可用模型列表

| 模型别名 | 完整名称 | 上下文 | 特点 |
|:--------|:--------|:-------|:----|
| `iflow-qwen-max` | iflow/qwen3-max | 256K | 最强通用模型 ⭐ 推荐 |
| `iflow-qwen-coder` | iflow/qwen3-coder-plus | 256K | 代码能力强 |
| `iflow-kimi-k2` | iflow/kimi-k2 | 128K | 长文本处理 |
| `iflow-deepseek-v3` | iflow/deepseek-v3.2 | 128K | 性价比高 |
| `iflow-deepseek-r1` | iflow/deepseek-r1 | 128K | 推理能力强 |
| `iflow-qwen-235b` | iflow/qwen3-235b | 128K | 支持图像理解 |

---

## 🚀 使用方法

### 方法 1：临时切换模型
```bash
openclaw --model iflow-qwen-max "帮我写个 Python 脚本"
```

### 方法 2：在对话中切换
```
/model iflow-qwen-max
```

### 方法 3：修改默认模型
编辑 `~/.openclaw/openclaw.cherry.json`：
```json
"agents": {
  "defaults": {
    "model": {
      "primary": "iflow/iflow-qwen-max"
    }
  }
}
```

---

## 💡 推荐场景

| 场景 | 推荐模型 | 理由 |
|:----|:--------|:----|
| 日常对话 | `iflow-qwen-max` | 综合能力最强 ⭐ |
| 代码编写 | `iflow-qwen-coder` | 代码优化好 |
| 长文档分析 | `iflow-kimi-k2` | 长文本擅长 |
| 复杂推理 | `iflow-deepseek-r1` | 推理能力强 |
| 图像理解 | `iflow-qwen-235b` | 支持多模态 |

---

## ⚠️ 注意事项

1. **API Key 有效期**：7 天
   - 到期后需要重新获取
   - 获取地址：https://iflow.cn/?open=setting

2. **免费政策**：
   - 个人用户永久免费
   - 无使用次数限制
   - 无流量限制

3. **速率限制**：
   - 如果遇到速率限制，稍等片刻再试
   - 避免短时间内大量请求

---

## 🔄 更新 API Key

如果 API Key 过期，按以下步骤更新：

1. 访问 https://iflow.cn/?open=setting
2. 生成新的 API Key
3. 编辑 `~/.openclaw/openclaw.cherry.json`
4. 找到 `"iflow"` 配置节
5. 更新 `"apiKey"` 字段
6. 保存文件

或者运行：
```bash
openclaw config set iflow.apiKey sk-新的 key
```

---

## 📊 成本对比

| 来源 | Qwen3 Max | Kimi K2 | DeepSeek V3 |
|:----|:--------|:-------|:-----------|
| **iFlow** | ✅ 免费 | ✅ 免费 | ✅ 免费 |
| **官方 API** | ~¥0.02/1K tokens | ~¥0.012/1K tokens | ~¥0.004/1K tokens |
| **月省费用** | ~¥300-600 | ~¥200-400 | ~¥100-200 |

**预计每月节省：¥600-1200**（根据使用量）

---

## ✅ 配置验证

运行以下命令测试：
```bash
openclaw --model iflow-qwen-max "测试 iFlow 连接"
```

如果正常回复，说明配置成功！

---

**配置时间**: 2026-03-11  
**配置状态**: ✅ 完成
