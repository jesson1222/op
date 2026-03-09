#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 Cooke 官网获取产品图片并截图保存
"""

import time
from pathlib import Path
from playwright.sync_api import sync_playwright


def fetch_cooke_images():
    """从 Cooke 官网截图保存产品图片"""
    
    print("🌐 启动浏览器...")
    playwright = sync_playwright().start()
    
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        viewport={'width': 1440, 'height': 900},
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        proxy={'server': 'http://127.0.0.1:9674'}  # 使用 ClashX 代理
    )
    page = context.new_page()
    
    # 创建保存目录
    images_dir = Path(__file__).parent / "images" / "cooke-legend"
    images_dir.mkdir(parents=True, exist_ok=True)
    
    # Cooke 官网产品页面
    products = [
        {
            'name': 'S8i-flagship',
            'url': 'https://cookeoptics.com/products/s8-i-full-frame-primes/',
            'description': 'S8/i 全画幅旗舰镜头'
        },
        {
            'name': 'S7i-fullframe',
            'url': 'https://cookeoptics.com/products/s7-i-full-frame-primes/',
            'description': 'S7/i 全画幅镜头'
        },
        {
            'name': 'S4i-super35',
            'url': 'https://cookeoptics.com/products/s4-i-primes/',
            'description': 'S4/i Super35 镜头'
        },
        {
            'name': '5i-speed',
            'url': 'https://cookeoptics.com/products/5-i-speed-primes/',
            'description': '5/i 高速定焦镜头'
        },
        {
            'name': 'sp3-zoom',
            'url': 'https://cookeoptics.com/products/sp3-zooms/',
            'description': 'SP3 变焦镜头'
        },
        {
            'name': 'cooke-look',
            'url': 'https://cookeoptics.com/cooke-look/',
            'description': 'Cooke Look 光学特色'
        },
        {
            'name': 'homepage',
            'url': 'https://cookeoptics.com/',
            'description': 'Cooke 官网首页'
        },
    ]
    
    print(f"📷 准备截取 {len(products)} 个产品页面...")
    print("=" * 60)
    
    saved_images = []
    
    for i, product in enumerate(products, 1):
        print(f"\n[{i}/{len(products)}] {product['name']}")
        print(f"URL: {product['url']}")
        
        try:
            # 打开页面
            page.goto(product['url'], wait_until='networkidle', timeout=30000)
            time.sleep(3)  # 等待页面完全加载
            
            # 滚动页面查看内容
            page.evaluate("window.scrollTo(0, document.body.scrollHeight / 3)")
            time.sleep(1)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
            time.sleep(1)
            page.evaluate("window.scrollTo(0, 0)")
            time.sleep(1)
            
            # 截图
            screenshot_path = images_dir / f"{i:02d}-{product['name']}.png"
            page.screenshot(path=str(screenshot_path), full_page=False)
            
            print(f"✅ 已保存：{screenshot_path.name}")
            saved_images.append(str(screenshot_path))
            
        except Exception as e:
            print(f"❌ 失败：{e}")
    
    # 截取一些产品特写（如果有产品图片元素）
    print("\n" + "=" * 60)
    print("🔍 尝试截取产品特写...")
    
    # 返回产品列表页
    page.goto('https://cookeoptics.com/products/', wait_until='networkidle', timeout=30000)
    time.sleep(3)
    
    # 截图产品列表
    products_list_path = images_dir / "00-products-overview.png"
    page.screenshot(path=str(products_list_path), full_page=False)
    print(f"✅ 产品概览：{products_list_path.name}")
    saved_images.insert(0, str(products_list_path))
    
    # 关闭浏览器
    browser.close()
    playwright.stop()
    
    print("\n" + "=" * 60)
    print(f"✅ 完成！共保存 {len(saved_images)} 张图片")
    print(f"📁 保存目录：{images_dir}")
    print("\n图片列表:")
    for img in saved_images:
        print(f"  - {Path(img).name}")
    
    return saved_images


if __name__ == "__main__":
    fetch_cooke_images()
