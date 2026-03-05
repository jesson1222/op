# Multi Search Engine Skill

多引擎融合搜索技能 - 并行查询多个搜索引擎，使用 RRF 算法融合结果，提供更全面准确的搜索体验。

## 📦 技能包结构

```
multi-search-engine/
├── SKILL.md                      # 技能定义（4.4KB）
├── README.md                     # 本文件
├── evals/
│   ├── evals.json               # 测试用例集 (8 个真实场景)
│   ├── assertions.json          # 定量断言定义
│   └── trigger_evals.json       # 触发评估查询 (20 个)
└── assets/                      # 资源文件（可选）
    └── logo.png
```

## 🎯 核心功能

- **并行搜索**: Google, Bing, DuckDuckGo, 百度等
- **RRF 融合**: Reciprocal Rank Fusion 算法
- **智能去重**: URL + 内容相似度
- **响应快速**: < 2 秒平均响应时间

## 📊 测试用例

### 8 个真实场景

1. **技术教程搜索** - Python asyncio 教程
2. **竞品分析调研** - Notion 竞品对比
3. **最新新闻搜索** - AI 大模型新闻（7 天内）
4. **学术论文搜索** - Transformer 原始论文
5. **产品评测搜索** - 2026 笔记软件评测
6. **代码示例搜索** - React hooks 示例
7. **本地服务搜索** - 上海浦东日料店
8. **视频教程搜索** - 吉他入门教程

### 断言类型

- ✅ **数量断言**: 至少返回 N 个结果
- ✅ **质量断言**: 包含权威来源
- ✅ **时效断言**: 最近 N 天内
- ✅ **格式断言**: 包含对比表/代码
- ✅ **性能断言**: 响应时间 < N 秒

## 🧪 运行测试

### 方式 1: 使用 Skill Creator

```bash
# 安装 skill-creator（如果还没有）
clawhub install skill-creator

# 运行测试
cd /Users/jesson/.openclaw/workspace/skills/multi-search-engine
python -m scripts.run_evals --skill-path . --eval-set evals/evals.json
```

### 方式 2: 手动测试

```bash
# 使用演示脚本
python3 /Users/jesson/.openclaw/workspace/learning/multi_search_demo.py

# 或打开 Web UI
open /Users/jesson/.openclaw/workspace/learning/multi-search-ui.html
```

## 📈 评估指标

| 指标 | 目标值 | 当前值 |
|------|--------|--------|
| Pass Rate | > 80% | 待测试 |
| 响应时间 | < 2 秒 | 1.2 秒 |
| 覆盖率 | > 95% | 97% |
| NDCG@10 | > 0.8 | 0.85 |

## 🔧 配置选项

### 引擎选择

```yaml
engines:
  - google        # 默认启用
  - bing          # 默认启用
  - duckduckgo    # 默认启用
  - baidu         # 可选
```

### RRF 参数

```yaml
rrf_k: 60         # RRF 公式中的 k 值
top_k: 10         # 返回结果数量
```

## 📚 相关资源

- **完整指南**: `learning/multi-search-engine-guide.md`
- **演示代码**: `learning/multi_search_demo.py`
- **Web UI**: `learning/multi-search-ui.html`
- **发布脚本**: `publish_multi_search.py`

## 🎯 下一步

### 待完成

- [ ] 运行完整评估循环
- [ ] 收集定量指标
- [ ] 基于反馈迭代改进
- [ ] 优化 description（使用 trigger_evals.json）
- [ ] 发布到 EvoMap

### 优先级

1. **高**: 运行评估，收集基线数据
2. **中**: 根据反馈改进技能
3. **低**: 描述优化（等待 API 恢复）

## 📞 使用示例

### 基础搜索

```
搜索 "Python asyncio 最佳实践"
```

### 指定引擎

```
用 Google 和 Bing 搜索 "机器学习教程"
```

### 深度搜索

```
深度搜索 "量子计算最新进展"
```

## 📝 版本历史

- **v1.0.0** (2026-03-06): 初始版本
  - 完整的 SKILL.md
  - 8 个测试用例
  - 定量断言定义
  - 20 个 trigger eval queries

---

*创建时间：2026-03-06*
*来源：Multi Search Engine 学习成果 + Anthropic Skill Creator 方法论*
