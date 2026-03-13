# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.

---

## 📰 新闻推送检查

每天检查 2-3 次新闻推送状态：

- [ ] 早上 09:00 - 推送早间新闻
- [ ] 下午 18:00 - 推送晚间新闻（可选）

**检查项：**
1. 推送脚本是否正常运行
2. logs/pusher.log 是否有错误
3. 是否需要补充新的 RSS 源

**推送渠道：** Telegram / 飞书（待配置）

**配置位置：** `news-pusher/config.yaml`

---

## 🧠 自学习检查

每次 heartbeat 时检查：

- [ ] 是否有新的错误需要记录到 `.learnings/ERRORS.md`
- [ ] 是否有用户纠正需要记录到 `.learnings/LEARNINGS.md`
- [ ] 是否有待解决的 learning 需要处理
- [ ] 是否有可以提升到 MEMORY.md 的学习内容

**检查命令：**
```bash
# 查看待处理的 learnings
grep -h "Status\*\*: pending" ~/.openclaw/workspace/.learnings/*.md | wc -l

# 查看高优先级的 errors
grep -B5 "Priority\*\*: high" ~/.openclaw/workspace/.learnings/ERRORS.md
```

---

## 🔑 iFlow 认证状态

**认证方式**: OAuth (通过 iFlow 登录)

**优势**: 
- ✅ Token 自动续期，无需手动管理
- ✅ 享受完整功能（WebSearch、WebFetch、多模态）
- ✅ 无需担心 API Key 过期

**检查项**:
- [ ] iFlow CLI 是否正常工作
- [ ] 测试命令：`iflow -p "test"`

**重新认证方法**（如需要）:
1. 运行 `iflow` 进入交互模式
2. 选择 "Login with iFlow"
3. 浏览器自动打开并完成登录
