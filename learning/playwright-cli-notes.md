# Agent Browser / Playwright CLI 学习笔记

## 📚 技能信息

**技能名称**: playwright-cli  
**来源**: OpenClaw Skills  
**核心功能**: 自动化浏览器控制

---

## 🎯 核心功能

### 主要能力

1. **页面控制**
   - 打开网页
   - 导航跳转
   - 标签页管理
   - 会话保持

2. **元素交互**
   - 点击 (click)
   - 输入 (type/fill)
   - 选择 (select)
   - 悬停 (hover)

3. **截图录制**
   - 页面截图
   - PDF 导出
   - Trace 录制
   - 网络/控制台日志

4. **会话管理**
   - 命名会话 (--session)
   - Cookie 持久化
   - 用户数据隔离
   - 并行场景

---

## 🔧 技术架构

### 底层引擎

```
OpenClaw Browser
    ↓
Playwright CDP Control Engine
    ↓
Browser (Chromium/Firefox/WebKit)
```

### 两种模式

**1. OpenClaw-managed Browser**
```bash
browser action=open profile="openclaw"
```

**2. Chrome Extension Relay**
```bash
browser action=open profile="chrome"
# 需要用户点击浏览器扩展图标
```

---

## 💻 使用方式

### 安装命令

```bash
npx playbooks add skill openclaw/skills --skill playwright-cli
```

### 基本用法

```bash
# 打开页面
playwright-cli open https://example.com

# 截图
playwright-cli screenshot --output page.png

# 点击元素
playwright-cli click --selector "#login-btn"

# 填写表单
playwright-cli fill --selector "#username" --value "user"
playwright-cli fill --selector "#password" --value "pass"

# 提交表单
playwright-cli press --key "Enter"
```

### 会话管理

```bash
# 创建命名会话
playwright-cli open https://example.com --session my-session

# 使用已有会话
playwright-cli click --selector "#btn" --session my-session

# 会话数据持久化（Cookie、LocalStorage 等）
```

---

## ⚙️ 配置选项

### 环境变量

```bash
# 浏览器类型
PLAYWRIGHT_MCP_BROWSER=chromium  # chromium, firefox, webkit, edge

# 允许的主机（安全限制）
PLAYWRIGHT_MCP_ALLOWED_HOSTS=example.com,api.example.com

# 输出目录
PLAYWRIGHT_MCP_OUTPUT_DIR=./output

# 无头模式
PLAYWRIGHT_MCP_HEADLESS=true  # true/false
```

### 命令行参数

```bash
# 浏览器类型
--browser chromium

# 无头模式
--headless

# 会话名称
--session my-session

# 输出目录
--output-dir ./screenshots

# 允许的主机
--allowed-hosts example.com
```

---

## 📊 最佳实践

### 1. 使用会话隔离

```bash
# ✅ 好：每个场景独立会话
playwright-cli open page1 --session scenario-1
playwright-cli open page2 --session scenario-2

# ❌ 不好：共享会话可能导致冲突
playwright-cli open page1
playwright-cli open page2
```

### 2. 设置主机限制

```bash
# 安全：限制访问范围
export PLAYWRIGHT_MCP_ALLOWED_HOSTS=example.com,api.example.com

# 不安全：无限制
# export PLAYWRIGHT_MCP_ALLOWED_HOSTS=*
```

### 3. 使用元素引用

```bash
# ✅ 好：使用稳定的选择器
playwright-cli click --selector "data-testid=submit-btn"

# ❌ 不好：使用易变的选择器
playwright-cli click --selector ".btn.btn-primary.mt-3"
```

### 4. 配置输出目录

```bash
# CI/CD 场景：统一输出位置
export PLAYWRIGHT_MCP_OUTPUT_DIR=./ci-artifacts

# 自动保存截图、PDF、Trace
```

### 5. 选择合适模式

```bash
# 调试：有头模式
playwright-cli open --headless=false

# CI：无头模式（节省资源）
playwright-cli open --headless=true
```

---

## 🎯 使用场景

### 场景 1: 自动化测试

```bash
# 打开登录页面
playwright-cli open https://app.example.com/login

# 填写表单
playwright-cli fill --selector "#email" --value "test@example.com"
playwright-cli fill --selector "#password" --value "password123"

# 提交
playwright-cli click --selector "button[type=submit]"

# 验证（截图）
playwright-cli screenshot --output login-success.png
```

### 场景 2: 数据抓取

```bash
# 导航到目标页面
playwright-cli open https://example.com/products

# 执行 JS 提取数据
playwright-cli eval --script "
  const products = document.querySelectorAll('.product');
  return Array.from(products).map(p => ({
    name: p.querySelector('.name').textContent,
    price: p.querySelector('.price').textContent
  }));
"

# 保存结果
```

### 场景 3: CI/CD 流水线

```yaml
# GitHub Actions 示例
- name: Run Browser Tests
  run: |
    npm install -g playwright-cli
    playwright-cli open https://staging.example.com --headless
    playwright-cli screenshot --output ci-artifacts/homepage.png
    playwright-cli click --selector "#signup-btn"
    playwright-cli screenshot --output ci-artifacts/signup.png

- name: Upload Artifacts
  uses: actions/upload-artifact@v3
  with:
    name: browser-screenshots
    path: ci-artifacts/
```

### 场景 4: 调试生产问题

```bash
# 开启控制台和网络日志
playwright-cli open https://prod.example.com \
  --console-log \
  --network-log

# 复现问题
playwright-cli click --selector "#problematic-btn"

# 查看日志定位问题
```

### 场景 5: PDF 导出

```bash
# 导出页面为 PDF
playwright-cli pdf --output report.pdf

# 自定义选项
playwright-cli pdf \
  --output report.pdf \
  --paper-format A4 \
  --print-background
```

---

## 📚 支持浏览器

| 浏览器 | 环境变量值 | 说明 |
|--------|-----------|------|
| Chromium | `chromium` | 默认，Chrome 内核 |
| Firefox | `firefox` | Mozilla Firefox |
| WebKit | `webkit` | Safari 内核 |
| Edge | `edge` | Microsoft Edge |

---

## 🔒 安全考虑

### 主机限制

```bash
# 白名单模式
export PLAYWRIGHT_MCP_ALLOWED_HOSTS="example.com,api.example.com"

# 支持通配符
export PLAYWRIGHT_MCP_ALLOWED_HOSTS="*.example.com"

# 拒绝访问不在白名单的主机
playwright-cli open https://malicious.com
# ❌ 会被阻止
```

### 会话隔离

```bash
# 不同用户使用不同会话
playwright-cli open --session user-A
playwright-cli open --session user-B

# 避免 Cookie 泄露
```

### 权限控制

```bash
# 限制危险操作
# - 文件下载
# - 文件系统访问
# - 剪贴板访问

# 通过 ALLOWED_HOSTS 间接控制
```

---

## 🛠️ 高级功能

### Trace 录制

```bash
# 开始录制 Trace
playwright-cli trace start --output trace.zip

# 执行操作
playwright-cli click --selector "#btn"
playwright-cli fill --selector "#input" --value "test"

# 停止录制
playwright-cli trace stop

# 查看 Trace（Playwright Trace Viewer）
```

### 网络拦截

```bash
# 监听网络请求
playwright-cli network-log --output network.json

# 拦截修改请求（高级）
playwright-cli eval --script "
  page.route('**/api/*', route => {
    route.continue({
      headers: { ...route.request().headers(), 'X-Custom': 'value' }
    });
  });
"
```

### 控制台日志

```bash
# 实时流式输出
playwright-cli console-log

# 保存到文件
playwright-cli console-log --output console.txt
```

---

## 📊 性能优化

### 并行执行

```bash
# 使用不同会话并行运行
playwright-cli open page1 --session s1 &
playwright-cli open page2 --session s2 &
playwright-cli open page3 --session s3 &
wait
```

### 资源节省

```bash
# 无头模式（节省 CPU/内存）
--headless

# 禁用图片加载（更快）
--block-resources=images

# 单进程模式（节省内存）
--single-process
```

### 缓存利用

```bash
# 使用持久会话（复用 Cookie/Cache）
--session cached-session

# 预加载页面
playwright-cli prefetch https://example.com
```

---

## 🎓 学习资源

- **官方文档**: https://docs.openclaw.ai/tools/browser
- **Playwright 文档**: https://playwright.dev
- **技能市场**: https://playbooks.com/skills/openclaw/skills/playwright-cli
- **GitHub**: https://github.com/openclaw/skills

---

## 🎯 明日计划

### 安装步骤

1. **安装技能**
   ```bash
   npx playbooks add skill openclaw/skills --skill playwright-cli
   ```

2. **配置环境**
   ```bash
   export PLAYWRIGHT_MCP_BROWSER=chromium
   export PLAYWRIGHT_MCP_HEADLESS=true
   export PLAYWRIGHT_MCP_OUTPUT_DIR=./browser-output
   ```

3. **测试基本功能**
   ```bash
   playwright-cli open https://example.com
   playwright-cli screenshot --output test.png
   ```

4. **创建使用示例**
   - 自动化测试示例
   - 数据抓取示例
   - CI/CD集成示例

---

*学习时间：2026-03-06 02:30 AM*
*来源：Playwright CLI Skill*
