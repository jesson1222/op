#!/usr/bin/env python3
"""小红书登录脚本 - 主机版本（用于首次登录保存 Cookie）"""

import asyncio
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright

# 配置 - 使用本地路径
XHS_URL = "https://creator.xiaohongshu.com"
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
COOKIE_FILE = DATA_DIR / "xiaohongshu_cookies.json"

async def login_and_save_cookie():
    """手动登录并保存 Cookie"""
    print("\n" + "=" * 60)
    print("📕 小红书登录工具 - 主机版")
    print("=" * 60)
    print("\n🔐 正在打开浏览器，请使用手机小红书 APP 扫码登录...")
    print("⏱️  你有 120 秒时间完成登录\n")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,  # 显示浏览器窗口
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = await browser.new_page()
        await page.goto(XHS_URL)
        
        # 等待登录（检测关键元素）
        try:
            await page.wait_for_selector('[class*="userAvatar"]', timeout=120000)
            print("\n✅ 检测到已登录！")
            
            # 保存 Cookie
            cookies = await page.context.cookies()
            import json
            with open(COOKIE_FILE, 'w', encoding='utf-8') as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Cookie 已保存到：{COOKIE_FILE}")
            print("\n🎉 登录完成！")
            print("📝 现在可以运行 Docker 容器自动发布了：")
            print("   cd xiaohongshu-publisher && docker-compose up")
            
            await page.close()
            await browser.close()
            return True
            
        except Exception as e:
            print(f"\n❌ 登录超时或失败：{e}")
            await page.close()
            await browser.close()
            return False

if __name__ == "__main__":
    success = asyncio.run(login_and_save_cookie())
    sys.exit(0 if success else 1)
