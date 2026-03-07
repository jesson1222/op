#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书推送测试脚本
"""

import requests
import json

# ============ 请在此处填入你的飞书 webhook 地址 ============
WEBHOOK_URL = "PLEASE_FILL_WEBHOOK_HERE"
# ========================================================

def test_feishu_push():
    """测试飞书推送"""
    
    # 测试消息
    message = """
📰 新闻推送系统测试

这是一条测试消息，用于验证飞书机器人是否正常工作。

✅ 如果收到此消息，说明推送系统配置成功！

---
推送时间：2026-03-07 13:00
"""
    
    # 飞书文本消息格式
    payload = {
        "msg_type": "text",
        "content": {
            "text": message
        }
    }
    
    print(f"📤 正在发送测试消息到飞书...")
    print(f"Webhook: {WEBHOOK_URL}")
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        result = response.json()
        
        if response.status_code == 200 and result.get('StatusCode') == 0:
            print("\n✅ 飞书推送成功！")
            print("请检查飞书群组是否收到消息")
            return True
        else:
            print(f"\n❌ 飞书推送失败")
            print(f"状态码：{response.status_code}")
            print(f"返回结果：{json.dumps(result, ensure_ascii=False, indent=2)}")
            return False
            
    except Exception as e:
        print(f"\n❌ 推送异常：{e}")
        return False


def test_rich_message():
    """测试富文本消息（带链接）"""
    
    # 飞书交互式卡片 - 更美观的格式
    payload = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "template": "blue",
                "title": {
                    "tag": "plain_text",
                    "content": "📰 新闻推送测试"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "**这是一条测试消息**\n\n用于验证飞书机器人是否正常工作。\n\n✅ 如果收到此消息，说明推送系统配置成功！"
                    }
                },
                {
                    "tag": "hr"
                },
                {
                    "tag": "note",
                    "elements": [
                        {
                            "tag": "plain_text",
                            "content": "推送时间：2026-03-07 13:00"
                        }
                    ]
                }
            ]
        }
    }
    
    print(f"\n📤 正在发送富文本测试消息...")
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        result = response.json()
        
        if response.status_code == 200 and result.get('StatusCode') == 0:
            print("✅ 富文本消息发送成功！")
            return True
        else:
            print(f"❌ 富文本消息发送失败：{json.dumps(result, ensure_ascii=False)}")
            return False
            
    except Exception as e:
        print(f"❌ 推送异常：{e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("🧪 飞书推送测试工具")
    print("=" * 50)
    
    if WEBHOOK_URL == "PLEASE_FILL_WEBHOOK_HERE":
        print("\n⚠️ 请先在脚本中填入你的飞书 webhook 地址！")
        print("\n获取方式：")
        print("1. 打开飞书群组 → 右上角设置")
        print("2. 找到「自定义机器人」")
        print("3. 复制 Webhook 地址")
        print("\n然后编辑此文件，替换 WEBHOOK_URL 的值")
        exit(1)
    
    # 测试简单文本消息
    success = test_feishu_push()
    
    if success:
        # 测试富文本消息
        test_rich_message()
    
    print("\n" + "=" * 50)
