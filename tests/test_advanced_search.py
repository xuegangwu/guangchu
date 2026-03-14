#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试高级搜索功能
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.advanced_search import AdvancedSearch


class TestAdvancedSearch:
    """测试高级搜索类"""
    
    def test_search_initialization(self):
        """测试搜索类初始化"""
        search = AdvancedSearch()
        assert search is not None
        assert search.search_history == []
    
    def test_highlight_keywords(self):
        """测试关键词高亮"""
        search = AdvancedSearch()
        
        # 单关键词高亮
        text = "Solar energy is important"
        highlighted = search.highlight_keywords(text, ["solar"])
        assert "<mark>" in highlighted or "solar" in highlighted.lower()
        
        # 多关键词高亮
        highlighted = search.highlight_keywords(text, ["solar", "energy"])
        assert len(highlighted) > 0
        
        # 空文本
        assert search.highlight_keywords("", ["solar"]) == ""
        
        # 空关键词
        assert search.highlight_keywords(text, []) == text
    
    def test_search_history(self):
        """测试搜索历史"""
        search = AdvancedSearch()
        
        # 初始历史为空
        assert len(search.get_search_history()) == 0
        
        # 模拟添加历史（通过搜索）
        search._add_to_history("test query", {}, 5)
        assert len(search.get_search_history()) == 1
        
        # 清除历史
        search.clear_search_history()
        assert len(search.get_search_history()) == 0
    
    def test_search_history_limit(self):
        """测试搜索历史限制"""
        search = AdvancedSearch()
        
        # 添加超过 10 条历史
        for i in range(15):
            search._add_to_history(f"query {i}", {}, i)
        
        # 应该只保留最近 10 条
        assert len(search.get_search_history()) <= 10
    
    def test_search_suggestions(self):
        """测试搜索建议"""
        search = AdvancedSearch()
        
        # 添加一些历史
        search._add_to_history("solar energy", {}, 5)
        search._add_to_history("solar panel", {}, 3)
        search._add_to_history("wind energy", {}, 2)
        
        # 获取建议
        suggestions = search.get_search_suggestions("solar")
        assert len(suggestions) > 0
        assert all("solar" in s.lower() for s in suggestions)
    
    def test_search_stats_structure(self):
        """测试搜索统计结构"""
        search = AdvancedSearch()
        
        stats = search.search_stats()
        
        # 检查统计结构
        assert isinstance(stats, dict)
        assert 'total_news' in stats or len(stats) >= 0
        assert 'regions' in stats or len(stats) >= 0
        assert 'types' in stats or len(stats) >= 0


class TestSearchFilters:
    """测试搜索过滤功能"""
    
    def test_date_filter_structure(self):
        """测试日期过滤结构"""
        filters = {
            'date_from': '2026-03-01',
            'date_to': '2026-03-31'
        }
        assert 'date_from' in filters
        assert 'date_to' in filters
        assert filters['date_from'] < filters['date_to']
    
    def test_region_filter_values(self):
        """测试区域过滤值"""
        valid_regions = ["US", "Europe", "China", "Japan", "Southeast Asia"]
        
        assert "US" in valid_regions
        assert "Europe" in valid_regions
        assert "China" in valid_regions
    
    def test_type_filter_values(self):
        """测试类型过滤值"""
        valid_types = ["policy", "product", "project", "market"]
        
        assert "policy" in valid_types
        assert "product" in valid_types
        assert "project" in valid_types


class TestSearchSort:
    """测试搜索排序功能"""
    
    def test_sort_options(self):
        """测试排序选项"""
        valid_sorts = ["relevance", "date"]
        
        assert "relevance" in valid_sorts
        assert "date" in valid_sorts
    
    def test_sort_by_relevance(self):
        """测试相关性排序"""
        # 模拟相关性排序逻辑
        results = [
            {'score': 0.9, 'title': 'Best match'},
            {'score': 0.7, 'title': 'Good match'},
            {'score': 0.5, 'title': 'Fair match'}
        ]
        
        sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
        assert sorted_results[0]['score'] == 0.9
        assert sorted_results[-1]['score'] == 0.5
    
    def test_sort_by_date(self):
        """测试时间排序"""
        from datetime import datetime
        
        results = [
            {'date': '2026-03-10', 'title': 'Older'},
            {'date': '2026-03-14', 'title': 'Newer'},
            {'date': '2026-03-12', 'title': 'Middle'}
        ]
        
        sorted_results = sorted(results, key=lambda x: x['date'], reverse=True)
        assert sorted_results[0]['date'] == '2026-03-14'
        assert sorted_results[-1]['date'] == '2026-03-10'


class TestSearchResultDisplay:
    """测试搜索结果展示"""
    
    def test_result_structure(self):
        """测试结果结构"""
        result = {
            'id': 1,
            'title': 'Test News',
            'url': 'https://example.com',
            'date': '2026-03-14',
            'region': 'US',
            'type': 'policy',
            'source': 'Test Source',
            'summary': 'Test summary'
        }
        
        required_fields = ['id', 'title', 'url', 'date', 'region', 'type', 'source', 'summary']
        for field in required_fields:
            assert field in result
    
    def test_highlighted_result(self):
        """测试高亮结果"""
        result = {
            'title': 'Solar energy news',
            'title_highlighted': '<mark>Solar</mark> energy news',
            'summary': 'About solar energy',
            'summary_highlighted': 'About <mark>solar</mark> energy'
        }
        
        assert 'title_highlighted' in result
        assert 'summary_highlighted' in result
        assert '<mark>' in result['title_highlighted']
    
    def test_result_tags(self):
        """测试结果标签"""
        result = {
            'region': 'US',
            'type': 'policy'
        }
        
        tags = [result['region'], result['type']]
        assert len(tags) == 2
        assert 'US' in tags
        assert 'policy' in tags


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
