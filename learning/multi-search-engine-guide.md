# Multi Search Engine 学习指南

## 📚 核心概念

### 什么是 Multi Search Engine（元搜索引擎）

**元搜索引擎（Metasearch Engine）** 是一种搜索架构，它不维护自己的索引，而是将用户查询发送到多个底层搜索引擎，然后合并和融合结果返回给用户。

---

## 🏗️ 架构设计

### 核心组件

```
┌─────────────────────────────────────────────────────────┐
│                    用户查询输入                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   查询处理器                            │
│  - 查询解析                                              │
│  - 查询转换/优化                                         │
│  - 查询分发                                              │
└────┬──────────────┬──────────────┬─────────────────────┘
     │              │              │
     ▼              ▼              ▼
┌─────────┐   ┌─────────┐   ┌─────────┐
│ Google  │   │ Bing    │   │ DuckDuck │
│  API    │   │  API    │   │   Go     │
└────┬────┘   └────┬────┘   └────┬────┘
     │              │              │
     └──────────────┴──────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│                  结果融合引擎                           │
│  - 结果去重                                              │
│  - 排名融合                                              │
│  - 相关性评分                                            │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                    最终结果返回                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 关键技术

### 1. 查询分发策略

```python
class QueryDispatcher:
    """查询分发器"""
    
    def __init__(self, engines):
        self.engines = engines  # ['google', 'bing', 'duckduckgo']
    
    def dispatch(self, query):
        """将查询发送到所有引擎"""
        results = {}
        for engine in self.engines:
            # 并行发送查询
            results[engine] = self._query_engine(engine, query)
        return results
    
    def _query_engine(self, engine, query):
        """调用单个搜索引擎 API"""
        # 实现具体的 API 调用逻辑
        pass
```

### 2. 结果融合算法

#### A. 加权位置融合 (Weighted Position Fusion)

```python
def weighted_position_fusion(results, weights=None):
    """
    基于位置的加权融合
    
    Args:
        results: dict {engine: [(url, title, rank), ...]}
        weights: dict {engine: weight}
    
    Returns:
        融合后的排序列表
    """
    if weights is None:
        weights = {'google': 0.5, 'bing': 0.3, 'duckduckgo': 0.2}
    
    # 收集所有 URL
    all_urls = {}
    for engine, engine_results in results.items():
        for rank, (url, title, _) in enumerate(engine_results, 1):
            if url not in all_urls:
                all_urls[url] = {'title': title, 'score': 0}
            # 排名越靠前，分数越高
            score = weights.get(engine, 0.33) * (1.0 / rank)
            all_urls[url]['score'] += score
    
    # 按分数排序
    sorted_results = sorted(
        all_urls.items(),
        key=lambda x: x[1]['score'],
        reverse=True
    )
    
    return [(url, data['title'], data['score']) for url, data in sorted_results]
```

#### B. Borda Count 融合

```python
def borda_count_fusion(results):
    """
    Borda Count 排序融合算法
    
    每个结果根据排名获得分数，最后汇总
    """
    n_engines = len(results)
    scores = {}
    
    for engine, engine_results in results.items():
        n_results = len(engine_results)
        for rank, (url, title, _) in enumerate(engine_results):
            if url not in scores:
                scores[url] = {'title': title, 'score': 0}
            # Borda 分数：排名越靠前分数越高
            scores[url]['score'] += n_results - rank
    
    # 排序
    sorted_results = sorted(
        scores.items(),
        key=lambda x: x[1]['score'],
        reverse=True
    )
    
    return sorted_results
```

#### C. Reciprocal Rank Fusion (RRF)

```python
def reciprocal_rank_fusion(results, k=60):
    """
    倒数排名融合 (Reciprocal Rank Fusion)
    
    经典的信息检索融合算法
    Score = Σ 1 / (k + rank)
    """
    scores = {}
    
    for engine, engine_results in results.items():
        for rank, (url, title, _) in enumerate(engine_results, 1):
            if url not in scores:
                scores[url] = {'title': title, 'score': 0}
            # RRF 公式
            scores[url]['score'] += 1.0 / (k + rank)
    
    # 排序
    sorted_results = sorted(
        scores.items(),
        key=lambda x: x[1]['score'],
        reverse=True
    )
    
    return sorted_results
```

---

### 3. 结果去重

```python
def deduplicate_results(results, threshold=0.9):
    """
    基于 URL 和内容的结果去重
    
    Args:
        results: 融合后的结果列表
        threshold: 相似度阈值
    
    Returns:
        去重后的结果
    """
    from urllib.parse import urlparse
    from difflib import SequenceMatcher
    
    unique_results = []
    seen_urls = set()
    
    for url, title, score in results:
        # 标准化 URL
        parsed = urlparse(url)
        normalized_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        
        # 检查是否已存在
        if normalized_url in seen_urls:
            continue
        
        # 检查标题相似度
        is_duplicate = False
        for seen_url, seen_title, _ in unique_results:
            similarity = SequenceMatcher(None, title, seen_title).ratio()
            if similarity > threshold:
                is_duplicate = True
                break
        
        if not is_duplicate:
            unique_results.append((url, title, score))
            seen_urls.add(normalized_url)
    
    return unique_results
```

---

## 🎯 排名优化策略

### 1. 基于用户画像的排名 (User Profile Based)

```python
class UserProfileRanker:
    """基于用户画像的排名优化"""
    
    def __init__(self):
        self.user_profiles = {}  # user_id -> {interests: [...], history: [...]}
    
    def personalize_ranking(self, results, user_id):
        """根据用户兴趣调整排名"""
        if user_id not in self.user_profiles:
            return results  # 无画像，返回原结果
        
        profile = self.user_profiles[user_id]
        personalized = []
        
        for url, title, score in results:
            # 计算与用户兴趣的匹配度
            interest_score = self._calculate_interest_match(
                title, profile['interests']
            )
            # 加权调整
            new_score = score * (1 + interest_score * 0.5)
            personalized.append((url, title, new_score))
        
        # 重新排序
        return sorted(personalized, key=lambda x: x[2], reverse=True)
    
    def _calculate_interest_match(self, text, interests):
        """计算文本与用户兴趣的匹配度"""
        text_lower = text.lower()
        matches = sum(1 for interest in interests if interest.lower() in text_lower)
        return matches / max(len(interests), 1)
```

### 2. 机器学习排名 (Learning to Rank)

```python
from sklearn.ensemble import GradientBoostingRegressor
import numpy as np

class LearningToRank:
    """基于机器学习的排名融合"""
    
    def __init__(self):
        self.model = GradientBoostingRegressor()
        self.is_trained = False
    
    def extract_features(self, results):
        """提取排名特征"""
        features = []
        for url, title, score in results:
            feature_vector = [
                score,  # 原始分数
                len(title),  # 标题长度
                title.lower().count('official'),  # 是否官方
                url.count('.edu') + url.count('.gov'),  # 权威域名
                # 可以添加更多特征...
            ]
            features.append(feature_vector)
        return np.array(features)
    
    def train(self, training_data, labels):
        """训练排名模型"""
        X = self.extract_features(training_data)
        y = np.array(labels)  # 人工标注的相关性分数
        self.model.fit(X, y)
        self.is_trained = True
    
    def predict_ranking(self, results):
        """预测排名"""
        if not self.is_trained:
            return results
        
        X = self.extract_features(results)
        predictions = self.model.predict(X)
        
        # 按预测分数排序
        ranked = sorted(
            zip(results, predictions),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [(r[0], r[1], pred) for r, pred in ranked]
```

---

## 📊 性能优化

### 1. 并行查询

```python
import asyncio
import aiohttp

class AsyncMultiSearch:
    """异步并行搜索"""
    
    def __init__(self, engines):
        self.engines = engines
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
    
    async def search_all(self, query):
        """并行搜索所有引擎"""
        tasks = [self._search_engine(engine, query) for engine in self.engines]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 过滤异常
        return {
            engine: result 
            for engine, result in zip(self.engines, results)
            if not isinstance(result, Exception)
        }
    
    async def _search_engine(self, engine, query):
        """搜索单个引擎"""
        # 实现具体的 API 调用
        async with self.session.get(api_url, params={'q': query}) as response:
            return await response.json()
```

### 2. 缓存机制

```python
from functools import lru_cache
import hashlib
import time

class SearchCache:
    """搜索结果缓存"""
    
    def __init__(self, ttl=3600):  # 1 小时过期
        self.cache = {}
        self.ttl = ttl
    
    def _generate_key(self, query, engines):
        """生成缓存键"""
        key_str = f"{query}:{','.join(sorted(engines))}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, query, engines):
        """获取缓存"""
        key = self._generate_key(query, engines)
        if key in self.cache:
            result, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return result
            else:
                del self.cache[key]
        return None
    
    def set(self, query, engines, results):
        """设置缓存"""
        key = self._generate_key(query, engines)
        self.cache[key] = (results, time.time())
```

---

## 🔍 实际应用案例

### 1. 学术搜索元引擎

```python
class AcademicMetaSearch:
    """学术搜索元引擎"""
    
    def __init__(self):
        self.engines = [
            'google_scholar',
            'semantic_scholar',
            'arxiv',
            'pubmed'
        ]
    
    def search(self, query, filters=None):
        """搜索学术论文"""
        # 1. 并行查询所有引擎
        results = self._query_all_engines(query, filters)
        
        # 2. 融合结果（使用 RRF）
        fused = reciprocal_rank_fusion(results)
        
        # 3. 去重
        deduped = deduplicate_results(fused)
        
        # 4. 按引用次数重新排序
        reranked = self._rank_by_citations(deduped)
        
        return reranked[:20]  # 返回前 20 条
```

### 2. 电商价格比较引擎

```python
class PriceComparisonEngine:
    """电商价格比较元引擎"""
    
    def __init__(self):
        self.engines = [
            'amazon',
            'ebay',
            'aliexpress',
            'shopify'
        ]
    
    def search_product(self, product_name):
        """搜索商品价格"""
        results = self._query_all_engines(product_name)
        
        # 融合时考虑价格因素
        fused = self._price_aware_fusion(results)
        
        # 按价格排序
        sorted_by_price = sorted(fused, key=lambda x: x['price'])
        
        return sorted_by_price
```

---

## 📈 评估指标

### 1. 搜索质量指标

- **Precision@K**: 前 K 个结果的相关性比例
- **NDCG@K**: 归一化折损累计增益
- **MRR**: 平均倒数排名 (Mean Reciprocal Rank)

### 2. 性能指标

- **响应时间**: 从查询到返回结果的时间
- **吞吐量**: 每秒处理的查询数
- **覆盖率**: 成功返回结果的查询比例

---

## 🛠️ 实现建议

### 最佳实践

1. **使用异步 IO**: 并行查询多个引擎
2. **实现缓存**: 减少重复查询
3. **错误处理**: 优雅处理引擎失败
4. **限流**: 遵守各引擎的 API 限制
5. **监控**: 跟踪各引擎的性能和质量

### 技术栈推荐

- **后端**: Python (FastAPI/Flask) + asyncio
- **缓存**: Redis
- **队列**: Celery + Redis/RabbitMQ
- **数据库**: PostgreSQL (存储用户画像和历史)
- **监控**: Prometheus + Grafana

---

## 📚 参考资源

1. **论文**: "Combinatorial Fusion Analysis for Meta Search"
2. **论文**: "Effective Ranking Fusion Methods for Personalized Metasearch"
3. **书籍**: "Search Engines: Information Retrieval in Practice"
4. **开源项目**: 
   - [SearX](https://github.com/searx/searx) - 开源元搜索引擎
   - [Metacrawler](https://github.com/metacrawler) - 元爬虫框架

---

*学习时间：2026-03-06*
*来源：EvoMap 技能学习*
