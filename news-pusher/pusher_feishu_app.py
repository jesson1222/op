#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书企业应用推送脚本
使用 App ID + App Secret 方式发送消息（无需 Webhook）
"""

import os
import sys
import json
import yaml
import hashlib
import feedparser
import requests
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# 项目根目录
BASE_DIR = Path(__file__).parent
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)


class FeishuAPI:
    """飞书开放平台 API 客户端"""
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.base_url = "https://open.feishu.cn/open-apis"
        self.token = None
        self.token_expire = 0
    
    def get_tenant_token(self) -> str:
        """获取企业访问令牌"""
        if self.token and datetime.now().timestamp() < self.token_expire:
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
            self.token_expire = datetime.now().timestamp() + result['expire'] - 60
            return self.token
        else:
            raise Exception(f"获取 token 失败：{result.get('msg', result)}")
    
    def send_text_message(self, chat_id: str, text: str) -> bool:
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
        
        params = {"receive_id_type": "chat_id"}
        
        response = requests.post(url, headers=headers, json=payload, params=params, timeout=10)
        result = response.json()
        
        if result.get('code') == 0:
            print("✅ 消息发送成功！")
            return True
        else:
            print(f"❌ 发送失败：{result}")
            return False
    
    def send_interactive_card(self, chat_id: str, card_config: Dict) -> bool:
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
    
    def get_chat_info(self, chat_id: str) -> Dict:
        """获取群组信息"""
        token = self.get_tenant_token()
        
        url = f"{self.base_url}/im/v1/chats/{chat_id}"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        result = response.json()
        
        if result.get('code') == 0:
            return result.get('data', {})
        else:
            raise Exception(f"获取群组信息失败：{result}")


class NewsPusher:
    """新闻推送器"""
    
    def __init__(self, config_path: str = "config_feishu_app.yaml"):
        self.config_path = BASE_DIR / config_path
        self.config = self.load_config()
        self.history = self.load_history()
        self.feishu = FeishuAPI(
            self.config['feishu_app']['app_id'],
            self.config['feishu_app']['app_secret']
        )
    
    def load_config(self) -> Dict:
        """加载配置文件"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def load_history(self) -> Dict:
        """加载已推送历史记录"""
        history_file = LOGS_DIR / self.config.get('logging', {}).get('history_file', 'history.json')
        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"pushed_ids": []}
    
    def save_history(self):
        """保存推送历史"""
        history_file = LOGS_DIR / self.config.get('logging', {}).get('history_file', 'history.json')
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def get_item_id(self, item: Any) -> str:
        """生成新闻唯一 ID"""
        content = f"{item.get('title', '')}{item.get('link', '')}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def fetch_feed(self, url: str) -> List[Dict]:
        """抓取 RSS 源"""
        try:
            feed = feedparser.parse(url)
            items = []
            for entry in feed.entries[:20]:
                item = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'summary': entry.get('summary', '')[:200] if entry.get('summary') else '',
                    'published': entry.get('published', ''),
                    'source': feed.feed.get('title', 'Unknown')
                }
                items.append(item)
            return items
        except Exception as e:
            print(f"❌ 抓取失败 {url}: {e}")
            return []
    
    def filter_items(self, items: List[Dict]) -> List[Dict]:
        """过滤新闻"""
        filter_config = self.config.get('filter', {})
        exclude_keywords = filter_config.get('exclude_keywords', [])
        min_title_length = filter_config.get('min_title_length', 5)
        
        filtered = []
        for item in items:
            # 跳过已推送的
            item_id = self.get_item_id(item)
            if item_id in self.history.get('pushed_ids', []):
                continue
            
            # 标题太短
            if len(item['title']) < min_title_length:
                continue
            
            # 排除关键词
            if any(kw in item['title'] for kw in exclude_keywords):
                continue
            
            filtered.append(item)
        
        return filtered
    
    def format_news_card(self, category: str, emoji: str, items: List[Dict]) -> Dict:
        """格式化新闻为交互式卡片"""
        if not items:
            return {}
        
        # 构建新闻列表内容
        news_content = ""
        for i, item in enumerate(items[:self.config['schedule']['max_items_per_push']], 1):
            news_content += f"{i}. **{item['title']}**\n"
            news_content += f"[查看详情]({item['link']})\n\n"
        
        card_config = {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "template": "blue",
                "title": {
                    "tag": "plain_text",
                    "content": f"{emoji} {category}"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": news_content.strip()
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
                            "content": f"推送时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} | 共 {len(items)} 条新闻"
                        }
                    ]
                }
            ]
        }
        
        return card_config
    
    def run(self):
        """执行推送"""
        print(f"\n📰 开始推送新闻 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        chat_id = self.config['feishu_app']['chat_id']
        
        # 遍历所有分类
        feeds_config = self.config.get('feeds', {})
        for category, feed_info in feeds_config.items():
            if not feed_info.get('enabled'):
                continue
            
            feed_path = BASE_DIR / feed_info['path']
            if not feed_path.exists():
                print(f"⚠️ 饲料文件不存在：{feed_path}")
                continue
            
            # 加载 RSS 源列表
            with open(feed_path, 'r', encoding='utf-8') as f:
                sources = yaml.safe_load(f)
            
            category_items = []
            for source in sources:
                print(f"📡 抓取：{source['name']}")
                items = self.fetch_feed(source['url'])
                filtered = self.filter_items(items)
                category_items.extend(filtered)
            
            # 按时间排序
            category_items.sort(key=lambda x: x.get('published', ''), reverse=True)
            
            if category_items:
                emoji = feed_info.get('emoji', '📰')
                title = feed_info.get('title', category)
                
                # 发送交互式卡片
                card = self.format_news_card(title, emoji, category_items)
                if card:
                    self.feishu.send_interactive_card(chat_id, card)
                    
                    # 记录历史
                    for item in category_items[:self.config['schedule']['max_items_per_push']]:
                        item_id = self.get_item_id(item)
                        if item_id not in self.history['pushed_ids']:
                            self.history['pushed_ids'].append(item_id)
        
        # 保存历史
        self.save_history()
        print("✅ 推送完成\n")


def test_connection():
    """测试飞书连接"""
    config_path = BASE_DIR / "config_feishu_app.yaml"
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    app_id = config['feishu_app']['app_id']
    app_secret = config['feishu_app']['app_secret']
    chat_id = config['feishu_app']['chat_id']
    
    if app_id == "cli_xxxxxxxxxxxxx":
        print("⚠️ 请先配置 config_feishu_app.yaml")
        print("\n需要配置：")
        print("1. feishu_app.app_id - 从飞书开放平台获取")
        print("2. feishu_app.app_secret - 从飞书开放平台获取")
        print("3. feishu_app.chat_id - 飞书群组 ID")
        return False
    
    try:
        feishu = FeishuAPI(app_id, app_secret)
        
        # 测试获取 token
        token = feishu.get_tenant_token()
        print("✅ Token 获取成功")
        
        # 测试获取群组信息
        chat_info = feishu.get_chat_info(chat_id)
        print(f"✅ 群组信息获取成功：{chat_info.get('name', 'Unknown')}")
        
        # 发送测试消息
        test_message = f"""📰 新闻推送系统测试

这是一条通过飞书企业应用发送的测试消息。

✅ 如果收到此消息，说明配置成功！

时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
        
        print("\n📤 正在发送测试消息...")
        feishu.send_text_message(chat_id, test_message)
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        return False


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        print("=" * 50)
        print("🧪 飞书企业应用连接测试")
        print("=" * 50)
        test_connection()
    else:
        pusher = NewsPusher()
        pusher.run()
