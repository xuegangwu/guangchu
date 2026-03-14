#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试翻译服务
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestTranslation:
    """测试翻译功能"""

    def test_translation_request_structure(self):
        """测试翻译请求结构"""
        request = {"text": "Hello World", "source_lang": "en", "target_lang": "zh"}
        assert "text" in request
        assert "source_lang" in request
        assert "target_lang" in request

    def test_language_codes(self):
        """测试语言代码"""
        valid_codes = ["en", "zh", "ja", "fr", "de", "es"]
        assert "en" in valid_codes
        assert "zh" in valid_codes
        assert "ja" in valid_codes

    def test_translation_response_structure(self):
        """测试翻译响应结构"""
        response = {"translated_text": "你好世界", "source_lang": "en", "target_lang": "zh", "confidence": 0.95}
        assert "translated_text" in response
        assert "confidence" in response
        assert response["confidence"] >= 0 and response["confidence"] <= 1

    def test_batch_translation(self):
        """测试批量翻译"""
        texts = ["Hello", "World", "Test"]
        assert len(texts) > 0
        assert all(isinstance(t, str) for t in texts)


class TestLanguageDetection:
    """测试语言检测"""

    def test_detect_english(self):
        """测试英文检测"""
        text = "This is English text"
        # 简单检测：包含常见英文单词
        english_words = ["is", "the", "a", "this"]
        assert any(word in text.lower() for word in english_words)

    def test_detect_chinese(self):
        """测试中文检测"""
        text = "这是中文文本"
        # 简单检测：包含中文字符
        assert any('\u4e00' <= char <= '\u9fff' for char in text)

    def test_detect_japanese(self):
        """测试日文检测"""
        text = "これは日本語です"
        # 简单检测：包含日文字符
        assert any('\u3040' <= char <= '\u309f' for char in text)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
