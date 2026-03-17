#!/bin/bash
# 每日光储新闻更新 + 头条生成 + 图文生成
cd /root/guangchu/scripts

# 1. Fetch news
python3 fetch-news-v4.py

# 2. Generate headline
python3 generate-headline.py

# 3. Generate toutiao article
python3 generate-toutiao.py

echo [Tue Mar 17 03:19:39 UTC 2026] Daily news + toutiao article generated >> /root/guangchu/logs/cron.log
