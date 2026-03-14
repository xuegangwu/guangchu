#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
光储龙虾 - 日志系统配置
统一的日志管理模块
"""

import logging
import os
from datetime import datetime

# 日志目录
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

# 日志文件格式
log_file = os.path.join(LOG_DIR, f'guangchu_{datetime.now().strftime("%Y%m%d")}.log')

# 创建 logger
logger = logging.getLogger('Guangchu')
logger.setLevel(logging.DEBUG)

# 防止重复添加 handler
if not logger.handlers:
    # 文件 handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # 控制台 handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 格式化器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 添加 handler
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


# 快捷函数
def info(msg):
    logger.info(msg)


def debug(msg):
    logger.debug(msg)


def warning(msg):
    logger.warning(msg)


def error(msg):
    logger.error(msg)


def critical(msg):
    logger.critical(msg)


if __name__ == '__main__':
    # 测试日志系统
    info("信息级别日志")
    debug("调试级别日志")
    warning("警告级别日志")
    error("错误级别日志")
    print(f"✅ 日志系统初始化完成，日志文件：{log_file}")
