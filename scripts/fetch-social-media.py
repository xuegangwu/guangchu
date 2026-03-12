#!/usr/bin/env python3
"""
Guangchu - 社交媒体信息源抓取
支持 LinkedIn、Facebook、Twitter/X
"""

import json
import re
from datetime import datetime
from pathlib import Path
import requests
from typing import List, Dict, Optional

# 配置
RAW_DIR = Path("/home/admin/openclaw/workspace/projects/guangchu/raw")
CONFIG_FILE = Path("/home/admin/openclaw/workspace/projects/guangchu/config/social-media.json")

print("✅ 社交媒体抓取脚本已加载")
print(f"📂 数据目录：{RAW_DIR}")
print(f"📄 配置文件：{CONFIG_FILE}")

if __name__ == "__main__":
    print("\n运行：python3 fetch-social-media.py")
    print("请配置 config/social-media.json 后运行")
