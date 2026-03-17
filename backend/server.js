#!/usr/bin/env node
/**
 * 光储电站投资地图 - 后端 API 服务器 (sql.js 版本)
 */

require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');

// 导入路由
const authRoutes = require('./routes/auth');
const userRoutes = require('./routes/users');
const provinceRoutes = require('./routes/provinces');
const projectRoutes = require('./routes/projects');
const priceRoutes = require('./routes/prices');
const logRoutes = require('./routes/logs');
const settingRoutes = require('./routes/settings');
const statsRoutes = require('./routes/stats');

// 中间件
const { authenticateToken, logOperation } = require('./middleware/auth');
const { autoSave } = require('./utils/database');

const app = express();
const PORT = process.env.PORT || 3000;

// 中间件
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 请求日志
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(`${req.method} ${req.path} ${res.statusCode} - ${duration}ms`);
  });
  next();
});

// API 路由（必须在静态文件之前）
app.use('/api/auth', authRoutes);
app.use('/api/users', authenticateToken, userRoutes);
app.use('/api/provinces', provinceRoutes);
app.use('/api/projects', projectRoutes);
app.use('/api/prices', priceRoutes);
app.use('/api/logs', authenticateToken, logRoutes);
app.use('/api/settings', authenticateToken, settingRoutes);
app.use('/api/stats', authenticateToken, statsRoutes);

// 健康检查
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// News API (public) - 光储新闻
app.get('/api/news', (req, res) => {
  const news = [
    { id: 1, source: 'PV Magazine', title: '欧盟宣布2030年光伏装机目标提升至600GW', url: 'https://www.pv-magazine.com', date: '2026-03-16', emoji: '☀️' },
    { id: 2, source: 'Solar Power World', title: '美国加州光伏装机突破80GW，储能需求激增', url: 'https://www.solarpowerworldonline.com', date: '2026-03-16', emoji: '🇺🇸' },
    { id: 3, source: 'Energy Storage News', title: '全球储能市场2025年增长45%，中国领先', url: '#', date: '2026-03-15', emoji: '🔋' },
    { id: 4, source: 'PV Magazine', title: '越南光伏政策调整，利好分布式项目', url: 'https://www.pv-magazine.com', date: '2026-03-15', emoji: '🇻🇳' },
    { id: 5, source: 'Solar Power World', title: '巴西光伏装机超50GW，拉美市场火热', url: 'https://www.solarpowerworldonline.com', date: '2026-03-14', emoji: '🇧🇷' }
  ];
  res.json(news);
});


// 静态文件服务（前端）

// 前端路由
// Counter API
const { getCounter, incrementCounter } = require('./counter');

app.get('/api/counter', (req, res) => {
    const count = incrementCounter();
    res.json({ count: count.count, label: '访问量' });
});

app.get('/api/counter/reset', (req, res) => {
    const count = getCounter();
    res.json({ count: count.count, label: '访问量' });
});

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../web/login-v1.0.html'));
});

// 错误处理
app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(err.status || 500).json({
    error: err.message || 'Internal Server Error'
  });
});

// 启动服务器
app.listen(PORT, () => {
  // 启动自动保存
  autoSave();
  
  console.log(`
╔════════════════════════════════════════════════════════╗
║   🌞 光储电站投资地图 - 后端 API 服务                    ║
╠════════════════════════════════════════════════════════╣
║   服务地址：http://localhost:${PORT}                      ║
║   环境：${process.env.NODE_ENV || 'development'}                                ║
║   数据库：data/solar-storage.db (sql.js)                ║
╠════════════════════════════════════════════════════════╣
║   API 文档：http://localhost:${PORT}/api/health           ║
║   前端页面：http://localhost:${PORT}                      ║
╚════════════════════════════════════════════════════════╝
  `);
});

module.exports = app;

// News API (public)

