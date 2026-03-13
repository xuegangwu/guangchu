# NocoBase 代码架构分析与飞书/自媒体集成方案

> 深入分析 NocoBase 源码架构，设计飞书集成与自媒体打通方案

**版本：** v1.0  
**分析日期：** 2026-03-13  
**目标：** 新能源内部管理系统 + 飞书集成 + 自媒体矩阵打通

---

## 📋 目录

1. [NocoBase 代码架构深度分析](#nocobase 代码架构深度分析)
2. [插件系统架构](#插件系统架构)
3. [AI 员工系统源码分析](#ai 员工系统源码分析)
4. [飞书集成方案](#飞书集成方案)
5. [自媒体矩阵打通方案](#自媒体矩阵打通方案)
6. [完整集成架构设计](#完整集成架构设计)
7. [实施路线图](#实施路线图)

---

## 🔍 NocoBase 代码架构深度分析

### 整体架构

```
nocobase/
├── packages/
│   ├── core/              # 核心模块
│   │   ├── acl/           # 访问控制列表
│   │   ├── actions/       # 动作系统
│   │   ├── ai/            # AI 核心引擎 ⭐
│   │   ├── app/           # 应用核心
│   │   ├── auth/          # 认证系统
│   │   ├── database/      # 数据库抽象层
│   │   ├── flow-engine/   # 流程引擎 ⭐
│   │   ├── data-source-manager/  # 数据源管理 ⭐
│   │   ├── resourcer/     # 资源 API
│   │   ├── server/        # 服务器核心
│   │   └── client/        # 前端客户端
│   │
│   ├── plugins/           # 插件系统 ⭐
│   │   └── @nocobase/     # 官方插件
│   │       ├── plugin-ai/                    # AI 插件
│   │       ├── plugin-workflow/              # 工作流引擎
│   │       ├── plugin-workflow-request/      # HTTP 请求 ⭐
│   │       ├── plugin-workflow-mailer/       # 邮件发送
│   │       ├── plugin-workflow-notification/ # 通知发送 ⭐
│   │       ├── plugin-api-keys/              # API 密钥管理
│   │       ├── plugin-data-source-manager/   # 数据源管理
│   │       └── ...
│   │
│   └── presets/           # 预设配置
```

### 核心模块解析

#### 1. AI 核心引擎 (`packages/core/ai`)

```typescript
// AI 服务架构
AI Core
├── AIProvider         # AI 提供商接口（支持多模型）
├── AIService          # AI 服务核心
├── AIEndpoint         # AI 端点管理
├── AIModel            # 模型配置
└── AIProxy            # 代理层

// 支持的 AI 提供商
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- 百度文心一言
- 阿里通义千问
- 智谱 AI
- 月之暗面 (Kimi)
```

**关键代码结构：**
```typescript
// packages/core/ai/src/types.ts
interface AIProvider {
  name: string;
  endpoint: string;
  apiKey: string;
  models: AIModel[];
}

interface AIEmployee {
  id: string;
  name: string;
  role: string;
  skills: Skill[];
  tools: Tool[];
  knowledgeBase: KnowledgeBase;
  context: AIContext;
}

interface Skill {
  name: string;
  description: string;
  prompt: string;
  parameters: Parameter[];
}

interface Tool {
  name: string;
  type: 'api' | 'function' | 'workflow';
  config: ToolConfig;
}
```

#### 2. 工作流引擎 (`packages/core/flow-engine`)

```typescript
// 工作流节点类型
Workflow Nodes
├── TriggerNode        # 触发器（定时/事件/Webhook）
├── ActionNode         # 动作节点
├── ConditionNode      # 条件判断
├── LoopNode           # 循环
├── ParallelNode       # 并行执行
├── DelayNode          # 延迟执行
├── RequestNode        # HTTP 请求 ⭐
├── ScriptNode         # JavaScript 脚本
└── AINode             # AI 调用 ⭐
```

**关键能力：**
- ✅ 可视化流程编排
- ✅ 支持 HTTP 请求（可调用飞书 API）
- ✅ 支持 JavaScript 脚本（自定义逻辑）
- ✅ 支持 AI 调用（嵌入 AI 员工）
- ✅ 支持定时触发（cron 表达式）
- ✅ 支持 Webhook 触发（接收外部事件）

#### 3. 数据源管理 (`packages/core/data-source-manager`)

```typescript
// 支持的数据源类型
Data Sources
├── MainDatabase       # 主数据库（PostgreSQL/MySQL）
├── ExternalDatabase   # 外部数据库
├── REST_API           # REST API ⭐
├── GraphQL_API        # GraphQL API
├── Webhook            # Webhook 接收 ⭐
└── ThirdParty         # 第三方服务（飞书/钉钉等）
```

---

## 🔌 插件系统架构

### 插件开发框架

```typescript
// 插件标准结构
plugin-custom-integration/
├── client/            # 前端代码
│   ├── index.tsx      # 入口
│   ├── components/    # React 组件
│   └── locales/       # 国际化
│
├── server/            # 后端代码
│   ├── index.ts       # 入口
│   ├── actions/       # 自定义动作
│   ├── services/      # 服务层
│   └── migrations/    # 数据库迁移
│
├── package.json
└── README.md
```

### 插件注册机制

```typescript
// server/index.ts
export default {
  name: 'plugin-custom-integration',
  displayName: 'Custom Integration',
  
  async load() {
    // 注册数据源类型
    this.app.dataSourceManager.registerDataSourceType('feishu', {
      displayName: '飞书',
      icon: 'FeishuIcon',
    });
    
    // 注册 API 端点
    this.app.resourcer.registerActionHandlers({
      'feishu:send-message': feishuSendMessage,
      'feishu:get-user': feishuGetUser,
    });
    
    // 注册工作流动作
    this.app.workflowManager.registerActionType('feishu-notification', {
      displayName: '发送飞书消息',
      component: 'FeishuNotificationAction',
    });
  },
};
```

---

## 🤖 AI 员工系统源码分析

### AI 员工架构

```typescript
// AI 员工完整结构
interface AIEmployee {
  // 基础信息
  id: string;
  name: string;
  role: string;
  avatar?: string;
  description: string;
  
  // 技能配置
  skills: {
    name: string;
    systemPrompt: string;  // 系统提示词
    temperature: number;   // 温度参数
    maxTokens: number;     // 最大 token 数
  }[];
  
  // 工具调用
  tools: {
    type: 'api_call' | 'workflow_trigger' | 'database_query';
    name: string;
    config: {
      method: 'GET' | 'POST' | 'PUT' | 'DELETE';
      url: string;
      headers: Record<string, string>;
      body?: any;
    };
  }[];
  
  // 知识库
  knowledgeBase: {
    type: 'vector' | 'document' | 'database';
    source: string;
    embeddingModel: string;
  }[];
  
  // 上下文管理
  context: {
    maxHistoryLength: number;
    includeCurrentRecord: boolean;
    includeRelatedRecords: boolean;
  };
  
  // 触发条件
  triggers: {
    type: 'manual' | 'auto' | 'schedule';
    event?: string;
    cron?: string;
    conditions?: Condition[];
  }[];
}
```

### AI 员工调用流程

```
用户操作/事件触发
    ↓
AI 员工接收请求
    ↓
读取上下文（当前记录 + 关联数据）
    ↓
加载知识库（向量检索）
    ↓
选择合适技能/工具
    ↓
调用 LLM API
    ↓
解析响应
    ↓
执行工具调用（如发送飞书消息）
    ↓
更新数据库
    ↓
返回结果
```

---

## 📱 飞书集成方案

### 飞书开放平台 API 能力

| API 类别 | 能力 | 使用场景 |
|---------|------|----------|
| **消息发送** | 发送文本/卡片/图片消息 | 通知推送、日报发送 |
| **机器人** | 群机器人、个人机器人 | 自动回复、指令处理 |
| **日历** | 创建/查询日程 | 会议管理、提醒 |
| **云文档** | 创建/更新文档 | 报告生成、知识沉淀 |
| **审批** | 发起/查询审批 | 流程审批 |
| **通讯录** | 获取用户/部门信息 | 权限管理、通知对象 |
| **事件订阅** | 接收飞书事件 | 双向同步 |

### 集成架构

```
┌─────────────────────────────────────────────────────────────┐
│                     NocoBase 系统                            │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  AI 员工     │  │  工作流引擎  │  │  自定义插件         │ │
│  │  (行业分析) │  │  (自动化)   │  │  (飞书集成)         │ │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘ │
│         │                 │                    │            │
│         └─────────────────┴────────────────────┘            │
│                               ↓                              │
│                    ┌──────────────────┐                     │
│                    │  HTTP Request    │                     │
│                    │  (Feishu API)    │                     │
│                    └──────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
                               ↓
                    ┌──────────────────┐
                    │   飞书开放平台    │
                    │  open.feishu.cn  │
                    └──────────────────┘
                               ↓
         ┌─────────────┬─────────────┬─────────────┐
         ↓             ↓             ↓             ↓
    群聊消息      个人消息      云文档       日历日程
```

### 飞书插件开发

#### 1. 插件结构

```
plugin-feishu-integration/
├── client/
│   ├── index.tsx
│   ├── components/
│   │   ├── FeishuConfigPanel.tsx    # 配置面板
│   │   ├── FeishuMessageAction.tsx  # 消息发送动作
│   │   └── FeishuCardTemplate.tsx   # 卡片模板
│   └── locales/
│       ├── zh-CN.json
│       └── en-US.json
│
├── server/
│   ├── index.ts
│   ├── services/
│   │   ├── FeishuService.ts         # 飞书 API 服务
│   │   ├── FeishuAuth.ts            # 认证管理
│   │   └── FeishuMessageBuilder.ts  # 消息构建器
│   └── actions/
│       ├── sendMessage.ts           # 发送消息
│       ├── createDoc.ts             # 创建文档
│       └── createEvent.ts           # 创建日程
│
├── package.json
└── README.md
```

#### 2. 核心服务代码

```typescript
// server/services/FeishuService.ts
import { Application } from '@nocobase/server';

export class FeishuService {
  private app: Application;
  private appId: string;
  private appSecret: string;
  private accessToken: string;
  
  constructor(app: Application, config: FeishuConfig) {
    this.app = app;
    this.appId = config.appId;
    this.appSecret = config.appSecret;
  }
  
  // 获取访问令牌
  async getAccessToken(): Promise<string> {
    const response = await fetch(
      'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          app_id: this.appId,
          app_secret: this.appSecret,
        }),
      }
    );
    const data = await response.json();
    this.accessToken = data.tenant_access_token;
    return this.accessToken;
  }
  
  // 发送文本消息
  async sendTextMessage(
    receiveId: string,
    msgType: 'user' | 'chat',
    content: string
  ): Promise<void> {
    const token = await this.getAccessToken();
    
    await fetch(
      `https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=${msgType}`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          receive_id: receiveId,
          msg_type: 'text',
          content: JSON.stringify({ text: content }),
        }),
      }
    );
  }
  
  // 发送卡片消息
  async sendCardMessage(
    receiveId: string,
    card: FeishuCard
  ): Promise<void> {
    const token = await this.getAccessToken();
    
    await fetch(
      `https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          receive_id: receiveId,
          msg_type: 'interactive',
          card: card,
        }),
      }
    );
  }
  
  // 创建云文档
  async createDoc(title: string, content: string): Promise<string> {
    const token = await this.getAccessToken();
    
    const response = await fetch(
      'https://open.feishu.cn/open-apis/docx/v1/documents',
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: title,
        }),
      }
    );
    
    const data = await response.json();
    const docId = data.document.document_id;
    
    // 更新文档内容
    await this.updateDocContent(docId, content);
    
    return docId;
  }
}
```

#### 3. 工作流动作集成

```typescript
// server/actions/sendFeishuMessage.ts
import { Context } from '@nocobase/actions';

export async function sendFeishuMessage(ctx: Context) {
  const { message, receiveId, msgType } = ctx.action.params;
  
  const feishuService = ctx.app.getService<FeishuService>('feishuService');
  
  await feishuService.sendTextMessage(receiveId, msgType, message);
  
  ctx.body = {
    success: true,
    message: '消息发送成功',
  };
}
```

### 飞书集成场景

#### 场景 1：新闻抓取后自动推送

```yaml
工作流：新闻推送自动化

触发器:
  类型：数据变更
  集合：新闻 (News)
  动作：创建后
  条件：重要性 >= 8

执行步骤:
  1. AI 员工分析新闻
     - 提取关键信息
     - 生成摘要
     - 判断推送对象
  
  2. 构建飞书卡片消息
     模板：
     ┌────────────────────────────────┐
     │ 🔴 重要行业快讯                │
     │                                │
     │ 标题：{news.title}            │
     │ 来源：{news.source}           │
     │ 时间：{news.publishDate}      │
     │                                │
     │ 摘要：{aiSummary}             │
     │                                │
     │ [查看详情] [投资信号]         │
     └────────────────────────────────┘
  
  3. 发送飞书消息
     - 目标群：光储投资研究群
     - @相关人员
  
  4. 记录推送日志
```

#### 场景 2：日报自动发送

```yaml
工作流：日报自动生成与推送

触发器:
  类型：定时触发
  Cron: 0 18 * * * (每天 18:00)

执行步骤:
  1. 查询今日数据
     - 今日新闻数量
     - 重要新闻列表
     - 系统更新日志
  
  2. AI 生成日报内容
     - 汇总今日工作
     - 提炼关键洞察
     - 生成明日计划建议
  
  3. 创建飞书云文档
     - 标题：光储龙虾日报 YYYY-MM-DD
     - 内容：格式化日报
  
  4. 发送飞书消息
     - 目标群：研发团队群
     - 附带文档链接
  
  5. 归档日报
```

#### 场景 3：审批流程集成

```yaml
工作流：投资审批流程

触发器:
  类型：数据变更
  集合：投资项目
  动作：状态变更为"待审批"

执行步骤:
  1. 获取审批人信息
     - 根据投资金额确定审批级别
  
  2. 发送飞书审批卡片
     - 项目信息
     - 投资金额
     - 风险评估
     - [同意] [拒绝] [查看详情] 按钮
  
  3. 等待用户操作
     - 接收飞书回调
  
  4. 更新项目状态
     - 同意 → "已批准"
     - 拒绝 → "已拒绝"
  
  5. 通知申请人
```

---

## 📢 自媒体矩阵打通方案

### 目标平台

| 平台 | 类型 | 集成方式 |
|------|------|----------|
| **微信公众号** | 图文推送 | 微信开放平台 API |
| **知乎** | 文章/回答 | 知乎 API / 自动化 |
| **LinkedIn** | 专业动态 | LinkedIn API |
| **Twitter/X** | 短内容 | Twitter API v2 |
| **小红书** | 图文笔记 | 自动化/第三方 |
| **今日头条** | 文章 | 头条开放平台 |

### 集成架构

```
┌─────────────────────────────────────────────────────────────┐
│                    NocoBase 内容管理中台                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐                                          │
│  │  内容创作    │                                          │
│  │  (AI 辅助)   │                                          │
│  └──────┬───────┘                                          │
│         ↓                                                   │
│  ┌──────────────┐                                          │
│  │  内容审核    │                                          │
│  │  (人工/AI)   │                                          │
│  └──────┬───────┘                                          │
│         ↓                                                   │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │  微信公众号  │    │   LinkedIn   │    │   Twitter    │ │
│  │   插件       │    │   插件       │    │   插件       │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│         ↓                    ↓                    ↓         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              统一发布工作流                           │  │
│  │  • 一键多发    • 定时发布    • 数据回传              │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 内容数据模型

```typescript
// 内容数据模型
interface Content {
  // 基础信息
  id: string;
  title: string;
  content: string;
  coverImage?: string;
  tags: string[];
  category: string;
  
  // AI 辅助
  aiGenerated: boolean;
  aiModel: string;
  aiPrompt: string;
  aiRevisions: number;
  
  // 多渠道发布
  channels: {
    wechat?: {
      status: 'draft' | 'pending' | 'published' | 'failed';
      articleId?: string;
      publishedAt?: Date;
      views?: number;
      likes?: number;
    };
    linkedin?: {
      status: 'draft' | 'pending' | 'published' | 'failed';
      postId?: string;
      publishedAt?: Date;
      impressions?: number;
      likes?: number;
      comments?: number;
    };
    twitter?: {
      status: 'draft' | 'pending' | 'published' | 'failed';
      tweetId?: string;
      publishedAt?: Date;
      impressions?: number;
      retweets?: number;
      likes?: number;
    };
    zhihu?: {
      status: 'draft' | 'pending' | 'published' | 'failed';
      articleId?: string;
      publishedAt?: Date;
      views?: number;
      upvotes?: number;
    };
  };
  
  // 数据分析
  analytics: {
    totalViews: number;
    totalLikes: number;
    totalShares: number;
    totalComments: number;
    engagementRate: number;
  };
  
  // 发布计划
  schedule: {
    enabled: boolean;
    publishAt: Date;
    timezone: string;
  };
}
```

### 微信公众号集成

```typescript
// plugin-wechat-official-account
// server/services/WechatService.ts

export class WechatService {
  private appId: string;
  private appSecret: string;
  private accessToken: string;
  
  // 获取访问令牌
  async getAccessToken(): Promise<string> {
    const response = await fetch(
      `https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=${this.appId}&secret=${this.appSecret}`
    );
    const data = await response.json();
    this.accessToken = data.access_token;
    return this.accessToken;
  }
  
  // 创建草稿
  async createDraft(article: WechatArticle): Promise<string> {
    const token = await this.getAccessToken();
    
    const response = await fetch(
      `https://api.weixin.qq.com/cgi-bin/draft/add?access_token=${token}`,
      {
        method: 'POST',
        body: JSON.stringify({
          articles: [{
            title: article.title,
            author: article.author,
            digest: article.summary,
            content: article.content,
            thumb_media_id: article.coverMediaId,
          }],
        }),
      }
    );
    
    const data = await response.json();
    return data.media_id;
  }
  
  // 发布文章
  async publish(mediaId: string): Promise<string> {
    const token = await this.getAccessToken();
    
    const response = await fetch(
      `https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token=${token}`,
      {
        method: 'POST',
        body: JSON.stringify({ media_id: mediaId }),
      }
    );
    
    const data = await response.json();
    return data.publish_id;
  }
}
```

### 自媒体内容生成工作流

```yaml
工作流：行业分析文章自动生成与发布

触发器:
  类型：定时触发
  Cron: 0 10 * * 1,3,5 (每周一三五 10:00)

执行步骤:
  1. 数据聚合
     - 查询本周重要新闻（重要性 >= 7）
     - 统计行业数据变化
     - 收集投资事件
  
  2. AI 生成文章
     角色：行业分析师
     提示词：|
       基于以下数据生成一篇行业分析文章：
       - 新闻：{newsList}
       - 数据：{marketData}
       - 趋势：{trendAnalysis}
       
       要求：
       - 标题吸引人，包含关键词
       - 结构清晰：摘要 - 正文 - 总结
       - 数据支撑观点
       - 字数 2000-3000
       - 适合微信公众号风格
  
  3. 人工审核
     - 创建审核任务
     - 发送飞书通知给编辑
     - 等待审核通过
  
  4. 多平台发布
     - 微信公众号（完整版）
     - LinkedIn（英文摘要版）
     - Twitter（要点 Thread）
     - 知乎（专业讨论版）
  
  5. 数据追踪
     - 定时获取各平台阅读/互动数据
     - 更新内容分析报表
```

### 一键多发功能

```typescript
// 一键多发服务
class MultiPlatformPublisher {
  async publish(content: Content, platforms: string[]) {
    const results = [];
    
    for (const platform of platforms) {
      try {
        switch (platform) {
          case 'wechat':
            const wechatService = this.app.getService('wechatService');
            const draftId = await wechatService.createDraft(content);
            results.push({ platform: 'wechat', status: 'success', draftId });
            break;
            
          case 'linkedin':
            const linkedinService = this.app.getService('linkedinService');
            const postId = await linkedinService.createPost(content);
            results.push({ platform: 'linkedin', status: 'success', postId });
            break;
            
          case 'twitter':
            const twitterService = this.app.getService('twitterService');
            const thread = await twitterService.createThread(content);
            results.push({ platform: 'twitter', status: 'success', threadId: thread.id });
            break;
        }
      } catch (error) {
        results.push({ platform, status: 'failed', error: error.message });
      }
    }
    
    return results;
  }
}
```

---

## 🏗️ 完整集成架构设计

### 系统整体架构

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            用户交互层                                    │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │  Web 界面 │  │  飞书    │  │  移动端  │  │  API     │  │  Webhook │ │
│  │          │  │  工作区  │  │  App     │  │  调用    │  │  触发    │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                         NocoBase 核心平台                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                        AI 员工系统                                 │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │ │
│  │  │ 行业分析 │  │ 数据科学 │  │ 内容创作 │  │ 多语言   │         │ │
│  │  │ 师       │  │ 家       │  │ 助手     │  │ 翻译官   │         │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                    │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                        工作流引擎                                  │ │
│  │  • 新闻抓取流程  • 内容发布流程  • 通知推送流程  • 审批流程      │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                    │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                        插件系统                                    │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │ │
│  │  │ 飞书集成 │  │ 微信集成 │  │ LinkedIn │  │ Twitter  │         │ │
│  │  │ 插件     │  │ 插件     │  │ 插件     │  │ 插件     │         │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                           数据层                                        │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │PostgreSQL│  │  Redis   │  │  向量    │  │  对象    │              │
│  │  主库    │  │  缓存    │  │  数据库  │  │  存储    │              │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                         外部服务集成                                    │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │  飞书    │  │  微信    │  │ LinkedIn │  │  新闻    │              │
│  │  开放平台│  │  开放平台│  │  API     │  │  源站    │              │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────────────────────┘
```

### 数据流向

```
1. 新闻抓取流程
   新闻源站 → 抓取脚本 → NocoBase 数据库 → AI 分析 → 飞书通知

2. 内容发布流程
   AI 生成内容 → 人工审核 → 多平台发布 → 数据回传 → 分析报表

3. 用户交互流程
   飞书命令 → Webhook → NocoBase 处理 → AI 响应 → 飞书回复
```

---

## 📅 实施路线图

### 第一阶段：基础搭建（2-3 周）

**Week 1-2: NocoBase 部署与配置**
- [ ] Docker 部署 NocoBase 2.0
- [ ] 配置数据模型（新闻/公司/项目/内容）
- [ ] 导入现有数据
- [ ] 配置 AI 提供商（Qwen/Claude）

**Week 3: 飞书基础集成**
- [ ] 创建飞书开放平台应用
- [ ] 开发飞书消息发送插件
- [ ] 配置工作流动作
- [ ] 测试消息推送

### 第二阶段：AI 员工上线（3-4 周）

**Week 4-5: AI 员工开发**
- [ ] 配置行业分析师 AI 员工
- [ ] 配置内容创作助手 AI 员工
- [ ] 配置多语言翻译官 AI 员工
- [ ] 测试 AI 调用流程

**Week 6-7: 工作流编排**
- [ ] 新闻抓取自动化工作流
- [ ] 日报自动生成工作流
- [ ] 飞书通知推送工作流
- [ ] 测试完整流程

### 第三阶段：自媒体集成（4-5 周）

**Week 8-9: 微信公众号集成**
- [ ] 申请微信开放平台账号
- [ ] 开发微信公众号插件
- [ ] 实现草稿创建和发布
- [ ] 测试发布流程

**Week 10-12: 多平台扩展**
- [ ] LinkedIn API 集成
- [ ] Twitter API 集成
- [ ] 一键多发功能
- [ ] 数据回传与分析

### 第四阶段：优化完善（持续）

- [ ] 性能优化
- [ ] 用户体验优化
- [ ] 数据分析报表
- [ ] 监控告警系统

---

## 💡 关键代码示例

### 飞书 Webhook 接收

```typescript
// server/actions/feishu-webhook.ts
export async function handleFeishuWebhook(ctx: Context) {
  const { header, event } = ctx.request.body;
  
  // 验证签名
  const isValid = verifyFeishuSignature(header, ctx.request.body);
  if (!isValid) {
    ctx.status = 401;
    ctx.body = { error: 'Invalid signature' };
    return;
  }
  
  // 处理不同类型事件
  switch (event.type) {
    case 'message.receive_v1':
      await handleMessageReceive(event);
      break;
    case 'approval.instance':
      await handleApprovalEvent(event);
      break;
  }
  
  ctx.body = { success: true };
}

async function handleMessageReceive(event: any) {
  const { message } = event;
  
  // 调用 AI 员工处理消息
  const aiService = app.getService('aiService');
  const response = await aiService.processMessage({
    employee: 'assistant',
    input: message.content,
    context: {
      userId: message.sender_id,
      chatId: message.chat_id,
    },
  });
  
  // 回复消息
  const feishuService = app.getService('feishuService');
  await feishuService.sendTextMessage(
    message.chat_id,
    'chat',
    response.text
  );
}
```

### AI 员工调用飞书 API

```typescript
// AI 员工工具定义
const feishuTool = {
  name: 'send_feishu_message',
  description: 'Send a message to Feishu chat or user',
  parameters: {
    type: 'object',
    properties: {
      receiveId: { type: 'string', description: '接收者 ID' },
      msgType: { type: 'string', enum: ['user', 'chat'] },
      content: { type: 'string', description: '消息内容' },
    },
    required: ['receiveId', 'msgType', 'content'],
  },
  execute: async (params: any) => {
    const feishuService = app.getService('feishuService');
    await feishuService.sendTextMessage(
      params.receiveId,
      params.msgType,
      params.content
    );
    return { success: true };
  },
};

// AI 员工配置
const industryAnalyst = {
  name: '行业分析师',
  role: 'analyst',
  skills: ['news_analysis', 'trend_identification'],
  tools: [feishuTool],
  systemPrompt: `你是一名专业的光伏储能行业分析师。
你的职责是：
1. 分析新闻内容，提取关键信息
2. 识别投资信号（利好/利空/中性）
3. 生成简洁的分析报告
4. 必要时通过飞书通知相关人员`,
};
```

---

## 📊 成本估算

| 项目 | 费用 | 说明 |
|------|------|------|
| **NocoBase** | ~$2,000/年 | 商业插件一次性付费 |
| **飞书** | 免费 | 基础功能免费 |
| **微信公众号** | 免费 | 订阅号免费 |
| **LinkedIn API** | 免费 | 基础 API 免费 |
| **Twitter API** | $100/月 | Basic 套餐 |
| **AI API** | ~$500/月 | Qwen/Claude 调用 |
| **服务器** | ~$50/月 | 2 核 4G 云服务器 |
| **合计** | **~$10,000/年** | 首年投入 |

---

## 📞 资源链接

- **NocoBase GitHub:** https://github.com/nocobase/nocobase
- **NocoBase 文档:** https://docs.nocobase.com
- **飞书开放平台:** https://open.feishu.cn
- **微信开放平台:** https://open.weixin.qq.com
- **LinkedIn API:** https://learn.microsoft.com/en-us/linkedin/
- **Twitter API:** https://developer.twitter.com/

---

**制定人：** Javis  
**审核人：** Terry Wu  
**更新日期：** 2026-03-13
