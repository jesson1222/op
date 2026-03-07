#!/usr/bin/env python3
"""
Cooke Optics 镜头数据 - 完整版
生成专业的中英文对照 Excel 图文表格
"""

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill, Color
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image
from openpyxl.chart import BarChart, Reference
import os

# 完整的 Cooke 镜头数据
cooke_lenses_complete = {
    "SP3 系列": {
        "series_name_en": "SP3 Series - Mirrorless Primes",
        "series_name_cn": "SP3 系列 - 无反定焦镜头",
        "description_cn": "基于 Speed Panchro 设计的全画幅球面定焦镜头，专为现代无反相机优化",
        "description_en": "Full Frame spherical prime lenses based on Speed Panchro design, optimized for modern mirrorless cameras",
        "features": [
            "T2.4 大光圈",
            "全画幅覆盖（兼容 S35）",
            "可更换卡口（E/RF/L/M）",
            "与 Panchro/i Classic 系列匹配",
            "小巧轻便设计",
            "经典 Cooke Look 成像风格"
        ],
        "lenses": [
            {"focal_length": "18mm", "aperture": "T2.4-T16", "close_focus": "123mm", "focus_rotation": "160°", "length": "109mm", "front_dia": "82mm", "weight": "688g", "filter": "M77 x 0.75", "angle_ff": "99°", "angle_s35": "82°", "price": "$4,500"},
            {"focal_length": "25mm", "aperture": "T2.4-T16", "close_focus": "139mm", "focus_rotation": "160°", "length": "98mm", "front_dia": "64mm", "weight": "575g", "filter": "M58 x 0.75", "angle_ff": "81°", "angle_s35": "62°", "price": "$4,500"},
            {"focal_length": "32mm", "aperture": "T2.4-T16", "close_focus": "223mm", "focus_rotation": "160°", "length": "94mm", "front_dia": "64mm", "weight": "520g", "filter": "M58 x 0.75", "angle_ff": "69°", "angle_s35": "50°", "price": "$4,500"},
            {"focal_length": "50mm", "aperture": "T2.4-T16", "close_focus": "394mm", "focus_rotation": "160°", "length": "94mm", "front_dia": "64mm", "weight": "500g", "filter": "M58 x 0.75", "angle_ff": "47°", "angle_s35": "34°", "price": "$4,500"},
            {"focal_length": "75mm", "aperture": "T2.4-T16", "close_focus": "689mm", "focus_rotation": "160°", "length": "98mm", "front_dia": "64mm", "weight": "520g", "filter": "M58 x 0.75", "angle_ff": "32°", "angle_s35": "22°", "price": "$4,500"},
            {"focal_length": "100mm", "aperture": "T2.4-T16", "close_focus": "663mm", "focus_rotation": "160°", "length": "124mm", "front_dia": "82mm", "weight": "690g", "filter": "M77 x 0.75", "angle_ff": "25°", "angle_s35": "17°", "price": "$4,970"}
        ]
    },
    "Panchro 65/i 系列": {
        "series_name_en": "Panchro 65/i Series - Large Format Primes",
        "series_name_cn": "Panchro 65/i 系列 - 大画幅定焦镜头",
        "description_cn": "为最重要的故事而生，大画幅电影镜头，继承 Cooke 经典 Speed Panchro 设计",
        "description_en": "Large format prime lenses for the biggest stories, inheriting Cooke's classic Speed Panchro design",
        "features": [
            "T1.8 超大光圈",
            "大画幅覆盖",
            "Cooke/i 技术",
            "经典 Cooke Look",
            "电影级光学性能",
            "坚固耐用的机械结构"
        ],
        "lenses": [
            {"focal_length": "35mm", "aperture": "T1.8", "close_focus": "350mm", "focus_rotation": "160°", "length": "152mm", "front_dia": "95mm", "weight": "1.8kg", "filter": "M82 x 0.75", "angle_ff": "63°", "angle_s35": "44°", "price": "$12,500"},
            {"focal_length": "50mm", "aperture": "T1.8", "close_focus": "450mm", "focus_rotation": "160°", "length": "152mm", "front_dia": "95mm", "weight": "1.8kg", "filter": "M82 x 0.75", "angle_ff": "47°", "angle_s35": "32°", "price": "$12,500"},
            {"focal_length": "65mm", "aperture": "T1.8", "close_focus": "550mm", "focus_rotation": "160°", "length": "152mm", "front_dia": "95mm", "weight": "1.8kg", "filter": "M82 x 0.75", "angle_ff": "37°", "angle_s35": "25°", "price": "$12,500"}
        ]
    },
    "S8/i FF 系列": {
        "series_name_en": "S8/i FF Series - Full Frame Primes",
        "series_name_cn": "S8/i FF 系列 - 全画幅定焦镜头",
        "description_cn": "搭载 Cooke/i 技术的全画幅定焦镜头，代表 Cooke 最高光学水准",
        "description_en": "Full Frame prime lenses with Cooke/i Technology, representing Cooke's highest optical standards",
        "features": [
            "T1.8 大光圈",
            "全画幅覆盖",
            "Cooke/i 元数据技术",
            "8K 分辨率支持",
            "完美匹配的电影镜头组",
            "专业电影制作标准"
        ],
        "lenses": [
            {"focal_length": "21mm", "aperture": "T1.8", "close_focus": "350mm", "focus_rotation": "160°", "length": "178mm", "front_dia": "114mm", "weight": "2.5kg", "filter": "M112 x 0.75", "angle_ff": "82°", "angle_s35": "56°", "price": "$18,500"},
            {"focal_length": "32mm", "aperture": "T1.8", "close_focus": "400mm", "focus_rotation": "160°", "length": "178mm", "front_dia": "114mm", "weight": "2.5kg", "filter": "M112 x 0.75", "angle_ff": "69°", "angle_s35": "47°", "price": "$18,500"},
            {"focal_length": "50mm", "aperture": "T1.8", "close_focus": "500mm", "focus_rotation": "160°", "length": "178mm", "front_dia": "114mm", "weight": "2.5kg", "filter": "M112 x 0.75", "angle_ff": "47°", "angle_s35": "32°", "price": "$18,500"},
            {"focal_length": "75mm", "aperture": "T1.8", "close_focus": "700mm", "focus_rotation": "160°", "length": "178mm", "front_dia": "114mm", "weight": "2.5kg", "filter": "M112 x 0.75", "angle_ff": "32°", "angle_s35": "22°", "price": "$18,500"}
        ]
    },
    "Panchro/i Classic FF 系列": {
        "series_name_en": "Panchro/i Classic FF Series",
        "series_name_cn": "Panchro/i Classic FF 系列",
        "description_cn": "经典 Speed Panchro 设计的现代复刻，全画幅覆盖",
        "description_en": "Modern recreation of classic Speed Panchro design, Full Frame coverage",
        "features": [
            "T2.2 光圈",
            "经典 Cooke Look",
            "全画幅覆盖",
            "Cooke/i 技术",
            "复古与现代的完美结合",
            "电影感成像"
        ],
        "lenses": [
            {"focal_length": "35mm", "aperture": "T2.2", "close_focus": "380mm", "focus_rotation": "160°", "length": "142mm", "front_dia": "95mm", "weight": "1.6kg", "filter": "M82 x 0.75", "angle_ff": "63°", "angle_s35": "44°", "price": "$11,500"},
            {"focal_length": "50mm", "aperture": "T2.2", "close_focus": "480mm", "focus_rotation": "160°", "length": "142mm", "front_dia": "95mm", "weight": "1.6kg", "filter": "M82 x 0.75", "angle_ff": "47°", "angle_s35": "32°", "price": "$11,500"},
            {"focal_length": "75mm", "aperture": "T2.2", "close_focus": "680mm", "focus_rotation": "160°", "length": "142mm", "front_dia": "95mm", "weight": "1.6kg", "filter": "M82 x 0.75", "angle_ff": "32°", "angle_s35": "22°", "price": "$11,500"}
        ]
    }
}

def create_professional_excel():
    """创建专业级 Excel 表格"""
    
    wb = Workbook()
    
    # ========== 工作表 1: 镜头规格总表 ==========
    ws1 = wb.active
    ws1.title = "镜头规格总表"
    
    # 定义专业样式
    title_font = Font(name='Microsoft YaHei', size=20, bold=True, color='FFFFFF')
    subtitle_font = Font(name='Arial', size=12, bold=True, color='E0E0E0')
    header_font = Font(name='Microsoft YaHei', size=11, bold=True, color='FFFFFF')
    header_font_en = Font(name='Arial', size=9, bold=True, color='CCCCCC')
    cell_font = Font(name='Microsoft YaHei', size=10)
    cell_font_en = Font(name='Arial', size=9, color='666666')
    price_font = Font(name='Arial', size=10, bold=True, color='C9A962')
    
    # 填充颜色 - 高级黑金配色
    title_fill = PatternFill(start_color='0D0D0D', end_color='0D0D0D', fill_type='solid')
    header_fill = PatternFill(start_color='1A1A1A', end_color='1A1A1A', fill_type='solid')
    header_fill_en = PatternFill(start_color='2D2D2D', end_color='2D2D2D', fill_type='solid')
    series_fill = PatternFill(start_color='3D3D3D', end_color='3D3D3D', fill_type='solid')
    alt_fill = PatternFill(start_color='F8F8F8', end_color='F8F8F8', fill_type='solid')
    highlight_fill = PatternFill(start_color='FFF8E7', end_color='FFF8E7', fill_type='solid')
    white_fill = PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')
    
    # 边框
    thin_border = Border(
        left=Side(style='thin', color='DDDDDD'),
        right=Side(style='thin', color='DDDDDD'),
        top=Side(style='thin', color='DDDDDD'),
        bottom=Side(style='thin', color='DDDDDD')
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
    right_align = Alignment(horizontal='right', vertical='center', wrap_text=True)
    
    # 列宽设置
    column_widths = {
        'A': 18,  # 系列
        'B': 14,  # 焦距
        'C': 16,  # 光圈
        'D': 16,  # 最近对焦
        'E': 16,  # 对焦旋转
        'F': 16,  # 光圈旋转
        'G': 14,  # 长度
        'H': 14,  # 前口径
        'I': 14,  # 重量
        'J': 18,  # 滤镜螺纹
        'K': 14,  # 视角 FF
        'L': 14,  # 视角 S35
        'M': 16,  # 价格
    }
    
    for col, width in column_widths.items():
        ws1.column_dimensions[col].width = width
    
    # 行高
    ws1.row_dimensions[1].height = 50  # 主标题
    ws1.row_dimensions[2].height = 30  # 副标题
    ws1.row_dimensions[3].height = 30  # 列标题
    
    # 创建主标题
    ws1.merge_cells('A1:M1')
    ws1['A1'] = "Cooke Optics 镜头规格大全"
    ws1['A1'].font = title_font
    ws1['A1'].fill = title_fill
    ws1['A1'].alignment = center_align
    ws1['A1'].border = thick_border
    
    # 副标题
    ws1.merge_cells('A2:M2')
    ws1['A2'] = "Complete Lens Specifications | 专业电影镜头技术参数对照表"
    ws1['A2'].font = subtitle_font
    ws1['A2'].fill = title_fill
    ws1['A2'].alignment = center_align
    ws1['A2'].border = thick_border
    
    # 中英文列标题
    headers_cn_en = [
        ("镜头系列", "Series"),
        ("焦距", "Focal Length"),
        ("光圈范围", "Aperture"),
        ("最近对焦", "Close Focus"),
        ("对焦旋转", "Focus Rotation"),
        ("光圈旋转", "Iris Rotation"),
        ("镜头长度", "Length"),
        ("前组直径", "Front Dia."),
        ("重量", "Weight"),
        ("滤镜螺纹", "Filter Thread"),
        ("视角 FF", "A.O.V FF"),
        ("视角 S35", "A.O.V S35"),
        ("参考价格", "Price")
    ]
    
    for col, (cn, en) in enumerate(headers_cn_en, 1):
        cell = ws1.cell(row=3, column=col, value=f"{cn}\n{en}")
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align
        cell.border = thin_border
    
    # 填充镜头数据
    current_row = 4
    
    for series_name, series_data in cooke_lenses_complete.items():
        # 系列标题行
        ws1.merge_cells(f'A{current_row}:M{current_row}')
        series_cell = ws1.cell(row=current_row, column=1, value=f"◆ {series_name} | {series_data['series_name_en']}")
        series_cell.font = Font(name='Microsoft YaHei', size=12, bold=True, color='FFFFFF')
        series_cell.fill = series_fill
        series_cell.alignment = left_align
        series_cell.border = thick_border
        ws1.row_dimensions[current_row].height = 30
        current_row += 1
        
        # 镜头数据行
        for lens_idx, lens in enumerate(series_data['lenses']):
            series_text = series_name if lens_idx == 0 else ""
            
            row_data = [
                series_text,
                lens['focal_length'],
                lens['aperture'],
                lens['close_focus'],
                lens.get('focus_rotation', '160°'),
                lens.get('iris_rotation', '78°'),
                lens['length'],
                lens['front_dia'],
                lens['weight'],
                lens['filter'],
                lens['angle_ff'],
                lens['angle_s35'],
                lens['price']
            ]
            
            for col, value in enumerate(row_data, 1):
                cell = ws1.cell(row=current_row, column=col, value=value)
                cell.font = cell_font
                cell.alignment = center_align
                cell.border = thin_border
                
                # 价格特殊样式
                if col == 13:
                    cell.font = price_font
                    cell.fill = highlight_fill
                # 交替行颜色
                elif current_row % 2 == 1:
                    cell.fill = alt_fill
                else:
                    cell.fill = white_fill
            
            ws1.row_dimensions[current_row].height = 28
            current_row += 1
    
    # ========== 工作表 2: 系列详细介绍 ==========
    ws2 = wb.create_sheet(title="系列详细介绍")
    
    ws2.merge_cells('A1:E1')
    ws2['A1'] = "Cooke 镜头系列详细介绍"
    ws2['A1'].font = title_font
    ws2['A1'].fill = title_fill
    ws2['A1'].alignment = center_align
    ws2.row_dimensions[1].height = 50
    
    ws2.merge_cells('A2:E2')
    ws2['A2'] = "Lens Series Detailed Introduction"
    ws2['A2'].font = subtitle_font
    ws2['A2'].fill = title_fill
    ws2['A2'].alignment = center_align
    ws2.row_dimensions[2].height = 30
    
    # 系列介绍标题
    info_headers = ["系列名称\nSeries", "英文名\nEnglish", "特点描述\nDescription", "主要特性\nFeatures", "镜头数量/价格\nCount/Price"]
    for col, header in enumerate(info_headers, 1):
        cell = ws2.cell(row=3, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align
        cell.border = thin_border
    
    # 填充系列信息
    for idx, (series_name, series_data) in enumerate(cooke_lenses_complete.items(), 4):
        lens_count = len(series_data['lenses'])
        prices = [float(l['price'].replace('$', '').replace(',', '')) for l in series_data['lenses']]
        price_range = f"${min(prices):,.0f} - ${max(prices):,.0f}"
        features_text = "\n".join([f"• {f}" for f in series_data['features']])
        
        ws2.cell(row=idx, column=1, value=series_name).font = cell_font
        ws2.cell(row=idx, column=2, value=series_data['series_name_en']).font = cell_font_en
        ws2.cell(row=idx, column=3, value=f"{series_data['description_cn']}\n\n{series_data['description_en']}").font = cell_font
        ws2.cell(row=idx, column=4, value=features_text).font = cell_font
        ws2.cell(row=idx, column=5, value=f"{lens_count} 款\n{price_range}").font = price_font
        
        for col in range(1, 6):
            ws2.cell(row=idx, column=col).alignment = left_align if col in [3, 4] else center_align
            ws2.cell(row=idx, column=col).border = thin_border
            ws2.cell(row=idx, column=col).fill = alt_fill if idx % 2 == 0 else white_fill
    
    ws2.column_dimensions['A'].width = 22
    ws2.column_dimensions['B'].width = 28
    ws2.column_dimensions['C'].width = 55
    ws2.column_dimensions['D'].width = 35
    ws2.column_dimensions['E'].width = 20
    
    # ========== 工作表 3: 快速选型指南 ==========
    ws3 = wb.create_sheet(title="快速选型指南")
    
    ws3.merge_cells('A1:H1')
    ws3['A1'] = "镜头快速选型指南"
    ws3['A1'].font = title_font
    ws3['A1'].fill = title_fill
    ws3['A1'].alignment = center_align
    ws3.row_dimensions[1].height = 50
    
    ws3.merge_cells('A2:H2')
    ws3['A2'] = "Quick Selection Guide"
    ws3['A2'].font = subtitle_font
    ws3['A2'].fill = title_fill
    ws3['A2'].alignment = center_align
    ws3.row_dimensions[2].height = 30
    
    # 选型指南内容
    selection_guide = [
        ["拍摄类型", "推荐系列", "推荐焦距", "理由", "预算范围"],
        ["纪录片/新闻", "SP3 系列", "25mm, 32mm, 50mm", "轻便、快速、性价比高", "$4,500 - $5,000"],
        ["剧情片/广告", "Panchro 65/i", "35mm, 50mm, 65mm", "大光圈、电影感强", "$12,000 - $13,000"],
        ["高端电影制作", "S8/i FF", "21mm, 32mm, 50mm, 75mm", "最高光学素质、8K 支持", "$18,000 - $19,000"],
        ["复古风格", "Panchro/i Classic", "35mm, 50mm, 75mm", "经典 Cooke Look", "$11,000 - $12,000"],
        ["人像特写", "SP3 / S8/i", "75mm, 100mm", "浅景深、背景虚化美", "$4,500 - $18,500"],
        ["风光/建筑", "SP3 / S8/i", "18mm, 21mm, 25mm", "广角、边缘画质好", "$4,500 - $18,500"]
    ]
    
    for row_idx, row_data in enumerate(selection_guide, 3):
        for col_idx, value in enumerate(row_data, 1):
            cell = ws3.cell(row=row_idx, column=col_idx, value=value)
            cell.font = header_font if row_idx == 3 else cell_font
            cell.fill = header_fill if row_idx == 3 else (alt_fill if row_idx % 2 == 0 else white_fill)
            cell.alignment = center_align
            cell.border = thin_border
    
    ws3.column_dimensions['A'].width = 18
    ws3.column_dimensions['B'].width = 22
    ws3.column_dimensions['C'].width = 20
    ws3.column_dimensions['D'].width = 35
    ws3.column_dimensions['E'].width = 18
    
    # 保存文件
    output_path = "/Users/jesson/Desktop/Cooke_Optics_镜头规格大全_完整版.xlsx"
    wb.save(output_path)
    
    print(f"\n✅ Excel 文件已生成：{output_path}")
    print(f"\n📊 统计信息:")
    print(f"   • 共包含 {len(cooke_lenses_complete)} 个系列")
    total_lenses = sum([len(s['lenses']) for s in cooke_lenses_complete.values()])
    print(f"   • 共包含 {total_lenses} 款镜头")
    all_prices = [float(l['price'].replace('$', '').replace(',', '')) for s in cooke_lenses_complete.values() for l in s['lenses']]
    print(f"   • 价格范围：${min(all_prices):,.0f} - ${max(all_prices):,.0f}")
    print(f"   • 工作表数量：3 个")
    print(f"\n📑 工作表列表:")
    print(f"   1. 镜头规格总表 - 完整技术参数")
    print(f"   2. 系列详细介绍 - 特点与描述")
    print(f"   3. 快速选型指南 - 选购建议")
    print(f"\n🎨 设计特色:")
    print(f"   • 专业黑金配色方案")
    print(f"   • 中英文双语对照")
    print(f"   • 清晰的视觉层次")
    print(f"   • 交替行颜色便于阅读")
    print(f"   • 价格高亮显示")
    
    return output_path

if __name__ == "__main__":
    create_professional_excel()
    print(f"\n✅ 完成！文件已保存到桌面")
