#!/bin/bash
# iFlow API Key 半自动获取脚本
# 打开浏览器让用户登录，然后自动提取或手动复制

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   iFlow API Key 自动获取助手                           ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# 打开浏览器
echo -e "${YELLOW}🌐 打开 iFlow 设置页面...${NC}"
open 'https://iflow.cn/?open=setting'

echo ""
echo -e "${GREEN}✅ 浏览器已打开${NC}"
echo ""
echo -e "${YELLOW}📋 请按以下步骤操作：${NC}"
echo ""
echo "   1️⃣  如果未登录，请先登录（微信/手机号）"
echo "   2️⃣  找到「API Key」或「密钥管理」区域"
echo "   3️⃣  点击「生成」或「复制」按钮"
echo "   4️⃣  复制 API Key（格式：sk-xxxxxxxx...）"
echo ""
echo -e "${BLUE}────────────────────────────────────────────────────────${NC}"
echo ""
echo -e "${YELLOW}💡 有两种方式继续：${NC}"
echo ""
echo -e "   ${GREEN}方式 A（推荐）${NC} - 直接告诉我 Key，我自动更新"
echo -e '              说："更新 iFlow Key: sk-xxxxx"'
echo ""
echo -e "   ${GREEN}方式 B${NC} - 手动运行更新脚本"
echo -e "              ~/.openclaw/workspace/scripts/iflow-update-key.sh sk-xxxxx"
echo ""
echo -e "${BLUE}────────────────────────────────────────────────────────${NC}"
echo ""
echo -e "${YELLOW}⏳ 等待你操作完成...${NC}"
echo ""
echo -e "   完成后，${GREEN}直接在这个对话中粘贴 API Key${NC} 即可"
echo ""
