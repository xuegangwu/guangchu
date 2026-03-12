#!/usr/bin/env python3
"""
光储龙虾 - 多语言翻译服务
支持 Google Translate、DeepL、百度翻译等 API
"""

import json
import hashlib
import time
from typing import Dict, Optional, List
from pathlib import Path

# 配置文件路径
CONFIG_PATH = Path(__file__).parent.parent / 'config' / 'translation.json'


class TranslationService:
    """翻译服务类"""
    
    def __init__(self, provider: str = 'google'):
        """
        初始化翻译服务
        
        Args:
            provider: 翻译服务提供商 (google, deepl, baidu, youdao)
        """
        self.provider = provider
        self.config = self._load_config()
        self.cache = {}  # 简单缓存
        self.cache_file = Path(__file__).parent.parent / 'data' / 'translation_cache.json'
        self._load_cache()
    
    def _load_config(self) -> Dict:
        """加载配置文件"""
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _load_cache(self):
        """加载翻译缓存"""
        if self.cache_file.exists():
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                self.cache = json.load(f)
    
    def _save_cache(self):
        """保存翻译缓存"""
        self.cache_file.parent.mkdir(exist_ok=True)
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)
    
    def _get_cache_key(self, text: str, target_lang: str) -> str:
        """生成缓存键"""
        return hashlib.md5(f"{text}:{target_lang}".encode()).hexdigest()
    
    def translate(self, text: str, target_lang: str, source_lang: str = 'auto') -> str:
        """
        翻译文本
        
        Args:
            text: 待翻译文本
            target_lang: 目标语言 (en, zh, ja)
            source_lang: 源语言
        
        Returns:
            翻译后的文本
        """
        if not text or len(text) < 2:
            return text
        
        # 检查缓存
        cache_key = self._get_cache_key(text, target_lang)
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # 选择翻译提供商
        if self.provider == 'google':
            result = self._translate_google(text, target_lang, source_lang)
        elif self.provider == 'deepl':
            result = self._translate_deepl(text, target_lang, source_lang)
        elif self.provider == 'baidu':
            result = self._translate_baidu(text, target_lang, source_lang)
        elif self.provider == 'youdao':
            result = self._translate_youdao(text, target_lang, source_lang)
        else:
            result = text  # 默认返回原文
        
        # 缓存结果
        if result and result != text:
            self.cache[cache_key] = result
            self._save_cache()
        
        return result
    
    def _translate_google(self, text: str, target_lang: str, source_lang: str) -> str:
        """
        Google Translate API
        
        需要安装：pip install googletrans==4.0.0-rc1
        """
        try:
            from googletrans import Translator
            translator = Translator()
            result = translator.translate(text, src=source_lang, dest=target_lang)
            return result.text
        except ImportError:
            print("⚠️  未安装 googletrans: pip install googletrans==4.0.0-rc1")
            return text
        except Exception as e:
            print(f"❌ Google 翻译失败：{e}")
            return text
    
    def _translate_deepl(self, text: str, target_lang: str, source_lang: str) -> str:
        """
        DeepL API
        
        需要安装：pip install deepl
        API Key: https://www.deepl.com/pro-api
        """
        try:
            import deepl
            
            api_key = self.config.get('deepl', {}).get('api_key')
            if not api_key:
                print("⚠️  DeepL API Key 未配置")
                return text
            
            translator = deepl.Translator(api_key)
            
            # 语言代码映射
            lang_map = {'en': 'EN-US', 'zh': 'ZH', 'ja': 'JA'}
            target = lang_map.get(target_lang, 'EN-US')
            
            result = translator.translate_text(text, target_lang=target)
            return result.text
        except ImportError:
            print("⚠️  未安装 deepl: pip install deepl")
            return text
        except Exception as e:
            print(f"❌ DeepL 翻译失败：{e}")
            return text
    
    def _translate_baidu(self, text: str, target_lang: str, source_lang: str) -> str:
        """
        百度翻译 API
        
        API: https://fanyi-api.baidu.com/
        """
        try:
            import requests
            
            config = self.config.get('baidu', {})
            appid = config.get('appid')
            secret = config.get('secret')
            
            if not appid or not secret:
                print("⚠️  百度翻译 API 未配置")
                return text
            
            # 语言代码映射
            lang_map = {'en': 'en', 'zh': 'zh', 'ja': 'jp'}
            target = lang_map.get(target_lang, 'en')
            
            # 生成签名
            salt = str(int(time.time()))
            sign_str = f"{appid}{text}{salt}{secret}"
            sign = hashlib.md5(sign_str.encode()).hexdigest()
            
            # 请求 API
            url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
            params = {
                'q': text,
                'from': source_lang if source_lang != 'auto' else 'auto',
                'to': target,
                'appid': appid,
                'salt': salt,
                'sign': sign
            }
            
            response = requests.get(url, params=params, timeout=10)
            result = response.json()
            
            if 'trans_result' in result:
                return result['trans_result'][0]['dst']
            else:
                print(f"❌ 百度翻译错误：{result}")
                return text
        except ImportError:
            print("⚠️  未安装 requests: pip install requests")
            return text
        except Exception as e:
            print(f"❌ 百度翻译失败：{e}")
            return text
    
    def _translate_youdao(self, text: str, target_lang: str, source_lang: str) -> str:
        """
        有道翻译 API
        
        API: https://ai.youdao.com/DOCSIRMA/html/trans/api/wbfy/index.html
        """
        try:
            import requests
            import hashlib
            import time
            
            config = self.config.get('youdao', {})
            app_key = config.get('app_key')
            secret = config.get('secret')
            
            if not app_key or not secret:
                print("⚠️  有道翻译 API 未配置")
                return text
            
            # 语言代码映射
            lang_map = {'en': 'EN', 'zh': 'zh-CHS', 'ja': 'JP'}
            target = lang_map.get(target_lang, 'EN')
            
            # 生成签名
            curtime = str(int(time.time()))
            salt = str(int(time.time() * 1000))
            
            # 处理长文本
            if len(text) > 20:
                input_text = text[:10] + str(len(text)) + text[-10:]
            else:
                input_text = text
            
            sign_str = f"{app_key}{input_text}{salt}{curtime}{secret}"
            sign = hashlib.sha256(sign_str.encode()).hexdigest()
            
            # 请求 API
            url = 'https://openapi.youdao.com/api'
            params = {
                'q': text,
                'from': source_lang if source_lang != 'auto' else 'auto',
                'to': target,
                'appKey': app_key,
                'salt': salt,
                'curtime': curtime,
                'signType': 'v3',
                'sign': sign
            }
            
            response = requests.get(url, params=params, timeout=10)
            result = response.json()
            
            if 'translation' in result:
                return ''.join(result['translation'])
            else:
                print(f"❌ 有道翻译错误：{result}")
                return text
        except ImportError:
            print("⚠️  未安装 requests")
            return text
        except Exception as e:
            print(f"❌ 有道翻译失败：{e}")
            return text
    
    def translate_to_multiple(self, text: str, source_lang: str = 'auto') -> Dict[str, str]:
        """
        翻译成多种语言
        
        Returns:
            {'en': '...', 'zh': '...', 'ja': '...'}
        """
        return {
            'en': self.translate(text, 'en', source_lang),
            'zh': self.translate(text, 'zh', source_lang),
            'ja': self.translate(text, 'ja', source_lang)
        }
    
    def batch_translate(self, texts: List[str], target_lang: str, source_lang: str = 'auto') -> List[str]:
        """
        批量翻译
        
        Args:
            texts: 待翻译文本列表
            target_lang: 目标语言
            source_lang: 源语言
        
        Returns:
            翻译后的文本列表
        """
        results = []
        for i, text in enumerate(texts):
            print(f"  翻译 {i+1}/{len(texts)}...")
            results.append(self.translate(text, target_lang, source_lang))
            time.sleep(0.1)  # 避免频率限制
        return results


# 使用示例
if __name__ == "__main__":
    # 初始化翻译服务
    translator = TranslationService(provider='google')
    
    # 单条翻译
    text = "太阳能电站投资评估系统"
    print(f"原文：{text}")
    print(f"英文：{translator.translate(text, 'en')}")
    print(f"日文：{translator.translate(text, 'ja')}")
    
    # 多条翻译
    translations = translator.translate_to_multiple("储能电池价格")
    print(f"\n多语言翻译:")
    print(f"  EN: {translations['en']}")
    print(f"  ZH: {translations['zh']}")
    print(f"  JA: {translations['ja']}")
