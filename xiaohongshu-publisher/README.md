# 📕 小红书全自动发布工具

基于 Docker + Playwright 的小红书自动化发布方案，**登录一次，永久自动**。

---

## 🚀 快速开始

### 1. 准备图片

将要发布的图片放入 `images/` 目录：

```bash
mkdir -p images
cp /path/to/cooke-photos/*.jpg images/
```

**要求**：
- 格式：JPG 或 PNG
- 数量：6-9 张
- 尺寸：建议 3:4 或 4:5 竖屏
- 大小：单张 < 10MB

### 2. 首次运行（登录并保存 Cookie）

```bash
cd xiaohongshu-publisher

# 构建并运行
docker-compose up --build
```

**此时会弹出浏览器窗口**：
1. 用手机小红书 APP 扫码登录
2. 登录成功后会自动保存 Cookie
3. 浏览器自动关闭

### 3. 后续运行（全自动发布）

```bash
# 直接运行，自动发布
docker-compose up
```

**无需重复登录！** Cookie 已保存在 `data/` 目录。

---

## 📁 目录结构

```
xiaohongshu-publisher/
├── docker-compose.yml    # Docker 配置
├── Dockerfile            # 容器镜像
├── publish.py            # 发布脚本
├── cookie_manager.py     # Cookie 管理
├── requirements.txt      # Python 依赖
├── data/                 # Cookie 存储（自动创建）
│   └── xiaohongshu_cookies.json
└── images/               # 待发布图片（手动放入）
    ├── image1.jpg
    ├── image2.jpg
    └── ...
```

---

## ⚙️ 配置发布内容

编辑 `publish.py` 中的 `PUBLISH_CONFIG`：

```python
PUBLISH_CONFIG = {
    "title": "你的标题",
    "content": "你的正文内容",
    "tags": ["标签 1", "标签 2", ...]
}
```

---

## 🔄 定时发布（Cron）

添加 Crontab 任务：

```bash
crontab -e

# 每天晚上 8 点发布
0 20 * * * cd /Users/jesson/.openclaw/workspace/xiaohongshu-publisher && docker-compose up
```

---

## 🛠️ 常见问题

### Cookie 过期了怎么办？

删除 Cookie 文件，重新登录：

```bash
rm data/xiaohongshu_cookies.json
docker-compose up --build
```

### 发布失败？

检查日志：

```bash
docker-compose logs
```

查看调试截图：

```bash
ls -la data/*.png
```

### 如何在后台运行？

```bash
docker-compose up -d
docker-compose logs -f
```

---

## 📊 发布流程

```
1. 加载 Cookie → 验证登录态
2. 打开创作者平台 → 点击发布
3. 上传图片 → 填写标题 → 填写正文
4. 添加标签 → 点击发布 → 完成
```

全程约 30-60 秒。

---

## 🔒 安全说明

- Cookie 仅保存在本地 `data/` 目录
- 不会上传到任何第三方服务器
- 建议定期更新 Cookie（每月重新登录一次）

---

## 📝 注意事项

1. **首次运行必须手动登录**（扫码）
2. **图片需提前放入 `images/` 目录**
3. **发布前请确认内容符合小红书规范**
4. **建议先在测试账号验证流程**

---

**祝你发布顺利！🎉**
