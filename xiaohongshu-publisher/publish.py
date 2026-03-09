#!/usr/bin/env python3
"""小红书全自动发布脚本 - 支持 Docker 部署"""

import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

# 导入 Cookie 管理器
from cookie_manager import save_cookies, load_cookies, is_logged_in, get_cookie_status

# 配置
XHS_URL = "https://creator.xiaohongshu.com"
DATA_DIR = Path("/app/data")
IMAGES_DIR = Path("/app/images")

# 发布内容配置（从 Markdown 草稿解析）
PUBLISH_CONFIG = {
    "title": "Cooke 镜头 | 好莱坞光学传奇",
    "content": """100 多年来，Cooke 镜头几乎拍摄了所有好莱坞经典电影！
从《星球大战》到《沙丘》，从《007》》到《权力的游戏》
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

📊 Cooke 镜头经典型号

【S8/i T1.4】全画幅旗舰
• 最新一代光学设计
• 内置/i Technology 数据输出
• 全焦段 T1.4 大光圈

【S7/i T2.0】专业全画幅
• 经典型号，大量影视作品使用
• 光学素质优秀
• 性价比高

【S4/i T2.0】Super35 经典
• 最畅销的 Cooke 系列
• 轻便紧凑
• 二手市场活跃

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


async def login_and_save_cookie(browser):
    """手动登录并保存 Cookie"""
    print("\n🔐 请登录小红书创作者平台...")
    print("📱 打开浏览器后，使用手机扫码登录")
    print("⏱️  你有 60 秒时间完成登录...\n")
    
    page = await browser.new_page()
    await page.goto(XHS_URL)
    
    # 等待登录（检测关键元素）
    try:
        await page.wait_for_selector('[class*="userAvatar"]', timeout=60000)
        print("✅ 检测到已登录！")
        
        # 保存 Cookie
        save_cookies(page.context)
        await page.close()
        return True
    except Exception as e:
        print(f"❌ 登录超时或失败：{e}")
        await page.close()
        return False


async def publish_note(browser):
    """发布笔记"""
    print("\n📝 开始发布笔记...")
    
    # 加载 Cookie
    cookies = load_cookies()
    if not cookies:
        print("❌ 未找到 Cookie，请先登录")
        return False
    
    page = await browser.new_page()
    await page.context.add_cookies(cookies)
    await page.goto(XHS_URL)
    await asyncio.sleep(3)  # 等待页面加载
    
    # 截图调试
    await page.screenshot(path="/app/data/page_loaded.png")
    print("📸 已截图：page_loaded.png")
    
    # 验证登录态 - 宽松模式
    try:
        await page.wait_for_selector('[class*="uploadBtn"], button:has-text("发布"), button:has-text("上传")', timeout=5000)
        print("✅ 登录态有效")
    except:
        print("⚠️  未找到发布按钮，尝试继续...")
        # 不直接返回，继续尝试
    
    # 点击发布按钮
    print("📤 点击发布按钮...")
    try:
        # 尝试多种选择器
        upload_btn = None
        selectors = [
            '[class*="uploadBtn"]',
            'button:has-text("发布")',
            'button:has-text("上传")',
            '.upload-btn',
            '[data-testid="upload"]'
        ]
        
        for selector in selectors:
            try:
                upload_btn = await page.query_selector(selector)
                if upload_btn:
                    await upload_btn.click()
                    print(f"✅ 找到发布按钮：{selector}")
                    break
            except:
                continue
        
        if not upload_btn:
            print("❌ 未找到发布按钮，页面可能已更新")
            await page.screenshot(path="/app/data/debug_page.png")
            await page.close()
            return False
        
        await asyncio.sleep(2)
        
        # 上传图片
        print("🖼️  上传图片...")
        image_files = list(IMAGES_DIR.glob("*.jpg")) + list(IMAGES_DIR.glob("*.png"))
        
        if not image_files:
            print("⚠️  未找到图片文件，请确保 /app/images 目录有图片")
        else:
            file_input = await page.query_selector('input[type="file"]')
            if file_input:
                await file_input.set_input_files([str(f) for f in image_files[:7]])
                print(f"✅ 已上传 {len(image_files[:7])} 张图片")
                await asyncio.sleep(3)
        
        # 填写标题
        print("✏️  填写标题...")
        title_input = await page.query_selector('input[placeholder*="标题"]')
        if title_input:
            await title_input.fill(PUBLISH_CONFIG["title"])
            print(f"✅ 标题已填写：{PUBLISH_CONFIG['title']}")
        
        # 填写正文
        print("✏️  填写正文...")
        content_input = await page.query_selector('div[contenteditable="true"]')
        if content_input:
            await content_input.fill(PUBLISH_CONFIG["content"])
            print("✅ 正文已填写")
        
        # 添加标签
        print("🏷️  添加标签...")
        for tag in PUBLISH_CONFIG["tags"][:15]:
            # 找到标签输入框
            tag_input = await page.query_selector('input[placeholder*="标签"]')
            if tag_input:
                await tag_input.fill(f"#{tag}")
                await asyncio.sleep(0.5)
                # 按回车确认
                await page.keyboard.press("Enter")
                await asyncio.sleep(0.5)
        print(f"✅ 已添加 {len(PUBLISH_CONFIG['tags'][:15])} 个标签")
        
        # 发布
        print("🚀 点击发布...")
        publish_btn = await page.query_selector('button:has-text("发布笔记")')
        if not publish_btn:
            publish_btn = await page.query_selector('button:has-text("发布")')
        
        if publish_btn:
            await publish_btn.click()
            print("✅ 已点击发布按钮！")
            
            # 等待发布完成
            await asyncio.sleep(5)
            
            # 检查是否发布成功
            success_msg = await page.query_selector('text~="发布成功"')
            if success_msg:
                print("🎉 发布成功！")
                await page.close()
                return True
            else:
                print("⚠️  发布状态待确认，请检查小红书后台")
                await page.screenshot(path="/app/data/publish_result.png")
                await page.close()
                return True
        else:
            print("❌ 未找到发布按钮")
            await page.close()
            return False
            
    except Exception as e:
        print(f"❌ 发布过程出错：{e}")
        await page.screenshot(path="/app/data/error.png")
        await page.close()
        return False


async def main():
    """主函数"""
    print("=" * 60)
    print("📕 小红书全自动发布工具")
    print("=" * 60)
    
    # 检查 Cookie 状态
    status = get_cookie_status()
    print(f"\n📊 Cookie 状态：{status['message']}")
    
    async with async_playwright() as p:
        # 检测是否有 Cookie，没有则显示浏览器用于登录
        has_cookie = get_cookie_status().get("valid", False)
        browser = await p.chromium.launch(
            headless=has_cookie,  # 有 Cookie 则后台运行
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        # 如果没有有效 Cookie，先登录
        if not status.get("valid"):
            success = await login_and_save_cookie(browser)
            if not success:
                print("❌ 登录失败，退出")
                await browser.close()
                sys.exit(1)
            
            print("\n✅ 登录完成！Cookie 已保存")
            print("📝 下次运行将自动发布，无需重复登录")
            await browser.close()
            sys.exit(0)
        
        # 已有有效 Cookie，直接发布
        print("\n🚀 开始自动发布...")
        success = await publish_note(browser)
        await browser.close()
        
        if success:
            print("\n🎉 发布流程完成！")
        else:
            print("\n❌ 发布失败，请检查日志")
            sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
