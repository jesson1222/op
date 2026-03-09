#!/bin/bash
# 新闻推送定时任务脚本
# 添加到 crontab: 0 9,18 * * * /Users/jesson/.openclaw/workspace/news-pusher/cron.sh

cd "$(dirname "$0")"

# 激活虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 完全禁用代理（系统代理 127.0.0.1:9674 未运行）
unset HTTP_PROXY
unset http_proxy
unset HTTPS_PROXY
unset https_proxy
export NO_PROXY="*"

# 运行飞书企业应用推送脚本
python3 pusher_feishu_app.py >> logs/pusher.log 2>&1

echo "[$(date)] 推送任务完成" >> logs/pusher.log
