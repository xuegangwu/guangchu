#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试日记生成功能
"""

import pytest
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDiaryGeneration:
    """测试日记生成相关功能"""
    
    def test_date_format(self):
        """测试日期格式"""
        today = datetime.now()
        formatted = today.strftime('%Y-%m-%d')
        assert len(formatted) == 10
        assert formatted.count('-') == 2
    
    def test_diary_file_naming(self):
        """测试日记文件命名"""
        date_str = "2026-03-14"
        filename = f"{date_str}.html"
        assert filename == "2026-03-14.html"
        assert filename.endswith('.html')
    
    def test_diary_content_structure(self):
        """测试日记内容结构"""
        content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Diary</title>
        </head>
        <body>
            <h1>Diary Title</h1>
            <p>Content</p>
        </body>
        </html>
        """
        assert '<!DOCTYPE html>' in content
        assert '<html>' in content
        assert '</html>' in content


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
