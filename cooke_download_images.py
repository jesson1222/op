#!/usr/bin/env python3
"""
Cooke 镜头图片批量下载并插入 Excel
从官网下载所有镜头图片
"""

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.drawing.image import Image
from openpyxl.utils import get_column_letter
import requests
from io import BytesIO
from datetime import datetime
import os

# 镜头数据库（官网图片 URL）
cooke_lenses = {
    "SP3 系列": {"en": "SP3 Series", "lenses": [
        {"fl": "18mm", "img": "https://cookeoptics.com/wp-content/uploads/2024/09/SP3-18mm-T2.4-Full-Frame-Prime-Lens-1.png"},
        {"fl": "25mm", "img": "https://cookeoptics.com/wp-content/uploads/2024/09/SP3-25mm-T2.4-Full-Frame-Prime-Lens-1.png"},
        {"fl": "32mm", "img": "https://cookeoptics.com/wp-content/uploads/2024/09/SP3-32mm-T2.4-Full-Frame-Prime-Lens-1.png"},
        {"fl": "50mm", "img": "https://cookeoptics.com/wp-content/uploads/2024/09/SP3-50mm-T2.4-Full-Frame-Prime-Lens-1.png"},
        {"fl": "75mm", "img": "https://cookeoptics.com/wp-content/uploads/2024/09/SP3-75mm-T2.4-Full-Frame-Prime-Lens-1.png"},
        {"fl": "100mm", "img": "https://cookeoptics.com/wp-content/uploads/2024/09/SP3-100mm-T2.4-Full-Frame-Prime-Lens-1.png"}
    ]},
    "Panchro 65/i": {"en": "Panchro 65/i", "lenses": [
        {"fl": "35mm", "img": "https://cookeoptics.com/wp-content/uploads/2024/01/Panchro-65i-35mm-T1.8-1.png"},
        {"fl": "50mm", "img": "https://cookeoptics.com/wp-content/uploads/2024/01/Panchro-65i-50mm-T1.8-1.png"},
        {"fl": "65mm", "img": "https://cookeoptics.com/wp-content/uploads/2024/01/Panchro-65i-65mm-T1.8-1.png"}
    ]},
    "S8/i FF": {"en": "S8/i FF", "lenses": [
        {"fl": "21mm", "img": "https://cookeoptics.com/wp-content/uploads/2023/05/S8i-FF-21mm-T1.8-1.png"},
        {"fl": "32mm", "img": "https://cookeoptics.com/wp-content/uploads/2023/05/S8i-FF-32mm-T1.8-1.png"},
        {"fl": "50mm", "img": "https://cookeoptics.com/wp-content/uploads/2023/05/S8i-FF-50mm-T1.8-1.png"},
        {"fl": "75mm", "img": "https://cookeoptics.com/wp-content/uploads/2023/05/S8i-FF-75mm-T1.8-1.png"}
    ]},
    "Panchro/i Classic": {"en": "Panchro/i Classic", "lenses": [
        {"fl": "35mm", "img": "https://cookeoptics.com/wp-content/uploads/2023/08/Panchro-i-Classic-FF-35mm-T2.2-1.png"},
        {"fl": "50mm", "img": "https://cookeoptics.com/wp-content/uploads/2023/08/Panchro-i-Classic-FF-50mm-T2.2-1.png"},
        {"fl": "75mm", "img": "https://cookeoptics.com/wp-content/uploads/2023/08/Panchro-i-Classic-FF-75mm-T2.2-1.png"}
    ]},
    "Anamorphic/i FF": {"en": "Anamorphic/i FF", "lenses": [
        {"fl": "32mm", "img": "https://cookeoptics.com/wp-content/uploads/2023/06/Anamorphic-i-FF-32mm-T2.3-1.png"},
        {"fl": "40mm", "img": "https://cookeoptics.com/wp-content/uploads/2023/06/Anamorphic-i-FF-40mm-T2.3-1.png"},
        {"fl": "50mm", "img": "https://cookeoptics.com/wp-content/uploads/2023/06/Anamorphic-i-FF-50mm-T2.3-1.png"},
        {"fl": "75mm", "img": "https://cookeoptics.com/wp-content/uploads/2023/06/Anamorphic-i-FF-75mm-T2.3-1.png"},
        {"fl": "100mm", "img": "https://cookeoptics.com/wp-content/uploads/2023/06/Anamorphic-i-FF-100mm-T2.3-1.png"}
    ]},
    "S4/i": {"en": "S4/i", "lenses": [
        {"fl": "14mm", "img": "https://cookeoptics.com/wp-content/uploads/2022/01/S4i-14mm-T2.0-1.png"},
        {"fl": "16mm", "img": "https://cookeoptics.com/wp-content/uploads/2022/01/S4i-16mm-T2.0-1.png"},
        {"fl": "21mm", "img": "https://cookeoptics.com/wp-content/uploads/2022/01/S4i-21mm-T2.0-1.png"},
        {"fl": "25mm", "img": "https://cookeoptics.com/wp-content/uploads/2022/01/S4i-25mm-T2.0-1.png"},
        {"fl": "32mm", "img": "https://cookeoptics.com/wp-content/uploads/2022/01/S4i-32mm-T2.0-1.png"},
        {"fl": "40mm", "img": "https://cookeoptics.com/wp-content/uploads/2022/01/S4i-40mm-T2.0-1.png"},
        {"fl": "50mm", "img": "https://cookeoptics.com/wp-content/uploads/2022/01/S4i-50mm-T2.0-1.png"},
        {"fl": "65mm", "img": "https://cookeoptics.com/wp-content/uploads/2022/01/S4i-65mm-T2.0-1.png"},
        {"fl": "75mm", "img": "https://cookeoptics.com/wp-content/uploads/2022/01/S4i-75mm-T2.0-1.png"},
        {"fl": "100mm", "img": "https://cookeoptics.com/wp-content/uploads/2022/01/S4i-100mm-T2.0-1.png"},
        {"fl": "135mm", "img": "https://cookeoptics.com/wp-content/uploads/2022/01/S4i-135mm-T2.0-1.png"},
        {"fl": "150mm", "img": "https://cookeoptics.com/wp-content/uploads/2022/01/S4i-150mm-T2.0-1.png"}
    ]},
    "S4/i Mini": {"en": "S4/i Mini", "lenses": [
        {"fl": "16mm", "img": "https://cookeoptics.com/wp-content/uploads/2022/03/S4i-Mini-16mm-T2.0-1.png"},
        {"fl": "25mm", "img": "https://cookeoptics.com/wp-content/uploads/2022/03/S4i-Mini-25mm-T2.0-1.png"},
        {"fl": "32mm", "img": "https://cookeoptics.com/wp-content/uploads/2022/03/S4i-Mini-32mm-T2.0-1.png"},
        {"fl": "50mm", "img": "https://cookeoptics.com/wp-content/uploads/2022/03/S4i-Mini-50mm-T2.0-1.png"},
        {"fl": "75mm", "img": "https://cookeoptics.com/wp-content/uploads/2022/03/S4i-Mini-75mm-T2.0-1.png"}
    ]},
    "SK4": {"en": "SK4 Zoom", "lenses": [
        {"fl": "15-40mm", "img": "https://cookeoptics.com/wp-content/uploads/2022/05/SK4-15-40mm-T2.0-1.png"},
        {"fl": "18-85mm", "img": "https://cookeoptics.com/wp-content/uploads/2022/05/SK4-18-85mm-T2.0-1.png"},
        {"fl": "25-250mm", "img": "https://cookeoptics.com/wp-content/uploads/2022/05/SK4-25-250mm-T2.8-1.png"}
    ]}
}

def download_image(url, timeout=10):
    """下载图片"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        if response.status_code == 200:
            return BytesIO(response.content)
        else:
            print(f"  ❌ HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"  ❌ {str(e)[:50]}")
        return None

def create_excel_with_images():
    """创建带图片的 Excel"""
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Cooke 镜头规格表 (带图片)"
    
    # 样式
    title_font = Font(name='Arial', size=16, bold=True)
    header_font = Font(name='Arial', size=9, bold=True)
    cell_font = Font(name='Arial', size=8)
    series_font = Font(name='Arial', size=10, bold=True, color='FFFFFF')
    price_font = Font(name='Arial', size=8, bold=True, color='006600')
    
    # 列宽
    cols = {'A': 12, 'B': 22, 'C': 12, 'D': 12, 'E': 14, 'F': 12, 'G': 12, 'H': 14, 'I': 12, 'J': 14}
    for c, w in cols.items():
        ws.column_dimensions[c].width = w
    
    # 标题
    ws.merge_cells('A1:J1')
    ws['A1'] = "📷 Cooke Optics 镜头规格大全 (官网图片版)"
    ws['A1'].font = title_font
    
    # 副标题
    ws.merge_cells('A2:J2')
    ws['A2'] = "Complete Lens Specifications with Official Product Images"
    ws['A2'].font = Font(name='Arial', size=10, italic=True)
    
    # 列标题
    headers = ["图片 Image", "系列 Series", "焦距 FL", "光圈 T", "最近对焦 CF", "长度 Len", "重量 Wt", "滤镜 Filter", "视角 AOV", "价格 Price"]
    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=3, column=col, value=h)
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center')
    
    # 填充数据
    row = 4
    total = 0
    success = 0
    failed = 0
    
    print("📥 开始下载并插入图片...\n")
    
    for series_name, series_data in cooke_lenses.items():
        # 系列标题
        ws.cell(row=row, column=1, value=f"◆ {series_name} | {series_data['en']}").font = series_font
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=10)
        ws.row_dimensions[row].height = 28
        row += 1
        
        # 镜头数据
        for i, lens in enumerate(series_data['lenses']):
            s = series_name if i == 0 else ""
            ws.cell(row=row, column=2, value=s).font = cell_font
            ws.cell(row=row, column=3, value=lens['fl']).font = cell_font
            ws.cell(row=row, column=4, value=lens.get('t', 'N/A')).font = cell_font
            ws.cell(row=row, column=5, value=lens.get('cf', 'N/A')).font = cell_font
            ws.cell(row=row, column=6, value=lens.get('len', 'N/A')).font = cell_font
            ws.cell(row=row, column=7, value=lens.get('wt', 'N/A')).font = cell_font
            ws.cell(row=row, column=8, value=lens.get('filter', 'N/A')).font = cell_font
            ws.cell(row=row, column=9, value=lens.get('aov', 'N/A')).font = cell_font
            
            price_val = lens.get('price', 'N/A')
            if price_val != 'N/A':
                pc = ws.cell(row=row, column=10, value=price_val)
                pc.font = price_font
            
            # 下载并插入图片
            print(f"📷 {series_name} - {lens['fl']}", end=" ")
            total += 1
            
            if 'img' in lens and lens['img']:
                img_data = download_image(lens['img'])
                if img_data:
                    try:
                        img = Image(img_data)
                        # 调整图片大小
                        img.width = 70
                        img.height = 70
                        # 插入到 A 列
                        ws.add_image(img, f'A{row}')
                        print("✅")
                        success += 1
                    except Exception as e:
                        print(f"❌ {str(e)[:30]}")
                        failed += 1
                        ws.cell(row=row, column=1, value="📷").font = Font(size=24)
                else:
                    failed += 1
                    ws.cell(row=row, column=1, value="📷").font = Font(size=24)
            else:
                failed += 1
                ws.cell(row=row, column=1, value="📷").font = Font(size=24)
            
            ws.row_dimensions[row].height = 75
            row += 1
    
    # 保存
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"/Users/jesson/Desktop/Cooke_Optics_镜头数据库_官网图片版_{timestamp}.xlsx"
    
    print(f"\n{'='*60}")
    print(f"📊 图片统计:")
    print(f"  ✅ 成功：{success} 张 ({success/total*100:.1f}%)")
    print(f"  ❌ 失败：{failed} 张")
    print(f"  📊 总计：{total} 张")
    print(f"\n💾 文件已保存：{output_path}")
    
    wb.save(output_path)
    
    # 打开文件
    os.system(f'open "{output_path}"')
    
    return output_path, success, failed, total

if __name__ == "__main__":
    path, success, failed, total = create_excel_with_images()
    print(f"\n✅ 完成！{success}/{total} 张图片已成功插入")
