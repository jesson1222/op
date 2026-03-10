# 🔤 翻译功能配置指南

## 问题背景

之前使用的 Google 翻译 API 在中国大陆无法访问，导致翻译失败，推送的新闻标题显示为英文原文。

## 解决方案

改用**百度翻译 API**，国内访问稳定，免费额度充足。

---

## ⚠️ 重要：使用前必须完成以下步骤

### 1. 实名认证（必须）

百度翻译 API 要求实名认证才能使用：

1. 访问 https://fanyi-api.baidu.com/
2. 点击右上角「管理控制台」
3. 登录百度账号
4. 完成实名认证（需要手机号）

### 2. 开通通用翻译 API

1. 进入控制台后，点击左侧「我的服务」
2. 点击「开通服务」
3. 选择「通用文本翻译」（标准版）
4. 点击「立即开通」
5. 填写应用信息：
   - 应用名称：`新闻推送`（随意）
   - 应用描述：`RSS 新闻自动翻译`
   - QPS 限制：默认 1 即可

### 3. 获取密钥

开通后，在「我的服务」→「通用文本翻译」→「默认应用」中可以看到：
- **APP ID**：类似 `20240310000000001`
- **密钥 (APP KEY)**：类似 `abcdefgh123456789`

---

## 📋 当前配置状态

已配置：
- APP ID: `20260310002569431`
- APP KEY: `4BYpyDUBHCnF1OOJLp9v`

**如遇到错误 `52003 UNAUTHORIZED USER`，说明：**
1. ❌ 未完成实名认证
2. ❌ 未开通「通用文本翻译」服务
3. ❌ APP ID 或密钥填写错误

---

## ⚙️ 配置推送脚本

编辑 `config_feishu_app.yaml`：

```yaml
translate:
  enabled: true
  baidu_app_id: "你的 APP ID"
  baidu_app_key: "你的密钥"
```

示例：
```yaml
translate:
  enabled: true
  baidu_app_id: "20240310000000001"
  baidu_app_key: "abcdefgh123456789"
```

---

## 🧪 测试翻译

```bash
cd /Users/jesson/.openclaw/workspace/news-pusher
source venv/bin/activate
python3 -c "
from pusher_feishu_app import Translator
t = Translator('你的 APP ID', '你的密钥')
print(t.translate('How AI is changing the world', 'en', 'zh'))
"
```

预期输出：`AI 如何改变世界`（类似）

---

## 📊 免费额度

- **QPS**：1 次/秒
- **月额度**：200 万字符
- **实际使用**：每次推送约 500-1000 字符，每天推送 2 次，每月约 6 万字符

✅ 免费额度完全够用！

---

## 🔧 临时跳过翻译

如果暂时不想配置翻译，可以在 `config_feishu_app.yaml` 中设置：

```yaml
skip_translation: true
```

这样会直接推送英文原文（当前状态）。

---

## ❓ 常见问题

### Q: 错误 52003 UNAUTHORIZED USER
A: 需要完成实名认证并开通「通用文本翻译」服务。

### Q: 错误 54001 INVALID SIGN
A: 签名计算错误，检查 APP ID 和密钥是否正确，或是否有空格。

### Q: 翻译速度慢？
A: 百度翻译 API 响应通常在 1-3 秒，如果超时可能是网络问题。代码已设置 10 秒超时。

### Q: 翻译质量如何？
A: 百度翻译对新闻标题的翻译质量较好，基本可读。如有更高要求可考虑 DeepL（需付费）。
