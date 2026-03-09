#!/usr/bin/env python3
"""小红书发布脚本 - 主机版本（带浏览器界面，用于调试）"""

import asyncio
import os
import sys
import json
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

# 配置 - 使用本地路径
XHS_URL = "https://creator.xiaohongshu.com"
DATA_DIR = Path(__file__).parent / "data"
IMAGES_DIR = Path(__file__).parent / "images"
COOKIE_FILE = DATA_DIR / "xiaohongshu_cookies.json"

# 发布内容配置
PUBLISH_CONFIG = {
    "title": "Cooke 镜头 | 好莱坞光学传奇",
    "content": """100 多年来，Cooke 镜头几乎拍摄了所有好莱坞经典电影！
从《星球大战》到《沙丘》，从《007》到《权力的游戏》
Cooke 镜头是好莱坞摄影师的首选🎥

✨ 为什么顶级摄影师都爱 Cooke？

Cooke 镜头有一个外号叫"电影镜头中的劳斯莱斯"
这不是吹出来的，是 100 多年光学积淀换来的

【Cooke Look 的 5 大秘密】

1️⃣ 温暖色调倾向
• 色温偏移约 +200K
• 肤色呈现健康红润
• 特别适合情感类场景

2️⃣ 柔和对比度
• 高光过渡极其平滑
• 暗部细节丰富
• 画面不刺眼，观感舒适

3️⃣ 奶油般散景
• 9 叶片光圈设计
• 焦外光斑圆润饱满
• 背景虚化自然

4️⃣ 超低色差
• 特殊玻璃配方
• 边缘画质优秀
• 色彩还原准确

5️⃣ 呼吸效应控制
• 对焦时视角稳定
• 专业视频必备
• 电影级表现

💰 购买建议

【全新 vs 二手】
• 全新：有保修，最新镀膜，价格高
• 二手：价格低 30-50%，无保修
• 建议：第一次购买选二手 S4/i，性价比最高

🎯 Cooke 镜头最佳使用场景

✅ 强烈推荐：
• 人物特写（肤色完美）
• 情感戏（温暖色调）
• 夜景（大光圈 + 柔和高光）
• 古装剧（经典光学感）

🔧 Cooke 镜头搭配建议

【摄影机搭配】
• ARRI Alexa 系列（最佳组合）
• RED V-RAPTOR
• Sony Venice 2

💡 保养与维护

【日常保养】
• 使用镜头盖和遮光罩
• 定期清洁前后镜片
• 存放于防潮箱

🎬 结语

Cooke 镜头代表的是一种电影美学
温暖、感性、以人为本

好镜头不会让你成为好摄影师
但好摄影师能让好镜头发光✨

👇 互动时间

你用过 Cooke 镜头吗？
最喜欢哪个焦段？
评论区聊聊你的使用体验！

也欢迎关注我，获取更多影视器材干货📚""",
    "tags": [
        "Cooke 镜头", "电影镜头", "摄影器材", "影视拍摄", "好莱坞",
        "摄影师", "电影制作", "光学传奇", "专业摄影", "器材党",
        "cinematography", "电影感", "灯光摄影", "ARRI", "RED 摄影机"
    ]
}


async def publish_note():
    """发布笔记"""
    print("\n" + "=" * 60)
    print("📕 小红书发布工具 - 主机调试版")
    print("=" * 60)
    
    # 加载 Cookie
    if not COOKIE_FILE.exists():
        print("❌ 未找到 Cookie 文件，请先运行 login-local.py")
        return False
    
    with open(COOKIE_FILE, 'r', encoding='utf-8') as f:
        cookies = json.load(f)
    
    print(f"\n✅ 已加载 {len(cookies)} 个 Cookie")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,  # 显示浏览器
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = await browser.new_page()
        await page.context.add_cookies(cookies)
        
        print(f"\n🌐 打开小红书创作者平台...")
        await page.goto(XHS_URL)
        await asyncio.sleep(5)  # 等待页面加载
        
        # 截图
        await page.screenshot(path=str(DATA_DIR / "01_homepage.png"))
        print("📸 已截图：01_homepage.png")
        
        # 查找发布按钮
        print("\n🔍 查找发布按钮...")
        
        # 尝试多种选择器
        selectors = [
            '[class*="uploadBtn"]',
            'button:has-text("发布")',
            'button:has-text("上传")',
            'button:has-text("发布笔记")',
            '.upload-btn',
            '[data-testid="upload"]',
            'a[href*="/publish"]',
        ]
        
        upload_btn = None
        for selector in selectors:
            try:
                upload_btn = await page.query_selector(selector)
                if upload_btn:
                    print(f"✅ 找到发布按钮：{selector}")
                    break
            except:
                continue
        
        if not upload_btn:
            print("❌ 未找到发布按钮")
            print("\n📋 页面标题:", await page.title())
            print("\n💡 请手动点击发布按钮，然后告诉我...")
            
            # 等待用户手动操作
            await asyncio.sleep(30)
            
            # 截图
            await page.screenshot(path=str(DATA_DIR / "02_manual.png"))
            print("📸 已截图：02_manual.png")
        
        await browser.close()
        return True


if __name__ == "__main__":
    asyncio.run(publish_note())
