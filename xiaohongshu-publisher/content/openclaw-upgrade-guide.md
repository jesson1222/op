# OpenClaw v2026.3.8 升级后不适？老用户带你快速上手！🦞

昨天升级完 v2026.3.8，我也懵了一下
配置好像变了，命令也不太一样了😅

花了一下午研究文档+测试，整理这份**避坑指南**
帮你 5 分钟搞定新系统！👇

---

## 🔥 升级后最大的 3 个变化

### 1️⃣ 备份功能上线（这个真的香！）
```bash
# 升级前先备份（重要！）
openclaw backup create

# 验证备份
openclaw backup verify

# 只备份配置（不包含工作区）
openclaw backup create --only-config
```

**位置：** `~/.openclaw/backups/`

---

### 2️⃣ macOS 远程网关 Token 保护
之前升级容易把 Token 搞丢，现在：
- ✅ 自动保留现有 Token
- ✅ 替换前会警告
- ✅ 新增远程模式配置字段

**配置位置：** `gateway.remote.token`

---

### 3️⃣ TUI 自动识别工作区
之前要手动配 agent，现在：
```bash
# 进入项目目录直接开用
cd my-project
openclaw tui
```
自动识别当前工作区的 agent！🎉

---

## ⚠️ 升级后常见问题

### Q1: 配置不生效？
```bash
# 重启网关
openclaw gateway restart

# 或者手动重启
launchctl bootout gui/$UID/ai.openclaw.gateway
launchctl bootstrap gui/$UID/ai.openclaw.gateway
```

### Q2: 找不到命令？
```bash
# 查看版本和 commit hash
openclaw --version

# 查看可用命令
openclaw help
```

### Q3: 备份在哪？
```bash
# 备份文件位置
ls ~/.openclaw/backups/

# 备份命名格式
openclaw-backup-YYYY-MM-DD-HHMMSS.tar.gz
```

---

## 🎯 新系统快速上手

### 第一步：创建备份
```bash
openclaw backup create
```

### 第二步：检查配置
```bash
# 查看当前配置
cat ~/.openclaw/openclaw.json | python3 -m json.tool

# 重点检查：
# - gateway.remote.token
# - agents.defaults.model.primary
# - tools.web.search.brave.mode
```

### 第三步：测试功能
```bash
# 测试备份
openclaw backup verify

# 测试 TUI
openclaw tui

# 测试网络搜索（Brave 新 API）
openclaw web search "test"
```

---

## 💡 隐藏技巧

### 1. Brave 搜索 LLM 模式
```json
{
  "tools": {
    "web": {
      "search": {
        "brave": {
          "mode": "llm-context"  // 返回带来源的摘要
        }
      }
    }
  }
}
```

### 2. 语音对话超时调整
```json
{
  "talk": {
    "silenceTimeoutMs": 2000  // 2 秒静音自动发送
  }
}
```

### 3. ACP 溯源（调试用）
```bash
openclaw acp --provenance meta+receipt
```

---

## 📊 我的配置参考

```json
{
  "gateway": {
    "mode": "local",
    "port": 18789
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "bailian/qwen3.5-plus"
      }
    }
  },
  "tools": {
    "profile": "coding",
    "web": {
      "search": {
        "enabled": true,
        "provider": "brave",
        "brave": {
          "mode": "llm-context"
        }
      }
    }
  }
}
```

---

## 🚀 推荐升级流程

1. ✅ 备份当前配置
2. ✅ 升级到最新版
3. ✅ 重启网关
4. ✅ 验证备份
5. ✅ 测试核心功能
6. ✅ 调整个性化配置

---

## 📍 资源指路

- GitHub: @openclaw/openclaw
- 文档：docs.openclaw.ai
- Discord: 社区蹲更新
- 问题：提 Issue 或社区提问

---

升级后有问题评论区问！
看到就回，一起避坑💪

#OpenClaw #AI 工具 #开发者日常 #开源项目 #效率工具 #程序员 #技术分享 #升级指南 #避坑指南 #数码科技
