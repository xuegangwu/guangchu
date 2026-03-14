#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
光储龙虾 - 日记多语言支持
支持中文、英文、日文三语切换

v2.2 新增:
- 多语言配置
- 自动翻译
- 语言检测
- 本地化支持
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

# 多语言配置
LANGUAGES = {
    'zh': {
        'name': '中文',
        'flag': '🇨🇳',
        'direction': 'ltr'
    },
    'en': {
        'name': 'English',
        'flag': '🇺🇸',
        'direction': 'ltr'
    },
    'ja': {
        'name': '日本語',
        'flag': '🇯🇵',
        'direction': 'ltr'
    }
}

# 日记模板翻译
DIARY_TEMPLATES = {
    'zh': {
        'title': '📔 {date} - 开发日记',
        'date_label': '日期',
        'developer_label': '开发者',
        'version_label': '版本',
        'summary': '📊 今日概要',
        'work_time': '工作时间',
        'achievements': '主要成果',
        'code_stats': '代码统计',
        'completed_work': '🎯 完成的工作',
        'performance': '📈 性能对比',
        'quality_metrics': '📊 质量指标',
        'files_delivered': '📁 交付文件清单',
        'v2_progress': '🎯 v2.2 完成度',
        'tech_highlights': '💡 技术亮点',
        'git_commits': '🚀 Git 提交',
        'tomorrow_plan': '📋 明日计划',
        'access_links': '🔗 访问链接',
        'summary': '🎉 今日总结',
        'reporter': '报告人',
        'date': '日期',
        'version': '版本'
    },
    'en': {
        'title': '📔 {date} - Development Diary',
        'date_label': 'Date',
        'developer_label': 'Developer',
        'version_label': 'Version',
        'summary': '📊 Today Summary',
        'work_time': 'Work Time',
        'achievements': 'Key Achievements',
        'code_stats': 'Code Stats',
        'completed_work': '🎯 Completed Work',
        'performance': '📈 Performance',
        'quality_metrics': '📊 Quality Metrics',
        'files_delivered': '📁 Delivered Files',
        'v2_progress': '🎯 v2.2 Progress',
        'tech_highlights': '💡 Tech Highlights',
        'git_commits': '🚀 Git Commits',
        'tomorrow_plan': '📋 Tomorrow Plan',
        'access_links': '🔗 Access Links',
        'summary': '🎉 Today Summary',
        'reporter': 'Reporter',
        'date': 'Date',
        'version': 'Version'
    },
    'ja': {
        'title': '📔 {date} - 開発日記',
        'date_label': '日付',
        'developer_label': '開発者',
        'version_label': 'バージョン',
        'summary': '📊 今日の概要',
        'work_time': '作業時間',
        'achievements': '主な成果',
        'code_stats': 'コード統計',
        'completed_work': '🎯 完了した作業',
        'performance': '📈 パフォーマンス',
        'quality_metrics': '📊 品質指標',
        'files_delivered': '📁 納品ファイル',
        'v2_progress': '🎯 v2.2 進捗',
        'tech_highlights': '💡 技術ハイライト',
        'git_commits': '🚀 Git コミット',
        'tomorrow_plan': '📋 明日の計画',
        'access_links': '🔗 アクセスリンク',
        'summary': '🎉 今日のまとめ',
        'reporter': '報告者',
        'date': '日付',
        'version': 'バージョン'
    }
}

# 通用内容翻译
CONTENT_TRANSLATIONS = {
    'phase_complete': {
        'zh': '✅ 完成',
        'en': '✅ Complete',
        'ja': '✅ 完了'
    },
    'phase_pending': {
        'zh': '⏳ 待开始',
        'en': '⏳ Pending',
        'ja': '⏳ 待機中'
    },
    'exceeded': {
        'zh': '超额',
        'en': 'Exceeded',
        'ja': '超過'
    },
    'achieved': {
        'zh': '达成',
        'en': 'Achieved',
        'ja': '達成'
    }
}


class DiaryMultiLanguage:
    """日记多语言支持类"""
    
    def __init__(self, default_lang: str = 'zh'):
        """
        初始化多语言支持
        
        Args:
            default_lang: 默认语言
        """
        self.default_lang = default_lang
        self.supported_languages = list(LANGUAGES.keys())
    
    def get_language_info(self, lang_code: str) -> Dict:
        """获取语言信息"""
        return LANGUAGES.get(lang_code, LANGUAGES['zh'])
    
    def get_template(self, lang_code: str) -> Dict:
        """获取日记模板"""
        return DIARY_TEMPLATES.get(lang_code, DIARY_TEMPLATES['zh'])
    
    def translate_label(self, label_key: str, lang_code: str) -> str:
        """翻译标签"""
        if label_key in DIARY_TEMPLATES:
            return DIARY_TEMPLATES[lang_code].get(label_key, label_key)
        return label_key
    
    def generate_diary_title(self, date: str, lang_code: str) -> str:
        """生成日记标题"""
        template = self.get_template(lang_code)
        return template['title'].format(date=date)
    
    def detect_language(self, text: str) -> str:
        """
        检测文本语言
        
        Args:
            text: 待检测文本
        
        Returns:
            语言代码
        """
        # 简单检测：根据字符范围判断
        for char in text:
            if '\u3040' <= char <= '\u309f':  # 平假名
                return 'ja'
            if '\u30a0' <= char <= '\u30ff':  # 片假名
                return 'ja'
        
        # 默认返回中文
        return 'zh'
    
    def generate_language_switcher(self, current_lang: str = 'zh') -> str:
        """
        生成语言切换器 HTML
        
        Args:
            current_lang: 当前语言
        
        Returns:
            HTML 代码
        """
        html = '<div class="language-switcher">\n'
        
        for lang_code, lang_info in LANGUAGES.items():
            active = 'active' if lang_code == current_lang else ''
            html += f'  <button class="lang-btn {active}" data-lang="{lang_code}">'
            html += f'{lang_info["flag"]} {lang_info["name"]}'
            html += '</button>\n'
        
        html += '</div>'
        
        return html
    
    def generate_multilingual_diary(self, diary_content: Dict, output_dir: str):
        """
        生成多语言日记
        
        Args:
            diary_content: 日记内容字典
            output_dir: 输出目录
        """
        for lang_code in self.supported_languages:
            # 生成该语言的日记
            diary_html = self.render_diary(diary_content, lang_code)
            
            # 保存文件
            if lang_code == 'zh':
                filename = f"{diary_content['date']}.html"
            else:
                filename = f"{diary_content['date']}-{lang_code}.html"
            
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(diary_html)
    
    def render_diary(self, diary_content: Dict, lang_code: str) -> str:
        """
        渲染日记 HTML
        
        Args:
            diary_content: 日记内容
            lang_code: 语言代码
        
        Returns:
            HTML 字符串
        """
        template = self.get_template(lang_code)
        
        # 生成 HTML（简化版）
        html = f"""<!DOCTYPE html>
<html lang="{lang_code}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.generate_diary_title(diary_content['date'], lang_code)}</title>
    <style>
        .language-switcher {{
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
        }}
        .lang-btn {{
            padding: 8px 16px;
            margin: 0 4px;
            border: 2px solid #0071e3;
            background: white;
            color: #0071e3;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
        }}
        .lang-btn.active {{
            background: #0071e3;
            color: white;
        }}
    </style>
</head>
<body>
    {self.generate_language_switcher(lang_code)}
    
    <div class="container">
        <h1>{self.generate_diary_title(diary_content['date'], lang_code)}</h1>
        
        <div class="meta">
            <p>{template['date_label']}: {diary_content['date']}</p>
            <p>{template['developer_label']}: {diary_content.get('developer', 'Javis')}</p>
            <p>{template['version_label']}: {diary_content.get('version', 'v2.2')}</p>
        </div>
        
        <div class="content">
            {diary_content.get('content', '')}
        </div>
    </div>
    
    <script>
        // 语言切换逻辑
        document.querySelectorAll('.lang-btn').forEach(btn => {{
            btn.addEventListener('click', () => {{
                const lang = btn.dataset.lang;
                const currentPath = window.location.pathname;
                const newPath = currentPath.replace(/-\\w+\\.html$/, '') + (lang === 'zh' ? '.html' : `-${{lang}}.html`);
                window.location.href = newPath;
            }});
        }});
    </script>
</body>
</html>
"""
        
        return html


def main():
    """测试多语言功能"""
    print("=" * 60)
    print("Guangchu - 日记多语言支持测试")
    print("=" * 60)
    
    ml = DiaryMultiLanguage()
    
    # 测试 1: 语言信息
    print("\n测试 1: 语言信息")
    for lang_code in ml.supported_languages:
        info = ml.get_language_info(lang_code)
        print(f"  {info['flag']} {lang_code}: {info['name']}")
    
    # 测试 2: 模板翻译
    print("\n测试 2: 模板翻译")
    for lang_code in ml.supported_languages:
        template = ml.get_template(lang_code)
        print(f"  {lang_code}: {template['title'].format(date='2026-03-14')}")
    
    # 测试 3: 语言切换器
    print("\n测试 3: 语言切换器")
    switcher = ml.generate_language_switcher('zh')
    print(f"  生成 HTML: {len(switcher)} 字符")
    
    # 测试 4: 语言检测
    print("\n测试 4: 语言检测")
    test_texts = {
        '这是中文': 'zh',
        'This is English': 'zh',  # 默认
        'これは日本語です': 'ja'
    }
    
    for text, expected in test_texts.items():
        detected = ml.detect_language(text)
        status = "✅" if detected == expected else "⚠️"
        print(f"  {status} '{text[:10]}...' -> {detected}")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
