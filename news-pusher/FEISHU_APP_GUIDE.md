# 📘 飞书企业应用配置指南

## 📋 完整配置流程

### 步骤 1：创建企业自建应用

1. **访问飞书开放平台**
   - 网址：https://open.feishu.cn/
   - 使用企业管理员账号登录

2. **创建应用**
   - 点击左侧 **「企业自建应用」**
   - 点击 **「创建应用」**
   - 填写应用信息：
     - 应用名称：新闻推送助手
     - 应用图标：可选
   - 点击 **「创建」**

---

### 步骤 2：获取应用凭证

1. **进入应用管理页面**
   - 点击创建好的应用

2. **查看凭证**
   - 点击左侧 **「凭证与基础信息」**
   - 复制以下信息：
     - **App ID** (格式：`cli_xxxxxxxxxxxxx`)
     - **App Secret** (点击「查看」按钮显示)

   ⚠️ **重要：** App Secret 只显示一次，请妥善保存！

---

### 步骤 3：配置应用权限

1. **添加权限**
   - 点击左侧 **「权限管理」**
   - 点击 **「申请权限」**

2. **搜索并添加以下权限：**
   - `im:message` - 发送消息
   - `im:chat` - 获取群组信息
   
3. **提交申请**
   - 点击 **「提交申请」**
   - 等待管理员审批（通常立即生效）

---

### 步骤 4：获取群组 ID (chat_id)

#### 方法 A：从飞书 URL 获取（推荐）

1. **打开飞书客户端**
2. **进入目标群组**
3. **查看 URL**
   - 在浏览器中打开群组链接
   - URL 格式：`https://applink.feishu.cn/client/chat/oc_xxxxxxxxxx`
   - `oc_xxxxxxxxxx` 就是群组 ID

#### 方法 B：使用 API 获取

运行以下命令获取群组列表：

```bash
cd ~/.openclaw/workspace/news-pusher
source venv/bin/activate

# 先配置好 config_feishu_app.yaml
python3 -c "
from pusher_feishu_app import FeishuAPI
import yaml

with open('config_feishu_app.yaml') as f:
    config = yaml.safe_load(f)

feishu = FeishuAPI(config['feishu_app']['app_id'], config['feishu_app']['app_secret'])

# 获取群组信息
chat_id = 'oc_xxxxxxxxxx'  # 替换为你的群组 ID
info = feishu.get_chat_info(chat_id)
print(f'群组名称：{info.get(\"name\")}')
print(f'群组 ID: {chat_id}')
"
```

---

### 步骤 5：配置文件

编辑 `config_feishu_app.yaml`：

```yaml
# 飞书开放平台配置
feishu_app:
  app_id: "cli_xxxxxxxxxxxxx"        # 替换为你的 App ID
  app_secret: "xxxxxxxxxxxxxxxx"      # 替换为你的 App Secret
  chat_id: "oc_xxxxxxxxxxxxx"         # 替换为你的群组 ID
```

---

### 步骤 6：测试推送

```bash
cd ~/.openclaw/workspace/news-pusher
source venv/bin/activate

# 运行测试
python3 pusher_feishu_app.py test
```

如果看到以下输出，说明配置成功：

```
✅ Token 获取成功
✅ 群组信息获取成功：群组名称
📤 正在发送测试消息...
✅ 消息发送成功！
```

---

### 步骤 7：正式推送

```bash
# 运行新闻推送
python3 pusher_feishu_app.py
```

---

## ⚙️ 定时推送配置

### 方式 A：使用 cron

```bash
crontab -e

# 每天早上 9 点推送
0 9 * * * cd ~/.openclaw/workspace/news-pusher && source venv/bin/activate && python3 pusher_feishu_app.py >> logs/pusher.log 2>&1
```

### 方式 B：使用 OpenClaw HEARTBEAT

编辑 `HEARTBEAT.md`，添加定时检查任务。

---

## 🔧 常见问题

### Q1: 获取 token 失败
**可能原因：**
- App ID 或 App Secret 错误
- 应用权限未审批

**解决方案：**
- 检查凭证是否正确复制
- 确认权限已审批通过

---

### Q2: 发送消息失败
**可能原因：**
- chat_id 错误
- 机器人未加入群组
- 权限不足

**解决方案：**
- 检查群组 ID 格式（应该是 `oc_` 开头）
- 确保应用有发送消息权限

---

### Q3: 找不到群组 ID
**解决方案：**
- 在飞书网页版打开群组，URL 中包含群组 ID
- 或联系飞书管理员获取

---

## 📝 配置检查清单

- [ ] 已创建企业自建应用
- [ ] 已获取 App ID
- [ ] 已获取 App Secret
- [ ] 已申请 `im:message` 权限
- [ ] 已申请 `im:chat` 权限
- [ ] 权限已审批通过
- [ ] 已获取群组 ID
- [ ] 已编辑 `config_feishu_app.yaml`
- [ ] 测试推送成功

---

## 🆘 需要帮助？

如果遇到问题，提供以下信息：

1. 错误信息截图
2. App ID（隐藏敏感部分）
3. 配置文件的 `feishu_app` 部分（隐藏 Secret）

---

**配置完成后，运行 `python3 pusher_feishu_app.py test` 测试！** 🚀
