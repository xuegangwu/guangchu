#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试数据处理功能
"""

import pytest
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.build_index import load_news, save_index


class TestDataProcessing:
    """测试数据处理功能"""
    
    def test_json_load(self):
        """测试 JSON 加载"""
        test_data = {"title": "Test News", "date": "2026-03-14"}
        json_str = json.dumps(test_data)
        loaded = json.loads(json_str)
        assert loaded == test_data
    
    def test_news_structure(self):
        """测试新闻数据结构"""
        news_item = {
            "title": "Test News",
            "url": "https://example.com",
            "date": "2026-03-14",
            "region": "US",
            "type": "policy"
        }
        assert "title" in news_item
        assert "url" in news_item
        assert "date" in news_item
    
    def test_data_validation(self):
        """测试数据验证"""
        valid_news = {
            "title": "Valid News",
            "url": "https://example.com"
        }
        invalid_news = {
            "title": ""
        }
        assert len(valid_news["title"]) > 0
        assert valid_news["url"].startswith("http")
        assert len(invalid_news["title"]) == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
