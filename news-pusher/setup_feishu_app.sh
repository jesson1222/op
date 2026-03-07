#!/bin/bash
# 飞书企业应用快速配置脚本

echo "======================================"
echo "📘 飞书企业应用配置向导"
echo "======================================"
echo ""

CONFIG_FILE="config_feishu_app.yaml"

# 检查配置文件是否存在
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ 配置文件不存在：$CONFIG_FILE"
    exit 1
fi

echo "请从飞书开放平台获取以下信息："
echo ""
echo "1. 访问：https://open.feishu.cn/"
echo "2. 进入「企业自建应用」"
echo "3. 创建或选择应用"
echo "4. 在「凭证与基础信息」中获取 App ID 和 App Secret"
echo "5. 在「权限管理」中添加 im:message 和 im:chat 权限"
echo ""
echo "获取群组 ID 的方法："
echo "- 打开飞书群组"
echo "- 在浏览器中查看 URL"
echo "- 格式：https://applink.feishu.cn/client/chat/oc_xxxxxxxxxx"
echo "- 其中 oc_xxxxxxxxxx 就是群组 ID"
echo ""
echo "======================================"
echo ""

# 读取用户输入
read -p "请输入 App ID (格式：cli_xxxxxxxxxxxxx): " APP_ID
read -p "请输入 App Secret: " APP_SECRET
read -p "请输入群组 ID (格式：oc_xxxxxxxxxxxxx): " CHAT_ID

echo ""
echo "正在更新配置文件..."

# 备份原文件
cp "$CONFIG_FILE" "${CONFIG_FILE}.bak"

# 替换配置
sed -i '' "s/app_id: \"cli_xxxxxxxxxxxxx\"/app_id: \"$APP_ID\"/" "$CONFIG_FILE"
sed -i '' "s/app_secret: \"xxxxxxxxxxxxxxxx\"/app_secret: \"$APP_SECRET\"/" "$CONFIG_FILE"
sed -i '' "s/chat_id: \"oc_xxxxxxxxxxxxx\"/chat_id: \"$CHAT_ID\"/" "$CONFIG_FILE"

echo "✅ 配置文件已更新"
echo ""
echo "======================================"
echo "🧪 现在测试连接..."
echo "======================================"
echo ""

# 激活虚拟环境并测试
source venv/bin/activate
python3 pusher_feishu_app.py test

echo ""
echo "======================================"
echo "💡 提示："
echo "- 如果测试成功，可以运行：python3 pusher_feishu_app.py"
echo "- 配置文件已备份：${CONFIG_FILE}.bak"
echo "======================================"
