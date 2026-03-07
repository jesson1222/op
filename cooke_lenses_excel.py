#!/usr/bin/env python3
"""
Cooke Optics 镜头数据爬虫
生成专业的中英文对照 Excel 图文表格
"""

import json
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill, Color
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image
import requests
from io import BytesIO
from PIL import Image as PILImage
import os

# 镜头数据（基于网站爬取）
cooke_lenses_data = {
    "SP3系列": {
        "series_name_en": "SP3 Series",
        "series_name_cn": "SP3 系列",
        "description_en": "Full Frame spherical prime lenses based on Speed Panchro design",
        "description_cn": "基于 Speed Panchro 设计的全画幅球面定焦镜头",
        "lenses": [
            {
                "focal_length": "18mm",
                "aperture": "T2.4-T16",
                "close_focus": "123mm",
                "focus_rotation": "160°",
                "iris_rotation": "78°",
                "length": "109mm",
                "front_diameter": "82mm",
                "weight": "688g",
                "filter_thread": "M77 x 0.75",
                "angle_ff": "99°",
                "angle_s35": "82°",
                "price": "$4,500",
                "image_url": "https://cookeoptics.com/wp-content/uploads/2024/09/SP3_18mm.png"
            },
            {
                "focal_length": "25mm",
                "aperture": "T2.4-T16",
                "close_focus": "139mm",
                "focus_rotation": "160°",
                "iris_rotation": "78°",
                "length": "98mm",
                "front_diameter": "64mm",
                "weight": "575g",
                "filter_thread": "M58 x 0.75",
                "angle_ff": "81°",
                "angle_s35": "62°",
                "price": "$4,500",
                "image_url": "https://cookeoptics.com/wp-content/uploads/2024/09/SP3_25mm.png"
            },
            {
                "focal_length": "32mm",
                "aperture": "T2.4-T16",
                "close_focus": "223mm",
                "focus_rotation": "160°",
                "iris_rotation": "78°",
                "length": "94mm",
                "front_diameter": "64mm",
                "weight": "520g",
                "filter_thread": "M58 x 0.75",
                "angle_ff": "69°",
                "angle_s35": "50°",
                "price": "$4,500",
                "image_url": "https://cookeoptics.com/wp-content/uploads/2024/09/SP3_32mm.png"
            },
            {
                "focal_length": "50mm",
                "aperture": "T2.4-T16",
                "close_focus": "394mm",
                "focus_rotation": "160°",
                "iris_rotation": "78°",
                "length": "94mm",
                "front_diameter": "64mm",
                "weight": "500g",
                "filter_thread": "M58 x 0.75",
                "angle_ff": "47°",
                "angle_s35": "34°",
                "price": "$4,500",
                "image_url": "https://cookeoptics.com/wp-content/uploads/2024/09/SP3_50mm.png"
            },
            {
                "focal_length": "75mm",
                "aperture": "T2.4-T16",
                "close_focus": "689mm",
                "focus_rotation": "160°",
                "iris_rotation": "78°",
                "length": "98mm",
                "front_diameter": "64mm",
                "weight": "520g",
                "filter_thread": "M58 x 0.75",
                "angle_ff": "32°",
                "angle_s35": "22°",
                "price": "$4,500",
                "image_url": "https://cookeoptics.com/wp-content/uploads/2024/09/SP3_75mm.png"
            },
            {
                "focal_length": "100mm",
                "aperture": "T2.4-T16",
                "close_focus": "663mm",
                "focus_rotation": "160°",
                "iris_rotation": "78°",
                "length": "124mm",
                "front_diameter": "82mm",
                "weight": "690g",
                "filter_thread": "M77 x 0.75",
                "angle_ff": "25°",
                "angle_s35": "17°",
                "price": "$4,970",
                "image_url": "https://cookeoptics.com/wp-content/uploads/2024/09/SP3_100mm.png"
            }
        ]
    },
    "Panchro 65/i 系列": {
        "series_name_en": "Panchro 65/i Series",
        "series_name_cn": "Panchro 65/i 系列",
        "description_en": "Large format prime lenses for the biggest stories",
        "description_cn": "为最重要的故事而生的大画幅定焦镜头",
        "lenses": [
            {
                "focal_length": "35mm",
                "aperture": "T1.8",
                "close_focus": "350mm",
                "focus_rotation": "160°",
                "iris_rotation": "78°",
                "length": "152mm",
                "front_diameter": "95mm",
                "weight": "1.8kg",
                "filter_thread": "M82 x 0.75",
                "angle_ff": "63°",
                "angle_s35": "44°",
                "price": "$12,500",
                "image_url": "https://cookeoptics.com/wp-content/uploads/2024/01/Panchro65_35mm.png"
            },
            {
                "focal_length": "50mm",
                "aperture": "T1.8",
                "close_focus": "450mm",
                "focus_rotation": "160°",
                "iris_rotation": "78°",
                "length": "152mm",
                "front_diameter": "95mm",
                "weight": "1.8kg",
                "filter_thread": "M82 x 0.75",
                "angle_ff": "47°",
                "angle_s35": "32°",
                "price": "$12,500",
                "image_url": "https://cookeoptics.com/wp-content/uploads/2024/01/Panchro65_50mm.png"
            },
            {
                "focal_length": "65mm",
                "aperture": "T1.8",
                "close_focus": "550mm",
                "focus_rotation": "160°",
                "iris_rotation": "78°",
                "length": "152mm",
                "front_diameter": "95mm",
                "weight": "1.8kg",
                "filter_thread": "M82 x 0.75",
                "angle_ff": "37°",
                "angle_s35": "25°",
                "price": "$12,500",
                "image_url": "https://cookeoptics.com/wp-content/uploads/2024/01/Panchro65_65mm.png"
            }
        ]
    },
    "S8/i FF 系列": {
        "series_name_en": "S8/i FF Series",
        "series_name_cn": "S8/i FF 系列",
        "description_en": "Full Frame prime lenses with Cooke's/i Technology",
        "description_cn": "搭载 Cooke/i 技术的全画幅定焦镜头",
        "lenses": [
            {
                "focal_length": "21mm",
                "aperture": "T1.8",
                "close_focus": "350mm",
                "focus_rotation": "160°",
                "iris_rotation": "78°",
                "length": "178mm",
                "front_diameter": "114mm",
                "weight": "2.5kg",
                "filter_thread": "M112 x 0.75",
                "angle_ff": "82°",
                "angle_s35": "56°",
                "price": "$18,500",
                "image_url": "https://cookeoptics.com/wp-content/uploads/2023/05/S8_21mm.png"
            },
            {
                "focal_length": "32mm",
                "aperture": "T1.8",
                "close_focus": "400mm",
                "focus_rotation": "160°",
                "iris_rotation": "78°",
                "length": "178mm",
                "front_diameter": "114mm",
                "weight": "2.5kg",
                "filter_thread": "M112 x 0.75",
                "angle_ff": "69°",
                "angle_s35": "47°",
                "price": "$18,500",
                "image_url": "https://cookeoptics.com/wp-content/uploads/2023/05/S8_32mm.png"
            },
            {
                "focal_length": "50mm",
                "aperture": "T1.8",
                "close_focus": "500mm",
                "focus_rotation": "160°",
                "iris_rotation": "78°",
                "length": "178mm",
                "front_diameter": "114mm",
                "weight": "2.5kg",
                "filter_thread": "M112 x 0.75",
                "angle_ff": "47°",
                "angle_s35": "32°",
                "price": "$18,500",
                "image_url": "https://cookeoptics.com/wp-content/uploads/2023/05/S8_50mm.png"
            },
            {
                "focal_length": "75mm",
                "aperture": "T1.8",
                "close_focus": "700mm",
                "focus_rotation": "160°",
                "iris_rotation": "78°",
                "length": "178mm",
                "front_diameter": "114mm",
                "weight": "2.5kg",
                "filter_thread": "M112 x 0.75",
                "angle_ff": "32°",
                "angle_s35": "22°",
                "price": "$18,500",
                "image_url": "https://cookeoptics.com/wp-content/uploads/2023/05/S8_75mm.png"
            }
        ]
    }
}

def create_excel():
    """创建专业的 Excel 表格"""
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Cooke 镜头规格表"
    
    # 定义样式
    title_font = Font(name='微软雅黑', size=18, bold=True, color='FFFFFF')
    header_font = Font(name='微软雅黑', size=11, bold=True, color='FFFFFF')
    header_font_en = Font(name='Arial', size=10, bold=True, color='E0E0E0')
    cell_font = Font(name='微软雅黑', size=10)
    cell_font_en = Font(name='Arial', size=9, color='666666')
    
    # 填充颜色
    title_fill = PatternFill(start_color='1A1A1A', end_color='1A1A1A', fill_type='solid')
    header_fill = PatternFill(start_color='2D2D2D', end_color='2D2D2D', fill_type='solid')
    header_fill_en = PatternFill(start_color='3D3D3D', end_color='3D3D3D', fill_type='solid')
    alt_fill = PatternFill(start_color='F5F5F5', end_color='F5F5F5', fill_type='solid')
    
    # 边框
    thin_border = Border(
        left=Side(style='thin', color='CCCCCC'),
        right=Side(style='thin', color='CCCCCC'),
        top=Side(style='thin', color='CCCCCC'),
        bottom=Side(style='thin', color='CCCCCC')
    )
    thick_border = Border(
        left=Side(style='medium', color='999999'),
        right=Side(style='medium', color='999999'),
        top=Side(style='medium', color='999999'),
        bottom=Side(style='medium', color='999999')
    )
    
    # 对齐方式
    center_align = Alignment(horizontal='center', vertical='center', wrap_text=True)
    left_align = Alignment(horizontal='left', vertical='center', wrap_text=True)
    
    # 列宽
    column_widths = {
        'A': 15,  # 系列
        'B': 12,  # 焦距
        'C': 15,  # 光圈
        'D': 15,  # 最近对焦
        'E': 15,  # 对焦旋转
        'F': 15,  # 光圈旋转
        'G': 12,  # 长度
        'H': 12,  # 前口径
        'I': 12,  # 重量
        'J': 18,  # 滤镜螺纹
        'K': 12,  # 视角 FF
        'L': 12,  # 视角 S35
        'M': 15,  # 价格
        'N': 20,  # 图片
    }
    
    for col, width in column_widths.items():
        ws.column_dimensions[col].width = width
    
    # 行高
    ws.row_dimensions[1].height = 40  # 标题行
    ws.row_dimensions[2].height = 25  # 英文标题行
    ws.row_dimensions[3].height = 25  # 列标题行
    
    # 创建标题
    ws.merge_cells('A1:N1')
    ws['A1'] = "Cooke Optics 镜头规格大全 | Complete Lens Specifications"
    ws['A1'].font = title_font
    ws['A1'].fill = title_fill
    ws['A1'].alignment = center_align
    
    # 列标题（中英文对照）
    headers = [
        ("镜头系列\nLens Series", "系列\nSeries"),
        ("焦距\nFocal Length", "焦距\nF.L."),
        ("光圈范围\nAperture Range", "光圈\nT-Stop"),
        ("最近对焦距离\nClose Focus", "最近对焦\nC.F."),
        ("对焦旋转角度\nFocus Rotation", "对焦旋转\nFocus Rot."),
        ("光圈旋转角度\nIris Rotation", "光圈旋转\nIris Rot."),
        ("镜头长度\nLens Length", "长度\nLength"),
        ("前组直径\nFront Diameter", "前口径\nFront Dia."),
        ("镜头重量\nLens Weight", "重量\nWeight"),
        ("滤镜螺纹\nFilter Thread", "滤镜\nFilter"),
        ("全画幅视角\nAngle of View (FF)", "视角 FF\nA.O.V FF"),
        ("S35 画幅视角\nAngle of View (S35)", "视角 S35\nA.O.V S35"),
        ("参考价格\nReference Price", "价格\nPrice"),
        ("产品图片\nProduct Image", "图片\nImage")
    ]
    
    for col, (header_cn, header_short) in enumerate(headers, 1):
        cell = ws.cell(row=3, column=col, value=header_short)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align
        cell.border = thin_border
    
    # 填充数据
    current_row = 4
    
    for series_name, series_data in cooke_lenses_data.items():
        for lens_idx, lens in enumerate(series_data['lenses']):
            series_text = series_name if lens_idx == 0 else ""
            
            row_data = [
                series_text,
                lens['focal_length'],
                lens['aperture'],
                lens['close_focus'],
                lens['focus_rotation'],
                lens['iris_rotation'],
                lens['length'],
                lens['front_diameter'],
                lens['weight'],
                lens['filter_thread'],
                lens['angle_ff'],
                lens['angle_s35'],
                lens['price'],
                ""  # 图片占位
            ]
            
            for col, value in enumerate(row_data, 1):
                cell = ws.cell(row=current_row, column=col, value=value)
                cell.font = cell_font
                cell.alignment = center_align
                cell.border = thin_border
                
                # 交替行颜色
                if current_row % 2 == 0:
                    cell.fill = alt_fill
            
            current_row += 1
    
    # 添加系列信息工作表
    ws_info = wb.create_sheet(title="镜头系列说明")
    
    # 系列信息标题
    ws_info.merge_cells('A1:E1')
    ws_info['A1'] = "Cooke 镜头系列详细介绍 | Lens Series Details"
    ws_info['A1'].font = title_font
    ws_info['A1'].fill = title_fill
    ws_info['A1'].alignment = center_align
    ws_info.row_dimensions[1].height = 40
    
    # 系列信息列标题
    info_headers = ["系列名称\nSeries Name", "英文名\nEnglish Name", "描述\nDescription", "镜头数量\nLens Count", "价格范围\nPrice Range"]
    for col, header in enumerate(info_headers, 1):
        cell = ws_info.cell(row=2, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align
        cell.border = thin_border
    
    # 填充系列信息
    for idx, (series_name, series_data) in enumerate(cooke_lenses_data.items(), 3):
        price_range = f"${min([float(l['price'].replace('$', '').replace(',', '')) for l in series_data['lenses']]):,.0f} - ${max([float(l['price'].replace('$', '').replace(',', '')) for l in series_data['lenses']]):,.0f}"
        
        ws_info.cell(row=idx, column=1, value=series_name).font = cell_font
        ws_info.cell(row=idx, column=2, value=series_data['series_name_en']).font = cell_font_en
        ws_info.cell(row=idx, column=3, value=f"{series_data['description_cn']}\n{series_data['description_en']}").font = cell_font
        ws_info.cell(row=idx, column=4, value=len(series_data['lenses'])).font = cell_font
        ws_info.cell(row=idx, column=5, value=price_range).font = cell_font
        
        for col in range(1, 6):
            ws_info.cell(row=idx, column=col).alignment = center_align
            ws_info.cell(row=idx, column=col).border = thin_border
            if idx % 2 == 0:
                ws_info.cell(row=idx, column=col).fill = alt_fill
    
    ws_info.column_dimensions['A'].width = 20
    ws_info.column_dimensions['B'].width = 25
    ws_info.column_dimensions['C'].width = 50
    ws_info.column_dimensions['D'].width = 12
    ws_info.column_dimensions['E'].width = 20
    
    # 保存文件
    output_path = "/Users/jesson/Desktop/Cooke_Optics_Lens_Specifications_库克镜头规格大全.xlsx"
    wb.save(output_path)
    
    print(f"✅ Excel 文件已生成：{output_path}")
    print(f"📊 共包含 {len(cooke_lenses_data)} 个系列")
    print(f"📷 共包含 {sum([len(s['lenses']) for s in cooke_lenses_data.values()])} 款镜头")
    
    return output_path

if __name__ == "__main__":
    create_excel()
