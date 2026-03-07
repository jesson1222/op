# OpenClaw 代理配置指南

## 方案：仅海外流量走代理 (127.0.0.1:9674)

### 1. 设置环境变量（推荐）
在 `~/.zshrc` 中添加：
```bash
# 全局代理设置
export http_proxy=http://127.0.0.1:9674
export https_proxy=http://127.0.0.1:9674

# 关键直连例外（飞书/国内域名）
export NO_PROXY="localhost,127.0.0.1,.feishu.cn,.larksuite.com,.cn,.baidu.com,.qq.com"
```

### 2. 应用配置
```bash
source ~/.zshrc
```

### 3. 验证
```bash
# 检查代理状态
echo $http_proxy
echo $NO_PROXY

# 测试飞书直连
curl -I https://open.feishu.cn

# 测试海外代理
curl -I https://google.com
```