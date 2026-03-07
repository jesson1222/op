#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书 API 推送脚本（无需 Webhook，使用 App ID + App Secret）
适用于企业自建应用
"""

import requests
import time
import hashlib
import base64
import json

# ============ 配置区域 ============
APP_ID = "cli_xxxxxxxxxxxxx"      # 飞书应用 App ID
APP_SECRET = "xxxxxxxxxxxxxxxx"    # 飞书应用 App Secret
CHAT_ID = "oc_xxxxxxxxxxxxx"       # 群组 ID 或 用户 ID
# =================================

class FeishuAPI:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.base_url = "https://open.feishu.cn/open-apis"
        self.token = None
        self.token_expire = 0
    
    def get_tenant_token(self):
        """获取应用访问令牌"""
        if self.token and time.time() < self.token_expire:
            return self.token
        
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        
        if result.get('code') == 0:
            self.token = result['tenant_access_token']
            self.token_expire = time.time() + result['expire'] - 60
            return self.token
        else:
            raise Exception(f"获取 token 失败：{result}")
    
    def send_text_message(self, chat_id, text):
        """发送文本消息"""
        token = self.get_tenant_token()
        
        url = f"{self.base_url}/im/v1/messages"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "receive_id": chat_id,
            "msg_type": "text",
            "content": json.dumps({"text": text})
        }
        
        params = {"receive_id_type": "chat_id"}  # 或 user_id
        
        response = requests.post(url, headers=headers, json=payload, params=params, timeout=10)
        result = response.json()
        
        if result.get('code') == 0:
            print("✅ 消息发送成功！")
            return True
        else:
            print(f"❌ 发送失败：{result}")
            return False
    
    def send_interactive_message(self, chat_id, card_config):
        """发送交互式卡片消息"""
        token = self.get_tenant_token()
        
        url = f"{self.base_url}/im/v1/messages"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "receive_id": chat_id,
            "msg_type": "interactive",
            "content": json.dumps(card_config)
        }
        
        params = {"receive_id_type": "chat_id"}
        
        response = requests.post(url, headers=headers, json=payload, params=params, timeout=10)
        result = response.json()
        
        if result.get('code') == 0:
            print("✅ 卡片消息发送成功！")
            return True
        else:
            print(f"❌ 发送失败：{result}")
            return False


def test_feishu_api():
    """测试飞书 API 推送"""
    
    if APP_ID == "cli_xxxxxxxxxxxxx" or APP_SECRET == "xxxxxxxxxxxxxxxx":
        print("⚠️ 请先配置 APP_ID 和 APP_SECRET")
        print("\n获取方式：")
        print("1. 访问 https://open.feishu.cn/")
        print("2. 进入「企业自建应用」")
        print("3. 创建应用 → 查看凭证")
        return
    
    try:
        feishu = FeishuAPI(APP_ID, APP_SECRET)
        
        # 测试文本消息
        message = """📰 新闻推送系统测试

这是一条通过飞书 API 发送的测试消息。

✅ 如果收到此消息，说明配置成功！"""
        
        print(f"📤 正在发送测试消息...")
        feishu.send_text_message(CHAT_ID, message)
        
    except Exception as e:
        print(f"❌ 测试失败：{e}")


if __name__ == "__main__":
    test_feishu_api()
