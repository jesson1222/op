#!/usr/bin/env python3
"""
提取 PPTX 内容并生成网页版
"""
import zipfile
import re
import json
from pathlib import Path

# PPTX 文件路径
pptx_path = Path("/Users/jesson/Desktop/龚璐简介 pptx.pptx")

print(f"处理文件：{pptx_path}")
print(f"文件存在：{pptx_path.exists()}")
print(f"文件大小：{pptx_path.stat().st_size / 1024 / 1024:.2f} MB\n")

slides_content = []

try:
    with zipfile.ZipFile(pptx_path, 'r') as zip_ref:
        # 获取所有幻灯片文件
        slide_files = sorted([
            f for f in zip_ref.namelist() 
            if 'ppt/slides/slide' in f and f.endswith('.xml')
        ])
        
        print(f"找到 {len(slide_files)} 张幻灯片\n")
        
        for slide_file in slide_files:
            try:
                content = zip_ref.read(slide_file).decode('utf-8')
                
                # 提取所有文本
                texts = re.findall(r'<a:t[^>]*>([^<]+)</a:t>', content)
                
                if texts:
                    slides_content.append({
                        'slide_number': len(slides_content) + 1,
                        'file': slide_file,
                        'texts': texts
                    })
                    
                    print(f"幻灯片 {len(slides_content)}:")
                    for text in texts:
                        print(f"  • {text}")
                    print()
                    
            except Exception as e:
                print(f"读取 {slide_file} 失败：{e}")
    
    # 保存提取的内容
    output_file = Path("/tmp/ppt_extracted_content.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(slides_content, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 内容已保存到：{output_file}")
    print(f"✓ 共提取 {len(slides_content)} 张幻灯片")
    
except Exception as e:
    print(f"\n✗ 错误：{e}")
    import traceback
    traceback.print_exc()