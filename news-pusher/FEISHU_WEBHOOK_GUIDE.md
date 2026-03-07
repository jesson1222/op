# 📍 飞书 Webhook 获取指南

## 方法 1：自定义机器人（推荐）

### 步骤：

1. **打开飞书群组**
2. **点击右上角设置** (⚙️ 图标)
3. **找到「机器人」选项卡**
4. **点击「添加机器人」**
5. **选择「自定义机器人」**
6. **设置机器人名称**（如：新闻推送）
7. **复制 Webhook 地址** ⚠️ 只显示一次！

### Webhook 格式：
```
https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

---

## 方法 2：查看已有机器人

如果群组已有自定义机器人：

1. 群组设置 → 机器人
2. 点击已有机器人
3. 查看是否有 **「查看 Webhook」** 选项

⚠️ 注意：飞书出于安全考虑，Webhook 可能只显示一次，如果看不到需要重新创建。

---

## 方法 3：企业自建应用

如果是企业应用，需要：

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 进入「企业自建应用」
3. 创建应用 → 获取 App ID 和 App Secret
4. 使用 API 方式推送（已提供脚本：`test_feishu_api.py`）

---

## 快速验证

运行以下命令测试 webhook 是否有效：

```bash
cd ~/.openclaw/workspace/news-pusher

# 替换 YOUR_WEBHOOK_URL
./test_quick.sh "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK_URL"
```

如果收到消息，说明配置成功！

---

## 常见问题

### Q: 找不到「自定义机器人」选项？
A: 可能被管理员禁用，联系飞书管理员开启。

### Q: Webhook 地址无效？
A: 确认复制完整，没有多余空格。

### Q: 消息发送失败？
A: 检查机器人是否在群组中，是否有发送权限。
