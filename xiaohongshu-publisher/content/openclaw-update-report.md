# OpenClaw 2026.3.8 更新报告 🦞

## 🎯 核心亮点

**一句话总结：** 你的私人 AI 助手变得更强大、更安全、更好用了！

---

## 📦 8 大重磅更新

### 1️⃣ 备份功能上线 🔒
- `openclaw backup create` - 一键备份所有配置和会话
- `openclaw backup verify` - 验证备份完整性
- 支持仅备份配置/排除工作区
- 再也不用担心数据丢失了！

### 2️⃣ macOS 远程网关增强 🍎
- 新增远程网关 Token 字段
- 保护现有 Token 不被意外覆盖
- Token 形状警告提示
- 远程模式更安全

### 3️⃣ 语音对话模式优化 🎙️
- 可配置静音超时时间 (`talk.silenceTimeoutMs`)
- 自动检测语音停顿并发送
- 每个平台保持默认暂停窗口
- 对话更流畅自然

### 4️⃣ TUI 智能感知 💻
- 自动检测当前工作区的 agent
- 保留显式 session 目标
- 启动即用，无需手动配置
- 开发效率 UP！

### 5️⃣ Brave 搜索升级 🔍
- 新增 `llm-context` 模式
- 返回带来源的摘要片段
- 更适合 AI 理解的网络搜索
- 搜索结果质量大幅提升

### 6️⃣ 版本信息完善 📋
- `openclaw --version` 显示 Git commit hash
- 安装程序版本检查兼容
- 问题排查更方便

### 7️⃣ ACP 溯源功能 🔗
- 可选的 ACP ingress 溯源元数据
- 可见的 receipt 注入
- 支持 session trace ID
- 调试和审计更轻松

### 8️⃣ 其他改进 ✨
- 备份命名优化（日期排序友好）
- 仅配置备份模式
- 边缘情况处理强化
- 文档和测试覆盖提升

---

## 🚀 如何升级

```bash
# 更新到最新版本
npm install -g openclaw@latest

# 查看版本
openclaw --version

# 创建备份（升级前建议）
openclaw backup create
```

---

## 💡 使用建议

1. **升级前先备份** - 避免配置丢失
2. **检查远程 Token** - macOS 用户注意
3. **尝试语音模式** - 配置静音超时
4. **体验新搜索** - Brave LLM 模式

---

## 📊 版本信息

- **最新版本：** v2026.3.8
- **发布时间：** 2026-03-09
- **许可证：** MIT
- **GitHub：** @openclaw/openclaw

---

## 🎁 彩蛋

这次更新感谢了 7 位贡献者：
@shichangs, @cgdusek, @danodoesdesign, @arceus77-7, @thirumaleshp, @sourman, @gumadeiras, @mbelinky

开源社区的力量！💪

---

#OpenClaw #AI 助手 #开源项目 #开发者工具 #自动化 #AI
