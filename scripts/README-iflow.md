# iFlow API Key 自动管理

## 📋 概述

iFlow API Key 有效期为 **7 天**，本工具包提供自动检查和便捷更新功能。

---

## 🛠️ 工具列表

| 脚本 | 用途 |
|:-----|:-----|
| `iflow-key-manager.sh` | API Key 有效期管理（检查/状态） |
| `iflow-update-key.sh` | 一键更新 API Key 到所有配置文件 |

---

## 🚀 快速开始

### 查看当前状态

```bash
~/.openclaw/workspace/scripts/iflow-key-manager.sh status
```

**输出示例**：
```
📊 iFlow API Key 状态
====================
配置日期：2026-03-13T21:12:02+08:00
到期日期：2026-03-20T21:12:02+08:00
剩余天数：6
状态：✅ 正常
```

### 手动检查有效期

```bash
~/.openclaw/workspace/scripts/iflow-key-manager.sh check
```

---

## ⏰ 自动检查（Cron 任务）

已配置以下定时任务：

| 任务 | 时间 | 说明 |
|:-----|:-----|:-----|
| **每日提醒** | 每天 09:00 | 发送系统事件提醒检查 |
| **智能检查** | 每天 10:00 | 自动检查，≤3 天时提醒用户 |

### 查看 Cron 任务

```bash
openclaw cron list
```

---

## 🔄 更新 API Key

### 步骤 1：获取新 Key

#### 方式 A：自动打开浏览器（推荐）

```bash
~/.openclaw/workspace/scripts/iflow-auto-key.sh
```

脚本会：
1. 自动打开浏览器到 iFlow 设置页面
2. 显示操作指引
3. 你登录后复制 Key
4. 直接告诉我 Key，我自动更新

#### 方式 B：手动访问

1. 访问 https://iflow.cn/?open=setting
2. 登录账号
3. 生成新的 API Key（类似 `sk-xxxxxxxx`）
4. 复制 Key

### 步骤 2：运行更新脚本

```bash
~/.openclaw/workspace/scripts/iflow-update-key.sh sk-新的 key
```

**示例**：
```bash
~/.openclaw/workspace/scripts/iflow-update-key.sh sk-9ec7afd604d8e826a8da01016fdd3a1c
```

### 步骤 3：验证更新

```bash
# 检查状态
~/.openclaw/workspace/scripts/iflow-key-manager.sh status

# 测试连接
~/.openclaw/workspace/scripts/iflow.sh -p "你好"
```

---

## 📂 配置文件

更新脚本会自动修改以下文件：

| 文件 | 说明 |
|:-----|:-----|
| `~/.iflow/settings.json` | iFlow CLI 配置 |
| `~/.openclaw/workspace/scripts/iflow.sh` | 包装脚本 |
| `~/.openclaw/openclaw.json` | OpenClaw 模型配置 |
| `~/.openclaw/workspace/.iflow-key-state.json` | 有效期状态文件 |

---

## 🚨 提醒规则

| 剩余天数 | 行为 |
|:---------|:-----|
| **> 3 天** | ✅ 正常，无提醒 |
| **≤ 3 天** | ⚠️ 警告提醒 |
| **≤ 1 天** | 🚨 紧急提醒 |
| **已过期** | 🚨 已过期，立即更新 |

---

## 📝 日志

**日志位置**: `~/.openclaw/workspace/logs/iflow-key-manager.log`

**查看日志**：
```bash
tail -20 ~/.openclaw/workspace/logs/iflow-key-manager.log
```

---

## ❓ 常见问题

### Q: 为什么需要手动更新？

A: iFlow API Key 需要通过浏览器登录获取，无法完全自动化。本工具提供**到期提醒**和**一键更新**，简化流程。

### Q: 忘记更新会怎样？

A: API Key 过期后，iFlow CLI 和 OpenClaw 的 iflow 模型将无法使用。运行更新脚本即可恢复。

### Q: 可以提前更新吗？

A: 可以！随时运行 `iflow-update-key.sh` 更新，新 Key 的 7 天有效期从更新时刻开始计算。

### Q: Cron 任务不执行怎么办？

A: 检查 OpenClaw Gateway 状态：
```bash
openclaw gateway status
```

---

## 📞 获取帮助

```bash
~/.openclaw/workspace/scripts/iflow-key-manager.sh help
~/.openclaw/workspace/scripts/iflow-update-key.sh
```

---

**最后更新**: 2026-03-13  
**当前 Key 到期**: 2026-03-20
