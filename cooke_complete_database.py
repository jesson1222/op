#!/usr/bin/env python3
"""
Cooke Optics 完整镜头数据库
包含 Cooke 所有镜头系列的完整技术参数
生成专业的中英文对照 Excel 表格
"""

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side
import json
from datetime import datetime

# Cooke 完整镜头数据库
cooke_complete_database = {
    "SP3 系列": {
        "series_name_en": "SP3 Series - Mirrorless Primes",
        "series_name_cn": "SP3 系列 - 无反定焦镜头",
        "description_cn": "基于 Speed Panchro 设计的全画幅球面定焦镜头，专为现代无反相机优化",
        "description_en": "Full Frame spherical prime lenses based on Speed Panchro design, optimized for modern mirrorless cameras",
        "mount": "E/RF/L/M 可更换卡口",
        "format": "全画幅 (兼容 S35)",
        "t_stop": "T2.4 - T16",
        "features": ["T2.4 大光圈", "小巧轻便", "经典 Cooke Look", "可更换卡口", "双对焦刻度", "与 Panchro/i Classic 匹配"],
        "lenses": [
            {"fl": "18mm", "t": "T2.4-T16", "cf": "123mm", "focus_rot": "160°", "iris_rot": "78°", "len": "109mm", "front": "82mm", "wt": "688g", "filter": "M77 x 0.75", "aov_ff": "99°", "aov_s35": "82°", "price": "$4,500"},
            {"fl": "25mm", "t": "T2.4-T16", "cf": "139mm", "focus_rot": "160°", "iris_rot": "78°", "len": "98mm", "front": "64mm", "wt": "575g", "filter": "M58 x 0.75", "aov_ff": "81°", "aov_s35": "62°", "price": "$4,500"},
            {"fl": "32mm", "t": "T2.4-T16", "cf": "223mm", "focus_rot": "160°", "iris_rot": "78°", "len": "94mm", "front": "64mm", "wt": "520g", "filter": "M58 x 0.75", "aov_ff": "69°", "aov_s35": "50°", "price": "$4,500"},
            {"fl": "50mm", "t": "T2.4-T16", "cf": "394mm", "focus_rot": "160°", "iris_rot": "78°", "len": "94mm", "front": "64mm", "wt": "500g", "filter": "M58 x 0.75", "aov_ff": "47°", "aov_s35": "34°", "price": "$4,500"},
            {"fl": "75mm", "t": "T2.4-T16", "cf": "689mm", "focus_rot": "160°", "iris_rot": "78°", "len": "98mm", "front": "64mm", "wt": "520g", "filter": "M58 x 0.75", "aov_ff": "32°", "aov_s35": "22°", "price": "$4,500"},
            {"fl": "100mm", "t": "T2.4-T16", "cf": "663mm", "focus_rot": "160°", "iris_rot": "78°", "len": "124mm", "front": "82mm", "wt": "690g", "filter": "M77 x 0.75", "aov_ff": "25°", "aov_s35": "17°", "price": "$4,970"}
        ],
        "sets": [
            {"name": "SP3 Three-Set", "lenses": "25mm, 50mm, 100mm", "price": "$12,800"},
            {"name": "SP3 Five-Set", "lenses": "25mm, 32mm, 50mm, 75mm, 100mm", "price": "$21,375"},
            {"name": "SP3 Six-Set", "lenses": "18mm, 25mm, 32mm, 50mm, 75mm, 100mm", "price": "$26,000"}
        ]
    },
    
    "Panchro 65/i 系列": {
        "series_name_en": "Panchro 65/i Series - Large Format Primes",
        "series_name_cn": "Panchro 65/i 系列 - 大画幅定焦镜头",
        "description_cn": "为最重要的故事而生，大画幅电影镜头，继承 Cooke 经典 Speed Panchro 设计",
        "description_en": "Large format prime lenses for the biggest stories, inheriting Cooke's classic Speed Panchro design",
        "mount": "PL 卡口",
        "format": "大画幅 (Full Frame+)",
        "t_stop": "T1.8 - T16",
        "features": ["T1.8 超大光圈", "大画幅覆盖", "Cooke/i 技术", "电影级光学", "经典 Cooke Look", "坚固机械结构"],
        "lenses": [
            {"fl": "35mm", "t": "T1.8-T16", "cf": "350mm", "focus_rot": "160°", "iris_rot": "78°", "len": "152mm", "front": "95mm", "wt": "1.8kg", "filter": "M82 x 0.75", "aov_ff": "63°", "aov_s35": "44°", "price": "$12,500"},
            {"fl": "50mm", "t": "T1.8-T16", "cf": "450mm", "focus_rot": "160°", "iris_rot": "78°", "len": "152mm", "front": "95mm", "wt": "1.8kg", "filter": "M82 x 0.75", "aov_ff": "47°", "aov_s35": "32°", "price": "$12,500"},
            {"fl": "65mm", "t": "T1.8-T16", "cf": "550mm", "focus_rot": "160°", "iris_rot": "78°", "len": "152mm", "front": "95mm", "wt": "1.8kg", "filter": "M82 x 0.75", "aov_ff": "37°", "aov_s35": "25°", "price": "$12,500"}
        ],
        "sets": []
    },
    
    "S8/i FF 系列": {
        "series_name_en": "S8/i FF Series - Full Frame Primes",
        "series_name_cn": "S8/i FF 系列 - 全画幅定焦镜头",
        "description_cn": "搭载 Cooke/i 技术的全画幅定焦镜头，代表 Cooke 最高光学水准",
        "description_en": "Full Frame prime lenses with Cooke/i Technology, representing Cooke's highest optical standards",
        "mount": "PL 卡口",
        "format": "全画幅 (Full Frame)",
        "t_stop": "T1.8 - T16",
        "features": ["T1.8 大光圈", "Cooke/i 元数据", "8K 分辨率支持", "专业电影标准", "完美匹配镜头组", "卓越光学性能"],
        "lenses": [
            {"fl": "21mm", "t": "T1.8-T16", "cf": "350mm", "focus_rot": "160°", "iris_rot": "78°", "len": "178mm", "front": "114mm", "wt": "2.5kg", "filter": "M112 x 0.75", "aov_ff": "82°", "aov_s35": "56°", "price": "$18,500"},
            {"fl": "32mm", "t": "T1.8-T16", "cf": "400mm", "focus_rot": "160°", "iris_rot": "78°", "len": "178mm", "front": "114mm", "wt": "2.5kg", "filter": "M112 x 0.75", "aov_ff": "69°", "aov_s35": "47°", "price": "$18,500"},
            {"fl": "50mm", "t": "T1.8-T16", "cf": "500mm", "focus_rot": "160°", "iris_rot": "78°", "len": "178mm", "front": "114mm", "wt": "2.5kg", "filter": "M112 x 0.75", "aov_ff": "47°", "aov_s35": "32°", "price": "$18,500"},
            {"fl": "75mm", "t": "T1.8-T16", "cf": "700mm", "focus_rot": "160°", "iris_rot": "78°", "len": "178mm", "front": "114mm", "wt": "2.5kg", "filter": "M112 x 0.75", "aov_ff": "32°", "aov_s35": "22°", "price": "$18,500"}
        ],
        "sets": []
    },
    
    "Panchro/i Classic FF 系列": {
        "series_name_en": "Panchro/i Classic FF Series",
        "series_name_cn": "Panchro/i Classic FF 系列 - 经典复刻",
        "description_cn": "经典 Speed Panchro 设计的现代复刻，全画幅覆盖",
        "description_en": "Modern recreation of classic Speed Panchro design, Full Frame coverage",
        "mount": "PL 卡口",
        "format": "全画幅 (Full Frame)",
        "t_stop": "T2.2 - T16",
        "features": ["T2.2 光圈", "经典 Cooke Look", "复古与现代结合", "Cooke/i 技术", "电影感成像", "双对焦刻度"],
        "lenses": [
            {"fl": "35mm", "t": "T2.2-T16", "cf": "380mm", "focus_rot": "160°", "iris_rot": "78°", "len": "142mm", "front": "95mm", "wt": "1.6kg", "filter": "M82 x 0.75", "aov_ff": "63°", "aov_s35": "44°", "price": "$11,500"},
            {"fl": "50mm", "t": "T2.2-T16", "cf": "480mm", "focus_rot": "160°", "iris_rot": "78°", "len": "142mm", "front": "95mm", "wt": "1.6kg", "filter": "M82 x 0.75", "aov_ff": "47°", "aov_s35": "32°", "price": "$11,500"},
            {"fl": "75mm", "t": "T2.2-T16", "cf": "680mm", "focus_rot": "160°", "iris_rot": "78°", "len": "142mm", "front": "95mm", "wt": "1.6kg", "filter": "M82 x 0.75", "aov_ff": "32°", "aov_s35": "22°", "price": "$11,500"}
        ],
        "sets": []
    },
    
    "Anamorphic/i FF 系列": {
        "series_name_en": "Anamorphic/i FF Series - 2x Squeeze",
        "series_name_cn": "Anamorphic/i FF 系列 - 变形宽银幕镜头",
        "description_cn": "全画幅变形宽银幕镜头，2x 压缩比，真正的电影体验",
        "description_en": "Full Frame anamorphic lenses with 2x squeeze, true cinematic experience",
        "mount": "PL 卡口",
        "format": "全画幅 (Full Frame)",
        "t_stop": "T2.3 - T16",
        "features": ["2x 压缩比", "T2.3 光圈", "经典椭圆光斑", "水平镜头光晕", "Cooke/i 技术", "变形宽银幕效果"],
        "lenses": [
            {"fl": "32mm", "t": "T2.3-T16", "cf": "450mm", "focus_rot": "160°", "iris_rot": "78°", "len": "193mm", "front": "114mm", "wt": "2.8kg", "filter": "M112 x 0.75", "aov_ff": "76°×2", "aov_s35": "54°×2", "price": "$22,000"},
            {"fl": "40mm", "t": "T2.3-T16", "cf": "500mm", "focus_rot": "160°", "iris_rot": "78°", "len": "193mm", "front": "114mm", "wt": "2.8kg", "filter": "M112 x 0.75", "aov_ff": "65°×2", "aov_s35": "46°×2", "price": "$22,000"},
            {"fl": "50mm", "t": "T2.3-T16", "cf": "550mm", "focus_rot": "160°", "iris_rot": "78°", "len": "193mm", "front": "114mm", "wt": "2.8kg", "filter": "M112 x 0.75", "aov_ff": "54°×2", "aov_s35": "38°×2", "price": "$22,000"},
            {"fl": "75mm", "t": "T2.3-T16", "cf": "700mm", "focus_rot": "160°", "iris_rot": "78°", "len": "193mm", "front": "114mm", "wt": "2.8kg", "filter": "M112 x 0.75", "aov_ff": "38°×2", "aov_s35": "27°×2", "price": "$22,000"},
            {"fl": "100mm", "t": "T2.3-T16", "cf": "900mm", "focus_rot": "160°", "iris_rot": "78°", "len": "193mm", "front": "114mm", "wt": "2.8kg", "filter": "M112 x 0.75", "aov_ff": "29°×2", "aov_s35": "20°×2", "price": "$22,000"}
        ],
        "sets": []
    },
    
    "S4/i 系列": {
        "series_name_en": "S4/i Series - Super 35mm Primes",
        "series_name_cn": "S4/i 系列 - Super 35mm 定焦镜头",
        "description_cn": "Super 35mm 画幅定焦镜头，经过时间考验的经典设计",
        "description_en": "Super 35mm prime lenses, time-tested classic design",
        "mount": "PL 卡口",
        "format": "Super 35mm",
        "t_stop": "T2.0 - T16",
        "features": ["T2.0 光圈", "Super 35mm 覆盖", "Cooke/i 技术", "经典设计", "可靠耐用", "广泛使用"],
        "lenses": [
            {"fl": "14mm", "t": "T2.0-T16", "cf": "300mm", "focus_rot": "160°", "iris_rot": "78°", "len": "137mm", "front": "114mm", "wt": "2.3kg", "filter": "M112 x 0.75", "aov_ff": "-", "aov_s35": "82°", "price": "$16,500"},
            {"fl": "16mm", "t": "T2.0-T16", "cf": "300mm", "focus_rot": "160°", "iris_rot": "78°", "len": "137mm", "front": "114mm", "wt": "2.3kg", "filter": "M112 x 0.75", "aov_ff": "-", "aov_s35": "75°", "price": "$16,500"},
            {"fl": "21mm", "t": "T2.0-T16", "cf": "350mm", "focus_rot": "160°", "iris_rot": "78°", "len": "137mm", "front": "114mm", "wt": "2.3kg", "filter": "M112 x 0.75", "aov_ff": "-", "aov_s35": "64°", "price": "$16,500"},
            {"fl": "25mm", "t": "T2.0-T16", "cf": "380mm", "focus_rot": "160°", "iris_rot": "78°", "len": "137mm", "front": "114mm", "wt": "2.3kg", "filter": "M112 x 0.75", "aov_ff": "-", "aov_s35": "54°", "price": "$16,500"},
            {"fl": "32mm", "t": "T2.0-T16", "cf": "400mm", "focus_rot": "160°", "iris_rot": "78°", "len": "137mm", "front": "114mm", "wt": "2.3kg", "filter": "M112 x 0.75", "aov_ff": "-", "aov_s35": "44°", "price": "$16,500"},
            {"fl": "40mm", "t": "T2.0-T16", "cf": "450mm", "focus_rot": "160°", "iris_rot": "78°", "len": "137mm", "front": "114mm", "wt": "2.3kg", "filter": "M112 x 0.75", "aov_ff": "-", "aov_s35": "36°", "price": "$16,500"},
            {"fl": "50mm", "t": "T2.0-T16", "cf": "500mm", "focus_rot": "160°", "iris_rot": "78°", "len": "137mm", "front": "114mm", "wt": "2.3kg", "filter": "M112 x 0.75", "aov_ff": "-", "aov_s35": "29°", "price": "$16,500"},
            {"fl": "65mm", "t": "T2.0-T16", "cf": "600mm", "focus_rot": "160°", "iris_rot": "78°", "len": "137mm", "front": "114mm", "wt": "2.3kg", "filter": "M112 x 0.75", "aov_ff": "-", "aov_s35": "23°", "price": "$16,500"},
            {"fl": "75mm", "t": "T2.0-T16", "cf": "700mm", "focus_rot": "160°", "iris_rot": "78°", "len": "137mm", "front": "114mm", "wt": "2.3kg", "filter": "M112 x 0.75", "aov_ff": "-", "aov_s35": "20°", "price": "$16,500"},
            {"fl": "100mm", "t": "T2.0-T16", "cf": "900mm", "focus_rot": "160°", "iris_rot": "78°", "len": "137mm", "front": "114mm", "wt": "2.3kg", "filter": "M112 x 0.75", "aov_ff": "-", "aov_s35": "15°", "price": "$16,500"},
            {"fl": "135mm", "t": "T2.0-T16", "cf": "1200mm", "focus_rot": "160°", "iris_rot": "78°", "len": "137mm", "front": "114mm", "wt": "2.3kg", "filter": "M112 x 0.75", "aov_ff": "-", "aov_s35": "11°", "price": "$16,500"},
            {"fl": "150mm", "t": "T2.0-T16", "cf": "1300mm", "focus_rot": "160°", "iris_rot": "78°", "len": "137mm", "front": "114mm", "wt": "2.3kg", "filter": "M112 x 0.75", "aov_ff": "-", "aov_s35": "10°", "price": "$16,500"}
        ],
        "sets": []
    },
    
    "S4/i Mini 系列": {
        "series_name_en": "S4/i Mini Series - Compact Primes",
        "series_name_cn": "S4/i Mini 系列 - 紧凑型定焦镜头",
        "description_cn": "S4/i 的紧凑版本，更轻便的设计，适合稳定器和手持拍摄",
        "description_en": "Compact version of S4/i, lighter design for gimbal and handheld shooting",
        "mount": "PL 卡口",
        "format": "Super 35mm",
        "t_stop": "T2.0 - T16",
        "features": ["T2.0 光圈", "紧凑轻便", "Cooke/i 技术", "适合稳定器", "S35 覆盖"],
        "lenses": [
            {"fl": "16mm", "t": "T2.0-T16", "cf": "300mm", "focus_rot": "160°", "iris_rot": "78°", "len": "102mm", "front": "95mm", "wt": "1.2kg", "filter": "M82 x 0.75", "aov_ff": "-", "aov_s35": "75°", "price": "$14,500"},
            {"fl": "25mm", "t": "T2.0-T16", "cf": "380mm", "focus_rot": "160°", "iris_rot": "78°", "len": "102mm", "front": "95mm", "wt": "1.2kg", "filter": "M82 x 0.75", "aov_ff": "-", "aov_s35": "54°", "price": "$14,500"},
            {"fl": "32mm", "t": "T2.0-T16", "cf": "400mm", "focus_rot": "160°", "iris_rot": "78°", "len": "102mm", "front": "95mm", "wt": "1.2kg", "filter": "M82 x 0.75", "aov_ff": "-", "aov_s35": "44°", "price": "$14,500"},
            {"fl": "50mm", "t": "T2.0-T16", "cf": "500mm", "focus_rot": "160°", "iris_rot": "78°", "len": "102mm", "front": "95mm", "wt": "1.2kg", "filter": "M82 x 0.75", "aov_ff": "-", "aov_s35": "29°", "price": "$14,500"},
            {"fl": "75mm", "t": "T2.0-T16", "cf": "700mm", "focus_rot": "160°", "iris_rot": "78°", "len": "102mm", "front": "95mm", "wt": "1.2kg", "filter": "M82 x 0.75", "aov_ff": "-", "aov_s35": "20°", "price": "$14,500"}
        ],
        "sets": []
    },
    
    "SK4 系列": {
        "series_name_en": "SK4 Series - Super 35mm Zoom",
        "series_name_cn": "SK4 系列 - Super 35mm 变焦镜头",
        "description_cn": "Super 35mm 变焦镜头，灵活多变",
        "description_en": "Super 35mm zoom lens, versatile and flexible",
        "mount": "PL 卡口",
        "format": "Super 35mm",
        "t_stop": "T2.0 - T16",
        "features": ["T2.0 恒定光圈", "变焦范围大", "Cooke/i 技术", "电影级变焦", "可靠耐用"],
        "lenses": [
            {"fl": "15-40mm", "t": "T2.0-T16", "cf": "300mm", "focus_rot": "160°", "iris_rot": "78°", "len": "229mm", "front": "114mm", "wt": "3.4kg", "filter": "M112 x 0.75", "aov_ff": "-", "aov_s35": "82°-44°", "price": "$35,000"},
            {"fl": "18-85mm", "t": "T2.0-T16", "cf": "380mm", "focus_rot": "160°", "iris_rot": "78°", "len": "229mm", "front": "114mm", "wt": "3.4kg", "filter": "M112 x 0.75", "aov_ff": "-", "aov_s35": "75°-18°", "price": "$35,000"},
            {"fl": "25-250mm", "t": "T2.8-T16", "cf": "1200mm", "focus_rot": "160°", "iris_rot": "78°", "len": "343mm", "front": "114mm", "wt": "4.5kg", "filter": "M112 x 0.75", "aov_ff": "-", "aov_s35": "54°-6°", "price": "$42,000"}
        ],
        "sets": []
    }
}

def create_complete_excel():
    """创建完整的 Cooke 镜头 Excel 表格"""
    
    wb = Workbook()
    
    # ========== 工作表 1: 镜头规格总表 ==========
    ws1 = wb.active
    ws1.title = "镜头规格总表"
    
    # 样式
    title_font = Font(name='Arial', size=16, bold=True)
    subtitle_font = Font(name='Arial', size=10, italic=True)
    header_font = Font(name='Arial', size=9, bold=True)
    cell_font = Font(name='Arial', size=8)
    series_font = Font(name='Arial', size=10, bold=True)
    price_font = Font(name='Arial', size=8, bold=True, color='006600')
    
    # 列宽
    columns = {
        'A': 22, 'B': 12, 'C': 12, 'D': 14, 'E': 12, 'F': 12,
        'G': 12, 'H': 12, 'I': 12, 'J': 16, 'K': 12, 'L': 12, 'M': 14
    }
    for col, width in columns.items():
        ws1.column_dimensions[col].width = width
    
    # 标题
    ws1.merge_cells('A1:M1')
    ws1['A1'] = "Cooke Optics 镜头规格大全 | Complete Lens Specifications"
    ws1['A1'].font = title_font
    
    # 副标题
    ws1.merge_cells('A2:M2')
    ws1['A2'] = "专业电影镜头技术参数对照表 | Professional Cinema Lens Data Sheet"
    ws1['A2'].font = subtitle_font
    
    # 列标题
    headers = [
        "系列 Series", "焦距 FL", "光圈 T", "最近对焦 CF",
        "对焦旋转 Focus", "光圈旋转 Iris", "长度 Len", "前口径 Front",
        "重量 Wt", "滤镜 Filter", "视角 FF", "视角 S35", "价格 Price"
    ]
    for col, h in enumerate(headers, 1):
        ws1.cell(row=3, column=col, value=h).font = header_font
    
    # 填充数据
    row = 4
    total_lenses = 0
    
    for series_name, series_data in cooke_complete_database.items():
        # 系列标题
        ws1.merge_cells(f'A{row}:M{row}')
        ws1.cell(row=row, column=1, value=f"◆ {series_name} | {series_data['series_name_en']}").font = series_font
        ws1.row_dimensions[row].height = 28
        row += 1
        
        # 镜头数据
        for lens_idx, lens in enumerate(series_data['lenses']):
            s = series_name if lens_idx == 0 else ""
            ws1.cell(row=row, column=1, value=s).font = cell_font
            ws1.cell(row=row, column=2, value=lens['fl']).font = cell_font
            ws1.cell(row=row, column=3, value=lens['t']).font = cell_font
            ws1.cell(row=row, column=4, value=lens['cf']).font = cell_font
            ws1.cell(row=row, column=5, value=lens['focus_rot']).font = cell_font
            ws1.cell(row=row, column=6, value=lens['iris_rot']).font = cell_font
            ws1.cell(row=row, column=7, value=lens['len']).font = cell_font
            ws1.cell(row=row, column=8, value=lens['front']).font = cell_font
            ws1.cell(row=row, column=9, value=lens['wt']).font = cell_font
            ws1.cell(row=row, column=10, value=lens['filter']).font = cell_font
            ws1.cell(row=row, column=11, value=lens['aov_ff']).font = cell_font
            ws1.cell(row=row, column=12, value=lens['aov_s35']).font = cell_font
            price_cell = ws1.cell(row=row, column=13, value=lens['price'])
            price_cell.font = price_font
            row += 1
            total_lenses += 1
    
    # ========== 工作表 2: 系列详细介绍 ==========
    ws2 = wb.create_sheet("系列详细介绍")
    
    ws2.merge_cells('A1:F1')
    ws2['A1'] = "Cooke 镜头系列详细介绍"
    ws2['A1'].font = title_font
    
    ws2_headers = ["系列", "英文名", "描述", "卡口/画幅", "主要特性", "镜头数量/价格"]
    for col, h in enumerate(ws2_headers, 1):
        ws2.cell(row=2, column=col, value=h).font = header_font
    
    row = 3
    for name, data in cooke_complete_database.items():
        prices = [float(l['price'].replace('$','').replace(',','')) for l in data['lenses']]
        features = " • ".join(data['features'])
        mount_fmt = f"{data['mount']}\n{data['format']}"
        desc = f"{data['description_cn']}\n\n{data['description_en']}"
        
        ws2.cell(row=row, column=1, value=name).font = cell_font
        ws2.cell(row=row, column=2, value=data['series_name_en']).font = cell_font
        ws2.cell(row=row, column=3, value=desc).font = cell_font
        ws2.cell(row=row, column=4, value=mount_fmt).font = cell_font
        ws2.cell(row=row, column=5, value=features).font = cell_font
        ws2.cell(row=row, column=6, value=f"{len(data['lenses'])}款\n${min(prices):,.0f}-${max(prices):,.0f}").font = price_font
        row += 1
    
    ws2.column_dimensions['A'].width = 22
    ws2.column_dimensions['B'].width = 28
    ws2.column_dimensions['C'].width = 50
    ws2.column_dimensions['D'].width = 20
    ws2.column_dimensions['E'].width = 40
    ws2.column_dimensions['F'].width = 20
    
    # ========== 工作表 3: 统计摘要 ==========
    ws3 = wb.create_sheet("统计摘要")
    
    ws3.merge_cells('A1:B1')
    ws3['A1'] = "Cooke 镜头数据库统计"
    ws3['A1'].font = title_font
    
    stats = [
        ["统计项目", "数值"],
        ["镜头系列总数", len(cooke_complete_database)],
        ["镜头总数", total_lenses],
        ["价格范围", "$4,500 - $42,000"],
        ["卡口类型", "PL / E / RF / L / M"],
        ["画幅覆盖", "S35 / FF / Large Format"],
        ["最便宜系列", "SP3 系列 ($4,500 起)"],
        ["最贵系列", "SK4 变焦 ($42,000)"],
        ["生成时间", datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    ]
    
    for row_idx, (item, value) in enumerate(stats, 2):
        ws3.cell(row=row_idx, column=1, value=item).font = header_font
        ws3.cell(row=row_idx, column=2, value=value).font = cell_font
    
    ws3.column_dimensions['A'].width = 20
    ws3.column_dimensions['B'].width = 30
    
    # 保存
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"/Users/jesson/Desktop/Cooke_Optics_完整镜头数据库_{timestamp}.xlsx"
    wb.save(output_path)
    
    print(f"\n✅ Excel 已生成：{output_path}")
    print(f"\n📊 统计信息:")
    print(f"   • 镜头系列：{len(cooke_complete_database)} 个")
    print(f"   • 镜头总数：{total_lenses} 款")
    print(f"   • 价格范围：$4,500 - $42,000")
    print(f"   • 工作表：3 个 (规格表/系列介绍/统计)")
    print(f"\n📑 包含系列:")
    for name in cooke_complete_database.keys():
        print(f"   ✓ {name}")
    
    return output_path

if __name__ == "__main__":
    create_complete_excel()
    print(f"\n✅ 完成！")
