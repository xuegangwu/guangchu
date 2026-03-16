#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
光储龙虾 - 配置管理模块
统一的配置管理中心

v2.1 改进:
- 集中管理所有配置
- 支持环境变量覆盖
- 添加配置验证
"""

import os
from dataclasses import dataclass, field
from typing import Dict, List
from pathlib import Path


@dataclass
class Config:
    """配置类"""

    # 项目根目录
    WORKDIR: str = field(init=False)

    # 数据目录
    RAW_DIR: str = field(init=False)
    PROCESSED_DIR: str = field(init=False)
    LOGS_DIR: str = field(init=False)
    STATS_DIR: str = field(init=False)

    # 数据库配置
    DATABASE_URL: str = field(init=False)

    # 网络配置
    REQUEST_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 2

    # 信息源配置
    SOURCES: Dict[str, Dict] = field(default_factory=dict)

    # 区域配置
    REGIONS: Dict[str, List[str]] = field(default_factory=dict)

    def __post_init__(self):
        """初始化后处理"""
        # 设置项目根目录
        self.WORKDIR = str(Path(__file__).parent.parent)
        
        # 设置数据目录
        self.RAW_DIR = os.path.join(self.WORKDIR, 'raw')
        self.PROCESSED_DIR = os.path.join(self.WORKDIR, 'processed')
        self.LOGS_DIR = os.path.join(self.WORKDIR, 'logs')
        self.STATS_DIR = os.path.join(self.WORKDIR, 'stats')
        
        # 数据库配置
        self.DATABASE_URL = os.path.join(self.WORKDIR, 'search.db')
        
        # 创建必要的目录
        for directory in [self.RAW_DIR, self.PROCESSED_DIR, self.LOGS_DIR, self.STATS_DIR]:
            Path(directory).mkdir(parents=True, exist_ok=True)

        # 从环境变量加载配置（如果存在）
        self.load_from_env()

    def load_from_env(self):
        """从环境变量加载配置"""
        if os.getenv('GUANGCHU_TIMEOUT'):
            self.REQUEST_TIMEOUT = int(os.getenv('GUANGCHU_TIMEOUT'))
        if os.getenv('GUANGCHU_MAX_RETRIES'):
            self.MAX_RETRIES = int(os.getenv('GUANGCHU_MAX_RETRIES'))

    def validate(self) -> bool:
        """验证配置有效性"""
        # 检查必要目录
        if not Path(self.WORKDIR).exists():
            raise ValueError(f"工作目录不存在：{self.WORKDIR}")

        # 检查配置值
        if self.REQUEST_TIMEOUT < 1:
            raise ValueError("请求超时时间必须大于 0")
        if self.MAX_RETRIES < 0:
            raise ValueError("重试次数不能为负数")

        return True

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'WORKDIR': self.WORKDIR,
            'RAW_DIR': self.RAW_DIR,
            'PROCESSED_DIR': self.PROCESSED_DIR,
            'DATABASE_URL': self.DATABASE_URL,
            'REQUEST_TIMEOUT': self.REQUEST_TIMEOUT,
            'MAX_RETRIES': self.MAX_RETRIES,
        }


# 全局配置实例
config = Config()


def get_config() -> Config:
    """获取配置实例"""
    return config


if __name__ == '__main__':
    # 测试配置
    cfg = get_config()
    print("✅ 配置加载成功")
    print(f"工作目录：{cfg.WORKDIR}")
    print(f"数据目录：{cfg.RAW_DIR}")
    print(f"日志目录：{cfg.LOGS_DIR}")
    print(f"请求超时：{cfg.REQUEST_TIMEOUT}秒")
    print(f"最大重试：{cfg.MAX_RETRIES}次")
