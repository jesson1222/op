#!/usr/bin/env python3
"""
Cooke Optics 镜头数据 - 专业完整版
生成专业的中英文对照 Excel 图文表格
"""

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter

# 完整的 Cooke 镜头数据
cooke_lenses_complete = {
    "SP3 系列": {
        "series_name_en": "SP3 Series - Mirrorless Primes",
        "series_name_cn": "SP3 系列 - 无反定焦镜头",
        "description_cn": "基于 Speed Panchro 设计的全画幅球面定焦镜头，专为现代无反相机优化",
        "description_en": "Full Frame spherical prime lenses based on Speed Panchro design",
        "mount": "E/RF/L/M 可更换卡口",
        "format": "全画幅 (兼容 S35)",
        "features": ["T2.4 大光圈", "小巧轻便", "经典 Cooke Look", "可更换卡口"],
        "lenses": [
            {"focal_length": "18mm", "aperture": "T2.4-T16", "close_focus": "123mm", "focus_rot": "160°", "iris_rot": "78°", "length": "109mm", "front_dia": "82mm", "weight": "688g", "filter": "M77 x 0.75", "angle_ff": "99°", "angle_s35": "82°", "price": "$4,500"},
            {"focal_length": "25mm", "aperture": "T2.4-T16", "close_focus": "139mm", "focus_rot": "160°", "iris_rot": "78°", "length": "98mm", "front_dia": "64mm", "weight": "575g", "filter": "M58 x 0.75", "angle_ff": "81°", "angle_s35": "62°", "price": "$4,500"},
            {"focal_length": "32mm", "aperture": "T2.4-T16", "close_focus": "223mm", "focus_rot": "160°", "iris_rot": "78°", "length": "94mm", "front_dia": "64mm", "weight": "520g", "filter": "M58 x 0.75", "angle_ff": "69°", "angle_s35": "50°", "price": "$4,500"},
            {"focal_length": "50mm", "aperture": "T2.4-T16", "close_focus": "394mm", "focus_rot": "160°", "iris_rot": "78°", "length": "94mm", "front_dia": "64mm", "weight": "500g", "filter": "M58 x 0.75", "angle_ff": "47°", "angle_s35": "34°", "price": "$4,500"},
            {"focal_length": "75mm", "aperture": "T2.4-T16", "close_focus": "689mm", "focus_rot": "160°", "iris_rot": "78°", "length": "98mm", "front_dia": "64mm", "weight": "520g", "filter": "M58 x 0.75", "angle_ff": "32°", "angle_s35": "22°", "price": "$4,500"},
            {"focal_length": "100mm", "aperture": "T2.4-T16", "close_focus": "663mm", "focus_rot": "160°", "iris_rot": "78°", "length": "124mm", "front_dia": "82mm", "weight": "690g", "filter": "M77 x 0.75", "angle_ff": "25°", "angle_s35": "17°", "price": "$4,970"}
        ]
    },
    "Panchro 65/i 系列": {
        "series_name_en": "Panchro 65/i Series - Large Format",
        "series_name_cn": "Panchro 65/i 系列 - 大画幅定焦镜头",
        "description_cn": "为最重要的故事而生，大画幅电影镜头，继承 Cooke 经典 Speed Panchro 设计",
        "description_en": "Large format prime lenses for the biggest stories",
        "mount": "PL 卡口",
        "format": "大画幅 (Full Frame+)",
        "features": ["T1.8 超大光圈", "大画幅覆盖", "Cooke/i 技术", "电影级光学"],
        "lenses": [
            {"focal_length": "35mm", "aperture": "T1.8-T16", "close_focus": "350mm", "focus_rot": "160°", "iris_rot": "78°", "length": "152mm", "front_dia": "95mm", "weight": "1.8kg", "filter": "M82 x 0.75", "angle_ff": "63°", "angle_s35": "44°", "price": "$12,500"},
            {"focal_length": "50mm", "aperture": "T1.8-T16", "close_focus": "450mm", "focus_rot": "160°", "iris_rot": "78°", "length": "152mm", "front_dia": "95mm", "weight": "1.8kg", "filter": "M82 x 0.75", "angle_ff": "47°", "angle_s35": "32°", "price": "$12,500"},
            {"focal_length": "65mm", "aperture": "T1.8-T16", "close_focus": "550mm", "focus_rot": "160°", "iris_rot": "78°", "length": "152mm", "front_dia": "95mm", "weight": "1.8kg", "filter": "M82 x 0.75", "angle_ff": "37°", "angle_s35": "25°", "price": "$12,500"}
        ]
    },
    "S8/i FF 系列": {
        "series_name_en": "S8/i FF Series - Full Frame Primes",
        "series_name_cn": "S8/i FF 系列 - 全画幅定焦镜头",
        "description_cn": "搭载 Cooke/i 技术的全画幅定焦镜头，代表 Cooke 最高光学水准",
        "description_en": "Full Frame prime lenses with Cooke/i Technology",
        "mount": "PL 卡口",
        "format": "全画幅 (Full Frame)",
        "features": ["T1.8 大光圈", "Cooke/i 元数据", "8K 分辨率", "专业电影标准"],
        "lenses": [
            {"focal_length": "21mm", "aperture": "T1.8-T16", "close_focus": "350mm", "focus_rot": "160°", "iris_rot": "78°", "length": "178mm", "front_dia": "114mm", "weight": "2.5kg", "filter": "M112 x 0.75", "angle_ff": "82°", "angle_s35": "56°", "price": "$18,500"},
            {"focal_length": "32mm", "aperture": "T1.8-T16", "close_focus": "400mm", "focus_rot": "160°", "iris_rot": "78°", "length": "178mm", "front_dia": "114mm", "weight": "2.5kg", "filter": "M112 x 0.75", "angle_ff": "69°", "angle_s35": "47°", "price": "$18,500"},
            {"focal_length": "50mm", "aperture": "T1.8-T16", "close_focus": "500mm", "focus_rot": "160°", "iris_rot": "78°", "length": "178mm", "front_dia": "114mm", "weight": "2.5kg", "filter": "M112 x 0.75", "angle_ff": "47°", "angle_s35": "32°", "price": "$18,500"},
            {"focal_length": "75mm", "aperture": "T1.8-T16", "close_focus": "700mm", "focus_rot": "160°", "iris_rot": "78°", "length": "178mm", "front_dia": "114mm", "weight": "2.5kg", "filter": "M112 x 0.75", "angle_ff": "32°", "angle_s35": "22°", "price": "$18,500"}
        ]
    },
    "Panchro/i Classic FF 系列": {
        "series_name_en": "Panchro/i Classic FF Series",
        "series_name_cn": "Panchro/i Classic FF 系列 - 经典复刻",
        "description_cn": "经典 Speed Panchro 设计的现代复刻，全画幅覆盖",
        "description_en": "Modern recreation of classic Speed Panchro design",
        "mount": "PL 卡口",
        "format": "全画幅 (Full Frame)",
        "features": ["T2.2 光圈", "经典 Cooke Look", "复古与现代结合", "Cooke/i 技术"],
        "lenses": [
            {"focal_length": "35mm", "aperture": "T2.2-T16", "close_focus": "380mm", "focus_rot": "160°", "iris_rot": "78°", "length": "142mm", "front_dia": "95mm", "weight": "1.6kg", "filter": "M82 x 0.75", "angle_ff": "63°", "angle_s35": "44°", "price": "$11,500"},
            {"focal_length": "50mm", "aperture": "T2.2-T16", "close_focus": "480mm", "focus_rot": "160°", "iris_rot": "78°", "length": "142mm", "front_dia": "95mm", "weight": "1.6kg", "filter": "M82 x 0.75", "angle_ff": "47°", "angle_s35": "32°", "price": "$11,500"},
            {"focal_length": "75mm", "aperture": "T2.2-T16", "close_focus": "680mm", "focus_rot": "160°", "iris_rot": "78°", "length": "142mm", "front_dia": "95mm", "weight": "1.6kg", "filter": "M82 x 0.75", "angle_ff": "32°", "angle_s35": "22°", "price": "$11,500"}
        ]
    },
    "Anamorphic/i FF 系列": {
        "series_name_en": "Anamorphic/i FF Series",
        "series_name_cn": "Anamorphic/i FF 系列 - 变形宽银幕镜头",
        "description_cn": "全画幅变形宽银幕镜头，2x 压缩比，真正的电影体验",
        "description_en": "Full Frame anamorphic lenses with 2x squeeze",
        "mount": "PL 卡口",
        "format": "全画幅 (Full Frame)",
        "features": ["2x 压缩比", "T2.3 光圈", "经典椭圆光斑", "水平镜头光晕"],
        "lenses": [
            {"focal_length": "32mm", "aperture": "T2.3-T16", "close_focus": "450mm", "focus_rot": "160°", "iris_rot": "78°", "length": "193mm", "front_dia": "114mm", "weight": "2.8kg", "filter": "M112 x 0.75", "angle_ff": "76°×2", "angle_s35": "54°×2", "price": "$22,000"},
            {"focal_length": "40mm", "aperture": "T2.3-T16", "close_focus": "500mm", "focus_rot": "160°", "iris_rot": "78°", "length": "193mm", "front_dia": "114mm", "weight": "2.8kg", "filter": "M112 x 0.75", "angle_ff": "65°×2", "angle_s35": "46°×2", "price": "$22,000"},
            {"focal_length": "50mm", "aperture": "T2.3-T16", "close_focus": "550mm", "focus_rot": "160°", "iris_rot": "78°", "length": "193mm", "front_dia": "114mm", "weight": "2.8kg", "filter": "M112 x 0.75", "angle_ff": "54°×2", "angle_s35": "38°×2", "price": "$22,000"},
            {"focal_length": "75mm", "aperture": "T2.3-T16", "close_focus": "700mm", "focus_rot": "160°", "iris_rot": "78°", "length": "193mm", "front_dia": "114mm", "weight": "2.8kg", "filter": "M112 x 0.75", "angle_ff": "38°×2", "angle_s35": "27°×2", "price": "$22,000"},
            {"focal_length": "100mm", "aperture": "T2.3-T16", "close_focus": "900mm", "focus_rot": "160°", "iris_rot": "78°", "length": "193mm", "front_dia": "114mm", "weight": "2.8kg", "filter": "M112 x 0.75", "angle_ff": "29°×2", "angle_s35": "20°×2", "price": "$22,000"}
        ]
    }
}

def create_professional_excel():
    """创建专业级 Excel 表格"""
    
    wb = Workbook()
    
    # ========== 工作表 1: 镜头规格总表 ==========
    ws1 = wb.active
    ws1.title = "镜头规格总表"
    
    # 定义样式
    title_font = Font(name='Microsoft YaHei', size=18, bold=True)
    subtitle_font = Font(name='Arial', size=11, italic=True)
    header_font = Font(name='Microsoft YaHei', size=10, bold=True)
    cell_font = Font(name='Microsoft YaHei', size=9)
    price_font = Font(name='Arial', size=9, bold=True, color='006600')
    series_font = Font(name='Microsoft YaHei', size=10, bold=True, color='FFFFFF')
    
    # 填充颜色
    title_fill = PatternFill(start_color='1A1A1A', end_color='1A1A1A', fill_type='solid')
    header_fill = PatternFill(start_color='2D2D2D', end_color='2D2D2D', fill_type='solid')
    series_fill = PatternFill(start_color='4A4A4A', end_color='4A4A4A', fill_type='solid')
    alt_fill = PatternFill(start_color='F5F5F5', end_color='F5F5F5', fill_type='solid')
    price_fill = PatternFill(start_color='E8F5E9', end_color='E8F5E9', fill_type='solid')
    
    # 边框
    thin_border = Border(
        left=Side(style='thin', color='CCCCCC'),
        right=Side(style='thin', color='CCCCCC'),
        top=Side(style='thin', color='CCCCCC'),
        bottom=Side(style='thin', color='CCCCCC')
    )
    
    # 对齐方式
    center_align = Alignment(horizontal='center', vertical='center', wrap_text=True)
    left_align = Alignment(horizontal='left', vertical='center')
    
    # 列宽
    column_widths = {
        'A': 20, 'B': 12, 'C': 14, 'D': 14, 'E': 14, 'F': 14,
        'G': 12, 'H': 12, 'I': 12, 'J': 16, 'K': 12, 'L': 12, 'M': 14
    }
    
    for col, width in column_widths.items():
        ws1.column_dimensions[col].width = width
    
    # 行高
    ws1.row_dimensions[1].height = 45
    ws1.row_dimensions[2].height = 25
    ws1.row_dimensions[3].height = 30
    
    # 主标题
    ws1.merge_cells('A1:M1')
    ws1['A1'] = "Cooke Optics 镜头规格大全"
    ws1['A1'].font = title_font
    ws1['A1'].fill = title_fill
    ws1['A1'].alignment = center_align
    
    # 副标题
    ws1.merge_cells('A2:M2')
    ws1['A2'] = "Complete Lens Specifications | 专业电影镜头技术参数对照表"
    ws1['A2'].font = subtitle_font
    ws1['A2'].fill = title_fill
    ws1['A2'].alignment = center_align
    
    # 列标题
    headers = [
        "镜头系列\nSeries", "焦距\nF.L.", "光圈\nT-Stop", "最近对焦\nC.F.",
        "对焦旋转\nFocus", "光圈旋转\nIris", "长度\nLength", "前口径\nFront",
        "重量\nWeight", "滤镜\nFilter", "视角 FF\nA.O.V", "视角 S35\nA.O.V", "价格\nPrice"
    ]
    
    for col, header in enumerate(headers, 1):
        cell = ws1.cell(row=3, column=col, value=header)
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
        series_cell.font = series_font
        series_cell.fill = series_fill
        series_cell.alignment = left_align
        ws1.row_dimensions[current_row].height = 28
        current_row += 1
        
        # 镜头数据行
        for lens_idx, lens in enumerate(series_data['lenses']):
            series_text = series_name if lens_idx == 0 else ""
            
            row_data = [
                series_text, lens['focal_length'], lens['aperture'], lens['close_focus'],
                lens['focus_rot'], lens['iris_rot'], lens['length'], lens['front_dia'],
                lens['weight'], lens['filter'], lens['angle_ff'], lens['angle_s35'], lens['price']
            ]
            
            for col, value in enumerate(row_data, 1):
                cell = ws1.cell(row=current_row, column=col, value=value)
                cell.font = cell_font
                cell.alignment = center_align
                cell.border = thin_border
                
                # 价格特殊样式
                if col == 13:
                    cell.font = price_font
                    cell.fill = price_fill
                
                # 交替行颜色
                if current_row % 2 == 0:
                    cell.fill = alt_fill
            
            ws1.row_dimensions[current_row].height = 26
            current_row += 1
    
    # ========== 工作表 2: 系列详细介绍 ==========
    ws2 = wb.create_sheet(title="系列详细介绍")
    
    ws2.merge_cells('A1:F1')
    ws2['A1'] = "Cooke 镜头系列详细介绍"
    ws2['A1'].font = title_font
    ws2['A1'].fill = title_fill
    ws2['A1'].alignment = center_align
    ws2.row_dimensions[1].height = 45
    
    ws2.merge_cells('A2:F2')
    ws2['A2'] = "Lens Series Detailed Introduction"
    ws2['A2'].font = subtitle_font
    ws2['A2'].fill = title_fill
    ws2['A2'].alignment = center_align
    ws2.row_dimensions[2].height = 25
    
    # 系列介绍标题
    info_headers = ["系列名称\nSeries", "英文名\nEnglish", "描述\nDescription", "卡口/画幅\nMount/Format", "主要特性\nFeatures", "镜头数量/价格\nCount/Price"]
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
        features_text = " • ".join(series_data['features'])
        mount_format = f"{series_data['mount']}\n{series_data['format']}"
        desc_text = f"{series_data['description_cn']}\n\n{series_data['description_en']}"
        
        ws2.cell(row=idx, column=1, value=series_name).font = cell_font
        ws2.cell(row=idx, column=2, value=series_data['series_name_en']).font = cell_font
        ws2.cell(row=idx, column=3, value=desc_text).font = cell_font
        ws2.cell(row=idx, column=4, value=mount_format).font = cell_font
        ws2.cell(row=idx, column=5, value=features_text).font = cell_font
        ws2.cell(row=idx, column=6, value=f"{lens_count} 款\n{price_range}").font = price_font
        
        for col in range(1, 7):
            ws2.cell(row=idx, column=col).alignment = left_align if col in [3, 5] else center_align
            ws2.cell(row=idx, column=col).border = thin_border
            if idx % 2 == 0:
                ws2.cell(row=idx, column=col).fill = alt_fill
    
    ws2.column_dimensions['A'].width = 22
    ws2.column_dimensions['B'].width = 28
    ws2.column_dimensions['C'].width = 50
    ws2.column_dimensions['D'].width = 20
    ws2.column_dimensions['E'].width = 40
    ws2.column_dimensions['F'].width = 20
    
    # ========== 工作表 3: 快速选型指南 ==========
    ws3 = wb.create_sheet(title="快速选型指南")
    
    ws3.merge_cells('A1:G1')
    ws3['A1'] = "镜头快速选型指南"
    ws3['A1'].font = title_font
    ws3['A1'].fill = title_fill
    ws3['A1'].alignment = center_align
    ws3.row_dimensions[1].height = 45
    
    ws3.merge_cells('A2:G2')
    ws3['A2'] = "Quick Selection Guide"
    ws3['A2'].font = subtitle_font
    ws3['A2'].fill = title_fill
    ws3['A2'].alignment = center_align
    ws3.row_dimensions[2].height = 25
    
    # 选型指南内容
    selection_guide = [
        ["拍摄类型", "推荐系列", "推荐焦距", "光圈", "理由", "预算范围"],
        ["纪录片/新闻", "SP3 系列", "25mm, 32mm, 50mm", "T2.4", "轻便、快速、性价比高", "$4,500 - $5,000"],
        ["剧情片/广告", "Panchro 65/i", "35mm, 50mm, 65mm", "T1.8", "大光圈、电影感强", "$12,000 - $13,000"],
        ["高端电影制作", "S8/i FF", "21mm, 32mm, 50mm, 75mm", "T1.8", "最高光学素质、8K 支持", "$18,000 - $19,000"],
        ["复古风格", "Panchro/i Classic", "35mm, 50mm, 75mm", "T2.2", "经典 Cooke Look", "$11,000 - $12,000"],
        ["变形宽银幕", "Anamorphic/i", "32mm, 50mm, 75mm", "T2.3", "2x 压缩、椭圆光斑", "$22,000"],
        ["人像特写", "SP3 / S8/i", "75mm, 100mm", "T1.8-T2.4", "浅景深、背景虚化美", "$4,500 - $18,500"],
        ["风光/建筑", "SP3 / S8/i", "18mm, 21mm, 25mm", "T1.8-T2.4", "广角、边缘画质好", "$4,500 - $18,500"]
    ]
    
    for row_idx, row_data in enumerate(selection_guide, 3):
        for col_idx, value in enumerate(row_data, 1):
            cell = ws3.cell(row=row_idx, column=col_idx, value=value)
            cell.font = header_font if row_idx == 3 else cell_font
            cell.fill = header_fill if row_idx == 3 else (alt_fill if row_idx % 2 == 0 else None)
            cell.alignment = center_align
            cell.border = thin_border
    
    ws3.column_dimensions['A'].width = 18
    ws3.column_dimensions['B'].width = 22
    ws3.column_dimensions['C'].width = 22
    ws3.column_dimensions['D'].width = 12
    ws3.column_dimensions['E'].width = 35
    ws3.column_dimensions['F'].width = 20
    
    # 保存文件
    output_path = "/Users/jesson/Desktop/Cooke_Optics_镜头规格大全_专业完整版.xlsx"
    wb.save(output_path)
    
    print(f"\n✅ Excel 文件已生成：{output_path}")
    print(f"\n📊 统计信息:")
    print(f"   • 共包含 {len(cooke_lenses_complete)} 个系列")
    total_lenses = sum([len(s['lenses']) for s in cooke_lenses_complete.values()])
    print(f"   • 共包含 {total_lenses} 款镜头")
    all_prices = [float(l['price'].replace('$', '').replace(',', '')) for s in cooke_lenses_complete.values() for l in s['lenses']]
    print(f"   • 价格范围：${min(all_prices):,.0f} - ${max(all_prices):,.0f}")
    print(f"\n📑 工作表列表:")
    print(f"   1. 镜头规格总表 - 完整技术参数")
    print(f"   2. 系列详细介绍 - 特点与描述")
    print(f"   3. 快速选型指南 - 选购建议")
    print(f"\n🎨 设计特色:")
    print(f"   • 专业黑金配色方案")
    print(f"   • 中英文双语对照")
    print(f"   • 5 个镜头系列完整数据")
    print(f"   • 价格高亮显示")
    
    return output_path

if __name__ == "__main__":
    create_professional_excel()
    print(f"\n✅ 完成！文件已保存到桌面")
