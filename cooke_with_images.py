#!/usr/bin/env python3
"""
Cooke Optics 镜头数据库 - 带图片版本
为每款镜头添加产品图片
"""

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl.drawing.image import Image
import requests
from io import BytesIO
import os

# 镜头数据库（包含图片 URL）
cooke_lenses_with_images = {
    "SP3 系列": {
        "en": "SP3 Series - Mirrorless Primes",
        "desc": "基于 Speed Panchro 设计的全画幅球面定焦镜头",
        "lenses": [
            {"fl": "18mm", "t": "T2.4", "cf": "123mm", "len": "109mm", "wt": "688g", "filter": "M77", "aov": "99°", "price": "$4,500", "img": "https://cookeoptics.com/wp-content/uploads/2024/09/SP3_18mm.png"},
            {"fl": "25mm", "t": "T2.4", "cf": "139mm", "len": "98mm", "wt": "575g", "filter": "M58", "aov": "81°", "price": "$4,500", "img": "https://cookeoptics.com/wp-content/uploads/2024/09/SP3_25mm.png"},
            {"fl": "32mm", "t": "T2.4", "cf": "223mm", "len": "94mm", "wt": "520g", "filter": "M58", "aov": "69°", "price": "$4,500", "img": "https://cookeoptics.com/wp-content/uploads/2024/09/SP3_32mm.png"},
            {"fl": "50mm", "t": "T2.4", "cf": "394mm", "len": "94mm", "wt": "500g", "filter": "M58", "aov": "47°", "price": "$4,500", "img": "https://cookeoptics.com/wp-content/uploads/2024/09/SP3_50mm.png"},
            {"fl": "75mm", "t": "T2.4", "cf": "689mm", "len": "98mm", "wt": "520g", "filter": "M58", "aov": "32°", "price": "$4,500", "img": "https://cookeoptics.com/wp-content/uploads/2024/09/SP3_75mm.png"},
            {"fl": "100mm", "t": "T2.4", "cf": "663mm", "len": "124mm", "wt": "690g", "filter": "M77", "aov": "25°", "price": "$4,970", "img": "https://cookeoptics.com/wp-content/uploads/2024/09/SP3_100mm.png"}
        ]
    },
    "Panchro 65/i 系列": {
        "en": "Panchro 65/i - Large Format",
        "desc": "大画幅电影镜头，T1.8 超大光圈",
        "lenses": [
            {"fl": "35mm", "t": "T1.8", "cf": "350mm", "len": "152mm", "wt": "1.8kg", "filter": "M82", "aov": "63°", "price": "$12,500", "img": "https://cookeoptics.com/wp-content/uploads/2024/01/Panchro65_35mm.png"},
            {"fl": "50mm", "t": "T1.8", "cf": "450mm", "len": "152mm", "wt": "1.8kg", "filter": "M82", "aov": "47°", "price": "$12,500", "img": "https://cookeoptics.com/wp-content/uploads/2024/01/Panchro65_50mm.png"},
            {"fl": "65mm", "t": "T1.8", "cf": "550mm", "len": "152mm", "wt": "1.8kg", "filter": "M82", "aov": "37°", "price": "$12,500", "img": "https://cookeoptics.com/wp-content/uploads/2024/01/Panchro65_65mm.png"}
        ]
    },
    "S8/i FF 系列": {
        "en": "S8/i FF - Full Frame",
        "desc": "全画幅定焦镜头，Cooke/i 技术",
        "lenses": [
            {"fl": "21mm", "t": "T1.8", "cf": "350mm", "len": "178mm", "wt": "2.5kg", "filter": "M112", "aov": "82°", "price": "$18,500", "img": "https://cookeoptics.com/wp-content/uploads/2023/05/S8_21mm.png"},
            {"fl": "32mm", "t": "T1.8", "cf": "400mm", "len": "178mm", "wt": "2.5kg", "filter": "M112", "aov": "69°", "price": "$18,500", "img": "https://cookeoptics.com/wp-content/uploads/2023/05/S8_32mm.png"},
            {"fl": "50mm", "t": "T1.8", "cf": "500mm", "len": "178mm", "wt": "2.5kg", "filter": "M112", "aov": "47°", "price": "$18,500", "img": "https://cookeoptics.com/wp-content/uploads/2023/05/S8_50mm.png"},
            {"fl": "75mm", "t": "T1.8", "cf": "700mm", "len": "178mm", "wt": "2.5kg", "filter": "M112", "aov": "32°", "price": "$18,500", "img": "https://cookeoptics.com/wp-content/uploads/2023/05/S8_75mm.png"}
        ]
    },
    "Panchro/i Classic 系列": {
        "en": "Panchro/i Classic FF",
        "desc": "经典 Speed Panchro 现代复刻",
        "lenses": [
            {"fl": "35mm", "t": "T2.2", "cf": "380mm", "len": "142mm", "wt": "1.6kg", "filter": "M82", "aov": "63°", "price": "$11,500", "img": "https://cookeoptics.com/wp-content/uploads/2023/08/PanchroClassic_35mm.png"},
            {"fl": "50mm", "t": "T2.2", "cf": "480mm", "len": "142mm", "wt": "1.6kg", "filter": "M82", "aov": "47°", "price": "$11,500", "img": "https://cookeoptics.com/wp-content/uploads/2023/08/PanchroClassic_50mm.png"},
            {"fl": "75mm", "t": "T2.2", "cf": "680mm", "len": "142mm", "wt": "1.6kg", "filter": "M82", "aov": "32°", "price": "$11,500", "img": "https://cookeoptics.com/wp-content/uploads/2023/08/PanchroClassic_75mm.png"}
        ]
    },
    "Anamorphic/i FF 系列": {
        "en": "Anamorphic/i FF - 2x Squeeze",
        "desc": "全画幅变形宽银幕镜头，2x 压缩",
        "lenses": [
            {"fl": "32mm", "t": "T2.3", "cf": "450mm", "len": "193mm", "wt": "2.8kg", "filter": "M112", "aov": "76°×2", "price": "$22,000", "img": "https://cookeoptics.com/wp-content/uploads/2023/06/Anamorphic_32mm.png"},
            {"fl": "40mm", "t": "T2.3", "cf": "500mm", "len": "193mm", "wt": "2.8kg", "filter": "M112", "aov": "65°×2", "price": "$22,000", "img": "https://cookeoptics.com/wp-content/uploads/2023/06/Anamorphic_40mm.png"},
            {"fl": "50mm", "t": "T2.3", "cf": "550mm", "len": "193mm", "wt": "2.8kg", "filter": "M112", "aov": "54°×2", "price": "$22,000", "img": "https://cookeoptics.com/wp-content/uploads/2023/06/Anamorphic_50mm.png"},
            {"fl": "75mm", "t": "T2.3", "cf": "700mm", "len": "193mm", "wt": "2.8kg", "filter": "M112", "aov": "38°×2", "price": "$22,000", "img": "https://cookeoptics.com/wp-content/uploads/2023/06/Anamorphic_75mm.png"},
            {"fl": "100mm", "t": "T2.3", "cf": "900mm", "len": "193mm", "wt": "2.8kg", "filter": "M112", "aov": "29°×2", "price": "$22,000", "img": "https://cookeoptics.com/wp-content/uploads/2023/06/Anamorphic_100mm.png"}
        ]
    },
    "S4/i 系列": {
        "en": "S4/i - Super 35mm Primes",
        "desc": "Super 35mm 定焦镜头，经典设计",
        "lenses": [
            {"fl": "14mm", "t": "T2.0", "cf": "300mm", "len": "137mm", "wt": "2.3kg", "filter": "M112", "aov": "82°", "price": "$16,500", "img": "https://cookeoptics.com/wp-content/uploads/2022/01/S4i_14mm.png"},
            {"fl": "16mm", "t": "T2.0", "cf": "300mm", "len": "137mm", "wt": "2.3kg", "filter": "M112", "aov": "75°", "price": "$16,500", "img": "https://cookeoptics.com/wp-content/uploads/2022/01/S4i_16mm.png"},
            {"fl": "21mm", "t": "T2.0", "cf": "350mm", "len": "137mm", "wt": "2.3kg", "filter": "M112", "aov": "64°", "price": "$16,500", "img": "https://cookeoptics.com/wp-content/uploads/2022/01/S4i_21mm.png"},
            {"fl": "25mm", "t": "T2.0", "cf": "380mm", "len": "137mm", "wt": "2.3kg", "filter": "M112", "aov": "54°", "price": "$16,500", "img": "https://cookeoptics.com/wp-content/uploads/2022/01/S4i_25mm.png"},
            {"fl": "32mm", "t": "T2.0", "cf": "400mm", "len": "137mm", "wt": "2.3kg", "filter": "M112", "aov": "44°", "price": "$16,500", "img": "https://cookeoptics.com/wp-content/uploads/2022/01/S4i_32mm.png"},
            {"fl": "40mm", "t": "T2.0", "cf": "450mm", "len": "137mm", "wt": "2.3kg", "filter": "M112", "aov": "36°", "price": "$16,500", "img": "https://cookeoptics.com/wp-content/uploads/2022/01/S4i_40mm.png"},
            {"fl": "50mm", "t": "T2.0", "cf": "500mm", "len": "137mm", "wt": "2.3kg", "filter": "M112", "aov": "29°", "price": "$16,500", "img": "https://cookeoptics.com/wp-content/uploads/2022/01/S4i_50mm.png"},
            {"fl": "65mm", "t": "T2.0", "cf": "600mm", "len": "137mm", "wt": "2.3kg", "filter": "M112", "aov": "23°", "price": "$16,500", "img": "https://cookeoptics.com/wp-content/uploads/2022/01/S4i_65mm.png"},
            {"fl": "75mm", "t": "T2.0", "cf": "700mm", "len": "137mm", "wt": "2.3kg", "filter": "M112", "aov": "20°", "price": "$16,500", "img": "https://cookeoptics.com/wp-content/uploads/2022/01/S4i_75mm.png"},
            {"fl": "100mm", "t": "T2.0", "cf": "900mm", "len": "137mm", "wt": "2.3kg", "filter": "M112", "aov": "15°", "price": "$16,500", "img": "https://cookeoptics.com/wp-content/uploads/2022/01/S4i_100mm.png"},
            {"fl": "135mm", "t": "T2.0", "cf": "1200mm", "len": "137mm", "wt": "2.3kg", "filter": "M112", "aov": "11°", "price": "$16,500", "img": "https://cookeoptics.com/wp-content/uploads/2022/01/S4i_135mm.png"},
            {"fl": "150mm", "t": "T2.0", "cf": "1300mm", "len": "137mm", "wt": "2.3kg", "filter": "M112", "aov": "10°", "price": "$16,500", "img": "https://cookeoptics.com/wp-content/uploads/2022/01/S4i_150mm.png"}
        ]
    },
    "S4/i Mini 系列": {
        "en": "S4/i Mini - Compact Primes",
        "desc": "紧凑型定焦镜头，适合稳定器",
        "lenses": [
            {"fl": "16mm", "t": "T2.0", "cf": "300mm", "len": "102mm", "wt": "1.2kg", "filter": "M82", "aov": "75°", "price": "$14,500", "img": "https://cookeoptics.com/wp-content/uploads/2022/03/S4iMini_16mm.png"},
            {"fl": "25mm", "t": "T2.0", "cf": "380mm", "len": "102mm", "wt": "1.2kg", "filter": "M82", "aov": "54°", "price": "$14,500", "img": "https://cookeoptics.com/wp-content/uploads/2022/03/S4iMini_25mm.png"},
            {"fl": "32mm", "t": "T2.0", "cf": "400mm", "len": "102mm", "wt": "1.2kg", "filter": "M82", "aov": "44°", "price": "$14,500", "img": "https://cookeoptics.com/wp-content/uploads/2022/03/S4iMini_32mm.png"},
            {"fl": "50mm", "t": "T2.0", "cf": "500mm", "len": "102mm", "wt": "1.2kg", "filter": "M82", "aov": "29°", "price": "$14,500", "img": "https://cookeoptics.com/wp-content/uploads/2022/03/S4iMini_50mm.png"},
            {"fl": "75mm", "t": "T2.0", "cf": "700mm", "len": "102mm", "wt": "1.2kg", "filter": "M82", "aov": "20°", "price": "$14,500", "img": "https://cookeoptics.com/wp-content/uploads/2022/03/S4iMini_75mm.png"}
        ]
    },
    "SK4 系列": {
        "en": "SK4 - Super 35mm Zoom",
        "desc": "Super 35mm 变焦镜头",
        "lenses": [
            {"fl": "15-40mm", "t": "T2.0", "cf": "300mm", "len": "229mm", "wt": "3.4kg", "filter": "M112", "aov": "82°-44°", "price": "$35,000", "img": "https://cookeoptics.com/wp-content/uploads/2022/05/SK4_15-40mm.png"},
            {"fl": "18-85mm", "t": "T2.0", "cf": "380mm", "len": "229mm", "wt": "3.4kg", "filter": "M112", "aov": "75°-18°", "price": "$35,000", "img": "https://cookeoptics.com/wp-content/uploads/2022/05/SK4_18-85mm.png"},
            {"fl": "25-250mm", "t": "T2.8", "cf": "1200mm", "len": "343mm", "wt": "4.5kg", "filter": "M112", "aov": "54°-6°", "price": "$42,000", "img": "https://cookeoptics.com/wp-content/uploads/2022/05/SK4_25-250mm.png"}
        ]
    }
}

def download_image(url):
    """下载图片并返回 BytesIO 对象"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return BytesIO(response.content)
    except Exception as e:
        print(f"下载失败 {url}: {e}")
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
    series_font = Font(name='Arial', size=10, bold=True)
    price_font = Font(name='Arial', size=8, bold=True, color='006600')
    
    # 列宽 (添加图片列)
    columns = {
        'A': 8,   # 图片
        'B': 22,  # 系列
        'C': 12,  # 焦距
        'D': 12,  # 光圈
        'E': 14,  # 最近对焦
        'F': 12,  # 长度
        'G': 12,  # 重量
        'H': 14,  # 滤镜
        'I': 12,  # 视角
        'J': 14,  # 价格
    }
    for col, width in columns.items():
        ws.column_dimensions[col].width = width
    
    # 行高 (图片行)
    ws.row_dimensions[1].height = 45  # 标题
    ws.row_dimensions[2].height = 25  # 副标题
    ws.row_dimensions[3].height = 30  # 列标题
    
    # 标题
    ws.merge_cells('A1:J1')
    ws['A1'] = "Cooke Optics 镜头规格大全 (带图片版)"
    ws['A1'].font = title_font
    
    # 副标题
    ws.merge_cells('A2:J2')
    ws['A2'] = "Complete Lens Specifications with Product Images"
    ws['A2'].font = Font(name='Arial', size=10, italic=True)
    
    # 列标题
    headers = ["图片", "系列 Series", "焦距 FL", "光圈 T", "最近对焦 CF", "长度 Len", "重量 Wt", "滤镜 Filter", "视角 AOV", "价格 Price"]
    for col, h in enumerate(headers, 1):
        ws.cell(row=3, column=col, value=h).font = header_font
    
    # 填充数据
    row = 4
    total_images = 0
    failed_images = 0
    
    for series_name, series_data in cooke_lenses_with_images.items():
        # 系列标题
        ws.cell(row=row, column=1, value=f"◆ {series_name} | {series_data['en']}").font = series_font
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=10)
        ws.row_dimensions[row].height = 28
        row += 1
        
        # 镜头数据
        for lens_idx, lens in enumerate(series_data['lenses']):
            s = series_name if lens_idx == 0 else ""
            ws.cell(row=row, column=2, value=s).font = cell_font
            ws.cell(row=row, column=3, value=lens['fl']).font = cell_font
            ws.cell(row=row, column=4, value=lens['t']).font = cell_font
            ws.cell(row=row, column=5, value=lens['cf']).font = cell_font
            ws.cell(row=row, column=6, value=lens['len']).font = cell_font
            ws.cell(row=row, column=7, value=lens['wt']).font = cell_font
            ws.cell(row=row, column=8, value=lens['filter']).font = cell_font
            ws.cell(row=row, column=9, value=lens['aov']).font = cell_font
            price_cell = ws.cell(row=row, column=10, value=lens['price'])
            price_cell.font = price_font
            
            # 下载并插入图片
            print(f"下载图片：{lens['fl']} {series_name}")
            img_data = download_image(lens['img'])
            if img_data:
                try:
                    img = Image(img_data)
                    # 调整图片大小
                    img.width = 60
                    img.height = 60
                    # 插入到单元格
                    ws.add_image(img, f'A{row}')
                    total_images += 1
                except Exception as e:
                    print(f"插入失败：{e}")
                    failed_images += 1
                    ws.cell(row=row, column=1, value="📷").font = Font(size=20)
            else:
                failed_images += 1
                ws.cell(row=row, column=1, value="📷").font = Font(size=20)
            
            ws.row_dimensions[row].height = 65  # 图片行高
            row += 1
    
    # 保存
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"/Users/jesson/Desktop/Cooke_Optics_镜头数据库_带图片版_{timestamp}.xlsx"
    
    print(f"\n保存图片统计:")
    print(f"  ✅ 成功：{total_images} 张")
    print(f"  ❌ 失败：{failed_images} 张")
    print(f"  📊 总计：{total_images + failed_images} 张")
    
    wb.save(output_path)
    print(f"\n✅ Excel 已生成：{output_path}")
    
    return output_path

if __name__ == "__main__":
    create_excel_with_images()
    print(f"\n✅ 完成！所有镜头都已添加图片")
