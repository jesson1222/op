#!/usr/bin/env python3
"""Cooke Optics 镜头数据 - 最终修复版"""

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side

cooke_lenses = {
    "SP3 系列": {
        "en": "SP3 Series - Mirrorless Primes",
        "desc": "基于 Speed Panchro 设计的全画幅球面定焦镜头",
        "lenses": [
            {"fl": "18mm", "t": "T2.4", "cf": "123mm", "len": "109mm", "wt": "688g", "filter": "M77", "aov": "99°", "price": "$4,500"},
            {"fl": "25mm", "t": "T2.4", "cf": "139mm", "len": "98mm", "wt": "575g", "filter": "M58", "aov": "81°", "price": "$4,500"},
            {"fl": "32mm", "t": "T2.4", "cf": "223mm", "len": "94mm", "wt": "520g", "filter": "M58", "aov": "69°", "price": "$4,500"},
            {"fl": "50mm", "t": "T2.4", "cf": "394mm", "len": "94mm", "wt": "500g", "filter": "M58", "aov": "47°", "price": "$4,500"},
            {"fl": "75mm", "t": "T2.4", "cf": "689mm", "len": "98mm", "wt": "520g", "filter": "M58", "aov": "32°", "price": "$4,500"},
            {"fl": "100mm", "t": "T2.4", "cf": "663mm", "len": "124mm", "wt": "690g", "filter": "M77", "aov": "25°", "price": "$4,970"}
        ]
    },
    "Panchro 65/i": {
        "en": "Panchro 65/i - Large Format",
        "desc": "大画幅电影镜头，T1.8 超大光圈",
        "lenses": [
            {"fl": "35mm", "t": "T1.8", "cf": "350mm", "len": "152mm", "wt": "1.8kg", "filter": "M82", "aov": "63°", "price": "$12,500"},
            {"fl": "50mm", "t": "T1.8", "cf": "450mm", "len": "152mm", "wt": "1.8kg", "filter": "M82", "aov": "47°", "price": "$12,500"},
            {"fl": "65mm", "t": "T1.8", "cf": "550mm", "len": "152mm", "wt": "1.8kg", "filter": "M82", "aov": "37°", "price": "$12,500"}
        ]
    },
    "S8/i FF": {
        "en": "S8/i FF - Full Frame",
        "desc": "全画幅定焦镜头，Cooke/i 技术",
        "lenses": [
            {"fl": "21mm", "t": "T1.8", "cf": "350mm", "len": "178mm", "wt": "2.5kg", "filter": "M112", "aov": "82°", "price": "$18,500"},
            {"fl": "32mm", "t": "T1.8", "cf": "400mm", "len": "178mm", "wt": "2.5kg", "filter": "M112", "aov": "69°", "price": "$18,500"},
            {"fl": "50mm", "t": "T1.8", "cf": "500mm", "len": "178mm", "wt": "2.5kg", "filter": "M112", "aov": "47°", "price": "$18,500"},
            {"fl": "75mm", "t": "T1.8", "cf": "700mm", "len": "178mm", "wt": "2.5kg", "filter": "M112", "aov": "32°", "price": "$18,500"}
        ]
    },
    "Panchro/i Classic": {
        "en": "Panchro/i Classic FF",
        "desc": "经典 Speed Panchro 现代复刻",
        "lenses": [
            {"fl": "35mm", "t": "T2.2", "cf": "380mm", "len": "142mm", "wt": "1.6kg", "filter": "M82", "aov": "63°", "price": "$11,500"},
            {"fl": "50mm", "t": "T2.2", "cf": "480mm", "len": "142mm", "wt": "1.6kg", "filter": "M82", "aov": "47°", "price": "$11,500"},
            {"fl": "75mm", "t": "T2.2", "cf": "680mm", "len": "142mm", "wt": "1.6kg", "filter": "M82", "aov": "32°", "price": "$11,500"}
        ]
    },
    "Anamorphic/i FF": {
        "en": "Anamorphic/i FF - 2x Squeeze",
        "desc": "全画幅变形宽银幕镜头，2x 压缩",
        "lenses": [
            {"fl": "32mm", "t": "T2.3", "cf": "450mm", "len": "193mm", "wt": "2.8kg", "filter": "M112", "aov": "76°×2", "price": "$22,000"},
            {"fl": "40mm", "t": "T2.3", "cf": "500mm", "len": "193mm", "wt": "2.8kg", "filter": "M112", "aov": "65°×2", "price": "$22,000"},
            {"fl": "50mm", "t": "T2.3", "cf": "550mm", "len": "193mm", "wt": "2.8kg", "filter": "M112", "aov": "54°×2", "price": "$22,000"},
            {"fl": "75mm", "t": "T2.3", "cf": "700mm", "len": "193mm", "wt": "2.8kg", "filter": "M112", "aov": "38°×2", "price": "$22,000"},
            {"fl": "100mm", "t": "T2.3", "cf": "900mm", "len": "193mm", "wt": "2.8kg", "filter": "M112", "aov": "29°×2", "price": "$22,000"}
        ]
    }
}

wb = Workbook()
ws = wb.active
ws.title = "Cooke 镜头规格表"

# 样式
title_font = Font(name='Arial', size=16, bold=True)
header_font = Font(name='Arial', size=10, bold=True)
cell_font = Font(name='Arial', size=9)
series_font = Font(name='Arial', size=10, bold=True)
price_font = Font(name='Arial', size=9, bold=True, color='006600')

# 列宽
for col, width in [('A', 20), ('B', 12), ('C', 12), ('D', 14), ('E', 12), ('F', 12), ('G', 12), ('H', 14), ('I', 12)]:
    ws.column_dimensions[col].width = width

# 标题
ws.merge_cells('A1:I1')
ws['A1'] = "Cooke Optics 镜头规格大全 | Complete Lens Specifications"
ws['A1'].font = title_font

# 列标题
headers = ["系列 Series", "焦距 FL", "光圈 T", "最近对焦 CF", "长度 Len", "重量 Wt", "滤镜 Filter", "视角 AOV", "价格 Price"]
for col, h in enumerate(headers, 1):
    ws.cell(row=2, column=col, value=h).font = header_font

# 数据
row = 3
for name, data in cooke_lenses.items():
    # 系列标题
    ws.merge_cells(f'A{row}:I{row}')
    ws.cell(row=row, column=1, value=f"◆ {name} | {data['en']}").font = series_font
    row += 1
    
    # 镜头数据
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
        price_cell = ws.cell(row=row, column=9, value=lens['price'])
        price_cell.font = price_font
        row += 1

# 工作表 2: 系列介绍
ws2 = wb.create_sheet("系列介绍")
ws2.merge_cells('A1:E1')
ws2['A1'] = "Cooke 镜头系列介绍"
ws2['A1'].font = title_font

ws2_headers = ["系列", "英文名", "描述", "镜头数量", "价格范围"]
for col, h in enumerate(ws2_headers, 1):
    ws2.cell(row=2, column=col, value=h).font = header_font

row = 3
for name, data in cooke_lenses.items():
    prices = [float(l['price'].replace('$','').replace(',','')) for l in data['lenses']]
    ws2.cell(row=row, column=1, value=name).font = cell_font
    ws2.cell(row=row, column=2, value=data['en']).font = cell_font
    ws2.cell(row=row, column=3, value=data['desc']).font = cell_font
    ws2.cell(row=row, column=4, value=len(data['lenses'])).font = cell_font
    ws2.cell(row=row, column=5, value=f"${min(prices):,.0f} - ${max(prices):,.0f}").font = price_font
    row += 1

# 保存
path = "/Users/jesson/Desktop/Cooke_Optics_镜头规格大全_完整版.xlsx"
wb.save(path)

print(f"\n✅ Excel 已生成：{path}")
print(f"📊 {len(cooke_lenses)} 个系列，{sum([len(s['lenses']) for s in cooke_lenses.values()])} 款镜头")
print(f"💰 价格范围：$4,500 - $22,000")
print(f"\n📑 包含 2 个工作表:")
print(f"   1. 镜头规格表 - 完整参数")
print(f"   2. 系列介绍 - 特点说明")
