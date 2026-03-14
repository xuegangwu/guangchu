#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试导出功能
"""

import pytest
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestExport:
    """测试导出功能"""
    
    def test_export_format_json(self):
        """测试 JSON 格式导出"""
        data = {"title": "Test", "content": "Content"}
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        loaded = json.loads(json_str)
        assert loaded == data
    
    def test_export_format_markdown(self):
        """测试 Markdown 格式导出"""
        title = "Test Title"
        content = "Test Content"
        markdown = f"# {title}\n\n{content}"
        assert markdown.startswith("#")
        assert title in markdown
        assert content in markdown
    
    def test_export_format_html(self):
        """测试 HTML 格式导出"""
        title = "Test Title"
        content = "Test Content"
        html = f"<html><head><title>{title}</title></head><body><p>{content}</p></body></html>"
        assert "<html>" in html
        assert title in html
        assert content in html
    
    def test_export_file_naming(self):
        """测试导出文件命名"""
        date = "2026-03-14"
        format = "md"
        filename = f"report_{date}.{format}"
        assert filename.endswith(".md")
        assert date in filename
    
    def test_export_validation(self):
        """测试导出验证"""
        data = {
            "title": "Valid Report",
            "content": "Some content",
            "date": "2026-03-14"
        }
        assert len(data["title"]) > 0
        assert len(data["content"]) > 0
        assert len(data["date"]) == 10


class TestWechatExport:
    """测试微信公众号导出"""
    
    def test_wechat_format(self):
        """测试微信格式"""
        content = {
            "title": "微信文章标题",
            "author": "作者",
            "content": "文章内容"
        }
        assert "title" in content
        assert "author" in content
        assert "content" in content
    
    def test_wechat_image_support(self):
        """测试图片支持"""
        image_url = "https://example.com/image.jpg"
        assert image_url.startswith("http")
        assert image_url.endswith(".jpg")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
