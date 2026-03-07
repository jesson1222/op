#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARRI 产品目录 - Excel 生成器
从 arri.com 收集的产品信息生成详细的 Excel 文件
"""

import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill, Color
from openpyxl.utils import get_column_letter
from datetime import datetime

# 创建 workbook
wb = openpyxl.Workbook()
wb.remove(wb.active)  # 移除默认 sheet

# 定义样式
header_font = Font(bold=True, size=12, color="FFFFFF")
header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
title_font = Font(bold=True, size=14, color="1F4E79")
cell_alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
border = Border(
    left=Side(style="thin"),
    right=Side(style="thin"),
    top=Side(style="thin"),
    bottom=Side(style="thin")
)

# ============================================
# Sheet 1: 摄影机系统 (Camera Systems)
# ============================================
ws_camera = wb.create_sheet("摄影机系统")
camera_data = [
    ["产品系列", "产品名称", "描述", "主要特性", "应用场景"],
    ["Cine Cameras", "ALEXA 35 Xtreme", "Motion meets emotion", "更高帧率、下一代编解码器降低数据率、更长的预录制时间、更低功耗、改进的 WiFi 功能", "电影制作、高端广告"],
    ["Cine Cameras", "ALEXA Mini LF", "Large format, small camera", "大画幅传感器、紧凑机身、高画质", "纪录片、电视剧、独立电影"],
    ["Cine Cameras", "ALEXA LF", "大画幅摄影机", "大画幅成像、高动态范围", "电影制作"],
    ["Cine Cameras", "AMIRA", "Go anywhere, shoot anything", "多功能纪录片摄影机、内置 ND 滤镜、优秀的人机工程学", "纪录片、新闻、电视剧"],
    ["Live Cameras", "ALEXA 35 Live", "多机位直播系统", "专为直播设计、集成控制接口", "体育赛事、演唱会、电视直播"],
    ["Live Cameras", "AMIRA Live", "直播摄影机", "广播级输出、低延迟", "现场活动直播"],
    ["Legacy", "ALEXA Mini", "经典紧凑摄影机", "轻便、可靠、广泛使用", "多种制作场景"],
    ["Legacy", "ALEXA SXT W", "经典摄影机", "成熟的技术平台", "电影制作"],
]

for row_idx, row_data in enumerate(camera_data, 1):
    row = ws_camera.append(row_data)
    # 设置样式
    for cell in ws_camera[row_idx]:
        cell.alignment = cell_alignment
        cell.border = border
        if row_idx == 1:
            cell.font = header_font
            cell.fill = header_fill

# ============================================
# Sheet 2: 镜头系统 (Lens Systems)
# ============================================
ws_lens = wb.create_sheet("镜头系统")
lens_data = [
    ["产品系列", "产品名称", "描述", "主要特性", "焦距范围"],
    ["Signature Lenses", "Signature Primes", "Modern lenses. Timeless look.", "现代设计、经典成像、紧凑轻便", "12mm, 15mm, 18mm, 21mm, 25mm, 28mm, 32mm, 35mm, 40mm, 45mm, 50mm, 58mm, 65mm, 75mm, 85mm, 100mm, 125mm, 135mm, 150mm, 180mm, 210mm"],
    ["Signature Lenses", "Signature Zooms", "变焦镜头系列", "恒定光圈、高质量成像", "16-28mm, 28-76mm, 45-135mm, 65-300mm"],
    ["Ensō Prime Lenses", "Ensō Primes", "Creative Flow", "创意流畅、独特成像风格", "多种焦距可选"],
    ["Ensō Prime Lenses", "Ensō Vintage Elements", "复古元素", "经典镜头风格", "特殊效果"],
    ["Ultra Wide Zooms", "Ultra Wide Zoom", "超广角变焦", "9.5-18mm T2.9", "9.5-18mm"],
    ["Ultra Wide Zooms", "Anamorphic Ultra Wide Zoom", "变形超广角变焦", "变形宽银幕效果", "超广角变形"],
    ["ARRI/Zeiss/Fujinon", "Master Primes", "高速定焦镜头", "T1.3 大光圈、高分辨率", "12mm-150mm 多种焦距"],
    ["Accessories", "Lens Accessories", "镜头配件", "遮光斗、跟焦器等", "N/A"],
]

for row_idx, row_data in enumerate(lens_data, 1):
    ws_lens.append(row_data)
    for cell in ws_lens[row_idx]:
        cell.alignment = cell_alignment
        cell.border = border
        if row_idx == 1:
            cell.font = header_font
            cell.fill = header_fill

# ============================================
# Sheet 3: 灯光系统 (Lighting Systems)
# ============================================
ws_lighting = wb.create_sheet("灯光系统")
lighting_data = [
    ["产品系列", "产品名称", "描述", "主要特性", "功率/类型"],
    ["LED Panel Lights", "SkyPanel X", "Soft | Modular | Hard", "模块化设计、软/硬光可选、高亮度", "LED 面板灯"],
    ["LED Panel Lights", "SkyPanel Pro", "专业级 LED 柔光灯", "高亮度、精确色彩控制", "LED 面板灯"],
    ["LED Panel Lights", "Orbiter", "多功能 LED 灯", "可更换光学附件、多种照明模式", "LED 多功能"],
    ["LED Spotlights", "L-Series Plus", "LED 聚光灯", "可聚焦菲涅尔、高效节能", "LED 聚光"],
    ["LED Ecosystem", "LED Ecosystem", "LED 生态系统", "完整的 LED 照明解决方案", "多种类型"],
    ["Daylight", "M-Series", "日光型灯具", "专利 MAX 反射器、高输出", "HMI 日光"],
    ["Daylight", "APOLLO", "日光型灯具", "高效日光光源", "HMI 日光"],
    ["Tungsten", "Tungsten", "钨丝灯系列", "传统钨丝光源、温暖色温", "钨丝灯"],
    ["Ballasts", "Electronic Ballasts", "电子镇流器", "稳定电源、调光控制", "电源设备"],
    ["Accessories", "Professional Lighting Accessories", "专业灯光配件", "灯架、滤色片、控光附件等", "配件"],
]

for row_idx, row_data in enumerate(lighting_data, 1):
    ws_lighting.append(row_data)
    for cell in ws_lighting[row_idx]:
        cell.alignment = cell_alignment
        cell.border = border
        if row_idx == 1:
            cell.font = header_font
            cell.fill = header_fill

# ============================================
# Sheet 4: 稳定系统 (Stabilizer Systems)
# ============================================
ws_stabilizer = wb.create_sheet("稳定系统")
stabilizer_data = [
    ["产品系列", "产品名称", "描述", "主要特性", "应用场景"],
    ["Hybrid Stabilizers", "TRINITY 2", "混合稳定器（机械 + 电子）", "获得奥斯卡科学技术奖、三轴稳定、可扩展 Pan Axis Module", "电影、广告、高端制作"],
    ["Mechanical Stabilizers", "ARTEMIS 2", "纯机械稳定器", "经典设计、可升级为 TRINITY 2", "电影、电视剧"],
    ["Live Production", "ARTEMIS 2 Live", "直播专用稳定器", "集成 Tally 系统、OB 车通信", "现场直播"],
    ["Live Production", "TRINITY Live", "直播混合稳定器", "轻量化、稳定通信", "广播制作"],
    ["Remote Heads", "360 EVO", "稳定遥控头", "360 度旋转、远程控制", "特殊拍摄、车载拍摄"],
    ["Modules", "TRINITY 2 Pan Axis Module", "Pan 轴模块", "将 TRINITY 2 转换为三轴遥控头", "扩展功能"],
    ["Accessories", "Stabilizer Accessories", "稳定器配件", "适配器、配重、支架等", "配件"],
]

for row_idx, row_data in enumerate(stabilizer_data, 1):
    ws_stabilizer.append(row_data)
    for cell in ws_stabilizer[row_idx]:
        cell.alignment = cell_alignment
        cell.border = border
        if row_idx == 1:
            cell.font = header_font
            cell.fill = header_fill

# ============================================
# Sheet 5: 辅助系统 (Electronic Control System)
# ============================================
ws_ecs = wb.create_sheet("辅助系统")
ecs_data = [
    ["产品系列", "产品名称", "描述", "主要特性", "用途"],
    ["Hand Units", "Hi-5 SX", "单轴手持控制单元", "可扩展、单轴跟焦", "镜头控制"],
    ["Hand Units", "Hi-5 Hand Unit", "多功能手持控制单元", "Further. Stronger. Faster.", "综合镜头控制"],
    ["Interface Adapters", "RIA-1 Radio Interface Adapter", "无线电接口适配器", "通用连接、支持第三方相机", "无线控制扩展"],
    ["Interface Adapters", "NIA-1 Network Interface Adapter", "网络接口适配器", "网络化控制选项", "网络控制"],
    ["Control Units", "ZMU-4", "变焦控制单元", "灵活连接和控制", "变焦控制"],
    ["Control Units", "Operator Control Unit OCU-1", "操作员控制单元", "Hi-5 和 WCU-4 覆盖解决方案", "备用控制"],
    ["Grips", "Master Grips", "主控手柄", "人体工程学设计", "手持控制"],
    ["Radio Modules", "ERM-2400 LCS", "外部无线电模块", "外部无线模块", "无线扩展"],
    ["Lens Motors", "Lens Motors and Encoders", "镜头马达和编码器", "紧凑智能设计", "自动跟焦"],
    ["Sensors", "UDM-1", "超声波测距单元", "精确距离测量", "跟焦辅助"],
    ["Accessories", "LCUBEs", "配件", "多功能配件", "系统扩展"],
    ["Motor Controllers", "Motor Controllers", "马达控制器", "UMC-4 等", "马达控制"],
    ["Third-party", "cmotion Products", "cmotion 产品", "Steady Zoom, cPro 等", "专业控制"],
    ["Legacy", "Discontinued ECS", "停产产品", "WCU-4 等经典产品", "历史产品"],
]

for row_idx, row_data in enumerate(ecs_data, 1):
    ws_ecs.append(row_data)
    for cell in ws_ecs[row_idx]:
        cell.alignment = cell_alignment
        cell.border = border
        if row_idx == 1:
            cell.font = header_font
            cell.fill = header_fill

# ============================================
# Sheet 6: 工具软件系统 (Software & Tools)
# ============================================
ws_tools = wb.create_sheet("工具软件系统")
tools_data = [
    ["软件类别", "软件名称", "描述", "主要功能", "使用阶段"],
    ["Camera Control", "Camera Companion App", "Configurable camera control in your pocket", "可配置的相机控制、移动设备控制", "拍摄现场"],
    ["Post Production", "ARRI Film Lab", "The soul of analog film", "OpenFX 插件、模拟胶片质感", "后期制作"],
    ["Post Production", "ARRI Reference Tool (ART)", "The tool for ARRIRAW processing", "ARRIRAW 处理工具", "后期制作"],
    ["Look Development", "ARRI Look Builder", "Mix features to create your individual look", "创建个性化 LUT 和外观", "前期/后期"],
    ["Pre Production", "Frame Line & Lens Illumination Tool", "Line by line for every format, sensor mode, and lens illumination", "画幅线和镜头照明计算", "前期准备"],
    ["Pre Production", "Formats & Data Rate Calculator", "Calculate the storage space for your production", "存储容量和数据率计算", "前期准备"],
    ["Post Production", "ARRIRAW HDE Transcoder", "CODEX High Density Encoding for ARRIRAW", "高密度编码转码", "后期制作"],
    ["Virtual Production", "ARRI Live Link Metadata", "The Plug-In for Unreal Engine", "Unreal Engine 元数据插件", "虚拟制作"],
    ["Look Development", "LUT Generator", "Create LUT's for on-set or post production", "创建 LUT", "现场/后期"],
    ["Pre Production", "Matte Box Checker", "Find out which matte box you can use with which ARRI lens", "遮光斗兼容性检查", "前期准备"],
    ["Look Development", "ARRI Look Library App", "The Look Library in your pocket", "外观库移动应用", "前期/现场"],
    ["Legacy", "Legacy Software", "ARRIRAW Converter, ARRI Color Tool, ARRI Meta Extract", "传统软件工具", "后期制作"],
]

for row_idx, row_data in enumerate(tools_data, 1):
    ws_tools.append(row_data)
    for cell in ws_tools[row_idx]:
        cell.alignment = cell_alignment
        cell.border = border
        if row_idx == 1:
            cell.font = header_font
            cell.fill = header_fill

# ============================================
# Sheet 7: 产品总览 (Overview)
# ============================================
ws_overview = wb.create_sheet("产品总览")
overview_data = [
    ["系统分类", "产品数量", "主要产品线", "官网链接"],
    ["摄影机系统", "7+", "ALEXA 35 Xtreme, ALEXA Mini LF, AMIRA, ALEXA 35 Live", "https://www.arri.com/en/camera-systems"],
    ["镜头系统", "8+", "Signature Primes, Signature Zooms, Ensō Primes, Master Primes", "https://www.arri.com/en/cine-lenses"],
    ["灯光系统", "10+", "SkyPanel X, SkyPanel Pro, Orbiter, L-Series Plus, M-Series", "https://www.arri.com/en/lighting"],
    ["稳定系统", "7+", "TRINITY 2, ARTEMIS 2, TRINITY Live, 360 EVO", "https://www.arri.com/en/camera-systems/camera-stabilizer-systems"],
    ["辅助系统", "14+", "Hi-5, RIA-1, NIA-1, ZMU-4, cmotion", "https://www.arri.com/en/camera-systems/electronic-control-system"],
    ["工具软件系统", "12+", "Camera Companion App, ARRI Film Lab, Look Builder, ART", "https://www.arri.com/en/learn-help/learn-help-camera-system/tools"],
]

for row_idx, row_data in enumerate(overview_data, 1):
    ws_overview.append(row_data)
    for cell in ws_overview[row_idx]:
        cell.alignment = cell_alignment
        cell.border = border
        if row_idx == 1:
            cell.font = header_font
            cell.fill = header_fill

# 调整列宽
for ws in wb.worksheets:
    for column in ws.columns:
        max_length = 0
        column_letter = get_column_letter(column[0].column)
        for cell in column:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column_letter].width = adjusted_width

# 设置行高
for ws in wb.worksheets:
    for row in ws.iter_rows(min_row=2):
        ws.row_dimensions[row[0].row].height = 40

# 保存文件
filename = f"ARRI_产品目录_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
wb.save(filename)
print(f"✓ Excel 文件已生成：{filename}")
print(f"✓ 包含 {len(wb.worksheets)} 个工作表:")
for ws in wb.worksheets:
    print(f"  - {ws.title}")
