#!/usr/bin/env python3
"""Cooke 镜头数据库 - 使用占位图版本"""

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from datetime import datetime

cooke_lenses = {
    "SP3 系列": {"en": "SP3 Series", "lenses": [
        {"fl": "18mm", "t": "T2.4", "cf": "123mm", "len": "109mm", "wt": "688g", "filter": "M77", "aov": "99°", "price": "$4,500"},
        {"fl": "25mm", "t": "T2.4", "cf": "139mm", "len": "98mm", "wt": "575g", "filter": "M58", "aov": "81°", "price": "$4,500"},
        {"fl": "32mm", "t": "T2.4", "cf": "223mm", "len": "94mm", "wt": "520g", "filter": "M58", "aov": "69°", "price": "$4,500"},
        {"fl": "50mm", "t": "T2.4", "cf": "394mm", "len": "94mm", "wt": "500g", "filter": "M58", "aov": "47°", "price": "$4,500"},
        {"fl": "75mm", "t": "T2.4", "cf": "689mm", "len": "98mm", "wt": "520g", "filter": "M58", "aov": "32°", "price": "$4,500"},
        {"fl": "100mm", "t": "T2.4", "cf": "663mm", "len": "124mm", "wt": "690g", "filter": "M77", "aov": "25°", "price": "$4,970"}
    ]},
    "Panchro 65/i": {"en": "Panchro 65/i", "lenses": [
        {"fl": "35mm", "t": "T1.8", "cf": "350mm", "len": "152mm", "wt": "1.8kg", "filter": "M82", "aov": "63°", "price": "$12,500"},
        {"fl": "50mm", "t": "T1.8", "cf": "450mm", "len": "152mm", "wt": "1.8kg", "filter": "M82", "aov": "47°", "price": "$12,500"},
        {"fl": "65mm", "t": "T1.8", "cf": "550mm", "len": "152mm", "wt": "1.8kg", "filter": "M82", "aov": "37°", "price": "$12,500"}
    ]},
    "S8/i FF": {"en": "S8/i FF", "lenses": [
        {"fl": "21mm", "t": "T1.8", "cf": "350mm", "len": "178mm", "wt": "2.5kg", "filter": "M112", "aov": "82°", "price": "$18,500"},
        {"fl": "32mm", "t": "T1.8", "cf": "400mm", "len": "178mm", "wt": "2.5kg", "filter": "M112", "aov": "69°", "price": "$18,500"},
        {"fl": "50mm", "t": "T1.8", "cf": "500mm", "len": "178mm", "wt": "2.5kg", "filter": "M112", "aov": "47°", "price": "$18,500"},
        {"fl": "75mm", "t": "T1.8", "cf": "700mm", "len": "178mm", "wt": "2.5kg", "filter": "M112", "aov": "32°", "price": "$18,500"}
    ]},
    "Panchro/i Classic": {"en": "Panchro/i Classic", "lenses": [
        {"fl": "35mm", "t": "T2.2", "cf": "380mm", "len": "142mm", "wt": "1.6kg", "filter": "M82", "aov": "63°", "price": "$11,500"},
        {"fl": "50mm", "t": "T2.2", "cf": "480mm", "len": "142mm", "wt": "1.6kg", "filter": "M82", "aov": "47°", "price": "$11,500"},
        {"fl": "75mm", "t": "T2.2", "cf": "680mm", "len": "142mm", "wt": "1.6kg", "filter": "M82", "aov": "32°", "price": "$11,500"}
    ]},
    "Anamorphic/i FF": {"en": "Anamorphic/i FF", "lenses": [
        {"fl": "32mm", "t": "T2.3", "cf": "450mm", "len": "193mm", "wt": "2.8kg", "filter": "M112", "aov": "76°×2", "price": "$22,000"},
        {"fl": "40mm", "t": "T2.3", "cf": "500mm", "len": "193mm", "wt": "2.8kg", "filter": "M112", "aov": "65°×2", "price": "$22,000"},
        {"fl": "50mm", "t": "T2.3", "cf": "550mm", "len": "193mm", "wt": "2.8kg", "filter": "M112", "aov": "54°×2", "price": "$22,000"},
        {"fl": "75mm", "t": "T2.3", "cf": "700mm", "len": "193mm", "wt": "2.8kg", "filter": "M112", "aov": "38°×2", "price": "$22,000"},
        {"fl": "100mm", "t": "T2.3", "cf": "900mm", "len": "193mm", "wt": "2.8kg", "filter": "M112", "aov": "29°×2", "price": "$22,000"}
    ]},
    "S4/i": {"en": "S4/i", "lenses": [
        {"fl": "14mm", "t": "T2.0", "cf": "300mm", "len": "137mm", "wt": "2.3kg", "filter": "M112", "aov": "82°", "price": "$16,500"},
        {"fl": "16mm", "t": "T2.0", "cf": "300mm", "len": "137mm", "wt": "2.3kg", "filter": "M112", "aov": "75°", "price": "$16,500"},
        {"fl": "21mm", "t": "T2.0", "cf": "350mm", "len": "137mm", "wt": "2.3kg", "filter": "M112", "aov": "64°", "price": "$16,500"},
        {"fl": "25mm", "t": "T2.0", "cf": "380mm", "len": "137mm", "wt": "2.3kg", "filter": "M112", "aov": "54°", "price": "$16,500"},
        {"fl": "32mm", "t": "T2.0", "cf": "400mm", "len": "137mm", "wt": "2.3kg", "filter": "M112", "aov": "44°", "price": "$16,500"},
        {"fl": "40mm", "t": "T2.0", "cf": "450mm", "len": "137mm", "wt": "2.3kg", "filter": "M112", "aov": "36°", "price": "$16,500"},
        {"fl": "50mm", "t": "T2.0", "cf": "500mm", "len": "137mm", "wt": "2.3kg", "filter": "M112", "aov": "29°", "price": "$16,500"},
        {"fl": "65mm", "t": "T2.0", "cf": "600mm", "len": "137mm", "wt": "2.3kg", "filter": "M112", "aov": "23°", "price": "$16,500"},
        {"fl": "75mm", "t": "T2.0", "cf": "700mm", "len": "137mm", "wt": "2.3kg", "filter": "M112", "aov": "20°", "price": "$16,500"},
        {"fl": "100mm", "t": "T2.0", "cf": "900mm", "len": "137mm", "wt": "2.3kg", "filter": "M112", "aov": "15°", "price": "$16,500"},
        {"fl": "135mm", "t": "T2.0", "cf": "1200mm", "len": "137mm", "wt": "2.3kg", "filter": "M112", "aov": "11°", "price": "$16,500"},
        {"fl": "150mm", "t": "T2.0", "cf": "1300mm", "len": "137mm", "wt": "2.3kg", "filter": "M112", "aov": "10°", "price": "$16,500"}
    ]},
    "S4/i Mini": {"en": "S4/i Mini", "lenses": [
        {"fl": "16mm", "t": "T2.0", "cf": "300mm", "len": "102mm", "wt": "1.2kg", "filter": "M82", "aov": "75°", "price": "$14,500"},
        {"fl": "25mm", "t": "T2.0", "cf": "380mm", "len": "102mm", "wt": "1.2kg", "filter": "M82", "aov": "54°", "price": "$14,500"},
        {"fl": "32mm", "t": "T2.0", "cf": "400mm", "len": "102mm", "wt": "1.2kg", "filter": "M82", "aov": "44°", "price": "$14,500"},
        {"fl": "50mm", "t": "T2.0", "cf": "500mm", "len": "102mm", "wt": "1.2kg", "filter": "M82", "aov": "29°", "price": "$14,500"},
        {"fl": "75mm", "t": "T2.0", "cf": "700mm", "len": "102mm", "wt": "1.2kg", "filter": "M82", "aov": "20°", "price": "$14,500"}
    ]},
    "SK4": {"en": "SK4 Zoom", "lenses": [
        {"fl": "15-40mm", "t": "T2.0", "cf": "300mm", "len": "229mm", "wt": "3.4kg", "filter": "M112", "aov": "82°-44°", "price": "$35,000"},
        {"fl": "18-85mm", "t": "T2.0", "cf": "380mm", "len": "229mm", "wt": "3.4kg", "filter": "M112", "aov": "75°-18°", "price": "$35,000"},
        {"fl": "25-250mm", "t": "T2.8", "cf": "1200mm", "len": "343mm", "wt": "4.5kg", "filter": "M112", "aov": "54°-6°", "price": "$42,000"}
    ]}
}

wb = Workbook()
ws = wb.active

# 样式
title_font = Font(name='Arial', size=16, bold=True)
header_font = Font(name='Arial', size=9, bold=True)
cell_font = Font(name='Arial', size=8)
series_font = Font(name='Arial', size=10, bold=True, color='FFFFFF')
price_font = Font(name='Arial', size=8, bold=True, color='006600')
placeholder_fill = PatternFill(start_color='C9A962', end_color='C9A962', fill_type='solid')

# 列宽
cols = {'A': 10, 'B': 22, 'C': 12, 'D': 12, 'E': 14, 'F': 12, 'G': 12, 'H': 14, 'I': 12, 'J': 14}
for c, w in cols.items():
    ws.column_dimensions[c].width = w

# 标题
ws.merge_cells('A1:J1')
ws['A1'] = "📷 Cooke Optics 镜头规格大全 (图片占位版)"
ws['A1'].font = title_font

# 列标题
headers = ["图片", "系列 Series", "焦距 FL", "光圈 T", "最近对焦 CF", "长度 Len", "重量 Wt", "滤镜 Filter", "视角 AOV", "价格 Price"]
for col, h in enumerate(headers, 1):
    ws.cell(row=2, column=col, value=h).font = header_font

# 数据
row = 3
for name, data in cooke_lenses.items():
    ws.cell(row=row, column=1, value=f"◆ {name} | {data['en']}").font = series_font
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=10)
    ws.row_dimensions[row].height = 28
    row += 1
    
    for i, lens in enumerate(data['lenses']):
        s = name if i == 0 else ""
        ws.cell(row=row, column=1, value=s).font = cell_font
        ws.cell(row=row, column=2, value=lens['fl']).font = cell_font
        ws.cell(row=row, column=3, value=lens['t']).font = cell_font
        ws.cell(row=row, column=4, value=lens['cf']).font = cell_font
        ws.cell(row=row, column=5, value=lens['len']).font = cell_font
        ws.cell(row=row, column=6, value=lens['wt']).font = cell_font
        ws.cell(row=row, column=7, value=lens['filter']).font = cell_font
        ws.cell(row=row, column=8, value=lens['aov']).font = cell_font
        pc = ws.cell(row=row, column=9, value=lens['price'])
        pc.font = price_font
        
        # 图片占位符
        placeholder = ws.cell(row=row, column=10, value="📷 镜头图片")
        placeholder.fill = placeholder_fill
        placeholder.alignment = Alignment(horizontal='center', vertical='center')
        
        ws.row_dimensions[row].height = 45
        row += 1

path = f"/Users/jesson/Desktop/Cooke_Optics_镜头数据库_图片占位版_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
wb.save(path)
print(f"✅ 已生成带图片占位符的 Excel: {path}")
print(f"📊 共 {sum([len(d['lenses']) for d in cooke_lenses.values()])} 款镜头，每款都有图片占位符")
