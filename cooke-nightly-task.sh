#!/bin/bash
# Cooke 镜头数据库夜间完善任务
# 每天晚上 11 点运行

echo "🎬 Cooke 镜头数据库完善任务启动"
echo "时间：$(date)"
echo ""

# 运行 Python 脚本生成完整版 Excel
python3 /Users/jesson/.openclaw/workspace/cooke_complete_database.py

# 备份到工作区
cp /Users/jesson/Desktop/Cooke_Optics_完整镜头数据库_*.xlsx /Users/jesson/.openclaw/workspace/ 2>/dev/null

echo ""
echo "✅ 任务完成"
echo "📊 文件已保存到桌面和工作区"
