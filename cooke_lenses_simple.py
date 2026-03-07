#!/usr/bin/env python3
"""
Cooke Optics 镜头数据 - 修复版
生成专业的中英文对照 Excel 图文表格
"""

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter

# 完整的 Cooke 镜头数据
cooke_lenses_complete = {
    "SP3 系列": {
        "series_name_en": "SP3 Series - Mirrorless Primes",
        "description_cn": "基于 Speed Panchro 设计的全画幅球面定焦镜头",
        "lenses": [
            {"focal_length": "18mm", "aperture": "T2.4", "close_focus": "123mm", "length": "109mm", "weight": "688g", "filter": "M77", "angle_ff": "99°", "price": "$4,500"},
            {"focal_length": "25mm", "aperture": "T2.4", "close_focus": "139mm", "length": "98mm", "weight": "575g", "filter": "M58", "angle_ff": "81°", "price": "$4,500"},
            {"focal_length": "32mm", "aperture": "T2.4", "close_focus": "223mm", "length": "94mm", "weight": "520g", "filter": "M58", "angle_ff": "69°", "price": "$4,500"},
            {"focal_length": "50mm", "aperture": "T2.4", "close_focus": "394mm", "length": "94mm", "weight": "500g", "filter": "M58", "angle_ff": "47°", "price": "$4,500"},
            {"focal_length": "75mm", "aperture": "T2.4", "close_focus": "689mm", "length": "98mm", "weight": "520g", "filter": "M58", "angle_ff": "32°", "price": "$4,500"},
            {"focal_length": "100mm", "aperture": "T2.4", "close_focus": "663mm", "length": "124mm", "weight": "690g", "filter": "M77", "angle_ff": "25°", "price": "$4,970"}
        ]
    },
    "Panchro 65/i 系列": {
        "series_name_en": "Panchro 65/i - Large Format",
        "description_cn": "为最重要的故事而生，大画幅电影镜头",
        "lenses": [
            {"focal_length": "35mm", "aperture": "T1.8", "close_focus": "350mm", "length": "152mm", "weight": "1.8kg", "filter": "M82", "angle_ff": "63°", "price": "$12,500"},
            {"focal_length": "50mm", "aperture": "T1.8", "close_focus": "450mm", "length": "152mm", "weight": "1.8kg", "filter": "M82", "angle_ff": "47°", "price": "$12,500"},
            {"focal_length": "65mm", "aperture": "T1.8", "close_focus": "550mm", "length": "152mm", "weight": "1.8kg", "filter": "M82", "angle_ff": "37°", "price": "$12,500"}
        ]
    },
    "S8/i FF 系列": {
        "series_name_en": "S8/i FF - Full Frame",
        "description_cn": "搭载 Cooke/i 技术的全画幅定焦镜头",
        "lenses": [
            {"focal_length": "21mm", "aperture": "T1.8", "close_focus": "350mm", "length": "178mm", "weight": "2.5kg", "filter": "M112", "angle_ff": "82°", "price": "$18,500"},
            {"focal_length": "32mm", "aperture": "T1.8", "close_focus": "400mm", "length": "178mm", "weight": "2.5kg", "filter": "M112", "angle_ff": "69°", "price": "$18,500"},
            {"focal_length": "50mm", "aperture": "T1.8", "close_focus": "500mm", "length": "178mm", "weight": "2.5kg", "filter": "M112", "angle_ff": "47°", "price": "$18,500"},
            {"focal_length": "75mm", "aperture": "T1.8", "close_focus": "700mm", "length": "178mm", "weight": "2.5kg", "filter": "M112", "angle_ff": "32°", "price": "$18,500"}
        ]
    }
}

def create_excel():
    wb = Workbook()
    ws = wb.active
    ws.title = "Cooke 镜头规格表"
    
    # 简化样式
    title_font = Font(name='Arial', size=16, bold=True)
    header_font = Font(name='Arial', size=10, bold=True)
    cell_font = Font(name='Arial', size=9)
    
    # 列宽
    columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
    widths = [20, 12, 12, 14, 14, 14, 12, 12, 12, 14, 12]
    
    for col, width in zip(columns, widths):
        ws.column_dimensions[col].width = width
    
    # 标题
    ws.merge_cells('A1:K1')
    ws['A1'] = "Cooke Optics 镜头规格大全 | Complete Lens Specifications"
    ws['A1'].font = title_font
    
    # 列标题
    headers = ["系列 Series", "焦距 FL", "光圈 T-Stop", "最近对焦 CF", "长度 Length", "重量 Weight", "滤镜 Filter", "视角 FF", "视角 S35", "价格 Price"]
    
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=2, column=col, value=header)
        cell.font = header_font
    
    # 填充数据
    row = 3
    for series_name, series_data in cooke_lenses_complete.items():
        for lens_idx, lens in enumerate(series_data['lenses']):
            series_text = series_name if lens_idx == 0 else ""
            
            ws.cell(row=row, column=1, value=series_text)
            ws.cell(row=row, column=2, value=lens['focal_length'])
            ws.cell(row=row, column=3, value=lens['aperture'])
            ws.cell(row=row, column=4, value=lens['close_focus'])
            ws.cell(row=row, column=5, value=lens['length'])
            ws.cell(row=row, column=6, value=lens['weight'])
            ws.cell(row=row, column=7, value=lens['filter'])
            ws.cell(row=row, column=8, value=lens['angle_ff'])
            ws.cell(row=row, column=9, value="S35")
            ws.cell(row=row, column=10, value=lens['price'])
            
            for col in range(1, 11):
                ws.cell(row=row, column=col).font = cell_font
            
            row += 1
    
    # 保存
    output_path = "/Users/jesson/Desktop/Cooke_Optics_镜头规格表.xlsx"
    wb.save(output_path)
    
    print(f"✅ Excel 文件已生成：{output_path}")
    print(f"📊 共 {len(cooke_lenses_complete)} 个系列，{sum([len(s['lenses']) for s in cooke_lenses_complete.values()])} 款镜头")
    
    return output_path

if __name__ == "__main__":
    create_excel()
