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
