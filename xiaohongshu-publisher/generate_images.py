#!/usr/bin/env python3
"""生成小红书配图 - 从官网获取内容并生成专业图片"""

from PIL import Image, ImageDraw, ImageFont
import os

# 确保目录存在
os.makedirs('images', exist_ok=True)

# 小红书图片尺寸：3:4 (1080x1440)
WIDTH, HEIGHT = 1080, 1440

# 颜色方案（来自官网）
COLORS = {
    'primary': (255, 90, 54),      # #FF5A36
    'primary_light': (255, 138, 107),  # #FF8A6B
    'background_light': (255, 255, 255),
    'background_dark': (14, 12, 13),
    'text_dark': (30, 25, 24),
    'text_light': (255, 255, 255),
}

def get_font(size):
    """获取字体"""
    try:
        return ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", size)
    except:
        return ImageFont.load_default()

def create_cover_image():
    """P1: 封面图 - 标题页"""
    img = Image.new('RGB', (WIDTH, HEIGHT), COLORS['primary'])
    draw = ImageDraw.Draw(img)
    
    # 标题
    title_font = get_font(80)
    subtitle_font = get_font(50)
    
    # 主标题
    draw.text((WIDTH//2, HEIGHT//2 - 100), "OpenClaw", fill='white', 
              font=title_font, anchor='mm', align='center')
    draw.text((WIDTH//2, HEIGHT//2), "v2026.3.8 更新", fill='white', 
              font=title_font, anchor='mm', align='center')
    
    # 副标题
    draw.text((WIDTH//2, HEIGHT//2 + 150), "升级不适？老用户带你上手", 
              fill='white', font=subtitle_font, anchor='mm', align='center')
    
    # 底部标签
    tag_font = get_font(35)
    draw.text((WIDTH//2, HEIGHT - 150), "🦞 备份·配置·调试 一篇搞定", 
              fill='white', font=tag_font, anchor='mm', align='center')
    
    # 保存
    img.save('images/xiaohongshu_p1.jpg', quality=95)
    print("✅ P1 封面图已生成")
    return 'images/xiaohongshu_p1.jpg'

def create_content_image_1():
    """P2: 3 大变化"""
    img = Image.new('RGB', (WIDTH, HEIGHT), COLORS['background_light'])
    draw = ImageDraw.Draw(img)
    
    title_font = get_font(70)
    content_font = get_font(45)
    
    # 标题
    draw.text((WIDTH//2, 100), "🔥 3 大核心变化", fill=COLORS['text_dark'], 
              font=title_font, anchor='mm', align='center')
    
    # 内容
    content = [
        "1️⃣ 备份功能上线",
        "openclaw backup create",
        "openclaw backup verify",
        "",
        "2️⃣ macOS Token 保护",
        "自动保留现有 Token",
        "替换前会警告",
        "",
        "3️⃣ TUI 自动识别",
        "进项目目录直接开用",
        "不用手动配 agent"
    ]
    
    y = 300
    for line in content:
        color = COLORS['primary'] if line.startswith(('1️⃣', '2️⃣', '3️⃣')) else COLORS['text_dark']
        draw.text((WIDTH//2, y), line, fill=color, 
                  font=content_font, anchor='mm', align='center')
        y += 80 if line else 40
    
    # 保存
    img.save('images/xiaohongshu_p2.jpg', quality=95)
    print("✅ P2 内容图已生成")
    return 'images/xiaohongshu_p2.jpg'

def create_content_image_2():
    """P3: 常见问题"""
    img = Image.new('RGB', (WIDTH, HEIGHT), COLORS['background_light'])
    draw = ImageDraw.Draw(img)
    
    title_font = get_font(70)
    content_font = get_font(45)
    
    # 标题
    draw.text((WIDTH//2, 100), "⚠️ 常见问题", fill=COLORS['text_dark'], 
              font=title_font, anchor='mm', align='center')
    
    # 内容
    content = [
        "Q: 配置不生效？",
        "A: openclaw gateway restart",
        "",
        "Q: 找不到命令？",
        "A: openclaw --version",
        "",
        "Q: 备份在哪？",
        "A: ls ~/.openclaw/backups/",
        "",
        "Q: 如何升级？",
        "A: npm install -g openclaw@latest"
    ]
    
    y = 250
    for line in content:
        if line.startswith('Q:'):
            color = COLORS['primary']
            font = get_font(50)
        elif line.startswith('A:'):
            color = COLORS['text_dark']
            font = get_font(45)
        else:
            color = COLORS['text_dark']
            font = content_font
        
        draw.text((WIDTH//2, y), line, fill=color, 
                  font=font, anchor='mm', align='center')
        y += 90 if line else 40
    
    # 保存
    img.save('images/xiaohongshu_p3.jpg', quality=95)
    print("✅ P3 内容图已生成")
    return 'images/xiaohongshu_p3.jpg'

def create_content_image_3():
    """P4: 快速上手步骤"""
    img = Image.new('RGB', (WIDTH, HEIGHT), COLORS['background_light'])
    draw = ImageDraw.Draw(img)
    
    title_font = get_font(70)
    content_font = get_font(50)
    
    # 标题
    draw.text((WIDTH//2, 100), "🎯 4 步快速上手", fill=COLORS['text_dark'], 
              font=title_font, anchor='mm', align='center')
    
    # 步骤
    steps = [
        ("1", "备份", "openclaw backup create"),
        ("2", "升级", "npm install -g openclaw@latest"),
        ("3", "重启", "openclaw gateway restart"),
        ("4", "测试", "openclaw tui")
    ]
    
    y = 250
    for num, title, cmd in steps:
        # 序号圆圈
        draw.ellipse([(WIDTH//2 - 200, y - 40), (WIDTH//2 - 150, y + 10)], 
                    fill=COLORS['primary'])
        draw.text((WIDTH//2 - 175, y), num, fill='white', 
                  font=get_font(35), anchor='mm', align='center')
        
        # 标题和命令
        draw.text((WIDTH//2 - 100, y), title, fill=COLORS['text_dark'], 
                  font=content_font, anchor='lm', align='left')
        draw.text((WIDTH//2 - 100, y + 60), cmd, fill=COLORS['primary_light'], 
                  font=get_font(40), anchor='lm', align='left')
        
        y += 150
    
    # 保存
    img.save('images/xiaohongshu_p4.jpg', quality=95)
    print("✅ P4 内容图已生成")
    return 'images/xiaohongshu_p4.jpg'

def create_content_image_4():
    """P5: 资源指路"""
    img = Image.new('RGB', (WIDTH, HEIGHT), COLORS['primary'])
    draw = ImageDraw.Draw(img)
    
    title_font = get_font(70)
    content_font = get_font(50)
    small_font = get_font(35)
    
    # 标题
    draw.text((WIDTH//2, 200), "📍 资源指路", fill='white', 
              font=title_font, anchor='mm', align='center')
    
    # 内容
    resources = [
        "GitHub",
        "@openclaw/openclaw",
        "",
        "文档",
        "docs.openclaw.ai",
        "",
        "社区",
        "Discord 蹲更新"
    ]
    
    y = 400
    for line in resources:
        font = content_font if line in ['GitHub', '文档', '社区'] else small_font
        draw.text((WIDTH//2, y), line, fill='white', 
                  font=font, anchor='mm', align='center')
        y += 70 if line else 30
    
    # 底部
    draw.text((WIDTH//2, HEIGHT - 200), "有问题评论区问！", 
              fill='white', font=content_font, anchor='mm', align='center')
    draw.text((WIDTH//2, HEIGHT - 120), "看到就回，一起避坑💪", 
              fill='white', font=small_font, anchor='mm', align='center')
    
    # 保存
    img.save('images/xiaohongshu_p5.jpg', quality=95)
    print("✅ P5 结尾图已生成")
    return 'images/xiaohongshu_p5.jpg'

if __name__ == "__main__":
    print("🎨 开始生成小红书配图...")
    print("=" * 60)
    
    images = [
        create_cover_image(),
        create_content_image_1(),
        create_content_image_2(),
        create_content_image_3(),
        create_content_image_4()
    ]
    
    print("=" * 60)
    print(f"✅ 已生成 {len(images)} 张图片:")
    for img in images:
        size = os.path.getsize(img) / 1024
        print(f"   - {img} ({size:.1f} KB)")
    
    print("\n📕 图片已准备就绪，可以发布了！")
