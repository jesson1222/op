#!/usr/bin/env python3
"""通过 MCP HTTP API 发布小红书内容"""

import requests
import json

MCP_URL = "http://localhost:18060/mcp"

session = requests.Session()
session.headers.update({"Content-Type": "application/json"})

# 使用 batch 请求：初始化 + initialized 通知 + 工具调用
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
            "arguments": {
                "title": "Cooke 镜头 | 好莱坞光学传奇",
                "content": "100 多年来，Cooke 镜头几乎拍摄了所有好莱坞经典电影！\nCooke 镜头是好莱坞摄影师的首选🎥\n\n✨ Cooke Look 的 5 大秘密：\n1️⃣ 温暖色调\n2️⃣ 柔和对比度\n3️⃣ 奶油般散景\n4️⃣ 超低色差\n5️⃣ 呼吸效应控制\n\n🎬 好摄影师能让好镜头发光✨\n\n👇 你用过 Cooke 镜头吗？",
                "images": [
                    "/app/images/Panchro65_resized.jpg",
                    "/app/images/S4i_resized.jpg",
                    "/app/images/S8iFF_resized.jpg",
                    "/app/images/SP3_resized.jpg"
                ],
                "tags": ["Cooke 镜头", "电影镜头", "摄影器材", "好莱坞", "摄影师"]
            }
        },
        "id": 100
    }
]

resp = session.post(MCP_URL, json=batch_request)
print("响应:", resp.status_code)

for item in resp.json():
    if item.get('id') == 100:
        if 'result' in item:
            print("\n✅ 发布成功!")
            print(json.dumps(item['result'], indent=2, ensure_ascii=False))
        elif 'error' in item:
            print("\n❌ 发布失败:", item['error'].get('message'))
        else:
            print("\n?", json.dumps(item, indent=2, ensure_ascii=False))
