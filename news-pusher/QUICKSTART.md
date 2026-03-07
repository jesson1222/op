# 🚀 新闻推送系统 - 快速启动指南

## ✅ 已完成

- ✅ 创建项目目录和配置文件
- ✅ 配置 RSS 源（AI 科技/影视器材/摄影）
- ✅ 编写推送脚本
- ✅ 安装 Python 依赖

## 📝 下一步配置

### 1️⃣ 选择推送渠道

#### 方式 A：Telegram（推荐）

1. **创建 Bot**
   - 在 Telegram 搜索 `@BotFather`
   - 发送 `/newbot` 创建新机器人
   - 获取 Bot Token（类似：`123456789:ABCdefGHIjklMNOpqrsTUVwxyz`）

2. **创建频道**
   - 创建新频道（Channel）
   - 邀请你的 Bot 加入频道
   - 设置 Bot 为管理员（可发送消息）
   - 获取频道 ID（转发消息到 `@getidsbot` 或 `@RawDataBot`）

3. **填写配置**
   ```bash
   # 编辑配置文件
   vim config.yaml
   
   # 修改这两行：
   telegram:
     enabled: true
     bot_token: "你的 BOT_TOKEN"
     chat_id: "@你的频道名"  # 或数字 ID如 -1001234567890
   ```

#### 方式 B：飞书 webhook

1. **创建机器人**
   - 在飞书群组 → 右上角设置 → 添加机器人 → 自定义机器人
   - 获取 Webhook 地址

2. **填写配置**
   ```yaml
   feishu:
     enabled: true
     webhook_url: "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
   ```

### 2️⃣ 测试推送

```bash
cd /Users/jesson/.openclaw/workspace/news-pusher

# 激活虚拟环境
source venv/bin/activate

# 运行测试
python3 pusher.py
```

查看日志：
```bash
tail -f logs/pusher.log
```

### 3️⃣ 设置定时推送

#### 方式 A：使用 cron（推荐）

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每天早上 9 点推送）
0 9 * * * cd /Users/jesson/.openclaw/workspace/news-pusher && source venv/bin/activate && python3 pusher.py >> logs/cron.log 2>&1

# 或者使用提供的脚本
0 9 * * * /Users/jesson/.openclaw/workspace/news-pusher/cron.sh
```

#### 方式 B：使用 OpenClaw HEARTBEAT

编辑 `HEARTBEAT.md`，添加定时检查任务（适合每天 2-4 次）。

## 🎯 自定义配置

### 修改推送时间

编辑 `config.yaml`：
```yaml
schedule:
  times: ["09:00", "18:00"]  # 每天推送 2 次
  max_items_per_push: 10     # 每次最多 10 条
```

### 添加新的 RSS 源

在对应分类文件中添加：
```yaml
# feeds/ai.yaml
- name: 新的来源
  url: https://example.com/feed.xml
  category: AI
  language: zh
```

### 创建新分类

1. 创建 `feeds/your_category.yaml`
2. 在 `config.yaml` 中添加配置：
```yaml
feeds:
  your_category:
    path: feeds/your_category.yaml
    enabled: true
    title: "分类名称"
    emoji: "🎯"
```

## 📊 查看推送历史

```bash
# 查看已推送记录
cat logs/history.json

# 查看日志
tail -f logs/pusher.log
```

## 🛠️ 常见问题

### Q: 如何重置推送历史？
```bash
# 删除历史记录（会重新推送所有新闻）
rm logs/history.json
```

### Q: 推送失败怎么办？
1. 检查 Token/webhook 是否正确
2. 检查 Bot 是否有频道发送权限
3. 查看日志：`cat logs/pusher.log`
4. 测试 RSS 源：用浏览器打开 URL 看是否正常

### Q: 如何调整推送频率？
- cron: 修改 crontab 表达式
- HEARTBEAT: 编辑 `HEARTBEAT.md`

## 📞 需要帮助？

查看完整文档：`README.md`

---

**下一步：** 告诉我你选择的推送渠道（Telegram 或 飞书），我可以帮你进一步配置！
