#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新闻抓取功能
"""

import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.fetch_news import classify_region, extract_keywords


class TestClassifyRegion:
    """测试区域分类功能"""
    
    def test_europe_classification(self):
        """测试欧洲区域分类"""
        assert classify_region("Germany") == "Europe"
        assert classify_region("France") == "Europe"
        assert classify_region("Spain") == "Europe"
    
    def test_us_classification(self):
        """测试美国区域分类"""
        assert classify_region("US") == "US"
        assert classify_region("California") == "US"
        assert classify_region("Texas") == "US"
    
    def test_japan_classification(self):
        """测试日本区域分类"""
        assert classify_region("Japan") == "Japan"
        assert classify_region("Tokyo") == "Japan"
    
    def test_southeast_asia_classification(self):
        """测试东南亚区域分类"""
        assert classify_region("Vietnam") == "Southeast Asia"
        assert classify_region("Thailand") == "Southeast Asia"
        assert classify_region("Singapore") == "Southeast Asia"
    
    def test_unknown_region(self):
        """测试未知区域"""
        assert classify_region("Unknown Country") == "Unknown"
        assert classify_region("") == "Unknown"
    
    def test_multiple_regions(self):
        """测试包含多个区域关键词"""
        text = "Germany and France collaboration"
        assert classify_region(text) == "Europe"


class TestExtractKeywords:
    """测试关键词提取功能"""
    
    def test_basic_keywords(self):
        """测试基础关键词提取"""
        text = "Solar panel efficiency improves with new technology"
        keywords = extract_keywords(text)
        assert len(keywords) > 0
        assert any('solar' in kw.lower() for kw in keywords)
    
    def test_empty_text(self):
        """测试空文本"""
        assert extract_keywords("") == []
    
    def test_stopwords_removal(self):
        """测试停用词移除"""
        text = "The solar panel is very efficient"
        keywords = extract_keywords(text)
        assert 'the' not in keywords
        assert 'is' not in keywords


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
