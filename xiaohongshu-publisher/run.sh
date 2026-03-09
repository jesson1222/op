#!/bin/bash
# 小红书发布工具 - 一键启动脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📕 小红书全自动发布工具"
echo "========================"
echo ""

# 检查图片目录
if [ ! -d "images" ] || [ -z "$(ls -A images 2>/dev/null)" ]; then
    echo "⚠️  images/ 目录为空！"
    echo ""
    echo "请先将要发布的图片放入 images/ 目录："
    echo "  cp /path/to/photos/*.jpg images/"
    echo ""
    echo "要求："
    echo "  - 格式：JPG 或 PNG"
    echo "  - 数量：6-9 张"
    echo "  - 尺寸：建议 3:4 或 4:5 竖屏"
    echo ""
    exit 1
fi

# 显示图片数量
IMAGE_COUNT=$(ls -1 images/*.jpg images/*.png 2>/dev/null | wc -l)
echo "✅ 找到 $IMAGE_COUNT 张图片"

# 检查 Cookie 状态
if [ -f "data/xiaohongshu_cookies.json" ]; then
    echo "✅ 检测到已保存的登录态"
    echo ""
    echo "🚀 开始自动发布..."
    echo ""
    docker-compose up
else
    echo "⚠️  未检测到登录态"
    echo ""
    echo "🔐 首次运行需要登录："
    echo "  1. 浏览器窗口会自动打开"
    echo "  2. 用手机小红书 APP 扫码登录"
    echo "  3. 登录成功后会自动保存"
    echo ""
    read -p "按回车继续..."
    echo ""
    echo "🔧 构建并启动..."
    docker-compose up --build
fi

echo ""
echo "✅ 完成！"
