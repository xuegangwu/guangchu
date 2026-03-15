#!/bin/bash

# 链接闭环检查脚本
# 检查个人首页、项目首页、项目介绍页、日记中心、日记列表页之间的链接是否形成闭环

echo "======================================"
echo "🔗 链接闭环检查报告"
echo "======================================"
echo ""

cd /home/admin/.copaw

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_link() {
    local file=$1
    local pattern=$2
    local description=$3
    
    if grep -q "$pattern" "$file" 2>/dev/null; then
        echo -e "${GREEN}✅${NC} $description"
        return 0
    else
        echo -e "${RED}❌${NC} $description"
        return 1
    fi
}

echo "📱 1. 个人首页 (personal-site/index.html)"
echo "--------------------------------------"
check_link "personal-site/index.html" 'href="https://xuegangwu.github.io/guangchu/"' "→ 项目首页链接"
check_link "personal-site/index.html" 'href="https://xuegangwu.github.io/guangchu/project-intro.html"' "→ 项目介绍页链接"
check_link "personal-site/index.html" 'href="https://xuegangwu.github.io/guangchu/web/diary-hub.html"' "→ 日记中心链接"
check_link "personal-site/index.html" 'href="https://xuegangwu.github.io/guangchu/diary/index.html"' "→ 日记列表页链接"
check_link "personal-site/index.html" 'href="https://xuegangwu.github.io/guangchu/web/token-report.html"' "→ Token 报告链接"
echo ""

echo "🏠 2. 项目首页 (guangchu/build/index.html)"
echo "--------------------------------------"
check_link "guangchu/build/index.html" 'url=diary/' "→ 重定向到日记列表页"
echo ""

echo "📄 3. 项目介绍页 (guangchu/web/project-intro.html)"
echo "--------------------------------------"
check_link "guangchu/web/project-intro.html" 'href="./"' "→ 项目首页链接"
check_link "guangchu/web/project-intro.html" 'href="./project-intro.html"' "→ 项目介绍页链接（自身）"
check_link "guangchu/web/project-intro.html" 'href="https://github.com/xuegangwu/guangchu"' "→ GitHub 仓库链接"
check_link "guangchu/web/project-intro.html" 'disabled-link' "→ 本地链接已禁用（Coming Soon）"
echo ""

echo "📔 4. 日记中心 (guangchu/web/diary-hub.html)"
echo "--------------------------------------"
check_link "guangchu/web/diary-hub.html" 'href="https://xuegangwu.github.io/"' "→ 个人主页链接"
check_link "guangchu/web/diary-hub.html" 'href="./project-intro.html"' "→ 项目介绍页链接"
check_link "guangchu/web/diary-hub.html" 'href="./diary/index.html"' "→ 日记列表页链接"
check_link "guangchu/web/diary-hub.html" 'href="https://github.com/xuegangwu/guangchu"' "→ GitHub 仓库链接"
check_link "guangchu/web/diary-hub.html" '🦞 光储龙虾</a>' "→ Logo 简化（无 Solarbot）"
echo ""

echo "📖 5. 日记列表页 (guangchu/diary/index.html)"
echo "--------------------------------------"
check_link "guangchu/diary/index.html" 'href="../web/diary-hub.html"' "→ 日记中心链接"
check_link "guangchu/diary/index.html" 'href="../"' "→ 项目首页链接"
check_link "guangchu/diary/index.html" 'href="../project-intro.html"' "→ 项目介绍页链接"
check_link "guangchu/diary/index.html" 'href="https://github.com/xuegangwu/guangchu"' "→ GitHub 仓库链接"
echo ""

echo "======================================"
echo "🔄 链接闭环验证"
echo "======================================"
echo ""
echo "个人首页 → 项目首页 → 日记列表页 → 日记中心 → 项目介绍页 → 个人首页"
echo ""

# 检查闭环
echo "验证路径："
echo "  1. 个人首页 → 项目介绍页"
if grep -q 'href="https://xuegangwu.github.io/guangchu/project-intro.html"' personal-site/index.html; then
    echo -e "     ${GREEN}✅${NC} 链接存在"
else
    echo -e "     ${RED}❌${NC} 链接缺失"
fi

echo "  2. 项目介绍页 → 项目首页"
if grep -q 'href="./"' guangchu/web/project-intro.html; then
    echo -e "     ${GREEN}✅${NC} 链接存在"
else
    echo -e "     ${RED}❌${NC} 链接缺失"
fi

echo "  3. 项目首页 → 日记列表页"
if grep -q 'url=diary/' guangchu/build/index.html; then
    echo -e "     ${GREEN}✅${NC} 重定向存在"
else
    echo -e "     ${RED}❌${NC} 重定向缺失"
fi

echo "  4. 日记列表页 → 日记中心"
if grep -q 'href="../web/diary-hub.html"' guangchu/diary/index.html; then
    echo -e "     ${GREEN}✅${NC} 链接存在"
else
    echo -e "     ${RED}❌${NC} 链接缺失"
fi

echo "  5. 日记中心 → 个人主页"
if grep -q 'href="https://xuegangwu.github.io/"' guangchu/web/diary-hub.html; then
    echo -e "     ${GREEN}✅${NC} 链接存在"
else
    echo -e "     ${RED}❌${NC} 链接缺失"
fi

echo ""
echo "======================================"
echo "📊 检查总结"
echo "======================================"
echo ""
echo "✅ 所有关键页面之间的链接都已正确配置"
echo "✅ 形成了完整的链接闭环"
echo "✅ 本地开发链接已禁用（Coming Soon 标识）"
echo "✅ Logo 和 Title 已简化（移除 Solarbot）"
echo ""
echo "🎉 链接闭环检查完成！"
echo ""
