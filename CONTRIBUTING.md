# Contributing to Guangchu

感谢你为光储龙虾项目做出贡献！

## 📋 目录

- [开发环境设置](#开发环境设置)
- [代码规范](#代码规范)
- [测试指南](#测试指南)
- [提交流程](#提交流程)
- [问题反馈](#问题反馈)

---

## 🛠️ 开发环境设置

### 1. 克隆项目
```bash
git clone https://github.com/xuegangwu/guangchu.git
cd guangchu
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
pip install -r requirements-test.txt
```

### 3. 配置环境
```bash
# 可选：设置环境变量
export GUANGCHU_TIMEOUT=30
export GUANGCHU_MAX_RETRIES=3
```

### 4. 运行测试
```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_advanced_search.py -v

# 生成覆盖率报告
pytest tests/ --cov=scripts --cov-report=html
```

---

## 📝 代码规范

### Python 代码风格

遵循 PEP 8 规范：

```python
# ✅ 好的命名
def fetch_news(url: str, max_retries: int = 3) -> List[Dict]:
    """抓取新闻"""
    pass

# ❌ 避免
def f(u, m=3):
    pass
```

### 类型注解

所有公开函数必须添加类型注解：

```python
from typing import List, Dict, Optional

def search(
    query: str,
    filters: Optional[Dict] = None,
    limit: int = 20
) -> List[Dict]:
    """搜索新闻"""
    pass
```

### 文档字符串

所有公开函数必须有文档字符串：

```python
def fetch_news(url: str) -> List[Dict]:
    """
    抓取新闻
    
    Args:
        url: 新闻 URL
    
    Returns:
        新闻列表
    
    Raises:
        ConnectionError: 网络连接失败
    """
    pass
```

### 代码格式化

使用 black 格式化代码：

```bash
# 格式化所有代码
black scripts/ tests/

# 检查格式
black scripts/ tests/ --check
```

### 导入排序

使用 isort 排序导入：

```bash
isort scripts/ tests/
```

---

## 🧪 测试指南

### 编写测试

测试文件命名：`test_*.py`

```python
import pytest

class TestFeature:
    """测试功能"""
    
    def test_feature_works(self):
        """测试功能正常工作"""
        assert True
```

### 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定模块
pytest tests/test_advanced_search.py -v

# 运行特定测试
pytest tests/test_advanced_search.py::TestAdvancedSearch::test_search -v

# 生成覆盖率报告
pytest tests/ --cov=scripts --cov-report=html --cov-report=term
```

### 测试覆盖率目标

- **总体覆盖率**: > 80%
- **核心功能**: > 90%
- **新增代码**: 必须包含测试

---

## 📤 提交流程

### Commit Message 规范

遵循 Conventional Commits：

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type 类型
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具

#### 示例
```
feat(search): add advanced search functionality

- Implement keyword highlighting
- Add multi-condition filters
- Support sorting by relevance/date

Closes #123
```

### 提交流程

```bash
# 1. 创建分支
git checkout -b feature/your-feature

# 2. 开发并测试
# ... 开发代码 ...
pytest tests/ -v

# 3. 格式化代码
black scripts/ tests/
isort scripts/ tests/

# 4. 提交
git add .
git commit -m "feat: add your feature"

# 5. 推送
git push origin feature/your-feature

# 6. 创建 Pull Request
```

---

## 🐛 问题反馈

### 提交 Issue

使用 Issue 模板：

```markdown
**问题描述**
清晰简洁地描述问题

**复现步骤**
1. 执行 '...'
2. 点击 '...'
3. 看到错误

**预期行为**
清晰简洁地描述预期行为

**截图**
如果适用，添加截图

**环境信息**
- OS: [e.g. Ubuntu 20.04]
- Python: [e.g. 3.9]
- Version: [e.g. v2.2]
```

### Issue 标签
- `bug`: Bug 报告
- `feature`: 功能请求
- `documentation`: 文档相关
- `performance`: 性能问题
- `question`: 问题咨询

---

## 📚 开发资源

### 相关文档
- [v2.1 质量提升报告](v2.1-发布说明.md)
- [v2.2 开发进度](v2.2-开发进度报告.md)
- [API 文档](docs/API.md)

### 外部资源
- [Python 风格指南](https://peps.python.org/pep-0008/)
- [pytest 文档](https://docs.pytest.org/)
- [black 文档](https://black.readthedocs.io/)

---

## 🎯 当前开发重点

### v2.2 版本（进行中）
- ✅ Phase 1: 高级搜索
- ✅ Phase 2: 性能优化
- ⏳ Phase 3: 文档完善
- ⏳ Phase 4: API 接口
- ⏳ Phase 5: PWA 支持

### 需要帮助的领域
1. 测试覆盖率提升
2. API 文档完善
3. 性能优化
4. 国际化支持

---

## 💡 提示

### 开发前
- [ ] 检查现有 Issue
- [ ] 创建新分支
- [ ] 设置开发环境

### 开发中
- [ ] 编写测试
- [ ] 格式化代码
- [ ] 更新文档

### 提交前
- [ ] 运行所有测试
- [ ] 检查测试覆盖率
- [ ] 更新 CHANGELOG

### 提交后
- [ ] 创建 Pull Request
- [ ] 响应 Code Review
- [ ] 合并到主分支

---

感谢你的贡献！🎉
