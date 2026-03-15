# 🌍 多语言切换功能说明

## 功能概述

项目介绍页现已支持**中文、英文、日文**三种语言切换，每次只显示一种语言，确保页面排版整洁美观。

---

## 🎯 主要特性

### 1. 语言切换按钮
- 🇨🇳 **中文** - 默认语言
- 🇬🇧 **English** - 英文版本
- 🇯🇵 **日本語** - 日文版本

### 2. 智能记忆
- ✅ 自动保存用户语言偏好到 localStorage
- ✅ 下次访问时自动加载上次选择的语言
- ✅ 默认语言为中文

### 3. 内容切换
切换语言时，以下内容会同步更新：
- 项目名称
- 副标题
- 描述文字
- 按钮文字
- 提示信息

---

## 📱 使用方式

### 桌面端
1. 打开项目介绍页
2. 点击顶部的语言切换按钮
3. 页面立即切换为对应语言

### 移动端
1. 打开手机浏览器访问页面
2. 点击顶部的语言切换按钮（已针对小屏优化）
3. 页面立即切换为对应语言

---

## 🎨 设计特点

### 按钮样式
- **未选中**: 半透明白色背景，白色边框
- **悬停**: 增加背景透明度
- **选中**: 白色背景，红色文字
- **形状**: 圆角胶囊形 (border-radius: 980px)

### 响应式适配
- **Desktop**: 按钮间距 12px，字体 14px
- **Tablet (≤768px)**: 按钮间距 8px，字体 13px
- **Mobile (≤375px)**: 按钮间距 6px，字体 12px

---

## 📊 语言对照表

| 项目 | 中文 | English | 日本語 |
|------|------|---------|--------|
| **项目名称** | 光储龙虾 | Solarbot | ソーラーロボ |
| **副标题** | 光伏 + 储能行业信息收集与分析系统 | Solar-Storage News Collection & Analysis System | 太陽光・蓄電池ニュース収集・分析システム |
| **描述** | 全球光伏 + 储能行业信息收集与分析系统<br>支持 22 个信息源，多语言自动翻译，智能数据处理 | Global solar and energy storage industry information collection and analysis system<br>Supporting 22 information sources, multi-language auto translation, intelligent data processing | 世界の太陽光発電およびエネルギー貯蔵業界の情報収集・分析システム<br>22 の情報源、多言語自動翻訳、インテリジェントデータ処理をサポート |
| **体验按钮** | 🔍 立即体验 | 🔍 Try Now | 🔍 今すぐ試す |
| **GitHub 按钮** | 🔗 GitHub 仓库 | 🔗 GitHub Repository | 🔗 GitHub リポジトリ |
| **即将上线** | 即将上线 · 敬请期待 | Coming Soon | 近日公開 |

---

## 💻 技术实现

### HTML 结构
```html
<!-- Language Switcher -->
<div class="language-switcher">
    <button class="lang-btn active" onclick="switchLanguage('zh')">🇨🇳 中文</button>
    <button class="lang-btn" onclick="switchLanguage('en')">🇬🇧 EN</button>
    <button class="lang-btn" onclick="switchLanguage('ja')">🇯🇵 日本語</button>
</div>

<!-- Language Content -->
<div class="lang-content lang-zh active">
    <!-- 中文内容 -->
</div>
<div class="lang-content lang-en">
    <!-- 英文内容 -->
</div>
<div class="lang-content lang-ja">
    <!-- 日文内容 -->
</div>
```

### CSS 样式
```css
.language-switcher {
    display: flex;
    gap: 12px;
    justify-content: center;
}

.lang-btn {
    padding: 8px 16px;
    border-radius: 980px;
    transition: all 0.2s;
}

.lang-content {
    display: none;
}

.lang-content.active {
    display: block;
}
```

### JavaScript 功能
```javascript
function switchLanguage(lang) {
    // 移除所有 active 类
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelectorAll('.lang-content').forEach(content => {
        content.classList.remove('active');
    });
    
    // 添加 active 类到选中语言
    document.querySelector(`.lang-btn[onclick="switchLanguage('${lang}')"]`).classList.add('active');
    document.querySelector(`.lang-${lang}`).classList.add('active');
    
    // 保存偏好
    localStorage.setItem('preferred-lang', lang);
}
```

---

## 🔧 扩展其他语言

如需添加其他语言（如韩文、西班牙文），按以下步骤：

### 1. 添加按钮
```html
<button class="lang-btn" onclick="switchLanguage('ko')">🇰🇷 한국어</button>
```

### 2. 添加内容
```html
<div class="lang-content lang-ko">
    <h1>태양로봇</h1>
    <p class="hero-subtitle">태양광 저장 뉴스 수집 및 분석 시스템</p>
    <!-- 其他内容 -->
</div>
```

### 3. 无需修改 JavaScript
切换逻辑已通用化，自动支持新语言。

---

## 📱 移动端优化

### 按钮尺寸
- **标准**: 8px padding, 14px 字体
- **平板**: 6px padding, 13px 字体
- **手机**: 5px padding, 12px 字体

### 布局调整
- Hero 区域 padding 从 100px 减少到 80px
- 语言切换按钮间距缩小
- 确保按钮在小屏幕上易于点击

---

## ✅ 优势对比

### ❌ 之前的问题
- 所有语言同时显示
- 页面冗长，排版扭曲
- 用户需要滚动查看
- 视觉焦点分散

### ✅ 现在的优势
- 每次只显示一种语言
- 页面简洁，排版整齐
- 一键切换，即时响应
- 视觉焦点集中
- 用户偏好自动保存

---

## 🌐 访问链接

**项目介绍页：**
```
https://xuegangwu.github.io/guangchu/project-intro.html
```

**测试步骤：**
1. 打开页面
2. 点击顶部的语言切换按钮
3. 观察内容变化
4. 刷新页面，验证偏好保存

---

## 📅 更新日志

### 2026-03-15
- ✅ 添加中文、英文、日文三种语言
- ✅ 实现语言切换功能
- ✅ 添加 localStorage 偏好保存
- ✅ 优化移动端显示
- ✅ 添加响应式适配

---

**功能开发**: Terry Wu (Copilot)  
**技术支持**: HTML5 + CSS3 + JavaScript  
**部署平台**: GitHub Pages
