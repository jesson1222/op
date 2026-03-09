# 小红书登录备用方案

如果扫码登录失败，请用以下方法：

## 方法 1：浏览器登录（推荐）

1. 打开 https://creator.xiaohongshu.com
2. 用手机小红书 APP 扫码登录
3. 登录成功后，按 F12 打开开发者工具
4. 去 Application → Cookies → https://creator.xiaohongshu.com
5. 右键 → Export All → JSON
6. 保存为 `data/xiaohongshu_cookies.json`

## 方法 2：使用登录脚本

```bash
cd /Users/jesson/.openclaw/workspace/xiaohongshu-publisher
python3 login-local.py
```

这会弹出浏览器窗口，扫码登录后自动保存 Cookie。

## 方法 3：手动复制 Cookie

登录成功后，在开发者工具 Console 中运行：

```javascript
document.cookie.split(';').map(c => c.trim()).forEach(c => {
  const [name, value] = c.split('=');
  console.log(`${name}: ${value}`);
});
```

然后告诉我 Cookie 内容，我帮你转换格式。
