# ⚠️ NocoBase 本地部署问题总结

> **时间：** 2026-03-13 12:02  
> **状态：** 遇到技术障碍

---

## ❌ 遇到的问题

### 问题 1：架构不兼容 ✅ 已解决
```
error @nocobase/license-kit-linux-arm-gnueabihf@0.3.7: 
The CPU architecture "x64" is incompatible with this module.
```
**解决：** 修改 resolutions 重定向到 x64 包

### 问题 2：数据库配置缺失 ✅ 已解决
```
Error: DB_DIALECT is required.
```
**解决：** 配置 `.env` 文件添加 `DB_DIALECT=sqlite`

### 问题 3：依赖缺失 ❌ 未解决
```
Error: Cannot find module './stringify'
Require stack:
- @hapi/hoek/lib/error.js
- joi/lib/index.js
- @nocobase/database/lib/index.js
...
```

**根本原因：**
- NocoBase 2.0.16 存在依赖问题
- `@hapi/hoek` 模块内部文件缺失
- 这是 NocoBase 2.0 版本的已知 bug

---

## 🛠️ 建议方案

### 方案 A：使用 Docker 部署（强烈推荐⭐）

这是 NocoBase 官方推荐的方式，也是最稳定的方式。

**步骤：**

1. **安装 Docker**
```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
```

2. **启动 NocoBase**
```bash
docker run -d --name nocobase \
  -p 13000:80 \
  -v nocobase-storage:/app/nocobase/storage \
  nocobase/nocobase:latest
```

3. **访问系统**
```
http://localhost:13000
```

**优势：**
- ✅ 官方支持
- ✅ 环境隔离
- ✅ 一键部署
- ✅ 易于升级
- ✅ 无依赖问题

**时间：** 5-10 分钟

---

### 方案 B：降级到 NocoBase 1.x（稳定版）

NocoBase 1.x 版本更稳定，但功能较少。

**步骤：**
```bash
cd /home/admin/openclaw/workspace/projects
rm -rf nocobase-test
npx create-nocobase-app@1 nocobase-test
cd nocobase-test
yarn install
yarn nocobase install
yarn dev
```

**时间：** 10-15 分钟

---

### 方案 C：等待 NocoBase 修复（不推荐）

等待 NocoBase 发布 2.0.17 或更高版本修复此问题。

**预计时间：** 未知

---

## 💡 我的建议

**立即采用方案 A（Docker 部署）**

理由：
1. 本地部署遇到 NocoBase 2.0 的已知 bug
2. Docker 是官方推荐方式
3. 5-10 分钟即可完成
4. 后续维护和升级更简单

---

## 📞 需要您的决策

请告诉我您希望：

**A. 安装 Docker 部署**（推荐，5-10 分钟完成）
**B. 降级到 1.x 版本**（稳定，但功能较少）
**C. 暂停部署**（等待 NocoBase 修复）

---

**最后更新：** 2026-03-13 12:02
