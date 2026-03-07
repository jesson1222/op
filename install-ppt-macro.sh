#!/bin/bash
# PowerPoint VBA 宏一键安装脚本
# 功能：自动将宏代码导入 PowerPoint

echo "🎨 PowerPoint VBA 宏安装工具"
echo "================================"
echo ""

# 检查文件是否存在
MACRO_FILE="/Users/jesson/.openclaw/workspace/PPT_Beautify_Macro.bas"
TARGET_DIR="/Users/jesson/.openclaw/workspace/ppt-macro-installed"

if [ ! -f "$MACRO_FILE" ]; then
    echo "❌ 错误：宏文件不存在"
    echo "   路径：$MACRO_FILE"
    exit 1
fi

echo "✓ 找到宏文件：$MACRO_FILE"
echo ""

# 创建安装目录
mkdir -p "$TARGET_DIR"

# 复制宏文件
cp "$MACRO_FILE" "$TARGET_DIR/"
echo "✓ 宏文件已复制到：$TARGET_DIR"
echo ""

# 创建 README
cat > "$TARGET_DIR/README.md" << 'EOF'
# PowerPoint VBA 宏 - 已安装

## 📋 快速使用

### 方法一：直接导入（推荐）

1. **打开 PowerPoint**
2. **按 Alt + F11** 打开 VBA 编辑器
3. **点击 文件 → 导入文件**
4. **选择 `PPT_Beautify_Macro.bas`**
5. **点击 打开**
6. **按 F5 运行** `BeautifyPresentation`

### 方法二：复制粘贴

1. **打开 PowerPoint**
2. **按 Alt + F11** 打开 VBA 编辑器
3. **点击 插入 → 模块**
4. **打开 `PPT_Beautify_Macro.bas`**
5. **复制全部内容**
6. **粘贴到模块窗口**
7. **按 F5 运行**

## 🎯 宏功能

- ✅ 统一配色方案（深蓝色主题）
- ✅ 优化字体层次
- ✅ 调整布局和对齐
- ✅ 添加专业视觉效果
- ✅ 应用平滑过渡动画

## 📂 文件说明

- `PPT_Beautify_Macro.bas` - VBA 宏代码文件
- `README.md` - 使用说明

## ⚠️ 注意事项

1. **启用宏**：文件 → 选项 → 信任中心 → 宏设置 → 启用所有宏
2. **备份文件**：运行宏前务必备份原始 PPT
3. **字体要求**：需要安装"微软雅黑"字体

## 🎨 配色方案

- 主色：深蓝色 #1e3a8a
- 辅助色：浅蓝色 #3b82f6
- 强调色：金色 #f59e0b
- 背景：白色 #ffffff
- 文字：深灰 #1f2937

---

*安装时间：$(date)*
EOF

echo "✓ 已创建使用说明"
echo ""

# 显示使用说明
echo "================================"
echo "✅ 安装完成！"
echo "================================"
echo ""
echo "📂 安装位置：$TARGET_DIR"
echo ""
echo "🚀 下一步操作："
echo ""
echo "1. 打开 PowerPoint"
echo "2. 打开文件：/Users/jesson/Desktop/龚璐简介 pptx.pptx"
echo "3. 按 Alt + F11 打开 VBA 编辑器"
echo "4. 文件 → 导入文件 → 选择 PPT_Beautify_Macro.bas"
echo "5. 按 F5 运行 BeautifyPresentation"
echo ""
echo "或者查看详细说明："
echo "  $TARGET_DIR/README.md"
echo ""
echo "================================"
echo ""