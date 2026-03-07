#!/usr/bin/env python3
"""
PDF 美化工具 - 使用 Python 创建专业 PDF
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# 文件路径
input_pdf = "/Users/jesson/Desktop/龚璐简介 - 美化版.pdf"
output_pdf = "/Users/jesson/Desktop/龚璐简介 - 专业美化版.pdf"

def create_beautified_pdf():
    """创建美化的 PDF"""
    
    # 创建文档
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # 容器
    elements = []
    
    # 样式定义
    styles = getSampleStyleSheet()
    
    # 标题样式 - 深蓝色
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # 副标题样式
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#3b82f6'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    # 正文样式
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=12,
        fontName='Helvetica',
        leading=18
    )
    
    # 添加内容
    elements.append(Paragraph("个人简介", title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # 示例内容（需要根据实际内容调整）
    elements.append(Paragraph("基本信息", subtitle_style))
    elements.append(Paragraph("姓名：龚璐", normal_style))
    elements.append(Paragraph("职位：[您的职位]", normal_style))
    elements.append(Paragraph("联系方式：[您的联系方式]", normal_style))
    elements.append(Spacer(1, 0.3*inch))
    
    elements.append(Paragraph("工作经历", subtitle_style))
    elements.append(Paragraph("• [公司名称] - [职位] ([时间范围])", normal_style))
    elements.append(Paragraph("  主要成就和职责描述", normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("教育背景", subtitle_style))
    elements.append(Paragraph("• [学校名称] - [学位] ([时间范围])", normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("专业技能", subtitle_style))
    elements.append(Paragraph("• 技能 1", normal_style))
    elements.append(Paragraph("• 技能 2", normal_style))
    elements.append(Paragraph("• 技能 3", normal_style))
    
    # 构建 PDF
    doc.build(elements)
    print(f"✓ PDF 已创建：{output_pdf}")

if __name__ == "__main__":
    try:
        create_beautified_pdf()
    except Exception as e:
        print(f"✗ 错误：{e}")
