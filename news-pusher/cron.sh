#!/bin/bash
# 新闻推送定时任务脚本
# 添加到 crontab: 0 9 * * * /Users/jesson/.openclaw/workspace/news-pusher/cron.sh

cd "$(dirname "$0")"

# 激活虚拟环境（如果有）
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 运行推送脚本
python3 pusher.py >> logs/cron.log 2>&1

echo "[$(date)] 推送任务完成" >> logs/cron.log
