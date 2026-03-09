#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书自动发布工具
使用 Playwright 浏览器自动化

⚠️ 注意事项：
1. 首次运行需要手动登录小红书
2. 登录态会保存在 sessions/ 目录
3. 有封号风险，建议谨慎使用
4. 不要频繁发布，模拟人工操作
"""

import json
import time
import random
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


class XiaohongshuPublisher:
    """小红书自动发布器"""
    
    def __init__(self, headless=False):
        """
        初始化发布器
        
        Args:
            headless: 是否无头模式（调试时建议设为 False）
        """
        self.headless = headless
        self.base_url = "https://creator.xiaohongshu.com"
        self.session_dir = Path(__file__).parent / "sessions"
        self.session_dir.mkdir(exist_ok=True)
        self.context = None
        self.page = None
        
    def launch_browser(self):
        """启动浏览器"""
        print("🌐 启动浏览器...")
        self.playwright = sync_playwright().start()
        
        # 使用 Chromium
        browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage',
            ]
        )
        
        # 加载或创建上下文
        context_path = self.session_dir / "xiaohongshu_context.json"
        
        if context_path.exists():
            print("📦 加载保存的登录态...")
            try:
                with open(context_path, 'r', encoding='utf-8') as f:
                    storage_state = json.load(f)
                self.context = browser.new_context(storage_state=storage_state)
            except Exception as e:
                print(f"⚠️ 加载登录态失败：{e}，将使用新会话")
                self.context = browser.new_context()
        else:
            print("🆕 创建新会话（需要手动登录）")
            self.context = browser.new_context(
                viewport={'width': 1280, 'height': 800},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
        
        # 防检测
        self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """)
        
        self.page = self.context.new_page()
        return browser
    
    def save_session(self):
        """保存登录态"""
        if self.context:
            context_path = self.session_dir / "xiaohongshu_context.json"
            try:
                storage_state = self.context.storage_state()
                with open(context_path, 'w', encoding='utf-8') as f:
                    json.dump(storage_state, f, ensure_ascii=False, indent=2)
                print("💾 登录态已保存")
            except Exception as e:
                print(f"⚠️ 保存登录态失败：{e}")
    
    def login(self):
        """
        登录小红书
        
        首次运行需要手动扫码/输入密码登录
        后续会自动使用保存的登录态
        """
        print("🔐 检查登录状态...")
        
        self.page.goto(self.base_url, wait_until='networkidle')
        time.sleep(2)
        
        # 检查是否已登录
        try:
            # 检测发布按钮是否存在
            self.page.wait_for_selector('button:has-text("发布笔记")', timeout=5000)
            print("✅ 已登录")
            return True
        except PlaywrightTimeout:
            print("⚠️ 未登录，需要手动登录")
            print("📱 请在浏览器中完成登录（扫码或密码）")
            print("⏳ 等待 60 秒...")
            
            # 等待用户手动登录（延长到 120 秒）
            for i in range(120, 0, -1):
                print(f"\r⏰ 剩余时间：{i}秒", end='', flush=True)
                time.sleep(1)
            
            # 再次检查
            try:
                self.page.wait_for_selector('button:has-text("发布笔记")', timeout=3000)
                print("\n✅ 登录成功！")
                self.save_session()
                return True
            except PlaywrightTimeout:
                print("\n❌ 登录超时，请重新运行")
                return False
    
    def publish_note(self, title: str, content: str, images: list = None, tags: list = None):
        """
        发布笔记
        
        Args:
            title: 笔记标题
            content: 笔记正文
            images: 图片路径列表
            tags: 标签列表
        """
        print(f"\n📝 开始发布笔记：{title[:20]}...")
        
        # 导航到发布页
        self.page.goto(f"{self.base_url}/publish", wait_until='networkidle')
        time.sleep(2)
        
        # 1. 上传图片
        if images:
            print(f"📷 上传 {len(images)} 张图片...")
            file_input = self.page.query_selector('input[type="file"]')
            if file_input:
                file_input.set_input_files(images)
                print("✅ 图片上传完成")
                time.sleep(3)  # 等待上传处理
            else:
                print("⚠️ 未找到图片上传控件，尝试点击触发...")
                # 尝试点击上传区域
                try:
                    upload_area = self.page.query_selector('div:has-text("上传图片"), .upload-area')
                    if upload_area:
                        upload_area.click()
                        time.sleep(1)
                        # 处理文件选择对话框（需要系统权限）
                        print("⚠️ 需要手动选择图片文件")
                except Exception as e:
                    print(f"⚠️ 图片上传失败：{e}")
        
        # 2. 填写标题
        print("✏️ 填写标题...")
        try:
            title_input = self.page.query_selector('input[placeholder*="标题"], input[maxlength="20"]')
            if title_input:
                title_input.fill(title)
                print("✅ 标题已填写")
            else:
                # 尝试其他选择器
                title_input = self.page.query_selector('input')
                if title_input:
                    title_input.fill(title)
                    print("✅ 标题已填写")
        except Exception as e:
            print(f"⚠️ 标题填写失败：{e}")
        
        # 3. 填写正文
        print("📄 填写正文...")
        try:
            # 小红书正文通常是 contenteditable 的 div
            content_area = self.page.query_selector('div[contenteditable="true"], .editor-content, [data-placeholder*="正文"]')
            if content_area:
                content_area.click()
                time.sleep(0.5)
                # 分段输入，模拟人工
                paragraphs = content.split('\n\n')
                for para in paragraphs:
                    if para.strip():
                        self.page.keyboard.type(para.strip())
                        self.page.keyboard.press('Enter')
                        time.sleep(random.uniform(0.3, 0.8))
                print("✅ 正文已填写")
            else:
                print("⚠️ 未找到正文输入框")
        except Exception as e:
            print(f"⚠️ 正文填写失败：{e}")
        
        # 4. 添加标签
        if tags:
            print("🏷️ 添加标签...")
            try:
                # 先输入 # 触发标签输入
                self.page.keyboard.type('#')
                time.sleep(0.5)
                
                for tag in tags[:10]:  # 最多 10 个标签
                    # 清除并输入新标签
                    tag_name = tag.replace('#', '').strip()
                    self.page.keyboard.type(tag_name)
                    time.sleep(0.5)
                    # 按回车确认
                    self.page.keyboard.press('Enter')
                    time.sleep(0.5)
                    # 输入下一个标签
                    if tag != tags[-1]:
                        self.page.keyboard.type('#')
                        time.sleep(0.3)
                
                print("✅ 标签已添加")
            except Exception as e:
                print(f"⚠️ 标签添加失败：{e}")
        
        # 5. 截图预览（调试用）
        print("📸 截取预览...")
        screenshot_path = self.session_dir / f"preview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        self.page.screenshot(path=str(screenshot_path), full_page=True)
        print(f"✅ 预览已保存：{screenshot_path}")
        
        # 6. 发布（需要手动确认，避免封号）
        print("\n⚠️ 发布前检查")
        print("请检查内容是否正确，然后手动点击发布按钮")
        print("或者等待 30 秒后自动发布...")
        
        # 倒计时
        for i in range(30, 0, -1):
            print(f"\r⏰ {i}秒后自动发布", end='', flush=True)
            time.sleep(1)
        
        # 尝试点击发布按钮
        try:
            publish_btn = self.page.query_selector('button:has-text("发布"), button:has-text("发布笔记")')
            if publish_btn:
                publish_btn.click()
                print("\n✅ 已点击发布按钮")
                time.sleep(5)
                
                # 检查发布结果
                try:
                    self.page.wait_for_url('**/success**', timeout=5000)
                    print("✅ 发布成功！")
                    return True
                except PlaywrightTimeout:
                    print("⚠️ 发布状态未知，请手动检查")
                    return None
            else:
                print("⚠️ 未找到发布按钮，请手动操作")
                return None
        except Exception as e:
            print(f"\n⚠️ 发布失败：{e}")
            return False
    
    def close(self):
        """关闭浏览器"""
        if hasattr(self, 'playwright'):
            self.playwright.stop()
            print("👋 浏览器已关闭")


def load_note_from_file(filepath: str) -> dict:
    """从 Markdown 文件加载笔记内容"""
    content = Path(filepath).read_text(encoding='utf-8')
    
    # 简单解析 Markdown
    note = {
        'title': '',
        'content': '',
        'tags': [],
        'images': []
    }
    
    lines = content.split('\n')
    in_content = False
    in_tags = False
    
    for line in lines:
        if line.startswith('### 【标题】'):
            in_content = True
            in_tags = False
            continue
        elif line.startswith('### 【正文】'):
            in_content = True
            in_tags = False
            continue
        elif line.startswith('### 【标签】'):
            in_content = False
            in_tags = True
            continue
        elif line.startswith('### 【图片】'):
            in_content = False
            in_tags = False
            continue
        
        if in_content and line.startswith('```'):
            continue
        elif in_content:
            note['content'] += line + '\n'
        elif in_tags and line.startswith('#'):
            note['tags'].append(line.strip())
    
    # 清理内容
    note['content'] = note['content'].strip()
    note['tags'] = [t for t in note['tags'] if t.strip()]
    
    return note


def main():
    """主函数"""
    print("=" * 60)
    print("📕 小红书自动发布工具")
    print("=" * 60)
    
    # 加载笔记内容
    note_file = Path(__file__).parent / "ready-to-publish" / "cooke-legend-v1.md"
    
    if not note_file.exists():
        print(f"❌ 笔记文件不存在：{note_file}")
        print("请先创建笔记内容文件")
        return
    
    print(f"📖 加载笔记：{note_file}")
    note = load_note_from_file(str(note_file))
    
    # 标题（从文件名或内容提取）
    title = "🎬 百年 Cooke 镜头 | 好莱坞背后的光学传奇"
    
    # 标签
    tags = [
        "#Cooke 镜头", "#电影镜头", "#摄影器材", "#影视拍摄", "#好莱坞",
        "#摄影师", "#电影制作", "#光学传奇", "#专业摄影", "#器材党",
        "#cinematography", "#电影感", "#灯光摄影", "#ARRI", "#RED 摄影机"
    ]
    
    # 图片（使用刚才截图的图片）
    images_dir = Path(__file__).parent / "images" / "cooke-legend"
    images = []
    if images_dir.exists():
        jpg_files = list(images_dir.glob("*.jpg"))
        png_files = list(images_dir.glob("*.png"))
        all_images = jpg_files + png_files
        # 按名称排序，确保封面在前
        images = sorted([str(p) for p in all_images])
        print(f"📷 找到 {len(images)} 张图片")
        for img in images:
            print(f"  - {Path(img).name}")
    else:
        print("⚠️ 未找到图片目录，将发布纯文字笔记")
    
    # 创建发布器
    publisher = XiaohongshuPublisher(headless=False)  # 首次建议用有头模式
    
    try:
        # 启动浏览器
        browser = publisher.launch_browser()
        
        # 登录
        if not publisher.login():
            print("❌ 登录失败，退出")
            return
        
        # 发布笔记
        result = publisher.publish_note(
            title=title,
            content=note['content'] if note['content'] else "内容加载中...",
            images=images if images else None,
            tags=tags
        )
        
        # 结果
        if result is True:
            print("\n🎉 发布成功！")
        elif result is False:
            print("\n❌ 发布失败")
        else:
            print("\n⚠️ 发布状态未知，请手动检查小红书账号")
        
        # 保存会话
        publisher.save_session()
        
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断")
    except Exception as e:
        print(f"\n❌ 发生错误：{e}")
        import traceback
        traceback.print_exc()
    finally:
        publisher.close()
    
    print("\n" + "=" * 60)
    print("✅ 执行完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
