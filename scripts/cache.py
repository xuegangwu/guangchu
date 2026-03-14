#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
光储龙虾 - 缓存管理模块
支持内存缓存和 Redis 缓存

v2.2 Phase 2 新增:
- 内存缓存
- Redis 缓存（可选）
- 缓存过期管理
- 缓存统计
"""

import time
import json
import hashlib
from typing import Any, Optional, Dict
from datetime import datetime, timedelta
from pathlib import Path
import sys

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.logger import logger, info, debug, error, warning
from scripts.config import get_config


class CacheEntry:
    """缓存条目"""
    
    def __init__(self, value: Any, ttl: int = 300):
        """
        初始化缓存条目
        
        Args:
            value: 缓存值
            ttl: 生存时间（秒），默认 5 分钟
        """
        self.value = value
        self.created_at = time.time()
        self.ttl = ttl
    
    def is_expired(self) -> bool:
        """检查是否过期"""
        return time.time() > (self.created_at + self.ttl)
    
    def remaining_ttl(self) -> float:
        """获取剩余生存时间"""
        remaining = (self.created_at + self.ttl) - time.time()
        return max(0, remaining)


class MemoryCache:
    """内存缓存类"""
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 300):
        """
        初始化内存缓存
        
        Args:
            max_size: 最大缓存条目数
            default_ttl: 默认生存时间（秒）
        """
        self.cache: Dict[str, CacheEntry] = {}
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.hits = 0
        self.misses = 0
        self.sets = 0
    
    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存
        
        Args:
            key: 缓存键
        
        Returns:
            缓存值，如果不存在或已过期则返回 None
        """
        if key not in self.cache:
            self.misses += 1
            debug(f"缓存未命中：{key}")
            return None
        
        entry = self.cache[key]
        
        # 检查是否过期
        if entry.is_expired():
            del self.cache[key]
            self.misses += 1
            debug(f"缓存已过期：{key}")
            return None
        
        self.hits += 1
        debug(f"缓存命中：{key} (剩余 TTL: {entry.remaining_ttl():.1f}s)")
        return entry.value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """
        设置缓存
        
        Args:
            key: 缓存键
            value: 缓存值
            ttl: 生存时间（秒），None 则使用默认值
        """
        # 如果缓存已满，删除最旧的条目
        if len(self.cache) >= self.max_size:
            self._evict_oldest()
        
        actual_ttl = ttl if ttl is not None else self.default_ttl
        self.cache[key] = CacheEntry(value, actual_ttl)
        self.sets += 1
        debug(f"缓存已设置：{key} (TTL: {actual_ttl}s)")
    
    def delete(self, key: str) -> bool:
        """
        删除缓存
        
        Args:
            key: 缓存键
        
        Returns:
            是否删除成功
        """
        if key in self.cache:
            del self.cache[key]
            debug(f"缓存已删除：{key}")
            return True
        return False
    
    def clear(self):
        """清空缓存"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        self.sets = 0
        info("缓存已清空")
    
    def _evict_oldest(self):
        """删除最旧的缓存条目"""
        if not self.cache:
            return
        
        # 找到最旧的条目
        oldest_key = min(
            self.cache.keys(),
            key=lambda k: self.cache[k].created_at
        )
        
        del self.cache[oldest_key]
        debug(f"已淘汰最旧缓存：{oldest_key}")
    
    def cleanup_expired(self) -> int:
        """
        清理所有过期缓存
        
        Returns:
            清理的条目数
        """
        expired_keys = [
            key for key, entry in self.cache.items()
            if entry.is_expired()
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            debug(f"清理了 {len(expired_keys)} 个过期缓存")
        
        return len(expired_keys)
    
    def get_stats(self) -> Dict:
        """
        获取缓存统计信息
        
        Returns:
            统计信息字典
        """
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            'total_entries': len(self.cache),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'sets': self.sets,
            'hit_rate': f"{hit_rate:.2f}%",
            'memory_usage': f"{len(self.cache) / self.max_size * 100:.1f}%"
        }
    
    def generate_key(self, prefix: str, *args, **kwargs) -> str:
        """
        生成缓存键
        
        Args:
            prefix: 键前缀
            *args: 位置参数
            **kwargs: 关键字参数
        
        Returns:
            生成的缓存键
        """
        key_data = {
            'prefix': prefix,
            'args': args,
            'kwargs': kwargs
        }
        
        key_str = json.dumps(key_data, sort_keys=True)
        key_hash = hashlib.md5(key_str.encode()).hexdigest()
        
        return f"{prefix}:{key_hash}"


class CacheManager:
    """缓存管理器"""
    
    def __init__(self, use_redis: bool = False, redis_url: Optional[str] = None):
        """
        初始化缓存管理器
        
        Args:
            use_redis: 是否使用 Redis（目前仅支持内存缓存）
            redis_url: Redis URL（暂未实现）
        """
        self.memory_cache = MemoryCache()
        self.use_redis = use_redis
        self.redis_client = None
        
        if use_redis and redis_url:
            warning("Redis 缓存暂未实现，使用内存缓存")
        
        info("缓存管理器已初始化")
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        return self.memory_cache.get(key)
    
    def set(self, key: str, value: Any, ttl: int = 300):
        """设置缓存"""
        self.memory_cache.set(key, value, ttl)
    
    def delete(self, key: str) -> bool:
        """删除缓存"""
        return self.memory_cache.delete(key)
    
    def clear(self):
        """清空缓存"""
        self.memory_cache.clear()
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self.memory_cache.get_stats()
    
    def cleanup(self) -> int:
        """清理过期缓存"""
        return self.memory_cache.cleanup_expired()


# 全局缓存实例
cache_manager = CacheManager()


def get_cache() -> CacheManager:
    """获取缓存管理器实例"""
    return cache_manager


def cached(ttl: int = 300, prefix: str = "func"):
    """
    函数缓存装饰器
    
    Args:
        ttl: 缓存时间（秒）
        prefix: 缓存键前缀
    
    Usage:
        @cached(ttl=600, prefix="search")
        def search(query):
            return results
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            cache = get_cache()
            
            # 生成缓存键
            cache_key = cache.memory_cache.generate_key(prefix, *args, **kwargs)
            
            # 尝试从缓存获取
            result = cache.get(cache_key)
            if result is not None:
                debug(f"缓存命中：{func.__name__}")
                return result
            
            # 执行函数
            result = func(*args, **kwargs)
            
            # 保存到缓存
            cache.set(cache_key, result, ttl)
            
            return result
        
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper
    
    return decorator


def main():
    """测试缓存功能"""
    info("=" * 60)
    info("Guangchu - 缓存功能测试")
    info("=" * 60)
    
    cache = get_cache()
    
    # 测试 1: 基本缓存操作
    info("\n测试 1: 基本缓存操作")
    cache.set("test_key", "test_value", ttl=60)
    value = cache.get("test_key")
    info(f"设置缓存：test_key = {value}")
    
    # 测试 2: 缓存过期
    info("\n测试 2: 缓存过期")
    cache.set("short_lived", "value", ttl=2)
    info(f"设置 2 秒过期缓存")
    time.sleep(3)
    value = cache.get("short_lived")
    info(f"3 秒后获取：{value} (应该为 None)")
    
    # 测试 3: 缓存统计
    info("\n测试 3: 缓存统计")
    for i in range(10):
        cache.set(f"key_{i}", f"value_{i}")
        cache.get(f"key_{i}")
    
    stats = cache.get_stats()
    info(f"缓存统计:")
    for key, value in stats.items():
        info(f"  {key}: {value}")
    
    # 测试 4: 缓存装饰器
    info("\n测试 4: 缓存装饰器")
    
    @cached(ttl=60, prefix="test")
    def expensive_function(x, y):
        time.sleep(0.1)  # 模拟耗时操作
        return x + y
    
    # 第一次调用（未缓存）
    start = time.time()
    result1 = expensive_function(10, 20)
    time1 = time.time() - start
    
    # 第二次调用（缓存命中）
    start = time.time()
    result2 = expensive_function(10, 20)
    time2 = time.time() - start
    
    info(f"第一次调用：{time1*1000:.2f}ms")
    info(f"第二次调用：{time2*1000:.2f}ms (缓存命中)")
    info(f"加速比：{time1/time2:.1f}x")
    
    # 测试 5: 清理过期缓存
    info("\n测试 5: 清理过期缓存")
    cleaned = cache.cleanup()
    info(f"清理了 {cleaned} 个过期缓存")
    
    info("\n" + "=" * 60)
    info("测试完成！")
    info("=" * 60)


if __name__ == '__main__':
    main()
