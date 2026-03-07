#!/usr/bin/env python3
"""
Cooke 镜头截图处理并插入 Excel
"""

import os
from openpyxl import load_workbook
from openpyxl.drawing.image import Image as XLImage
from PIL import Image

# 截图文件映射
SCREENSHOTS = {
    "SP3": "/Users/jesson/.openclaw/media/browser/ad13cbeb-03a7-40c6-bb09-ff0947cd1e9b.jpg",
    "Panchro65": "/Users/jesson/.openclaw/media/browser/b6c9c3ec-4a74-4d51-b24b-0b1e2285984a.jpg",
    "S8iFF": "/Users/jesson/.openclaw/media/browser/c2882425-76ea-4b73-9387-eea8323f70d9.jpg",
    "S4i": "/Users/jesson/.openclaw/media/browser/3e241fd4-cee9-486f-a860-a26e8e8af57b.jpg",
}

# Excel 文件路径
EXCEL_FILE = os.path.expanduser("~/Desktop/Cooke_Optics_镜头数据库_官网图片版_20260305_000240.xlsx")
OUTPUT_FILE = os.path.expanduser("~/Desktop/Cooke_Optics_镜头数据库_带截图版_20260305.xlsx")

# 镜头系列在 Excel 中的起始行（根据实际文件调整）
SERIES_START_ROWS = {
    "SP3": 2,        # SP3 系列从第 2 行开始
    "Panchro65": 9,  # Panchro 65/i 从第 9 行开始
    "S8iFF": 13,     # S8/i FF 从第 13 行开始
    "S4i": 18,       # S4/i 从第 18 行开始
}

def resize_image(input_path, output_path, max_width=400):
    """调整图片大小"""
    with Image.open(input_path) as img:
        # 计算新高度（保持宽高比）
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        
        # 调整大小
        resized = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        # 保存
        resized.save(output_path, quality=90)
        return max_width, new_height

def insert_screenshots():
    """将截图插入 Excel"""
    if not os.path.exists(EXCEL_FILE):
        print(f"❌ 找不到 Excel 文件：{EXCEL_FILE}")
        return
    
    # 加载 Excel
    wb = load_workbook(EXCEL_FILE)
    ws = wb.active
    
    # 调整列宽以容纳图片
    ws.column_dimensions['A'].width = 50  # 加宽 A 列
    
    screenshots_dir = os.path.expanduser("~/Desktop/cooke_screenshots_resized")
    os.makedirs(screenshots_dir, exist_ok=True)
    
    inserted_count = 0
    
    for series, screenshot_path in SCREENSHOTS.items():
        if not os.path.exists(screenshot_path):
            print(f"⚠️  截图不存在：{screenshot_path}")
            continue
        
        # 调整图片大小
        resized_path = os.path.join(screenshots_dir, f"{series}_resized.jpg")
        width, height = resize_image(screenshot_path, resized_path, max_width=400)
        
        # 获取起始行
        start_row = SERIES_START_ROWS.get(series, 2)
        
        # 插入图片
        try:
            img = XLImage(resized_path)
            img.width = width
            img.height = height
            
            # 插入到 A 列起始行
            cell = f'A{start_row}'
            ws.add_image(img, cell)
            
            print(f"✅ 已插入 {series} 系列截图到 {cell}")
            inserted_count += 1
        except Exception as e:
            print(f"❌ 插入 {series} 失败：{e}")
    
    # 保存文件
    try:
        wb.save(OUTPUT_FILE)
        print(f"\n🎉 完成！已保存：{OUTPUT_FILE}")
        print(f"📊 成功插入 {inserted_count}/{len(SCREENSHOTS)} 个系列截图")
    except Exception as e:
        print(f"❌ 保存失败：{e}")

if __name__ == "__main__":
    print("=" * 60)
    print("Cooke 镜头截图处理工具")
    print("=" * 60)
    print(f"\n📁 Excel 文件：{EXCEL_FILE}")
    print(f"📸 截图数量：{len(SCREENSHOTS)}")
    print(f"📤 输出文件：{OUTPUT_FILE}")
    print("\n开始处理...\n")
    
    insert_screenshots()
