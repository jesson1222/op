#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻推送脚本 - AI 模型翻译版
使用 Bailian AI 模型翻译新闻后推送
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

class NewsPusherAI:
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = BASE_DIR / config_path
        self.config = self.load_config()
        self.history = self.load_history()
        
        # AI 模型配置
        self.ai_config = {
            'base_url': 'https://coding.dashscope.aliyuncs.com/v1',
            'api_key': 'sk-sp-9f96977287be4cf8ba33b60b77121481',
            'model': 'bailian/qwen3.5-plus',  # 使用 qwen3.5-plus 翻译
            'max_tokens': 2048
        }
        
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
            for entry in feed.entries[:20]:  # 每个源最多取 20 条
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
    
    def filter_items(self, items: List[Dict], feed_config: Dict) -> List[Dict]:
        """过滤新闻"""
        filter_config = self.config.get('filter', {})
        include_keywords = filter_config.get('include_keywords', [])
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
            
            # 包含关键词（如果设置了）
            if include_keywords and not any(kw in item['title'] for kw in include_keywords):
                continue
            
            filtered.append(item)
        
        return filtered
    
    def translate_with_ai(self, text: str) -> str:
        """使用 AI 模型翻译文本"""
        if not text or len(text.strip()) < 5:
            return text
        
        try:
            headers = {
                'Authorization': f"Bearer {self.ai_config['api_key']}",
                'Content-Type': 'application/json'
            }
            
            prompt = f"""请将以下英文新闻标题/摘要翻译成中文，要求：
1. 准确传达原意
2. 符合中文表达习惯
3. 保持简洁
4. 专业术语保留英文原名

原文：{text}

翻译："""
            
            data = {
                'model': self.ai_config['model'].replace('bailian/', ''),
                'messages': [
                    {
                        'role': 'system',
                        'content': '你是一个专业的新闻翻译助手，擅长将英文科技新闻翻译成流畅的中文。'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'max_tokens': self.ai_config['max_tokens'],
                'temperature': 0.3
            }
            
            response = requests.post(
                f"{self.ai_config['base_url']}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                translated = result['choices'][0]['message']['content'].strip()
                return translated
            else:
                print(f"⚠️ 翻译失败：{response.status_code}")
                return text
                
        except Exception as e:
            print(f"⚠️ AI 翻译异常：{e}")
            return text
    
    def translate_batch(self, items: List[Dict]) -> List[Dict]:
        """批量翻译新闻"""
        print(f"🔄 正在翻译 {len(items)} 条新闻...")
        
        translated_items = []
        for i, item in enumerate(items, 1):
            print(f"  🔄 [{i}/{len(items)}] {item['title'][:50]}...")
            
            # 翻译标题
            translated_title = self.translate_with_ai(item['title'])
            
            # 翻译摘要（如果有）
            translated_summary = ''
            if item.get('summary'):
                translated_summary = self.translate_with_ai(item['summary'])
            
            translated_items.append({
                **item,
                'title_zh': translated_title,
                'summary_zh': translated_summary,
                'translated': True
            })
        
        return translated_items
    
    def format_message(self, category: str, emoji: str, items: List[Dict]) -> str:
        """格式化推送消息（支持中文）"""
        if not items:
            return ""
        
        lines = [f"{emoji} *{category}*\n"]
        for i, item in enumerate(items[:self.config['schedule']['max_items_per_push']], 1):
            # 优先使用翻译后的标题
            title = item.get('title_zh', item['title'])
            link = item['link']
            summary = item.get('summary_zh', item.get('summary', ''))
            
            lines.append(f"{i}. *{title}*")
            lines.append(f"   🔗 {link}")
            if summary:
                lines.append(f"   └ {summary}")
            lines.append("")
        
        lines.append(f"\n_推送时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}__")
        return "\n".join(lines)
    
    def push_telegram(self, message: str):
        """推送到 Telegram"""
        tg_config = self.config.get('telegram', {})
        if not tg_config.get('enabled'):
            return
        
        token = tg_config.get('bot_token')
        chat_id = tg_config.get('chat_id')
        
        if not token or not chat_id:
            print("⚠️ Telegram 配置不完整")
            return
        
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        
        try:
            response = requests.post(url, json=data, timeout=15)
            if response.status_code == 200:
                print("✅ Telegram 推送成功")
            else:
                print(f"❌ Telegram 推送失败：{response.text}")
        except Exception as e:
            print(f"❌ Telegram 推送异常：{e}")
    
    def push_feishu(self, message: str):
        """推送到飞书（卡片消息）"""
        fs_config = self.config.get('feishu', {})
        if not fs_config.get('enabled'):
            return
        
        webhook_url = fs_config.get('webhook_url')
        if not webhook_url:
            print("⚠️ 飞书 webhook 未配置")
            return
        
        # 提取纯文本
        text = message.replace('*', '').replace('_', '')
        
        data = {
            "msg_type": "text",
            "content": {
                "text": text
            }
        }
        
        try:
            response = requests.post(webhook_url, json=data, timeout=15)
            if response.status_code == 200:
                print("✅ 飞书推送成功")
            else:
                print(f"❌ 飞书推送失败：{response.text}")
        except Exception as e:
            print(f"❌ 飞书推送异常：{e}")
    
    def run(self):
        """执行推送"""
        print(f"\n📰 开始推送新闻 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🤖 使用 AI 模型翻译：{self.ai_config['model']}")
        
        all_items = []
        
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
                filtered = self.filter_items(items, source)
                category_items.extend(filtered)
            
            # 按时间排序，取最新的
            category_items.sort(key=lambda x: x.get('published', ''), reverse=True)
            
            if category_items:
                # 🤖 AI 翻译
                translated_items = self.translate_batch(category_items)
                
                emoji = feed_info.get('emoji', '📰')
                title = feed_info.get('title', category)
                message = self.format_message(title, emoji, translated_items)
                
                if message:
                    # 推送
                    self.push_telegram(message)
                    self.push_feishu(message)
                    
                    # 记录历史
                    for item in translated_items[:self.config['schedule']['max_items_per_push']]:
                        item_id = self.get_item_id(item)
                        if item_id not in self.history['pushed_ids']:
                            self.history['pushed_ids'].append(item_id)
        
        # 保存历史
        self.save_history()
        print("✅ 推送完成\n")


if __name__ == "__main__":
    pusher = NewsPusherAI()
    pusher.run()
