# 📰 新闻推送系统

每天定时推送行业资讯，支持定制分类。

## 📂 目录结构

```
news-pusher/
├── README.md           # 本文件
├── config.yaml         # 配置文件（RSS 源 + 推送设置）
├── feeds/              # RSS 源列表
│   ├── ai.yaml         # AI 科技类
│   ├── camera.yaml     # 影视器材类
│   └── photography.yaml # 摄影类
├── pusher.py           # 推送脚本
└── cron.sh             # 定时任务脚本
```

## 🚀 快速开始

### 方式一：Telegram Bot（推荐）

1. 在 Telegram 搜索 `@BotFather`，创建新 Bot，获取 Token
2. 创建一个频道或群组，邀请 Bot 加入并设为管理员
3. 获取频道 ID（转发一条消息到 `@getidsbot`）
4. 编辑 `config.yaml`，填入 Token 和频道 ID
5. 运行 `python3 pusher.py` 测试

### 方式二：飞书企业应用（推荐）

使用飞书开放平台的企业自建应用，更稳定可靠：

1. **配置应用**
   ```bash
   cd /Users/jesson/.openclaw/workspace/news-pusher
   ./setup_feishu_app.sh
   ```
   按提示输入 App ID、App Secret 和群组 ID

2. **或手动配置**
   - 编辑 `config_feishu_app.yaml`
   - 填入从飞书开放平台获取的凭证
   - 详见：`FEISHU_APP_GUIDE.md`

3. **测试推送**
   ```bash
   source venv/bin/activate
   python3 pusher_feishu_app.py test
   ```

4. **正式推送**
   ```bash
   python3 pusher_feishu_app.py
   ```

### 方式三：飞书 webhook（自定义机器人）

1. 在飞书群组添加「自定义机器人」
2. 获取 Webhook 地址
3. 编辑 `config.yaml`，填入 webhook URL
4. 运行测试：`./test_quick.sh "YOUR_WEBHOOK_URL"`

### 方式三：RSS-to-Telegram-Bot（免代码）

使用现成的开源项目：
- [iovxw/rssbot](https://github.com/iovxw/rssbot) - 轻量级
- [Rongronggg9/RSS-to-Telegram-Bot](https://github.com/Rongronggg9/RSS-to-Telegram-Bot) - 功能丰富

```bash
# Docker 部署 rssbot
docker run -d \
  --name rssbot \
  -v $(pwd)/rssbot.json:/app/rssbot.json \
  iovxw/rssbot \
  <your-telegram-bot-token>
```

## ⏰ 定时任务

### macOS/Linux (cron)

```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每天早上 9 点推送）
0 9 * * * cd ~/.openclaw/workspace/news-pusher && python3 pusher.py >> logs/pusher.log 2>&1
```

### 使用 HEARTBEAT（OpenClaw 内置）

在 `HEARTBEAT.md` 中添加检查任务，由 OpenClaw 定期执行。

## 📋 配置说明

编辑 `config.yaml`：

```yaml
# Telegram 配置
telegram:
  bot_token: "YOUR_BOT_TOKEN"
  chat_id: "@your_channel"  # 或数字 ID

# 飞书配置
feishu:
  webhook_url: "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"

# 推送时间
schedule:
  timezone: "Asia/Shanghai"
  times: ["09:00", "18:00"]  # 每天推送 2 次

# RSS 源分类
feeds:
  ai: feeds/ai.yaml
  camera: feeds/camera.yaml
  photography: feeds/photography.yaml
```

## 🔧 自定义分类

在 `feeds/` 目录下创建新的 YAML 文件：

```yaml
# feeds/your_category.yaml
- name: 来源名称
  url: https://example.com/feed.xml
  category: 分类标签
  filter:  # 可选：关键词过滤
    include: ["AI", "新闻"]
    exclude: ["广告", "推广"]
```

## 📝 日志查看

```bash
# 查看推送日志
tail -f logs/pusher.log

# 查看历史记录
cat logs/history.json
```

## 🛡️ 注意事项

1. **频率控制**：避免推送过于频繁（建议每天 1-2 次）
2. **内容过滤**：使用 `filter` 字段排除无关内容
3. **错误处理**：失败的 RSS 源会记录到日志，不影响其他源
4. **隐私保护**：Token 和 webhook 不要提交到公开仓库

## 📞 问题反馈

遇到问题查看日志或检查：
- RSS 源是否有效（用浏览器打开 URL 测试）
- Bot 权限是否正确
- 网络连接是否正常
