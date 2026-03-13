# iFlow OAuth 认证配置完成

## ✅ 认证方式

**OAuth (通过 iFlow 登录)** - 已配置完成！

---

## 🎯 优势

| 特性 | API Key 方式 | OAuth 方式 |
|:-----|:----------:|:----------:|
| **有效期** | 7 天 | ✅ 自动续期 |
| **手动更新** | 需要 | ✅ 无需 |
| **WebSearch** | ✅ | ✅ |
| **WebFetch** | ✅ | ✅ |
| **多模态** | ✅ | ✅ |
| **工具调用优化** | ✅ | ✅ |

---

## 📦 配置文件

### ~/.iflow/settings.json
```json
{
  "selectedAuthType": "oauth-iflow",
  "bootAnimationShown": true
}
```

### ~/.iflow/oauth_creds.json
- 包含访问令牌和刷新令牌
- 自动管理，无需手动干预

### ~/.iflow/iflow_accounts.json
```json
{
  "active": "oauth-iflow",
  "authType": "oauth-iflow"
}
```

---

## 🚀 使用方法

### 直接使用
```bash
iflow -p "帮我写个 Python 脚本"
```

### 通过包装脚本
```bash
~/.openclaw/workspace/scripts/iflow.sh -p "分析这个项目"
```

### 在 OpenClaw 中
```
/model iflow-qwen-max
```

---

## 🔄 重新认证（如需要）

如果 OAuth 失效，重新认证：

```bash
# 方式 1：交互式
iflow
# 选择 "Login with iFlow"

# 方式 2：一键命令
iflow --help  # 查看认证选项
```

浏览器会自动打开并完成登录，Token 自动续期！

---

## 📊 测试验证

```bash
# 测试连接
echo "测试" | iflow -p "请回复：OAuth 认证成功"
```

---

## 🗑️ 已清理的配置

- ❌ API Key 管理脚本（不再需要）
- ❌ API Key 到期检查 Cron（不再需要）
- ❌ API Key 更新脚本（不再需要）

---

**配置时间**: 2026-03-13 21:39  
**认证状态**: ✅ OAuth 已激活  
**Token 状态**: ✅ 自动续期  

---

## 💡 说明

之前配置的 API Key 自动管理工具包已废弃，因为：
1. OAuth 方式更简单
2. 无需担心 7 天过期
3. 功能完全相同
4. 官方推荐方式

保留的脚本（仅供学习参考）：
- `scripts/iflow-auto-get-key-v3.mjs` - Playwright 自动获取
- `scripts/iflow-update-key.sh` - Key 更新
- `scripts/iflow-key-manager.sh` - 有效期管理

**现在无需使用这些脚本！** 🎉
