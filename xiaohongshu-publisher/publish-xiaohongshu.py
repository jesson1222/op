#!/usr/bin/env python3
"""发布到小红书 - 使用 xiaohongshu-mcp 服务"""

import http.client
import json
import time

MCP_HOST = "localhost"
MCP_PORT = 18060

def create_session():
    """创建 MCP 会话"""
    conn = http.client.HTTPConnection(MCP_HOST, MCP_PORT, timeout=30)
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/event-stream'
    }
    
    # 1. 初始化
    init_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "clientInfo": {"name": "publish-script", "version": "1.0.0"}
        },
        "id": 1
    })
    
    print("🔄 初始化会话...")
    conn.request("POST", "/mcp", init_request, headers)
    response = conn.getresponse()
    init_result = json.loads(response.read().decode('utf-8'))
    print(f"初始化响应：{init_result.get('result', {}).get('serverInfo', {})}")
    
    # 2. 发送 initialized 通知（不能等待响应）
    print("📤 发送 initialized 通知...")
    notify_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    })
    conn.request("POST", "/mcp", notify_request, headers)
    time.sleep(0.5)  # 等待通知处理
    
    return conn, headers

def publish_content(conn, headers):
    """发布内容到小红书"""
    
    payload = {
        "title": "OpenClaw v2026.3.8 升级不适？",
        "content": """OpenClaw v2026.3.8 升级后不适？老用户带你快速上手！🦞

昨天升级完 v2026.3.8，我也懵了一下
配置好像变了，命令也不太一样了😅

花了一下午研究文档 + 测试，整理这份避坑指南
帮你 5 分钟搞定新系统！👇

🔥 升级后最大的 3 个变化

1️⃣ 备份功能上线（这个真的香！）
openclaw backup create
openclaw backup verify

2️⃣ macOS Token 保护
之前升级容易把 Token 搞丢，现在自动保留

3️⃣ TUI 自动识别工作区
进项目目录直接开用，不用手动配 agent

⚠️ 常见问题

Q: 配置不生效？
A: openclaw gateway restart

Q: 备份在哪？
A: ls ~/.openclaw/backups/

🎯 快速上手 4 步

1. 备份：openclaw backup create
2. 升级：npm install -g openclaw@latest
3. 重启：openclaw gateway restart
4. 测试：openclaw tui

💡 隐藏技巧

- Brave 搜索 LLM 模式
- 语音超时调整
- ACP 溯源调试

📍 资源指路
GitHub: @openclaw/openclaw
文档：docs.openclaw.ai

#OpenClaw #AI 工具 #开发者日常 #开源项目 #效率工具 #程序员 #技术分享""",
        "images": ["/Users/jesson/.openclaw/workspace/xiaohongshu-publisher/images/upgrade_guide_cover.jpg"],
        "tags": ["OpenClaw", "AI 工具", "开发者日常", "开源项目", "效率工具", "程序员", "技术分享"]
    }
    
    # 3. 调用发布工具
    publish_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "publish_content",
            "arguments": payload
        },
        "id": "publish-001"
    })
    
    print("\n🚀 正在发布到小红书...")
    print("=" * 60)
    print(f"标题：{payload['title']}")
    print(f"标签：{', '.join(payload['tags'])}")
    print("=" * 60)
    
    conn.request("POST", "/mcp", publish_request, headers)
    response = conn.getresponse()
    result = json.loads(response.read().decode('utf-8'))
    
    if 'result' in result:
        print("\n✅ 发布成功!")
        print(json.dumps(result['result'], indent=2, ensure_ascii=False))
        return True
    elif 'error' in result:
        print(f"\n❌ 发布失败：{result['error'].get('message')}")
        return False
    else:
        print(f"\n? 响应：{json.dumps(result, indent=2, ensure_ascii=False)}")
        return False

if __name__ == "__main__":
    try:
        conn, headers = create_session()
        success = publish_content(conn, headers)
        conn.close()
        
        if success:
            print("\n🎉 小红书笔记发布完成！")
        else:
            print("\n💡 提示：可以手动复制内容到小红书 App 发布")
            print("   文案：content/openclaw-upgrade-guide.md")
            print("   封面：images/upgrade_guide_cover.jpg")
    except Exception as e:
        print(f"\n❌ 请求失败：{e}")
        print("\n💡 提示：")
        print("1. 确保 xiaohongshu-mcp 容器正在运行：docker ps | grep xiaohongshu")
        print("2. 检查端口 18060：lsof -i :18060")
        print("3. 手动发布：复制内容到小红书 App")
