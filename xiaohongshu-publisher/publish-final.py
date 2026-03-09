#!/usr/bin/env python3
"""发布到小红书 - 最终版本（使用 MCP 协议）"""

import requests
import json

MCP_URL = "http://localhost:18060/mcp"

def publish_to_xiaohongshu():
    """发布内容到小红书"""
    
    session = requests.Session()
    
    # 准备发布内容
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
        "images": [
            "/Users/jesson/.openclaw/workspace/xiaohongshu-publisher/images/xiaohongshu_p1.jpg",
            "/Users/jesson/.openclaw/workspace/xiaohongshu-publisher/images/xiaohongshu_p2.jpg",
            "/Users/jesson/.openclaw/workspace/xiaohongshu-publisher/images/xiaohongshu_p3.jpg",
            "/Users/jesson/.openclaw/workspace/xiaohongshu-publisher/images/xiaohongshu_p4.jpg",
            "/Users/jesson/.openclaw/workspace/xiaohongshu-publisher/images/xiaohongshu_p5.jpg"
        ],
        "tags": ["OpenClaw", "AI 工具", "开发者日常", "开源项目", "效率工具", "程序员", "技术分享"]
    }
    
    print("🚀 开始发布到小红书...")
    print("=" * 60)
    print(f"标题：{payload['title']}")
    print(f"图片数：{len(payload['images'])}")
    print(f"标签数：{len(payload['tags'])}")
    print("=" * 60)
    
    try:
        # 使用 batch 请求（MCP 协议要求）
        batch_request = [
            {
                "jsonrpc": "2.0",
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "clientInfo": {"name": "publish-script", "version": "1.0.0"}
                },
                "id": 1
            },
            {
                "jsonrpc": "2.0",
                "method": "notifications/initialized"
            },
            {
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "publish_content",
                    "arguments": payload
                },
                "id": 100
            }
        ]
        
        # 发送请求（增加超时时间）
        response = session.post(MCP_URL, json=batch_request, timeout=120)
        
        print(f"\n📊 响应状态：{response.status_code}")
        
        results = response.json()
        
        for item in results:
            if item.get('id') == 100:
                if 'result' in item:
                    print("\n✅ 发布成功!")
                    print(json.dumps(item['result'], indent=2, ensure_ascii=False))
                    return True
                elif 'error' in item:
                    error_msg = item['error'].get('message', 'Unknown error')
                    print(f"\n❌ 发布失败：{error_msg}")
                    print("\n💡 错误分析:")
                    if "invalid during session initialization" in error_msg:
                        print("   - MCP 会话初始化问题")
                    elif "timeout" in error_msg.lower():
                        print("   - 请求超时，网络或服务器问题")
                    else:
                        print(f"   - {error_msg}")
                    return False
        
        return False
        
    except requests.exceptions.Timeout:
        print("\n❌ 请求超时（120 秒）")
        print("\n💡 可能原因:")
        print("   1. 小红书 API 响应慢")
        print("   2. 网络连接问题")
        print("   3. MCP 服务处理中")
        return False
    except Exception as e:
        print(f"\n❌ 请求失败：{e}")
        return False

if __name__ == "__main__":
    success = publish_to_xiaohongshu()
    
    if success:
        print("\n🎉 小红书笔记发布完成！")
    else:
        print("\n" + "=" * 60)
        print("💡 发布失败，可以手动发布:")
        print("=" * 60)
        print("1. 打开小红书 App")
        print("2. 选择图片:")
        print("   images/xiaohongshu_p1.jpg ~ p5.jpg")
        print("3. 复制文案:")
        print("   cat content/openclaw-upgrade-guide.md | pbcopy")
        print("4. 添加标签并发布")
