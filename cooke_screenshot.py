#!/usr/bin/env python3
"""
Cooke 镜头图片自动截图并插入 Excel
"""

import os
import subprocess
import time
from openpyxl import load_workbook
from openpyxl.drawing.image import Image as XLImage
import re

# 镜头列表
LENSES = {
    "SP3": [
        ("18mm", "sp3-18mm"),
        ("25mm", "sp3-25mm"),
        ("32mm", "sp3-32mm"),
        ("50mm", "sp3-50mm"),
        ("75mm", "sp3-75mm"),
        ("100mm", "sp3-100mm"),
    ],
    "Panchro65": [
        ("35mm", "panchro-65"),
        ("50mm", "panchro-65"),
        ("65mm", "panchro-65"),
    ],
    "S8iFF": [
        ("21mm", "s8i-ff"),
        ("32mm", "s8i-ff"),
        ("47mm", "s8i-ff"),
        ("65mm", "s8i-ff"),
    ],
    "S4i": [
        ("14mm", "s4i"),
        ("15mm", "s4i"),
        ("18mm", "s4i"),
        ("21mm", "s4i"),
        ("25mm", "s4i"),
        ("32mm", "s4i"),
        ("40mm", "s4i"),
        ("50mm", "s4i"),
        ("65mm", "s4i"),
        ("75mm", "s4i"),
        ("100mm", "s4i"),
        ("135mm", "s4i"),
    ],
}

# 截图保存目录
SCREENSHOT_DIR = os.path.expanduser("~/Desktop/cooke_lens_screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def take_screenshot(filename):
    """使用 macOS screencapture 截图"""
    filepath = os.path.join(SCREENSHOT_DIR, filename)
    # 这里需要配合浏览器自动化来截图
    # 简化版本：使用固定的截图区域
    print(f"截图：{filepath}")
    return filepath

def find_lens_row(ws, lens_name, focal_length):
    """在 Excel 中查找镜头所在行"""
    for row in range(2, ws.max_row + 1):
        cell_value = str(ws.cell(row=row, column=2).value)  # B 列是镜头名称
        if lens_name in cell_value and focal_length in cell_value:
            return row
    return None

def insert_image_to_excel(excel_path, lens_images):
    """将截图插入 Excel"""
    wb = load_workbook(excel_path)
    ws = wb.active
    
    for lens_key, screenshot_path in lens_images.items():
        if not os.path.exists(screenshot_path):
            print(f"跳过不存在的图片：{screenshot_path}")
            continue
            
        # 解析镜头信息
        parts = lens_key.split("_")
        if len(parts) >= 2:
            series = parts[0]
            focal = parts[1].replace("mm", "")
            
            # 查找对应行
            row = find_lens_row(ws, series, focal)
            if row:
                # 插入图片到 A 列
                img = XLImage(screenshot_path)
                # 调整图片大小
                img.width = 70
                img.height = 70
                # 设置位置
                ws.add_image(img, f'A{row}')
                print(f"已插入：{lens_key} -> 行{row}")
            else:
                print(f"未找到镜头：{lens_key}")
    
    # 保存
    output_path = excel_path.replace(".xlsx", "_with_images.xlsx")
    wb.save(output_path)
    print(f"已保存：{output_path}")
    return output_path

if __name__ == "__main__":
    print("Cooke 镜头图片自动截图工具")
    print(f"截图保存目录：{SCREENSHOT_DIR}")
    
    # 示例：截图并插入
    excel_file = os.path.expanduser("~/Desktop/Cooke_Optics_镜头数据库_官网图片版_20260305_000240.xlsx")
    
    if os.path.exists(excel_file):
        print(f"找到 Excel 文件：{excel_file}")
        # 这里需要实际的截图文件
        # insert_image_to_excel(excel_file, {})
    else:
        print(f"未找到 Excel 文件：{excel_file}")
