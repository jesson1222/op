#!/bin/bash
# 飞书推送快速测试脚本
# 用法：./test_quick.sh YOUR_WEBHOOK_URL

WEBHOOK_URL=$1

if [ -z "$WEBHOOK_URL" ]; then
    echo "❌ 请提供飞书 webhook 地址"
    echo ""
    echo "用法：./test_quick.sh https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
    echo ""
    echo "获取方式："
    echo "1. 打开飞书群组 → 右上角设置"
    echo "2. 找到「自定义机器人」"
    echo "3. 复制 Webhook 地址"
    exit 1
fi

echo "📤 正在发送测试消息到飞书..."
echo "Webhook: $WEBHOOK_URL"
echo ""

# 发送测试消息
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "text",
    "content": {
      "text": "📰 新闻推送系统测试\n\n✅ 如果收到此消息，说明推送系统配置成功！\n\n---\n推送时间：'"$(date '+%Y-%m-%d %H:%M')"'",
      "飞书机器人测试"
    }
  }'

echo ""
echo ""
if [ $? -eq 0 ]; then
    echo "✅ 请求发送成功！"
    echo "请检查飞书群组是否收到消息"
else
    echo "❌ 请求发送失败"
fi
