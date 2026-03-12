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
from concurrent.futures import ThreadPoolExecutor, as_completed

# 禁用代理（避免系统代理干扰）
os.environ['HTTP_PROXY'] = ''
os.environ['http_proxy'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['https_proxy'] = ''
os.environ['NO_PROXY'] = '*'
os.environ['ALL_PROXY'] = ''

# 创建不信任环境配置的 Session（避免系统代理）
_requests_session = requests.Session()
_requests_session.trust_env = False
_requests_session.proxies = {}  # 明确设置空代理

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
        
        response = _requests_session.post(url, json=payload, timeout=10)
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
        
        response = _requests_session.post(url, headers=headers, json=payload, params=params, timeout=10)
        result = response.json()
        
        if result.get('code') == 0:
            print("✅ 消息发送成功！")
            return True
        else:
            print(f"❌ 发送失败：{result}")
            return False
    
    def send_interactive_card(self, chat_id: str, card_config: Dict, max_retries: int = 3) -> bool:
        """发送交互式卡片消息（带重试机制）"""
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
        
        # 重试逻辑：处理速率限制等临时错误
        for attempt in range(1, max_retries + 1):
            response = _requests_session.post(url, headers=headers, json=payload, params=params, timeout=10)
            result = response.json()
            
            if result.get('code') == 0:
                print("✅ 卡片消息发送成功！")
                return True
            else:
                code = result.get('code')
                msg = result.get('msg', '')
                
                # 9499 = too many request，需要重试
                if code == 9499 and attempt < max_retries:
                    wait_time = attempt * 30  # 指数退避：30s, 60s, 90s
                    print(f"⚠️  速率限制（{code}: {msg}），{wait_time}秒后重试 ({attempt}/{max_retries})...")
                    import time
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"❌ 发送失败：{result}")
                    return False
        
        return False
    
    def get_chat_info(self, chat_id: str) -> Dict:
        """获取群组信息"""
        token = self.get_tenant_token()
        
        url = f"{self.base_url}/im/v1/chats/{chat_id}"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        response = _requests_session.get(url, headers=headers, timeout=10)
        result = response.json()
        
        if result.get('code') == 0:
            return result.get('data', {})
        else:
            raise Exception(f"获取群组信息失败：{result}")


class Translator:
    """翻译器 - 使用 Ollama 本地 AI 模型翻译"""
    
    def __init__(self, app_id: str = None, app_key: str = None):
        self.cache = {}  # 翻译缓存
        # Ollama API 端点
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model = "qwen3:4b"  # 使用轻量 qwen 模型（更快）
        self.use_ollama = True
        
        # 测试 Ollama 是否可用
        try:
            test_resp = requests.get("http://localhost:11434/api/tags", timeout=10)
            if test_resp.status_code == 200:
                print(f"✅ Ollama 翻译已启用（模型：{self.model}）")
            else:
                print("⚠️ Ollama 响应异常，将跳过翻译")
                self.use_ollama = False
        except Exception as e:
            print(f"⚠️ Ollama 连接失败 ({e})，将跳过翻译")
            self.use_ollama = False
    
    def translate(self, text: str, source: str = "en", target: str = "zh") -> str:
        """使用 Ollama 本地模型翻译文本"""
        if not text or len(text.strip()) < 2:
            return text
        
        # 检查缓存
        cache_key = f"{source}->{target}:{text[:100]}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # 检测是否已经是中文
        if self._is_chinese(text):
            return text
        
        # Ollama 不可用，返回原文
        if not self.use_ollama:
            return text
        
        try:
            # 构建翻译提示
            prompt = f"Translate the following English text to Chinese (only output the translation, no explanations):\n\n{text[:500]}"
            
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "num_predict": 256
                }
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                translated = result.get('response', '').strip()
                
                if translated:
                    self.cache[cache_key] = translated
                    return translated
                else:
                    print(f"    ⚠️ 翻译无结果：{text[:50]}...")
            else:
                print(f"    ⚠️ 翻译失败 (status={response.status_code}): {text[:50]}...")
            
            return text
            
        except Exception as e:
            # 记录失败原因
            print(f"    ⚠️ 翻译异常 ({type(e).__name__}): {e} - {text[:50]}...")
            return text
    
    def _is_chinese(self, text: str) -> bool:
        """检测文本是否包含中文"""
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                return True
        return False
    
    def translate_batch(self, items: List[Dict]) -> List[Dict]:
        """批量翻译新闻"""
        translated_items = []
        
        for i, item in enumerate(items, 1):
            print(f"  🔄 [{i}/{len(items)}] {item.get('title', '')[:50]}...")
            translated_item = item.copy()
            try:
                # 只翻译英文标题和摘要
                title = item.get('title', '')
                summary = item.get('summary', '')[:100]
                
                # 检测是否为英文（简单检测：包含常见英文字符）
                if any(ord(c) > 127 for c in title) and not any(c.isalpha() for c in title):
                    # 已经是中文，跳过翻译
                    translated_items.append(translated_item)
                    continue
                
                # 翻译标题
                translated_title = self.translate(title, 'en', 'zh')
                if translated_title:
                    translated_item['title'] = translated_title
                
                # 翻译摘要
                if summary:
                    translated_summary = self.translate(summary, 'en', 'zh')
                    if translated_summary:
                        translated_item['summary'] = translated_summary
                
            except Exception as e:
                print(f"    ⚠️ 翻译异常：{e}")
            
            translated_items.append(translated_item)
        
        return translated_items


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
        
        # 初始化翻译器（读取百度翻译配置）
        translate_config = self.config.get('translate', {})
        baidu_app_id = translate_config.get('baidu_app_id')
        baidu_app_key = translate_config.get('baidu_app_key')
        self.translator = Translator(baidu_app_id, baidu_app_key)
    
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
        history_filename = self.config.get('logging', {}).get('history_file', 'history.json')
        history_file = LOGS_DIR / history_filename
        LOGS_DIR.mkdir(exist_ok=True)
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
                
                # 🌐 翻译英文内容为中文（可配置跳过）
                skip_translation = self.config.get('skip_translation', False)
                if skip_translation:
                    print(f"⏭️  跳过翻译，使用原文")
                    translated_items = category_items
                else:
                    print(f"🔄 正在翻译 {len(category_items)} 条新闻...")
                    translated_items = self.translator.translate_batch(category_items)
                
                # 发送交互式卡片
                card = self.format_news_card(title, emoji, translated_items)
                if card:
                    self.feishu.send_interactive_card(chat_id, card)
                    
                    # 记录历史
                    for item in translated_items[:self.config['schedule']['max_items_per_push']]:
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
